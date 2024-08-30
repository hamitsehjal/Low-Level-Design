from typing import Dict, List

from display_board import DisplayBoard, Subscriber
from parking_spot import ParkingSpot, ParkingSpotFactory
from payment_processor import CardPayment, PaymentProcessor
from pricing_strategy import HourlyPricingStrategy, PricingStrategy
from ticket import Ticket
from vehicle import Vehicle, VehicleType


class ParkingLot:
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      print("Creating a new Instance")
      cls._instance = super(ParkingLot, cls).__new__(cls)
      cls._instance.initialize()  # run initialization
    return cls._instance

  def initialize(self):
    self.spots: Dict[VehicleType, List[ParkingSpot]] = {}
    self.tickets: Dict[int, Ticket] = {}  # unique identifier to a Ticket
    self.displayBoard = DisplayBoard()
    self.pricingStrategy: PricingStrategy = HourlyPricingStrategy()
    self.payment: PaymentProcessor = CardPayment()
    self.subscribers: List[Subscriber] = [self.displayBoard]

  def add_parking_spot(self, vehicleType: VehicleType, count: int):

    start_id = len(self.spots[vehicleType])
    new_spots = [
        ParkingSpotFactory.create_spot(vehicleType, i)
        for i in range(start_id, start_id + count)
    ]

    self.spots[vehicleType].extend(new_spots)
    self.notify_subscribers()

  def park_vehicle(self, vehicle: Vehicle) -> Ticket:
    # is parking spot for vehicleType avaialbe
    available_spots = [
        spot for spot in self.spots[vehicle.getType()] if not spot.is_occupied
    ]
    if not available_spots:
      raise Exception(
          f"Not enough Parking Spot for Vehicle of Type {vehicle.getType()}")
    spot = available_spots[0]
    ticket = Ticket(vehicle, spot)

    self.notify_subscribers()  # notify subscribers for parking spot changes
    return ticket

  def unpark_vehicle(self, id: int) -> bool:
    if id not in self.tickets:
      raise ValueError(f"Invalid Ticket Number - {id}")

    ticket = self.tickets[id]
    vehicle = ticket.vehicle
    spot = ticket.spot

    ticket.end_parking()  # update the exit time
    total_duration = ticket.parking_duration
    amount_due = self.pricingStrategy.calculate_price(total_duration,
                                                      vehicle.getType())
    if self.payment.process_payment(amount_due):
      print("Payment Processed")

      spot.vacate()  # vacate the parking spot
      self.notify_subscribers()  # notify the observer
      del self.tickets[id]  # delete the ticket from parking lot system

      return True
    else:
      raise Exception("Payment Failed")

  def get_availalbe_spots(self) -> Dict[VehicleType, int]:
    # available_spots = {}
    # for vehicleType,spots in self.spots.items():
    #   count = sum(1 for spot in spots if not spot.is_occupied)
    #   available_spots[vehicleType] = count

    # return available_spots

    # dictionary Comprehension Version
    return {
        vehicleType: sum(1 for spot in spots if not spot.is_occpied)
        for vehicleType, spots in self.spots.items()
    }

  def set_payment_processor(self, payment_method: PaymentProcessor):
    self.payment = payment_method

  def set_pricing_strategy(self, strategy: PricingStrategy):
    self.pricingStrategy = strategy

  def add_subscriber(self, subscriber: Subscriber):
    self.subscribers.append(subscriber)

  def remove_subscriber(self, subsriber: Subscriber):
    self.subscribers.remove(subsriber)

  def notify_subscribers(self):
    # get available spots
    spots = self.get_availalbe_spots()
    for sub in self.subscribers:
      sub.update(spots)
