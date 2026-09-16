# Interview desk — locked setup

## PRIMARY (fullscreen for live audience)
**VS Code Insiders** — open this folder only:

\C:\\Users\\Dylan Kane\\relex_recbktrees_freelance\\relex_monitoring-api-demo_freelance.worktrees\\kane-relex-explorative-work
Why: clean editor + terminal; Copilot/Agents available but not the main stage; audience sees *you* coding.

Layout: editor 70% | terminal 30%. One \.py\ file. No Agents window fullscreen during live share.

Interpreter: \C:\\Users\\Dylan Kane\\.venvs\\relex-ds\\Scripts\\python.exe\ (workspace already points here).

Morning smoke (30s):
\\powershell
cd "...\\kane_relex_explorative_work"
.\\run_arena.ps1
\
## FALLBACK A — Insiders Agents panel (same window, side chat)
Use when you want agent help without switching apps. Keep it docked, not fullscreen.
Model order if the UI offers picks: strongest available first (Opus / GPT-class), then **Kimi** if tokens dry up.

## FALLBACK B — Grok Bot teammates (this chat ecosystem)
Use when Insiders Copilot hits limits. See \AGENT-FALLBACK.md\.
Cascade: primary Grok/xPathfinderLabs → RELEX DS Primary → RELEX DS Kimi Fallback.

## NOT installed on this PC
Standalone **Cursor IDE** was not found under Program Files / Local\\Programs. Do not hunt for it mid-interview. Use Insiders + Grok Bot instead.

## Notebook policy
Kernel registered: **Python (relex-ds)**. Use only if they require \.ipynb\. Default deliverable = \.py\ (see DELIVERABLE-STYLE.md + FINLAND-BAR.md).
