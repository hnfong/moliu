# Scripts to generate things
# Dependencies:
# - ask.py from my public-crap repo
# - whisper.cpp (whisper-cli in path)
#   - ffmpeg
# - yt-dlp

DOWNLOADED_VIDEOS := $(shell ls downloads/*.webm)
TRANSCRIPTIONS := $(shell ls downloads/*.webm | sed 's/webm/webm.transcribe.txt/;')
EXTRACTIONS := $(shell ls downloads/*.webm | sed 's/webm/out/; s/downloads/extractions/;' )

all:
	# Dependent, so make them sequential.
	make download_videos
	make transcribe_videos
	make extractions

download_videos: stream_urls.txt download_vids
	./download_vids stream_urls.txt

transcribe_videos: $(TRANSCRIPTIONS)
extractions: $(EXTRACTIONS)

downloads/%.webm.transcribe.txt: downloads/%.webm
	./transcribe $<

extractions/%.out: downloads/%.webm.transcribe.txt
	mkdir -p extractions
	./extract "$<" > "$@.tmp"
	mv -vf "$@.tmp" "$@"

.PHONEY: download_videos transcribe_videos extractions
