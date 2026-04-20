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

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for idx, rec in enumerate(recommendations, start=1):
        # (song_dict, score, explanation_str)
        song, score, explanation = rec
        print(f"{idx}. {song.get('title','Unknown Title')}  —  Score: {score:.2f}")
        # split reasons and print each on its own indented line for readability
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
