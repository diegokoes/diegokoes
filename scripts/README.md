# SCRIPTS FOR MY README.MD
None of the commits are reflected in my commit history, they are done via automated actions and explicitly configured so that it doesn't clutter my commit history/activity.
## WakaTime Spanish Sync

This repository uses the official `anmol098/waka-readme-stats` action to inject the stats (between `<!--START_SECTION:waka-->` / `<!--END_SECTION:waka-->`) into `README.md` in English. A custom Python helper, `scripts/sync_waka_spanish.py`, then mirrors and translates that block into the Spanish file `README_es.md` using a second marker pair `<!--START_SECTION:waka_es-->` / `<!--END_SECTION:waka_es-->`.

This has been my way of doing it, feel free to grab it and use it in your repo if you like it.
