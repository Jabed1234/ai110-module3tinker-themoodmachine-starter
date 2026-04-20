"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Define several diverse user profiles for evaluation
    profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
        },
        # An adversarial/conflicting profile to test behavior
        "Conflicting (HighEnergy + Sad)": {
            "genre": "pop",
            "mood": "moody",
            "energy": 0.95,
        },
    }

    # Baseline run for each profile
    for name, prefs in profiles.items():
        print(f"\n=== Profile: {name} ===")
        recs = recommend_songs(prefs, songs, k=5)
        for idx, (song, score, explanation) in enumerate(recs, start=1):
            print(f"{idx}. {song.get('title','Unknown Title')}  —  Score: {score:.2f}")
            reasons = [r.strip() for r in explanation.split(';') if r.strip()]
            if reasons:
                print("   Reasons:")
                for r in reasons:
                    print(f"     - {r}")
            else:
                print("   Reasons: (none)")
        print()

    # Experimental run: Weight shift (double numeric importance, half genre)
    exp_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "weights": {"genre": 1.0, "mood": 1.0, "numeric_scale": 4.0}}
    print("\n=== Experimental Profile: Higher numeric weight (energy) ===")
    exp_recs = recommend_songs(exp_prefs, songs, k=5)
    for idx, (song, score, explanation) in enumerate(exp_recs, start=1):
        print(f"{idx}. {song.get('title','Unknown Title')}  —  Score: {score:.2f}")
        reasons = [r.strip() for r in explanation.split(';') if r.strip()]
        if reasons:
            print("   Reasons:")
            for r in reasons:
                print(f"     - {r}")
        else:
            print("   Reasons: (none)")
    print()


if __name__ == "__main__":
    main()
