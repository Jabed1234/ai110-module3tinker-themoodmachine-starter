from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
import math

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # Score each song using the same recipe as the functional recommender
        scored: List[Tuple[Song, float, List[str]]] = []
        for s in self.songs:
            score, reasons = self._score_song_obj(user, s)
            scored.append((s, score, reasons))

        # sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)

        # return top-k Song objects
        return [s for s, _, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score_song_obj(user, song)
        return "; ".join(reasons) + f" (total={score:.2f})"

    def _score_song_obj(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """
        Score a Song dataclass against a UserProfile. Returns (score, reasons).
        This mirrors the dict-based score_song function used by recommend_songs/main.
        """
        reasons: List[str] = []

        # Genre and mood points
        genre_pts = 2.0 if song.genre == user.favorite_genre else 0.0
        if genre_pts > 0:
            reasons.append(f"genre match (+{genre_pts:.1f})")

        mood_pts = 1.0 if song.mood == user.favorite_mood else 0.0
        if mood_pts > 0:
            reasons.append(f"mood match (+{mood_pts:.1f})")

        # Numeric similarity on energy (user currently only has target_energy)
        f_u = float(user.target_energy)
        f_i = float(song.energy)
        sigma = 0.15
        score_energy = math.exp(- ((f_i - f_u) ** 2) / (2 * sigma * sigma))
        numeric_pts = 2.0 * score_energy
        reasons.append(f"energy closeness (+{numeric_pts:.2f})")

        # Acoustic preference
        acoustic_bonus = 0.0
        if user.likes_acoustic and song.acousticness >= 0.7:
            acoustic_bonus = 0.5
            reasons.append(f"acoustic preference (+{acoustic_bonus:.2f})")

        total = genre_pts + mood_pts + numeric_pts + acoustic_bonus
        return total, reasons

def load_songs(csv_path: str) -> List[Dict]:
    """
    Load songs from a CSV file and convert numeric fields to proper types.
    Required by src/main.py
    """
    songs: List[Dict] = []
    print(f"Loading songs from {csv_path}...")
    with open(csv_path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # convert types
            try:
                row_parsed: Dict = {
                    'id': int(row['id']),
                    'title': row.get('title', ''),
                    'artist': row.get('artist', ''),
                    'genre': row.get('genre', ''),
                    'mood': row.get('mood', ''),
                    'energy': float(row.get('energy') or 0.0),
                    'tempo_bpm': float(row.get('tempo_bpm') or 0.0),
                    'valence': float(row.get('valence') or 0.0),
                    'danceability': float(row.get('danceability') or 0.0),
                    'acousticness': float(row.get('acousticness') or 0.0),
                }
            except Exception:
                # fall back: keep raw row but do best-effort conversions
                row_parsed = dict(row)
            songs.append(row_parsed)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a single song against user preferences and return (score, reasons).
    Required by recommend_songs() and src/main.py
    """
    reasons: List[str] = []

    # Read optional weights from user_prefs; fall back to defaults
    weights = user_prefs.get('weights', {}) if isinstance(user_prefs.get('weights', {}), dict) else {}
    genre_w = float(weights.get('genre', 2.0))
    mood_w = float(weights.get('mood', 1.0))
    numeric_scale = float(weights.get('numeric_scale', 2.0))

    # Genre and mood
    genre_pts = genre_w if user_prefs.get('genre') and song.get('genre') == user_prefs.get('genre') else 0.0
    if genre_pts > 0:
        reasons.append(f"genre match (+{genre_pts:.2f})")

    mood_pts = mood_w if user_prefs.get('mood') and song.get('mood') == user_prefs.get('mood') else 0.0
    if mood_pts > 0:
        reasons.append(f"mood match (+{mood_pts:.2f})")

    # Numeric similarity on energy (expect user_prefs to have 'energy' or 'target_energy')
    target_energy = float(user_prefs.get('energy') or user_prefs.get('target_energy') or 0.0)
    try:
        song_energy = float(song.get('energy') or 0.0)
    except Exception:
        song_energy = 0.0

    sigma = float(weights.get('sigma_energy', 0.15))
    score_energy = math.exp(- ((song_energy - target_energy) ** 2) / (2 * sigma * sigma))
    numeric_pts = numeric_scale * score_energy
    reasons.append(f"energy closeness (+{numeric_pts:.2f})")

    total = genre_pts + mood_pts + numeric_pts
    return total, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic; returns top-k scored songs.
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, List[str]]] = []
    for s in songs:
        score, reasons = score_song(user_prefs, s)
        scored.append((s, score, reasons))

    # sort by score descending (highest first)
    scored.sort(key=lambda x: x[1], reverse=True)

    results: List[Tuple[Dict, float, str]] = []
    for s, score, reasons in scored[:k]:
        explanation = "; ".join(reasons)
        results.append((s, score, explanation))

    return results
