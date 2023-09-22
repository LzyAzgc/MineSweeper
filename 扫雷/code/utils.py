import time

class Time():
    def __init__(self):#初始化
        self.time = 0
        self.createTime = time.time()
        self.partTime = 0

    def timeUpdate(self):
        self.time += 1
    
    def getPartTime(self):
        self.partTime = time.time()-self.createTime
        return self.partTime
    
    def setCreateTime(self):
        self.createTime = time.time()

    def getCurrentTime(self):
        return time.time()
    
    def itsTimetoPlay(self):
        return self.time == 0
    
