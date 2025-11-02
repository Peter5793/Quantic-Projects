from typing import List, Optional, Dict, Tuple
from models.space import ParkingSpace, RegularSpace, EVSpace
from models.vehicle import Vehicle, VehicleInfo, Car, Motorcycle, ElectricCar, ElectricBike

class ParkingLotController:
    """Controller for parking lot operations"""
    
    def __init__(self):
        self._regular_spaces: Dict[int, RegularSpace] = {}
        self._ev_spaces: Dict[int, EVSpace] = {}
        self._vehicle_locations: Dict[str, Tuple[bool, int]] = {}  # registration -> (is_ev, space_id)

    def initialize_lot(self, regular_capacity: int, ev_capacity: int, level: int) -> None:
        """Initialize the parking lot with given capacities"""
        self._regular_spaces = {
            i: RegularSpace(i, level) for i in range(1, regular_capacity + 1)
        }
        self._ev_spaces = {
            i: EVSpace(i, level) for i in range(1, ev_capacity + 1)
        }

    def find_available_space(self, is_ev: bool) -> Optional[ParkingSpace]:
        """Find an available parking space"""
        spaces = self._ev_spaces if is_ev else self._regular_spaces
        return next((space for space in spaces.values() if not space.is_occupied), None)

    def park_vehicle(self, info: VehicleInfo, is_ev: bool, is_motorcycle: bool) -> Optional[int]:
        """Park a vehicle and return the space ID if successful"""
        # Create appropriate vehicle instance
        if is_ev:
            vehicle = ElectricBike(info) if is_motorcycle else ElectricCar(info)
        else:
            vehicle = Motorcycle(info) if is_motorcycle else Car(info)

        # Find available space
        space = self.find_available_space(is_ev)
        if not space:
            return None

        # Park vehicle
        if space.park_vehicle(vehicle):
            self._vehicle_locations[info.registration] = (is_ev, space.space_id)
            return space.space_id
        return None

    def remove_vehicle(self, space_id: int, is_ev: bool) -> bool:
        """Remove a vehicle from a parking space"""
        spaces = self._ev_spaces if is_ev else self._regular_spaces
        if space_id not in spaces:
            return False

        space = spaces[space_id]
        vehicle = space.remove_vehicle()
        if vehicle:
            self._vehicle_locations.pop(vehicle.registration, None)
            return True
        return False

    def get_vehicle_location(self, registration: str) -> Optional[Tuple[bool, int]]:
        """Find vehicle location by registration number"""
        return self._vehicle_locations.get(registration)

    def find_vehicles_by_color(self, color: str, is_ev: bool) -> List[Tuple[int, Vehicle]]:
        """Find vehicles by color"""
        spaces = self._ev_spaces if is_ev else self._regular_spaces
        return [(space_id, space.vehicle) 
                for space_id, space in spaces.items()
                if space.is_occupied and space.vehicle.color == color]

    def get_lot_status(self) -> Dict[str, List[Tuple[int, Vehicle]]]:
        """Get current status of all parking spaces"""
        return {
            'regular': [(space_id, space.vehicle) 
                       for space_id, space in self._regular_spaces.items()
                       if space.is_occupied],
            'ev': [(space_id, space.vehicle)
                  for space_id, space in self._ev_spaces.items()
                  if space.is_occupied]
        }

    def get_ev_charge_status(self) -> List[Tuple[int, int]]:
        """Get charging status of all EVs"""
        return [(space_id, space.vehicle.charge_level)
                for space_id, space in self._ev_spaces.items()
                if space.is_occupied]