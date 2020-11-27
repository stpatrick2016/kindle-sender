class CargoError(Exception):
    pass

class CargoEmptyError(CargoError):
    pass

class CargoLostError(CargoError):
    pass
