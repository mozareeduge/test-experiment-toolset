"""Locks in the fixture's own hand-verified ground truth.

This test has NO dependency on the ontograph engine (which doesn't exist
yet at Phase 0) — it only checks that the fixture's raw JSON matches the
`_fixture_ground_truth` block in manifest.json. Once the real engine
exists (Phase 1+), its census/mapping functions should be tested against
this SAME `_fixture_ground_truth` block rather than against a second,
possibly-drifted copy of these numbers — import `GROUND_TRUTH` from here.

Run: pytest fixtures/mini-ganjoor/test_fixture_ground_truth.py -q
"""
import json
import glob
import collections
import pathlib

HERE = pathlib.Path(__file__).parent
MIRROR_FORMS = ["آینه", "آیینه"]
RUST = "زنگار"

with open(HERE / "manifest.json", encoding="utf-8") as f:
    GROUND_TRUTH = json.load(f)["_fixture_ground_truth"]


def _scan():
    mirror_hits = collections.Counter()
    poems_with_mirror, poems_with_rust = [], []
    couplet_tight = []
    poem_files = sorted(glob.glob(str(HERE / "poets/*/ghazal/p*.json")))
    assert len(poem_files) == 15, "fixture should have exactly 15 poems"
    for fp in poem_files:
        d = json.loads(pathlib.Path(fp).read_text(encoding="utf-8"))
        mc, rc = set(), set()
        for v in d["Verses"]:
            text = v["Text"]
            ci = v["CoupletIndex"]
            for form in MIRROR_FORMS:
                if form in text:
                    mirror_hits[form] += 1
                    mc.add(ci)
            if RUST in text:
                rc.add(ci)
        if mc:
            poems_with_mirror.append(d["Id"])
        if rc:
            poems_with_rust.append(d["Id"])
        if mc & rc:
            couplet_tight.append(d["Id"])
    return mirror_hits, poems_with_mirror, poems_with_rust, couplet_tight


def test_poem_count():
    poem_files = glob.glob(str(HERE / "poets/*/ghazal/p*.json"))
    assert len(poem_files) == GROUND_TRUTH["eligible_poems_total"]


def test_mirror_hit_counts_match_ground_truth():
    mirror_hits, poems_with_mirror, poems_with_rust, couplet_tight = _scan()
    assert sum(mirror_hits.values()) == GROUND_TRUTH["mirror_anchor_hits_total"]
    assert dict(mirror_hits) == GROUND_TRUTH["mirror_anchor_hits_by_form"]


def test_poems_with_mirror_and_rust_match_ground_truth():
    _, poems_with_mirror, poems_with_rust, _ = _scan()
    assert sorted(poems_with_mirror) == sorted(GROUND_TRUTH["poems_with_mirror"])
    assert sorted(poems_with_rust) == sorted(GROUND_TRUTH["poems_with_rust"])


def test_poem_scale_coincidence_matches_ground_truth():
    _, poems_with_mirror, poems_with_rust, _ = _scan()
    coincidence = sorted(set(poems_with_mirror) & set(poems_with_rust))
    expected = sorted(int(x) for x in GROUND_TRUTH["poem_scale_mirror_rust_coincidence"])
    assert coincidence == expected


def test_couplet_scale_tight_cases_match_ground_truth():
    _, _, _, couplet_tight = _scan()
    # ground truth encodes couplet-scale cases as descriptive strings prefixed
    # with the poem id; extract just the ids for a robust structural check.
    expected_ids = sorted(
        int(s.split()[0]) for s in GROUND_TRUTH["couplet_scale_mirror_rust_coincidence"]
    )
    assert sorted(couplet_tight) == expected_ids


def test_zero_incidence_control_poet_has_no_hits():
    for fp in sorted(glob.glob(str(HERE / "poets/sample3/ghazal/p*.json"))):
        d = json.loads(pathlib.Path(fp).read_text(encoding="utf-8"))
        for v in d["Verses"]:
            for form in MIRROR_FORMS + [RUST]:
                assert form not in v["Text"], f"{fp} unexpectedly contains {form!r}"
