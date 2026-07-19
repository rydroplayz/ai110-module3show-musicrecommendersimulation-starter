# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a content-based music recommender: it represents songs and a listener's taste profile as structured data, scores every song in a 20-track catalog against that profile using a weighted point system, and returns a ranked, explained list of recommendations.

---

## How The System Works

Real-world music platforms like Spotify and YouTube generally combine two approaches. Collaborative filtering looks at behavior across many users — if people who liked the songs you liked also liked a new song, it gets recommended to you, even if the system knows nothing about the song's actual sound. Content-based filtering instead looks at the song's own
attributes (genre, tempo, mood, energy) and compares them to attributes you've responded well to in the past. Most production systems blend both, since collaborative filtering needs a lot of user history to work well, while content-based filtering can make reasonable suggestions even for a brand-new song nobody has listened to yet (the "cold-start problem").

This simulation is a content-based recommender only — it doesn't use other users' behavior at all. Every song is represented as a set of attributes (genre, mood, energy, tempo, etc.), and a listener's taste is represented as a target profile over those same attributes. A `Recommender` scores every song in the catalog against that profile using a weighted point system, then ranks and returns the top-scoring
songs.

**Song features used:** title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness

**UserProfile features used:** favorite_genre, favorite_mood,
target_energy, likes_acoustic

### Algorithm Recipe

| Rule | Points |
|---|---|
| Genre match | +2.0 |
| Mood match | +1.5 |
| Energy closeness | up to +2.0 (sliding scale, not exact-match only) |
| Acoustic preference match | +1.0 |
| Mood tag overlap | +1.0 |
| Popularity bonus | up to +0.5 |

Potential bias to watch for: genre and mood are fixed-point matches, so a
song that's a near-perfect vibe match but technically a different genre
label could score lower than a mediocre song in the "right" genre. This
system might over-prioritize genre labels over actual sonic similarity.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
$ python -m src.main
Loaded songs: 20
Strategy: balanced

=== Happy Pop ===
+----------------+----------------+---------+---------------------------------------------------------------------------------------------------------------+
| Title          | Artist         |   Score | Reasons                                                                                                       |
+================+================+=========+===============================================================================================================+
| Sunrise City   | Neon Echo      |    5.85 | genre match: pop (+2.0); mood match: happy (+1.5); energy closeness (+1.96); popularity bonus (+0.39)         |
+----------------+----------------+---------+---------------------------------------------------------------------------------------------------------------+
| Sugar Rush     | Paper Lanterns |    5.75 | genre match: pop (+2.0); mood match: happy (+1.5); energy closeness (+1.9); popularity bonus (+0.35)          |
+----------------+----------------+---------+---------------------------------------------------------------------------------------------------------------+
| Gym Hero       | Max Pulse      |    4.09 | genre match: pop (+2.0); energy closeness (+1.74); popularity bonus (+0.35)                                   |
+----------------+----------------+---------+---------------------------------------------------------------------------------------------------------------+
| Rooftop Lights | Indigo Parade  |    3.76 | mood match: happy (+1.5); energy closeness (+1.92); popularity bonus (+0.34)                                  |
+----------------+----------------+---------+---------------------------------------------------------------------------------------------------------------+
| Golden Hour    | Indigo Parade  |    3.1  | mood match: happy (+1.5); energy closeness (+1.78); popularity bonus (+0.32); artist diversity penalty (-0.5) |
+----------------+----------------+---------+---------------------------------------------------------------------------------------------------------------+
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Switching from the balanced strategy to mood_first changes weight priority (mood becomes worth +4.0 instead of +1.5), which visibly reorders results — e.g. under mood_first, Spacewalk Thoughts jumps into the Chill Lofi top 3 even without a genre match, purely because mood weight dominates. This confirms the strategy pattern actually changes ranking behavior, not just labels.

---

## Limitations and Risks

- Genre/mood matching is exact-string only — "indie pop" gets zero credit against a "pop" preference even though it's a close subgenre.
- The Adversarial profile test showed the system silently ignores preferences (like a mood) that don't exist anywhere in the catalog, instead of warning the user.
- Small catalog (20 songs) means some genres only have 2-3 songs, limiting variety within any single genre.

See `model_card.md` for the full bias analysis.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this made it clear that "recommendation" is really just scoring plus sorting — nothing more mysterious than that. The most interesting bias I found wasn't in the math, it was in what the system does when a user's preference has no match at all: it doesn't fail, it just silently stops using that part of the input, which could easily mislead a real user into thinking their preference was respected when it wasn't.