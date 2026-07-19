# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name
VibeMatch 1.0

## 2. Intended Use
This recommender is a classroom simulation of content-based filtering. It generates a ranked list of songs from a fixed 20-song catalog based on how closely each song's attributes match a stated listener taste profile. It assumes the "user" is really just a dictionary of preferences typed in by a developer, not a real person with browsing history — there's no login, no learning over time, and no real user data involved. It's built for exploring how scoring and ranking work, not for real-world music recommendations.

## 3. How the Model Works
For every song in the catalog, the system checks: does its genre match what the listener said they like? Does its mood match? Is its energy close to what they want (partial credit for being close, not just an exact match)? Does the listener like acoustic songs, and is this song acoustic enough? Do any of the listener's favorite mood tags (like "cozy" or "euphoric") appear on this song? Each of these checks adds points if it's true. All songs get scored this way, then sorted from highest to lowest score, and the top 5 are shown along with the specific reasons each song earned its score.

## 4. Data
- 20 songs in `data/songs.csv`, each with 14 attributes: title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness, popularity, release_decade, duration_sec, is_explicit, mood_tags.
- Numeric features (energy, valence, danceability, acousticness) are hand-set on a 0.0–1.0 scale; tempo_bpm and popularity use their natural ranges.
- Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop, acoustic, edm — 9 genres across 20 songs, so some genres (pop, lofi, rock) have 2-3 songs while others (jazz, ambient, acoustic) also have 2-3, making the catalog reasonably but not perfectly balanced.
- This is a hand-authored dataset, not real streaming data — attribute values are estimates, not measured from real audio.

## 5. Strengths
The Happy Pop and Chill Lofi profiles both gave results that felt right immediately. Sunrise City and Sugar Rush topping the Happy Pop list makes sense, they're both pop, both happy, both close to the 0.8 energy target. Same with Chill Lofi, Library Rain and Midnight Coding are legit chill lofi tracks and they scored highest. The Acoustic Low-Energy profile also worked well, Wandering Strings and Slow Burn are the two most acoustic-heavy songs in the whole catalog, so it makes sense they came out on top once likes_acoustic kicked in. The scoring clearly separates opposite-vibe profiles too, EDM and Acoustic Low-Energy don't share a single song in their top 5, which is what should happen when two profiles ask for almost opposite energy levels.

## 6. Limitations and Bias
The clearest bias I found was with the Adversarial profile. It asked for genre "metal" and mood "sad," and my catalog has neither. Instead of telling the user that, the system just quietly stops scoring on those two rules and falls back to ranking by energy and popularity alone. That's a silent failure, not an obvious one, someone using this wouldn't know their genre preference got ignored unless they checked the reasons closely.

There's also a genre-matching bias I noticed directly in the output: Rooftop Lights and Golden Hour are labeled "indie pop," and when I ran the Happy Pop profile (genre: "pop"), neither song got genre-match points even though "indie pop" is basically a pop subgenre. My scoring only checks for an exact string match, so close-but-not-identical genres get treated the same as a completely wrong genre. That's probably not how a real listener would judge similarity.

Smaller thing: the popularity bonus, even though it's only worth up to 0.5 points, always nudges already-popular songs up a bit. In a bigger catalog that could snowball into a rich-get-richer effect where popular songs stay on top just because they're popular, not because they're actually the best match.

## 7. Evaluation

Five user profiles were tested, each requesting the top 5 recommendations:

### Happy Pop
```
Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'min_popularity': 0}
1. Sunrise City - Score: 5.85
   Because: genre match: pop (+2.0); mood match: happy (+1.5); energy closeness (+1.96); popularity bonus (+0.39)
2. Sugar Rush - Score: 5.75
   Because: genre match: pop (+2.0); mood match: happy (+1.5); energy closeness (+1.9); popularity bonus (+0.35)
3. Gym Hero - Score: 4.09
   Because: genre match: pop (+2.0); energy closeness (+1.74); popularity bonus (+0.35)
4. Rooftop Lights - Score: 3.76
   Because: mood match: happy (+1.5); energy closeness (+1.92); popularity bonus (+0.34)
5. Golden Hour - Score: 3.1
   Because: mood match: happy (+1.5); energy closeness (+1.78); popularity bonus (+0.32); artist diversity penalty (-0.5)
```

