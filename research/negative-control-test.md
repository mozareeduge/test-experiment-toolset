# Negative-control test — mozare-critic against real Mozare prose

Run after applying the fixes in `research/opus5-harness-review.md` (F1,
F2/F3/F11/F12, F5/F7/F14, F8/F9, and the structural-tells genre-scoping and
open-questions additions), per the review's own recommended order: run this
before trusting any further calibration work, because its result determines
how much of the review's other findings were real versus artifacts of the
broken pre-fix state.

**Target:** `/home/user/mozare-wiki/03-objects/works/the-black-bird.md` — an
actual mozare-wiki canonical page, not a test draft authored to exercise the
harness. **Invocation:** genre and recipient only, per the fixed
invocation-contract discipline.

## Result

- **Mechanical check, both files:** zero hits. The F1 fix (deleting "rather
  than," moving the contrast-before-characterization and context-dependent
  entries to `banned-review.txt`) held — the harness no longer flags
  Mohammad's own prose for constructions that were never actually AI tells.
- **Structural pass:** clean. No forced monotony, tricolon, hedge-stacking,
  chiasmus, or em-dash flags. The critic explicitly declined to apply the
  sentence-spread numbers or an em-dash rate, correctly citing the new
  open-questions/genre-scope discipline rather than inventing a threshold —
  this is the exact failure mode (F5/the em-dash hole) the fixes targeted,
  and it didn't recur.
- **No forced taxonomy completion.** Nine real flaws reported, zero padding
  to fill categories, and — unlike the original smoke test — every flaw is
  substantive: all nine are provenance/evidence-currency problems (a stale
  `updated:` date, an alias asserting an identity the archive's own
  evidence separates, a rights notice with a dropped temporal qualifier,
  claims not linked to source records per `wiki-records.md`), not style
  complaints. This is real diagnostic work, not rubric-filling.
- **An open question named instead of a flag invented:** a real structural
  candidate (ten "define by refusal" negation constructions in 587 words)
  was surfaced but explicitly *not* reported as a `positive-characterization`
  flaw, because the protocol's rule targets contrast against an invented
  opponent and every negation here has a specific real referent. Correctly
  distinguished from the flaw type it superficially resembles.
- **An unanticipated finding: partial self-reference in the control itself.**
  `voice-patterns.md` quotes this same file's "Object-field" section as its
  canonical positive exemplar. The critic caught this unprompted, disclosed
  it as a caveat, and discounted its own clean style verdict accordingly —
  exactly the behavior now made an explicit instruction in `mozare-critic.md`
  (see that file's voice-patterns.md paragraph) rather than something that
  happened to occur once.
- **Verdict:** "Close, not ready" — for real reasons (record currency), not
  for style. The prose passed; the archive's own bookkeeping around it
  didn't.

## What this validates about the harness

The negative control's whole point was to check whether F1 and F5 were real
or artifacts of a broken pre-fix state (the review's own words: "my
prediction is that the critic returns a substantial flaw list on his own
canonical prose. If it does, the harness is currently calibrated to fail
his voice"). It did not. The style axis came back clean, and the flaws that
did surface are exactly the kind a careful human editor would raise —
provenance and currency, not vocabulary or rhythm. That's the harness
behaving as designed rather than penalizing Mohammad's own writing.

## What this is not

This is not a wiki-content finding to act on here. The nine flaws above are
about `the-black-bird.md`'s currency inside mozare-wiki's own evidence and
version-tracking discipline — that repo has its own governance for this
(`wiki-validate`, human adjudication, the `_proposals/` queue) and this
sandbox harness has no standing to fix mozare-wiki content. Recorded here as
a byproduct of the test, for Mohammad to act on or not, separately.
