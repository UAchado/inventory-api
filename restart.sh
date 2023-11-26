docker compose down -v
docker image rm mysql
docker image rm inventory-api-inventory-api
docker system prune --force
docker compose up  --build