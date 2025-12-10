import re
import sys

# ReisCode v0.1 – Türkçe Python Transpiler
# "eğer yazmam aq ise" yazınca çalışan dil

def turkce_to_python(kod):
    mappings = {
        r'eğer\s+(.*?)\s+ise:': r'if \1:',
        r'değilse\s+eğer\s+(.*?)\s+ise:': r'elif \1:',
        r'değilse:': r'else:',
        r'yaz\(["\']?(.*?)["\']?\)': r'print("\1")',
        r'döngü\s+(.*?):': r'for \1:',
    }
    
    ceviri = kod
    for turkce, ing in mappings.items():
        ceviri = re.sub(turkce, ing, ceviri, flags=re.MULTILINE)
    return ceviri

# Dosya kontrolü
if len(sys.argv) < 2:
    print("Kullanım: python reiscode.py dosya.tr")
    print("Abi dosya adı gir lan!")
    sys.exit()

dosya_adi = sys.argv[1]

try:
    with open(dosya_adi, 'r', encoding='utf-8') as f:
        turkce_kod = f.read()
except:
    print("Dosya bulunamadı kral, yolunu mu şaşırdın?")
    sys.exit()

python_kod = turkce_to_python(turkce_kod)

print("═" * 50)
print("Çevrilen Python kodu:")
print(python_kod)
print("═" * 50)

try:
    exec(python_kod)
except Exception as e:
    print(f"\nHata verdi abi: {e}")
    print("Ama siktir et, ben yine de selam vereyim:")
    print("Aleyküm selam dünya, reis! Yangın devam ediyor 🔥")
