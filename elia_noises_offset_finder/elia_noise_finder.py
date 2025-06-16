import argparse

import librosa
import numpy as np
from scipy import signal
import json

def find_offset(haystack_file, needle_file, needle_file_2):
    y_haystack, sr_haystack = librosa.load(haystack_file, sr=None)
    y_find, _ = librosa.load(needle_file, sr=sr_haystack)

    c = signal.correlate(y_haystack, y_find, mode='valid', method='fft')
    maxv = np.max(c)
    threshold = maxv * 3 / 4
    peaks, _ = signal.find_peaks(c, height=threshold)
    offsets_and_values = [(peak / sr_haystack, c[peak]) for peak in peaks]


    # It seems Elia changed the volume of the sounds around 2h44m... so we need to recalibrate after this point.
    softer_sound_offset = (2*3600+43*60)
    y_find_2, _ = librosa.load(needle_file_2, sr=sr_haystack)
    c_2 = signal.correlate(y_haystack, y_find_2, mode='valid', method='fft')
    maxv_2 = np.max(c[(softer_sound_offset + 1000) * sr_haystack:]) # There is a weird false positive at some 2:58:xx point, so skipping it as well
    threshold_2 = maxv_2 * 3 / 4
    peaks_2, _ = signal.find_peaks(c[softer_sound_offset * sr_haystack:], height=threshold_2)
    offsets_and_values_2 = [(peak / sr_haystack + softer_sound_offset, c[peak + softer_sound_offset * sr_haystack]) for peak in peaks_2]
    return offsets_and_values + offsets_and_values_2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--needle', metavar='audio file', type=str, help='Find the offset of file')
    parser.add_argument('--needle2', metavar='audio file', type=str, help='Find the offset of file')
    parser.add_argument('--haystack', metavar='audio file', type=str, help='Within file')
    args = parser.parse_args()
    offsets = find_offset(args.haystack, args.needle, args.needle2)
    for offset, val in offsets:
        human_readable = f"{offset // 3600:02.0f}:{(offset % 3600) // 60:02.0f}:{offset % 60:06.3f}"
        print(json.dumps([offset, human_readable, float(val)]))



if __name__ == '__main__':
    main()
