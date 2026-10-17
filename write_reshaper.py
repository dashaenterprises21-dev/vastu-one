from pathlib import Path

code = '''"""
VASTU ONE - Devanagari Reshaper for fpdf2
Fixes i-matra (ि) rendering order for legacy PDF generators
"""

import re

# Devanagari consonants and matras
DEVANAGARI_CONSONANTS = "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"
VIRAMA = "्"
I_MATRA = "ि"

def reshape_devanagari(text: str) -> str:
    """
    Reshape Devanagari text for legacy PDF renderers.
    Moves i-matra (ि) before its consonant cluster.
    """
    if not text:
        return text
    
    # Pattern: consonant cluster + i-matra
    # Cluster = consonant (virama consonant)*
    pattern = r'([' + DEVANAGARI_CONSONANTS + r'](?:' + VIRAMA + r'[' + DEVANAGARI_CONSONANTS + r'])*)' + I_MATRA
    
    def replacer(match):
        cluster = match.group(1)
        return I_MATRA + cluster
    
    return re.sub(pattern, replacer, text)


def reshape_text(text: str) -> str:
    """Alias for reshape_devanagari"""
    return reshape_devanagari(text)


if __name__ == "__main__":
    # Test cases
    tests = [
        "किताब",
        "किसान",
        "विकास",
        "रिसर्च",
        "ज्योतिषीय",
        "भविष्यवाणी",
        "महादशा",
        "अंतर्दशा",
        "प्रत्यंतर्दशा",
    ]
    for t in tests:
        print(f"Original: {t}")
        print(f"Reshaped: {reshape_devanagari(t)}")
        print()
'''

Path("engine/report/devanagari_reshaper.py").write_text(code, encoding="utf-8")
print("File written:", Path("engine/report/devanagari_reshaper.py").stat().st_size, "bytes")