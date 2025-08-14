# WakaTime Multi-language README Workaround

**Problem:**  
The [anmol098/waka-readme-stats](https://github.com/anmol098/waka-readme-stats) action (as of v4) only updates a single file (`README.md`). It supports a `SECTION_NAME` input—but this is only for customizing the marker in that file. There’s no `FILE_PATH` input in the stable version.

**Goal:**  
Show WakaTime stats in both English (`README.md`) and Spanish (`README_es.md`).

**Solution:**  
- Run the Waka Readme action as normal; it writes to `README.md`.
- After it completes, a workflow triggers a Python script (`scripts/sync_waka_spanish.py`).
- The script:
  - Extracts the Waka section from `README.md`.
  - Translates known phrases into Spanish (I took them from the contributor that added them into the project).
  - Updates the Waka section (using custom markers) in `README_es.md`.
  - Only commits if there’s a real change.

**Why:**  
There’s no native way to update multiple files or localize the output using the official action. This workflow automates copying, translating, and syncing the stats block to the Spanish README.
