$ErrorActionPreference = "Continue"
$repo = Split-Path -Parent $PSScriptRoot
$reportsDir = Join-Path $repo "tools\koikeyz-monitor\monitor_reports"

if (Test-Path $reportsDir) {
    $pending = Get-ChildItem $reportsDir -Filter "report_*.json" -File
    if ($pending.Count -gt 0) {
        $names = ($pending | ForEach-Object { $_.Name }) -join ", "
        $ctx = "KO1KEYZ監視スクリプトの未処理レポートが $($pending.Count) 件あるワン(" + $names + ")。tools/koikeyz-monitor/monitor_reports/ 配下のこれらのファイルを読んで、記事に使えそうな新情報(トレカ交換等のノイズは除外)だけ抽出し、ユーザーに「この情報をこの記事に反映する」形で報告してワン。報告し終えたら、該当レポートファイルを tools/koikeyz-monitor/monitor_reports/processed/ に移動してワン。"
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