### Chill Lofi
```
Profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'favorite_mood_tags': ['relaxing', 'cozy']}
1. Library Rain - Score: 6.69
   Because: genre match: lofi (+2.0); mood match: chill (+1.5); energy closeness (+2.0); mood tag overlap (+1.0); popularity bonus (+0.19)
2. Midnight Coding - Score: 6.59
   Because: genre match: lofi (+2.0); mood match: chill (+1.5); energy closeness (+1.86); mood tag overlap (+1.0); popularity bonus (+0.23)
3. Focus Flow - Score: 4.6
   Because: genre match: lofi (+2.0); energy closeness (+1.9); mood tag overlap (+1.0); popularity bonus (+0.2); artist diversity penalty (-0.5)
4. Spacewalk Thoughts - Score: 4.5
   Because: mood match: chill (+1.5); energy closeness (+1.86); mood tag overlap (+1.0); popularity bonus (+0.14)
5. Coffee Shop Stories - Score: 3.13
   Because: energy closeness (+1.96); mood tag overlap (+1.0); popularity bonus (+0.17)
```

### High-Energy EDM
```
Profile: {'genre': 'edm', 'mood': 'intense', 'energy': 0.95, 'min_popularity': 50}
1. Neon Pulse - Score: 5.9
   Because: genre match: edm (+2.0); mood match: intense (+1.5); energy closeness (+2.0); popularity bonus (+0.4)
2. Bass Drop City - Score: 5.83
   Because: genre match: edm (+2.0); mood match: intense (+1.5); energy closeness (+1.96); popularity bonus (+0.37)
3. Gym Hero - Score: 3.31
   Because: mood match: intense (+1.5); energy closeness (+1.96); popularity bonus (+0.35); artist diversity penalty (-0.5)
4. Storm Runner - Score: 3.23
   Because: mood match: intense (+1.5); energy closeness (+1.92); popularity bonus (+0.31); artist diversity penalty (-0.5)
5. Broken Amps - Score: 2.65
   Because: mood match: intense (+1.5); energy closeness (+1.86); popularity bonus (+0.29); artist diversity penalty (-0.5); artist diversity penalty (-0.5)
```

### Acoustic Low-Energy
```
Profile: {'genre': 'acoustic', 'mood': 'relaxed', 'energy': 0.25, 'likes_acoustic': True}
1. Wandering Strings - Score: 6.58
   Because: genre match: acoustic (+2.0); mood match: relaxed (+1.5); energy closeness (+1.98); acoustic preference match (+1.0); popularity bonus (+0.1)
2. Slow Burn - Score: 6.0
   Because: genre match: acoustic (+2.0); mood match: relaxed (+1.5); energy closeness (+1.88); acoustic preference match (+1.0); popularity bonus (+0.12); artist diversity penalty (-0.5)
3. Coffee Shop Stories - Score: 4.43
   Because: mood match: relaxed (+1.5); energy closeness (+1.76); acoustic preference match (+1.0); popularity bonus (+0.17)
4. Old Town Jazz - Score: 3.8
   Because: mood match: relaxed (+1.5); energy closeness (+1.62); acoustic preference match (+1.0); popularity bonus (+0.18); artist diversity penalty (-0.5)
5. Spacewalk Thoughts - Score: 3.08
   Because: energy closeness (+1.94); acoustic preference match (+1.0); popularity bonus (+0.14)
```

