# It’s Not Hidden Knowledge! — Red-Teaming a Large R-Lens Rank Advantage

## Executive Summary — What Survives?

**A large early-layer R-Lens rank advantage looked initially compatible with hidden factual recovery, but it did not track behavioral accessibility and was reproduced by increasingly irrelevant controls, including frequency-matched lexical targets.**

### Question

* [State in 1–2 sentences what you tested and why the question matters.]
* [Give a one-clause explanation of R-Lens and J-Lens.]
* [State immediately that target-token rank is a readout proxy, not proposition decoding.]

### Key result 1 — the motivating hypothesis

* [Primary hypothesis.]
* [Headline estimate / uncertainty.]
* [Plain-English meaning of the result.]

**Figure 1:** `DeltaA` vs `D_RJ`

### Key result 2 — the control ladder

* [Large incidental R-vs-J effect.]
* [Same-topic wrong fact.]
* [Cross-topic wrong fact.]
* [Random lexical.]
* [Frequency-matched lexical.]
* [Summarize which interpretations survive this ladder and which do not.]

**Figure 2:** control ladder summary

### Survivors

* [Supported claim 1.]
* [Supported claim 2.]
* [Supported claim 3.]
* [Exploratory residual / unresolved point.]

**Closing sentence:**
[One sentence stating the strongest methodological lesson.]

---

## Random Qualitative Examples

> Include 3–5 randomly selected raw examples, as requested in the rubric.

### Example 1

* Prompt / fact:
* Response:
* Label:
* Why the label is right or questionable:

### Example 2

* Prompt / fact:
* Response:
* Label:
* Why the label is right or questionable:

### Example 3

* Prompt / fact:
* Response:
* Label:
* Why the label is right or questionable:

---

# Main Write-Up

## 1. Setup / Research Question

Start by making the research inheritance explicit rather than leaving the reader to infer it.

* What problem were you trying to solve?
* Why are censored / politically sensitive factual questions a useful testbed?
* Model: Qwen3.5-27B.
* Readouts: R-Lens, J-Lens, and the ordinary logit lens.
* Development topics and held-out topic.
* Define:

  * `DeltaA`
  * `E_L`
  * `D_RJ`
  * target-token selection

### Inherited setup

From Casademunt et al.:

* benchmark
* topic taxonomy
* NT0-style elicitation setup

[Cite Casademunt et al. for the benchmark, topic taxonomy, and NT0 setup.]

If you discuss their model, use the corrected source-model reference: **Qwen3-32B**.

### This project’s extension

* apply R-Lens / J-Lens / logit-lens readouts to the setup
* replace a purely binary behavioral framing with continuous `DeltaA`
* measure target-token rank
* progressively test the semantic specificity of the observed rank effect

### Interpretive guardrails

* NT0 is an entire elicitation intervention, not a pure censorship intervention.
* The lens context is identical across behavioral conditions.
* `DeltaA` operationalizes behavioral accessibility under that intervention; it is not a direct measure of a latent censorship state.
* Target-token rank is not proposition decoding.
* Keep intentional-state language such as “lying,” “confessing,” or “believing” out of your own claims unless the evidence warrants it.

---

## 2. It’s Not Suppression

### What I expected

* [State the motivating suppression / hidden-accessibility hypothesis.]
* [Explain why that hypothesis predicts a relationship between behavioral accessibility and the R-vs-J readout.]

### What I tested

* [Behavioral assay.]
* [Primary correlation test.]
* [Explain why the hierarchical bootstrap and within-question permutation are appropriate.]

### What happened

* [Headline result.]
* [Uncertainty.]
* [Sensitivity checks.]

### What changed in my interpretation

* [Which version of the suppression hypothesis became unsupported?]
* [Which weaker interpretations were still available?]

**Figure:** refer to Figure 1 / optional body version.

---

## 3. A Large R Effect Appears

The failed primary hypothesis reveals a second phenomenon that becomes the real object of investigation.

* [Describe the unexpected R-vs-J / R-vs-logit rank advantage.]
* [Include the layerwise structure if useful.]
* [Explain why the size of the effect was surprising.]
* [Describe your first interpretation in past tense.]

### Put the effect on an absolute scale

Geometric-mean target ranks are approximately:

* **R-Lens: 2.8k**
* **J-Lens: 6.6k**
* **Logit lens: 7.5k**
* from a vocabulary of roughly **248k tokens**

The framing should make both facts visible at once:

* the relative rank improvement is large;
* the target token is still deep in the vocabulary tail.

Do not let this read as though R-Lens directly “decoded the hidden fact.”

**Optional figure:** layerwise R/J/logit comparison.

---

## 4. It’s Not the Hidden Fact

### Interpretation under test

* [Perhaps R-Lens specifically promotes the correct fact being queried.]

### Specificity control

* Replace the correct target with a factual target from a different question in the same topic.
* Compare the true target against this matched same-topic wrong target.

### Result

* [True vs matched wrong target.]
* [Effect size / uncertainty.]

### Sanity check

* [Independent acquisition / exact rank reproduction.]

### Belief update

* [State what correct-fact specificity this rules out.]
* [State the weaker explanation that could still survive.]

