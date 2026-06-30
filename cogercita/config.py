"""Configuration for the SEPE booking agent."""

from __future__ import annotations

import os
from dataclasses import dataclass

from .models import AppointmentPreferences, PersonalData


@dataclass(frozen=True)
class AgentConfig:
    """Top-level agent configuration."""

    sepe_url: str
    personal_data: PersonalData
    preferences: AppointmentPreferences
    load_timeout_seconds: int = 30

    @staticmethod
    def from_env() -> "AgentConfig":
        """Build config from environment variables with safe defaults."""
        return AgentConfig(
            sepe_url="https://sede.sepe.gob.es/portalSede/procedimientos-y-servicios/personas/proteccion-por-desempleo/cita-previa",
            personal_data=PersonalData(
                document_id=os.getenv("COGERCITA_DNI", "02520328B"),
                full_name=os.getenv("COGERCITA_FULL_NAME", "Juana Sanchez Sanchez"),
                postal_code=os.getenv("COGERCITA_POSTAL_CODE", "28915"),
                phone=os.getenv("COGERCITA_PHONE", "665343111"),
                email=os.getenv("COGERCITA_EMAIL", "jsanchezsanchez59@gmail.com"),
            ),
            preferences=AppointmentPreferences(
                procedure_type=os.getenv("COGERCITA_PROCEDURE_TYPE", "Cita previa SEPE"),
                office_type=os.getenv("COGERCITA_OFFICE_TYPE", "PRESTACIONES"),
                office=os.getenv("COGERCITA_OFFICE", "Leganés Butarque"),
                channel=os.getenv("COGERCITA_CHANNEL", "Presencial"),
                related_channel=os.getenv("COGERCITA_RELATED_CHANNEL", "Presencial"),
                procedure=os.getenv(
                    "COGERCITA_PROCEDURE",
                    "He finalizado un trabajo: acceso o reanudación de prestación o subsidio",
                ),
                subprocedure=os.getenv(
                    "COGERCITA_SUBPROCEDURE",
                    "He finalizado un trabajo: acceso o reanudación de prestación/subsidio",
                ),
                linked_procedure_choice=os.getenv("COGERCITA_LINKED_PROCEDURE_CHOICE", "AMBOS"),
            ),
            load_timeout_seconds=int(os.getenv("COGERCITA_LOAD_TIMEOUT", "30")),
        )
