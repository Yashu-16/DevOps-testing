import pytest
import random
import time
import os
from app import add, subtract, multiply, divide, fetch_user, process_payment, get_api_data

# ── Stable tests (always pass) ────────────────────────────────────────────

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(10, 4) == 6

def test_multiply(:
    assert multiply(3, 4) == 12

def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

def test_fetch_user_valid():
    user = fetch_user(1)
    assert user["id"] == 1
    assert user["active"] is True

def test_fetch_user_invalid():
    with pytest.raises(ValueError):
        fetch_user(-1)

def test_process_payment_valid():
    result = process_payment(100.0)
    assert result["status"] == "success"
    assert result["amount"] == 100.00

def test_process_payment_invalid():
    with pytest.raises(ValueError):
        process_payment(-50)

def test_get_api_data_valid():
    result = get_api_data("/health")
    assert result["data"]["status"] == "ok"

def test_get_api_data_invalid():
    with pytest.raises(ValueError):
        get_api_data("")


# ── Flaky tests (fail ~30% of the time — simulates real transient failures) ──

def test_flaky_network_call():
    """
    Simulates a test that depends on network timing.
    Fails ~30% of the time — like a real flaky test hitting a slow API.
    This is the kind of failure that self-healing can fix by retrying.
    """
    # Simulate network jitter
    latency = random.uniform(0, 1.0)
    time.sleep(latency * 0.01)  # Don't actually sleep long in CI

    # Use a fixed seed based on current second to make it deterministic per run
    # but different across runs — simulates transient failures
    seed = int(time.time()) % 10
    if seed < 3:  # ~30% of the time (when second ends in 0, 1, or 2)
        pytest.fail(
            "Network timeout: upstream API did not respond within SLA. "
            "This is a transient failure — retry should succeed."
        )

    result = get_api_data("/users")
    assert result["data"]["status"] == "ok"


def test_flaky_database_connection():
    """
    Simulates a test that depends on database availability.
    Fails ~30% of the time — like a real flaky test hitting a busy DB.
    """
    seed = int(time.time() * 1.3) % 10
    if seed < 3:  # ~30% chance
        pytest.fail(
            "Database connection timeout: could not acquire connection from pool. "
            "This is a transient failure — retry should succeed."
        )

    user = fetch_user(42)
    assert user["id"] == 42


def test_flaky_external_service():
    """
    Simulates a test that calls an external payment service.
    Fails ~25% of the time — like a real flaky test hitting a rate limit.
    """
    seed = int(time.time() * 1.7) % 10
    if seed < 2:  # ~20-25% chance
        pytest.fail(
            "Payment gateway rate limit exceeded: 429 Too Many Requests. "
            "This is a transient failure — retry should succeed."
        )

    result = process_payment(50.0)
    assert result["status"] == "success"


def test_flaky_cache_miss():
    """
    Simulates a cache miss that causes a slow fallback.
    Fails ~20% of the time — like a real cache being cleared mid-test.
    """
    seed = int(time.time() * 2.1) % 10
    if seed < 2:  # ~20% chance
        pytest.fail(
            "Cache miss: Redis cache was cleared during test run. "
            "Fallback query exceeded timeout threshold. "
            "This is a transient failure — retry should succeed."
        )

    # Cache hit simulation
    result = {"cached": True, "data": add(100, 200)}
    assert result["data"] == 300
    assert result["cached"] is True
