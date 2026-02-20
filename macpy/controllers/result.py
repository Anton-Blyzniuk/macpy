from dataclasses import dataclass
from subprocess import CompletedProcess


@dataclass
class CommandResult:
    success: bool
    message: str
    error: str | None = None
    output: CompletedProcess | None = None
