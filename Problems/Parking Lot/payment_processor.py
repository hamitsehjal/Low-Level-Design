from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
  @abstractmethod
  def process_payment(self,amount:float)->bool:
    pass

class CashPayment(PaymentProcessor):
  def process_payment(self, amount: float) -> bool:
    print(f"Processing payment using Cash: Amount - {amount}")
    return True

class CardPayment(PaymentProcessor):
  def process_payment(self, amount: float) -> bool:
    print(f"Processing payment using Card: Amount - {amount}")
    return True