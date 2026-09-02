### Behavioral/readout redesign — frozen before experiment

The preregistered binary suppression criterion (`0/10` ordinary-chat recovery and
`>=1/10` NT0 recovery) yielded only 3/368 qualifying facts across two independent
Qwen3.5-4B development cases and was rejected before inspecting any lens outputs.

Qwen3.5-27B is now the primary experimental organism. The earlier Qwen3.5-4B runs are treated as development/pilot data; any 4B→27B differences are exploratory model-variant comparisons, not clean parameter-scaling evidence.

Tiananmen remains held out from development and will only be opened after the behavioral and lens-analysis pipeline is frozen on the development topics.

Fact target tokens are selected mechanically from the benchmark fact text before lens inspection, using the preregistered lexical-selection rule; behavioral correctness judgments do not use those target tokens.

For every benchmark atomic fact f:

    A_chat(f) = k_chat(f) / 10
    A_NT0(f)  = k_NT0(f) / 10
    DeltaA(f) = A_NT0(f) - A_chat(f)

DeltaA is the primary behavioral quantity and is interpreted as the change in
factual accessibility under the complete NT0 elicitation protocol, not as a pure
measure of censorship. In particular, NT0 produces substantially longer responses,
which is retained as an interpretive limitation.

All benchmark facts are retained in the primary analysis, including facts recovered
in 0/20 behavioral samples. A secondary sensitivity analysis excludes 0/20 facts.
No threshold on DeltaA is used. Explicit contradictions are recorded separately.

Lens readout always uses a single fixed context independent of the behavioral
conditions: the benchmark question rendered with the ordinary chat template
(`enable_thinking=False`). J-Lens, R-Lens, and logit lens receive the identical
rendered token sequence and are scored at the final prompt token. No generated
chat or NT0 response enters the lens context.

"Early layers" means the first half of transformer blocks, matching the R-Lens
evaluation convention: layers 0–15 for Qwen3.5-4B and 0–31 for Qwen3.5-27B.

For each fact and layer, fact rank is the best rank among its mechanically selected
target tokens. For lens L:

    E_L(f)  = mean_early_layers log(rank_L(f, layer))
    D_RJ(f) = E_J(f) - E_R(f)

Positive D_RJ therefore indicates an R-Lens advantage.

Primary hypothesis:
facts with larger NT0-vs-chat accessibility differentials have larger early-layer
R-Lens advantages over J-Lens.

Primary effect estimate:
Spearman correlation between DeltaA and D_RJ across all benchmark facts.

Uncertainty:
hierarchical bootstrap over questions and facts.

Primary confounding check:
a within-question permutation test, shuffling DeltaA only among facts belonging to
the same benchmark question.

Secondary robustness checks:
- repeat after excluding facts recovered in 0/20 behavioral samples;
- inspect R-vs-J results separately for linear-attention and full-attention layers;
- if a positive effect is observed, inspect whether NT0 recoveries driving the
  high-DeltaA tail occur primarily early or late in the generated completion.

No experimental lens outputs on the development or held-out benchmark facts were inspected before freezing this redesign. Diagnostic smoke-test lens outputs were inspected only to verify compatibility, shapes, memory use, and non-degenerate decoding.