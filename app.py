import random
import time


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def fetch_user(user_id: int) -> dict:
    """Simulates a database call with occasional latency."""
    time.sleep(0.01)
    if user_id <= 0:
        raise ValueError("Invalid user ID")
    return {"id": user_id, "name": f"User {user_id}", "active": True}


def process_payment(amount: float) -> dict:
    """Simulates a payment gateway call."""
    if amount <= 0:
        raise ValueError("Amount must be positive")
    return {"status": "success", "amount": amount, "transaction_id": f"TXN{random.randint(1000, 9999)}"}


def get_api_data(endpoint: str) -> dict:
    """Simulates an external API call."""
    if not endpoint:
        raise ValueError("Endpoint cannot be empty")
    return {"endpoint": endpoint, "data": {"status": "ok"}, "latency_ms": random.randint(10, 100)}
