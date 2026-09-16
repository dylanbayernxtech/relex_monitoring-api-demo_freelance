Continue = "Stop"
 = Split-Path -Parent System.Management.Automation.InvocationInfo.MyCommand.Path
utf-8 = "utf-8"
1 = "1"
 = Join-Path  ".venv\Scripts\python.exe"
if (-not (Test-Path )) {  = "C:\Users\Dylan Kane\.venvs\relex-ds\Scripts\python.exe" }
Set-Location 
&  warmup.py
if ( -ne 0) { exit  }
&  arena\interview_warmachine\run_all.py
exit 
