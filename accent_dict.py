import re


def clean_orth(orth):
    orth = re.sub('[()△×･〈〉{}]', '', orth)  #
    orth = orth.replace('…', '〜')  # change depending on what you use
    return orth


def is_katakana(s):
    num_ktkn = 0
    for ch in s:
        if ch == 'ー' or ('ァ' <= ch <= 'ヴ'):
            num_ktkn += 1
    return num_ktkn / max(1, len(s)) > .5


def hira_to_kata(s):
    return ''.join(
        [chr(ord(ch) + 96) if ('ぁ' <= ch <= 'ゔ') else ch for ch in s]
    )


def get_accent_dict(path):
    acc_dict = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            orths_txt, hira, hz, accs_txt, patts_txt = line.strip().split('\u241e')
            orth_txts = orths_txt.split('\u241f')
            if clean_orth(orth_txts[0]) != orth_txts[0]:
                orth_txts = [clean_orth(orth_txts[0])] + orth_txts
            patts = patts_txt.split(',')
            patt_common = patts[0]  # TODO: extend to support variants?
            if is_katakana(orth_txts[0]):
                hira = hira_to_kata(hira)
            for orth in orth_txts:
                if not orth in acc_dict:
                    acc_dict[orth] = []
                new = True
                for patt in acc_dict[orth]:
                    if patt[0] == hira and patt[1] == patt_common:
                        new = False
                        break
                if new:
                    acc_dict[orth].append((hira, patt_common))
    return acc_dict
