# Extracting interesting noises from https://www.youtube.com/watch?v=OiUhDlThctE

One-off script to extract interesting noises from Elia Stellaria's stream "making interesting 'noises' 【the voice mimicry show 】"

Note that you really need quite a bit of RAM to run a similarity test on a 4 hour audio.

Grab the media files yourself:

- making interesting 'noises' 【the voice mimicry show 】 [OiUhDlThctE].mp4
  - This is the pure-audio file.
- video.mp4
  - This is the video file for extracting screenshots (frames) from the video. It is so named just to avoid conflicting with the audio file above.

- aftersound\*.wav
  - bunzip2 them.
  - These are the sounds from the game that marks the end of the player's attempt to reproduce the sound. So, before this timestamp is the original sound made by the player. After this timestamp is the score and the replay of the player's sound.

# Requirements

- Any system with sufficient RAM probably works, but if you're not on a Mac you'll probably have to figure out some OCR solution instead of ocrmac in `grab_shots_from_offsets.py`
