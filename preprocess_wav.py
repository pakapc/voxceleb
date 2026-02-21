import os
import glob
from tqdm import tqdm
from argparse import ArgumentParser
from pydub import AudioSegment

"""
Convert dataset audio files from .mp (or .mp3/.m4a) to .wav

Arguments:
    root_file:      Path where original dataset is stored
    output_file:    Path where converted wav dataset will be saved

Example:
python preprocess_wav.py --root_file ./dataset_mp --output_file ./dataset_wav


"""

parser = ArgumentParser()
parser.add_argument("--root_file", required=True, help="Path to input dataset")
parser.add_argument("--output_file", required=True, help="Path to output dataset (wav format)")


def make_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def convert_to_wav(input_audio_path, output_audio_path):
    """
    Convert audio file to wav format
    """
    audio = AudioSegment.from_file(input_audio_path)
    audio.export(output_audio_path, format="wav")


def process_dataset(root_file, output_file):

    print("Scanning dataset...")
    ids_path = glob.glob(os.path.join(root_file, "*/"))
    ids_path.sort()

    print("Dataset has {} identities".format(len(ids_path)))

    for i, id_path in enumerate(ids_path):

        id_name = id_path.split("/")[-2]
        print("--------------------------------------------------")
        print("Identity {}/{}: {}".format(i+1, len(ids_path), id_name))

        # Create identity output folder
        output_id_path = os.path.join(output_file, id_name)
        make_path(output_id_path)

        # Find all audio files recursively
        audio_files = glob.glob(os.path.join(id_path, "**", "*.*"), recursive=True)
        audio_files = [f for f in audio_files if f.lower().endswith((".mp", ".mp3", ".m4a"))]

        print("Found {} audio files".format(len(audio_files)))

        for audio_path in tqdm(audio_files):

            relative_path = os.path.relpath(audio_path, id_path)
            relative_dir = os.path.dirname(relative_path)

            output_subdir = os.path.join(output_id_path, relative_dir)
            make_path(output_subdir)

            filename = os.path.splitext(os.path.basename(audio_path))[0] + ".wav"
            output_audio_path = os.path.join(output_subdir, filename)

            try:
                convert_to_wav(audio_path, output_audio_path)
            except Exception as e:
                print("Error converting {}: {}".format(audio_path, e))

    print("Finished converting dataset.")


if __name__ == "__main__":

    args = parser.parse_args()

    root_file = args.root_file
    output_file = args.output_file

    if not os.path.exists(root_file):
        print("Input dataset path does not exist.")
        exit()

    make_path(output_file)

    print("Input path:  {}".format(root_file))
    print("Output path: {}".format(output_file))

    process_dataset(root_file, output_file)
