# PowerShell Script: reset_venv.ps1
# 🔁 Nukes + recreates virtual environment from requirements.txt

$venvPath = "myenv"
$requirementsPath = "requirements.txt"

Write-Host "🧹 Cleaning up old virtual environment: $venvPath"
if (Test-Path $venvPath) {
    Remove-Item -Recurse -Force $venvPath
}

Write-Host "🚀 Creating new virtual environment..."
python -m venv $venvPath

Write-Host "✅ Activating new virtual environment..."
& "$venvPath\Scripts\activate.ps1"

Write-Host "📦 Upgrading pip..."
pip install --upgrade pip

if (Test-Path $requirementsPath) {
    Write-Host "📥 Installing from $requirementsPath..."
    pip install -r $requirementsPath
} else {
    Write-Host "⚠️ requirements.txt not found. Skipping dependency install."
}

Write-Host "`n✅ Done. Venv rebuilt and ready!"
