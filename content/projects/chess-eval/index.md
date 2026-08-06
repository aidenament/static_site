# Out-of-Distribution Generalization in Chess Puzzles

[< Back to Projects](/projects)

## An LLM Evaluation on Mate-in-n Puzzles Under Modified Movement Rules

Frontier language models are trained heavily on domains like mathematics and software engineering. It is unclear how much of that performance comes from familiarity with tasks seen during training, and how much of it generalizes to unfamiliar problems.

This project measures that using chess checkmate puzzles: a task that appears in training data, admits verifiable solutions, and allows strange rule variants that push a puzzle out of distribution. Difficulty is held fixed within each mate depth so that generalization is the primary variable. The resulting benchmark is 300 puzzles spanning three mate depths and four tiers of increasing rules modifications, evaluated on GPT-5.6 Terra, Grok 4.5, and Gemini 3.6 Flash.

Accuracy degrades clearly with mate depth, but stays flat across the rules modifications, indicating that performance does generalize to out-of-distribution variants. Testing lower reasoning variants of Terra, which score worse on ARC-AGI-2, did not isolate a generalizability property either: those variants are equally flat across modified puzzles. The most likely conclusion is that the primary driver of performance is general capability.

### Links

- [Results viewer](https://chess-eval-production.up.railway.app/) with all 300 puzzles, their prompts, every model answer, and the full reasoning traces
- [Source code](https://github.com/aidenament/chess-eval) on GitHub
- [The original report](/projects/chess-eval/Epoch_Chess_Eval.pdf) as a PDF

### Introduction

Modern models are enormously capable on tasks they are trained on. Labs have invested heavily in training on math and software engineering problems, and models have correspondingly become good at those domains. They read the entire corpus of human writing and then receive dedicated post-training on these tasks, and so far that strategy has been very effective.

The question is how well models generalize beyond their training domains. Do they perform well only because they have seen everything before? There will always be novel tasks that resemble a familiar problem but carry unique rules that must be accounted for. If a model needs to be trained on every niche problem to gain proficiency, that is a significant limitation.

### Experimental Design

The goal is to test how well frontier models generalize from in-distribution to out-of-distribution tasks at a fixed level of difficulty. Fixing difficulty is critical, because it is what isolates the performance change caused by the distribution shift.

The task is mate-in-n puzzles. A mate-in-n puzzle is one where the active player has exactly one move leading to checkmate in n moves against best defense; every other move lets the opponent escape. These make good benchmark items because the answer is verifiable and the ruleset can be altered progressively.

The benchmark uses mate-in-1, mate-in-2, and mate-in-3 puzzles with white to move. These are the primary difficulty tiers, since finding checkmate gets exponentially harder the deeper you have to look. There is still considerable variance in difficulty within a given mate depth, and that has to be controlled so the modified puzzles are not accidentally harder or easier.

Three factors determine the difficulty of a mate-in-n puzzle.

**1. The number of active pieces.** An active piece is one the puzzle needs. Removing it ruins the puzzle, by allowing multiple mating moves, removing the mate entirely, or changing the correct move.

![A position where the queen and rook are active but the knight is not](/images/chess-eval/active-pieces.webp)

The queen and the rook are active, since the puzzle cannot work without them. The knight is not: the puzzle still works whether or not it is there. This is a reasonable difficulty measure because it counts the pieces the model actually has to process and track. A puzzle with two active pieces should be easier than one with six.

**2. The number of replies available to black after white's first move.** This is trivial for mate-in-1, where black never replies, but matters for the deeper tiers. More replies mean more paths the model has to search to confirm its answer. Many of them may be easy to dismiss, but a puzzle with ten replies should still be harder than one with two.

![A sparse position offering black few replies](/images/chess-eval/defender-replies-few.webp)

![A crowded position offering black many replies](/images/chess-eval/defender-replies-many.webp)

**3. The total number of moves available to white.** This is the weakest of the three proxies, but it keeps guessing from being a viable strategy. Every puzzle must offer white more than fifteen legal moves.

Fixing these ensures the primary difficulty comes from mate depth, and that puzzles within a depth are roughly equal regardless of ruleset:

- Mate-in-1 puzzles have exactly 5 active pieces and 0 defender replies
- Mate-in-2 puzzles have 5 to 8 active pieces and 5 to 15 defender replies
- Mate-in-3 puzzles have 8 to 11 active pieces and 5 to 15 defender replies

### Generating the Rule Modifications

For each piece except the king, I wrote a rules bank containing two small, two medium, and one large alteration. The king is excluded because expanding or restricting its movement implicitly changes how hard checkmate is, which would confound the treatment with the variable being controlled.

Generating and categorizing these rules was the least rigorous part of the experiment. Each rule was written by hand and sorted roughly where I judged it belonged, and the boundary between a small, medium, and large modification is admittedly subjective.

With the modifications in place, each mate depth gets four tiers:

- **Base** puzzles have no modifications
- **Tier 1** puzzles have 2 small modifications
- **Tier 2** puzzles have 2 medium and 1 small modification
- **Tier 3** puzzles have 1 large and 2 medium modifications

Puzzle generation picks the pieces for each player first, then samples the relevant rules based on which pieces are present, then tests random placements until a mate-in-n puzzle with the desired properties appears. This produced 25 puzzles at each of the 3 mate levels and 4 modification tiers, for 300 in total.

The evaluation pipeline is simple. The board state in FEN notation and the rules modifications are given to the model, and the answer is extracted in UCI notation. I tested GPT-5.6 Terra, Grok 4.5, and Gemini 3.6 Flash through OpenRouter, choosing models on the Pareto frontier of cost and performance; at 300 puzzles, frontier models costing over a dollar per puzzle were beyond the budget. Each model was configured for its maximum allowable output tokens.

Terra at maximum reasoning had a tendency to think past its token limit without answering. In that case I fed the reasoning trace back to a no-reasoning variant and elicited an immediate answer, and did the same when a response failed to parse. The goal of the benchmark is to give every model the best chance it can to answer.

![The results viewer showing puzzles, analytics, and reasoning traces](/images/chess-eval/results-viewer.webp)

The [results viewer](https://chess-eval-production.up.railway.app/) displays the analytics, the puzzles, their solutions, the rule modifications, the prompt for each puzzle, and the full model reasoning traces.

### Results

![Accuracy by condition across all five model configurations](/images/chess-eval/accuracy-by-condition.webp)

Models generalize well on out-of-distribution puzzles, with little drop across the tiers beyond what looks like random noise. Mate depth is the primary difficulty lever, and there is clear degradation for deeper mates. But even for the harder puzzles, the stranger rules variants do not appear to affect performance. That is good evidence both that models generalize and that the puzzles really are of comparable difficulty. The largest drop observed, Terra at maximum reasoning on tier 3 mate-in-3, is partly explained by Terra overthinking and needing most of those responses salvaged.

Seeing these results, it is possible I did not make the puzzles weird enough to produce a noticeable drop. Another potential flaw is that the rules bank contains some duplicate rules across pieces. For example:

- A rook can only move at most 4 squares along ranks and files
- A bishop can only move at most 4 squares along the diagonals

A model that generalizes this kind of movement change for rooks will likely manage it for bishops too, so the rules bank may have lacked the diversity needed to produce genuinely out-of-distribution puzzles.

These are real concerns, but I think it more likely that models simply do generalize well on board-game-style puzzles. Anecdotally I find the tier 3 puzzles harder myself, which suggests I do not generalize well out of distribution even when the puzzles are theoretically equal in difficulty.

The results were not especially surprising. This benchmark resembles [ARC-AGI-2](https://arcprize.org/arc-agi/2) in that it tests models on novel out-of-distribution puzzles, and models score well on that benchmark. If lower ARC-AGI performance indicated weaker generalization, that would show up here, which led me to test GPT-5.6 Terra at medium and low reasoning.

![Accuracy by condition for Terra at maximum, medium, and low reasoning](/images/chess-eval/accuracy-by-reasoning-effort.webp)

My hypothesis was that a "generalizability" property exists, and that models scoring low on it would degrade more on the stranger variants. That also appears not to be the case. Even Terra at low reasoning is flat along the modification tiers, with no more falloff than medium or maximum despite markedly worse ARC-AGI performance.

The final results are informative if mundane. Models do generalize well on out-of-distribution puzzles, and the leading factor in performance is general capability rather than some separate generalizability property.

If I continued this project, I would focus on generating far more out-of-distribution puzzles, and benchmark more models to develop a clearer picture of the correlation between performance and ARC-AGI. With the current model selection, the analysis is forced to make educated guesses from only a few data points.

### Appendix: Rules That Are Never Used

Some puzzles carry rules modifications that the solution does not actually depend on. Below are two mate-in-1 puzzles that both carry the modification that a knight moves (1,3) instead of (1,2).

![A puzzle whose solution requires the modified knight movement](/images/chess-eval/rule-required.webp)

![A puzzle that works identically without the modification](/images/chess-eval/rule-unused.webp)

The first requires the rule for the puzzle to work; the second does not.

The same ablation idea used to decide whether a piece is active also decides whether a rule is active: if the puzzle still works with the vanilla rule in place of the modification, the rule is not active. While the example above is somewhat egregious, it does not seem obviously wrong for some puzzles not to use all of their rules, since the model still has to work out that the rules are irrelevant. Even so, I required every tier to contain at least 50% of puzzles that genuinely need the novel ruleset. This mattered mostly for tier 1, since nearly every tier 2 and tier 3 puzzle uses at least one extra rule.

For puzzles with modified but irrelevant rules, I benchmarked the vanilla version as well, to see whether performance degraded purely from the presence of extra rules in the prompt.

![Solve rates on inert-rule pairs, modified prompt versus vanilla prompt](/images/chess-eval/paired-presentations.webp)

As expected, performance on these pairs was nearly identical. Terra at medium reasoning does markedly worse on the vanilla versions, but that is likely noise. On the dashboard, each rule for a modified puzzle is marked clearly so you can see how it is or is not used.

### The Engine

The measurement only means something if the modified puzzles are genuinely valid and clear the same difficulty bar, which is where most of the engineering went.

**No chess library anywhere in the pipeline.** This is forced rather than stylistic. A reference implementation cannot represent a knight that leaps (1,3), so it would be wrong the moment the first rule changes. The engine is written from scratch in pure standard library Python. python-chess appears only in the test suite, as a standard-rules oracle.

**Movement is data, not code.** Each piece's movement is a list of atoms: a leap to a fixed offset, or a ride along a direction with a range and a count of occupied squares it may pass over. Each atom carries a modality, since pawns move and capture differently. A rule modification is a declarative patch on that table, and composing standard chess with a set of patches yields a ruleset whose canonical serialization is hashed into a digest that serves as its identity.

**Attacks and legality reduce to one predicate.** Check, checkmate, stalemate, pins, castling through check, and king flight squares all derive from a single question: does any capture-modality atom of the given side reach this square, under that atom's own jump and blocking semantics. That predicate assumes nothing about standard geometry, so modifying a knight automatically changes what counts as check with no code change anywhere.

The four special rules, castling, en passant, promotion, and the pawn double-step, are held at their standard forms in every condition. Even so, the double-step is derived rather than hardcoded: it exists only if the pawn's atom list still contains a straight forward step, so a rule removing that step also removes the double advance and its en passant target.

**The ruleset digest salts the solver's memoization.** Deciding whether a rule matters means removing it and re-solving. If the memo table were not keyed by ruleset digest, that re-solve could hit an entry computed under the original rules, and the measurement would be quietly wrong.

**A second solver checks the first.** A separate checker re-derives every puzzle's classification with a deliberately naive search: no memoization, no move ordering, no shared state. It also produces a concrete refutation for every alternative first move rather than simply asserting the solution is unique. The two are independent at the level of search; both rest on the same move generator, which is covered instead by perft counts, cross-validation, and unit tests.

### Verification

The suite is 198 tests, 179 of them on the engine. These include published perft counts at several depths, move-for-move cross-validation against python-chess over hundreds of random positions plus fixtures chosen for the cases engines get wrong, such as en passant that would expose the king along a rank and castling through an attacked square, and a property test asserting that the fast attack index and a naive scan agree across every square, both sides, sixty positions, and thirty-two rulesets.

One suite exists specifically to catch cheating. It builds rulesets that carry the full modification machinery, with a different digest and reordered atoms, but which are extensionally standard, then asserts the generated moves match standard chess exactly. That catches any fast path keyed on whether a ruleset is modified, and any dependence on the order atoms happen to appear in.

The evaluation produced 1,700 graded responses over roughly 34 million reasoning tokens.
