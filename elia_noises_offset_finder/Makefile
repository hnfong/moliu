all: offsets.txt shots.done

offsets.txt: elia_noise_finder.py
	uv run python elia_noise_finder.py --needle aftersound.wav --needle2 aftersound2.wav --haystack making\ interesting\ \'noises\'\ 【the\ voice\ mimicry\ show\ 】\ \[OiUhDlThctE\].mp4 > offsets.txt

shots.done: offsets.txt grab_shots_from_offsets.py
	uv run python grab_shots_from_offsets.py
	touch shots.done
