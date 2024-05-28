# README

Hi! This repo was made to solve an euerka challenge

What's about? Is a simple API to call an external service to retrieve stock information, with a basic auth system.

This project requires docker installed.

## Setting up

Initially, we'll need to start the docker instances:

```
cd stock_market_api
docker compose up --build
```

There, we'll have the running instances. Now, we have to run the migrations:

```
docker exec -it stock_market_api_service bash
# app/ cd src
# app/src/ alembic upgrade head 
```

## Running

Now, with the migrations made we need to create a first user:

```
curl -X POST "http://localhost:8080/api/users/" -H "Content-Type: application/json" -d \
    '{
        "email": "testuser@example.com",
        "first_name": "agus",
        "last_name": "gutierrez"
    }' | jq
```

In the answer we'll have:

```
{
    "id": 1,
    "first_name": "agus",
    "last_name": "gutierrez",
    "api_key": "SOME_API_KEY"
}
```

There, we can call the stock API:

```
curl -X GET "http://localhost:8080/api/stock/info/?symbol=META" -H "STOCK-INFO-API-Key: SOME_API_KEY" | jq
```

## Api Throttling

We've implemented API Throttling in our two endpoints. You can not perform more than 1 request per minute.

## External API calls

There is an external API call (to vantage). This call is wrapped by a circuit breaker, so be carefull: if the external api call is down, the circuit breaker can open.

## Doc

To check the API doc, go to your browser to the following url:

```
http://localhost:8080/doc/
```

## Testing

There are two ways to run tests:

```
docker compose up --build test
```

or

```
docker exec -it stock_market_api_service bash
# app/pytest
...
```

## Contributing

This repo has implemented CI, so all the tests must pass before merging a PR.
