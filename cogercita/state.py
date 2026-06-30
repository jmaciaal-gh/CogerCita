"""State management for conversation and automation workflow."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AgentState(str, Enum):
    """High-level workflow states."""

    IDLE = "idle"
    OPENING_PAGE = "opening_page"
    FILLING_DATA = "filling_data"
    SELECTING_OPTIONS = "selecting_options"
    SELECTING_SLOT = "selecting_slot"
    WAITING_CONFIRMATION = "waiting_confirmation"
    SUBMITTED = "submitted"
    BLOCKED = "blocked"


@dataclass
class SessionState:
    """Mutable execution state."""

    status: AgentState = AgentState.IDLE
    last_error: str | None = None
