# Script to create GitHub repository and push code

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Health-Bite - Push to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repoUrl = "https://github.com/AyeshaMuhammad-dev/Health-Bite.git"

Write-Host "Your 5 commits are ready:" -ForegroundColor Green
git log --oneline --date=short --pretty=format:"  %ad | %s" -5

Write-Host ""
Write-Host "⚠️  Repository not found. You have 2 options:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Option 1: Create repository on GitHub first" -ForegroundColor Cyan
Write-Host "   1. Go to: https://github.com/new" -ForegroundColor White
Write-Host "   2. Repository name: Health-Bite" -ForegroundColor White
Write-Host "   3. Choose Private or Public" -ForegroundColor White
Write-Host "   4. DO NOT initialize with README, .gitignore, or license" -ForegroundColor White
Write-Host "   5. Click 'Create repository'" -ForegroundColor White
Write-Host ""
Write-Host "Option 2: Push with GitHub CLI (if installed)" -ForegroundColor Cyan
Write-Host ""

$choice = Read-Host "Have you created the repository on GitHub? (y/n)"

if ($choice -eq "y" -or $choice -eq "Y") {
    Write-Host ""
    Write-Host "🚀 Attempting to push..." -ForegroundColor Yellow
    
    # Try pushing
    Write-Host "Pushing to: $repoUrl" -ForegroundColor Cyan
    git push -u origin main --force
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
        Write-Host "View: https://github.com/AyeshaMuhammad-dev/Health-Bite" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "❌ Push failed. Possible issues:" -ForegroundColor Red
        Write-Host "   1. Repository name doesn't match" -ForegroundColor Yellow
        Write-Host "   2. Repository is private and needs authentication" -ForegroundColor Yellow
        Write-Host "   3. Need Personal Access Token (not password)" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Get token: https://github.com/settings/tokens" -ForegroundColor Cyan
        Write-Host "Then use: git push -u origin main" -ForegroundColor Cyan
    }
} else {
    Write-Host ""
    Write-Host "Please create the repository first, then run this script again." -ForegroundColor Yellow
    Write-Host "Or use GitHub CLI: gh repo create Health-Bite --private --source=. --remote=origin --push" -ForegroundColor Cyan
}

Write-Host ""
pause
