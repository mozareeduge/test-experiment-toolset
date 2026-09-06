---
name: mozare-finalize
description: Clear a draft for actual sending or submission — the export gate, the mechanical and structural checks, and a required separate mozare-critic pass. Has side effects (writes to _exports/ and _audits/) and must be invoked manually, never silently from mozare-write.
disable-model-invocation: true
---

# Mozare Finalize

Finalizing is a different act from drafting: it is the decision that a text
is safe to leave Mohammad's hands. Do not run this from inside the same pass
that just wrote or revised the draft, and do not shortcut any step because
the draft "already looks done" — that judgment is exactly what this gate
exists to check independently.

This skill cannot be invoked by the model — that's intentional (it has side
effects, and mozare-wiki's governance requires side-effect workflows to be
manually invoked). If `mozare-write` said a draft is ready for this gate,
Mohammad runs `/mozare-finalize <path>` himself; nothing else substitutes
for that.

## Preconditions

- A concrete draft file exists (not just an idea of one).
- The destination is known: who receives it, what genre, what public/private
  boundary applies.

## Procedure

1. **Read** the draft in full.
2. **Run the mozare-critic subagent** against it explicitly (a real separate
   invocation, passing only its path, genre, and recipient — not this
   skill reasoning about the draft itself). Do not proceed past a
   `fundamentally off` verdict; take it back to `mozare-write` for revision
   instead of finalizing around it. **This step-2 abort does not consume the
   one repair pass in step 6** — the draft returns to drafting and a later
   finalize run starts over with a fresh repair budget.
3. **Run the mechanical check**, both files, separately:
   ```
   rg -i -f .claude/skills/mozare-write/banned-hard.txt <draft path>
   rg -i -f .claude/skills/mozare-write/banned-review.txt <draft path>
   ```
   Every `banned-hard.txt` hit is fixed, no exceptions. Every
   `banned-review.txt` hit is read in context and either fixed or logged as a
   deliberate, defensible exception — that file exists precisely because not
   every hit is wrong. Record whether these actually ran (`executed`) or
   were reasoned about without running (`model_only`) — if either command
   errors out instead of printing matches or "no matches," it did not run;
   record `not_run`, never `executed`.
4. **Apply `structural-tells.md`** to whatever the critic pass didn't already
   cover, respecting its genre-scope notes and its "Open questions" section
   (don't invent a threshold — e.g. an em-dash rate — that isn't written down
   there). Its editor-constraints section applies here too — a finalize-stage
   fix that "smooths" a sentence must not add a specific, a first-person
   aside, or a contrast the source material never contained.
5. **Run the export gate** from `protocol.md`'s writing-and-export-discipline
   section against this specific delivery — check, and record the answer
   for each:
   - source and citation status (every consequential claim traced to a real,
     checkable source, not invented);
   - current institutional facts (verify via real web access if available;
     otherwise mark `[VERIFY]` and flag it here rather than silently passing
     the check);
   - delivery and publication status (is this actually going out, or a draft
     being mistaken for final);
   - privacy and rights (should this specific material be visible to this
     specific recipient);
   - claim permission — **this skill does not govern claim status itself**
     (`protocol.md`'s "Relation to the archive" section is explicit about
     that). If the draft leans on wiki-sourced material and mozare-wiki is
     reachable, check the wording against
     `03-objects/methods/evidence-to-claim-workflow.md` and
     `03-objects/methods/evidence-firewall.md` rather than deciding it here
     from prose-level reasoning alone. If the check is non-trivial, record
     the open question in the audit and stop rather than adjudicating it;
   - omitted material (what belongs to another genre and was correctly left
     out, not lost);
   - version identity — see the `export_sha256` field in step 8; this is
     where that item gets an actual mechanism instead of a judgment call.
6. **One repair pass, then stop.** If the critic or the export gate finds a
   blocking problem, send it back to `mozare-write` for one corrective pass,
   then re-run this gate once more. If it still fails, stop and report the
   unresolved issue plainly rather than cycling — this bound exists because
   an unbounded fix-and-recheck loop is how a gate stops actually gating.
7. **Write the cleared copy** — only on an outcome that actually clears —
   to `_exports/<slug>--<date>--<n>.md`, where `<n>` is the next unused
   integer for that slug and date (check what's already there; **never
   overwrite an existing export** — a second run on the same draft the same
   day is a new numbered attempt, not a replacement). This directory is
   git-ignored — it holds personal delivery copies, not project/archive
   content. Inside mozare-wiki specifically, this is where the file lands;
   here in the sandbox the convention is the same, kept local.
8. **Write the audit record unconditionally** — this is the last action of
   *every* finalize run, including one that stops at step 2 or fails at
   step 6, not only a successful one. Path:
   `_audits/<date>--mozare-finalize--<slug>--<n>.md` (same numbering
   discipline as step 7; never overwrite an existing audit file). Fields:
   - `result:` one of `cleared | cleared_after_repair | blocked_by_critic |
     blocked_by_gate | aborted`
   - the critic verdict (or "not reached," if blocked before step 2 ran)
   - the mechanical-check result for both files, and whether each was
     `executed` or `model_only`
   - the export-gate answers from step 5, including any open question
     logged rather than adjudicated
   - `sources_consulted:` — every wiki record, source record, or external
     source that informed the draft (this is `writing-and-export-discipline.md`'s
     own procedure step 7 — "record which sources informed the output" —
     which is otherwise unimplemented anywhere in this harness)
   - any exception taken and why
   - `export_sha256:` (only on a clearing outcome) — the SHA-256 of the file
     written in step 7, so "version identity" is a fact this record carries
     rather than a question a later reader has to re-ask
   This file is committed — it is the evidence the gate actually ran, and a
   blocked or aborted run is exactly the case where that evidence matters
   most; it must not be the one case that leaves no trace.
9. Report back: is it cleared, what was fixed, what exception was taken and
   why, whether a repair pass was used, and the exact path of the cleared
   copy (or, on a blocked/aborted run, the exact path of the audit record
   and why nothing was cleared).

## What this skill will not do

It will not clear a draft whose critic verdict is unresolved, will not
silently skip the export gate because "it's just an email," will not run a
second repair loop past the one bounded retry above, will not adjudicate
claim permission itself when mozare-wiki's evidence-workflow objects say
otherwise, and will not write directly into any canonical wiki path — a
finalized personal text is not, by itself, a canonical wiki page. If the
task turns out to actually be about writing or revising a mozare-wiki
canonical article, stop and use that repo's `wiki-write` skill instead.
