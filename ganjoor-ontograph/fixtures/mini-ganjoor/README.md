# mini-ganjoor fixture corpus

Fabricated, schema-accurate synthetic corpus for automated tests. **Not
real Persian poetry and not real Ganjoor content** — every line was
written for this fixture and should never be quoted as if it were.

- 3 poets (`sample1`, `sample2`, `sample3`), 5 poems each, 15 poems total.
- `sample1` carries most of the mirror/rust signal (1 tight couplet-scale
  case, 1 broad-poem-only case, 1 mirror-alone case, 1 spelling-variant
  case, 1 figurative/ambiguous case).
- `sample2` carries one minority tight case plus four unrelated filler
  poems — this is what makes the ablation fixture meaningful: removing
  `sample1` should reduce, not eliminate, the tight-scale relation.
- `sample3` has zero incidence of either anchor — pure denominator padding
  and a check that a zero-incidence poet stays in the eligible-unit count
  rather than being dropped.

Regenerate with `python3 generate_fixture.py` (deterministic; re-running it
produces byte-identical output). **If you edit the generator, re-derive
`_fixture_ground_truth` in `manifest.json` by hand and then verify it
independently** — do not just trust arithmetic. The verification script
below is exactly how the numbers currently in `manifest.json` were checked
before being committed (it should print numbers matching
`_fixture_ground_truth` exactly):

```bash
python3 - <<'PYEOF'
import json, glob, collections
MIRROR_FORMS, RUST = ["آینه", "آیینه"], "زنگار"
mirror_hits, poems_with_mirror, poems_with_rust, couplet_tight = collections.Counter(), [], [], []
for f in sorted(glob.glob("poets/*/ghazal/p*.json")):
    d = json.load(open(f, encoding="utf-8")); pid = d["Id"]
    mc, rc = set(), set()
    for v in d["Verses"]:
        for form in MIRROR_FORMS:
            if form in v["Text"]: mirror_hits[form] += 1; mc.add(v["CoupletIndex"])
        if RUST in v["Text"]: rc.add(v["CoupletIndex"])
    if mc: poems_with_mirror.append(pid)
    if rc: poems_with_rust.append(pid)
    if mc & rc: couplet_tight.append((pid, sorted(mc & rc)))
print("mirror:", dict(mirror_hits), "poem-scale co-inc:", sorted(set(poems_with_mirror) & set(poems_with_rust)),
      "couplet-scale:", couplet_tight)
PYEOF
```

This fixture is the ground truth for spec §67 Tests A–F (Phase 7 of
`../../implementation/BUILD_PLAN.md`):

| Test (§67) | Fixture case |
|---|---|
| A — concentrated frequency | mirror is concentrated in `sample1` (5/6 poem hits) |
| B — scale collapse | poem 9102: co-occurs at poem scale, never at couplet scale |
| C — lexical ambiguity | poem 9105: figurative "mirror of the heart" |
| D — ablation false centre | removing `sample1` drops couplet-scale co-incidence from 2 to 1 |
| E — local close-reading insight | poem 9201's tight case survives `sample1` removal |
| F — research-made mediation | not covered here; needs a Relation-Object fixture built in Phase 4 |
