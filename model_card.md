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
