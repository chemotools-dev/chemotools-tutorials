from dataclasses import dataclass

@dataclass
class Spectrum:
    x: list[float]
    y: list[float]
    metadata: dict