# Update .env model names to Gemini, create launcher, restart uvicorn with logging, re-run failing questions, and tail logs

cd C:\Users\hp\OneDrive\Desktop\lenspilot-ai-assistant\backend

# 1. Fix the stale OpenAI model names in .env
(Get-Content .env) -replace 'EMBEDDING_MODEL=.*', 'EMBEDDING_MODEL=gemini-embedding-001' `
                   -replace 'CHAT_MODEL=.*', 'CHAT_MODEL=gemini-2.5-flash' | Set-Content .env
Get-Content .env | Select-String "EMBEDDING_MODEL|CHAT_MODEL"

# 2. Create a small launcher script that redirects uvicorn's output reliably
@'
cd C:\Users\hp\OneDrive\Desktop\lenspilot-ai-assistant\backend
.\venv\Scripts\python -m uvicorn app.main:app --reload *> $env:TEMP\uvicorn_output.log
'@ | Set-Content start_uvicorn_logged.ps1

# 3. Stop any running server, start fresh with logging
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Start-Process powershell -ArgumentList "-NoExit","-File","$PWD\start_uvicorn_logged.ps1"
Start-Sleep -Seconds 6
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
    Write-Host "health OK" -ForegroundColor Green
} catch {
    Write-Host "health check failed: $_" -ForegroundColor Red
}

# 4. Helper that extracts the REAL error body, not just the status code
function Invoke-ChatQuestion {
    param([string]$Question)
    $body = @{ message = $Question } | ConvertTo-Json
    try {
        $r = Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method Post -ContentType "application/json" -Body $body -TimeoutSec 60
        return ($r | ConvertTo-Json -Depth 5)
    } catch {
        $statusCode = $null
        $errorBody = $null
        if ($_.Exception.Response -ne $null) {
            try { $statusCode = $_.Exception.Response.StatusCode.value__ } catch { $statusCode = $_.Exception.Response.StatusCode }
            try {
                $stream = $_.Exception.Response.GetResponseStream()
                $reader = New-Object System.IO.StreamReader($stream)
                $errorBody = $reader.ReadToEnd()
            } catch {
                $errorBody = $_.Exception.Message
            }
        } else {
            $errorBody = $_.Exception.Message
        }
        return "STATUS: $statusCode`nBODY: $errorBody"
    }
}

# 5. Re-run the two failing questions with real error extraction
foreach ($q in @("What's the monthly subscription price?", "Can I get a refund?")) {
    Write-Host "`n--- $q ---" -ForegroundColor Cyan
    $out = Invoke-ChatQuestion -Question $q
    Write-Host $out
    Start-Sleep -Seconds 3
}

# 6. Show what the server actually logged
Write-Host "`n=== Server log tail ===" -ForegroundColor Yellow
Start-Sleep -Seconds 2
Get-Content -Path "$env:TEMP\uvicorn_output.log" -Tail 120 -ErrorAction SilentlyContinue
