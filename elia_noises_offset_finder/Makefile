all: offsets.txt preoffsets.txt

offsets.txt: elia_noise_finder.py
	uv run python elia_noise_finder.py --needle aftersound.wav --needle2 aftersound2.wav --haystack making\ interesting\ \'noises\'\ 【the\ voice\ mimicry\ show\ 】\ \[OiUhDlThctE\].mp4 > offsets.txt
	echo "Copy offsets.txt to manual_offsets.txt and remove false positives as needed"
preoffsets.txt:  elia_noise_finder.py
	uv run python elia_noise_finder.py --needle beforesound.wav --needle2 beforesound2.wav --haystack making\ interesting\ \'noises\'\ 【the\ voice\ mimicry\ show\ 】\ \[OiUhDlThctE\].mp4 > preoffsets.txt

annotations.txt: manual_offsets.txt grab_shots_from_offsets.py
	uv run python grab_shots_from_offsets.py
	echo "Copy annotations.txt to manual_annotations.txt and fix them for further processing"

sounds.zip:
	uv run python extract_segments.py
	uv run python putting_everything_together.py
