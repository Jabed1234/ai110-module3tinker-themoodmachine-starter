# Model Card - Mood Machine (prototype)

## Limitations and Bias

- The dataset is very small (10 songs), and genres like `pop` are relatively frequent; the recommender therefore tends to surface pop tracks often, which can create a popularity/genre bias.
- The scoring logic places explicit weight on genre (default 2.0 points), so cross-genre matches that nevertheless fit a user's numerical preferences (energy/valence) can be under-ranked.
- Mood tags are hand-labeled and subjective; inconsistencies in `mood` values can mislead the scoring rule.
- This prototype uses surface-level audio descriptors (energy) and does not include learned embeddings or lyrics, limiting semantic understanding and novelty.

## Evaluation (experiment summary)

We tested several user profiles to see whether the recommender behaves as expected and to surface edge-cases.

- Profiles tested: "High-Energy Pop", "Chill Lofi", "Deep Intense Rock", and an adversarial "Conflicting (HighEnergy + Sad)" profile.
- Observations: For genre-aligned profiles (e.g., Chill Lofi), the top results strongly match both genre and energy, which is expected because genre match contributes a large fixed bonus and energy closeness scales the score. For conflicting profiles, genre often dominates (users asking for high energy but a 'moody' mood still received pop tracks if genre matched). This indicates genre weight may be too strong relative to numeric similarity for some use cases.
- Experimental change: increasing numeric importance (numeric_scale from 2.0 to 4.0) caused songs with closer energy to bubble up even if genre match was reduced, improving alignment with pure energy-driven intents but sometimes reducing genre coherence.

## Recommendations

- To reduce filter bubbles, lower the genre weight or mix in a diversity term at ranking time.
- To improve content understanding, add audio embeddings (OpenL3/VGGish) and textual features (lyrics) and incorporate collaborative signals.

## Model Card

Model Name: Mood Machine v0.1

Goal / Task:

- Suggest 3–5 songs from a small catalog that match a user's stated genre, mood, and target energy.

Data Used:

- A small CSV catalog with 10 starter songs (title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness).
- The dataset is tiny and hand-curated for classroom exploration only.

Algorithm Summary:

- Each song is scored by combining: a genre bonus (default +2.0), a mood bonus (default +1.0), and a numeric similarity score based on energy (Gaussian kernel scaled to contribute up to +2.0 by default).
- Scores are summed to produce a single scalar per song. The top-scoring items are returned. A simple experiment allows changing weights (e.g., increase numeric importance).

Observed Behavior / Biases:

- The system strongly favors songs that match the user's genre because genre gives a fixed bonus. This can hide good cross-genre matches.
- Mood labels are subjective and can be noisy; the recommender relies on them but also uses numeric features like energy to reduce noise.
- Small catalog size exaggerates popularity/genre effects and reduces diversity.

Evaluation Process:

- I tested multiple user profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock, and a conflicting HighEnergy+Moody profile).
- I ran an experiment increasing numeric weight to see how rankings change. Results were inspected qualitatively and documented in `reflection.md` and `README.md`.

Intended Use and Non-Intended Use:

- Intended: educational demo of content-based recommendation ideas and a basis for experimentation.
- Not intended: production recommendations, accurate personalized music recommendations, or deployment to real users.

Ideas for Improvement:

- Add more songs and real user interaction logs to learn collaborative signals.
- Use audio embeddings (OpenL3/VGGish) and text features (lyrics) for richer similarity.
- Add ranking-level diversity or novelty constraints and tune weights with A/B testing.

Personal Reflection

- Biggest learning: small, transparent scoring rules make behavior easy to reason about and test. Fixed bonuses (genre/mood) are powerful levers.
- AI tools helped generate prompts, suggestions, and documentation structure, but I verified and edited all code and explanations manually.
- I was surprised how a simple energy-based Gaussian score combined with a genre bonus can produce recommendations that "feel" right for many profiles.
- Next: expand the catalog, add embeddings, and run simple offline metrics (precision@k) with simulated or collected labels.

