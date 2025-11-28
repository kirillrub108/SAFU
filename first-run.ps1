# First run script - запуск проекта с нуля

Write-Host "=== SAFU Timetable - First Run ===" -ForegroundColor Green
Write-Host ""

Write-Host "1. Building Docker images..." -ForegroundColor Yellow
docker compose build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "2. Starting services..." -ForegroundColor Yellow
docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to start services!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "3. Waiting for database to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "4. Running database migrations..." -ForegroundColor Yellow
docker compose exec backend alembic upgrade head
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Migrations may have failed. Check logs." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "5. Seeding database with test data..." -ForegroundColor Yellow
docker compose exec backend python -m app.seeds.main
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Seeding may have failed. Check logs." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Done! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Open in browser:" -ForegroundColor Cyan
Write-Host "  Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Check status: docker compose ps" -ForegroundColor Gray
Write-Host "View logs:    docker compose logs -f" -ForegroundColor Gray
