# Oshi Lore Extractor

Extract lore from yappings of your (my) oshi. Put youtube stream/video URLs
into stream_urls.txt and run `make`. Dependencies are specified in the
Makefile.

## TODO

- Add more stream urls (this needs to be kinda manual, since I think the
  non-zatsudan streams are probably less info dense - that said maybe we could
  still do it all. Main concern is Youtube banning my IP if I download too many
  vids in a short period of time...)

- Maybe do another LLM run over the first round of extraction to throw away
  superfluous items.

## Errata

- Occasionally mis-identifies the dono messages (read by streamer) as her own
  story.

- Due to limitations of either the prompt or the model or the context size of
  models, when if there is nothing actually interesting to extract (especially
  now that we've segmented the full transcript into smaller blocks), the model
  just extracts trivial-trivia.
