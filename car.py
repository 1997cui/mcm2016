from misc.py import findnextroad
class Car:
	def __init__(self,startime_,drivingtime=0,car_index,destination,currentroad,currentqueue=0,drivingdist=0):
		self.startime=startime
		#startime is the time when the car starts to drive 
		self.drivingtime=drivingtime
		#drivingtime is the amount of time the car has driven for
		self.destination=destination
		self.nextcross=findnextroad()
		self.currentroad=currentroad
		self.currentqueue=currentqueue
		self.drivingdist=drivingdist
