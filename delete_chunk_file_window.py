import os
import shutil
from pathlib import Path
from tqdm import tqdm

# --- WINDOWS PATH CONFIGURATION ---
# 1. Use 'r' before the string for raw paths.
# 2. Use Path().resolve() to ensure the script sees the absolute Windows path.
# 3. If paths are very deep, Windows sometimes needs the "\\?\" prefix to bypass the 260-character limit.
INPUT_DIR = Path(r"C:\Users\Student\Downloads\Dataset\Vox1\VoxCeleb1_train_original").resolve()
OUTPUT_DIR = Path(r"C:\Users\Student\Downloads\Dataset\Vox1\Voxceleb1_train").resolve()

def process_dataset(input_dir, output_dir):
    if not input_dir.exists():
        print(f"❌ Error: Input directory not found at {input_dir}")
        return

    # Get all ID directories
    ids = [d for d in input_dir.iterdir() if d.is_dir()]
    print(f"Found {len(ids)} identities. Processing...")

    for id_path in tqdm(ids, desc="Processing IDs"):
        for video_path in id_path.iterdir():
            if not video_path.is_dir():
                continue
            
            # Define target: OUTPUT/id0001/video_id/
            target_video_dir = output_dir / id_path.name / video_path.name
            
            try:
                target_video_dir.mkdir(parents=True, exist_ok=True)

                # Specifically look for 'chunk_video'
                chunk_folder = video_path / "chunk_video"
                
                # Determine which folder to pull files from
                source_folder = chunk_folder if (chunk_folder.exists() and chunk_folder.is_dir()) else video_path
                
                for file in source_folder.iterdir():
                    if file.is_file():
                        # shutil.copy2 preserves metadata (date/time)
                        # We use str() because some Windows environments prefer strings over Path objects for shutil
                        shutil.copy2(str(file), str(target_video_dir / file.name))
            
            except Exception as e:
                print(f"\n⚠️ Error processing {video_path.name}: {e}")

if __name__ == "__main__":
    # Ensure Output exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    process_dataset(INPUT_DIR, OUTPUT_DIR)
    print("\n✅ Finished restructuring dataset.")