---
name: mozare-write
description: Draft, continue, or revise Mohammad Zare's own writing (proposals, letters, papers, artist statements, research notes — anything that isn't a canonical wiki page) in his compositional voice. Triggers on any request to write, draft, continue, expand, condense, or revise prose for him, from a bare prompt, raw source files, or an existing draft.
---

# Mozare Write

Read `protocol.md` in this skill folder before a substantial task — it's a
condensed, portable copy of mozare-wiki's canonical Adaptive Writing
Protocol and Writing and Export Discipline objects. **When mozare-wiki is
actually open, read the live objects there instead**
(`03-objects/methods/adaptive-writing-protocol.md` and
`03-objects/methods/writing-and-export-discipline.md`) — they're the living,
revisable standard; this file is a snapshot for working outside that repo.
If the two ever disagree, the wiki object wins, and the disagreement is
worth reporting rather than silently resolving.

Also read `voice-patterns.md` for grounded before/after examples, and — for
a task with real stakes (a proposal, a submission, a letter to a specific
recipient) — pull relevant source material or wiki records before drafting
rather than assuming.

Never grade your own draft against this standard in the same pass that wrote
it. That's what `mozare-critic` (a separate subagent, no memory of writing
the draft) and `mozare-finalize` (a separate, manually-invoked skill) are for.

## Which mode is this?

Decide before writing, don't blend silently:

### Mode A — from scratch (a prompt, and maybe raw inputs)

Nothing exists yet but the request, possibly with attached rough notes,
source PDFs/DOCX, or a call for proposals.

1. Read every real supplied file before drafting — don't assume its content.
2. Run the protocol's "before writing" diagnosis (genre, audience, purpose,
   central problem, strongest concrete materials, source traditions, density,
   rhetorical rhythm, academic risks, the contribution the text must make) —
   silently, then write from it.
3. If the input is rough, compressed, multilingual, or fragmentary: infer the
   conceptual problem underneath rather than polishing the surface; separate
   core material from reserve; classify anything speculative (hypothesis,
   research pressure, possible route, unsuitable for this genre) instead of
   presenting it as settled.
4. Build the draft block by block (material scene → problem → concept →
   method → example → source grounding → risk → contribution), one function
   per block, following `protocol.md`'s structural strategy and genre-control
   table.

### Mode B — from the middle (a draft, fragment, or reservoir exists)

1. Read the existing material in full before changing anything — its own
   genre, its stage of finish, and where its register has already drifted
   from `voice-patterns.md`.
2. Distinguish what's core, what's reserve, and what belongs to a different
   genre than the one now being asked for — per the protocol, omit rather
   than delete material that belongs elsewhere.
3. Continue or rewrite in the register the existing material already
   establishes unless asked to change it; if asked to change it, say what
   changes and why rather than silently overwriting voice along with content.
4. If the existing text already violates the protocol (contrast before
   characterization, keyword chains, invented specifics, generic filler),
   fix those as part of the revision — don't preserve a flaw just because it
   was already there.
5. Applies here as much as to fresh drafting: don't fix a flagged tell by
   introducing a new one. Read `structural-tells.md`'s editor-constraints
   section before rewriting someone's — including your own earlier — prose.

### Mode C — finalizing for publication or delivery

Drafting is not the same task as clearing a draft to send. When the request
is "is this ready," "finalize this," "prepare this for submission/sending,"
or similar: do the drafting/revision work here if needed, then hand off to
the **`mozare-finalize`** skill (invoke it explicitly) rather than declaring
the draft done from inside this skill. Finalization requires the export gate,
the mechanical checks, and a `mozare-critic` pass that this skill cannot
supply on its own.

## Mechanical check (run it, don't just remember it)

Before treating any draft as finished enough to hand to `mozare-finalize` or
to the user:

```
rg -i -f banned-patterns.txt path/to/draft.md
```

Anything flagged gets replaced with something exact and concrete, or is a
deliberate, defensible exception — never a silent miss. This catches
vocabulary; it does not catch shape. For paragraph- and sentence-level tells
(tricolon stacking, chiasmus, mini-aphorism closers, hedge-stacking, keyword
chains, sentence-rhythm uniformity), read `structural-tells.md` — those need
a second look at the whole draft, not a grep, and that file also has the
constraints on what a *rewrite* itself may never add.

**Report which checks actually ran.** If you ran the `rg` command, say so
explicitly and show what it flagged (including "nothing flagged"). If you
only reasoned about the text without running it, say that too. Never let a
mechanical check's absence read as though it happened — this is the single
most important discipline in the whole harness, borrowed from the external
survey's strongest find (`research/adaptive-writing-external-survey.md`):
a check is `not_run`, `model_only` (you reasoned about it without executing
anything), or `executed` (the command actually ran) — never blur the three.

## Output rules

Write directly when asked to write — brief framing is fine, don't overexplain
the plan before producing it. Give section functions, sequence, and rationale
when asked for a plan rather than a draft. Diagnose strengths, risks, and
next revision when asked to evaluate, rather than silently rewriting.
Restructure to reduce length rather than only cutting sentences when asked
for something shorter. Produce a full rewrite, not just comments, when asked
to rewrite.

## If Mohammad criticizes a draft

Don't defend it, and don't self-diagnose in the same breath that produced it.
Ask him to invoke the `mozare-critic` subagent against the draft and apply
its flaw classification directly — never repeat the criticism back as
ornament.
