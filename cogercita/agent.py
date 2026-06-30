"""Main orchestration logic for the SEPE appointment agent."""

from __future__ import annotations

import logging
from datetime import datetime

from .config import AgentConfig
from .errors import (
    CaptchaDetectedError,
    NoSlotsAvailableError,
    OptionUnavailableError,
    PageUnavailableError,
    SessionExpiredError,
)
from .models import AppointmentDraft, SelectionResolution
from .navigator import BrowserNavigator
from .scheduler import compute_target_datetime, select_best_slot

LOGGER = logging.getLogger(__name__)


def resolve_option(options: list[str], desired: str) -> SelectionResolution:
    """Return exact desired option and alternatives without auto-fallback."""
    normalized = {o.casefold(): o for o in options}
    selected = normalized.get(desired.casefold())
    alternatives = [o for o in options if o.casefold() != desired.casefold()]
    return SelectionResolution(selected=selected, alternatives=alternatives)


class SepeAppointmentAgent:
    """Coordinates the full appointment preparation flow."""

    def __init__(self, config: AgentConfig) -> None:
        self.config = config

    def prepare_draft(self, navigator: BrowserNavigator, now: datetime | None = None) -> AppointmentDraft:
        """Prepare the request but never submit without explicit confirmation."""
        run_now = now or datetime.now()
        target = compute_target_datetime(run_now)
        LOGGER.info("Opening SEPE page")

        try:
            navigator.open(self.config.sepe_url, self.config.load_timeout_seconds)
            navigator.wait_page_ready()
        except Exception as exc:  # pragma: no cover - adapter-level failures
            raise PageUnavailableError(str(exc)) from exc

        if navigator.captcha_or_official_auth_required():
            raise CaptchaDetectedError("Autenticación oficial/CAPTCHA detectado. Intervención del usuario requerida.")

        navigator.fill_personal_data(
            document_id=self.config.personal_data.document_id,
            full_name=self.config.personal_data.full_name,
            postal_code=self.config.personal_data.postal_code,
            phone=self.config.personal_data.phone,
            email=self.config.personal_data.email,
        )

        warnings: list[str] = []
        self._ensure_required_option(navigator, "procedure_type", self.config.preferences.procedure_type, warnings)
        self._ensure_required_option(navigator, "office_type", self.config.preferences.office_type, warnings)
        self._ensure_required_option(navigator, "office", self.config.preferences.office, warnings)
        self._ensure_required_option(navigator, "channel", self.config.preferences.channel, warnings)
        self._ensure_required_option(navigator, "related_channel", self.config.preferences.related_channel, warnings)
        self._ensure_required_option(navigator, "procedure", self.config.preferences.procedure, warnings)
        self._ensure_required_option(navigator, "subprocedure", self.config.preferences.subprocedure, warnings)

        if navigator.has_linked_procedure_prompt():
            navigator.choose_linked_procedure(self.config.preferences.linked_procedure_choice)

        if navigator.session_expired():
            raise SessionExpiredError("Sesión caducada durante la preparación de la cita.")

        slots = list(navigator.get_available_slots())
        if not slots:
            raise NoSlotsAvailableError("No existen citas disponibles.")

        selected_slot = select_best_slot(target, slots)
        if selected_slot is None:
            raise NoSlotsAvailableError("No existen citas válidas disponibles.")

        navigator.choose_slot(selected_slot)

        summary = {
            "DNI": self.config.personal_data.document_id,
            "Nombre y apellidos": self.config.personal_data.full_name,
            "Código Postal": self.config.personal_data.postal_code,
            "Oficina": self.config.preferences.office,
            "Tipo de oficina": self.config.preferences.office_type,
            "Canal": self.config.preferences.channel,
            "Canal relacionado": self.config.preferences.related_channel,
            "Trámite": self.config.preferences.procedure,
            "Subtrámite": self.config.preferences.subprocedure,
            "Fecha seleccionada": selected_slot.date_time.strftime("%d/%m/%Y"),
            "Hora seleccionada": selected_slot.date_time.strftime("%H:%M"),
            "Teléfono": self.config.personal_data.phone,
            "Correo electrónico": self.config.personal_data.email,
        }

        return AppointmentDraft(
            target_date_time=target,
            selected_slot=selected_slot,
            summary=summary,
            warnings=warnings,
            requires_user_action=bool(warnings),
        )

    def submit_with_confirmation(self, navigator: BrowserNavigator, confirmed: bool) -> bool:
        """Submit only after explicit user confirmation."""
        if not confirmed:
            LOGGER.info("Submission canceled by user")
            return False
        if navigator.captcha_or_official_auth_required():
            raise CaptchaDetectedError("Autenticación oficial/CAPTCHA detectado antes de enviar.")
        navigator.submit()
        LOGGER.info("Request submitted")
        return True

    def _ensure_required_option(
        self,
        navigator: BrowserNavigator,
        field_key: str,
        desired: str,
        warnings: list[str],
    ) -> None:
        options = list(navigator.get_options(field_key))
        resolution = resolve_option(options, desired)
        if resolution.selected is None:
            msg = (
                f"No disponible '{desired}' para '{field_key}'. "
                f"Alternativas: {', '.join(resolution.alternatives) if resolution.alternatives else 'ninguna'}"
            )
            warnings.append(msg)
            raise OptionUnavailableError(msg)
        navigator.choose_option(field_key, resolution.selected)
