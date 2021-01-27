import backtrader as bt
from datetime import datetime
from Model import longCalc
from Model import shortCalc

startDay = datetime(2018, 11, 1)
endDay = datetime(2019, 2, 1)
orderStatus = 0
orderTP = 0
orderSL = 0 

class Regression(bt.Strategy):
	def next(self):
		global orderStatus
		global orderTP
		global orderSL

		self.currentDay = self.datetime.datetime(ago=0)
		self.price = self.datas[0].close
		self.max_stake = self.broker.getvalue() / self.price

		self.boundsLong = longCalc(self.currentDay)
		self.boundsShort = shortCalc(self.currentDay)

		self.longCheck = False
		self.shortCheck = False

		if(self.boundsShort[2] > self.boundsLong[2]):
			self.TP = self.boundsShort[0]
			self.SL = self.boundsShort[1]
			self.shortCheck = True
		else:
			self.TP = self.boundsLong[0]
			self.SL = self.boundsLong[1]
			self.longCheck = True

		if not self.position:
			if(self.longCheck):
				if(self.TP != 0 and self.SL != 0):
					self.buy(size=round(self.max_stake, 0))
					orderTP = self.TP
					orderSL = self.SL
					orderStatus = 1
			elif(self.shortCheck):
				if(self.TP != 0 and self.SL != 0):
					self.sell(size=round(self.max_stake, 0))
					orderTP = self.TP
					orderSL = self.SL
					orderStatus = -1
		else:
			if(orderStatus == 1):
				if(self.price >= orderTP or self.price <= orderSL):
					self.close()
				elif(self.shortCheck):
					self.close()
			elif(orderStatus == -1):
				if(self.price <= orderTP or self.price >= orderSL):
					self.close()
				elif(self.longCheck):
					self.close()

		print('Testing: ' + str(self.currentDay.strftime('%Y-%m-%d')))	


if __name__ == '__main__':
	cerebro = bt.Cerebro()
	cerebro.addstrategy(Regression)
	data = bt.feeds.YahooFinanceData(dataname='SPY', 
									 fromdate=startDay,
									 todate=endDay)

	cerebro.adddata(data)
	cerebro.run()
	cerebro.plot()


'''
Had to do the following for backtrader to work:
pip uninstall matplotlib
pip install matplotlib==3.2.2
'''