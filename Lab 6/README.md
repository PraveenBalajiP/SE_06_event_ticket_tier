## Lab 6 — Code and Branch Coverage Analysis

### Objective
To analyse code coverage and branch coverage of the Event Ticket Tier application using pytest and pytest-cov, and to design test cases that exercise statements, decision branches, and edge cases.

### Application
The application contains two functions:

- `process_ticket_manifest()` — processes confirmed ticket manifests, applies ticket-tier pricing, promotional discounts, fraud handling, lounge charges, and service tax.
- `monitor_gate_flow()` — monitors turnstile entry rates and detects consecutive high-congestion readings.

### Test Deliverables

| File | Purpose |
|---|---|
| `event_ticket_tier.py` | Application source code |
| `CodeCoverageTest_06_event_ticket_tier.py` | Test cases for code coverage |
| `BranchCoverageTest_06_event_ticket_tier.py` | Test cases for branch coverage |
| `test_event_ticket.py` | Original combined test suite |

### Coverage Results

| Metric | Result |
|---|---:|
| Tests passed | 33 |
| Statements | 57 |
| Missing statements | 0 |
| Statement coverage | 100% |
| Branches | 40 |
| Partial branches | 0 |
| Branch coverage | 100% |

### Commands to Run

**Code coverage:**

```bash
python -m pytest -v CodeCoverageTest_06_event_ticket_tier.py --cov=event_ticket_tier --cov-report=term-missing
```

**Branch coverage:**

```bash
python -m pytest -v BranchCoverageTest_06_event_ticket_tier.py --cov=event_ticket_tier --cov-branch --cov-report=term-missing
```

**HTML coverage report:**

```bash
python -m pytest --cov=event_ticket_tier --cov-branch --cov-report=html
```

### Evidence

Terminal screenshots and the HTML coverage report are maintained in the `screenshots/` and `htmlcov/` directories.

### Conclusion

The test suite achieved 100% statement coverage and 100% branch coverage for the application. All 33 test executions passed, exceeding the minimum 90% coverage target specified in the Lab 6 handout.
