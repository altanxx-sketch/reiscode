#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ReisCode - Türkçe Kod Yangını - Geyik + Hata Kodu + Reisçe Sözlük Versiyonu

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


HEADER_LINE = "=" * 60

MOTIVATION_MESSAGES = [
    "Reis, kodu çalıştırıyoruz. Bu noktadan sonra kader ortaklığı var.",
    "Derin bir nefes al, bu kod ya çalışır ya da bize güzel bir hata hikayesi bırakır.",
    "Şimdi güzel patlayabilir, ruhunu hazırlaman iyi olabilir.",
    "Bu satırları yazan eller dert görmesin, bakalım ne olacak.",
    "Çalışırsa benim sayemde, patlarsa sen yazdın, aramızda kalsın.",
]

# Eski sade Türkçe anahtarlar (geriye dönük uyumluluk için)
BASE_KEYWORDS = {
    "değilse_eğer": "elif",
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

# Yeni: Reisçe geyik sözlüğü + kısaltmalar
REIS_FUN_KEYWORDS = {
    # Temel kontrol yapıları
    "yani": "if",
    "yn": "if",

    "he_olmadıysa": "elif",
    "ho": "elif",

    "olmadı": "else",
    "om": "else",

    "döne_döne": "for",
    "dd": "for",

    "dön_dur": "while",
    "dr": "while",

    "kes_kardeşim": "break",
    "ks": "break",

    "devam_reis": "continue",
    "drs": "continue",

    "boşver_gitsin": "pass",
    "bv": "pass",

    "geri_ver": "return",
    "gv": "return",

    "tarif_et": "def",
    "tf": "def",

    "ekip": "class",
    "ek": "class",

    "içinde_mi": "in",
    "im": "in",

    "değil_abi": "not",
    "da": "not",

    "hem_de": "and",
    "hd": "and",

    "ya_da": "or",
    "yd": "or",

    # Veri tipleri
    "tam_sayıcık": "int",
    "ts": "int",

    "kaypak_sayı": "float",
    "ksy": "float",

    "yazı_metin": "str",
    "ym": "str",

    "doğru_mu_ulan": "bool",
    "dmu": "bool",

    "torba": "list",
    "trb": "list",

    "torba_kilitli": "tuple",
    "trk": "tuple",

    "torba_tekil": "set",
    "ttk": "set",

    "sözlükçük": "dict",
    "szk": "dict",

    "hiçbişey": "None",
    "hç": "None",

    # Liste / sözlük işleri
    "torbaya_at": "append",
    "ta": "append",

    "araya_sokuştur": "insert",
    "asok": "insert",

    "uzat_gitsin": "extend",
    "ug": "extend",

    "kopar": "pop",
    "kp": "pop",

    "sök": "remove",
    "sk": "remove",

    "nerede_ulan": "index",
    "nrd": "index",

    "say_say": "count",
    "ss": "count",

    "anahtarlar": "keys",
    "ak": "keys",

    "değerler": "values",
    "drl": "values",

    "çiftler": "items",
    "cft": "items",

    "kap": "get",
    "kapk": "get",

    # Fonksiyonel
    "gizli_fonksiyon": "lambda",
    "gf": "lambda",

    "hepsine_uygula": "map",
    "hu": "map",

    "elemeleri_yap": "filter",
    "ely": "filter",

    "topla_şunları": "zip",
    "tsn": "zip",

    "çağrılabilir_mi": "callable",
    "crm": "callable",

    "kim_konuştu": "input",
    "kk": "input",

    "yardım_et_reis": "help",
    "yrm": "help",

    # Dosya işleri
    "aç_bakim": "open",
    "ab": "open",

    "oku_şunu": "read",
    "os": "read",

    "çak_yazıyı": "write",
    "cy": "write",

    "kapa_defteri": "close",
    "kdf": "close",

    "yol_baba": "Path",
    "yb": "Path",

    "json_yut": "json.load",
    "jy": "json.load",

    "json_kus": "json.dump",
    "jk": "json.dump",

    # Hata yönetimi
    "dene_bakim": "try",
    "db": "try",

    "yakala_yapıştır": "except",
    "yy": "except",

    "en_sonda_ne_olsa_da": "finally",
    "esd": "finally",

    "fırlat_gitsin": "raise",
    "fg": "raise",

    "emin_ol_bak": "assert",
    "eob": "assert",

    "büyük_patlangaç": "Exception",
    "bp": "Exception",

    # Yerleşik fonksiyonlar ve çeşitli
    "sayı_sallaması": "range",
    "sss": "range",

    "hem_say_hem_geç": "enumerate",
    "hsg": "enumerate",

    "sırala_reis": "sorted",
    "sr": "sorted",

    "topla_gari": "sum",
    "tg": "sum",

    "en_ufak": "min",
    "enf": "min",

    "en_koca": "max",
    "enk": "max",

    "bir_tane_var_mı": "any",
    "btv": "any",

    "hepsi_var_mı": "all",
    "hv": "all",

    "söyle_yav": "print",
    "sy": "print",

    "uyu_biraz": "time.sleep",
    "ub": "time.sleep",

    "sallama_sayi": "random.randint",
    "ss2": "random.randint",

    "dolabı_karıştır": "os.listdir",
    "dk": "os.listdir",

    "şu_an": "datetime.now",
    "şn": "datetime.now",
}

# Hepsini birleştir: önce geyik sözlük, sonra sade Türkçe
TURKISH_KEYWORDS = {}
TURKISH_KEYWORDS.update(REIS_FUN_KEYWORDS)
TURKISH_KEYWORDS.update(BASE_KEYWORDS)


# Hata kodu tanımları
ERROR_DEFINITIONS = {
    "SyntaxError": (
        "REIS_001_SOZDIZIM",
        "Söz dizimi patladı reis"
    ),
    "NameError": (
        "REIS_002_ISIM",
        "İsim hatası reis"
    ),
    "TypeError": (
        "REIS_003_TUR",
        "Tür karmaşası reis"
    ),
    "Default": (
        "REIS_999_BILINMEYEN",
        "Tanımlanamayan patlama reis"
    ),
}


def get_error_info(exc: Exception):
    """
    Hata türüne göre ReisCode hata kodu ve başlık döndürür.
    """
    exc_type_name = type(exc).__name__

    if exc_type_name in ERROR_DEFINITIONS:
        return ERROR_DEFINITIONS[exc_type_name]
    return ERROR_DEFINITIONS["Default"]


def translate_line(line: str) -> str:
    """
    Bir satır içindeki Reisçe veya sade Türkçe anahtar kelimeleri
    Python karşılıklarına çevirir.
    Yorum satırlarının içini bozmaz.
    """

    stripped = line.lstrip()
    if stripped.startswith("#"):
        # Yorum satırı, dokunma, insanın özel alanı
        return line

    translated = line

    # En uzun anahtarları önce çevir (örneğin en_sonda_ne_olsa_da önce)
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


def pretty_traceback(exc: Exception, error_code: str) -> None:
    """
    Hata ayrıntılarını biraz tatlandırıp yazdırır.
    Hata kodunu da başlığa iliştirir.
    """
    tb = traceback.format_exc()
    print(HEADER_LINE)
    print(f"Teknik detaylar (mühendis modu, {error_code}):")
    print(tb)
    print(HEADER_LINE)


def run_python_code(py_code: str, filename: str = "<reiscode>") -> None:
    """
    Çevrilmiş Python kodunu çalıştırır.
    Hata olursa Türkçe, geyik dolu ve kodlu bir çıktı verir.
    """
    try:
        compiled = compile(py_code, filename, "exec")
        exec_globals = {}
        exec(compiled, exec_globals, exec_globals)

    except SyntaxError as exc:
        error_code, title = get_error_info(exc)
        print("")
        print(f"💥 {title}")
        print("Kod biraz fazla özgür takılmış olabilir.")
        print("")
        print(f"Hata Kodu   : {error_code}")
        print(f"Dosya       : {exc.filename}")
        print(f"Satır       : {exc.lineno}")
        print(f"Problemli   : {exc.text.strip() if exc.text else 'yok gibi görünüyor'}")
        print(f"Açıklama    : {exc.msg}")
        pretty_traceback(exc, error_code)
        print("")
        print("Reis işin içinden çıkamadıysa bir bildiği vardır.")
        print(HEADER_LINE)

    except NameError as exc:
        error_code, title = get_error_info(exc)
        print("")
        print(f"🤦 {title}")
        print("Bir şeyi çağırıyorsun ama hiç tanıtmamışsın. Önce tanım, sonra çağrı.")
        print("")
        print(f"Hata Kodu   : {error_code}")
        print(f"Mesaj       : {exc}")
        pretty_traceback(exc, error_code)
        print("")
        print("Reis işin içinden çıkamadıysa bir bildiği vardır.")
        print(HEADER_LINE)

    except TypeError as exc:
        error_code, title = get_error_info(exc)
        print("")
        print(f"🧩 {title}")
        print("Bazı türler birbirini istememiş olabilir. Sayı ile metni evlendirmeye çalışma mesela.")
        print("")
        print(f"Hata Kodu   : {error_code}")
        print(f"Mesaj       : {exc}")
        pretty_traceback(exc, error_code)
        print("")
        print("Reis işin içinden çıkamadıysa bir bildiği vardır.")
        print(HEADER_LINE)

    except Exception as exc:
        error_code, title = get_error_info(exc)
        print("")
        print(f"🔥 ReisCode Panik Merkezi: {title}")
        print("Abi nolur dikkat et ya, tanımlayamadığımız bir patlama oldu.")
        print("")
        print(f"Hata Kodu   : {error_code}")
        print(f"Hata türü   : {type(exc).__name__}")
        print(f"Mesaj       : {exc}")
        pretty_traceback(exc, error_code)
        print("")
        print("Reis işin içinden çıkamadıysa bir bildiği vardır.")
        print(HEADER_LINE)


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

    print("Çevrilmiş Python kodu aşağıdadır:\n")
    print(py_code)
    print("\n" + HEADER_LINE)
    print("Şimdi bu kodu çalıştırıyoruz. Olur da patlarsa, hata kodu ile hatırlarız.\n")

    run_python_code(py_code, filename=str(path))


def repl() -> None:
    """
    Etkileşimli ReisCode geyik modu.
    Kullanıcıya satır satır Reisçe veya sade Türkçe komut yazdırır ve çalıştırır.
    """

    print(HEADER_LINE)
    print("ReisCode Etkileşimli Geyik Modu")
    print("Boş satır ile bloğu çalıştır, Ctrl+C ile çıkabilirsin.")
    print("")
    print("Mini örnekler:")
    print("    tarif_et selam(isim):")
    print("        yani isim == 'reis':")
    print("            söyle_yav('Hoş geldin büyük reis')")
    print("        olmadı:")
    print("            söyle_yav('Hoş geldin', isim)")
    print("")
    print("    selam('reis')")
    print("")
    print("ya da klasik:")
    print("    tanım selam(isim):")
    print("        eğer isim == 'reis':")
    print("            yaz('Hoş geldin büyük reis')")
    print("        değilse:")
    print("            yaz('Hoş geldin', isim)")
    print(HEADER_LINE)

    buffer = []
    while True:
        try:
            line = input("reis_konsol> ")

        except KeyboardInterrupt:
            print("\nTam zamanında çıktın reis, görüşürüz 👋")
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
