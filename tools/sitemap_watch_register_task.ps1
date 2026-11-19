# Register "SitemapWatch" in Task Scheduler (runs tools/sitemap_watch.py --fix every Monday 9:00). Run once per PC.
# Remove: Unregister-ScheduledTask -TaskName SitemapWatch -Confirm:$false
# (Keep this file ASCII only: Windows PowerShell 5.1 misreads UTF-8 without BOM.)
$repo = Split-Path -Parent $PSScriptRoot
$pyw = Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\pythonw.exe"
if (-not (Test-Path $pyw)) { $pyw = (Get-Command pythonw).Source }
$script = Join-Path $repo "tools\sitemap_watch.py"

$action = New-ScheduledTaskAction -Execute $pyw -Argument "`"$script`" --fix" -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9:00
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "SitemapWatch" -Action $action -Trigger $trigger -Settings $settings `
    -Description "sitemap_watch: Search Console sitemap check -> LINE only when something is wrong" -Force | Out-Null
Get-ScheduledTask -TaskName "SitemapWatch" | Get-ScheduledTaskInfo | Select-Object TaskName, NextRunTime
