# news-image-20261118 — The world in one day: Wednesday 18 November 2026

A newspaper-style front page summing up 18 November 2026 in one image
(1024×1024 PNG). `draw.py` draws it with PIL; `main.ts` copies the held
`entry.png` to the output directory.

## Stories covered (all reported 18 Nov 2026, verified by web search)

- **Lead — The Gulf:** Iranian drones targeted a U.S. radar at Sheikh Isa
  base in Bahrain; U.S. jets hit a missile site on Qeshm Island. Bahrain
  issued an all-clear early Wednesday; Kuwait said its air defences were
  countering drones. (Reuters, 18 Nov 00:16 UTC)
- **Ukraine:** Kyiv says Flamingo missiles destroyed a road span of the
  Kerch Bridge to Crimea for a second day; Russia struck bridges in Kyiv.
- **Diplomacy:** Trump arrives in Manila for Quad talks ahead of a China
  visit, as ASEAN leaders meet in the Philippines.
- **Trade:** Canada and China extend trade deals; Xi meets Carney ahead of
  the APEC summit.
- **Britain:** UK sanctions Israeli settlement firms in a push to protect
  the two-state solution.
- **Weather:** Cyclone Akvan gathers strength in the Bay of Bengal, set to
  turn severe by 19 November.
- **Business:** Nvidia sales jump 103% year on year as Jensen Huang steps
  down as chief executive.
- **In brief:** Dhoni retires from the IPL and becomes Chennai mentor;
  India win a 10th SAFF title, beating Pakistan 2–1 in Dhaka; the U.S.
  loses measles elimination status in its worst outbreak since 1991;
  India condemns the attack on LPG tanker MT Tara Gas in the Strait of
  Hormuz.

## Build

```sh
python3 draw.py        # regenerates entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # test the entrypoint
```
