# Implementation ledger

The single source of truth for "what's next." One `/ontograph-build`
iteration = find the first row with `Status: todo` (rows are already in
dependency order — do not skip ahead even if a later row looks easier),
implement it, run its Verify command, flip it to `done` only if Verify
passes, commit+push, stop. See
`../../.claude/skills/ontograph-build/SKILL.md` for the exact algorithm and
`BUILD_PLAN.md` for the phase rationale.

Never edit a `done` row's Verify command to make it pass — if a later task
reveals an earlier row's Verify was wrong or insufficient, add a new row
noting the correction; don't rewrite history silently.

Status values: `todo` · `in-progress` · `done` · `blocked` (with a Notes
entry explaining the blocker — never leave a row `blocked` silently).

## Phase 0 — Bootstrap and ground truth

| ID | Task | Spec refs | Verify | Status | Notes |
|---|---|---|---|---|---|
| P0.1 | Fixture corpus + ground-truth test | §67 | `pytest fixtures/mini-ganjoor/test_fixture_ground_truth.py -q` | done | Built this session; 6/6 pass. |
| P0.2 | `pyproject.toml` + `src/ontograph/` package skeleton (empty modules: corpus, normalize, field, anchors, census, encounters, metrics, compare, ablation, mediation, workspace, release, validate — each with a module docstring citing its spec section, no logic yet) | §59 | `python -c "import ontograph"` succeeds after `pip install -e .` | todo | |
| P0.3 | Pin dependencies (stdlib + PyYAML only, unless a task below needs more — do not add a dependency the spec doesn't require) | §59 | `pip install -e .` succeeds from a clean venv | todo | Depends on P0.2. |
| P0.4 | `CorpusSnapshot` loader: reads a `manifest.json` root, records commit/path + manifest hash, exposes poet/poem counts | §56, §65 | unit test loads `fixtures/mini-ganjoor/manifest.json` and asserts `PoetsCount==3`, `PoemsCount==15` | todo | Depends on P0.2. |

## Phase 1 — Deterministic core

| ID | Task | Spec refs | Verify | Status | Notes |
|---|---|---|---|---|---|
| P1.1 | Persian normalization pipeline: Yeh/Kaf variants, Unicode NFC, ZWNJ policy, optional diacritic strip, whitespace — versioned, original text+offsets preserved | §58 | round-trip test: normalize then map offsets back to original text on 5 hand-picked fixture verses, exact match | todo | |
| P1.2 | Token boundary definition for token-window scale (ZWNJ/half-space, punctuation, clitics) | §58 | unit test on at least one fixture verse containing a compound/ZWNJ case | todo | Depends on P1.1. Flag if the fixture has no such case yet — add one rather than skipping. |
| P1.3 | `FieldCharter` + `ScopeSpec`: native filters (poet/category/poem/format/metre/rhyme/source), union/intersection/difference | §7, §23, §48 | build a field over `sample1 ∪ sample2` and assert poem count == 10; build `all minus sample3` and assert == 10 | todo | Depends on P0.4. |
| P1.4 | Derived fraction support: poet-life chronological proxy construction (rule stored with the field, never presented as a poem date) | §11, §23.2 | field built with a proxy rule shows `derived: true` and the exact rule string in its charter | todo | Fixture poets have no birth/death years yet — add minimal fake ones to `poet.json` fixtures rather than skip. |
| P1.5 | `LexicalAnchor` + exact `AnchorHit` census against a field | §8, §27.1 | census for anchor `آینه`+`آیینه` over the full fixture field returns exactly 6 hits matching `_fixture_ground_truth` | todo | Depends on P1.1, P1.3. This is the first real cross-check against P0.1's ground truth — treat any mismatch as an engine bug, not a fixture bug. |
| P1.6 | SQLite derived research index (poets/categories/poems/sections/verses/couplets/normalized_verses/token_offsets) + manifest linking rows to source addresses | §57 | rebuild index from fixture, assert row counts match manifest counts exactly | todo | Depends on P1.1, P1.3. |
| P1.7 | Workspace-as-git-repo: `ontograph study new` initializes `ontograph-workspaces/<id>/` as its own git repo | §60 | after `study new`, `git -C <workspace> rev-parse HEAD` succeeds | todo | |

## Phase 2 — Calibration and occurrence assessment

| ID | Task | Spec refs | Verify | Status | Notes |
|---|---|---|---|---|---|
| P2.1 | Close Calibration sampler: stratified/random sample over Anchor Hits, seeded, context-ladder opening | §9 | seeded sample of size 5 over the 6 fixture mirror hits is reproducible across two runs with the same seed | todo | Depends on P1.5. |
| P2.2 | `OccurrenceAssessment` + `OccurrencePolicy` records; modes `anchor`/`assessed-full`/`assessed-rule`/`estimated` | §8.1, §49 | mark poem 9105's hit `ambiguous`, all others `accepted`; `assessed-full` census reports 5 accepted, 1 ambiguous | todo | Depends on P2.1. This is where poem 9105 (figurative "mirror of the heart") earns its place in the fixture. |
| P2.3 | Ambiguous-hit denominator rule | §8.1.1 (v2.3.0) | prevalence under `assessed-full` on the fixture reports denominator 15 (not 14), numerator 5 (not 6), plus "1 unit with only ambiguous hits" shown separately | todo | Depends on P2.2. This is a v2.3.0 addition with no prior art to copy — write the test from the spec text directly. |
| P2.4 | Default estimator: stratified proportion + Wilson score interval (+ finite-population correction above 10% sampling fraction) | §27.2, Appendix C.3 (v2.3.0) | on the fixture, a 100%-sampling-fraction `estimated` run recovers the same point estimate as `assessed-full` (sanity check: estimating with no held-out data must reduce to the exact answer) | todo | Depends on P2.2. |

## Phase 3 — Metrics and mapping operations

| ID | Task | Spec refs | Verify | Status | Notes |
|---|---|---|---|---|---|
| P3.1 | Unit incidence, prevalence, spread, concentration | §27.3–27.6 | on fixture, prevalence(mirror, poem-scale, assessed-full) == 5/15 (per P2.3's corrected denominator); top-poet share reported alongside | todo | Depends on P2.3. |
| P3.2 | Dispersion (named, versioned Gries DP-family measure) shown only with raw counts + partition sizes | §27.7 | dispersion value never rendered without both raw counts in the same result object | todo | Depends on P3.1. |
| P3.3 | Typed co-incidence matrix (`AᵀA` from occurrence policy, not raw anchors) + separate `A_anchor` | §28.1 | on fixture, poem-scale mirror×rust co-incidence == 3 (matches ground truth); couplet-scale == 2 | todo | Depends on P2.2, P1.6. |
| P3.4 | Conditional association P(B\|A), P(A\|B) — labelled "conditional association," never causation | §28.2 | unit test asserts the two directions differ on the fixture and neither output string contains "cause" | todo | Depends on P3.3. |
| P3.5 | Lift with minimum-support guard; never called "statistical significance" without a declared reference condition | §28.3 | lift computation refuses (raises/labels) below the configured minimum support | todo | Depends on P3.3. |
| P3.6 | Relation Scale Profile / `ScaleSurvival` across poem→section→couplet→verse→token-window | §29 | on fixture, mirror-rust scale profile shows poem-scale 3, couplet-scale 2, and correctly isolates 9102 as the poem that only survives broadly | todo | Depends on P3.3, P1.2. |
| P3.7 | Compare Fields (raw incidence, prevalence, dispersion/concentration deltas, companions gained/lost, close-reading cases behind the biggest difference) | §30 | compare `sample1`-field vs `sample2`-field; assert the report includes raw support alongside any ratio | todo | Depends on P3.1, P3.3. |
| P3.8 | Ablation + `AblationRetention` | §31 | removing `sample1` from the full fixture field drops couplet-scale mirror-rust co-incidence from 2 to 1 (50% retention) — must match `manifest.json`'s `_fixture_ground_truth` exactly | todo | Depends on P3.3. This is the Test D fixture case (§67) — the whole point of the `sample2` minority tight case. |

## Phase 4 — Records, events, release

| ID | Task | Spec refs | Verify | Status | Notes |
|---|---|---|---|---|---|
| P4.1 | Trace, Relation-Object, Profile, Experiment, Finding record CRUD (JSONL-backed, per workspace schema) | §49–55 | round-trip write/read for one instance of each record type | todo | Depends on P1.7. |
| P4.2 | AI-summary Profile provenance fields (`summarizer_model_version`, `summarizer_prompt_version`) required when `access_apparatus=ai-summary` | §40, §52 (v2.3.0) | creating an ai-summary Profile without these fields raises/rejects | todo | Depends on P4.1. |
| P4.3 | Append-only `EventRecord` log | §51 | attempting to mutate/delete a past event raises; replay reconstructs a sequence of study states | todo | Depends on P4.1. |
| P4.4 | `ResearchRelease` generator incl. `data_license_notice` | §55, §56 (v2.3.0) | release refuses to generate if `data_license_notice` is empty; generated release for the fixture study contains the three-part licensing chain text verbatim | todo | Depends on P4.1, P4.3. |
| P4.5 | Release-as-git-tag convention | §60 (v2.3.0) | `ontograph release` creates a git tag in the study workspace matching the release version | todo | Depends on P1.7, P4.4. |

## Phase 5 — CLI

| ID | Task | Spec refs | Verify | Status | Notes |
|---|---|---|---|---|---|
| P5.1 | `ontograph` console script wired to Phases 1–4, every verb accepts `--json` | §62, §78 | each of `study new`, `field build`, `object add`, `calibrate`, `census`, `map recurrence`, `companions`, `compare`, `ablate`, `release` runs against the fixture and exits 0 with well-formed JSON | todo | Depends on all of Phase 1–4. |
| P5.2 | Verb-naming check: no `search`/`query` verbs anywhere in the CLI | §25 (v2.3.0 disambiguation note) | `ontograph --help` output contains neither literal string | todo | Depends on P5.1. |
| P5.3 | Explicit failure mode: non-zero exit + stderr message on bad input, on missing workspace, on malformed field spec — never a silent empty JSON success | §61, §78 | one negative test per failure class above | todo | Depends on P5.1. |

## Phase 6 — Claude Code binding

| ID | Task | Spec refs | Verify | Status | Notes |
|---|---|---|---|---|---|
| P6.1 | Point `.claude/skills/persian-poetry-ontograph/SKILL.md`'s invocation examples at the real, now-working CLI (already scaffolded this session; update only the "Status: scaffold" note once Phase 5 is done) | Part XIII | manually run one invocation from the SKILL.md example block against the fixture, confirm the JSON shape matches | todo | Depends on P5.1. |
| P6.2 | `.claude/settings.json` allowlist entries for corpus-mutating/release verbs per §79 | §79 | settings.json contains explicit entries for `field build`, `object add`, `calibrate`, `release`; no blanket Bash grant added | todo | |

## Phase 7 — Tests and gates (v0.1 completion)

| ID | Task | Spec refs | Verify | Status | Notes |
|---|---|---|---|---|---|
| P7.1 | Deterministic corpus test suite (full §65 list) | §65 | `pytest tests/deterministic/ -q` all pass | todo | Depends on Phases 1–3. |
| P7.2 | Epistemic contract test suite (full §66 list — the "does NOT" scenarios) | §66 | `pytest tests/epistemic/ -q` all pass | todo | Depends on Phases 1–4. |
| P7.3 | Close–distant loop tests A–F against the fixture | §67 | `pytest tests/loop/ -q` all pass; Test F may be `xfail`-marked with a comment pointing at §72 (mediation is v0.2 scope) rather than silently skipped | todo | Depends on Phases 1–4. |
| P7.4 | Implementation gates 1–5 | §69 | a single `ontograph validate --gates --json` (or equivalent script) reports all five gates green against the fixture | todo | Depends on P7.1–P7.3. |
| P7.5 | Occurrence-assessment scalability gate | §70 | the fixture study demonstrates all three routes (`assessed-full` on the real 6 hits, `assessed-rule` with one versioned rule, `estimated` with the P2.4 estimator) without ever mislabeling one as another | todo | Depends on P2.2–P2.4. |
| P7.6 | End-to-end replay: run one full study (Field Charter → Release) on the fixture, then independently reconstruct its state from the release package alone | §69 gate 5 | a second script rebuilds study state from `release.json` only and asserts it matches the live workspace | todo | Depends on all prior phases. **This row passing is the v0.1 stop condition** — see `BUILD_PLAN.md` Definition of Done. |

## Phase 8 — Real-corpus integration (manual, not loop-driven)

| ID | Task | Spec refs | Verify | Status | Notes |
|---|---|---|---|---|---|
| P8.1 | Point pinned-corpus config at real `ganjoor-data`/fork commits, rebuild real SQLite index | §56 | poet/poem counts match the live manifests re-audited in `EVALUATION.md` | manual | **Not part of the automated loop** — needs a multi-GB clone. Do this yourself, or in a separately-approved session, after Phase 7 passes. |
| P8.2 | Run the spec's own worked example (§45, mirror/rust in Hafez) as a smoke test on the real corpus | §45 | a human reviews the actual output against §45's narrative | manual | Depends on P8.1. |

## Out of loop scope (do not add rows for these without a Research Situation justifying them — §73–74)

Mediation/relation-mediated-thickness (v0.2, §72), multiplex graph
diagnostics beyond bridge-diagnostic ablation, matrix decomposition,
spectral/community diagnostics, any browser workbench, any graph database,
corpus-wide LLM labeling, a universal Persian lemmatizer.
