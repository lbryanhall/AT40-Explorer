# AT40 Explorer

A first project to learn Claude and GitHub.

A fan of the American Top 40 shows hosted by Casey Kasem throughout the 1970's. A simple HTML project to view song / artist information, with lookups by week, artist, song title, and year.

## Features

- **Pick a Week's Countdown** - Select any of the 522 chart weeks (grouped by year) and see the complete Top 40 for that week:
  - This week / last week position with up-down movement
  - NEW and RE (re-entry) markers
  - Weeks on chart and all-time peak
  - Click any title to jump to its full chart history
- **Search by Artist** - Find all songs by a specific artist that charted on AT40, sorted by entry date
- **Search by Song** - Look up individual songs with complete chart history including:
  - Peak position
  - Total weeks at #1
  - Total weeks on AT40 chart
  - Entry and exit dates
  - Week-by-week chart positions
- **Search by Year** - Browse all #1 songs for any year (1970-1979) with their performance metrics
- **Interactive Results** - Beautiful data tables with sortable information
- **No Installation Required** - Runs entirely in your browser

## Quick Start

1. Download `AT40ExplorerStandalone.html`
2. Double-click to open in your browser
3. Start searching!

## Data Source

- **Years**: 1970-1979
- **Chart Weeks**: 522 (Jan 3, 1970 - Dec 29, 1979), 40 songs each
- **Song Records**: 2,438 recordings across 2,386 unique titles
- **Total Artists**: 948
- **Total Chart Entries**: 20,880 weekly appearances

### Competing versions of the same title

50 titles were recorded by more than one artist during the decade, and the original
data merged them into a single record. Each recording is now its own entry, keyed as
`Title — Artist`. For example, "Best Of My Love" is two records: the Eagles' 1975 #1
and The Emotions' 1977 #1. In a handful of cases both versions charted the same week,
such as July 24, 1971, when James Taylor's "You've Got A Friend" sat at #3 while
Roberta Flack & Donny Hathaway's was at #32.

## Files Included

| File | Purpose |
|------|---------|
| `AT40ExplorerStandalone.html` | Complete app with embedded data (current) |
| `rebuild.py` | Splits merged same-title records by artist and rebuilds the dataset |
| `at40_compact.json` | Processed chart data |
| `at40_data.json` / `at40_data.js` | Intermediate data formats |
| `AT40Explorer.html` / `AT40Explorer.jsx` | Earlier non-standalone versions |
| `AT40Explorer-Standalone.html` | Earlier standalone build (superseded) |
| `AT40_19XX_Weekly_Charts.xlsx` | Original spreadsheet data, one file per year |

## Rebuilding the data

`rebuild.py` reads `data.json` (the `AT40_DATA` object pulled out of the HTML) and
writes `data_fixed.json`. It separates each merged title into per-recording chart runs
by threading entries on the `weeks_on_chart` field, assigns each run to its artist from
a verified lookup table, recomputes peak / weeks-at-#1 / total-weeks / entry / exit
dates per record, and rebuilds the artist index. It also clamps six late-1976 records
whose stored peak was worse than a position they actually charted at (one listed #41,
impossible in a Top 40 dataset).

Re-run it if the data is ever extended past 1979 — the artist assignment table will
need new entries for any additional competing versions.

## How to Use

1. **Pick a Week** - Choose a chart date to see that week's entire countdown, #1 through #40
2. **Search by Artist** - Type artist name to see all their charted songs sorted by entry date
3. **Search by Song** - Look up a song title to see complete chart history with weekly positions
4. **Search by Year** - Select 1970-1979 to see all #1 songs for that year

## Browser Compatibility

Works on Chrome, Firefox, Safari, Edge, and Opera.

## Technology

- React 18
- Tailwind CSS
- JSON data format
- Browser-based (no server required)

---

**Created**: August 2026  
**Maintainer**: Bryan Hall (lbryanhall)
