import glob
import os
import json
import zipfile
import shutil

def main():
    # create working directory "elia-cute-noises"
    working_dir = "elia-cute-noises"
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    # open manual_annotations.txt, read the timestamps and the titles
    for idx, line in enumerate(open("manual_annotations.txt", "r")):
        # Eg. `01:51:11.093 - Drum can`
        line = line.strip()
        timestamp, title = line.split(" - ", maxsplit=1)
        # Find the corresponding wav file
        wav_file = glob.glob(f"segment-{timestamp}.wav")[0]
        # print(f"Found {wav_file} for {title}")

        # Rename the wav file to the title, eg. Elia-001-Drum can.wav
        new_wav_file = os.path.join(working_dir, f"Elia-{idx + 1:03d}-{title}.wav")
        print(wav_file, new_wav_file)
        shutil.move(wav_file, new_wav_file)

if __name__ == "__main__":
    main()
