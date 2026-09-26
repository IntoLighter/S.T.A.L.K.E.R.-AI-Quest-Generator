from dataclasses import dataclass


@dataclass
class ErrorInfo:
    msg: str
    details: str
