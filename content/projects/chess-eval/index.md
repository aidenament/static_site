# Epoch Chess Eval

[< Back to Projects](/projects)

## Evaluating Out-of-Distribution Generalization with Chess Puzzles

I built 300 checkmate puzzles with progressively stranger rules, a knight that leaps (1,3), a rook that runs out of steam after four squares, to test whether frontier models are good at chess or just good at chess they've already seen. They generalize fine. Mate depth is what hurts them, weird rules don't, and the model with much worse reasoning is just as flat across the variants as the strongest one.

### Links

- [Results viewer](https://chess-eval-production.up.railway.app/) with all 300 puzzles, their prompts, every model answer, and the full reasoning traces
- [Source code](https://github.com/aidenament/chess-eval) on GitHub
- [The original report](/projects/chess-eval/Epoch_Chess_Eval.pdf) as a PDF

### Abstract

Frontier language models are trained heavily on domains like mathematics and software engineering. It is unclear how much of that performance comes from existing familiarity with tasks seen during training and how much of it generalizes to unfamiliar problems. I try to evaluate to what extent model capabilities generalize by using chess checkmate puzzles. This is a task that is seen during training, admits verifiable solutions, and allows for strange rule variants to piece movement for out-of-distribution puzzles. Puzzle difficulty is fixed within mate depth to isolate model generalization as the primary performance variable. The resulting benchmark comprises 300 puzzles spanning three mate depths and four tiers of increasing rules modifications. This benchmark is evaluated on GPT 5.6 Terra, Grok 4.5, and Gemini 3.6 flash. Accuracy clearly degrades with mate depth but is constant among rules modifications indicating that model performance does generalize to out-of-distribution variants. I tested lower reasoning variants of Terra, which score worse on ARC AGI 2, in an attempt to isolate a generalizability property, however even these lower reasoning variants have consistent scores among the modified puzzles, leading to the conclusion that the primary driver of performance is general capability.

### Introduction

Modern AI models are incredibly capable on the tasks they are trained on. Labs have invested immense resources training models on math and software engineering problems, and they have correspondingly gotten quite good at these domains. Not only do these models read the entire corpus of all human writing, they also receive dedicated post training on these tasks. So far this strategy has been incredibly effective at improving model capabilities.

The question arises though, how well do these models generalize beyond their training domains? Do they only do well because they've seen everything before in their training? There will always be novel tasks that, while perhaps similar to some existing problem the model is familiar with, have unique and different rules that must be accounted for. If models require being trained on every niche problem to gain proficiency, this would be a very significant limitation.

### Experimental Design

The goal of the experiment is to test how well frontier models actually generalize from in distribution to out of distribution tasks at a fixed level of difficulty. Fixing the difficulty is critical here in order to isolate the performance change from the distribution shift.

The task chosen to test on is chess puzzles. Models have undoubtedly seen significant chess material and strategy in their training data which provide a clean in distribution baseline to evaluate from. By benchmarking on puzzles with progressively weirder modifications and changes to the standard ruleset, we can see if performance actually degrades from the baseline.

Formally, this experiment is testing on mate in n puzzles. A mate in n puzzle is a specific kind of chess puzzle where the active player has exactly one move that leads to checkmate in n moves even with the best counterplay from their opponent. Every other move allows their opponent to avoid mate in the provided time. These puzzles are good candidates for benchmarking because they have a clear verifiable answer and allow for progressively extreme alterations to the rules.

For this benchmark I have mate in 1, mate in 2, and mate in 3 puzzles with white to move. These act as the primary difficulty tiers; it gets exponentially harder to find checkmate the deeper you have to look. That being said, there is still a considerable amount of variance in difficulty for a given mate level. This needs to be controlled in order to ensure the puzzles with modified rules aren't meaningfully harder or easier.

There are three key factors I used to determine the difficulty of a mate in n puzzle.

**1. The number of active pieces.** An active piece is one that is essential to the puzzle to work. Specifically, removing this piece ruins the puzzle by doing any of

- allowing multiple moves that lead to mate
- removing the ability for a mate to happen
- changing the correct move

This is pretty clear from the example below.

![A position where the queen and rook are active but the knight is not](/images/chess-eval/active-pieces.webp)

The queen and the rook are active, the puzzle cannot work without them, but the knight is not, the puzzle still works regardless of whether it's there. This is a reasonably good measure of puzzle difficulty because it represents the minimum number of pieces the model actually needs to process and track. A puzzle with 2 active pieces should be easier than one with 6.

**2. The number of responses from black after white's first move.** This is trivial for the mate in 1 puzzles, as black will always have 0 responses. But for the mate in 2 and 3 tiers, this number is much more relevant. More responses from black mean more paths the model has to search through in order to confirm the correct answer. Of course many black moves may be easily dismissable, but I still generally expect a puzzle with 10 responses from black to be more challenging than one with 2, an example of which is shown below.

![A sparse position offering black few responses](/images/chess-eval/defender-replies-few.webp)

![A crowded position offering black many responses](/images/chess-eval/defender-replies-many.webp)

**3. The total number of moves white has.** This is the weakest of the three proxies for difficulty, but is still important to ensure guessing remains a very weak strategy. The simple quality cap here is that all puzzles must have more than 15 legal moves.

By fixing these, we can ensure that the primary difficulty comes from the mate depth, and puzzles within a given depth should all be roughly the same difficulty regardless of the ruleset.

- Mate in 1 puzzles have exactly 5 active pieces, 0 defender responses
- Mate in 2 puzzles have 5 to 8 active pieces, 5 to 15 defender responses
- Mate in 3 puzzles have 8 to 11 active pieces, 5 to 15 defender responses

The next step is generating rules modifications. For each piece, excluding the king, I created a rules bank with 2 small, 2 medium, and 1 large alteration. I excluded the king because expanding or restricting his moves implicitly changes the difficulty of checkmate. The generation and categorization of these rules was probably the least rigorous part of this experiment. I created each rule by hand and categorized it roughly where I thought it should go. The distinction between what constitutes a small medium or large modification is admittedly subjective.

With the modifications in place, we now have a good way to generate progressively more out of distribution puzzles. Each mate difficulty has 4 tiers: base, tier 1, tier 2, and tier 3.

- Base puzzles have no modifications
- Tier 1 puzzles have 2 small modifications
- Tier 2 puzzles have 2 medium and 1 small modifications
- Tier 3 puzzles have 1 large and 2 medium modifications

Puzzle generation starts by picking the pieces for each player. Then based on the pieces, it randomly samples from the relevant rules. Finally, with a selected set of pieces and rules, random placements are tested until a mate in n puzzle with the desired properties is created. This process generated 25 puzzles at each of the 3 mate levels and 4 modification tiers, yielding 300 puzzles in total. There are some nuances to puzzle generation that are discussed in the appendix.

The evaluation pipeline itself was rather simple. The board state (in FEN format) and rules modifications were provided to the model, and the answer was extracted in UCI notation. I tested GPT 5.6 Terra, Grok 4.5, and Gemini 3.6 flash using OpenRouter. The primary factor here was picking models that were on the pareto frontier of cost and performance. With 300 puzzles, frontier models costing $1+/puzzle were clearly beyond the budget of this experiment. Each model was configured for the maximum allowable output tokens. Of note, 5.6 terra max had a tendency to think past its token limit and not answer. In this case, I would feed back the reasoning trace to a no reasoning variant and elicit an immediate answer. This would also be done if there was some parsing error in the model response. The goal of this benchmark is to give every model the best chance it can to answer the questions.

The full details of the experiment can be found in [this viewer](https://chess-eval-production.up.railway.app/).

![The results viewer showing puzzles, analytics, and reasoning traces](/images/chess-eval/results-viewer.webp)

It displays the analytics, the puzzles, their solutions, the rule modifications, the prompt for each puzzle, and the full model reasoning traces in an easily understandable format. All of the code can be found [here](https://github.com/aidenament/chess-eval) as well.

### Results

![Accuracy by condition across all five model configurations](/images/chess-eval/accuracy-by-condition.webp)

It seems that the models do generalize well on out of distribution puzzles with little drop among the tiers beyond what seems random noise. Mate depth does seem to be the primary difficulty lever, as we see clear degradation for deeper mates. But even for more difficult puzzles, the stranger rules variants do not seem to affect performance. This is good evidence that models do generalize well (and that puzzles are roughly the same difficulty). Also of note, the biggest drop observed, Terra (max) on the Tier 3 Mate in 3 puzzles, is partly due to Terra overthinking and requiring the majority of the responses to be salvaged.

On seeing these results, it is potentially the case that I didn't make the puzzles weird enough to elicit noticeable drop. Another potential flaw is that the rules bank has some duplicate rules between pieces. For example

- Rook can only move at most 4 squares along the ranks and files
- Bishops can only move at most 4 squares along the diagonals

A model that can generalize this type of movement for rooks will likely be able to do the same for the bishop. Thus my rules bank potentially lacked enough diversity to elicit truly out of distribution puzzles.

These are genuine concerns, but I think it more likely that the models indeed generalize well on board game style puzzles. Anecdotally, I find tier 3 puzzles to be more difficult, indicating that I probably don't generalize well out of distribution, even if the puzzles are theoretically equal in difficulty.

Seeing these results didn't surprise me too much. After all, this benchmark reminds me of [ARC AGI 2](https://arcprize.org/arc-agi/2) in that it tests models on novel, out of distribution, puzzles and models score quite well on this bench. Perhaps lower performance on ARC AGI would indicate weaker generalization capabilities, leading me to test GPT 5.6 Terra on medium and low reasoning.

![Accuracy by condition for Terra at max, medium, and low reasoning](/images/chess-eval/accuracy-by-reasoning-effort.webp)

My hypothesis was the existence of a "generalizability" property, and models that score low on this property (as seen from ARC AGI) would see more degradation in the stranger puzzle variants. This too appears not to be the case, as even GPT 5.6 terra low is flat along the modification tiers. There is no more falloff than medium or max despite markedly worse performance on ARC AGI.

The final results are informative if mundane. Models do generalize well on out of distribution puzzles, and the leading factor in performance is likely general capability (ECI) rather than some other "generalizability" property.

If I were to continue to work on this project, I would focus on generating extremely out of distribution puzzles. I'd also benchmark on more models to develop a clear understanding of the correlation between performance and ARC AGI or ECI. With the current model selection, the analysis is forced to make educated guesses from only a few data points.

### Appendix

One note for rules variations. Some puzzles have rules modifications that aren't actually used in the puzzle. Below is an example of two mate in 1 puzzles with the rule modification: a knight now moves (1,3) instead of the (1,2) movement.

![A puzzle that requires the modified knight movement](/images/chess-eval/rule-required.webp)

![A puzzle that works the same without the modification](/images/chess-eval/rule-unused.webp)

It is clear that the one on the left requires the rule in order to work and the one on the right doesn't.

We can use a similar concept of ablation, as was used to determine if a piece is active, to determine if a rule is active. If a puzzle works with the vanilla rule in place of the modification, the rule is not active. While the example above is a bit egregious, it doesn't seem obviously wrong that some puzzles don't use all or any of the rules, it still requires the model to know that the rules aren't relevant. That being said, I still required every tier to contain at least 50% of puzzles that actually require the novel ruleset. This was primarily relevant for the tier 1 puzzles, as nearly every tier 2 and tier 3 puzzle requires utilizing at least one extra rule.

For puzzles with modified but irrelevant rules, I benchmarked on the vanilla version to see if performance degraded just by adding the extra rules.

![Solve rates on inert-rule pairs, modified prompt versus vanilla prompt](/images/chess-eval/paired-presentations.webp)

As expected, performance on these pairs was nearly identical. Strangely Terra medium does markedly worse on the vanilla versions, but this is likely noise.

Furthermore, on the dashboard each rule for a modified puzzle is marked clearly so you can see how it is or isn't used.

### The Engine

That's the experiment. The code under it is a chess engine I wrote from scratch in standard library Python, because no chess library can represent a knight that leaps (1,3).

The thing that makes the rest work is that movement is a table, not code. Each piece gets a list of atoms: a leap to a fixed offset, or a ride along a direction with a range and a count of pieces it's allowed to pass over. A rule modification is a patch on that table, and standard chess plus a set of patches is just another ruleset. I hash the serialized ruleset and use the digest as its identity.

Attacks then reduce to one question: does any capturing atom on this side reach this square, under its own jump and blocking rules? Check, checkmate, stalemate, pins, castling through check and king flight squares all fall out of that predicate, which assumes nothing about normal geometry. Change how the knight moves and check changes with it, without touching any code.

The digest also salts the solver's memo table, which matters more than it sounds. Ablation means pulling a rule out and re-solving, and if the digest isn't in the memo key, that re-solve can hit an entry computed under the original rules.

A second, deliberately dumb solver checks the first: no memoization, no shared state, and it produces an actual refutation for every alternative first move instead of just declaring the solution unique.

198 tests. Published perft counts, move-for-move cross-validation against python-chess on hundreds of random positions plus fixtures for the cases engines get wrong, and a property test that the fast attack index and a naive scan agree across every square, both sides, 60 positions and 32 rulesets. python-chess shows up only in the tests, as a standard-rules oracle.
