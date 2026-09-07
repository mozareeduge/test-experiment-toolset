# Portable mozare writing harness

Vendor-neutral build of the `mozare-write` / `mozare-critic` /
`mozare-finalize` harness, for using it outside Claude Code or Codex — a
Hermes-family model behind a custom or third-party harness, or any other
"standard" agentic setup that consumes a system prompt rather than
discovering skills from a folder convention.

Claude Code and Codex have their own native, richer builds of this same
harness elsewhere in this repo:

- `.claude/skills/mozare-write/`, `.claude/skills/mozare-finalize/`,
  `.claude/agents/mozare-critic.md` — Claude Code (skills + a real
  subagent with its own tool restrictions and context isolation).
- `.agents/skills/mozare-write/`, `.agents/skills/mozare-critic/`,
  `.agents/skills/mozare-finalize/` — Codex (`$name` custom prompts).

This directory (`portable/`) is what to use for anything else. It
intentionally serves **both** "Hermes" and "any other standard agentic
env" with the same three files, rather than maintaining near-duplicate
content twice: neither has a native skill-discovery or subagent-sandboxing
mechanism, so both consume the harness the same way — as plain text loaded
into a system prompt, a tool description, or a document the model reads —
and the isolation/manual-invocation guarantees that Claude Code and Codex
get from their platforms have to be re-stated as explicit discipline
instead. That restatement is the only real difference from the native
builds; the compositional standard itself (`shared/protocol.md`,
`shared/voice-patterns.md`, `shared/structural-tells.md`, the banned-word
lists) is identical everywhere.

## What's here

```
portable/
  README.md              this file
  mozare-write.md         drafting/revision — load whenever asked to write
  mozare-critic.md        fresh-reader diagnosis — load in a brand-new,
                           memory-less session, never the one that drafted
  mozare-finalize.md      the export gate — load only when the operator
                           deliberately wants to clear a draft to send
  shared/
    protocol.md            condensed Adaptive Writing Protocol +
                           Writing and Export Discipline
    voice-patterns.md      grounded before/after examples
    structural-tells.md    paragraph/sentence-level tells + their fixes
    banned-hard.txt         always-replace vocabulary
    banned-review.txt      judgment-call vocabulary
```

## How to use it

1. **Copy the whole `portable/` directory** wherever your harness reads
   prompts, documents, or context from. It's self-contained — nothing in
   it references a path outside itself except the optional live
   mozare-wiki objects mentioned inline (purely optional, not required).
2. **Load `mozare-write.md`** as the system prompt (or a tool/function
   description, or a document in context) for a drafting or revision
   session. It expects `shared/` to sit next to it; if your harness has a
   file-reading tool, it can read `shared/*` on demand instead of having
   everything inlined up front.
3. **Never load `mozare-critic.md` in the same session that ran
   `mozare-write.md`.** Start over — a genuinely new conversation, thread,
   or context window with nothing carried in from drafting except the
   draft's file path (or text), target genre, and intended recipient. This
   is the one rule the whole harness depends on, and it is the one thing
   no vendor-neutral prompt can enforce for you — your harness's operator
   has to actually do it.
4. **Load `mozare-finalize.md` only when a human deliberately wants to
   clear a draft for sending.** Never let `mozare-write.md` trigger it
   automatically, and never let a model narrate finalize's steps as a
   substitute for actually running them in their own session.

## If your harness has no file-reading tool at all

Some Hermes deployments and minimal agentic harnesses give the model only
a system prompt and no tools, or only tool-calling with no filesystem
access. In that case, the operator has to paste the contents of
`shared/protocol.md`, `shared/voice-patterns.md`, `shared/structural-tells.md`,
`shared/banned-hard.txt`, and `shared/banned-review.txt` directly into the
prompt before using `mozare-write.md`, `mozare-critic.md`, or
`mozare-finalize.md` for real work — each file says this explicitly rather
than silently degrading into "reasoning from vibes." The mechanical
`rg`-based checks in `mozare-write.md`/`mozare-critic.md`/`mozare-finalize.md`
likewise cannot run without shell access; in that case the model must
report the check as `not_run`, never claim it as `executed`.

## Keeping this in sync

`shared/*` here is a copy, not a symlink, of the same files vendored inside
`.claude/skills/mozare-write/` and `.agents/skills/mozare-write/` — a
deliberate choice so this directory stays copy-and-go portable on its own,
matching how the Claude Code build is already documented as installed (see
the root `README.md`). When the shared content changes, re-copy it into
all three locations; there's no update-in-place mechanism yet.
