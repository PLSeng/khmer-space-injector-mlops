# ======================================================
# Khmer decoding (space insertion)
# ======================================================
_KHMER_COMBINING = {
    "្",  # coeng (subscript marker)
    "់", "ៈ", "៎", "៏", "័", "៌", "៍", "៑", "៓", "៕", "។", "៘",
    "ា", "ិ", "ី", "ឹ", "ឺ", "ុ", "ូ", "ួ", "ើ", "ឿ", "ៀ", "េ", "ែ", "ៃ", "ោ", "ៅ",
    "ំ", "ះ",
}


def decode_spaces(text: str, pred_labels: list[int]) -> str:
    """
    label=1 means insert a space AFTER this character.
    Avoid inserting spaces before Khmer combining marks to not split grapheme clusters.
    """
    out: list[str] = []
    n = min(len(text), len(pred_labels))

    for i in range(n):
        ch = text[i]
        out.append(ch)

        if pred_labels[i] != 1:
            continue

        # If next codepoint is combining, don't insert a space
        if i + 1 < n and text[i + 1] in _KHMER_COMBINING:
            continue

        out.append(" ")

    return "".join(out).strip()
