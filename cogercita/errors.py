"""Domain errors for the SEPE appointment agent."""


class AgentError(Exception):
    """Base agent error."""


class PageUnavailableError(AgentError):
    """Raised when page cannot be opened or loaded."""


class SessionExpiredError(AgentError):
    """Raised when the remote site session has expired."""


class CaptchaDetectedError(AgentError):
    """Raised when human intervention is needed for authentication/CAPTCHA."""


class ValidationError(AgentError):
    """Raised when form values are rejected by the website."""


class OptionUnavailableError(AgentError):
    """Raised when a required option is not available."""


class NoSlotsAvailableError(AgentError):
    """Raised when the site has no appointment slots."""
