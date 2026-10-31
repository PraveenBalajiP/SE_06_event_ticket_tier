
import pytest

from event_ticket_tier import (
    process_ticket_manifest,
    monitor_gate_flow
)

# TESTS FOR process_ticket_manifest

# 1. Invalid input validation
def test_invalid_manifests_input():
    with pytest.raises(ValueError):
        process_ticket_manifest("invalid", 0.1)
def test_negative_service_tax():
    with pytest.raises(ValueError):
        process_ticket_manifest([], -0.1)

# 2. Unconfirmed manifests
def test_unconfirmed_manifest_is_skipped():
    manifests = [
        {
            "is_confirmed": False,
            "tier": "vip",
            "orders": [{"qty": 2, "promo": ""}]
        }
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result == {
        "total_revenue": 0.0,
        "status": "ZERO_SALES"
    }

# 3. Ticket tier pricing
@pytest.mark.parametrize(
    "tier, expected",
    [
        ("vip", 330.0),
        ("premium", 198.0),
        ("general", 99.0)
    ]
)
def test_ticket_tier_pricing(tier, expected):
    manifests = [
        {
            "is_confirmed": True,
            "tier": tier,
            "orders": [{"qty": 2, "promo": ""}]
        }
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["total_revenue"] == expected
    assert result["status"] == "COMPLETED"

# 4. Invalid ticket tier
def test_invalid_ticket_tier():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "student",
            "orders": [{"qty": 2, "promo": ""}]
        }
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["status"] == "ZERO_SALES"

# 5. Invalid quantities
@pytest.mark.parametrize("qty", [0, -1, -5])
def test_invalid_order_quantity(qty):
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "orders": [{"qty": qty, "promo": ""}]
        }
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["status"] == "ZERO_SALES"

# 6. VIP fraudulent booking
def test_vip_fraud_resets_manifest_total():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "vip",
            "orders": [
                {"qty": 2, "promo": ""},
                {"qty": 1, "promo": "FRAUD_RISK"},
                {"qty": 3, "promo": ""}
            ]
        }
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["status"] == "ZERO_SALES"
    assert result["total_revenue"] == 0.0

# 7. Non-VIP fraudulent booking
def test_non_vip_fraud_order():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "premium",
            "orders": [
                {"qty": 1, "promo": "FRAUD_RISK"}
            ]
        }
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["total_revenue"] == 99.0
    assert result["status"] == "COMPLETED"

# 8. Early bird promotion
def test_earlybird_discount():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "orders": [
                {"qty": 2, "promo": "EARLYBIRD"}
            ]
        }
    ]

    result = process_ticket_manifest(manifests, 0.0)

    assert result["total_revenue"] == 72.0
    assert result["status"] == "COMPLETED"


# 9. Quantity-based discount

def test_quantity_discount_at_five():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "orders": [{"qty": 5, "promo": ""}]
        }
    ]

    result = process_ticket_manifest(manifests, 0.0)

    assert result["total_revenue"] == 205.0


def test_quantity_below_five():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "orders": [{"qty": 4, "promo": ""}]
        }
    ]

    result = process_ticket_manifest(manifests, 0.0)

    assert result["total_revenue"] == 180.0


# 10. Exclusive lounge charge

def test_exclusive_lounge_charge():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "exclusive_lounge": True,
            "orders": [{"qty": 2, "promo": ""}]
        }
    ]

    result = process_ticket_manifest(manifests, 0.0)

    assert result["total_revenue"] == 165.0


# 11. Audit rejection

def test_audit_rejected_after_more_than_four_rejections():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "invalid",
            "orders": []
        }
        for _ in range(5)
    ]

    result = process_ticket_manifest(manifests, 0.1)

    assert result["status"] == "AUDIT_REJECTED"


def test_exactly_four_rejections_not_audit_rejected():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "invalid",
            "orders": []
        }
        for _ in range(4)
    ]

    result = process_ticket_manifest(manifests, 0.1)

    assert result["status"] == "ZERO_SALES"


# 12. Zero sales

def test_zero_sales_with_empty_orders():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "orders": []
        }
    ]

    result = process_ticket_manifest(manifests, 0.1)

    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_SALES"


# 13. Default values

def test_default_tier_and_orders():
    manifests = [
        {
            "is_confirmed": True
        }
    ]

    result = process_ticket_manifest(manifests, 0.0)

    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_SALES"


# 14. Multiple manifests

def test_multiple_manifests_revenue():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "orders": [{"qty": 2, "promo": ""}]
        },
        {
            "is_confirmed": True,
            "tier": "premium",
            "orders": [{"qty": 1, "promo": ""}]
        }
    ]

    result = process_ticket_manifest(manifests, 0.1)

    assert result["total_revenue"] == 198.0
    assert result["status"] == "COMPLETED"


# 15. Lounge charge after VIP fraud break

def test_lounge_charge_after_vip_fraud():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "vip",
            "exclusive_lounge": True,
            "orders": [
                {"qty": 1, "promo": "FRAUD_RISK"}
            ]
        }
    ]

    result = process_ticket_manifest(manifests, 0.0)

    assert result["total_revenue"] == 75.0
    assert result["status"] == "COMPLETED"


# ============================================================
# TESTS FOR monitor_gate_flow()
# ============================================================

# 16. Empty input

@pytest.mark.parametrize("streams", [[], None])
def test_no_turnstile_data(streams):
    assert monitor_gate_flow(streams) == "NO_DATA"


# 17. Normal flow

def test_normal_gate_flow():
    streams = [
        [10, 20, 30, 40]
    ]

    assert monitor_gate_flow(streams) == "FLOW_NORMAL"


# 18. Rate exactly 50

def test_rate_exactly_fifty():
    streams = [
        [50, 50, 50]
    ]

    assert monitor_gate_flow(streams) == "FLOW_NORMAL"


# 19. Single congestion reading

def test_single_high_rate():
    streams = [
        [60]
    ]

    assert monitor_gate_flow(streams) == "FLOW_NORMAL"


# 20. Consecutive congestion

def test_two_consecutive_high_rates():
    streams = [
        [60, 70]
    ]

    assert monitor_gate_flow(streams) == "OVERFLOW"


def test_three_consecutive_high_rates():
    streams = [
        [60, 70, 80]
    ]

    assert monitor_gate_flow(streams) == "OVERFLOW"


# 21. Congestion streak reset

def test_normal_rate_resets_congestion_streak():
    streams = [
        [60, 40, 70]
    ]

    assert monitor_gate_flow(streams) == "FLOW_NORMAL"


# 22. Congestion in a later stream

def test_overflow_in_second_stream():
    streams = [
        [60],
        [70, 80]
    ]

    assert monitor_gate_flow(streams) == "OVERFLOW"


# 23. Separate streams do not share congestion streak

def test_congestion_streak_resets_between_streams():
    streams = [
        [60],
        [70]
    ]

    assert monitor_gate_flow(streams) == "FLOW_NORMAL"


# 24. Empty individual stream

def test_empty_individual_stream():
    streams = [
        [],
        [20, 30, 40]
    ]

    assert monitor_gate_flow(streams) == "FLOW_NORMAL"
