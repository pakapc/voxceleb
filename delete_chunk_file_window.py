import os
import shutil
from pathlib import Path
from tqdm import tqdm

INPUT_DIR = Path(r"C:\Users\Student\Downloads\Dataset\Vox1\VoxCeleb1_train_original")
OUTPUT_DIR = Path(r"C:\Users\Student\Downloads\Dataset\Vox1\Voxceleb1_train")

def process_dataset(input_dir, output_dir):
    # Get all ID directories
    ids = [d for d in input_dir.iterdir() if d.is_dir()]
    print(f"Found {len(ids)} identities. Processing...")

    for id_path in tqdm(ids, desc="Processing IDs"):
        # Iterate through video folders (the YouTube IDs)
        for video_folder in id_path.iterdir():
            if not video_folder.is_dir():
                continue
            
            # Define target: OUTPUT/id0001/video_id/
            target_dir = output_dir / id_path.name / video_folder.name
            target_dir.mkdir(parents=True, exist_ok=True)

            # FIX: Use .rglob("*") to find ALL files inside this folder, 
            # no matter how deep they are (handles 'chunk_video', 'video', etc.)
            files_found = list(video_folder.rglob("*"))
            
            for file in files_found:
                # We only want to copy actual files (mp4, wav, etc.), not directories
                if file.is_file():
                    # This flattens the files into the target_dir
                    shutil.copy2(file, target_dir / file.name)

if __name__ == "__main__":
    if not INPUT_DIR.exists():
        print(f"Error: Input directory {INPUT_DIR} does not exist.")
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        process_dataset(INPUT_DIR, OUTPUT_DIR)
        print("\n✅ Finished restructuring dataset.")