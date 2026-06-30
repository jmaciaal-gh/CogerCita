"""CLI entrypoint for local/manual execution."""

from __future__ import annotations

from .agent import SepeAppointmentAgent
from .config import AgentConfig
from .logging_config import configure_logging


def render_summary(summary: dict[str, str]) -> str:
    """Render final summary shown before submit."""
    lines = ["Resumen previo al envío:"]
    for key, value in summary.items():
        lines.append(f"- {key}: {value}")
    lines.append("\n¿Deseas confirmar y enviar la solicitud?")
    return "\n".join(lines)


def main() -> None:
    """Run the agent using an external navigator implementation."""
    configure_logging()
    config = AgentConfig.from_env()
    _ = SepeAppointmentAgent(config)
    print(
        "Este proyecto define la arquitectura del agente. "
        "Integra una implementación de BrowserNavigator (por ejemplo, Playwright) para ejecutar la automatización real."
    )


if __name__ == "__main__":
    main()
