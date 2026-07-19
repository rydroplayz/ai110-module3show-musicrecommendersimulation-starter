# AI Interactions Log

## Agentic Workflow (SF8)

**What task did you give the agent?**
Expand the song dataset with 5+ new attributes and update scoring to use them.

**Prompts used:**
"My song dataset only has genre, mood, energy, tempo_bpm, valence, danceability, acousticness. Suggest 5+ additional attributes for a content-based recommender and show how to add them to the CSV and scoring function without breaking existing rows."

**What did the agent generate or change?**
Added popularity (0-100), release_decade, duration_sec, is_explicit, and mood_tags (semicolon-separated list) to data/songs.csv and updated load_songs() to parse the new types, and score_song() to use mood_tags overlap and a popularity bonus.

**What did you verify or fix manually?**
Ran load_songs() and checked a sample row printed with correct types (floats, booleans, list for mood_tags). Confirmed all 20 rows have all 14 columns filled in so nothing breaks float conversion.

---

## Design Pattern (SF10)

**Which design pattern did you use?**
Strategy pattern — STRATEGY_WEIGHTS dict holding different weight presets (balanced, genre_first, mood_first, energy_similarity), all read by the same score_song() function.

**How did AI help you brainstorm or implement it?**
Asked how to support multiple ranking modes without duplicating the scoring function four times. AI suggested keeping one scoring function and parameterizing it with a weights dictionary selected by strategy name, rather than writing separate classes per strategy.

**How does the pattern appear in your final code?**
src/recommender.py — STRATEGY_WEIGHTS dict and the strategy parameter threaded through score_song(), recommend_songs(), and Recommender. src/main.py lets the strategy be picked via a CLI argument (python -m src.main mood_first).