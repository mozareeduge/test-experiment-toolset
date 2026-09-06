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

## Preconditions

- A concrete draft file exists (not just an idea of one).
- The destination is known: who receives it, what genre, what public/private
  boundary applies.

## Procedure

1. **Read** the draft in full.
2. **Run the mozare-critic subagent** against it explicitly (a real separate
   invocation — not this skill reasoning about the draft itself). Do not
   proceed past a `fundamentally off` verdict; take it back to `mozare-write`
   for revision instead of finalizing around it.
3. **Run the mechanical check**:
   ```
   rg -i -f .claude/skills/mozare-write/banned-patterns.txt <draft path>
   ```
   Every hit is either fixed or logged as a deliberate, defensible exception.
   Record whether this actually ran (`executed`) or was reasoned about
   without running (`model_only`) — never let the report imply the stronger
   of the two happened.
4. **Apply `structural-tells.md`** to whatever the critic pass didn't already
   cover, including its editor-constraints section — a finalize-stage fix
   that "smooths" a sentence must not add a specific, a first-person aside,
   or a contrast the source material never contained.
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
   - claim permission (does the wording match what the evidence actually
     supports — check against mozare-wiki's claim records if the draft leans
     on wiki-sourced material and that repo is reachable);
   - omitted material (what belongs to another genre and was correctly left
     out, not lost);
   - version identity (is this the version that was actually approved).
6. **One repair pass, then stop.** If the critic or the export gate finds a
   blocking problem, send it back to `mozare-write` for one corrective pass,
   then re-run this gate once more. If it still fails, stop and report the
   unresolved issue plainly rather than cycling — this bound exists because
   an unbounded fix-and-recheck loop is how a gate stops actually gating.
7. **Write the cleared copy** to `_exports/<slug>--<date>.md` (git-ignored —
   holds personal delivery copies, not project/archive content). Inside
   mozare-wiki specifically, this is where the file lands; here in the
   sandbox the convention is the same, kept local.
8. **Write a short record** to `_audits/<date>--mozare-finalize--<slug>.md`
   with: the critic verdict, the mechanical-check result (and whether it was
   `executed` or `model_only`), the export-gate answers above, and any
   exceptions taken. This file is committed — it is the evidence the gate
   actually ran, not the text itself.
9. Report back: is it cleared, what was fixed, what exception was taken and
   why, whether a repair pass was used, and the exact path of the cleared copy.

## What this skill will not do

It will not clear a draft whose critic verdict is unresolved, will not
silently skip the export gate because "it's just an email," will not run a
second repair loop past the one bounded retry above, and will not write
directly into any canonical wiki path — a finalized personal text is not, by
itself, a canonical wiki page. If the task turns out to actually be about
writing or revising a mozare-wiki canonical article, stop and use that
repo's `wiki-write` skill instead.
