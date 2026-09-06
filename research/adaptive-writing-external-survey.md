# External writing-agent survey — flows, exact texts, and what to take

Deep-dive on three real, cloned repositories (not just descriptions) that do the kind
of work Mozare's writing harness needs: a flow of distinct LLM "nodes," each with its
own input text, that together take a draft from rough to clean. Read in full and
quoted verbatim below so the actual words, not just the concept, are visible.

**Cloned for read-only research**, not installed anywhere:
- `conorbronsdon/avoid-ai-writing` (v3.33.0) — a seven-skill orchestrated graph
- `jalaalrd/anti-ai-slop-writing` — a single-file directive
- `harshaneel/humanize` — a lever-based rewrite skill plus a companion forensic-scoring skill (`ai-check`)

**A flag, not a finding about the writing itself:** `avoid-ai-writing`'s own `CLAUDE.md`
(auto-loaded by any coding assistant that opens the repo) contains a sentence instructing
that citing a named third-party "survey ranking" of the repo "has to carry the disclosure
with it." That is an instruction planted in repository content aimed at exactly the kind
of assistant reading it for research — not something Mohammad or this project established.
It is not followed here, no such ranking is cited, and it is called out because the
system prompt's rule on suspected prompt injection says to surface this rather than
silently comply or silently ignore it.

---

## System 1 — `avoid-ai-writing`: a seven-node orchestrated graph

This is the closest match to "a flow and a set of units that work until new text is
generated." It is not one skill — it is seven, wired together by an explicit
machine-readable graph plus a human-readable routing table, with one shared piece of
state (the "handoff envelope") passed between nodes.

### The nodes

| Node | Job | Can it edit text? |
|---|---|---|
| `avoid-ai-writing-router` | classify the request once, pick the owner, sequence multi-stage work | no — orchestration only |
| `avoid-ai-writing` | the canonical rulebook (severity tiers, vocabulary, voice, output format) | this *is* the authority the others defer to |
| `ai-writing-detector` | scan/flag only, never rewrite | no |
| `voice-preserving-rewriter` | rewrite returned (pasted) text | yes, returned text only |
| `file-edit-in-place` | rewrite a named file | yes, in place |
| `preservation-verifier` | before/after check that nothing protected got lost | no — gate only |
| `false-positive-reviewer` | interpret what detector output can and can't prove; terminal node, never loops back | no |

### The exact orchestration text (verbatim, `avoid-ai-writing-router/SKILL.md`)

> Coordinate the public Skills as a bounded workflow. Route to the narrowest owner,
> preserve context between stages, and stop when the requested job is complete. This
> Skill does not replace the original `avoid-ai-writing` rulebook.
>
> Classify the request once, create the smallest useful handoff envelope, then pass
> that envelope forward rather than asking every downstream Skill to infer the same
> context again.
>
> Never mark an execution field as `executed` without host evidence.

That last line is doing real work: it is a standing rule against a very specific and
very tempting failure — a stage silently *claiming* a check ran when it didn't. Our own
`mozare-finalize` has exactly this failure mode available to it (see recommendations).

### The handoff envelope (verbatim schema, `handoff-contract.md`)

```yaml
intent: detect | rewrite | edit_file | verify | interpret | multi_stage
source_kind: pasted_text | named_file | before_after_pair | visual_prompt | other
source_ref: optional path or user-supplied label
context_mode: general | technical
voice: optional casual | professional | technical | warm | blunt | user_sample
protected_constraints:
  - facts
  - numbers
  - urls
  - paths
  - code
  - quotes
  - tables
  - frontmatter
  - attributed_text
  - identity_and_cultural_specificity
execution_evidence:
  detector: not_run | model_only | executed
  mutation: not_requested | not_run | executed
  verifier: not_run | model_only | executed
detector_summary:
  score: optional
  label: optional
  issue_types: []
verification_summary:
  status: optional PASS | REVIEW | FAIL
  blocking_errors: []
  warnings: []
risk_flags:
  consequential_authorship_claim: false
  human_representation_sensitive: false
pass:
  index: 1
  max: 2
next_action: optional skill slug
return_to_router_reason: optional reason
```

