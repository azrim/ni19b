# The World in One Day — 19 November 2026

One 1024x1024 front page for a single day of news, submitted to the make.fun
bounty *Sum up 19 November's world news in one image*.

The page carries nine illustrated cover stories and twenty-four short briefs,
grouped by region: a three-way summit in Shenzhen, the Crimean Bridge strike,
Anthropic's record IPO, GTA VI's release, the ICJ ruling on Myanmar, Cyclone
Akvan, COP31 in Antalya, the APEC declaration and the Florida floods, with the
rest of the day in the brief grid. Every story happened, or was first reported,
on Thursday 19 November 2026; claims that are disputed are attributed to a named
source rather than stated as fact, and the DATE CHECK box lists the items left
out because they broke on an earlier day.

## Layout

- Masthead with a calendar block and the date set large.
- Region bar whose segment counts, the story total and the brief total are all
  computed from the story tables, so the page cannot contradict itself.
- Four stat cells, three hero cards, two rows of three cards, a brief grid.
- Everything is drawn from a data table; no text is placed by hand.

## Program contract

`main.py` is standard library only. It copies `poster.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), creating the directory if
needed, and prints the destination, the byte count and the sha256. It refuses to
run if `poster.png` is missing, larger than 1 MiB, or different from the poster
it was committed with. Python 3.13 is the target runtime.

`gen_poster.py` is the offline generator and needs Pillow; `main.py` does not.

## Determinism

No randomness, no clock reads, no network, sorted iteration. Rendering twice
writes byte-identical PNGs, and running `main.py` twice writes byte-identical
`entry.png` files that match `poster.png` exactly.

## License

MIT. See `LICENSE`.
