from abc import ABC, abstractmethod
from enum import Enum


class VehicleType(Enum):
  CAR = "car"
  MOTORCYCLE = "MOTORCYLCE"


class Vehicle(ABC):

  def __init__(self, license:str):
    self.license_plate = license

  @abstractmethod
  def getType(self) -> VehicleType:
    pass


class Car(Vehicle):
  def __init__(self, license:str):
    super().__init__(license)

  def getType(self):
    return VehicleType.CAR


class MotorCycle(Vehicle):
  def __init__(self, license:str):
    super().__init__(license)

  def getType(self):
    return VehicleType.MOTORCYCLE
  