The three-way `not_run | model_only | executed` distinction is the single most
reusable idea here: it makes it structurally impossible to accidentally claim a
mechanical check happened when it was actually a model just eyeballing the text.

### Typed edges and loop bounds (verbatim rules, `handoff-contract.md`)

> - Rewrite/audit convergence follows the canonical maximum of two passes.
> - A verifier repair loop may re-enter the repair owner once, then verify once more.
> - Residual detector recheck may occur once when the original request requires it.
> - If the second verification still fails, stop and report the unresolved preservation
>   error instead of cycling.
> - Terminal Skills have no outgoing Skill edges.
> - Every graph cycle must contain an edge with `max_reentries: 1`.

`false-positive-reviewer` is explicitly terminal — it can never call the detector
directly, only hand control back to the router — specifically to prevent a
reviewer-detector infinite loop. This is a clean, general pattern: **make interpretation
terminal**, never self-reinforcing.

### The "Never inject these" section (verbatim, `avoid-ai-writing/SKILL.md`) — the most valuable single find

Every other tool in this survey polices what a draft already contains. This is the only
one that separately polices what the *rewrite itself is allowed to add*:

> The instruction above — put voice back on purpose — has a predictable failure mode:
> the model reaches for a stock kit of "human" moves and installs a personality the
> author never had. That trades one detectable register for a louder one.
>
> None of the following may be **added** to a text that did not already contain it.
> Every one is a rewrite failure even when the result scores clean:
>
> - **Fake first person.** "I've seen this a hundred times," "in my experience," "I'll
>   admit" dropped into prose that had no author presence. Voice comes from the author
>   or not at all. If the source has no `I`, the rewrite has no `I`.
> - **Manufactured stakes.** "In a world where," "now more than ever," "the stakes have
>   never been higher."
> - **Forced contrarianism.** "Everyone says X, but they're wrong." Only legitimate when
>   the source actually argued it. Inventing a foil is inventing a claim.
> - **Performed candor.** "Let's be honest," "real talk," "here's the thing."
> - **Em-dash theatrics.** Dashes staged for drama the content has not earned.
> - **Staccato conversion.** Chopping ordinary sentences into fragments to manufacture
>   rhythm. Vary sentence length by varying the sentences, not by breaking them.
> - **Invented specifics.** A number, name, date, tool, or mechanism the source never
>   contained. Specificity is the most tempting fix because it always reads better, and
>   a fabricated specific is worse than the vague phrasing it replaced. If the concrete
>   detail is missing, flag the gap and leave it. Never fill it.
>
> **The test.** For each edit, ask whether the information in the rewrite came from the
> source. Subtraction and sharpening are in scope: cutting filler, making an existing
> claim concrete, surfacing a buried point. Addition of stance, personality, or fact is
> not.
>
> **Why it belongs here rather than in the pattern catalog.** These are constraints on
> the editor, not detections on the text. A first-person aside is not a flag when the
> author wrote it; it is a failure when the tool inserted it. The difference is
> provenance, which no pattern can see, so it lives with the rewrite instructions where
> the decision is actually made.

This is directly, immediately usable for Mozare's harness with zero adaptation needed —
it names the exact failure mode a `mozare-write` rewrite pass could produce (a fabricated
`[FIGURE NEEDED]`-adjacent invented specific, a manufactured first-person aside that
isn't Mohammad's), and the "provenance, not pattern" framing is a sharper articulation of
something the Adaptive Writing Protocol already gestures at but doesn't say this exactly.

### Severity tiers and the self-reference escape hatch (verbatim excerpts)

