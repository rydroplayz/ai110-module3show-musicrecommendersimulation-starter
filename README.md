# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



