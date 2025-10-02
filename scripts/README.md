---

### WakaTime Spanish Sync

This repository uses the official `anmol098/waka-readme-stats` action to inject the stats (between `<!--START_SECTION:waka-->` / `<!--END_SECTION:waka-->`) into `README.md` in English. A custom Python helper, `scripts/sync_waka_spanish.py`, then mirrors and translates that block into the Spanish file `README_es.md` using a second marker pair `<!--START_SECTION:waka_es-->` / `<!--END_SECTION:waka_es-->`.

Workflow summary:

1. Action updates English stats in `README.md` (default markers).
2. Python script runs after the action finishes.
3. Script extracts the raw inner Waka block from `README.md`.
4. Phrase + heading translations and small inline word replacements are applied (only known, safe tokens are changed; code/text formatting is preserved).
5. A column alignment pass normalizes spacing in the time-of-day distribution table so labels, commit counts, bars, and percentages line up after translation.
6. The translated block replaces (or appends) the Spanish markers in `README_es.md` only if any change is detected—avoiding empty commits.

Feel free to reuse or modify the script for other languages for your repo
