docker-compose run web alembic revision --autogenerate -m "Initial migration"
docker-compose run web alembic upgrade head

curl -X POST "http://localhost:8080/users/" -H "Content-Type: application/json" -d \
    '{
        "email": "testuser@example.com",
        "first_name": "agus",
        "last_name": "gutierrez"
    }' | jq