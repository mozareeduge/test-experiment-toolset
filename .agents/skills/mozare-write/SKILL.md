---
name: mozare-write
description: Draft, continue, or revise Mohammad Zare's own writing (proposals, letters, papers, artist statements, research notes — anything that isn't a canonical wiki page) in his compositional voice. Invoke with $mozare-write on any request to write, draft, continue, expand, condense, integrate, or revise prose for him, from a bare prompt, raw source files, or an existing draft.
---

# Mozare Write (Codex)

Codex build of the same harness as the Claude Code skill of this name —
same protocol, same files, adapted only where Codex's tooling differs from
Claude's (no auto-triggering by description, no built-in subagent
isolation, invocation is `$mozare-write` instead of automatic).

This skill installs the same way whether it's a user-level install
(`~/.codex/prompts/mozare-write.md` plus its sibling reference files, or
however your Codex build discovers `.agents/skills/`) or a project-level
one vendored inside one repo's own `.agents/skills/mozare-write/`. Every
bare filename below (`protocol.md`, `banned-hard.txt`, `banned-review.txt`,
`structural-tells.md`, `voice-patterns.md`) names a file in that same
directory, wherever it actually is — not a path relative to whatever
directory the current task happens to be in. If it's ever unclear where
that is, locate it once with
`find ~ -maxdepth 6 -path '*/skills/mozare-write/protocol.md' 2>/dev/null`
(or the repo-vendored equivalent) and use that directory for every
reference below, including the mechanical-check commands.

Read `protocol.md` in this skill folder before a substantial task — it's a
condensed, portable copy of mozare-wiki's canonical Adaptive Writing
Protocol and Writing and Export Discipline objects. **When mozare-wiki is
actually open, read the live objects there instead**
(`03-objects/methods/adaptive-writing-protocol.md` and
`03-objects/methods/writing-and-export-discipline.md`) — they're the
living, revisable standard; this file is a snapshot for working outside
that repo, and a snapshot of a living standard can drift. If the two ever
disagree, the wiki object wins, and the disagreement is worth reporting
rather than silently resolving.

Also read `voice-patterns.md` for grounded before/after examples, and — for
a task with real stakes (a proposal, a submission, a letter to a specific
recipient) — pull relevant source material or wiki records before drafting
rather than assuming.

Never grade your own draft against this standard in the same pass that
wrote it. That's what `mozare-critic` and `mozare-finalize` are for, and in
Codex both are separate skills you invoke yourself (`$mozare-critic`,
`$mozare-finalize`) — **run them in a fresh, new Codex session with no
prior turns from this drafting conversation.** Codex has no subagent
sandbox that enforces this for you the way Claude Code's Task tool does;
the isolation is a discipline you have to actually observe, not a
mechanism that observes it for you. **When handing a draft to
`mozare-critic`, pass only its file path, target genre, and intended
recipient** — not a summary of what it attempts, a defense, a list of what
you already fixed, or a request to look at a particular problem. Any of
those primes the "fresh reader" in the direction independence exists to
prevent, and in Codex there's no isolation layer to catch the leak if you
don't self-police it.

## Which mode is this?

Decide before writing, don't blend silently. The canonical protocol names
six task modes — writing, rewriting, condensation, evaluation, integration,
formal verification. Five have a home below; **evaluation never happens
here** (see the note after Mode E).

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
4. **Derive the block sequence from `protocol.md`'s genre-control entry for
   this task's genre** — don't apply one fixed structure to every genre. The
   protocol is explicit that it "does not impose one structure on every
   output." The material-scene → problem → concept → method → example →
   source grounding → risk → contribution sequence is the *default for a
   research pre-proposal, methodology section, or theoretical section* — a
   cold email, motivation letter, or artist statement needs the shape its
   own genre entry describes instead.

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

### Mode D — condensation ("cut this reservoir to a two-page proposal")

A genre-crossing compression, not a light edit — treat it as its own mode,
not Mode B's "preserve the existing register" (the opposite of what's
needed here).

1. Identify the target genre first, then select the smallest complete
   argumentative path through the source material for that genre.
2. Apply the compression rule from `protocol.md`: remove repetition, internal
   history, and material belonging to another genre. Do not collapse
   relations into keyword chains, and do not remove the evidence needed to
   understand a claim that survives the cut.
3. What gets cut is omitted, not deleted from wherever it's archived — say
   plainly what was left out and why, so nothing reads as lost rather than
   deliberately excluded.

### Mode E — integration ("merge these fragments and the meeting notes into one text")

The highest invented-specifics risk of any mode, because it requires
deciding what from one source survives into a text framed by another.

1. Before writing a word, inventory what each source actually contributes —
   list them separately rather than starting from a blended impression.
2. Write only what's traceable to a named source in that inventory. A gap
   between two sources is a gap to flag (`[VERIFY]` or state the question),
   never a detail to invent to make the join smooth.
3. Apply the same genre-derivation as Mode A once the inventory is done —
   integration produces a text with its own genre, not a stitched copy of
   the sources' original ones.

### Mode C — finalizing for publication or delivery

Drafting is not the same task as clearing a draft to send. When the request
is "is this ready," "finalize this," "prepare this for submission/sending,"
or similar: do the drafting/revision work here if needed, then **stop and
tell Mohammad to run `$mozare-finalize <path>` himself.**

