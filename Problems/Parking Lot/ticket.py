from datetime import datetime

from parking_spot import ParkingSpot
from vehicle import Vehicle


class Ticket:

  def __init__(self, vehicle: Vehicle, parkingSpot: ParkingSpot):
    self.id = id(self)  # unique integer for this object
    self.vehicle = vehicle
    self.spot = parkingSpot
    self.entry_time = datetime.now()
    self.exit_time = None

  def end_parking(self):
    self.exit_time = datetime.now()

  @property
  def parking_duration(self) -> float:
    if self.exit_time is None:
      return (datetime.now() - self.entry_time).total_seconds() / 3600
    return (self.exit_time - self.entry_time).total_seconds() / 3600
