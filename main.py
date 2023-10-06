# from passenger import Passenger
# from plane import Plane
# import random

# def changePercentPassengers(decimalPercent, passengers):
#   copiedPassengers = passengers.copy()
#   numPassengers = len(copiedPassengers)
#   numFinalPassengers = int(decimalPercent * numPassengers)
#   finalPassengers = []
#   for i in range(numFinalPassengers):
#     randIdx = random.randint(0, numPassengers-1)
#     finalPassengers.append(copiedPassengers.pop(randIdx))
#     numPassengers -= 1
#   return finalPassengers

# figure1 = Plane([[]] + [[3, 0]] + [[3, 3]] * 31)

# figure2 = Plane([[]] + [[0, 6, 6, 6, 0]] * 3 + [[3, 6, 6, 6, 3]] * 11)

# figure3 = Plane([[2, 2, 2]] * 3 + [[]] + [[2, 3, 2]] * 14 + [[2,0,2]] + [[2,3,2]] * 21 + [[]])

# print("\n")
# passengers = figure1.getSectionedSeats()
# passengers2 = figure1.getSectionedSeats()
# print((0, 0) in passengers)
# print("\n")
# print((0, 0) in passengers2)
# print((0, 1) in passengers)
# print("\n")
# print((0, 1) in passengers2)
# print((0, 2) in passengers)
# print("\n")
# print((0, 2) in passengers2)

# print(passengers)
# print(len(passengers))
# print("\n")
# newPassengers = changePercentPassengers(0.5, passengers)
# print(newPassengers)
# print(len(newPassengers))
# print("\n")
# print(passengers)
# print(len(passengers))
# print("\n")

import random # To generate random numbers
from passenger import Passenger # Passenger object
from plane import Plane # Plane object
import os # Allows us to clear the console for our diagnostic animation
from time import sleep # Allows us to slow down the algorithm for the animation
from matplotlib import pyplot as plt # Allows us to plot results

tickTime = 0.25 # The amount of time between ticks in the animation
runs = 0 # Global variable that stores the number of simulations that have been run

# Takes a queue and removes 100*(1-decimalPercent)% of the passengers
def changePercentPassengers(decimalPercent, passengers):
  copiedPassengers = passengers.copy()
  numPassengers = len(copiedPassengers)
  numFinalPassengers = int(decimalPercent * numPassengers)
  finalPassengers = []
  for i in range(numFinalPassengers):
    randIdx = random.randint(0, numPassengers-1)
    finalPassengers.append(copiedPassengers.pop(randIdx))
    numPassengers -= 1
  return finalPassengers

# Takes a list of numbers and finds the nth percentile among them
def percentileCalc(percentile, timesLst):
  sortedTimesLst = sorted(timesLst)
  decimalPercentile = percentile/100
  percentileIdx = int(decimalPercentile*len(sortedTimesLst)-1)
  return(sortedTimesLst[percentileIdx])

# Takes a plane layout in s/a/w form and makes it look like a plane (for animation)
def reprPlane(plane):
  arr = [[0 for item in row] for row in plane]
  dct = {'s': '☐', 'a': '|', 'A': '-', 'w': 'X', 'e': '#'}
  for r in range(len(plane)):
    for c in range(len(plane[r])):
      if plane[r][c][0] is not None:
        pgr = plane[r][c][0]
        if pgr.waitTicks > 0:
          arr[r][c] = "w"
        else:
          arr[r][c] = "p"
      else:
        arr[r][c] = dct[plane[r][c][1]]
    arr[r] = ' '.join(arr[r])
  return "\n".join(arr)

# Clears the console and prints the plane again, along with the current tick count
def display(plane, ticks):
  os.system("clear")
  print(ticks)
  print(reprPlane(plane))
  print()
  sleep(tickTime)

