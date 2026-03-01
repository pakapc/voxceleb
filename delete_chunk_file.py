import os
import shutil
from tqdm import tqdm

# =======================
# CONFIGURE HERE
# =======================
INPUT_DIR = r"C:\Users\Student\Downloads\Dataset\Vox1\VoxCeleb1_train_original"
OUTPUT_DIR = r"C:\Users\Student\Downloads\Dataset\Vox1\VoxCeleb1_train"
# =======================


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def process_dataset(input_dir, output_dir):

    print("Scanning dataset...")
    ids = [d for d in os.listdir(input_dir)
           if os.path.isdir(os.path.join(input_dir, d))]
    ids.sort()

    print(f"Found {len(ids)} identities")

    for id_name in tqdm(ids):

        id_input_path = os.path.join(input_dir, id_name)
        id_output_path = os.path.join(output_dir, id_name)
        make_dir(id_output_path)

        # Loop over video folders
        videos = [v for v in os.listdir(id_input_path)
                  if os.path.isdir(os.path.join(id_input_path, v))]

        for video_name in videos:

            video_input_path = os.path.join(id_input_path, video_name)
            video_output_path = os.path.join(id_output_path, video_name)
            make_dir(video_output_path)

            chunk_path = os.path.join(video_input_path, "chunk_video")

            # If chunk_video exists → move its contents up one level
            if os.path.exists(chunk_path):

                files = os.listdir(chunk_path)

                for file in files:
                    src = os.path.join(chunk_path, file)
                    dst = os.path.join(video_output_path, file)

                    if os.path.isfile(src):
                        shutil.copy2(src, dst)

            else:
                # If no chunk_video folder, just copy contents normally
                for file in os.listdir(video_input_path):
                    src = os.path.join(video_input_path, file)
                    dst = os.path.join(video_output_path, file)

                    if os.path.isfile(src):
                        shutil.copy2(src, dst)

    print("Finished restructuring dataset.")


if __name__ == "__main__":

    if not os.path.exists(INPUT_DIR):
        print("Input directory does not exist.")
        exit()

    make_dir(OUTPUT_DIR)

    print("Input :", INPUT_DIR)
    print("Output:", OUTPUT_DIR)

    process_dataset(INPUT_DIR, OUTPUT_DIR)
