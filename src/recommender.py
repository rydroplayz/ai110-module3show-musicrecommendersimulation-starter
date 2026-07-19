from typing import List, Dict, Tuple
from dataclasses import dataclass, field
import csv


@dataclass
class Song:
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: float = 50.0
    release_decade: str = "2020s"
    duration_sec: float = 200.0
    is_explicit: bool = False
    mood_tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "id": self.id, "title": self.title, "artist": self.artist,
            "genre": self.genre, "mood": self.mood, "energy": self.energy,
            "tempo_bpm": self.tempo_bpm, "valence": self.valence,
            "danceability": self.danceability, "acousticness": self.acousticness,
            "popularity": self.popularity, "release_decade": self.release_decade,
            "duration_sec": self.duration_sec, "is_explicit": self.is_explicit,
            "mood_tags": self.mood_tags,
        }


@dataclass
class UserProfile:
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool = False
    favorite_mood_tags: List[str] = field(default_factory=list)
    min_popularity: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "genre": self.favorite_genre, "mood": self.favorite_mood,
            "energy": self.target_energy, "likes_acoustic": self.likes_acoustic,
            "favorite_mood_tags": self.favorite_mood_tags,
            "min_popularity": self.min_popularity,
        }


def load_songs(csv_path: str) -> List[Dict]:
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]), "title": row["title"], "artist": row["artist"],
                "genre": row["genre"], "mood": row["mood"],
                "energy": float(row["energy"]), "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]), "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "popularity": float(row.get("popularity", 50)),
                "release_decade": row.get("release_decade", "2020s"),
                "duration_sec": float(row.get("duration_sec", 200)),
                "is_explicit": row.get("is_explicit", "False").strip().lower() == "true",
                "mood_tags": [t.strip() for t in row.get("mood_tags", "").split(";") if t.strip()],
            })
    return songs


def _closeness(target: float, actual: float, max_points: float) -> float:
    gap = abs(target - actual)
    return round(max_points * max(0.0, 1 - gap), 2)


# --- Strategy pattern: each mode is a different weighting of the same rules ---
STRATEGY_WEIGHTS = {
    "balanced":          {"genre": 2.0, "mood": 1.5, "energy": 2.0, "acoustic": 1.0, "tag": 1.0, "pop": 0.5},
    "genre_first":       {"genre": 4.0, "mood": 1.0, "energy": 1.0, "acoustic": 0.5, "tag": 0.5, "pop": 0.3},
    "mood_first":        {"genre": 1.0, "mood": 4.0, "energy": 1.0, "acoustic": 0.5, "tag": 1.5, "pop": 0.3},
    "energy_similarity": {"genre": 0.5, "mood": 0.5, "energy": 4.0, "acoustic": 0.3, "tag": 0.3, "pop": 0.2},
}


def score_song(user_prefs: Dict, song: Dict, strategy: str = "balanced") -> Tuple[float, List[str]]:
    """Scores a single song against user preferences using the named strategy. Returns (score, reasons)."""
    w = STRATEGY_WEIGHTS.get(strategy, STRATEGY_WEIGHTS["balanced"])
    score = 0.0
    reasons = []

    if user_prefs.get("genre") == song.get("genre"):
        score += w["genre"]
        reasons.append(f"genre match: {song['genre']} (+{w['genre']})")

    if user_prefs.get("mood") == song.get("mood"):
        score += w["mood"]
        reasons.append(f"mood match: {song['mood']} (+{w['mood']})")

    energy_pts = _closeness(user_prefs.get("energy", 0.5), song.get("energy", 0.5), w["energy"])
    if energy_pts > 0:
        score += energy_pts
        reasons.append(f"energy closeness (+{energy_pts})")

    if user_prefs.get("likes_acoustic") and song.get("acousticness", 0) >= 0.6:
        score += w["acoustic"]
        reasons.append(f"acoustic preference match (+{w['acoustic']})")

    favorite_tags = set(user_prefs.get("favorite_mood_tags", []))
    song_tags = set(song.get("mood_tags", []))
    if favorite_tags and favorite_tags.intersection(song_tags):
        score += w["tag"]
        reasons.append(f"mood tag overlap (+{w['tag']})")

    if song.get("popularity", 0) >= user_prefs.get("min_popularity", 0):
        pop_pts = round(w["pop"] * (song.get("popularity", 0) / 100), 2)
        score += pop_pts
        reasons.append(f"popularity bonus (+{pop_pts})")

    if not reasons:
        reasons.append("no strong matches, included for catalog variety")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                     strategy: str = "balanced", diversity_penalty: float = 0.0) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, ranks them, and returns the top k as (song_dict, score, explanation) tuples.

    diversity_penalty > 0 enables an artist-repetition penalty: each time an
    artist already appears in the results, remaining songs by that artist
    get the penalty subtracted before the next pick, so one artist can't
    fill the whole top k. This is a simple filter-bubble guard.
    """
    scored = [[song, *score_song(user_prefs, song, strategy)] for song in songs]

    if diversity_penalty <= 0:
        scored.sort(key=lambda item: item[1], reverse=True)
        top = scored[:k]
        return [(song, score, "; ".join(reasons)) for song, score, reasons in top]

    remaining = scored
    chosen = []
    while remaining and len(chosen) < k:
        remaining.sort(key=lambda item: item[1], reverse=True)
        best = remaining.pop(0)
        chosen.append(best)
        artist = best[0]["artist"]
        for item in remaining:
            if item[0]["artist"] == artist:
                item[1] = round(item[1] - diversity_penalty, 2)
                item[2] = item[2] + [f"artist diversity penalty (-{diversity_penalty})"]

    return [(song, score, "; ".join(reasons)) for song, score, reasons in chosen]


class Recommender:
    """OOP wrapper around the same scoring engine used by the functional API above."""

    def __init__(self, songs: List[Song], strategy: str = "balanced", diversity_penalty: float = 0.0):
        self.songs = songs
        self.strategy = strategy
        self.diversity_penalty = diversity_penalty

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        song_dicts = [s.to_dict() for s in self.songs]
        results = recommend_songs(user.to_dict(), song_dicts, k=k,
                                   strategy=self.strategy, diversity_penalty=self.diversity_penalty)
        result_ids = [song["id"] for song, score, explanation in results]
        by_id = {s.id: s for s in self.songs}
        return [by_id[song_id] for song_id in result_ids]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = score_song(user.to_dict(), song.to_dict(), self.strategy)
        return "; ".join(reasons)