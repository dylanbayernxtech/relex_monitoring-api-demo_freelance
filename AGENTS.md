# Agents — RELEX interview beast mode

You are helping Dylan Kane prep / execute a **RELEX Solutions (Finland)** data-science Python interview task.

## Repo layout
- Demo root: monitoring API demo (file_events / job_events)
- Explorative pack: `kane_relex_explorative_work/` on branch `kane_relex_explorative_work`
- Arena drills: `kane_relex_explorative_work/arena/*` (13 packs)
- Company brief: `kane_relex_explorative_work/COMPANY-BRIEF.md` + `TALKING-POINTS.md`

## Defaults
- Interpreter: `kane_relex_explorative_work/.venv/Scripts/python.exe`
- Prefer **PowerShell** terminals (not Git Bash) to avoid auth/shell-integration relaunch loops
- Metrics: WMAPE + bias over RMSE-only; SKU-location thinking; promo/inventory constraints
- Do not invent customer KPIs; keep synthetic data reproducible

## Warmup
```powershell
cd kane_relex_explorative_work
.\.venv\Scripts\Activate.ps1
python warmup.py
python arena\interview_warmachine\run_all.py
```
