"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

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


if __name__ == "__main__":
    main()
