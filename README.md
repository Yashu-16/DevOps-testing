# DecisionOps Test Project

A simple Python project with intentionally flaky tests to demonstrate
DecisionOps self-healing capabilities.

## How the flaky tests work

| Test | Failure rate | Simulates |
|---|---|---|
| `test_flaky_network_call` | ~30% | Network timeout to upstream API |
| `test_flaky_database_connection` | ~30% | Database connection pool exhaustion |
| `test_flaky_external_service` | ~25% | Payment gateway rate limiting |
| `test_flaky_cache_miss` | ~20% | Redis cache cleared mid-test |

These are **transient failures** — running the exact same tests again
will likely pass. This is what DecisionOps self-healing is designed for.

## Running locally

```bash
pip install -r requirements.txt
pytest test_app.py -v
```

Run multiple times and you will see different tests fail on each run.

## How DecisionOps healing works with this project

1. A push triggers GitHub Actions
2. A flaky test fails
3. GitHub Actions notifies DecisionOps via webhook
4. DecisionOps classifies the failure as `test_failure` (transient)
5. The self-healing engine retries the pipeline
6. The retry run passes (because the flaky condition resolved)
7. Healing tab shows ✓ Healed