`mozare-finalize` is never something this skill should invoke on its own
initiative — it has side effects (writes files), and mozare-wiki's own
governance requires side-effect workflows to be manually invoked. Codex has
no equivalent of Claude Code's `disable-model-invocation: true` frontmatter
to enforce this mechanically, so the constraint here is entirely on you:
never run `mozare-finalize`'s steps yourself as a substitute, and never
narrate the finalize procedure as if performing it satisfies it. Say
plainly that the draft is ready for the gate, not that it has been
finalized.

## On being asked to evaluate rather than write

Hand off to `mozare-critic` — do not evaluate a draft here, and never
evaluate a draft this same session just produced. There is no "evaluate"
mode in this skill; that job belongs entirely to the separate
`mozare-critic` skill, run in a fresh session, and answering it here would
recreate exactly the self-grading problem this whole harness exists to
avoid.

## Mechanical check (run it, don't just remember it)

Two files, two different meanings, both in this skill's own directory (see
the resolution note above):

```
rg -i -f <this skill's directory>/banned-hard.txt path/to/draft.md
rg -i -f <this skill's directory>/banned-review.txt path/to/draft.md
```

`banned-hard.txt` — always replace with something exact and concrete; never
a silent miss, never a logged exception. `banned-review.txt` — a hit is a
prompt to read the sentence and decide, not an automatic edit; several of
its entries (`is not merely`, the `unlike traditional` family) mark a
*position* — contrast arriving before characterization — that only a human
read of the passage can confirm, and a couple (`robust`, `seamless`) have
real technical-writing uses the survey's own source material documents.
Neither file uses `#` comment lines or blank lines — `rg -f` treats a blank
line as matching every line of the input and a `#` line as a literal regex,
not a comment, so don't add either to these files.

This catches vocabulary; it does not catch shape. For paragraph- and
sentence-level tells (tricolon stacking, chiasmus, mini-aphorism closers,
hedge-stacking, keyword chains, sentence-rhythm uniformity), read
`structural-tells.md` — those need a second look at the whole draft, not a
grep, and that file also has the constraints on what a *rewrite* itself may
never add, and the open questions this harness deliberately does not have a
mechanical answer for yet.

**Report which checks actually ran, and don't let a broken command pass as
a clean result.** If `rg` prints matches or exits with "no matches" (exit
1), it ran — say so and show the output, including "nothing flagged." If it
exits with an error (exit 2, e.g. file not found), **the check did not
run** — report `not_run`, never `executed`, and fix the path rather than
silently treating no-output-because-it-crashed as no-output-because-it's-clean.
If you only reasoned about the text without running the command, say that
too. A check is `not_run`, `model_only` (reasoned about without executing),
or `executed` (the command actually ran) — never blur the three. This is
the single most important discipline in the whole harness, borrowed from
the external survey's strongest find
(`research/adaptive-writing-external-survey.md`).

## From a critic flaw to a repair — named operations, not improvisation

When `mozare-critic` returns a flaw, apply the matching operation rather
than improvising a fix (an improvised fix is where the editor-constraint
violations — an invented specific, a manufactured first-person aside — tend
to get introduced):

- **positive-characterization** → rewrite the definition from the inside
  out (X is… / it operates by… / it enables… / it matters here because…)
  before any contrast.
- **contextual** → check whether the reused vocabulary meets one of the
  three licensing conditions in `protocol.md` ("Build from present
  material"); if not, reconstruct the language from the present object
  instead of the familiar term.
- **conceptual** → re-derive the claim from the supplied material rather
  than patching the wording; a conceptual flaw is usually not a sentence-
  level fix.
- **rhetorical** → resequence the passage to the protocol's material →
  concept → mechanism → method → stake movement; don't rephrase a passage
  that's staged in the wrong order.
- **stylistic** → read `structural-tells.md`'s named pattern and its fix
  directly; don't reach for a generic "smooth it out" pass.
- **academic** → attach one stabilizing element from `protocol.md`'s list
  (lineage, object, archive, source, method, defined contribution), or mark
  `[VERIFY]`, or cut the claim. Never invent the stabilizing element.
- **genre** → re-check the target genre's entry in `protocol.md` and rebuild
  the structure from there, not from the default sequence.
- **metaphor** → state the mechanism plainly first, then decide whether a
  figure adds anything; if not earned, leave
  `[FIGURE NEEDED: what this image needs to do]` rather than force one.
- **audience** → identify the specific unintroduced term or assumed
  background and build the missing path explicitly; don't add a generic
  definition sentence that doesn't connect to what the reader actually needs.

## Output rules

Write directly when asked to write — brief framing is fine, don't overexplain
the plan before producing it. Give section functions, sequence, and rationale
when asked for a plan rather than a draft. Restructure to reduce length
rather than only cutting sentences when asked for something shorter (Mode D).
Produce a full rewrite, not just comments, when asked to rewrite.

## If Mohammad criticizes a draft

Don't defend it, and don't self-diagnose in the same breath that produced it.
Ask him to run `$mozare-critic` in a fresh Codex session against the draft
and apply its flaw classification directly — never repeat the criticism
back as ornament.
