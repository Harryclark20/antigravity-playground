# install_apps.ps1
# This script uses the built-in Windows Package Manager (winget) to install the requested applications.

Write-Host "Starting installation of applications..." -ForegroundColor Cyan

# Define the winget package IDs for the requested software
$apps = @(
    "VideoLAN.VLC",
    "Adobe.Acrobat.Reader.64-bit",
    "Mozilla.Firefox",
    "Google.Chrome",
    "Microsoft.Office"
)

foreach ($app in $apps) {
    Write-Host "`nInstalling $app..." -ForegroundColor Cyan
    
    # We use --silent for unattended installation and --accept-source-agreements / --accept-package-agreements to bypass prompts
    winget install --id $app --exact --silent --accept-package-agreements --accept-source-agreements
    
    if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 2316632065) {
        Write-Host "Successfully installed $app (or it was already installed)." -ForegroundColor Green
    } else {
        Write-Host "Finished attempt to install $app. (Exit code: $LASTEXITCODE)" -ForegroundColor Yellow
        Write-Host "If it failed, you may need to run this script as Administrator." -ForegroundColor Yellow
    }
}

Write-Host "`nAll requested installations have been processed!" -ForegroundColor Green
Write-Host "Note: Microsoft Office might require you to sign in with your Office 365 account after installation." -ForegroundColor Yellow
