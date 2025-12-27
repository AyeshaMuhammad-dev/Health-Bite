# PowerShell script to push Health-Bite to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Health-Bite - Push to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path ".git")) {
    Write-Host "❌ Error: Not in a git repository!" -ForegroundColor Red
    Write-Host "Please run this script from: D:\Health-Bite\health_bite_backend" -ForegroundColor Yellow
    pause
    exit
}

Write-Host "📊 Checking commit status..." -ForegroundColor Yellow
git log --oneline -5

Write-Host ""
Write-Host "📍 Remote repository:" -ForegroundColor Yellow
git remote -v

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ready to push 5 commits to GitHub!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$response = Read-Host "Do you want to push now? (y/n)"

if ($response -eq "y" -or $response -eq "Y") {
    Write-Host ""
    Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⚠️  You may be prompted for credentials:" -ForegroundColor Yellow
    Write-Host "   Username: AyeshaMuhammad-dev" -ForegroundColor Cyan
    Write-Host "   Password: Use Personal Access Token (not your GitHub password!)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   Get token: https://github.com/settings/tokens" -ForegroundColor Cyan
    Write-Host ""
    
    $force = Read-Host "Force push (replace existing commits)? (y/n)"
    
    if ($force -eq "y" -or $force -eq "Y") {
        Write-Host "⚠️  Force pushing (will overwrite existing commits)..." -ForegroundColor Red
        git push -u origin main --force
    } else {
        git push -u origin main
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
        Write-Host "View your repository: https://github.com/AyeshaMuhammad-dev/Health-Bite" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "❌ Push failed. Check authentication or network connection." -ForegroundColor Red
        Write-Host "See PUSH_NOW.md for detailed instructions." -ForegroundColor Yellow
    }
} else {
    Write-Host "Push cancelled." -ForegroundColor Yellow
}

Write-Host ""
pause
