Reflection on profile comparisons

- High-Energy Pop vs Chill Lofi:
  - High-Energy Pop surfaced upbeat pop tracks like "Sunrise City" and "Gym Hero" because genre match (+2) plus high energy closeness boosted those items.
  - Chill Lofi prioritized lofi tracks ("Library Rain", "Midnight Coding") where both genre and low energy matched the profile. This shows the system correctly blends categorical anchors and numeric closeness.

- Deep Intense Rock vs Chill Lofi:
  - Deep Intense Rock strongly favored "Storm Runner" (rock, intense, high energy) showing genre+mood+energy alignment yields clear winners.
  - Chill Lofi did not surface rock tracks because genre mismatch removed the +2 bonus, even when energy might have been similar for some tracks.

- Conflicting profile (High energy + moody):
  - This profile exposed a ranking bias: genre match and energy closeness still pushed pop tracks to the top despite the moody mood tag. It suggests mood is a weaker, softer constraint relative to genre and numeric fit.

Overall takeaways:
- The recommender behaves predictably given the scoring recipe: fixed categorical bonuses have a large effect, and numeric closeness fine-tunes ordering.
- In small catalogs, genre priors dominate and can hide credible cross-genre matches; balancing weights and adding diversity constraints would improve perceived quality.
