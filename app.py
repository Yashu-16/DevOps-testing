"""Simple Python application with arithmetic and API simulation functions."""

import random
import time
from typing import Dict, Union


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Add two numbers."""
    return a + b


def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Subtract second number from first."""
    return a - b


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Multiply two numbers."""
    return a * b


def divide(a: Union[int, float], b: Union[int, float]) -> float:
    """Divide first number by second.
    
    Args:
        a: Dividend
        b: Divisor
        
    Returns:
        Result of division
        
    Raises:
        ValueError: If divisor is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def fetch_user(user_id: int) -> Dict[str, Union[int, str, bool]]:
    """Simulate a database call with occasional latency.
    
    Args:
        user_id: ID of user to fetch
        
    Returns:
        User dictionary with id, name, and active status
        
    Raises:
        ValueError: If user_id is invalid
    """
    time.sleep(0.01)
    if user_id <= 0:
        raise ValueError("Invalid user ID")
    return {
        "id": user_id,
        "name": f"User {user_id}",
        "active": True
    }


def process_payment(amount: float) -> Dict[str, Union[str, float]]:
    """Simulate a payment gateway call.
    
    Args:
        amount: Payment amount
        
    Returns:
        Payment result dictionary
        
    Raises:
        ValueError: If amount is not positive
    """
    if amount <= 0:
        raise ValueError("Amount must be positive")
    
    transaction_id = f"TXN{random.randint(1000, 9999)}"
    return {
        "status": "success",
        "amount": amount,
        "transaction_id": transaction_id
    }


def get_api_data(endpoint: str) -> Dict[str, Union[str, Dict, int]]:
    """Simulate an external API call.
    
    Args:
        endpoint: API endpoint to call
        
    Returns:
        API response dictionary
        
    Raises:
        ValueError: If endpoint is empty
    """
    if not endpoint:
        raise ValueError("Endpoint cannot be empty")
    
    return {
        "endpoint": endpoint,
        "data": {"status": "ok"},
        "latency_ms": random.randint(10, 100)
    }
