# Register "NetaWatch" in Task Scheduler (runs neta_watch.py --auto every hour). Run once per PC.
# Remove: Unregister-ScheduledTask -TaskName NetaWatch -Confirm:$false
# (Keep this file ASCII only: Windows PowerShell 5.1 misreads UTF-8 without BOM.)
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$pyw = Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\pythonw.exe"
if (-not (Test-Path $pyw)) { $pyw = (Get-Command pythonw).Source }
$script = Join-Path $repo "tools\neta_watch\neta_watch.py"

$action = New-ScheduledTaskAction -Execute $pyw -Argument "`"$script`" --auto" -WorkingDirectory $repo
$start = (Get-Date).Date.AddHours((Get-Date).Hour + 1)
$trigger = New-ScheduledTaskTrigger -Once -At $start -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 55) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "NetaWatch" -Action $action -Trigger $trigger -Settings $settings `
    -Description "neta_watch: official YouTube/SNS -> Gemini -> LINE at 8:00/20:00" -Force | Out-Null
Get-ScheduledTask -TaskName "NetaWatch" | Get-ScheduledTaskInfo | Select-Object TaskName, NextRunTime
