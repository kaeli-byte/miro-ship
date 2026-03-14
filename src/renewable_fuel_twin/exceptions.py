class ConfigValidationError(ValueError):
    pass


class WorldBuildError(ValueError):
    pass


class SimulationStateError(RuntimeError):
    pass


class InterventionError(RuntimeError):
    pass


class ReportingError(RuntimeError):
    pass
