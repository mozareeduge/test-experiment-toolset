# Ganjoor Ontograph

A research-apparatus specification for OOO-informed close/distant reading over
the [Ganjoor](https://ganjoor.net/) Persian poetry corpus, plus a starting
Claude Code skill scaffold for implementing it.

- `Ganjoor_Ontograph_Research_Apparatus_Project_Spec_v2.3.0.md` — the project
  specification (drop-in revision of v2.2.0; see `EVALUATION.md` for the diff
  and why each change was made).
- `EVALUATION.md` — the review that produced v2.3.0: a verified factual
  correction, real gaps closed, and the new Claude Code runtime binding
  (Part XIII of the spec).
- `../.claude/skills/persian-poetry-ontograph/` — the skill scaffold named in
  the spec's Part XIII. It is a scaffold, not a working implementation: the
  Python engine and CLI it shells out to (spec §59, §62) are not built yet.

This directory landed in this repository because it was the designated
target repo for this task. If this repository is a generic scratch/toolset
repo rather than the intended home for this project, the content here is
self-contained and easy to relocate wholesale.

Related repositories referenced by the spec:

- `ganjoor/ganjoor-data` — the pinned documentary corpus.
- `erfanbashar1/persian-poetry-ai-agent-plugin` — the existing
  Markdown/QMD/MCP retrieval layer this spec builds alongside, not on top of.
