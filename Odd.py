class Odd:
  def __init__(self, hw):
      self.hw=hw
      self.draw=0
      self.home=0
      self.away=0
      self.aw=0

  home:float
  draw:float
  away:float
  hw:float
  aw:float
  def fillodds(self):
      self.aw=1-self.hw
      self.draw=abs(self.hw-self.aw)
      while(self.draw>0.4):
          self.draw/=2
      left=1-self.draw
      self.home=left*self.hw/(self.hw+self.aw)
      self.away=left*self.aw/(self.hw+self.aw)