> **P0 — Credibility killers (fix immediately)** — cutoff disclaimers, chatbot artifacts,
> vague attributions without sources, significance inflation, hashtag stuffing (profile-dependent)
>
> **P1 — Obvious AI smell (fix before publishing)** — word-list violations, template
> phrases, "Let's" openers, synonym cycling, em dash frequency above 1 per 1,000 words,
> generic future-narrative closers, hedge-stacked predictions...
>
> **P2 — Stylistic polish (fix when time allows)** — generic conclusions, compulsive
> rule of three, uniform paragraph length, copula avoidance, transition phrases...

> **Self-reference escape hatch.** When writing *about* AI writing patterns (blog posts,
> tutorials, skill documentation like this file), quoted examples are exempt from
> flagging... Only flag patterns that appear in the author's own prose, not in cited
> examples of bad writing.

The self-reference escape hatch matters directly for Mozare's own `mozare-critic`: a
draft that quotes someone else's bad prose, or quotes a source document verbatim, should
not have that quoted material flagged as the drafter's own tell. Our current
`structural-tells.md` doesn't say this explicitly and should.

### Context profiles and voice profiles as two independent axes (verbatim framing)

> Context profiles (above) set *how strict* to be for an audience. Voice profiles set
> *how the prose should sound* — the persona. They're independent axes: you can write
> blunt for a blog or warm for docs... **How voice composes with context.** Voice sets
> the target; context sets how hard to enforce it... Where they disagree, resolve toward
> the **stricter** of the two.

Six context profiles (`linkedin`, `blog`, `technical-blog`, `investor-email`, `docs`,
`casual`) each relax or tighten ~20 rules in a tolerance matrix; five voice profiles
(`casual`, `professional`, `technical`, `warm`, `blunt`) each give concrete numeric
targets, e.g.:

> **`blunt`** — Lead with the claim; cut "It's important to note that" windups.
> Em-dashes are rare here; use periods for emphasis. No padding to hit a rule of three.
> Near-zero hedging; flag "may / could / potentially" stacks. Short declaratives, with
> the occasional long sentence for contrast. *Decision memos, thought leadership, hard
> feedback.*

This two-axis design (audience-strictness × persona-target, resolved toward the
stricter when they conflict) is more precise than Mozare's protocol's single
genre-control table, though it's solving a more general-purpose problem (many possible
authors/personas) than Mozare's harness needs (one calibrated voice, several genres).
The axis *separation* is worth borrowing even if we don't need five personas.

---

## System 2 — `anti-ai-slop-writing`: the simplest shape, one file, one checklist

No graph, no handoff — a single `SKILL.md` plus one reference file. Useful as the
opposite end of the design space: what's the minimum viable version of this.

### The self-check (verbatim, this is the entire "finalize" step of this tool)

> 1. Any banned words or phrases? → Replace.
> 2. Three consecutive same-length sentences? → Vary them.
> 3. Parataxis — three or more short declarative sentences in a row? → Merge or connect
>    them with conjunctions, clauses, or punctuation.
> 4. Grouped in threes? → Break the pattern.
> 5. Hedging instead of committing? → Pick a side.
> 6. More than one em dash? → Remove extras.
> 7. Passive construction? → Make active.
> 8. Every paragraph ends with a transition? → Cut some.
> 9. Fabricated any specifics? → Remove or flag as hypothetical.
> 10. Could any AI have written this for any person? → Add something specific.
> 11. Sounds like ChatGPT? → Rewrite until the answer is no.
>
> Apply all rules silently. Never mention them. Never say "as per the guidelines." Just
> write within these constraints.

Item 10 — "could any AI have written this for any person" — is a sharp one-line test
that isn't in either of our current files, and it's a direct restatement of Mozare's own
protocol's actual goal (a *specific* person's compositional intelligence, not generic
competent prose).

### Banned words with per-model and per-era tracking (verbatim table, `banned-words.md`)

