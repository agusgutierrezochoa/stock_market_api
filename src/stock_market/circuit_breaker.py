import circuitbreaker
import requests


class VantageCircuitBreaker(circuitbreaker.CircuitBreaker):
    FAILURE_THRESHOLD = 5
    RECOVERY_TIMEOUT = 60
    EXPECTED_EXCEPTION = requests.RequestException
