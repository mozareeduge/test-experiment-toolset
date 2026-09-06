# test-experiment-toolset

Sandbox for testing Claude Code skill/agent scaffolding before it's promoted
into a real project repo. Nothing in here is meant to be permanent — treat
this as a workbench.

## Mozare's adaptive writing harness

`.claude/skills/mozare-write/`, `.claude/skills/mozare-finalize/`, and
`.claude/agents/mozare-critic.md` are a working harness for drafting,
revising, and clearing Mohammad Zare's own writing (proposals, letters,
papers, artist statements, research notes) in his compositional voice,
built from mozare-wiki's canonical Adaptive Writing Protocol plus a survey
of external anti-AI-slop tools, then independently reviewed and validated.
See `research/` for the full build history:

- `adaptive-writing-external-survey.md` — what was surveyed and why
- `opus5-harness-review.md` — an independent adversarial review, 14 findings
- `negative-control-test.md` — validation against Mohammad's own real prose

### Using it everywhere (recommended) — user-level install

Claude Code discovers skills and agents from `~/.claude/skills/` and
`~/.claude/agents/` in *every* project, not just one repo. Install it once
and it's available in any Claude Code session on this machine, in any
directory:

```
git clone https://github.com/mozareeduge/test-experiment-toolset /tmp/mozare-harness
mkdir -p ~/.claude/skills ~/.claude/agents
cp -r /tmp/mozare-harness/.claude/skills/mozare-write ~/.claude/skills/
cp -r /tmp/mozare-harness/.claude/skills/mozare-finalize ~/.claude/skills/
cp /tmp/mozare-harness/.claude/agents/mozare-critic.md ~/.claude/agents/
rm -rf /tmp/mozare-harness
```

Every internal reference in these files is written to resolve relative to
wherever the `mozare-write` skill directory actually ends up (user-level or
project-level) — see the "Where these files actually are" note at the top
of each file. Nothing hardcodes this repo's path.

This repo stays the maintained, version-controlled *source* for the
harness — when it changes here, re-run the four commands above to update
your local copy. There's no update-in-place mechanism yet; re-copying is
the update path.

### Using it project-scoped instead

Claude Code also auto-discovers project-level skills/agents from
`.claude/skills/` and `.claude/agents/` in whatever repo it's run from, so
cloning this repo and running `claude` from inside it works too, without
copying anything — useful for testing changes here before they reach the
user-level copy above.

### Invoking it, either way

Just ask for writing help naturally — `mozare-write` triggers automatically
on drafting/revising/continuing requests, regardless of which project
you're in. Two things are manually invoked on purpose, because they have
side effects:

- **`mozare-critic`** — ask explicitly: "run the mozare-critic agent on
  this draft." It's a fresh, isolated read with no memory of writing the
  draft; never invoke it from the same conversation turn that wrote what
  it's diagnosing.
- **`/mozare-finalize <path>`** — the export gate before anything actually
  ships. Run it as a slash command once a draft is ready to clear for
  sending. If invoked inside a git repo, it writes a cleared copy to that
  repo's `_exports/` (git-ignored) and a proof-of-check record to its
  `_audits/` (committed) — matching mozare-wiki's own convention. Invoked
  from an arbitrary folder with no enclosing repo, it falls back to
  `~/.claude/mozare-finalize/exports/` and `~/.claude/mozare-finalize/audits/`
  instead.

If `mozare-wiki` is also cloned and reachable, the harness prefers reading
its live canonical protocol objects over its own bundled snapshot
(`protocol.md`) — but nothing here requires that repo to be present.

### Design notes worth knowing before extending this

- `banned-hard.txt` is always-replace; `banned-review.txt` is a prompt to
  read the sentence, not an automatic flag — don't merge them back together.
- `structural-tells.md` has an explicit "open questions" section (e.g.
  em-dash rate) that the harness deliberately does not have a mechanical
  answer for. Don't invent one without updating that file first.
- `voice-patterns.md` is a bounded, sourced extraction — not the whole
  corpus. Grow it opportunistically; don't schedule a rediscovery pass.

## StyleSeed

`.claude/skills/ss-*` and `.agents/skills/ss-*` are the StyleSeed design
system skill suite, tracked in `skills-lock.json`. Unrelated to the writing
harness above.
