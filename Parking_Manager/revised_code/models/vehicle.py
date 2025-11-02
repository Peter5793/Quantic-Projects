from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class VehicleInfo:
    """Data class for vehicle information"""
    registration: str
    make: str
    model: str
    color: str

class Vehicle(ABC):
    """Abstract base class for all vehicles"""
    
    def __init__(self, info: VehicleInfo):
        self._info = info
        self._is_electric = False

    @property
    def registration(self) -> str:
        return self._info.registration

    @property
    def make(self) -> str:
        return self._info.make

    @property
    def model(self) -> str:
        return self._info.model

    @property
    def color(self) -> str:
        return self._info.color

    @property
    def is_electric(self) -> bool:
        return self._is_electric

    def __str__(self) -> str:
        return f"{self.color} {self.make} {self.model} ({self.registration})"

    # Legacy support - camelCase methods delegating to new properties
    def get_regnum(self) -> str:
        return self.registration

    def get_make(self) -> str:
        return self.make

    def get_model(self) -> str:
        return self.model

    def get_color(self) -> str:
        return self.color

class Car(Vehicle):
    """Regular car implementation"""
    pass

class Motorcycle(Vehicle):
    """Regular motorcycle implementation"""
    pass

class ElectricVehicle(Vehicle):
    """Base class for electric vehicles"""
    
    def __init__(self, info: VehicleInfo):
        super().__init__(info)
        self._is_electric = True
        self._charge_level = 0

    @property
    def charge_level(self) -> int:
        return self._charge_level

    @charge_level.setter
    def charge_level(self, value: int):
        self._charge_level = max(0, min(100, value))

    # Legacy support
    def get_charge(self) -> int:
        return self.charge_level

    def set_charge(self, value: int) -> None:
        self.charge_level = value

class ElectricCar(ElectricVehicle):
    """Electric car implementation"""
    pass

class ElectricBike(ElectricVehicle):
    """Electric motorcycle implementation"""
    pass