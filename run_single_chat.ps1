param([string]$Question)

$body = @{ message = $Question } | ConvertTo-Json
try {
    $r = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/chat' -Method Post -ContentType 'application/json' -Body $body -TimeoutSec 60
    $r | ConvertTo-Json -Depth 5
} catch {
    if ($_.Exception.Response -ne $null) { Write-Host "STATUS: $($_.Exception.Response.StatusCode)" -ForegroundColor Red }
    Write-Host $_.Exception.Message
}
