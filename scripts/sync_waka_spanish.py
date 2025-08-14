#!/usr/bin/env python3
import re
from pathlib import Path

EN_START = "<!--START_SECTION:waka-->"
EN_END = "<!--END_SECTION:waka-->"
ES_START = "<!--START_SECTION:waka_es-->"
ES_END = "<!--END_SECTION:waka_es-->"

repo_root = Path(__file__).resolve().parents[1]
readme_en_path = repo_root / "README.md"
readme_es_path = repo_root / "README_es.md"

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
    return re.sub(r"📅\s*I'?m Most Productive on\s+([A-Za-z]+)", repl, text)

def translate_simple_phrases(text: str) -> str:
    replacements = [
        (r"\*\s*I'?m an? Early (?:Bird )?🐤\s*\*", "Soy diurno 🐤"),
        (r"\*\s*I'?m a Night 🦉\s*\*", "Soy nocturno 🦉"),
        (r"\*\*I'?m an? Early (?:Bird )?🐤\*\*", "**Soy diurno 🐤**"),
        (r"\*\*I'?m a Night 🦉\*\*", "**Soy nocturno 🦉**"),

        (r"📊\s*This Week I Spent My Time On", "📊 Esta semana me dediqué a"),
        (r"⌚︎?\s*Time Zone:", "⌚︎ Zona Horaria:"),
        (r"💬\s*Languages:", "💬 Lenguajes:"),
        (r"🔥\s*Editors:", "🔥 Editores:"),
        (r"🐱‍💻\s*Projects:", "🐱‍💻 Proyectos:"),
        (r"💻\s*Operating System:", "💻 Sistema Operativo:"),

        (r"Last Updated on", "Última actualización el"),

        (r"No Activity Tracked This Week", "Sin actividad registrada esta semana"),
        (r"No activity tracked this week", "Sin actividad registrada esta semana"),

        (r"Unknown Project", "Proyecto desconocido"),

        (r"\*\*I Mostly Code in ([^\*]+)\*\*", r"**Codifico principalmente en \1**"),
    ]
    out = text
    for pat, repl in replacements:
        out = re.sub(pat, repl, out, flags=re.IGNORECASE)
    return out

def translate_inline_words(text: str) -> str:
    word_map = {
        "Morning": "Mañana",
        "Day": "Día",
        "Daytime": "Día",
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
