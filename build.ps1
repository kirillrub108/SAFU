# PowerShell script for building and managing the project
# UTF-8 with BOM encoding

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Available commands:"
    Write-Host "  .\build.ps1 build    - Build Docker images"
    Write-Host "  .\build.ps1 up       - Start all services"
    Write-Host "  .\build.ps1 down     - Stop all services"
    Write-Host "  .\build.ps1 migrate  - Run database migrations"
    Write-Host "  .\build.ps1 seed     - Seed database with test data"
    Write-Host "  .\build.ps1 test     - Run tests"
    Write-Host "  .\build.ps1 fmt      - Format code (black, isort)"
    Write-Host "  .\build.ps1 lint    - Lint code"
    Write-Host "  .\build.ps1 logs     - Show logs"
    Write-Host "  .\build.ps1 clean   - Remove containers and volumes"
}

switch ($Command) {
    "build" {
        Write-Host "Building Docker images..."
        docker compose build
    }
    "up" {
        Write-Host "Starting services..."
        docker compose up -d
    }
    "down" {
        Write-Host "Stopping services..."
        docker compose down
    }
    "migrate" {
        Write-Host "Running migrations..."
        docker compose exec backend alembic upgrade head
    }
    "seed" {
        Write-Host "Seeding database..."
        docker compose exec backend python -m app.seeds.main
    }
    "test" {
        Write-Host "Running tests..."
        docker compose exec backend pytest -v
    }
    "fmt" {
        Write-Host "Formatting code..."
        docker compose exec backend black app tests
        docker compose exec backend isort app tests
    }
    "lint" {
        Write-Host "Linting code..."
        docker compose exec backend black --check app tests
        docker compose exec backend isort --check app tests
        docker compose exec backend flake8 app tests
    }
    "logs" {
        docker compose logs -f
    }
    "clean" {
        Write-Host "Removing containers and volumes..."
        docker compose down -v
        docker system prune -f
    }
    default {
        Show-Help
    }
}
