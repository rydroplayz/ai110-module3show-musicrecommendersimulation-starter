"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import load_songs, recommend_songs


USER_PROFILES = {
    "Happy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8, "min_popularity": 0},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "favorite_mood_tags": ["relaxing", "cozy"]},
    "High-Energy EDM": {"genre": "edm", "mood": "intense", "energy": 0.95, "min_popularity": 50},
    "Acoustic Low-Energy": {"genre": "acoustic", "mood": "relaxed", "energy": 0.25, "likes_acoustic": True},
    "Adversarial (conflicting prefs)": {"genre": "metal", "mood": "sad", "energy": 0.9},
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in USER_PROFILES.items():
        print(f"\n=== {profile_name} ===")
        print(f"Profile: {user_prefs}")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{i}. {song['title']} - Score: {score:.2f}")
            print(f"   Because: {explanation}")


if __name__ == "__main__":
    main()