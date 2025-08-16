#!/usr/bin/env python3
import re
from pathlib import Path

# Markers
EN_START = "<!--START_SECTION:waka-->"
EN_END = "<!--END_SECTION:waka-->"
ES_START = "<!--START_SECTION:waka_es-->"
ES_END = "<!--END_SECTION:waka_es-->"

readme_en_path = Path("README.md")
readme_es_path = Path("README_es.md")


def extract_waka_section(md: str):
    m = re.search(rf"{re.escape(EN_START)}(.*?){re.escape(EN_END)}", md, re.DOTALL)
    return m.group(1) if m else None


def translate_heading_most_productive(text: str) -> str:
    day_map = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }

    def repl(m: re.Match) -> str:
        day_en = m.group(1)
        day_es = day_map.get(day_en, day_en)
        return f"📅 Soy más productivo los {day_es}"

    # Handle variations: with/without emoji, caps, optional punctuation
    patterns = [
        r"📅\s*I'?m Most Productive on\s+([A-Za-z]+)",
        r"I'?m Most Productive on\s+([A-Za-z]+)",
    ]
    out = text
    for pat in patterns:
        out = re.sub(pat, repl, out, flags=re.IGNORECASE)
    return out


def translate_simple_phrases(text: str) -> str:
    """
      !TODO documentar el script 
    """

    out = text

    out = re.sub(
        r"(\*{1,2})\s*I'?m an? Early (?:Bird )?🐤\s*(\*{1,2})",
        r"\1Soy diurno 🐤\2",
        out,
        flags=re.IGNORECASE,
    )
    out = re.sub(
        r"(\*{1,2})\s*I'?m a Night(?: Owl)? 🦉\s*(\*{1,2})",
        r"\1Soy nocturno 🦉\2",
        out,
        flags=re.IGNORECASE,
    )

    out = re.sub(
        r"(📊\s*)(\*{0,2})\s*This Week I Spent My Time On\s*(\*{0,2})",
        r"\1\2Mi actividad semanala\3",
        out,
        flags=re.IGNORECASE,
    )
    out = re.sub(
        r"(^|\n)(\*{0,2})\s*This Week I Spent My Time On\s*(\*{0,2})",
        r"\1\2Esta semana me dediqué a\3",
        out,
        flags=re.IGNORECASE,
    )

    colon_map = [
        (r"(💬\s*)(\*{0,2})\s*Programming Languages\s*:(\s*)", r"\1\2Lenguajes:\3"),
        (r"(💬\s*)(\*{0,2})\s*Languages\s*:(\s*)", r"\1\2Lenguajes:\3"),
        (r"(^|\n)(\*{0,2})\s*Programming Languages\s*:(\s*)", r"\1\2Lenguajes:\3"),
        (r"(^|\n)(\*{0,2})\s*Languages\s*:(\s*)", r"\1\2Lenguajes:\3"),
        
        (r"(🔥\s*)(\*{0,2})\s*Editors\s*:(\s*)", r"\1\2Editores:\3"),
        (r"(^|\n)(\*{0,2})\s*Editors\s*:(\s*)", r"\1\2Editores:\3"),
        
        (r"(🐱‍💻\s*)(\*{0,2})\s*Projects\s*:(\s*)", r"\1\2Proyectos:\3"),
        (r"(^|\n)(\*{0,2})\s*Projects\s*:(\s*)", r"\1\2Proyectos:\3"),
        
        (r"(💻\s*)(\*{0,2})\s*Operating Systems?\s*:(\s*)", r"\1\2Sistemas Operativos:\3"),
        (r"(💻\s*)(\*{0,2})\s*Operating System\s*:(\s*)", r"\1\2Sistema Operativo:\3"),
        (r"(^|\n)(\*{0,2})\s*Operating Systems?\s*:(\s*)", r"\1\2Sistemas Operativos:\3"),
        (r"(^|\n)(\*{0,2})\s*Operating System\s*:(\s*)", r"\1\2Sistema Operativo:\3"),
        
        (r"(⌚︎?\s*)(\*{0,2})\s*Time\s*Zone\s*:(\s*)", r"\1\2Zona Horaria:\3"),
        
        (r"(^|\n)(\*{0,2})\s*Code Time\s*(\*{0,2})", r"\1\2Tiempo de código\3"),
        (r"(^|\n)(\*{0,2})\s*Profile Views\s*(\*{0,2})", r"\1\2Vistas de perfil\3"),
        (r"(^|\n)(\*{0,2})\s*Total Time\s*(\*{0,2})", r"\1\2Tiempo total\3"),
    ]
    for pat, repl in colon_map:
        out = re.sub(pat, repl, out, flags=re.IGNORECASE)

    out = re.sub(r"Last Updated on", "Última actualización el", out, flags=re.IGNORECASE)

    out = re.sub(
        r"No Activity Tracked This Week", "Sin actividad registrada esta semana", out, flags=re.IGNORECASE
    )
    out = re.sub(
        r"No activity tracked this week", "Sin actividad registrada esta semana", out, flags=re.IGNORECASE
    )
    out = re.sub(
        r"No Activity Tracked Today", "Sin actividad registrada hoy", out, flags=re.IGNORECASE
    )

    out = re.sub(r"Unknown Project", "Proyecto desconocido", out, flags=re.IGNORECASE)

    out = re.sub(
        r"(\*{0,2})\s*I Mostly Code in\s+([^\*\n]+)\s*(\*{0,2})",
        r"\1Programo principalmente en \2\3",
        out,
        flags=re.IGNORECASE,
    )

    return out


def translate_inline_words(text: str) -> str:
    word_map = {
        "Morning": "Mañana",
        "Daytime": "Día",
        "Day": "Día",
        "Evening": "Tarde",
        "Night": "Noche",
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
        "System": "Sistema",
    }
    out = text
    for en, es in word_map.items():
        out = re.sub(rf"\b{re.escape(en)}\b", es, out)
    return out


def translate_waka_block(inner: str) -> str:
    t = inner
    t = translate_heading_most_productive(t)
    t = translate_simple_phrases(t)
    t = translate_inline_words(t)
    return t


def replace_es_section(src_md: str, translated_inner: str) -> str:
    def do_replace(start_marker: str, end_marker: str, content: str, md: str):
        pattern = re.compile(rf"{re.escape(start_marker)}(.*?){re.escape(end_marker)}", re.DOTALL)
        if pattern.search(md):
            return pattern.sub(f"{start_marker}{content}{end_marker}", md), True
        return md, False

    new_md, changed = do_replace(ES_START, ES_END, translated_inner, src_md)
    if changed:
        return new_md

    new_md, changed = do_replace(EN_START, EN_END, translated_inner, src_md)
    if changed:
        return new_md

    suffix = f"\n\n{ES_START}{translated_inner}{ES_END}\n"
    return src_md + suffix


def main() -> int:
    if not readme_en_path.exists():
        print("README.md not found; aborting.")
        return 1
    if not readme_es_path.exists():
        print("README_es.md not found; aborting.")
        return 1

    en_md = readme_en_path.read_text(encoding="utf-8")
    es_md = readme_es_path.read_text(encoding="utf-8")

    inner = extract_waka_section(en_md)
    if inner is None:
        print("No Waka section found in README.md; nothing to sync.")
        return 0

    inner = "\n" + inner.strip("\n") + "\n"

    translated = translate_waka_block(inner)
    updated_es = replace_es_section(es_md, translated)

    if updated_es != es_md:
        readme_es_path.write_text(updated_es, encoding="utf-8", newline="\n")
        print("README_es.md updated.")
    else:
        print("README_es.md already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
