---
name: mozare-finalize
description: Clear a draft for actual sending or submission — the export gate, the mechanical and structural checks, and a required separate mozare-critic pass. Has side effects (writes to _exports/ and _audits/). Invoke with $mozare-finalize <path>, manually and only, never automatically from mozare-write.
---

# Mozare Finalize (Codex)

Codex build of the same gate as the Claude Code `mozare-finalize` skill.
Claude Code enforces manual-only invocation with a
`disable-model-invocation: true` frontmatter field; Codex custom prompts
have no such field, but they also have no auto-triggering-by-description
mechanism at all — every Codex skill is already manual-only by construction,
invoked explicitly with `$name`. That happens to satisfy this skill's
manual-invocation requirement for free, but don't let that coincidence
loosen the underlying rule: `mozare-write` must never narrate these steps
as a substitute for actually running `$mozare-finalize`, and finalizing
must never happen in the same pass that just drafted or revised the text.

Finalizing is a different act from drafting: it is the decision that a text
is safe to leave Mohammad's hands. Do not run this from inside the same
pass that just wrote or revised the draft, and do not shortcut any step
because the draft "already looks done" — that judgment is exactly what
this gate exists to check independently.

This skill reads the `mozare-write` skill's own files as siblings
(typically `.agents/skills/mozare-finalize/` next to
`.agents/skills/mozare-write/` for a repo-vendored install, or the
equivalent under wherever your Codex prompts/skills directory actually
is). Every bare filename below (`protocol.md`, `structural-tells.md`,
`banned-hard.txt`, `banned-review.txt`) refers to that sibling directory —
locate it once with
`find ~ -maxdepth 6 -path '*/skills/mozare-write/protocol.md' 2>/dev/null`
if it's ever unclear, and use that directory for step 3's commands.

## Preconditions

- A concrete draft file exists (not just an idea of one).
- The destination is known: who receives it, what genre, what public/private
  boundary applies.

## Procedure

1. **Read** the draft in full.
2. **Run `$mozare-critic` in a brand-new Codex session** against it
   explicitly (a real separate invocation, passing only its path, genre,
   and recipient — not this skill reasoning about the draft itself).
   Codex has no subagent sandbox, so "brand-new session" is load-bearing
   here, not a formality — reusing the current conversation defeats the
   whole point of the pass. Do not proceed past a `fundamentally off`
   verdict; take it back to `mozare-write` for revision instead of
   finalizing around it. **This step-2 abort does not consume the one
   repair pass in step 6** — the draft returns to drafting and a later
   finalize run starts over with a fresh repair budget.
3. **Run the mechanical check**, both files, separately:
   ```
   rg -i -f <mozare-write skill directory>/banned-hard.txt <draft path>
   rg -i -f <mozare-write skill directory>/banned-review.txt <draft path>
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
7. **Write the cleared copy** — only on an outcome that actually clears.
   **Where it goes depends on what invoked this skill is running inside:**
   - If the current working directory is inside a git repository (check
     `git rev-parse --show-toplevel`): write to `<repo root>/_exports/<slug>--<date>--<n>.md`,
     matching the existing convention in mozare-wiki and this sandbox repo.
     If that repo has no `_exports/` entry in its `.gitignore` yet, add one
     — these are personal delivery copies, never project/archive content.
   - Otherwise (invoked from an arbitrary local folder with no enclosing
     repo — the ordinary case for a user-level install used across
     unrelated projects): write to `~/.codex/mozare-finalize/exports/<slug>--<date>--<n>.md`
     instead, creating that directory if needed. Never git-tracked, because
     there's no repo here to track it in.

   Either way, `<n>` is the next unused integer for that slug and date
   (check what's already there; **never overwrite an existing export** — a
   second run on the same draft the same day is a new numbered attempt, not
   a replacement).
8. **Write the audit record unconditionally** — this is the last action of
   *every* finalize run, including one that stops at step 2 or fails at
   step 6, not only a successful one. Same repo-vs-no-repo choice as step 7:
   `<repo root>/_audits/<date>--mozare-finalize--<slug>--<n>.md` when inside
   a repo, or `~/.codex/mozare-finalize/audits/<date>--mozare-finalize--<slug>--<n>.md`
   otherwise (same numbering discipline as step 7; never overwrite an
   existing audit file). Fields:
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
   When written inside a repo, this file is meant to be committed — it is
   the evidence the gate actually ran, and a blocked or aborted run is
   exactly the case where that evidence matters most; it must not be the
   one case that leaves no trace. When written to the no-repo fallback
   location, it has no commit to be part of, but the same "never leave a
   blocked run silent" rule still applies — the file's existence is the record.
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
