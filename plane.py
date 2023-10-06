import random
import math
from passenger import Passenger

class Plane:

  # Initializer and Test Functions
  
  def __init__(self, chunks):
    self.data = chunks

  def __str__(self):
    temp = ""
    for lst in self.data:
      if (len(lst) == 0):
        temp += "e"
      else:
        for c in range(len(lst)):
          for i in range(lst[c]):
            temp += "s "
          if (c != len(lst)-1):
            temp += "r "
      temp += "\n"
    return temp

  # Quality of Code Functions
  
  def numRows(self):
    temp = [x.copy() for x in self.data]
    while [] in temp:
      temp.remove([])
    return len(temp)

  def sumChunks(self, row):
    temp = 0
    for chunk in self.data[row]:
      temp += chunk
    return temp

  def greatestChunk(self):
    max = 0
    for lst in self.data:
      for i in range(len(lst)):
        if (i == 0 or i == len(lst)-1):
          if (lst[i] > max):
            max = lst[i]
        else:
          if (math.ceil(lst[i]/2) > max):
            max = math.ceil(lst[i]/2)
    return max

  def convertToPassengers(self, seats):
    passengerList = []
    for i in range(len(seats)):
      passengerList.append(Passenger(seats[i]))
    return passengerList
  
  def getSeats(self):
    seats = []
    for l in range(len(self.data)):
      rowLength = 0
      for chunk in self.data[l]:
        rowLength += chunk
      for i in range(rowLength):
        seats.append((l, i))
    return seats

  # Seating Arrangement Functions

  def getRandomSeats(self):
    seats = self.getSeats()
    random.shuffle(seats)
    return self.convertToPassengers(seats)

  # Need to adjust for different combinations of aft, mid, and bow.
  def getSectionedSeats(self):
    seats = self.getSeats()
    numRows = self.numRows()
    aft = []
    mid = []
    bow = []
    for i in range(len(seats)):
      seat = seats[i]
      if (seat[0] <= numRows//3 + numRows%3/2):
        bow.append(seat)
      elif (seat[0] <= numRows//3 + (numRows//3 + numRows%3/2)):
        mid.append(seat)
      else:
        aft.append(seat)
    random.shuffle(aft)
    random.shuffle(mid)
    random.shuffle(bow)
    return aft + mid + bow

  def getStackingSeats(self):
    seats = []
    for l in range(len(self.data)-1, -1, -1):
      rowSeats = self.sumChunks(l)
      if (len(self.data[l]) != 0):
        for c in range(rowSeats, rowSeats-self.data[l][-1], -1):
            seats.append((l, c-1))
        if (len(self.data[l]) > 1):
          for a in range(len(self.data[l])-2, 0, -1):
            s = 0
            for x in range(0, a):
              s += self.data[l][x]
            for c in range(s+self.data[l][a]//2, s+self.data[l][a]):
              seats.append((l, c))
            for c in range(s+math.ceil(self.data[l][a]/2), s, -1):
              seats.append((l, c-1))
          for c in range(0, self.data[l][0]):
            seats.append((l, c))
    return self.convertToPassengers(seats)

  def getColumnSeats(self):
    seats = []
    for i in range(self.greatestChunk()):
      seats.append([])
    for l in range(len(self.data)):
      if (len(self.data[l]) != 0):
        temp = 0
        for c in range(0, self.data[l][0]):
          seats[temp].append((l, c))
          temp += 1
        if (len(self.data[l]) >= 2):
          temp = 0
          for c in range(self.sumChunks(l)-1, self.sumChunks(l)-self.data[l][-1]-1, -1):
            seats[temp].append((l, c))
            temp += 1
          if (len(self.data[l]) >= 3):
            for i in range(1, len(self.data[l])-1):
              s = 0
              for x in range(0, i):
                s += self.data[l][x]
              temp = 0
              for c in range(math.ceil(self.data[l][i]/2), 0, -1):
                seats[temp].append((l, s + c - 1))
                temp += 1
              temp = 0
              for c in range(math.ceil(self.data[l][i]/2)+1, self.data[l][i]+1):
                seats[temp].append((l, s + c - 1))
                temp += 1
    newSeats = []
    for i in seats:
      random.shuffle(i)
      newSeats = newSeats + i
    return self.convertToPassengers(newSeats)
  
  def getWindowSeats(self):
    seats = []
    for i in range(self.greatestChunk()):
      seats.append([])
    for i in range(1, len(self.data[1])-1): 
      for l in range(len(self.data)):
        if (len(self.data[l]) >= 3):
          s = 0
          for x in range(0, i):
            s += self.data[l][x]
          temp = 0
          for c in range(math.ceil(self.data[l][i]/2), 0, -1):
            seats[temp].append((l, s + c - 1))
            temp += 1
    for l in range(len(self.data)):
      if (len(self.data[l]) >= 2):
        temp = 0
        for c in range(self.sumChunks(l)-1, self.sumChunks(l)-self.data[l][-1]-1, -1):
          seats[temp].append((l, c))
          temp += 1
    for l in range(len(self.data)):
      if (len(self.data[l]) != 0):
        temp = 0
        for c in range(0, self.data[l][0]):
          seats[temp].append((l, c))
          temp += 1
    for i in range(1, len(self.data[1])-1): 
      for l in range(len(self.data)):
        if (len(self.data[l]) >= 3):
          s = 0
          for x in range(0, i):
            s += self.data[l][x]
          temp = 0
          for c in range(math.ceil(self.data[l][i]/2)+1, self.data[l][i]+1):
            seats[temp].append((l, s + c - 1))
            temp += 1
    newSeats = []
    for i in seats:
      i.reverse()
      newSeats = newSeats + i
    return self.convertToPassengers(newSeats)

  # We'll probably never use this.
  def getReverseSeats(self):
    seats = []
    for l in range(len(self.data)):
      rowSeats = self.sumChunks(l)
      if (len(self.data[l]) != 0):
        for c in range(rowSeats, rowSeats-self.data[l][-1], -1):
            seats.append((l, c-1))
        if (len(self.data[l]) > 1):
          for c in range(rowSeats-self.data[l][-1], self.data[l][0], -1):
            seats.append((l, c-1))
          for c in range(1, self.data[l][0]+1):
            seats.append((l, c-1))
    return seats 