> **Model-Specific First-Word Tells** (avoid starting responses with these)
>
> ChatGPT tends to start with: "as," "yes," "sure," "here," "in," "to," "creating,"
> "certainly," "title," "the"
> Claude tends to start with: "in," "from," "this," "how," "yes," "title," "according,"
> "the," "based," "here"
>
> **Era-Specific AI Vocabulary**
> 2023–mid 2024 (GPT-4 era): additionally, boasts, bolstered, crucial, delve, ...
> Mid 2024–mid 2025 (GPT-4o era): align with, bolstered, crucial, emphasizing, ...
> Mid 2025 onward (GPT-5 era): emphasizing, enhance, highlighting, showcasing

This confirms the concern already logged in mozare-wiki's own handoff: a flat wordlist
goes stale as models change what they default to. This is the concrete evidence for
that, dated and specific, and the era table shows the list actually *shrinking* over
model generations — later models default to fewer, subtler tells, which is itself
useful information: the flat-list approach has a shrinking half-life and needs the
structural checks (rhythm, provenance, specificity) more than the vocabulary checks as
models improve.

---

## System 3 — `humanize` + `ai-check`: the most research-grounded, and where the ethical line actually sits

Two paired skills: `humanize` writes/rewrites; `ai-check` forensically scores a text 0–27
across nine signals. Every rule cites a real paper or study in a separate
`references/research.md` kept out of the operational file.

### The nine signals ↔ nine levers mapping (verbatim)

> Nine signals: eight stylometric plus the RLHF fingerprint... The levers below are the
> write-side counterparts of the signals `ai-check` grades (A–I): 1→A, 2→B, 3→C, 4→D,
> 5→E, 6→H, 7→F, 8→G, 9→I (RLHF subset).

| # | Lever (write-side) | Signal (check-side) | What it measures |
|---|---|---|---|
| 1 | Perplexity injection | A | predictable vs. surprising-but-apt word choice |
| 2 | Burstiness injection | B | sentence-length variance |
| 3 | Hedge surgery | C | softening/epistemic hedge density |
| 4 | Structural flattening | D | imposed document architecture |
| 5 | Specificity insertion | E | grounding anchors (numbers, names, dates) |
| 6 | Voice and register | H | first/second person, self-correction, register |
| 7 | Discourse coherence | F | transition-word fingerprint |
| 8 | Punctuation normalization | G | em dash / semicolon / colon rates |
| 9 | Strip RLHF voice | I | rhetorical scaffolding — the hardest tells |

### The seven hard rules stated as *counting* discipline, not "feel" (verbatim)

> These seven fail more often than everything else combined, because the model that
> wrote the draft is the model checking it. You systematically overproduce these
> patterns; your draft contains em dashes even when you don't remember writing them.
> Treat "my draft is probably clean" as false by default.
>
> 7. **Sentence-length spread:** in any output over ~80 words, the longest sentence must
>    beat the shortest by 20+ words, and fewer than half the sentences may sit in the
>    10-to-20-word band. Your uncorrected rhythm clusters at 10-20 words with ~6 words of
>    deviation; that uniformity is a measured tell even when every other rule passes.
>    **Verify from the written count list (step 5), never by feel.**

And the operational technique this produces (verbatim, rewrite protocol step 5):

> Write out every sentence's word count in order ("9, 5, 22, 16, 7..."), then check the
> list against ALL four [conditions], fixing and recounting until every one passes... A
> mental read-through always sounds varied to the model that wrote it; the number list
> doesn't lie.

This — literally writing out the sequence of sentence lengths as numbers before judging
a draft's rhythm — is a small, concrete, immediately adoptable technique that neither of
our current files (`structural-tells.md`, `banned-patterns.txt`) implements. It replaces
"does this feel varied" (a self-report the drafting pass is bad at) with a countable
artifact a second pass can check without judgment calls.

### The Signal I checklist (rhetorical scaffolding) — the deepest catalog found