**Figure:** randomized-world / specificity plot.

---

## 5. It’s Not the Topic

### Remaining possibility

* [Maybe the effect is not specific to the queried fact, but still reflects the topic or domain represented in context.]

### Cross-topic control

* Perform a **cross-topic target swap** using factual targets drawn from another topic.

### Result

* [Headline comparison.]
* [True vs same-topic vs cross-topic result.]

### Belief update

* [Explain what topic specificity is no longer supported.]
* [Make explicit why topic-level factual recovery is not sufficient to explain the effect.]

**Optional figure:** true / same-topic / cross-topic layerwise curves.

---

At this point in the application, I traveled for my Uncle James’s funeral. He always wanted me to do more math. Thank you for the extension.

---

## 6. Maybe It’s Lexical

By this point, the surviving interpretation should be deliberately weaker.

### New possibility

* [Perhaps R-Lens generally favors lexical items that look like factual/content-bearing tokens, irrespective of the actual queried information.]

### Control A — random lexical targets

* [Describe how random lexical targets were selected.]
* [Result.]
* [Record the interpretation you considered at this stage.]

### Control B — frequency-matched lexical targets

* [Describe the matching procedure.]
* [Result.]
* [Explain why this materially weakens the semantic interpretation.]

### Belief update

Say: **frequency matching reproduces most of the R-vs-J effect.**

Do not say: **frequency explains or causes the mechanism.**

* [State any remaining residual.]

**Figure:** true vs random lexical vs frequency-matched lexical.

---

## 7. Held-Out Tiananmen

Use this section to separate genuine pre-inspection replication from conclusions developed after looking at the development topics.

* What was frozen before inspecting the held-out topic?
* Which broad pattern replicated?
* Which pattern did not replicate?
* Which hypotheses were never tested here?
* [Optional failed pre-opening prediction.]
* Keep the interpretation narrow.
* Explicitly distinguish conclusions learned on the development topics from those independently checked on Tiananmen.

**Optional figure:** held-out layerwise / topic comparison.

---

## 8. Behavioral Assay / Annotation QA

### Why the metric changed

* Describe the original binary criterion.
* Explain why you abandoned it.
* Introduce continuous `DeltaA`.
* Show the broad behavioral effect of NT0.

### Annotation quality

* Include important counterexamples and the style confound.
* Describe the LLM-judge methodology.
* Describe the human / random audit.
* Report the likely false positive instead of silently removing it.
* Do not claim that your validation was stronger than the source paper’s unless that comparison has been independently verified.

### Appropriate interpretation

* `DeltaA` is noisy and is not ground truth.
* It measures behavioral accessibility under the full NT0 intervention.

---

## 9. Limitations / Notes to Keep Honest

Collect the global caveats here so the conclusion can end on the actual research update.

* `DeltaA` measures the whole NT0 intervention.
* Facts are clustered within questions and topics.
* Behavioral labels are noisy.
* Target rank is a proxy rather than proposition decoding.
* Later controls are exploratory / post-primary.
* `wordfreq` is an external unigram-frequency proxy, not Qwen training frequency.
* Frequency matching supplies descriptive evidence, not a causal account.
* Avoid causal claims about attention-layer differences.
* Avoid anthropomorphic or intentional-state interpretations unsupported by the assay.
* [Any tokenizer / multi-token-target limitations.]
* [Any limited-topic / benchmark-distribution limitations.]

---

## 10. So, Again: What Survives?

### Supported

* [There is a large reproducible R rank advantage.]
* [It does not associate with behavioral accessibility.]
* [It is not specific to the correct queried fact.]
* [It is not specific to the topic.]
* [Frequency-matched irrelevant lexical targets reproduce most of the R-vs-J effect.]
* [Include any robust residual relative to the ordinary logit lens.]

### Not supported

* [R specifically reveals suppressed knowledge.]
* [R preferentially recovers the hidden queried fact.]
* [The layerwise transitions represent localized factual recovery.]
* [Frequency is the mechanism.]
* [A target-token rank shift alone demonstrates proposition recovery.]

### Still open

* [Residual difference from the ordinary logit lens.]
* [Lexical / tokenization / frequency-proxy issues.]
* [Mechanism producing the early-layer transition.]

### Final takeaway

* End with what the investigation changed your mind about, rather than with a future-work catalogue.
* [Candidate framing: the notable result was not that R-Lens recovered hidden knowledge, but that a large and reproducible internal-readout effect remained while successive controls removed most of the semantic interpretation that initially made it interesting.]
* [Methodological lesson: rank advantages need specificity controls before they can be interpreted as evidence of recovering latent content.]

---

# Writing Reminders

For each experiment, keep returning to four questions:

* What did I believe before running it?
* Why was this the right test?
* What happened?
* What interpretation did that eliminate?

More generally:

* Narrative > notebook chronology.
* Use exact numbers only when they carry argumentative weight.
* Put abandoned explanations in past tense.
* Let the section titles provide most of the personality; keep the body prose restrained.
* Keep behavioral observation, internal-readout result, and interpretation visibly distinct.
* Do not rewrite history as though the lexical explanation was obvious from the beginning; the reader should see the interpretation weaken as the controls accumulate.
