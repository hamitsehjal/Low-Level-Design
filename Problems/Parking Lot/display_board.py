from abc import ABC, abstractmethod
from typing import Dict

from vehicle import VehicleType


class Subscriber(ABC):

  @abstractmethod
  def update(self, available_spots: Dict[VehicleType, int]):
    pass


class DisplayBoard(Subscriber):

  def __init__(self):
    self.parking_spots: Dict[VehicleType,
                             int] = {}  # mapping vehicle type --> capacity

  def _display(self):
    for vehicleType, capacity in self.parking_spots.items():
      print(f"{vehicleType} - {capacity}")

  def update(self, available_spots: Dict[VehicleType, int]):
    self.parking_spots = available_spots
    self._display()
