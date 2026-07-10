$ErrorActionPreference = "Continue"
$repo = Split-Path -Parent $PSScriptRoot
$reportsDir = Join-Path $repo "tools\koikeyz-monitor\monitor_reports"

if (Test-Path $reportsDir) {
    $pending = Get-ChildItem $reportsDir -Filter "report_*.json" -File
    if ($pending.Count -gt 0) {
        $names = ($pending | ForEach-Object { $_.Name }) -join ", "
        $ctx = "KO1KEYZ監視スクリプトの未処理レポートが $($pending.Count) 件あるワン(" + $names + ")。.claude/skills/koikeyz-rewrite/SKILL.md の「監視レポート由来の新着情報の自動反映」セクションに従い、ユーザーの確認を待たず自動でリサーチ→対象記事の特定→WordPress記事の更新まで実行してワン(1記事ずつのOK待ちは不要、2026-07-09にユーザーが指示)。対象記事が見つからない情報や信頼性が低い情報だけチャットで報告にとどめてワン。完了後は必ずチャット報告とLINE通知を行い、該当する .json と .summary.txt を tools/koikeyz-monitor/monitor_reports/processed/ に移動してワン。"
        $obj = @{
            hookSpecificOutput = @{
                hookEventName = "SessionStart"
                additionalContext = $ctx
            }
        }
        $out = $obj | ConvertTo-Json -Compress -Depth 5
        [Console]::Out.Write($out)
    }
}
