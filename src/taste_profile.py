"""Default taste profile for the music recommender simulation.

This module exposes a single default profile dict and a small helper
to return a copy for use in experiments.
"""

from copy import deepcopy


DEFAULT_TASTE_PROFILE = {
    "user_id": "user_001",
    "liked_song_ids": [2, 4, 9],
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_tempo_bpm": 78,
    "target_valence": 0.58,
    "target_danceability": 0.60,
    "target_acousticness": 0.78,
    "feature_weights": {
        "genre": 2.0,
        "mood": 1.5,
        "energy": 1.0,
        "tempo": 0.8,
        "valence": 0.8,
        "danceability": 0.6,
        "acousticness": 0.6,
    },
    "tolerance": {
        "energy": 0.12,
        "tempo_bpm": 10,
        "valence": 0.15,
        "danceability": 0.15,
        "acousticness": 0.15,
    },
}


def get_default_taste_profile(copy_profile: bool = True):
    """Return the default taste profile.

    If `copy_profile` is True (default) a deep copy is returned so callers
    can mutate the profile without changing the module-level constant.
    """
    return deepcopy(DEFAULT_TASTE_PROFILE) if copy_profile else DEFAULT_TASTE_PROFILE


__all__ = ["DEFAULT_TASTE_PROFILE", "get_default_taste_profile"]
