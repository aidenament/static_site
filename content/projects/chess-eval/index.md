# Out-of-Distribution Generalization in Chess Puzzles

[< Back to Projects](/projects)

## An LLM Evaluation on Mate-in-n Puzzles Under Modified Movement Rules

Frontier models are trained heavily on mathematics and software engineering, and they are very good at both. How much of that comes from having seen the task before, and how much of it generalizes to problems the training data never covered?

This project builds an instrument to measure that. Chess mate-in-n puzzles make a useful probe: models have certainly read a great deal of chess, the answer is verifiable, and the rules can be altered to push a puzzle progressively further from anything in the training distribution. Each puzzle comes in one of four conditions, from standard chess through three tiers of increasingly strange movement rules, such as a knight that leaps (1,3) instead of (1,2). Difficulty is held fixed across all four by an identical quality floor, so a drop in solve rate would measure distance from the distribution rather than a harder puzzle.

### Links

- [Results viewer](https://chess-eval-production.up.railway.app/) for all 300 puzzles, their prompts, every model answer, and the full reasoning traces
- [Source code](https://github.com/aidenament/chess-eval) on GitHub
- [Full report](/projects/chess-eval/Epoch_Chess_Eval.pdf) as a PDF, also embedded at the bottom of this page

### The Result

The effect I set out to find is not there. Across 300 puzzles and five model configurations, solve rate does not fall as the rules get stranger. The curves are flat or non-monotone, and tier 2 is frequently the best condition rather than the worst: GPT-5.6 Terra at maximum reasoning scores 80%, 84%, 89%, then 77% across the four tiers, and Grok 4.5 scores 47%, 48%, 61%, 55%.

What does drive performance is search depth. Pooled across conditions, models solve between 86% and 100% of mate-in-1 puzzles, between 38% and 98% of mate-in-2, and between 12% and 50% of mate-in-3. Depth dominates; distance from the training distribution does not show up at all.

I then tested a narrower hypothesis, that there is some distinct "generalizability" property and that models scoring poorly on ARC-AGI would degrade more on the strange variants. Running GPT-5.6 Terra at low, medium, and maximum reasoning did not support it either. The low-reasoning configuration is just as flat across tiers as the maximum one, despite far worse ARC-AGI performance. The most likely reading is that general capability, not a separate generalization faculty, is what carries these puzzles.

This is a null result, and it is worth being precise about how much weight it can hold. See the limitations below.

### The Engine

The measurement only means anything if the modified puzzles are genuinely valid and genuinely equal in difficulty, which is where most of the work went.

**No chess library anywhere in the pipeline.** This is forced rather than stylistic. A reference implementation cannot represent a knight that leaps (1,3), so it would be wrong the moment the first rule is modified. The engine is written from scratch in pure standard-library Python. python-chess appears in exactly two files, both tests, where it serves as a standard-rules oracle.

**Movement is data, not code.** Each piece's movement is a list of atoms: a `leap` to a fixed offset, or a `ride` along directions with a range and a count of occupied squares it may pass over. A rule modification is a declarative patch on that table. Composing standard chess with a set of patches produces a ruleset, whose canonical JSON is hashed into a digest that serves as its identity.

**Everything reduces to one predicate.** Check, checkmate, stalemate, pins, castling through check, and king flight squares are all derived from `attacked(square, side, occupancy)`, true when some capture-modality atom of that side reaches the square under its own jump semantics. Nothing assumes standard geometry, so modifying a knight automatically changes what counts as check with no code change anywhere. The same idea extends to special rules: a pawn's two-square advance exists only if its atom list actually contains a forward step, so a rule removing that step also removes the double-step and its en-passant target, with no special-casing.

**The digest is the memoization salt.** This detail matters more than it looks. Measuring whether a rule was actually used means removing it and re-solving. If the solver's memo table were not salted by the ruleset digest, that re-solve could hit an entry computed under the original rules, and the measurement would be silently wrong.

**A second solver that distrusts the first.** A separate checker re-derives every puzzle's classification using a deliberately naive search, with no memoization, no move ordering, and no shared state, so that a bug in the fast solver cannot quietly agree with itself. It also produces a concrete refutation for every alternative first move rather than merely asserting the solution is unique. The independence is at the search level: both share the same move generator, whose assurance comes instead from perft values, cross-validation against python-chess, and unit tests.

**One ablation mechanism, three uses.** Remove a piece and re-solve to learn whether it was essential, which is the project's difficulty measure. Remove one rule and re-solve to learn whether that rule was causally load-bearing. Re-solve under fully standard rules to learn whether the puzzle is secretly a normal chess puzzle. All three are the same operation: perturb the input, re-classify, compare.

That last bit enables the nicest part of the design. Puzzles that are provably identical under standard rules get presented twice, once with the modified rules text and once with ordinary text, which separates degradation caused by strange rules appearing in the prompt from degradation caused by having to calculate with them.

### Limitations

The honest reading of a null result depends on saying what it cannot rule out.

- **The eval is underpowered by its own pre-registered numbers.** The design notes estimate that roughly 165 to 350 puzzles per arm are needed for 80% power against a 10 to 15 percentage point drop. Each condition-depth cell holds 25.
- **There is no statistical analysis in the repository.** The dashboard reports raw ratios. Significance tests, effect sizes, and the planned paired analysis are described in the design document but not implemented, so nothing here is a measured effect size.
- **One sample per puzzle.** Every configuration ran each presentation once, so model noise cannot be separated from real differences.
- **The paired comparison is small and unbalanced.** Only 40 of 225 modified puzzles qualify, and they concentrate in tier 1.
- **The rules may simply not be strange enough.** Size labels are hand-assigned judgment calls, and several modifications are structurally similar across pieces, so a model generalizing one likely generalizes another.
- **Scale.** This is a single run over 300 puzzles and 1,700 model responses across three model families, not a benchmark.

### Scale and Verification

The bank holds 300 puzzles, 25 in each of twelve cells, built from 25 hand-authored rule modifications covering every piece except the king. Kings are deliberately never modified, since changing king mobility would alter how hard checkmate is and confound the treatment with the variable being controlled.

The engine and harness come to roughly 3,700 lines, with another 2,300 lines of tests. The 198 tests include published perft values at several depths, move-for-move cross-validation against python-chess over hundreds of random and adversarially chosen positions, and a property test asserting that the fast attack index and the naive scan agree across every square, both sides, sixty positions, and thirty-two rulesets.

The evaluation itself produced 1,700 graded responses over roughly 34 million reasoning tokens, at about $372 in API spend.

### Full Report

You can view the report below or [download it directly](/projects/chess-eval/Epoch_Chess_Eval.pdf).

```pdf
/projects/chess-eval/Epoch_Chess_Eval.pdf
```
