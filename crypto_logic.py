ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ---------- CESAR ----------

def cesar_chiffrement(chaine, clef):
    chainechiffre = ""
    for eachcar in chaine:
        cipherd = int(((ord(eachcar) - 65 + int(clef)) % 26) + 65)
        chainechiffre += chr(cipherd)
    return chainechiffre


def cesar_dechiffrement(chaine, clef):
    chainedechiffre = ""
    for eachcar in chaine:
        dechpherd = int(((ord(eachcar) - 65 - int(clef)) % 26) + 65)
        chainedechiffre += chr(dechpherd)
    return chainedechiffre


# ---------- VERNAM ----------

def vernam_chiffrement(text_clair, cle):
    text_chiffre = ""
    for i in range(len(text_clair)):
        lettre_claire = text_clair[i]
        lettre_cle = cle[i]
        index_clair = ALPHABET.index(lettre_claire)
        index_cle = ALPHABET.index(lettre_cle)
        index_chiffre = (index_clair + index_cle) % 26
        text_chiffre += ALPHABET[index_chiffre]
    return text_chiffre


def vernam_dechiffrement(text_chiffre, cle):
    text_dechiffre = ""
    for i in range(len(text_chiffre)):
        lettre_chiffree = text_chiffre[i]
        lettre_cle = cle[i]
        index_chiffre = ALPHABET.index(lettre_chiffree)
        index_cle = ALPHABET.index(lettre_cle)
        index_dechiffre = (index_chiffre - index_cle) % 26
        text_dechiffre += ALPHABET[index_dechiffre]
    return text_dechiffre


# ---------- VIGENERE ----------

def _repeat_key_for_text(key: str, text: str) -> str:
    """
    Étend la clé pour avoir exactement la même longueur que le texte.
    Suppose que key et text sont déjà en majuscules et alphabetiques.
    """
    if not key:
        raise ValueError("La clé Vigenère ne peut pas être vide.")
    times = len(text) // len(key)
    rest = len(text) % len(key)
    return key * times + key[:rest]


def vigenere_chiffrement(text_clair: str, cle: str) -> str:
    """
    Chiffrement Vigenère classique sur A-Z uniquement.
    """
    cle_etendue = _repeat_key_for_text(cle, text_clair)
    text_chiffre = ""
    for i, lettre_claire in enumerate(text_clair):
        index_clair = ALPHABET.index(lettre_claire)
        index_cle = ALPHABET.index(cle_etendue[i])
        index_chiffre = (index_clair + index_cle) % 26
        text_chiffre += ALPHABET[index_chiffre]
    return text_chiffre


def vigenere_dechiffrement(text_chiffre: str, cle: str) -> str:
    """
    Déchiffrement Vigenère classique sur A-Z uniquement.
    """
    cle_etendue = _repeat_key_for_text(cle, text_chiffre)
    text_dechiffre = ""
    for i, lettre_chiffree in enumerate(text_chiffre):
        index_chiffre = ALPHABET.index(lettre_chiffree)
        index_cle = ALPHABET.index(cle_etendue[i])
        index_dechiffre = (index_chiffre - index_cle) % 26
        text_dechiffre += ALPHABET[index_dechiffre]
    return text_dechiffre
