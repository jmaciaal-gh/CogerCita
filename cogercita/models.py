"""Data models used by the agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Sequence


@dataclass(frozen=True)
class PersonalData:
    """Personal details preloaded for automation."""

    document_id: str
    full_name: str
    postal_code: str
    phone: str
    email: str


@dataclass(frozen=True)
class AppointmentPreferences:
    """Preferred administrative options for the appointment request."""

    procedure_type: str
    office_type: str
    office: str
    channel: str
    related_channel: str
    procedure: str
    subprocedure: str
    linked_procedure_choice: str = "AMBOS"


@dataclass(frozen=True)
class AppointmentSlot:
    """An appointment date-time option returned by the website."""

    date_time: datetime
    raw_label: str


@dataclass
class SelectionResolution:
    """Selection result for one field."""

    selected: str | None
    alternatives: Sequence[str] = field(default_factory=tuple)


@dataclass
class AppointmentDraft:
    """Prepared appointment state before final submit."""

    target_date_time: datetime
    selected_slot: AppointmentSlot | None
    summary: dict[str, str]
    warnings: list[str] = field(default_factory=list)
    requires_user_action: bool = False
    confirmation_prompt: str = "¿Deseas confirmar y enviar la solicitud?"
