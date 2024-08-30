from abc import ABC, abstractmethod

from vehicle import VehicleType


class ParkingSpot(ABC):

  def __init__(self, id: int):
    self.id = id
    self.is_occupied = False

  def occupy(self) -> bool:
    if not self.is_occupied:
      self.is_occpied = True
      return True
    return False

  def vacate(self) -> bool:
    if self.is_occupied:
      self.is_occpied = False
      return True
    return False

  @abstractmethod
  def can_fit_vehicle(self, vehicleType: VehicleType) -> bool:
    pass


class CarSpot(ParkingSpot):

  def can_fit_vehicle(self, vehicleType: VehicleType) -> bool:
    return vehicleType == VehicleType.CAR


class MotorCycleSpot(ParkingSpot):

  def can_fit_vehicle(self, vehicleType: VehicleType) -> bool:
    return vehicleType == VehicleType.MOTORCYCLE


class ParkingSpotFactory:

  @staticmethod
  def create_spot(vehicleType: VehicleType, spot_id: int) -> ParkingSpot:
    if vehicleType == VehicleType.CAR:
      return CarSpot(spot_id)
    elif vehicleType == VehicleType.MOTORCYCLE:
      return MotorCycleSpot(spot_id)
    else:
      raise ValueError(
          f"Unsupported Vehicle Type {vehicleType} - Id({spot_id})")
