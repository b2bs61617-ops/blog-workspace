$ErrorActionPreference = "Continue"
$repo = Split-Path -Parent $PSScriptRoot
$reportsDir = Join-Path $repo "tools\koikeyz-monitor\monitor_reports"

if (Test-Path $reportsDir) {
    $pending = Get-ChildItem $reportsDir -Filter "report_*.json" -File
    if ($pending.Count -gt 0) {
        $names = ($pending | ForEach-Object { $_.Name }) -join ", "
        $ctx = "KO1KEYZ監視スクリプトの未処理レポートが $($pending.Count) 件あるワン(" + $names + ")。tools/koikeyz-monitor/monitor_reports/ 配下で、同名の .summary.txt ファイルがあればそちら(Geminiによる要約済み)を優先して読み、無ければ .json (生データ、ノイズ除外・重複統合済み)を読んでワン。記事に使えそうな新情報だけ抽出し、ユーザーに「この情報をこの記事に反映する」形で報告してワン。報告し終えたら、該当する .json と .summary.txt を両方 tools/koikeyz-monitor/monitor_reports/processed/ に移動してワン。"
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