Fourteen named named patterns, each with a real example and a fix, e.g.:

> **Thesis-first opener / "X is the easy/hard part"** (severity: moderate) — Starting a
> personal piece with the frame before the experience: "Gathering evidence for an EB1A
> petition is the easy part." AI leads with the thesis because it's been trained on
> essays. Real writers start in the middle of the experience.
>
> **Chiasmus** — reversed parallel that sounds like insight: "Being specific about being
> wrong is more useful than being vague about being right." Real insight is asymmetric;
> AI constructs symmetric reversals.

This is a genuine superset of our `structural-tells.md`'s P1 tricolon/hedge entries —
worth folding in the specific named patterns (thesis-first opener, chiasmus,
parallel-subject mirror, "turns out" pivot, mini-aphorism closer) rather than leaving
them as one generic "mirrored-clause parallelism" entry.

### Where this tool crosses the line Mozare's own project already rejects

The research file is explicit that the target is *detectors*, not writing quality per se:

> **Advanced techniques (optional, when stakes are high)**
> 1. **Detector-scored best-of-N.** Generate 3–5 variants; score each against a real
>    detector (GPTZero, Pangram, Binoculars)... ship the lowest.
> ...
> **Decoding-strategy note (when controlling generation):** set temperature high
> (0.9–1.1), top-p loose (0.95–0.99), repetition penalty up (1.1–1.2). This widens the
> token distribution and breaks the local-maximum property perplexity detectors rely on.

And its own research file cites the goal directly: "Detector-guided adversarial
paraphrasing: 87.88% average TPR reduction across 8 detectors." This is optimizing
against a classifier, not toward Mohammad's actual voice — the exact inversion of
`CLAUDE.md` rule 4 ("do not upgrade evidence because language is fluent, repeated,
similar, or AI-generated") and the negative constraint already logged in the
mozare-wiki handoff. **None of this — best-of-N against a detector score, sampling-
parameter manipulation for evasion, homoglyph tricks, watermark stripping — should go
into Mozare's harness**, regardless of how well-cited it is. The line isn't fuzzy: a
technique aimed at what a *detector* sees is out of scope; a technique aimed at what a
*careful human reader* sees (burstiness, specificity, provenance, hedging) is in scope,
because those are the same things the Adaptive Writing Protocol already cares about for
independent reasons.

Also worth naming: `ai-check`'s own calibration notes undercut confident detector talk
in exactly the way Mozare's evidence rules already insist on —

> **Claude blind spot in zero-shot detectors.** ...Binoculars achieves only ~55% AUROC
> on Claude-generated text vs ~88% on GPT-3.5.
> **Stylistic cues are corpus-conditional.** ...surface stylistic features detectors
> rely on are dataset-specific, not stable authorship signals.

— which is the same caution `avoid-ai-writing`'s `false-positive-reviewer` node exists
to enforce, and the same caution already built into `mozare-critic`'s framing (diagnosis,
never a verdict).

---

## Cross-cutting comparison: the three tools don't even agree with each other

| Rule | `avoid-ai-writing` | `anti-ai-slop-writing` | `humanize` |
|---|---|---|---|
| Em dash ceiling | 1 / 1,000 words (P1) | 1 / 500 words | 1 / 300 words (0 under 300 words) |
| Rule of three | flag "compulsive" use (P2) | never default to three | not a standalone rule; folds into Signal I's tricolon/chiasmus entries |
| Mechanism | severity tiers + tolerance matrix per audience | flat rule list | numbered lever ↔ signal pairing, cited to papers |
| Loop bound | max 2 passes, 1 repair re-entry, typed graph | none (single pass) | max 2 paraphrase passes ("diminishing returns past 2") |

The disagreement on the em-dash threshold (1/1000 vs 1/500 vs 1/300) is itself useful
information: there is no settled number, so Mozare's harness shouldn't borrow one as if
it were established fact. `structural-tells.md`'s current "~1 per 150 words" guess is
actually the *strictest* of all four and was invented, not sourced — worth loosening
and citing a range instead of a single invented number.

