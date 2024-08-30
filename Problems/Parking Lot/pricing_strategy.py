from abc import ABC, abstractmethod

from vehicle import VehicleType


class PricingStrategy(ABC):

  @abstractmethod
  def calculate_price(self, duration: float,
                      vehicleType: VehicleType) -> float:
    pass


class HourlyPricingStrategy(PricingStrategy):

  def __init__(self):
    self.prices = {VehicleType.CAR: 20.00, # 20 dollars/hr
                   VehicleType.MOTORCYCLE: 15.00 # 15 dollars/hr
                  }

  def calculate_price(self, duration: float,
                      vehicleType: VehicleType) -> float:
    return duration * self.prices[vehicleType]
