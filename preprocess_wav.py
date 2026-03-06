import os
import glob
import subprocess
from argparse import ArgumentParser
from tqdm import tqdm

# -----------------------------
# local replacement for make_path
# -----------------------------
def make_path(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


"""
VoxCeleb preprocessing
Convert mp4 chunk videos into wav files using ffmpeg

Output format:
- mono channel
- 16kHz sampling rate

Equivalent to:
ffmpeg -i input.mp4 -ac 1 -ar 16000 output.wav
"""


'''
python preprocess_wav.py \
--root_path /Users/pakap/Documents/Senior/Code/voxceleb/example_data \
--dataset vox1

'''

parser = ArgumentParser()
parser.add_argument("--root_path", required=True, help="Path to VoxCeleb videos")
# parser.add_argument("--metadata_path", required=True, help="Path to metadata")
parser.add_argument("--dataset", required=True, type=str, choices=("vox1", "vox2"))

parser.add_argument("--delete_videos", action="store_true")
parser.set_defaults(delete_videos=False)

parser.add_argument("--delete_or_frames", action="store_true")
parser.set_defaults(delete_or_frames=False)


# -----------------------------
# convert mp4 -> wav
# -----------------------------
def convert_to_wav(input_video, output_wav):

    cmd = [
        "ffmpeg",
        "-i", input_video,
        "-ac", "1",
        "-ar", "16000",
        output_wav,
        "-y"
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# -----------------------------
# extract wav files
# -----------------------------
def extract_audio(videos_tmp, output_path):

    print("1. Extract wav from mp4")

    make_path(output_path)

    for video in tqdm(videos_tmp):

        base_name = os.path.splitext(os.path.basename(video))[0]
        output_wav = os.path.join(output_path, base_name + ".wav")
        
        try:
            convert_to_wav(video, output_wav)
        except Exception as e:
            print(f"Error converting {video}: {e}")


# -----------------------------
# main
# -----------------------------
if __name__ == "__main__":

    args = parser.parse_args()

    root_path = args.root_path
    # metadata_path = args.metadata_path
    dataset = args.dataset
    delete_videos = args.delete_videos

    if not os.path.exists(root_path):
        print(f"Videos path {root_path} does not exist")
        exit()

    # if not os.path.exists(metadata_path):
    #     print(f"Metadata path {metadata_path} does not exist")
    #     exit()

    ids_path = glob.glob(os.path.join(root_path, "*/"))
    ids_path.sort()

    print(f"Dataset has {len(ids_path)} identities")

    for i, id_path in enumerate(ids_path):

        id_index = os.path.basename(os.path.normpath(id_path))

        videos_path = glob.glob(os.path.join(id_path, "*/"))
        videos_path.sort()

        print("*********************************************************")
        print(f"Identity {i}/{len(ids_path)}")

        for j, video_path in enumerate(videos_path):

            video_id = os.path.basename(os.path.normpath(video_path))

            print(f"{j}/{len(videos_path)} videos")

            output_path_video = os.path.join(root_path, id_index, video_id)
            chunk_path = os.path.join(output_path_video, "chunk_video")

            if not os.path.exists(chunk_path):
                print(f"path {chunk_path} does not exist")
                continue

            videos_tmp = glob.glob(os.path.join(chunk_path, "*.mp4"))
            videos_tmp.sort()

            if len(videos_tmp) == 0:
                print(f"No videos in {chunk_path}")
                continue

            audio_output = os.path.join(output_path_video, "wav")

            extract_audio(videos_tmp, audio_output)

            # optional: delete mp4
            if delete_videos:
                for vid in videos_tmp:
                    os.remove(vid)

        print("*********************************************************")
