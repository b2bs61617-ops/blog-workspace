# 24時間マラソン現在地トラッカーを「10分おき」でタスクスケジューラに登録する。
# 管理者権限の PowerShell で実行推奨。
# 稼働時間帯は config.json の active_from / active_until で制御しているので、
# マラソン終了後にこのタスクを消し忘れても記事は更新されない(各回が即終了する)。
# ただし無駄に走り続けるので、終わったら Unregister するのが望ましい。

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path "$PSScriptRoot\..\..").Path
$bat  = Join-Path $PSScriptRoot "run.bat"
$taskName = "MarathonTracker_HoshinoMari"

# run.bat 経由(PYTHONUTF8=1 をセットしてから python を呼ぶ)。cp932 環境での文字化け対策。
$action  = New-ScheduledTaskAction -Execute "cmd.exe" `
    -Argument "/c `"$bat`"" -WorkingDirectory $repo

# 10分おき、今日から明日いっぱいまで
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Minutes 10) `
    -RepetitionDuration (New-TimeSpan -Days 2)

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
    -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 9)
# 注: yt-dlp のチャット取得(既定25秒)+ Gemini 抽出で1回あたり実測 40〜90 秒程度。
#     10分間隔なら次回実行に食い込まない。

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
    -Settings $settings -Description "24時間テレビ 星野真里マラソンの現在地を記事12158へ自動追記" -Force

Write-Host "登録完了: $taskName (10分おき)"
Write-Host "解除するには: Unregister-ScheduledTask -TaskName $taskName -Confirm:`$false"