# Plane definitions according to the Ordering Algorithm's layout system ("blocks")
figure1 = Plane([[]] + [[3, 0]] + [[3, 3]] * 31)
figure2 = Plane([[]] + [[0, 6, 6, 6, 0]] * 3 + [[3, 6, 6, 6, 3]] * 11)
figure3 = Plane([[2, 2, 2]] * 3 + [[]] + [[2, 3, 2]] * 14 + [[2,0,2]] + [[2,3,2]] * 21 + [[]])
figure4 = Plane([[]] + [[3, 0]] + [[3, 3]] * 9)

# Plane definitions according to the Timing Algorithm's layout system ("s/a/w")
plane1layout = [["e"] + ["A"]*6] + [["s", "s", "s", "a", "w", "w", "w"]] + [["s", "s", "s", "a", "s", "s", "s"]]*31
plane2layout = [["e"] + ["A"]*27] + [["w"]*3 + (["a"] + ["s"]*6)*3 + ["a"] + ["w"]*3]*3 + [["s"]*3 + (["a"] + ["s"]*6)*3 + ["a"] + ["s"]*3]*11
plane3layout = [["s", "s", "a", "s", "w", "s", "a", "s", "s"]]*3 + [["e"] + ["A"]*8] + [["s", "s", "a", "s", "s", "s", "a", "s", "s",]]*14 + [["s", "s", "a", "w", "w", "w", "a", "s", "s"]] + [["s", "s", "a", "s", "s", "s", "a", "s", "s",]]*21 + [["e"] + ["A"]*8]
plane4layout = [["e"] + ["A"]*6] + [["s", "s", "s", "a", "w", "w", "w"]] + [["s", "s", "s", "a", "s", "s", "s"]]*9

# Layout in s/a/w form -> A 3D array plane within which the simulation occurs
def generatePlane(layout):
  plane = [[[None, item] for item in row] for row in layout]
  return plane

