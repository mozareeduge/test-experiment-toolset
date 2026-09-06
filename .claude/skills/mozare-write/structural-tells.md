# Structural tells (beyond the word list)

`banned-hard.txt` and `banned-review.txt` catch vocabulary. They can't catch a draft that uses
zero banned words and still reads as generated, because the tell is in the
*shape* of the prose. These need a second look at the whole draft, not a
line-by-line grep — that's why they're split out from the mechanical check.

Sourced from `research/adaptive-writing-external-survey.md` in this repo,
which surveys three external tools in depth (`conorbronsdon/avoid-ai-writing`,
`jalaalrd/anti-ai-slop-writing`, `harshaneel/humanize`+`ai-check`) and states
exactly what's adopted here versus rejected. **Not adopted from any of them:**
anything framed as defeating a detector — see that file's "reject outright"
list. Everything below is framed as what a careful human reader notices, not
what a classifier scores.

## Self-reference escape hatch (apply this before anything else)

When the draft quotes someone else's prose, a source document, or an
attributed passage, don't flag tells inside the quotation — only flag
patterns in the author's *own* prose. A draft *about* AI writing patterns
that quotes a bad example is not itself exhibiting the pattern. Adapted from
`avoid-ai-writing`'s "self-reference escape hatch."

## The sentence-count technique (replaces "eyeball the rhythm")

Don't judge sentence-length variety by feel — a mental read-through reads
varied to the pass that wrote it. Instead, write out the word count of every
sentence in the paragraph or section in order: `9, 5, 22, 16, 7, 31, 4...`.
Then check the list, not the memory of reading it:

- is there at least one sentence under 8 words and at least one over 25, in
  any stretch of ~150 words?
- do three consecutive sentences ever land within ~5 words of each other?
  If so, that stretch is metronomic even if the piece overall looks varied.
- for a run of very short sentences, is there a longer one nearby to
  counter-balance it? A run of short fragments with nothing longer reads
  choppy, not deliberate.

The three external tools surveyed disagree on the exact numeric thresholds
for this (one wants a 20-word spread over any 80-word stretch, another just
wants no three-in-a-row within 5 words) — treat the specific numbers as
guidance, not a hard-coded rule Mozare's protocol never asked for. The
technique — write the counts down, judge the list — is the actual find, not
any single number.

**Genre-scope the spread requirement — don't apply it everywhere.** The
numbers above come from tools calibrated on blog and personal-essay prose.
`protocol.md`'s own style calibration says prose should be "dense when the
material demands it" and that "long sentences are fine when each one
moves" — a methodology section, theoretical section, or technical appendix
built from long accumulating sentences is doing exactly that, not failing
this check. For those genres, use the count list only to catch genuine
**monotony** — three consecutive sentences within ~5 words of each other —
and don't apply the 8-word-minimum / 25-word-spread requirement, which
pulls toward blog rhythm. For narrative, letter, and artist-statement
genres, the full spread check applies.

**Genre-scope "thesis-first opener" the same way** (below, under P1): a
research pre-proposal is *required by its own genre entry* to lead with the
research object and problem — that is not the tell this pattern names. Only
flag a thesis-first opener in narrative, letter, and artist-statement
genres, where leading with the frame instead of the material really is
generic.

## Editor constraints — what a rewrite may never *add*

These are constraints on the pass doing the rewriting, not detections on the
input. Adapted near-verbatim from `avoid-ai-writing`'s "Never inject these"
section, because it names a real failure mode our own rewriting is exposed
to: fixing every flagged tell while quietly introducing new ones in the act
of "sounding more natural."

None of the following may be **added** to text that didn't already contain
it, even when the result reads clean:

- **Invented first person or reaction** that the source material never had.
  If the source has no `I`, no stated preference, no aside, the rewrite adds
  none — voice comes from what's actually there, not from installing a
  personality kit.
