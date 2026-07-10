$ErrorActionPreference = "Continue"
$raw = [Console]::In.ReadToEnd()

try {
    $data = $raw | ConvertFrom-Json
} catch {
    Write-Output ""
    exit 0
}

$session = $data.rate_limits.five_hour.used_percentage
$week = $data.rate_limits.seven_day.used_percentage

$parts = @()

if ($null -ne $session) {
    $mark = if ($session -ge 70) { "⚠" } else { "" }
    $parts += "セッション$mark$([math]::Round($session))%"
}
if ($null -ne $week) {
    $mark = if ($week -ge 70) { "⚠" } else { "" }
    $parts += "週間$mark$([math]::Round($week))%"
}

if ($parts.Count -gt 0) {
    Write-Output ($parts -join " / ")
}

