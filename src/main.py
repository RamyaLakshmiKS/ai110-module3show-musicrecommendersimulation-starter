"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_profile_header(profile_name: str, user_prefs: dict) -> None:
    """Print a formatted header for a user profile."""
    print("\n" + "=" * 70)
    print(f"PROFILE: {profile_name}")
    print("=" * 70)
    print(f"Preferences: {user_prefs}")
    print("-" * 70)


def print_recommendations(recommendations: list) -> None:
    """Print formatted recommendations with scores and reasons."""
    print("\nTop recommendations:\n" + "=" * 60)
    for idx, rec in enumerate(recommendations, start=1):
        # `rec` is a dict with original song attributes plus `score` and `reasons`.
        title = rec.get('title', '<unknown>')
        artist = rec.get('artist') or ''
        score = rec.get('score', 0.0)
        reasons = rec.get('reasons') or []

        # Header line with index, title and score
        print(f"\n{idx}. {title} — Score: {score:.2f}")
        if artist:
            print(f"   Artist: {artist}")

        # Bulleted reasons to explain the recommendation
        print("   Reasons:")
        if reasons:
            for r in reasons:
                print(f"     - {r}")
        else:
            print("     - overall match")

        # Separator between recommendations
        print("\n" + ("-" * 60))


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"🎵 Music Recommender Stress Test - Loaded {len(songs)} songs\n")

    # Define diverse user profiles for stress testing
    test_profiles = [
        {
            "name": "High-Energy Pop",
            "prefs": {"genre": "pop", "mood": "happy", "energy": 0.8}
        },
        {
            "name": "Chill Lofi",
            "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.35}
        },
        {
            "name": "Deep Intense Rock",
            "prefs": {"genre": "rock", "mood": "intense", "energy": 0.9}
        },
        {
            "name": "Conflicting Preferences (High Energy + Chill Mood)",
            "prefs": {"genre": "ambient", "mood": "chill", "energy": 0.95}
        },
        {
            "name": "Classical Ethereal",
            "prefs": {"genre": "classical", "mood": "ethereal", "energy": 0.3}
        },
        # Edge cases: designed to challenge the recommender
        {
            "name": "[EDGE CASE] Intense but Low Energy (Contradiction)",
            "prefs": {"genre": "rock", "mood": "intense", "energy": 0.1}
        },
        {
            "name": "[EDGE CASE] Non-Existent Mood + Genre",
            "prefs": {"genre": "rock", "mood": "sad", "energy": 0.5}
        },
        {
            "name": "[EDGE CASE] Extreme Low Energy",
            "prefs": {"genre": "pop", "mood": "happy", "energy": 0.01}
        },
        {
            "name": "[EDGE CASE] Extreme High Energy",
            "prefs": {"genre": "ambient", "mood": "chill", "energy": 1.0}
        },
        {
            "name": "[EDGE CASE] Minimal Preferences (Genre Only)",
            "prefs": {"genre": "jazz"}
        },
    ]

    # Run recommender for each profile
    for profile in test_profiles:
        print_profile_header(profile["name"], profile["prefs"])
        recommendations = recommend_songs(profile["prefs"], songs, k=5)
        print_recommendations(recommendations)

    print("\n" + "=" * 70)
    print("STRESS TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
