from hypothesis import given, strategies as st
from processor import (
    decode_promo_voucher,
    calculate_seat_tier_price,
    parse_attendee_badge,
)


@given(st.text() | st.none())
def test_decode_promo_voucher_no_crash(value):
    try:
        decode_promo_voucher(value)
    except Exception as exc:
        assert False, f"decode_promo_voucher crashed for {value!r}: {exc}"


@given(st.text() | st.none())
def test_calculate_seat_tier_price_safe(value):
    try:
        calculate_seat_tier_price(value)
    except Exception as exc:
        assert False, f"calculate_seat_tier_price crashed for {value!r}: {exc}"


@given(st.text() | st.none())
def test_parse_attendee_badge_safe(value):
    try:
        parse_attendee_badge(value)
    except Exception as exc:
        assert False, f"parse_attendee_badge crashed for {value!r}: {exc}"


def test_valid_promo_voucher():
    assert decode_promo_voucher("EARLY-20") == "Valid EARLY: 20% OFF"


def test_valid_seat_price():
    assert calculate_seat_tier_price("VIP@4") == 158.0


def test_valid_attendee_badge():
    assert parse_attendee_badge("Praveen,21,A12") == "Praveen [Adult] - Seat A12"