- **Manufactured stakes** ("this matters more than ever," "in a moment
  when...") not supported by the source.
- **Forced contrast against an invented opponent** — a "traditional
  approaches" strawman the source never argued against. This is already a
  protocol violation (`positive-characterization` flaw), and it's also
  something a rewrite can newly introduce while "fixing" a flat paragraph.
- **Staccato conversion** — chopping ordinary sentences into fragments to
  fake the sentence-rhythm variety in the technique above. Vary sentence
  length by varying the sentences, not by breaking a fine one in half.
- **Invented specifics** — a number, name, date, source, or mechanism the
  material never contained. This is the most tempting fix, because a
  concrete-sounding detail always reads better than a vague one, and it is
  worse than the vague phrasing it replaced. If a concrete detail is
  missing, flag the gap or use `[VERIFY]` — never fabricate one to fill it.
- **Performed candor** — "let's be honest," "here's the thing," "real talk,"
  "in the interest of full disclosure" (unless it's an actual conflict-of-
  interest disclosure, which is legitimate and should stay) — announcing
  transparency instead of just being transparent. If the frame can be
  deleted with no loss of information, it wasn't content.
- **Em-dash theatrics** — dashes staged for drama the content hasn't earned,
  added *during* a rewrite rather than present in the source. This is
  distinct from the open question below about what rate is acceptable in
  general; this entry is only about a rewrite *adding* dashes that weren't
  there to fix a different flaw.

**The test for any edit:** did the information in the rewrite come from the
source? Cutting filler, sharpening an existing claim, surfacing a buried
point — in scope. Adding stance, personality, or fact that wasn't there —
not in scope, regardless of how much better the sentence reads.

## Named structural patterns (a P1/P2 catalog, adapted and narrowed)

Severity is about how much it undercuts credibility, not about certainty of
machine authorship — Mozare's own `CLAUDE.md` already forbids treating
fluency or pattern-matches as evidence of anything; these are craft flags a
careful editor would raise regardless of who wrote the draft.

**P0 — breaks the protocol itself, not just the surface**
- Contrast before characterization (see protocol.md) — a term or claim
  defined by what it isn't before the reader knows what it is.
- Keyword-chain sentences — a comma-separated list of concepts standing in
  for an argued relation, with no sentence stating what the list *does*.
- Invented specificity — see the editor-constraints section above; this is
  the single most credibility-destroying tell, and a fluent read won't catch
  it because it has to be checked against source, not against prose quality.

**P1 — visible on a careful re-read**
- **Thesis-first opener** (narrative, letter, and artist-statement genres
  only — see the genre-scope note above; a research pre-proposal's own genre
  entry requires leading with the object and problem, which is not this
  tell). A personal or research narrative that leads with the frame instead
  of the material: "The hardest part of this project was X" before X has
  been shown. Start with the concrete situation; let the thesis emerge, per
  the protocol's own core writing principle.
- **Chiasmus / mirrored-clause parallelism as decoration.** A reversed
  parallel construction staged to sound like insight ("being specific about
  being wrong is more useful than being vague about being right") when the
  underlying claim isn't actually symmetric. Real insight is usually
  asymmetric; if the mirroring is doing the persuading instead of the
  content, cut it.
- **Mini-aphorism closer.** A short, quotable "lesson" fragment ending a
  paragraph that the paragraph's own content hasn't earned. Cut it or fold
  it into the preceding sentence.
- **Parallel-subject mirror.** Two consecutive sentences with mirrored
  noun-phrase openers ("The archive is one thing. Interpreting it is
  another.") used as a rhetorical tic rather than because the parallel is
  load-bearing.
- **"Turns out" / reveal-narrative pivot.** Staging a discovery instead of
  stating it: "Turns out the source contradicted the claim" → "The source
  contradicted the claim."
- **Tricolon stacking.** A rule-of-three construction is fine once; a
  paragraph that hits a triplet in every other sentence is a tic, not
  thinking. Count triplets per paragraph — more than one is suspicious.
- **Hedge-stacking.** Multiple hedges compounding in one clause ("may
  potentially suggest a possible..."). One deliberate hedge is fine; a stack
  is throat-clearing.

**P2 — worth a look, not automatically wrong**
- **Throat-clearing openers** that restate the obvious before getting to
  content.
- **Meta-commentary about the writing itself** ("this section will
  explore...") outside a roadmap paragraph where it's the genre-appropriate move.
- **Symmetric list padding** — three-to-five items of matching grammatical
  weight regardless of whether the underlying content is actually that
  symmetric.

## Open questions — do not flag these, and don't invent a threshold either

**Em-dash rate.** The three external tools surveyed disagree by more than 3x
(1 per 1,000 words, 1 per 500, 1 per 300 — see the survey file's cross-tool
comparison table), and none of their calibration is grounded in Mozare's own
prose rather than the blog/LinkedIn corpora those tools were built for. This
harness has deliberately not adopted a number. If a specific rate ever gets
decided (Mohammad's call), it goes here with its source; until then, don't
flag em-dash *rate* as a structural tell at all, and don't reason your own
way to a number in the meantime — a threshold that isn't written down here
is a prior, not a finding, and reporting it as though it were a documented
rule is worse than saying nothing. (Em-dash *theatrics* — a rewrite adding
new dashes for drama — is a real, separate rule; see the editor-constraints
section above.)

## How to use this file

Run this as a distinct pass from the mechanical `rg` check in
`banned-hard.txt` / `banned-review.txt` — it needs judgment, not just pattern
matching. `mozare-critic` applies this list as part of a genuinely separate
read; `mozare-finalize` requires that pass to have happened before treating a
draft as gate-checked. Don't apply any of it to quoted material, code, or
another author's words (see the escape hatch above). If you find yourself
applying a rule not written down in this file, that's your own prior, not
the standard — name it as an open question rather than reporting it as a flaw.
