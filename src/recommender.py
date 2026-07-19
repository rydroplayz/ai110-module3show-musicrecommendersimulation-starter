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
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "genre": self.genre,
            "mood": self.mood,
            "energy": self.energy,
            "tempo_bpm": self.tempo_bpm,
            "valence": self.valence,
            "danceability": self.danceability,
            "acousticness": self.acousticness,
            "popularity": self.popularity,
            "release_decade": self.release_decade,
            "duration_sec": self.duration_sec,
            "is_explicit": self.is_explicit,
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
            "genre": self.favorite_genre,
            "mood": self.favorite_mood,
            "energy": self.target_energy,
            "likes_acoustic": self.likes_acoustic,
            "favorite_mood_tags": self.favorite_mood_tags,
            "min_popularity": self.min_popularity,
        }


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with correct types."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "popularity": float(row.get("popularity", 50)),
                "release_decade": row.get("release_decade", "2020s"),
                "duration_sec": float(row.get("duration_sec", 200)),
                "is_explicit": row.get("is_explicit", "False").strip().lower() == "true",
                "mood_tags": [t.strip() for t in row.get("mood_tags", "").split(";") if t.strip()],
            })
    return songs


def _energy_closeness(target: float, actual: float, max_points: float) -> float:
    """Sliding-scale score: full points at a perfect match, fewer as the gap grows."""
    gap = abs(target - actual)
    return round(max_points * max(0.0, 1 - gap), 2)


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the weighted
    Algorithm Recipe from README.md. Returns (score, reasons).
    """
    score = 0.0
    reasons = []

    if user_prefs.get("genre") == song.get("genre"):
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    if user_prefs.get("mood") == song.get("mood"):
        score += 1.5
        reasons.append(f"mood match: {song['mood']} (+1.5)")

    energy_pts = _energy_closeness(user_prefs.get("energy", 0.5), song.get("energy", 0.5), 2.0)
    if energy_pts > 0:
        score += energy_pts
        reasons.append(f"energy closeness (+{energy_pts})")

    if user_prefs.get("likes_acoustic") and song.get("acousticness", 0) >= 0.6:
        score += 1.0
        reasons.append("acoustic preference match (+1.0)")

    favorite_tags = set(user_prefs.get("favorite_mood_tags", []))
    song_tags = set(song.get("mood_tags", []))
    if favorite_tags and favorite_tags.intersection(song_tags):
        score += 1.0
        reasons.append("mood tag overlap (+1.0)")

    if song.get("popularity", 0) >= user_prefs.get("min_popularity", 0):
        pop_pts = round(0.5 * (song.get("popularity", 0) / 100), 2)
        score += pop_pts
        reasons.append(f"popularity bonus (+{pop_pts})")

    if not reasons:
        reasons.append("no strong matches, included for catalog variety")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, sorts by score descending, and returns the top k
    as (song_dict, score, explanation_string) tuples.
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda item: item[1], reverse=True)
    top = scored[:k]
    return [(song, score, "; ".join(reasons)) for song, score, reasons in top]


class Recommender:
    """OOP wrapper around the same scoring engine used by the functional API above."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        song_dicts = [s.to_dict() for s in self.songs]
        results = recommend_songs(user.to_dict(), song_dicts, k=k)
        result_ids = [song["id"] for song, score, explanation in results]
        by_id = {s.id: s for s in self.songs}
        return [by_id[song_id] for song_id in result_ids]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = score_song(user.to_dict(), song.to_dict())
        return "; ".join(reasons)