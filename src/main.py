"""
Command line runner for the Music Recommender Simulation.
"""

import sys
from src.recommender import load_songs, recommend_songs

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


USER_PROFILES = {
    "Happy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8, "min_popularity": 0},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "favorite_mood_tags": ["relaxing", "cozy"]},
    "High-Energy EDM": {"genre": "edm", "mood": "intense", "energy": 0.95, "min_popularity": 50},
    "Acoustic Low-Energy": {"genre": "acoustic", "mood": "relaxed", "energy": 0.25, "likes_acoustic": True},
    "Adversarial (conflicting prefs)": {"genre": "metal", "mood": "sad", "energy": 0.9},
}


def print_recommendations(profile_name, results):
    print(f"\n=== {profile_name} ===")
    if HAS_TABULATE:
        rows = [[song["title"], song["artist"], score, explanation] for song, score, explanation in results]
        print(tabulate(rows, headers=["Title", "Artist", "Score", "Reasons"], tablefmt="grid"))
    else:
        for i, (song, score, explanation) in enumerate(results, start=1):
            print(f"{i}. {song['title']} - Score: {score:.2f}")
            print(f"   Because: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    strategy = "balanced"
    if len(sys.argv) > 1 and sys.argv[1] in ("balanced", "genre_first", "mood_first", "energy_similarity"):
        strategy = sys.argv[1]

    print(f"Strategy: {strategy}")

    for profile_name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5, strategy=strategy, diversity_penalty=0.5)
        print_recommendations(profile_name, recommendations)


if __name__ == "__main__":
    main()