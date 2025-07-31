# Download URL for Python 3.13.5
$pythonUrl = "https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe"
$installerPath = "$env:TEMP\python-3.13.5-installer.exe"
$targetPath = "C:\Users\BRISTOL\AppData\Local\Programs\Python\Python313"

Write-Host "Downloading Python 3.13.5..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath

Write-Host "Installing Python 3.13.5..." -ForegroundColor Yellow
Start-Process -FilePath $installerPath -ArgumentList @(
    "/quiet"
    "InstallAllUsers=0"
    "PrependPath=1"
    "Include_test=0"
    "Include_pip=1"
    "Include_doc=0"
    "DefaultAllUsersTargetDir=$targetPath"
) -Wait

Write-Host "Installation complete!" -ForegroundColor Green
Remove-Item $installerPath