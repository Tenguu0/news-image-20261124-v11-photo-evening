# The World in One Page — Evening Photo Edition, 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Tenguu0/news-image-20261124-v11-photo-evening/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Tenguu0/news-image-20261124-v11-photo-evening/reward.svg)](https://make.fun/bounty/news-image-20261124)

A make.fun entry for
[news-image-20261124](https://make.fun/bounty/news-image-20261124):
the whole world of Tuesday 24 November 2026 on a single newspaper
front page, as an evening photo edition. A big pictorial lead — a
fighter jet, a Patriot battery and an explosion over a Bahraini
airbase at dusk — then eleven more stories told as a photo essay:
every story is led by a picture that shows what it is about, from
rescuers in a blacked-out Kyiv street to a tennis champion lifting
the trophy in Turin. Dense on purpose: no whitespace wasted, and a
"The Day in Numbers" box fills the last slot.

## How to run

Requirements: Python 3.12 or newer, with Pillow (PIL) installed —
nothing else, and no network access is needed. The program reads the
twelve pictures already committed under `assets/` and typesets the
page from them.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

It writes `out/entry.png` (1024x1024 PNG) and exits 0. If
`MAKEFUN_OUTPUT_DIR` is not set, or any of the twelve pictures is
missing from `assets/`, it prints an error to stderr and exits 2
instead of writing a partial page.

Determinism: the build uses no network, no randomness, and no clock,
so every run produces byte-identical output. Verify it yourself:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/v11-run1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/v11-run2 python3 main.py
sha256sum /tmp/v11-run1/entry.png /tmp/v11-run2/entry.png entry.png
```

All three hashes should match — the committed `entry.png` is the
reference output.

## How it works

`main.py` composites the page from the twelve pictures committed
under `assets/` (AI-generated illustrations, one per story): a
newsprint masthead with the date line, the wide lead panorama with
its headline and deck underneath, then a four-column photo-essay
grid — picture on top of each cell with a place tag, a headline of
up to two lines, and a summary of up to two lines below. The last
slot of the grid is a "The Day in Numbers" box. Every story on the
page is a real event from 24 November 2026, cross-checked in news
sources; claims are hedged as claims ("IRAN CLAIMS", "KYIV CLAIMS").

## The twelve stories

Every story below is a real event reported on 24 November 2026.
Figures were cross-checked against at least two independent reports;
one-sided claims stay labelled as claims on the page rather than
stated as fact.

1. **Bahrain** — Iran's Revolutionary Guard says its missiles and
   drones struck two radars of US Patriot batteries in Bahrain;
   Bahrain says the strike hit a civilian site on Sitra Island,
   wounding two. Sources: AFP, Al Jazeera, Middle East Eye.
2. **Kyiv** — Russian strikes on the Kyiv region killed at least 15
   people over the weekend, and the power grid faces months of repair
   as winter sets in. Sources: UN News, Euronews, Al Jazeera, AFP,
   Reuters.
3. **Antalya** — the COP31 climate talks collapsed without a deal
   after the draft pact left out any mention of fossil fuels.
   Sources: CNN, Le Monde, CNBC Africa.
4. **The Hague** — the International Court of Justice ruled 9–6
   that Myanmar committed genocide against the Rohingya, the first
   time the court has held a state responsible for genocide.
   Sources: Human Rights Watch, CNN, Le Monde, OHCHR.
5. **Shenzhen** — the first ever three-way meeting of Xi, Trump and
   Putin ended without a breakthrough on Ukraine or Iran. Sources:
   RFE/RL, AP.
6. **Turin** — Carlos Alcaraz beat Alexander Zverev 6–2, 7–6 to win
   his first ATP Finals title and a record $5.17M cheque. Sources:
   ATP Tour, BBC, The Times.
7. **Libya** — Kyiv claims a Russian warship was sunk off the
   Libyan coast; Moscow has said nothing about the claim.
8. **Seoul** — South Korea scrambled fighter jets after Russian
   aircraft entered its air defence identification zone.
9. **Java** — a fire at a candy factory killed 24 people, with 34
   more missing as crews fought the blaze.
10. **Colombia** — a car bomb struck the governor's office in Meta
    province; the toll was still feared to rise.
11. **Himalayas** — floods left 4 people dead and around 100
    missing as rivers burst their banks and swamped villages.
12. **Dhaka** — Bangladesh began vaccinating 50 million children
    against typhoid, the world's largest drive of its kind.

Stories 7–12 are wire-reported events from the same news day; the
page hedges the sinking claim (story 7) as Kyiv's claim, not as
established fact.

## Design notes

- Evening photo-edition format: one wide lead panorama (992x250)
  with a one-line headline and a one-line deck, then a dense
  four-column photo-essay grid — picture first, words second.
- The pictures are matched to their stories, not decorative: a
  fighter jet and a burning radar base for Bahrain, rescuers in a
  dark Kyiv street, an empty COP31 hall, the court bench in The
  Hague, three leaders deadlocked in Shenzhen, Alcaraz lifting the
  trophy, and so on. All twelve are AI-generated illustrations
  committed under `assets/`; the footer says so plainly ("Pictures
  are AI-generated illustrations.").
- Density on purpose: the lead plus three grid rows fill the
  1024x1024 page edge to edge, with a 10-pixel gutter between
  columns. The last grid slot is a "The Day in Numbers" box (15
  dead in Kyiv; 24 dead in Java; $5.17M Alcaraz cheque; 50M
  children in the Dhaka drive) instead of blank space.
- Typography: DejaVu Serif Bold (44pt) for the masthead, DejaVu
  Sans Bold for headlines (shrinking from 14pt down to 11pt to fit
  two lines), DejaVu Sans for summaries (11pt down to 9pt, two
  lines). Headline and summary text shrink to fit rather than
  wrapping or overflowing the cell.

## Verifying the numbers

Every figure printed on the page can be traced back to the story
it belongs to, so a reader can check each one without taking the
page's word for it:

- The lead counts two Patriot radars: that is the number in the
  Revolutionary Guard's own claim, while Bahrain's version of the
  same event is one civilian site on Sitra Island and two people
  wounded. Both versions are named in the story list above, and
  the page prints the claim as a claim.
- "At least 15" for Kyiv is a floor, not a final toll — the
  wording on the page keeps the "at least", because the count was
  still moving when the reports came in.
- The Java fire is 24 dead with 34 more missing; the Himalayan
  floods are 4 dead with around 100 missing. The two figures are
  kept apart on purpose: a death toll and a missing count are
  different things, and the page never merges them into one number.
- The $5.17M is the winner's cheque for the ATP Finals, paired
  with the 6–2, 7–6 scoreline, both from the tournament's own
  reporting. The 9–6 is the ICJ vote on the Myanmar genocide
  case — the first time the court has held a state responsible
  for genocide.
- The 50 million is the number of children in Bangladesh's
  typhoid vaccination drive, described by its organisers as the
  largest drive of its kind anywhere.

## Reproducing the entry

From a clean checkout, the committed `entry.png` can be rebuilt
exactly. The build needs nothing beyond Python 3.12 and Pillow:

```sh
git clone https://github.com/Tenguu0/news-image-20261124-v11-photo-evening.git
cd news-image-20261124-v11-photo-evening
MAKEFUN_OUTPUT_DIR=/tmp/v11-check1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/v11-check2 python3 main.py
sha256sum /tmp/v11-check1/entry.png /tmp/v11-check2/entry.png entry.png
```

The reference hash is
`c376a1383ccf13a8660686e0983575ca7fd275cd7dab584f1784df96ed1c1e2e`.
All three hashes should be identical. If a hash differs, the first
things to check are the `assets/` folder (all twelve pictures must
be present) and the Pillow version, since the layout depends on
the fonts Pillow finds on the system.

## Editorial choices

- Pictures lead, words follow: this is an evening edition, so
  the reader meets the picture of each story before its headline.
  The lead panorama is the widest picture on the page because the
  Bahrain strike is the day's biggest story, and a night-time
  airbase scene reads best at that size.
- The "Day in Numbers" box exists because the grid had one slot
  left and a list of bare figures fills it better than a
  thirteenth small story would. The four numbers in it are the
  ones a reader is most likely to remember the next morning: two
  death tolls, one record prize, and one vaccination drive.
- Claims stay attached to whoever made them. The Tehran claim,
  the Kyiv claim about the warship, and Bahrain's account of the
  same strike are all printed with their claimant named, and
  Moscow's silence on the ship claim is noted rather than filled
  in with a guess.
- The footer is honest about the pictures: every one of them is
  an AI-generated illustration matched to its story, and the page
  says so in plain words instead of passing them off as
  photographs.
