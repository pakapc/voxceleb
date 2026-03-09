import os
import glob
import subprocess
from tqdm import tqdm
from argparse import ArgumentParser
'''
python preprocess_wav_vctk.py \
--root_path example_data \
--output_path example_data_wav
'''
parser = ArgumentParser()

parser.add_argument("--root_path", required=True)
parser.add_argument("--output_path", required=True)

parser.add_argument("--delete_videos", action="store_true")
parser.set_defaults(delete_videos=False)


def make_path(path):
    os.makedirs(path, exist_ok=True)


def convert_to_wav(input_video, output_wav):

    cmd = [
        "ffmpeg",
        "-loglevel", "quiet",
        "-i", input_video,
        "-ac", "1",
        "-ar", "16000",
        "-vn",
        output_wav,
        "-y"
    ]

    subprocess.run(cmd)


if __name__ == "__main__":

    args = parser.parse_args()

    root_path = args.root_path
    output_root = args.output_path

    make_path(output_root)

    speakers = sorted(os.listdir(root_path))

    print(f"Dataset has {len(speakers)} speakers")

    for speaker in speakers:

        speaker_path = os.path.join(root_path, speaker)

        if not os.path.isdir(speaker_path):
            continue

        print(f"\nProcessing speaker {speaker}")

        output_speaker = os.path.join(output_root, speaker)
        make_path(output_speaker)

        videos = glob.glob(os.path.join(speaker_path, "*"))

        for video_folder in videos:

            video_id = os.path.basename(video_folder)

            chunk_path = os.path.join(video_folder, "chunk_videos")

            if not os.path.exists(chunk_path):
                continue

            mp4_files = glob.glob(os.path.join(chunk_path, "*.mp4"))

            for mp4 in tqdm(mp4_files, leave=False):

                chunk_name = os.path.splitext(os.path.basename(mp4))[0]

                wav_name = f"{video_id}_{chunk_name}.wav"

                output_wav = os.path.join(output_speaker, wav_name)

                convert_to_wav(mp4, output_wav)

                if args.delete_videos:
                    os.remove(mp4)

    print("\nDone.")