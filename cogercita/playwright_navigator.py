"""Playwright-based navigator implementation with resilient selectors."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .models import AppointmentSlot


class PlaywrightNavigator:
    """Concrete navigator using Playwright page object.

    This adapter prioritizes role/label queries and keeps selector fallbacks
    to better tolerate minor UI changes.
    """

    def __init__(self, page: Any) -> None:
        self.page = page

    def open(self, url: str, timeout_seconds: int) -> None:
        self.page.goto(url, wait_until="domcontentloaded", timeout=timeout_seconds * 1000)

    def wait_page_ready(self) -> None:
        self.page.wait_for_load_state("networkidle")

    def fill_personal_data(self, *, document_id: str, full_name: str, postal_code: str, phone: str, email: str) -> None:
        self._fill(["DNI", "NIF", "NIE"], document_id)
        self._fill(["Nombre y apellidos", "Nombre"], full_name)
        self._fill(["Código Postal", "Código postal"], postal_code)
        self._fill(["Teléfono", "Movil", "Móvil"], phone)
        self._fill(["Correo", "Email"], email)

    def get_options(self, field_key: str) -> list[str]:
        select = self._find_select(field_key)
        options = select.locator("option")
        return [o.inner_text().strip() for o in options.all() if o.inner_text().strip()]

    def choose_option(self, field_key: str, value: str) -> None:
        select = self._find_select(field_key)
        select.select_option(label=value)

    def has_linked_procedure_prompt(self) -> bool:
        return self.page.get_by_text("Si desea solicitar además cita adicional", exact=False).count() > 0

    def choose_linked_procedure(self, option: str) -> None:
        self.page.get_by_role("button", name=option).click()

    def get_available_slots(self) -> list[AppointmentSlot]:
        items = self.page.locator("[data-slot-datetime], .slot, .cita-disponible")
        result: list[AppointmentSlot] = []
        for it in items.all():
            raw = (it.get_attribute("data-slot-datetime") or it.inner_text()).strip()
            dt = self._parse_datetime(raw)
            if dt is not None:
                result.append(AppointmentSlot(date_time=dt, raw_label=raw))
        return result

    def choose_slot(self, slot: AppointmentSlot) -> None:
        self.page.get_by_text(slot.raw_label, exact=False).first.click()

    def submit(self) -> None:
        self.page.get_by_role("button", name="Confirmar").click()

    def session_expired(self) -> bool:
        return self.page.get_by_text("sesión ha caducado", exact=False).count() > 0

    def captcha_or_official_auth_required(self) -> bool:
        return (
            self.page.get_by_text("captcha", exact=False).count() > 0
            or self.page.get_by_text("Cl@ve", exact=False).count() > 0
            or self.page.get_by_text("certificado digital", exact=False).count() > 0
            or self.page.get_by_text("firma electrónica", exact=False).count() > 0
        )

    def _fill(self, labels: list[str], value: str) -> None:
        for label in labels:
            locator = self.page.get_by_label(label, exact=False)
            if locator.count() > 0:
                locator.first.fill(value)
                return
        raise ValueError(f"No se encontró un campo para: {labels}")

    def _find_select(self, field_key: str):
        field_labels = {
            "procedure_type": ["Tipo de trámite", "Trámite"],
            "office_type": ["Tipo de oficina"],
            "office": ["Oficina"],
            "channel": ["Canal"],
            "related_channel": ["Canal relacionado"],
            "procedure": ["Trámite"],
            "subprocedure": ["Subtrámite", "Sub trámite"],
        }
        for label in field_labels.get(field_key, [field_key]):
            select = self.page.get_by_label(label, exact=False)
            if select.count() > 0:
                return select.first
        raise ValueError(f"No se encontró selector para: {field_key}")

    @staticmethod
    def _parse_datetime(text: str) -> datetime | None:
        for fmt in ("%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M", "%d-%m-%Y %H:%M"):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
        return None