# The simulation function
def simulation(queue, layout, disProb=0.1, carryProb=0.87, maxCarryOns=1):
  # Helper function that tests if everyone is seated or not  
  def allSeated():
    for passenger in seated:
      if seated[passenger] == False:
        return False
    return True

  # Helper function that checks if there is someone in a row between a seat and the aisle (both exclusive)
  def shufflingTest(row, seat, aisle):
    if seat < aisle:
      low = seat + 1
      high = aisle
    else:
      low = aisle + 1
      high = seat

    for i in range(low, high):
      if plane[row][i][0] != None:
        return True
    return False

  # Helper function that counts how many people are within a row between seat and aisle, exclusive
  def countPeople(row, seat, aisle):
    if seat < aisle:
      low = seat + 1
      high = aisle
    else:
      low = aisle + 1
      high = seat

    count = 0
    for i in range(low, high):
      if plane[row][i][0] != None:
        count += 1

    return count

  # Choosing the closest entrance to each passenger
  whichEntrance = dict()
  entrances = []
  for r in range(len(layout)):
      if layout[r][0] == 'e':
        entrances.append(r)

  for passenger in queue:
    shortest = entrances[0]
    for entrance in entrances:
      if abs(passenger.seat[0] - entrance) < abs(passenger.seat[0] - shortest):
        shortest = entrance
    whichEntrance[passenger] = shortest
    
  # Creating a list that will be populated with people who are disobedient
  disobedients = []

  # Loop through each passenger in queue-order
  for passenger in queue:
    # Determining whether or not each passenger will be disobedient and have a carry on
    passenger.disobedience = random.random() < disProb
    
    for n in range(maxCarryOns):
      passenger.numCarryOns += int(random.random() < carryProb)
    passenger.hasCarryOn = bool(passenger.numCarryOns)

    # Redoing the coordinate system for the simulation's purposes
    row = layout[passenger.seat[0]]
    temp = 0
    col = 0
    
    for item in row:
      if item == "a" or item == "w":
        temp += 1
      if item == "s":
        col += 1
        if col-1 == passenger.seat[1]:
          break
    passenger.seat = (passenger.seat[0], passenger.seat[1]+temp)
    
    # Determining which aisle the passenger would use
    aisles = []
    for i, item in enumerate(row):
      if item == "a":
        aisles.append(i)
    minDist = aisles[0]
    
    for ais in aisles:
      if abs(ais - passenger.seat[1]) < abs(minDist - passenger.seat[1]):
        minDist = ais

    passenger.aisle = minDist

  # New loop through each passenger
  for passenger in queue:
    # Adding disobedient passengers to their list and removing them from the queue
    if passenger.disobedience == True:
      disobedients.append(passenger)
      queue.remove(passenger)

  # Re-inserting disobedient passengers into the queue at a random spot
  for passenger in disobedients:
    queue.insert(random.randint(0, len(queue) + 1), passenger) # Remove the "+ 1" from this statement if error
    
  # Simulation
  plane = generatePlane(layout) # Setting the stage
  ticks = 0
  seated = {passenger : False for passenger in queue} # Makes it easy to check if a particular passenger is seated

  # While not everyone is seated
  while allSeated() == False:
    # For each passenger in the order of the queue
    for passenger in queue:
      ent = whichEntrance[passenger] # The entrance the passenger will use
      pos = passenger.position # The passenger's current position
      row = passenger.seat[0] # The passenger's seat's row

      # Passenger is seated if they are in their seat and not waiting
      if passenger.position == list(passenger.seat) and passenger.waitTicks == 0:
        seated[passenger] = True

      # If passenger is waiting, subtract one from tick counter
      if passenger.waitTicks > 0:
        passenger.waitTicks -= 1

      # If passenger is seated, skip all other tests
      elif seated[passenger] == True:
        pass

      # Else if passenger is not on the plane and their entrance is open, go to the entrance
      elif passenger.status == "queued" and plane[ent][0][0] == None:
        passenger.status = "boarded"
        passenger.position = [whichEntrance[passenger], 0]
        plane[ent][0][0] = passenger

      # Else if passenger is not on the plane, wait
      elif passenger.status == "queued" or pos[0] == None or pos[1] == None:
        pass
        
      # Else if in horizontal aisle and wants to turn down vertical aisle
      elif (plane[pos[0]][pos[1]][1] == "A" or plane[pos[0]][pos[1]][1] == "e") and pos[1] == passenger.aisle:
        # If they are behind their seat, set their direction to forward
        if pos[0] > passenger.seat[0]:
          dir = (-1, 0)
        # Else, set their direction to backward
        else:
          dir = (1, 0)
        # If the spot in the direction they want to go is open, go there
        if plane[pos[0] + dir[0]][pos[1] + dir[1]][0] == None:
          passenger.position = [pos[0] + dir[0], pos[1] + dir[1]]
          plane[pos[0] + dir[0]][pos[1] + dir[1]][0] = passenger
          plane[pos[0]][pos[1]][0] = None

      # Else if in horizontal aisle and next space is empty, move to next space
      elif (plane[pos[0]][pos[1]][1] == "A" or plane[pos[0]][pos[1]][1] == "e") and plane[pos[0]][pos[1] + 1][0] is None:
        passenger.position[1] += 1
        plane[pos[0]][pos[1] - 1][0] = None
        plane[pos[0]][pos[1]][0] = passenger
        
      # Else if shuffling around needs to happen (and passanger is ahead of their seat)
      elif pos == [row - 1, passenger.aisle] and shufflingTest(row, passenger.seat[1], pos[1]):
        openSpaces = True
        requiredSpaces = countPeople(row, passenger.seat[1], pos[1]) + 1

        # Check if next n + 1 spaces are open
        for n in range(1, requiredSpaces + 1):
          if pos[0] + n < len(plane):
            if plane[pos[0] + n][pos[1]][0] != None:
              openSpaces = False

        # If they are, move into seat row
        if openSpaces:
          passenger.position[0] += 1
          plane[pos[0] - 1][pos[1]][0] = None
          plane[pos[0]][pos[1]][0] = passenger
        if pos == passenger.seat:
            seated[passenger] = True

      # Else if shuffling around needs to happen (and passanger is behind their seat) 
      elif pos == [row + 1, passenger.aisle] and shufflingTest(row, passenger.seat[1], pos[1]):
        openSpaces = True
        requiredSpaces = countPeople(row, passenger.seat[1], pos[1]) + 1

        for n in range(1, requiredSpaces + 1):
          if pos[0] - n >= 0:
            if plane[pos[0] - n][pos[1]][0] != None:
              openSpaces = False

        if openSpaces:
          passenger.position[0] -= 1
          plane[pos[0] + 1][pos[1]][0] = None
          plane[pos[0]][pos[1]][0] = passenger
        if pos == passenger.seat:
            seated[passenger] = True

      # Else if in vertical aisle and reached target row and have carry-on, stow carry-on
      elif plane[pos[0]][pos[1]][1] == "a" and pos[0] == passenger.seat[0] and passenger.hasCarryOn:
        passenger.waitTicks = random.randint(6, 13)*passenger.numCarryOns
        if pos == passenger.seat:
            seated[passenger] = True
        passenger.hasCarryOn = False

      # Else if in vertical aisle and reached target row, move into row
      elif plane[pos[0]][pos[1]][1] == "a" and pos[0] == passenger.seat[0]:
        # If there are people between the aisle and the seat, skip over them and wait
        if shufflingTest(row, passenger.seat[1], pos[1]):
          passenger.waitTicks = abs(passenger.seat[1] - pos[1]) - 1
          passenger.position = list(passenger.seat)
          plane[pos[0]][pos[1]][0] = None
          pos = passenger.position
          plane[pos[0]][pos[1]][0] = passenger

        # Move one space toward their seat
        elif pos[1] > passenger.seat[1]:
          passenger.position[1] -= 1
          plane[pos[0]][pos[1] + 1][0] = None
          plane[pos[0]][pos[1]][0] = passenger
          if pos == passenger.seat:
            seated[passenger] = True
        else:
          passenger.position[1] += 1
          plane[pos[0]][pos[1] - 1][0] = None
          plane[pos[0]][pos[1]][0] = passenger
          if pos == passenger.seat:
            seated[passenger] = True

      # Else if in vertical aisle, move one space forward 
      elif plane[pos[0]][pos[1]][1] == "a":
        if passenger.seat[0] > pos[0]:
          if plane[pos[0] + 1][pos[1]][0] is None:
            passenger.position[0] += 1
            plane[pos[0] - 1][pos[1]][0] = None
            plane[pos[0]][pos[1]][0] = passenger
        else:
          if plane[pos[0] - 1][pos[1]][0] is None:
            passenger.position[0] -= 1
            plane[pos[0] + 1][pos[1]][0] = None
            plane[pos[0]][pos[1]][0] = passenger

      # Else if in row but not in seat, move towards seat
      elif pos[0] == passenger.seat[0] and pos[1] != passenger.seat[1]:
        if pos[1] > passenger.seat[1]:
          passenger.position[1] -= 1
          plane[pos[0]][pos[1] + 1][0] = None
          plane[pos[0]][pos[1]][0] = passenger
          if pos == passenger.seat:
            seated[passenger] = True
        else:
          passenger.position[1] += 1
          plane[pos[0]][pos[1] - 1][0] = None
          plane[pos[0]][pos[1]][0] = passenger 
          if pos == passenger.seat:
            seated[passenger] = True
  
    ticks += 1 # Update tick counter
    display(plane, ticks) # Clear console and display the plane and the tick counter

  global runs # Allows us to update the runs variable within the function
  runs += 1 # Each time the simulation runs, add one to "runs"
  # print(runs)
  return ticks

simulation(figure3.getRandomSeats(), plane3layout)