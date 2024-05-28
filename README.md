docker-compose run web alembic revision --autogenerate -m "Initial migration"
docker-compose run web alembic upgrade head

curl -X POST "http://localhost:8080/api/users/" -H "Content-Type: application/json" -d \
    '{
        "email": "testuser@example.com",
        "first_name": "agus",
        "last_name": "gutierrez"
    }' | jq



curl -X GET "http://localhost:8080/api/stock/info/?symbol=META" -H "STOCK-INFO-API-Key: 71c2f484-beba-493d-ae8c-8517948b0738" | jq

curl -X GET "http://localhost:8080/api/stock/info/?symbol=META&function=TIME_SERIES_DAILY_ADJUSTED" -H "STOCK-INFO-API-Key: 71c2f484-beba-493d-ae8c-8517948b0738" | jq

curl -XGET "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=META&outputsize=compact&apikey=X86NOH6II01P7R24" | jq