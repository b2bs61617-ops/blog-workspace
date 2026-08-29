# 24時間マラソン現在地トラッカーを「10分おき」でタスクスケジューラに登録する。
# 管理者権限の PowerShell で実行推奨。
# 稼働時間帯は config.json の active_from / active_until で制御しているので、
# マラソン終了後にこのタスクを消し忘れても記事は更新されない(各回が即終了する)。
# ただし無駄に走り続けるので、終わったら Unregister するのが望ましい。

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path "$PSScriptRoot\..\..").Path
$py   = (Get-Command python).Source
$taskName = "MarathonTracker_HoshinoMari"

$action  = New-ScheduledTaskAction -Execute $py `
    -Argument "tools\marathon-tracker\tracker.py" -WorkingDirectory $repo

# 10分おき、今日から明日いっぱいまで
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Minutes 10) `
    -RepetitionDuration (New-TimeSpan -Days 2)

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
    -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 9)
# 注: claude -p の抽出は初回コールドスタートで 2〜3 分かかることがある(実測 ~140s)。
#     10分間隔なら次回実行に食い込まない範囲。遅ければ config.json の llm_primary を "gemini" に。

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
    -Settings $settings -Description "24時間テレビ 星野真里マラソンの現在地を記事12158へ自動追記" -Force

Write-Host "登録完了: $taskName (10分おき)"
Write-Host "解除するには: Unregister-ScheduledTask -TaskName $taskName -Confirm:`$false"
