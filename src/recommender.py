from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
        # Simple recommendation logic for the OOP part
        scored_songs = []
        for song in self.songs:
            score = 0.0
            if song.genre == user.favorite_genre:
                score += 1.0
            if song.mood == user.favorite_mood:
                score += 1.0
            score += (1.0 - abs(song.energy - user.target_energy))
            scored_songs.append((song, score))
        
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"it matches your favorite genre ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"it matches your mood ({song.mood})")
        if abs(song.energy - user.target_energy) < 0.2:
            reasons.append("the energy level is close to your preference")
        
        if not reasons:
            return "This song is a top pick based on overall popularity."
        return "Because " + " and ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of song dicts with numeric conversions and basic error handling."""
    import csv
    from pathlib import Path

    songs: List[Dict] = []
    path = Path(csv_path)

    if not path.exists():
        print(f"Error: CSV file not found: {csv_path}")
        return songs

    try:
        with path.open(newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row_number, row in enumerate(reader, start=2):
                try:
                    # Clean up string fields
                    title = (row.get('title') or '').strip()
                    artist = (row.get('artist') or '').strip()
                    genre = (row.get('genre') or '').strip()
                    mood = (row.get('mood') or '').strip()

                    # Parse numeric fields; allow ValueError to be caught per-row
                    song_id = int(row['id']) if row.get('id') not in (None, '') else None
                    energy = float(row['energy']) if row.get('energy') not in (None, '') else None
                    tempo_bpm = float(row['tempo_bpm']) if row.get('tempo_bpm') not in (None, '') else None
                    valence = float(row['valence']) if row.get('valence') not in (None, '') else None
                    danceability = float(row['danceability']) if row.get('danceability') not in (None, '') else None
                    acousticness = float(row['acousticness']) if row.get('acousticness') not in (None, '') else None

                    songs.append({
                        'id': song_id,
                        'title': title,
                        'artist': artist,
                        'genre': genre,
                        'mood': mood,
                        'energy': energy,
                        'tempo_bpm': tempo_bpm,
                        'valence': valence,
                        'danceability': danceability,
                        'acousticness': acousticness,
                    })
                except ValueError as e:
                    print(f"Warning: Skipping malformed row {row_number} in {csv_path}: {e}")
    except Exception as exc:
        print(f"Error reading CSV file {csv_path}: {exc}")

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Compute a transparent score and explanatory reasons for a single song given user preferences (genre, mood, energy)."""
    score = 0.0
    reasons: List[str] = []

    # Helper to safely read fields from either a dict or an object
    def _get_field(obj, key, default=None):
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    # Genre match: +2.0
    user_genre = user_prefs.get('genre') if isinstance(user_prefs, dict) else getattr(user_prefs, 'favorite_genre', None)
    song_genre = _get_field(song, 'genre')
    if user_genre and song_genre == user_genre:
        score += 2.0
        reasons.append('Matched favorite genre: +2.0')

    # Mood match: +1.0
    user_mood = user_prefs.get('mood') if isinstance(user_prefs, dict) else getattr(user_prefs, 'favorite_mood', None)
    song_mood = _get_field(song, 'mood')
    if user_mood and song_mood == user_mood:
        score += 1.0
        reasons.append('Matched favorite mood: +1.0')

    # Energy similarity: award (1.0 - energy_gap), clamped to >= 0
    # Support both dict keys 'energy' or 'target_energy' and dataclass attribute 'target_energy'
    if isinstance(user_prefs, dict):
        user_energy = user_prefs.get('target_energy', user_prefs.get('energy', 0.0))
    else:
        user_energy = getattr(user_prefs, 'target_energy', getattr(user_prefs, 'target_energy', 0.0))

    song_energy = _get_field(song, 'energy', 0.0)
    try:
        song_energy = float(song_energy)
    except (TypeError, ValueError):
        song_energy = 0.0
    try:
        user_energy = float(user_energy)
    except (TypeError, ValueError):
        user_energy = 0.0

    energy_gap = abs(song_energy - user_energy)
    energy_points = max(0.0, 1.0 - energy_gap)
    score += energy_points
    reasons.append(f"Energy similarity: +{energy_points:.3f} (gap={energy_gap:.3f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Dict]:
    """Score and rank songs using `score_song()` and return the top-k song dictionaries annotated with `score` and `reasons`."""
    scored: List[Dict] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)

        # Produce a dictionary representation of the song without mutating
        # the original input item. Support both dicts and dataclass objects.
        if isinstance(song, dict):
            song_dict = song.copy()
        else:
            # Fallback for objects (e.g., dataclass `Song`)
            song_dict = {
                'id': getattr(song, 'id', None),
                'title': getattr(song, 'title', ''),
                'artist': getattr(song, 'artist', ''),
                'genre': getattr(song, 'genre', ''),
                'mood': getattr(song, 'mood', ''),
                'energy': getattr(song, 'energy', 0.0),
                'tempo_bpm': getattr(song, 'tempo_bpm', None),
                'valence': getattr(song, 'valence', None),
                'danceability': getattr(song, 'danceability', None),
                'acousticness': getattr(song, 'acousticness', None),
            }

        song_dict['score'] = score
        song_dict['reasons'] = reasons
        scored.append(song_dict)

    # Sort descending by score and return top-k
    ranked = sorted(scored, key=lambda s: s['score'], reverse=True)
    return ranked[:k]
