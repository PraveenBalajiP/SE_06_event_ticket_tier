# L6_L7_06 — Event Ticket Tier

## Lab 6: Code and Branch Coverage

### 1. Project Overview

This project implements an event ticket pricing and gate-flow monitoring system using Python.

The system processes confirmed ticket manifests, calculates ticket revenue based on seating tiers and promotional offers, handles fraudulent booking orders, applies additional charges and service tax, and determines whether ticket sales require an audit.

It also monitors turnstile entry rates to identify possible congestion at event gates.

### 2. Project Files

| File | Description |
|---|---|
| `event_ticket_tier.py` | Main implementation containing ticket processing and gate monitoring functions |
| `test_event_ticket.py` | Pytest test suite |
| `README.md` | Project documentation |
| `htmlcov/` | Generated HTML coverage report |

### 3. Functions Implemented

#### A. process_ticket_manifest()

Processes ticket booking manifests and calculates final revenue.

Features:
- VIP, Premium and General ticket pricing.
- Order quantity validation.
- EARLYBIRD promotional discount.
- FRAUD_RISK detection.
- Quantity-based discount.
- Exclusive lounge charges.
- Service tax calculation.
- Audit rejection when rejected orders exceed four.
- Zero-sales and completed transaction statuses.

#### B. monitor_gate_flow()

Monitors turnstile entry rates.

Features:
- Handles empty input.
- Monitors multiple turnstile streams.
- Detects consecutive congestion readings above 50.
- Resets congestion streaks when normal readings occur.
- Returns OVERFLOW or FLOW_NORMAL.

### 4. Testing Approach

The project uses pytest to test both functions.

Test cases cover:
- Valid and invalid inputs.
- All ticket pricing tiers.
- Promotional discounts.
- Fraudulent booking scenarios.
- Invalid quantities.
- Lounge charges.
- Audit rejection conditions.
- Zero-sales scenarios.
- Multiple manifests.
- Normal and congested gate conditions.
- Congestion streak resets.
- Multiple turnstile streams.

### 5. Tools and Technologies

- Python 3.12.10
- pytest 9.1.1
- pytest-cov 7.1.0
- Coverage.py 7.16.0

### 6. Execution Instructions

Install dependencies:

```bash
python -m pip install pytest pytest-cov
```

Run tests:

```bash
python -m pytest -v
```

Run tests with line and branch coverage:

```bash
python -m pytest --cov=event_ticket_tier --cov-branch --cov-report=term-missing
```

Generate an HTML coverage report:

```bash
python -m pytest --cov=event_ticket_tier --cov-branch --cov-report=html
```

Open the report:

```bash
start htmlcov/index.html
```

### 7. Test Results

The completed test suite contains 33 test executions.

| Metric | Result |
|---|---:|
| Total tests | 33 |
| Passed | 33 |
| Failed | 0 |
| Statements | 57 |
| Missing statements | 0 |
| Branches | 40 |
| Partial branches | 0 |
| Line and branch coverage | 100% |

### 8. Conclusion

The Event Ticket Tier project was tested using pytest and pytest-cov.

The test suite achieved 100% statement coverage and 100% branch coverage for `event_ticket_tier.py`, with all 33 test executions passing.

The project demonstrates systematic testing of conditional logic, input validation, pricing rules, fraud handling, and gate congestion monitoring.
