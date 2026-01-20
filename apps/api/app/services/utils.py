# ======================================================
# Khmer decoding (space insertion)
# ======================================================
_KHMER_COMBINING = {
    "្",  # coeng (subscript marker)
    "់", "ៈ", "៎", "៏", "័", "៌", "៍", "៑", "៓", "៕", "។", "៘",
    "ា", "ិ", "ី", "ឹ", "ឺ", "ុ", "ូ", "ួ", "ើ", "ឿ", "ៀ", "េ", "ែ", "ៃ", "ោ", "ៅ",
    "ំ", "ះ",
}


def decode_spaces(
    text: str,
    pred_labels: list[int],
    insert_on_label: int = 1,
) -> str:
    """
    insert_on_label means: insert a space AFTER this character when label == insert_on_label.
    Avoid inserting spaces before Khmer combining marks to not split grapheme clusters.
    """
    out: list[str] = []
    n = min(len(text), len(pred_labels))

    for i in range(n):
        ch = text[i]
        out.append(ch)

        if pred_labels[i] != insert_on_label:
            continue

        # If next codepoint is combining, don't insert a space
        if i + 1 < n and text[i + 1] in _KHMER_COMBINING:
            continue

        out.append(" ")

    # if text longer than labels, append remaining
    if len(text) > n:
        out.append(text[n:])

    return "".join(out).strip()
