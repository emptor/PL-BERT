import string
from text_normalize import normalize_text, remove_accents

import string

# Assuming normalize_text and remove_accents functions are defined elsewhere
# and are appropriate for Spanish text.

special_mappings = {
    "que": "ke",
    "qui": "ki",
    "gue": "ge",
    "gui": "gi",
    "ce": "se",
    "ci": "si",
    "ll": "j",  # Latin American Spanish
    "ñ": "ɲ",
    "v": "b",  # 'v' and 'b' are pronounced the same in Spanish
    "z": "s",  # In Latin American Spanish, 'z' is pronounced as 's'
    "j": "x",
    "h": "",  # 'h' is silent in Spanish
    # Additional context-sensitive mappings can be placed here
}


def phonemize(text, global_phonemizer, tokenizer):
    text = normalize_text(remove_accents(text))
    words = tokenizer.tokenize(text)

    phonemes_bad = [
        (
            global_phonemizer.phonemize([word], strip=True)[0]
            if word not in string.punctuation
            else word
        )
        for word in words
    ]
    input_ids = []
    phonemes = []

    for i, word in enumerate(words):
        phoneme = phonemes_bad[i]

        for k, v in special_mappings.items():
            if word.startswith(k):  # Adjusted for context-sensitive beginnings
                phoneme = v + word[len(k) :]
                break

        # Adjustments for context-sensitive pronunciation
        if word.startswith("g") and len(word) > 1 and word[1] in "ei":
            phoneme = "x" + phoneme[1:]
        elif word.startswith("c") and len(word) > 1 and word[1] in "ei":
            phoneme = "s" + phoneme[1:]

        # Handling aspiration of 's' in specific contexts
        if "s" in word[:-1]:  # Check if 's' occurs not at the end of the word
            phoneme = phoneme.replace(
                "s", "sʰ", 1
            )  # Aspirate the first occurrence of 's'
        if word.endswith("s"):
            phoneme = phoneme[:-1] + "sʰ"  # Aspirate the final 's'

        input_ids.append(tokenizer.encode(word)[0])
        phonemes.append(phoneme)

    assert len(input_ids) == len(phonemes)
    r = {"input_ids": input_ids, "phonemes": phonemes}
    # print(r)
    return r
