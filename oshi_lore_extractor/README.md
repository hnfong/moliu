# Oshi Lore Extractor

Extract lore from yappings of your (my) oshi. Put youtube stream/video URLs
into stream_urls.txt and run `make`. Dependencies are specified in the
Makefile.

## Errata

- Occasionally mis-identifies the dono messages (read by streamer) as her own
  story.

- Due to limitations of either the prompt or the model or the context size of
  models, when if there is nothing actually interesting to extract (especially
  now that we've segmented the full transcript into smaller blocks), the model
  just extracts trivial-trivia.
