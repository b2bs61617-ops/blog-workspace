$ErrorActionPreference = "Continue"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

$output = git pull 2>&1
$exitCode = $LASTEXITCODE

function Escape-Json($s) {
    return ($s -replace '\\','\\\\' -replace '"','\"' -replace "`r`n"," " -replace "`n"," ")
}

if ($exitCode -ne 0) {
    $joined = Escape-Json(($output | Out-String).Trim())
    Write-Output ('{"systemMessage":"git pull に失敗したワン。手動で確認してほしいワン: ' + $joined + '"}')
} elseif (($output | Out-String) -notmatch "Already up to date") {
    Write-Output '{"systemMessage":"blog-workspaceを最新に更新したワン(git pull完了)"}'
}
