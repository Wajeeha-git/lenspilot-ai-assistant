param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$questions = @(
    "What is LensPilot?",
    "Do I need to install an app?",
    "Do I need to create an account?",
    "Is LensPilot free?",
    "Which browsers are supported?",
    "Does LensPilot store my face?",
    "How do I renew my subscription?",
    "Where is my QR code?",
    "Which AI model does LensPilot use?",
    "Walk me through the full LensPilot workflow.",
    "What happens after a shopkeeper registers?",
    "How does a customer access the try-on without an account?",
    "What can an admin do that a shopkeeper can't?",
    "Can a customer manage the lens catalogue?",
    "What can a shopkeeper see on their dashboard?",
    "Do customers need to log in?",
    "My camera isn't opening, what should I do?",
    "I denied camera permission by accident.",
    "My QR code isn't working.",
    "My subscription expired, what happens?",
    "The lens overlay isn't aligned with my eyes.",
    "What's the monthly subscription price?",
    "Will LensPilot support video calls with an optician soon?",
    "What database do you use internally?",
    "Can I get a refund?",
    "How long do you keep my camera data?"
)

$refusalPhrase = "I'm not certain"
$results = @()

Write-Host "Running $($questions.Count) questions against $BaseUrl/chat ...`n" -ForegroundColor Cyan

foreach ($q in $questions) {
    try {
        $body = @{ message = $q } | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "$BaseUrl/chat" -Method Post -ContentType "application/json" -Body $body -TimeoutSec 30

        $reply = $response.reply
        $topSource = if ($response.sources.Count -gt 0) { $response.sources[0].category } else { "(none)" }
        $refused = $reply -like "*$refusalPhrase*"

        $results += [PSCustomObject]@{
            Question   = $q
            Category   = $topSource
            Refused    = $refused
            ReplyStart = if ($reply.Length -gt 90) { $reply.Substring(0, 90) + "..." } else { $reply }
        }
    }
    catch {
        $results += [PSCustomObject]@{
            Question   = $q
            Category   = "ERROR"
            Refused    = $false
            ReplyStart = $_.Exception.Message
        }
    }
}

Write-Host "=== Results ===`n" -ForegroundColor Cyan
$results | Format-Table -Wrap -AutoSize

Write-Host "`n=== Must-not-do check ===" -ForegroundColor Yellow
Write-Host "Expect 4 of the last 5 to show Refused=True. The 'internal database' question is a deliberate exception -- it SHOULD answer, not refuse.`n"
$results | Select-Object -Last 5 | Format-Table -Wrap -AutoSize

$refusedCount = ($results | Select-Object -Last 5 | Where-Object { $_.Refused }).Count
Write-Host "`n$refusedCount of 5 refusal-expected questions actually refused." -ForegroundColor $(if ($refusedCount -ge 4) { "Green" } else { "Red" })
