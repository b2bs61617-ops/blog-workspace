# Register the 24h-marathon location tracker as a scheduled task that runs
# every 10 minutes. Run from an elevated PowerShell if possible.
#
# The active window is controlled by config.json (active_from / active_until),
# so even if you forget to remove this task after the broadcast, each run just
# exits immediately. Still, Unregister it when done to stop the churn.
#
# NOTE: this file is ASCII-only on purpose. Windows PowerShell 5.1 reads a
# BOM-less .ps1 as the system ANSI codepage (cp932 here); non-ASCII text would
# be mis-decoded and break parsing.

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path "$PSScriptRoot\..\..").Path
$bat  = Join-Path $PSScriptRoot "run.bat"
$taskName = "MarathonTracker_HoshinoMari"

# Go through run.bat so PYTHONUTF8=1 is set and Python is called by full path.
$action  = New-ScheduledTaskAction -Execute "cmd.exe" `
    -Argument "/c `"$bat`"" -WorkingDirectory $repo

# Every 10 minutes, starting now, for 2 days.
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Minutes 10) `
    -RepetitionDuration (New-TimeSpan -Days 2)

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
    -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 9)
# One run = yt-dlp chat capture (~25s) + Gemini extract, measured ~35-90s.
# Comfortably inside the 10-minute gap.

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
    -Settings $settings -Description "24h-TV Hoshino Mari marathon: auto-append current location to post 12158" -Force

Write-Host "Registered: $taskName (every 10 min)"
Write-Host "To remove: Unregister-ScheduledTask -TaskName $taskName -Confirm:`$false"
