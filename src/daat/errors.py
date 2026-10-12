"""Error codes are DaaT-local, not new IK wire codes."""
class DaatError(Exception):
    def __init__(self, code: str, message: str = "") -> None:
        self.code = code
        super().__init__(message or code)

class ContractError(DaatError):
    pass

class MappingError(DaatError):
    pass

class AdmissionError(DaatError):
    pass
