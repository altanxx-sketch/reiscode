#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ReisCode - Türkçe Kod Yangını - Geyik Versiyonu

Kullanım:
    python reiscode.py dosya.reis
veya
    python reiscode.py
    (sonra geyik modunda satır yazarsın)
"""

import sys
import re
import random
from pathlib import Path
import traceback


# Türkçe -> Python anahtar kelime sözlüğü
TURKISH_KEYWORDS = {
    "değilse_eğer": "elif",   # önce bunu değiştir, yoksa "değilse" ile kavga eder
    "eğer": "if",
    "değilse": "else",
    "iken": "while",
    "için": "for",
    "aralık": "range",

    "tanım": "def",
    "sınıf": "class",
    "dön": "return",

    "veya": "or",
    "ve": "and",
    "değil": "not",

    "doğru": "True",
    "yanlış": "False",

    "yaz": "print",
}

MOTIVATION_MESSAGES = [
    "Reis, kodu çalıştırıyoruz. Şu saatten sonra kader birliği yaptık.",
    "Derin bir nefes al, bu kod ya çalışır ya da bize güzel bir hata hikayesi bırakır.",
    "Bak şimdi güzel patlayabilir, hazırlıklı ol.",
    "Bu kodu yazan eller dert görmesin, hadi bakalım.",
    "Çalışırsa ben yazdım, patlarsa sen yazdın, anlaşalım.",
]

HEADER_LINE = "=" * 60


def translate_line(line: str) -> str:
    """
    Bir satır içindeki Türkçe anahtar kelimeleri
    Python karşılıklarına çevirir.
    Yorum satırlarının içini bozmaz.
    """

    stripped = line.lstrip()
    if stripped.startswith("#"):
        # Yorum satırı, dokunma, insanın özel alanı
        return line

    translated = line

    # En uzun anahtarları önce çevir
    for tr_word, py_word in sorted(
        TURKISH_KEYWORDS.items(),
        key=lambda x: -len(x[0])
    ):
        pattern = r"\b" + re.escape(tr_word) + r"\b"
        translated = re.sub(pattern, py_word, translated)

    return translated


def translate_source(src: str) -> str:
    """
    Tüm kaynak metni satır satır çevirir.
    """
    lines = src.splitlines()
    converted_lines = [translate_line(line) for line in lines]
    return "\n".join(converted_lines)


def pretty_traceback(exc: Exception) -> None:
    """
    Hata ayrıntılarını biraz tatlandırıp yazdırır.
    """
    tb = traceback.format_exc()
    print(HEADER_LINE)
    print("Teknik detaylar (mühendis ruhu için):")
    print(tb)
    print(HEADER_LINE)


def run_python_code(py_code: str, filename: str = "<reiscode>") -> None:
    """
    Çevrilmiş Python kodunu çalıştırır.
    Hata olursa Türkçe, geyik dolu bir çıktı verir.
    """
    try:
        compiled = compile(py_code, filename, "exec")
        exec_globals = {}
        exec(compiled, exec_globals, exec_globals)

    except SyntaxError as exc:
        print("")
        print("💥 Söz dizimi patladı reis")
        print("Kod biraz fazla özgür takılmış olabilir.")
        print("")
        print(f"Dosya       : {exc.filename}")
        print(f"Satır       : {exc.lineno}")
        print(f"Problemli   : {exc.text.strip() if exc.text else 'yok gibi'}")
        print(f"Açıklama    : {exc.msg}")
        pretty_traceback(exc)

    except NameError as exc:
        print("")
        print("🤦 İsim hatası reis")
        print("Bir şeyi çağırıyorsun ama hiç tanımamışsın. Önce tanım, sonra çağrı.")
        print(f"Mesaj       : {exc}")
        pretty_traceback(exc)

    except TypeError as exc:
        print("")
        print("🧩 Tür karmaşası reis")
        print("Bir şeyleri birbirine karıştırmış olabilirsin. Sayıya yazı ekleme, listeye muz atma gibi.")
        print(f"Mesaj       : {exc}")
        pretty_traceback(exc)

    except Exception as exc:
        print("")
        print("🔥 ReisCode Panik Merkezi 🔥")
        print("Abi nolur dikkat et ya, bir şeyler fena patladı...")
        print("")
        print(f"Hata türü   : {type(exc).__name__}")
        print(f"Mesaj       : {exc}")
        pretty_traceback(exc)


def run_file(path: Path) -> None:
    """
    .reis uzantılı bir dosyayı okuyup çalıştırır.
    """
    if not path.exists():
        print(f"📁 Dosya bulunamadı reis: {path}")
        return

    src = path.read_text(encoding="utf-8")
    py_code = translate_source(src)

    print(HEADER_LINE)
    print("ReisCode çeviri servisi devreye girdi.")
    print(f"Kaynak dosya : {path}")
    print(random.choice(MOTIVATION_MESSAGES))
    print(HEADER_LINE)

    print("Çevrilmiş Python kodu aşağıdadır, inkar edemeyiz:\n")
    print(py_code)
    print("\n" + HEADER_LINE)
    print("Şimdi bu kodu çalıştırıyoruz. Olur da patlarsa, birlikte güleriz.\n")

    run_python_code(py_code, filename=str(path))


def repl() -> None:
    """
    Etkileşimli ReisCode geyik modu.
    Kullanıcıya satır satır Türkçe komut yazdırır ve çalıştırır.
    """

    print(HEADER_LINE)
    print("ReisCode Etkileşimli Geyik Modu")
    print("Boş satır ile bloğu çalıştır, Ctrl+C ile kaç.")
    print("")
    print("Mini örnek:")
    print("    tanım selam(isim):")
    print("        eğer isim == 'reis':")
    print("            yaz('Hoş geldin büyük reis')")
    print("        değilse:")
    print("            yaz('Hoş geldin', isim)")
    print("")
    print("    selam('reis')")
    print(HEADER_LINE)

    buffer = []
    while True:
        try:
            line = input("reis_konsol> ")

        except KeyboardInterrupt:
            print("\nTam yerinde çıktın reis, görüşürüz 👋")
            break
        except EOFError:
            print("\nSessizce ayrıldın reis, saygı duyuyorum 👋")
            break

        # Boş satır: biriken bloğu çalıştır
        if not line.strip():
            if buffer:
                src = "\n".join(buffer)
                py_code = translate_source(src)
                run_python_code(py_code, filename="<reiscode-repl>")
                buffer.clear()
            continue

        buffer.append(line)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        # Dosya verilmemiş, direkt geyik moduna gir
        repl()
        return

    file_path = Path(argv[0])

    # Uzantı yoksa .reis varsay
    if file_path.suffix == "":
        file_path = file_path.with_suffix(".reis")

    run_file(file_path)


if __name__ == "__main__":
    main()
