# 定义一个工作的类

class Job():
    def __init__(self, positionId, positionName, city, createTime, salary, companyId, companyName, companyFullName):
        self.positionId = positionId
        self.positionName = positionName
        self.city = city
        self.createTime = createTime
        self.salary = salary
        self.companyId = companyId
        self.companyName = companyName
        self.companyFullName = companyFullName

    def __str__(self):
        return '{positionId = ' + self.positionId + '; positionName = ' + self.positionName + \
               '; city = ' + self.city + '; createTime = ' + self.createTime + '; salary = ' + self.salary + '; companyId = ' + self.companyId \
               + '; companyName = ' + self.companyName + '; companyFullName' + self.companyFullName + '}';

    def __repr__(self):
        return self.__str__()
