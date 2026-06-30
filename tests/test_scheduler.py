import unittest
from datetime import datetime

from cogercita.models import AppointmentSlot
from cogercita.scheduler import compute_target_datetime, select_best_slot


class SchedulerTests(unittest.TestCase):
    def test_compute_target_datetime_adds_7_days_and_1_hour(self) -> None:
        now = datetime(2026, 6, 30, 9, 15)
        self.assertEqual(compute_target_datetime(now), datetime(2026, 7, 7, 10, 15))

    def test_select_best_slot_prefers_exact_match(self) -> None:
        target = datetime(2026, 7, 7, 10, 15)
        slots = [
            AppointmentSlot(datetime(2026, 7, 7, 9, 0), "prev"),
            AppointmentSlot(datetime(2026, 7, 7, 10, 15), "exact"),
            AppointmentSlot(datetime(2026, 7, 7, 11, 0), "next"),
        ]

        selected = select_best_slot(target, slots)
        self.assertIsNotNone(selected)
        self.assertEqual(selected.raw_label, "exact")

    def test_select_best_slot_picks_first_later_when_no_exact(self) -> None:
        target = datetime(2026, 7, 7, 10, 15)
        slots = [
            AppointmentSlot(datetime(2026, 7, 7, 12, 0), "later_2"),
            AppointmentSlot(datetime(2026, 7, 7, 11, 0), "later_1"),
        ]

        selected = select_best_slot(target, slots)
        self.assertIsNotNone(selected)
        self.assertEqual(selected.raw_label, "later_1")

    def test_select_best_slot_uses_nearest_when_all_before_target(self) -> None:
        target = datetime(2026, 7, 7, 10, 15)
        slots = [
            AppointmentSlot(datetime(2026, 7, 6, 10, 15), "day_before"),
            AppointmentSlot(datetime(2026, 7, 7, 9, 15), "one_hour_before"),
        ]

        selected = select_best_slot(target, slots)
        self.assertIsNotNone(selected)
        self.assertEqual(selected.raw_label, "one_hour_before")


if __name__ == "__main__":
    unittest.main()
