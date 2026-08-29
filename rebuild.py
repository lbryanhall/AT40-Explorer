import json, datetime, collections, sys

d = json.load(open('data.json'))

def pd(s): return datetime.date(*map(int, s.split('-')))

def chains(hist):
    """Thread chart entries into per-recording runs.
    A recording advances one week and one weeks_on_chart at a time; a re-entry
    after k missing weeks advances weeks_on_chart by k."""
    ent = sorted(hist, key=lambda e: (e['date'], e['weeks_on_chart']))
    ch = []
    for e in ent:
        dt = pd(e['date']); w = e['weeks_on_chart']
        best = None; bestgap = None
        for c in ch:
            last = c[-1]; gap = (dt - pd(last['date'])).days // 7
            if gap < 1: continue
            if w - last['weeks_on_chart'] == gap and gap <= 8:
                if bestgap is None or gap < bestgap:
                    best, bestgap = c, gap
        if best is not None: best.append(e)
        else: ch.append([e])
    return ch

# Which recording charted in which run, in chronological run order.
# Verified against peak position and chart dates.
ASSIGN = {
 "Heaven Knows": ["The Grass Roots", "Donna Summer With Brooklyn Dreams"],
 "Cupid": ["Johnny Nash", "Tony Orlando & Dawn"],
 "Breaking Up Is Hard To Do": ["Lenny Welch", "The Partridge Family Starring Shirley Jones Featuring David Cassidy", "Neil Sedaka"],
 "Woodstock": ["Crosby, Stills, Nash & Young", "Matthews' Southern Comfort"],
 "Baby Hold On": ["The Grass Roots", "Eddie Money"],
 "I Want To Take You Higher": ["Sly & The Family Stone", "Ike & Tina Turner & The Ikettes"],
 "Big Yellow Taxi": ["The Neighborhood", "Joni Mitchell"],
 "(I Know) I'm Losing You": ["Rare Earth", "Rod Stewart With Faces"],
 "I (Who Have Nothing)": ["Tom Jones", "Sylvester"],
 "Love The One You're With": ["Stephen Stills", "The Isley Brothers"],
 "Amazing Grace": ["Judy Collins", "The Pipes And Drums And The Military Band Of The Royal Scots Dragoon Guards"],
 "Me And Bobby McGee": ["Janis Joplin", "Jerry Lee Lewis"],
 "Help Me Make It Through The Night": ["Sammi Smith", "Gladys Knight And The Pips"],
 "Free": ["Chicago", "Deniece Williams"],
 "You're All I Need To Get By": ["Aretha Franklin", "Tony Orlando & Dawn"],
 "Never Can Say Goodbye": ["Jackson 5", "Isaac Hayes", "Gloria Gaynor"],
 "Superstar": ["Murray Head With The Trinidad Singers", "Paul Davis"],
 "I Don't Know How To Love Him": ["Helen Reddy", "Yvonne Elliman"],
 "Lowdown": ["Chicago", "Boz Scaggs"],
 "You've Got A Friend": ["James Taylor", "Roberta Flack & Donny Hathaway"],
 "Never My Love": ["The 5th Dimension", "Blue Swede"],
 "I'd Like To Teach The World To Sing (In Perfect Harmony)": ["The Hillside Singers", "The New Seekers"],
 "Tumbling Dice": ["The Rolling Stones", "Linda Ronstadt"],
 "(If Loving You Is Wrong) I Don't Want To Be Right": ["Luther Ingram", "Barbara Mandrell"],
 "Midnight Rider": ["Joe Cocker and The Chris Stainton Band", "Gregg Allman"],
 "Sweet Surrender": ["Bread", "John Denver"],
 "Angel": ["Rod Stewart", "Aretha Franklin"],
 "I Can't Stand The Rain": ["Ann Peebles", "Eruption"],
 "My Sweet Lady": ["Cliff DeYoung", "John Denver"],
 "The Entertainer": ['Marvin Hamlisch/"The Sting"', "Billy Joel"],
 "Daybreak": ["Nilsson", "Barry Manilow"],
 "On And On": ["Gladys Knight And The Pips", "Stephen Bishop"],
 "Feel Like Makin' Love": ["Roberta Flack", "Bad Company"],
 "Fallin' In Love": ["The Souther, Hillman, Furay Band", "Hamilton, Joe Frank & Reynolds"],
 "Dream On": ["The Righteous Brothers", "Aerosmith"],
 "Fire": ["Ohio Players", "The Pointer Sisters"],
 "Best Of My Love": ["Eagles", "The Emotions"],
 "Lady": ["Styx", "Little River Band"],
 "Emotion": ["Helen Reddy", "Samantha Sang"],
 "I'm On Fire": ["Dwight Twilley Band", "5000 Volts"],
 "Dance With Me": ["Orleans", "Peter Brown With Betty Wright"],
 "Your Love": ["Graham Central Station", "Marilyn McCoo & Billy Davis Jr."],
 "You": ["George Harrison", "Rita Coolidge"],
 "Somewhere In The Night": ["Helen Reddy", "Barry Manilow"],
 "Renegade": ["Michael Murphey", "Styx"],
 "Young Blood": ["Bad Company", "Rickie Lee Jones"],
 "Got To Get You Into My Life": ["The Beatles", "Earth, Wind & Fire"],
 "Love Ballad": ["L.T.D.", "George Benson"],
 "Crazy Love": ["Poco", "The Allman Brothers Band"],
 "Hold On": ["Triumph", "Ian Gomm"],
}