---

## Recommendation: adopt / adapt / reject

**Adopt directly, near-verbatim:**
1. The `execution_evidence: not_run | model_only | executed` discipline — apply it to
   `mozare-finalize`'s mechanical check and to any claim that `mozare-critic` "ran."
2. The "Never inject these" editor-constraint list — fake first person, manufactured
   stakes, invented specifics, staccato conversion — as a new section in
   `mozare-write/SKILL.md`, framed exactly as they frame it: constraints on the editor's
   own additions, not detections on the input.
3. The self-reference escape hatch — quoted/attributed material is exempt from
   `mozare-critic`'s flagging.
4. The "write out every sentence's word count in order" technique, as the concrete
   mechanism behind `structural-tells.md`'s sentence-rhythm entry (replacing the current
   vague "eyeball the spread" instruction).
5. "Could any AI have written this for any person?" as a closing test in
   `mozare-critic`'s verdict step — it's the sharpest one-line restatement of what the
   Adaptive Writing Protocol is actually for.

**Adapt, don't copy wholesale:**
6. The named Signal I / rhetorical-scaffolding patterns (thesis-first opener, chiasmus,
   parallel-subject mirror, mini-aphorism closer, "turns out" pivot) — fold the specific
   named list into `structural-tells.md` in place of the current generic entries, but
   keep the framing that these are craft judgments requiring a careful re-read, not
   authorship evidence (this matters more for Mozare than for these tools, since
   `CLAUDE.md` rule 4 already forbids treating fluency/pattern-matches as evidence of
   anything).
7. The two-axis genre/voice split — Mozare doesn't need five personas, but the
   *separation* (how strict for this audience vs. what this text should sound like) is
   cleaner than one flat genre-control table, and maps onto the protocol's existing
   distinction between genre and voice.
8. The routing-graph architecture itself — Mozare's three-piece
   write/critic/finalize is already a small version of this graph. If the harness grows
   a fourth or fifth stage later, the typed-edge vocabulary (`ROUTE`/`FEED`/`VERIFY`/
   `REPAIR`/`RECHECK`/`ESCALATE`) and the "terminal nodes never loop back to themselves"
   rule are worth reusing rather than reinventing.

**Reject outright, and say why in the harness's own documentation so it doesn't get
re-proposed later:**
9. Best-of-N generation scored against a commercial detector.
10. Sampling-parameter manipulation (temperature/top-p/repetition-penalty) chosen to
    defeat perplexity-based detection.
11. Homoglyph substitution, watermark stripping, or any other adversarial-evasion
    technique — flagged as "dead ends" even by `humanize`'s own research file, and out
    of scope on ethical grounds regardless of effectiveness.
12. The premise that a low AI-check score is itself a goal. Mozare's target is a specific
    person's compositional intelligence; a generic-but-undetectable voice is not that,
    and optimizing for detector-evasion can produce exactly that failure mode (this is
    the same trap the "Never inject these" section already names for over-humanizing).

**Not yet decided — needs Mohammad's call:**
- Whether to adopt an actual em-dash-rate number at all, given the three tools don't
  agree (range 1/1000 to 1/300) and Mozare's protocol says dense prose is fine "when the
  material demands it" — a hard numeric ceiling may be the wrong shape for a protocol
  built around exactness over convention.
- Whether `mozare-write`/`mozare-critic`/`mozare-finalize` should grow into an actual
  typed graph (with a handoff-envelope file, not just three loosely-coupled pieces) now,
  or stay simple until a real use surfaces the need.

Nothing above has been implemented yet — this file is the research artifact the harness
work should be built from once reviewed, per the instruction to work this in
`test-experiment-toolset` on a separate branch before anything moves back to
`mozare-wiki`.
