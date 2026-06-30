"""Appointment slot selection rules."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable

from .models import AppointmentSlot


def compute_target_datetime(now: datetime) -> datetime:
    """Target datetime: now + 7 days + 1 hour."""
    return now + timedelta(days=7, hours=1)


def select_best_slot(target: datetime, slots: Iterable[AppointmentSlot]) -> AppointmentSlot | None:
    """Apply the required priority rules to select the best slot."""
    ordered = sorted(slots, key=lambda s: s.date_time)
    if not ordered:
        return None

    for slot in ordered:
        if slot.date_time == target:
            return slot

    for slot in ordered:
        if slot.date_time > target:
            return slot

    return min(
        ordered,
        key=lambda s: (abs((s.date_time - target).total_seconds()), s.date_time),
    )
