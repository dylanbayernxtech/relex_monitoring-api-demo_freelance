$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
$py = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) { $py = "C:\Users\Dylan Kane\.venvs\relex-ds\Scripts\python.exe" }
Set-Location $Root
& $py warmup.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $py arena\interview_warmachine\run_all.py
exit $LASTEXITCODE
