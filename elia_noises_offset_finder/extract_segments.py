import numpy as np
import soundfile
import librosa
import functools

@functools.lru_cache(maxsize=128)
def data_length_of_file(file):
    """Get the length of the audio data in seconds."""
    data, sr = librosa.load(file, sr=None)
    return len(data)

@functools.lru_cache(maxsize=128)
def data_load(from_file):
    data, sr = librosa.load(from_file, sr=None)
    return data, sr

# It seems Elia changed the volume of the sounds around 2h44m... so we need to recalibrate after this point.
softer_sound_offset = (2*3600+43*60)

def extract_segment(from_file, start_time, end_time, out_path):
    if start_time < softer_sound_offset:
        prefix_length = data_length_of_file("beforesound.wav")
    else:
        prefix_length = data_length_of_file("beforesound2.wav")

    # Load the entire audio file
    data, sr = data_load(from_file)

    # Convert time to sample indices
    start_sample = int(start_time * sr) + prefix_length
    end_sample = int(end_time * sr)

    # The first half is the game's sound, the second half is Elia's cute noises.
    mid_point = start_sample + (end_sample - start_sample) // 2

    # Extract the segment
    segment = data[mid_point:end_sample]
    print(segment)
    print(segment.shape)
    print(sr)

    # Save the segment
    soundfile.write(out_path, segment, sr, subtype='PCM_24')

if __name__ == "__main__":
    import json

    # Read the offsets in preoffsets.txt
    pre_offsets = []
    for line in open("preoffsets.txt"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        secs, human_readable, _ = json.loads(line)
        pre_offsets.append((secs, human_readable))

    assert sorted(pre_offsets) == pre_offsets, "preoffsets.txt is not sorted"
    import bisect

    # For every non-commented (with r'^#') line in manual_offsets.txt
    for line in open("manual_offsets.txt"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Read jsonl
        secs, human_readable, _ = json.loads(line)

        # Find the time that is just smaller than secs in preoffsets.txt (same jsonl format)
        idx = bisect.bisect_left(pre_offsets, (secs, human_readable))
        assert idx > 0, "No preoffset found for {} in preoffsets.txt".format(human_readable)
        pre_secs, pre_human_readable = pre_offsets[idx - 1]

        print(f"Extracting segment for {human_readable}")

        extract_segment("making interesting 'noises' 【the voice mimicry show 】 [OiUhDlThctE].mp4", pre_secs, secs, "segment-" + human_readable + ".wav")