### Adversarial (conflicting prefs)
```
Profile: {'genre': 'metal', 'mood': 'sad', 'energy': 0.9}
1. Neon Pulse - Score: 2.3
   Because: energy closeness (+1.9); popularity bonus (+0.4)
2. Gym Hero - Score: 2.29
   Because: energy closeness (+1.94); popularity bonus (+0.35)
3. Sugar Rush - Score: 2.25
   Because: energy closeness (+1.9); popularity bonus (+0.35)
4. Sunrise City - Score: 2.23
   Because: energy closeness (+1.84); popularity bonus (+0.39)
5. Rooftop Lights - Score: 2.06
   Because: energy closeness (+1.72); popularity bonus (+0.34)
```

### Comparisons

- **Happy Pop vs. Chill Lofi**: Happy Pop's top picks have energy around 0.82-0.93 and happy mood tags; Chill Lofi's top picks drop to energy 0.35-0.42 with relaxing/cozy tags. The two profiles ask for nearly opposite energy targets, and the scoring correctly separates them — there's no overlap between the top 5 lists.
- **High-Energy EDM vs. Acoustic Low-Energy**: EDM's top result (Neon Pulse) has energy 0.95; Acoustic's top result (Wandering Strings) has energy 0.26. This is the widest energy gap of any pair tested, and it's exactly what the "energy closeness" scoring is designed to detect.
- **Adversarial profile**: with no song labeled genre "metal" or mood "sad" in the catalog, both of those scoring rules contribute zero points for every song, and the system silently falls back to ranking almost entirely by energy closeness and popularity. In plain language — if a listener asks for a genre or mood the catalog simply doesn't have, the system doesn't say "I can't help with that," it just quietly stops listening to that part of the request and recommends based on whatever's left.

## 8. Intended Use and Non-Intended Use
**Intended use**: an educational demo of how weighted, content-based scoring and ranking work together to produce recommendations.
**Not intended for**: real music recommendations, any claim about actual listener behavior, or use with real user data — the attribute values in the dataset are hand-estimated, not measured from real audio, and the system has no way of learning from real usage.

## Diversity / Fairness Component

recommend_songs() accepts a diversity_penalty parameter. After each song is picked for the results, any remaining song by that same artist gets the penalty subtracted from its score before the next pick. This is meant to stop one artist with several catalog entries from filling the whole top 5.

Tested against the High-Energy EDM profile at diversity_penalty=0.5, the penalty does visibly fire: Gym Hero, Storm Runner, and Broken Amps all pick up an "artist diversity penalty (-0.5)" reason, and Broken Amps is penalized twice (once for sharing an artist with Neon Pulse, once for sharing an artist with Storm Runner), dropping it from what would otherwise be a higher score down to 2.65. However, at this penalty value it isn't strong enough to actually change who makes the top 5 — all 5 slots are still held by just two artists, Voltline and Max Pulse. A real fix would need either a larger penalty per repeat or a hard cap (e.g. "max 2 songs per artist in the results"), which is now listed under Future Work.

## 9. Future Work
1. Add fuzzy/partial genre matching so subgenres like "indie pop" get partial credit against "pop" instead of zero.
2. When a stated preference (genre or mood) doesn't exist anywhere in the catalog, show a warning instead of silently ignoring it, so the user knows part of their request had no effect.
3. Increase the artist diversity penalty (or add a hard per-artist cap) — at the current 0.5-point penalty, Voltline and Max Pulse still occupy all 5 slots in the High-Energy EDM results, so the fairness mechanism isn't strong enough yet to meaningfully diversify results in a small catalog like this one.

## 10. Personal Reflection
The biggest thing I learned is that "recommendation" is really just scoring every option and sorting them, there's no extra magic step once you break it down like that. What surprised me was the Adversarial profile, I expected it to just return low scores across the board, not to silently drop two of my three scoring rules and rank almost entirely on the leftover ones. That's a good example of how a system can look like it's working while quietly ignoring part of what you asked for. AI helped me build the scoring logic fast, but I still had to actually run it myself to catch real bugs, like when I ran main.py and got a ModuleNotFoundError because the import didn't match how I was actually running the script. Reading the actual test output instead of assuming it worked is what caught that.