# True Billboard peaks for runs that were already descending when the data begins
# (the song peaked before 1970-01-03, so the peak isn't visible in chart_history).
PEAK_OVERRIDE = {("Heaven Knows", "The Grass Roots"): 24}

errors = []
new_songs = {}
split_map = {}   # original title -> [new keys]

for title, sd in d['songs'].items():
    if title not in ASSIGN:
        new_songs[title] = dict(sd, title=title)
        continue

    order = ASSIGN[title]
    if sorted(order) != sorted(sd['artists']):
        errors.append(f"{title}: assignment {sorted(order)} != data {sorted(sd['artists'])}")
        continue

    runs = chains(sd['chart_history'])
    if len(runs) != len(order):
        errors.append(f"{title}: {len(runs)} runs but {len(order)} artists")
        continue

    keys = []
    for artist, seg in zip(order, runs):
        seg = sorted(seg, key=lambda e: e['date'])
        key = f"{title} — {artist}"          # em dash
        peak = PEAK_OVERRIDE.get((title, artist), min(e['pos'] for e in seg))
        new_songs[key] = {
            "title": title,
            "artists": [artist],
            "peak": peak,
            "weeks_at_1": sum(1 for e in seg if e['pos'] == 1),
            "total_weeks": len(seg),
            "entry_date": seg[0]['date'],
            "exit_date": seg[-1]['date'],
            "chart_history": seg,
        }
        keys.append(key)
    split_map[title] = keys

if errors:
    print("ERRORS:"); [print("  ", e) for e in errors]; sys.exit(1)

# A peak can never be worse than a position the record actually reached.
# Six late-1976 records in the source are off by one (one lists #41, which is
# impossible in a Top 40 dataset). Clamp to the best position actually charted.
clamped = []
for key, sd in new_songs.items():
    best = min(e['pos'] for e in sd['chart_history'])
    if sd['peak'] > best:
        clamped.append((key, sd['peak'], best))
        sd['peak'] = best
print("peaks clamped to best charted position:", len(clamped))
for k, was, now in clamped:
    print(f"    {k}: #{was} -> #{now}")

# Rebuild the artists index from the new song records
artists = collections.defaultdict(list)
for key, sd in new_songs.items():
    for a in sd['artists']:
        artists[a].append(key)
artists = {a: {"songs": sorted(set(v))} for a, v in sorted(artists.items())}

out = {"songs": new_songs, "artists": artists}

# ---- integrity checks -------------------------------------------------
weeks = collections.defaultdict(list)
for key, sd in new_songs.items():
    for e in sd['chart_history']:
        weeks[e['date']].append((e['pos'], key))

problems = []
for dt, v in weeks.items():
    if len(v) != 40: problems.append(f"{dt}: {len(v)} entries")
    if sorted(p for p, _ in v) != list(range(1, 41)): problems.append(f"{dt}: bad positions")
    if len(set(k for _, k in v)) != 40: problems.append(f"{dt}: duplicate song key")

multi = [k for k, sd in new_songs.items() if len(sd['artists']) > 1]

print("songs before:", len(d['songs']), "-> after:", len(new_songs))
print("titles split:", len(split_map))
print("artists before:", len(d['artists']), "-> after:", len(artists))
print("weeks:", len(weeks))
print("records still carrying >1 artist:", len(multi), multi)
print("week integrity problems:", len(problems), problems[:5])

# every original chart entry must survive exactly once
before = sum(len(sd['chart_history']) for sd in d['songs'].values())
after = sum(len(sd['chart_history']) for sd in new_songs.values())
print("chart entries before:", before, "after:", after, "MATCH" if before == after else "MISMATCH")

# artist index must round-trip
bad_idx = [a for a, v in artists.items() for k in v['songs'] if k not in new_songs]
print("dangling artist->song refs:", len(bad_idx))

json.dump(out, open('data_fixed.json', 'w'), ensure_ascii=False)
print("\nsample split:")
for t in ["Best Of My Love", "You've Got A Friend", "Never Can Say Goodbye"]:
    for k in split_map[t]:
        s = new_songs[k]
        print(f"  {k}  peak #{s['peak']}  wks@1 {s['weeks_at_1']}  total {s['total_weeks']}  {s['entry_date']}..{s['exit_date']}")
