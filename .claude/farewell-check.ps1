$stdinStream = [Console]::OpenStandardInput()
$reader = New-Object System.IO.StreamReader($stdinStream, [System.Text.Encoding]::UTF8)
$stdin = $reader.ReadToEnd()
try {
    $data = $stdin | ConvertFrom-Json
    $prompt = [string]$data.prompt
} catch {
    $prompt = ""
}

$keywords = @("今日はおしまい", "また明日ね", "また明日", "バイバイ", "またね", "お休み", "お疲れ様", "おつかれー")
$matched = $false
foreach ($k in $keywords) {
    if ($prompt -like "*$k*") {
        $matched = $true
        break
    }
}

if ($matched) {
    $ctx = "ユーザーが今日の作業を終える挨拶をしたワン。今日教えた事やスキル、ルールなどをファイル(CLAUDE.mdや.claude/skills/など)にちゃんと書いたか確認してワン！書いていなければ、今日覚えた事を全てファイルに書いてから締めくくってほしいワン！わんこそば！"
    $obj = @{
        hookSpecificOutput = @{
            hookEventName = "UserPromptSubmit"
            additionalContext = $ctx
        }
    }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $out = $obj | ConvertTo-Json -Compress -Depth 5
    [Console]::Out.Write($out)
}