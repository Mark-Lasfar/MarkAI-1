# scripts/start_production.sh
#!/bin/bash
docker-compose -f infrastructure/docker-compose.prod.yml up --build -d