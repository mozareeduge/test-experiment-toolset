#!/usr/bin/env python3
"""Generate the mini-ganjoor fixture corpus with known ground truth.

This is FABRICATED synthetic text, not real Ganjoor content — it exists
only to give the deterministic engine (spec Part IX) a corpus small enough
to reason about by hand and a "true distribution" fixed in advance (spec
Part XI §67: "crafted miniature corpora where the true distribution is
known"). Do not treat any line here as real Persian poetry.

Schema is a best-effort match to the real ganjoor-data JSON, verified
against a live poem at `poets/hafez/ghazal/sh1.json` in
erfanbashar1/persian-poetry-ai-agent-plugin on 2026-08-27 for the Poem/
Section/Verse fields. Poet.json and _cat.json fields beyond Id/Name/
Nickname/Description and Id/Title/Path/ChildCategories/Poems are NOT
independently verified against the real schema and should be treated as
plausible approximations only — do not build engine logic that depends on
an unverified field here without checking it against a real fixture first.

Run: python3 generate_fixture.py
Writes the poets/, index/, and manifest.json under this directory.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent

MIRROR = "آینه"
MIRROR_VARIANT = "آیینه"
RUST = "زنگار"

def section(verses: list[tuple[str, str]], poem_format="Ghazal"):
    """verses: list of (right_hemistich, left_hemistich) per couplet.

    PlainText is DERIVED from the verses (a plain-text rendering of the
    same couplets), matching real Ganjoor semantics where the section's
    plain text is the same source text as the Verses array, not an
    independent paraphrase — see the fork's own skill docs on the «متن
    ساده» field. Any anchor census must therefore count each occurrence
    once at the verse level; counting PlainText and Verses separately
    would double-count every hit in this fixture (and, if unnoticed,
    would double-count in the real corpus too).
    """
    v = []
    order = 1
    plain_lines = []
    for ci, (right, left) in enumerate(verses):
        v.append({"VOrder": order, "Position": "Right", "Text": right,
                   "CoupletIndex": ci, "SectionIndex1": 0})
        order += 1
        v.append({"VOrder": order, "Position": "Left", "Text": left,
                   "CoupletIndex": ci, "SectionIndex1": 0})
        order += 1
        plain_lines.append(f"{right} / {left}")
    plain_text = "\n".join(plain_lines)
    sec = {
        "Index": 0, "Number": 1, "SectionType": "WholePoem", "VerseType": "First",
        "RhymeLetters": "ها", "PlainText": plain_text,
        "HtmlText": f"<div class='b'>{plain_text}</div>",
        "PoemFormat": poem_format, "CoupletsCount": len(verses),
    }
    return sec, v

def poem(poem_id, cat_id, title, verses, summary):
    sec, v = section(verses)
    return {
        "Id": poem_id, "CatId": cat_id, "Title": title,
        "FullTitle": title, "FullUrl": f"/fixture/{poem_id}",
        "RhymeLetters": "ها", "SourceName": "mini-ganjoor-fixture",
        "SourceUrlSlug": "fixture", "PoemSummary": summary,
        "Metre": {"Id": 1, "Rhythm": "فعولن فعولن فعولن فعل (fixture metre)"},
        "Sections": [sec], "Verses": v,
    }

POETS = {}
POEMS = {}

# --- Poet 1: two tight mirror-rust cases, one broad-only, one spelling
#     variant, one figurative/ambiguous case. This poet is the ablation
#     "dominant source" for the tight-scale relation. ---
POETS["sample1"] = {"Id": 9001, "Name": "شاعر آزمایشی یک", "Nickname": "آزمایشی۱",
                     "Description": "Fabricated fixture poet, not a real historical figure."}

POEMS[9101] = poem(9101, 1, "غزل آزمایشی ۱-۱",
    [(f"{MIRROR} در دست من است امشب", f"{RUST} بر آن نشسته پنهان"),
     ("باد سحری وزید آرام", "بر رخ ما و بر رخ ایوان")],
    "Tight case: mirror and rust share the first couplet.")

POEMS[9102] = poem(9102, 1, "غزل آزمایشی ۱-۲",
    [(f"{MIRROR} به دیوار کهن آویزان", "روزی روشن نشان می‌داد"),
     ("سال‌ها بگذشت و خاموش شد", "دیگر پیدا نبود آن تابان"),
     ("در پستوی خانه چیزی بود", f"{RUST} به زیر زمین در انبان")],
    "Broad-only case: mirror and rust appear in the same poem but different couplets.")

POEMS[9103] = poem(9103, 1, "غزل آزمایشی ۱-۳",
    [(f"{MIRROR} تنها بر طاقچه نشسته", "کسی به او نگاه نمی‌کند")],
    "Mirror alone, no rust — contributes to prevalence only.")

POEMS[9104] = poem(9104, 1, "غزل آزمایشی ۱-۴",
    [(f"{MIRROR_VARIANT} کهنه در صندوق خانه", "خاک بر او نشسته آرام")],
    "Spelling-variant anchor test (آیینه instead of آینه); no rust present.")

POEMS[9105] = poem(9105, 1, "غزل آزمایشی ۱-۵",
    [(f"{MIRROR} دل من شکسته از غم", "نه از شیشه، که از اندوه")],
    "Figurative/ambiguous case: 'mirror of the heart', not a literal object — "
    "intended calibration test for the ambiguous Occurrence Assessment.")

# --- Poet 2: one tight case (minority contributor), rest unrelated filler.
#     Ablating poet 1 should leave this poet's tight case surviving, so the
#     relation is concentrated (retention > 0%) rather than eliminated
#     entirely — a more realistic ablation fixture than a 0% collapse. ---
POETS["sample2"] = {"Id": 9002, "Name": "شاعر آزمایشی دو", "Nickname": "آزمایشی۲",
                     "Description": "Fabricated fixture poet, not a real historical figure."}

POEMS[9201] = poem(9201, 2, "غزل آزمایشی ۲-۱",
    [(f"{MIRROR} و {RUST} در یک نفس", "با هم به دست باد سپردیم")],
    "Tight case from the minority poet: mirror and rust in the same couplet.")

POEMS[9202] = poem(9202, 2, "غزل آزمایشی ۲-۲",
    [("باغ بهاری پر از گل سرخ", "بلبل به شاخه نغمه می‌خواند")],
    "Unrelated filler poem (control unit for the denominator).")

POEMS[9203] = poem(9203, 2, "غزل آزمایشی ۲-۳",
    [("کوه بلند و رود روان", "در دامنه چادر زدیم")],
    "Unrelated filler poem (control unit for the denominator).")

POEMS[9204] = poem(9204, 2, "غزل آزمایشی ۲-۴",
    [("مرغ سحر آواز خواند", "بر شاخه‌ی بید کهنسال")],
    "Unrelated filler poem (control unit for the denominator).")

POEMS[9205] = poem(9205, 2, "غزل آزمایشی ۲-۵",
    [("شمع فروزان تا سحر", "قصه‌ی دل با کس نگفت")],
    "Unrelated filler poem (control unit for the denominator).")

# --- Poet 3: zero incidence of either anchor. Purely denominator padding,
#     and a check that a poet with no hits is still counted as eligible
#     units contributing zero, not silently dropped from the field. ---
POETS["sample3"] = {"Id": 9003, "Name": "شاعر آزمایشی سه", "Nickname": "آزمایشی۳",
                     "Description": "Fabricated fixture poet, not a real historical figure."}

for i, text in enumerate([
    "باران بهاری بر بام",
    "کاروان در دشت خاموش",
    "ستاره‌ای بر آسمان شب",
    "درخت کهن در باد",
    "چشمه‌ای در دل کوه",
], start=1):
    pid = 9300 + i
    POEMS[pid] = poem(pid, 3, f"غزل آزمایشی ۳-{i}",
        [(text, "بی هیچ نشانی از این دو یافت نمی‌شود")],
        "Control poem, no anchors present, poet 3 has zero incidence.")

POET_SLUGS = {"sample1": 9001, "sample2": 9002, "sample3": 9003}
POET_POEM_IDS = {
    "sample1": [9101, 9102, 9103, 9104, 9105],
    "sample2": [9201, 9202, 9203, 9204, 9205],
    "sample3": [9301, 9302, 9303, 9304, 9305],
}

def write():
    for slug, pdata in POETS.items():
        poet_dir = ROOT / "poets" / slug
        (poet_dir / "ghazal").mkdir(parents=True, exist_ok=True)
        (poet_dir / "poet.json").write_text(
            json.dumps(pdata, ensure_ascii=False, indent=2), encoding="utf-8")
        cat = {
            "Id": POET_SLUGS[slug], "PoetId": POET_SLUGS[slug],
            "Title": "غزلیات آزمایشی", "Path": f"/{slug}/ghazal",
            "ChildCategories": [], "Poems": POET_POEM_IDS[slug],
        }
        (poet_dir / "ghazal" / "_cat.json").write_text(
            json.dumps(cat, ensure_ascii=False, indent=2), encoding="utf-8")
        for pid in POET_POEM_IDS[slug]:
            (poet_dir / "ghazal" / f"p{pid}.json").write_text(
                json.dumps(POEMS[pid], ensure_ascii=False, indent=2), encoding="utf-8")

    manifest = {
        "SchemaVersion": 1,
        "GeneratedAtUtc": "2026-08-27T00:00:00Z",
        "PoetsCount": len(POETS),
        "PoemsCount": len(POEMS),
        "IdIndexShardSize": 2000,
        "UrlTemplates": {
            "Poet": "poets/{poetSlug}/poet.json",
            "Category": "poets/{poetSlug}/{catPath}/_cat.json",
            "Poem": "poets/{poetSlug}/{catPath}/{poemSlug}.json",
        },
        "Poets": [{"Id": POET_SLUGS[s], "Nickname": POETS[s]["Nickname"],
                    "FullUrl": f"/{s}"} for s in POETS],
        "_fixture_ground_truth": {
            "note": "Computed by hand, verse-by-verse, from the poems above "
                    "(each verse counted at most once per anchor; see the "
                    "PlainText-derivation comment on section() for why "
                    "PlainText must not be counted separately from Verses). "
                    "The engine's own results must match these exactly on "
                    "this fixture, or the fixture/engine disagreement is a "
                    "bug to root-cause, not a fixture to quietly edit.",
            "eligible_poems_total": len(POEMS),
            "mirror_anchor_hits_total": 6,
            "mirror_anchor_hits_by_form": {"آینه": 5, "آیینه": 1},
            "rust_anchor_hits_total": 3,
            "poems_with_mirror": [9101, 9102, 9103, 9104, 9105, 9201],
            "poems_with_rust": [9101, 9102, 9201],
            "mirror_prevalence_poem_scale": "6/15",
            "poem_scale_mirror_rust_coincidence": ["9101", "9102", "9201"],
            "couplet_scale_mirror_rust_coincidence": [
                "9101 couplet 0 (mirror in Right, rust in Left of the same couplet)",
                "9201 couplet 0 (mirror and rust both in the Right hemistich)"
            ],
            "couplet_scale_broad_only_case": "9102 (mirror in couplet 0, rust in couplet 2 -- same poem, never the same couplet)",
            "ablation_remove_sample1_poet_scale_retention": "1/3 poems remain (9201 only)",
            "ablation_remove_sample1_couplet_scale_retention": "1/2 couplet-scale cases remain (9201 only)",
            "ambiguous_occurrence_assessment_case": "poem 9105 (figurative 'mirror of the heart')",
            "anchor_normalization_case": "poem 9104 (آیینه spelling variant, no rust present)",
            "zero_incidence_control_poet": "sample3 (all 5 poems, 0 mirror, 0 rust)",
        },
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    write()
    print("Wrote fixture corpus under", ROOT)
