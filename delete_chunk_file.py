import os
import shutil
from pathlib import Path
from tqdm import tqdm

# Update these paths as needed
INPUT_DIR = Path("/Users/pakap/Documents/Senior/Code/voxceleb/example_data")
OUTPUT_DIR = Path("/Users/pakap/Documents/Senior/Code/voxceleb/example_data_wav")

def process_dataset(input_dir, output_dir):
    # Get all ID directories (id0001, id0002, etc.)
    ids = [d for d in input_dir.iterdir() if d.is_dir()]
    print(f"Found {len(ids)} identities. Processing...")

    for id_path in tqdm(ids, desc="Processing IDs"):
        # Iterate through video folders (e.g., 1zcIwhmdeo4)
        for video_path in id_path.iterdir():
            if not video_path.is_dir():
                continue
            
            # Define the target directory: OUTPUT/id0001/1zcIwhmdeo4/
            target_video_dir = output_dir / id_path.name / video_path.name
            target_video_dir.mkdir(parents=True, exist_ok=True)

            # Specifically look for the 'chunk_video' subfolder
            chunk_folder = video_path / "chunk_video"
            
            if chunk_folder.exists() and chunk_folder.is_dir():
                # Grab all files inside chunk_video and move them up to target_video_dir
                for file in chunk_folder.iterdir():
                    if file.is_file():
                        shutil.copy2(file, target_video_dir / file.name)
            else:
                # Fallback: If chunk_video doesn't exist, check if files are already in video_path
                for file in video_path.iterdir():
                    if file.is_file():
                        shutil.copy2(file, target_video_dir / file.name)

if __name__ == "__main__":
    if not INPUT_DIR.exists():
        print(f"Error: Input directory {INPUT_DIR} does not exist.")
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        process_dataset(INPUT_DIR, OUTPUT_DIR)
        print("\n✅ Finished restructuring dataset.")