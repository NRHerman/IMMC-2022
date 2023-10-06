class Passenger:
  
  def __init__(self, seat):
    self.seat = seat
    self.hasCarryOn = None
    self.disobedience = None
    self.waitTicks = 0
    self.status = "queued" # Becomes "boarded"
    self.position = [None, None]
    self.aisle = None
    self.numCarryOns = 0