from abc import ABC, abstractmethod
from typing import Optional
from models.vehicle import Vehicle

class ParkingSpace(ABC):
    """Abstract base class for parking spaces"""
    
    def __init__(self, space_id: int, level: int):
        self._space_id = space_id
        self._level = level
        self._vehicle: Optional[Vehicle] = None
        self._is_occupied = False

    @property
    def is_occupied(self) -> bool:
        return self._is_occupied

    @property
    def space_id(self) -> int:
        return self._space_id

    @property
    def level(self) -> int:
        return self._level

    @property
    def vehicle(self) -> Optional[Vehicle]:
        return self._vehicle

    @abstractmethod
    def can_park(self, vehicle: Vehicle) -> bool:
        """Check if this space can accommodate the given vehicle"""
        pass

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        """Park a vehicle in this space"""
        if not self.can_park(vehicle):
            return False
        self._vehicle = vehicle
        self._is_occupied = True
        return True

    def remove_vehicle(self) -> Optional[Vehicle]:
        """Remove and return the parked vehicle"""
        if not self._is_occupied:
            return None
        vehicle = self._vehicle
        self._vehicle = None
        self._is_occupied = False
        return vehicle

class RegularSpace(ParkingSpace):
    """Regular parking space for non-electric vehicles"""
    
    def can_park(self, vehicle: Vehicle) -> bool:
        return not self.is_occupied and not vehicle.is_electric

class EVSpace(ParkingSpace):
    """Specialized parking space for electric vehicles"""
    
    def can_park(self, vehicle: Vehicle) -> bool:
        return not self.is_occupied and vehicle.is_electric