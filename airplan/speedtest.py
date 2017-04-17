import machine
import ujson
#
import libtime
import libpin


def _TimerDecorator(aFunc):
    def Wrapper(aCount, aPar1):
        TimeStart = libtime.GetTicks()
        aFunc(aCount, aPar1)
        return libtime.GetTicks() - TimeStart
    return Wrapper

def EmptyFunc(aData):
    return aData

@_TimerDecorator
def TestSum(aCount, aSum = 0):
    for i in range(aCount):
        aSum += i * 3

@_TimerDecorator
def TestJson(aCount, aStr):
    for i in range(aCount):
        Obj = ujson.loads(aStr)
        ujson.dumps(Obj)

@_TimerDecorator
def TestSetPin(aCount, aPin):
    for i in range(aCount):
        libpin.SetPin(aPin, i % 2)

@_TimerDecorator
def TestSetPwmDuty(aCount, aPin):
    for i in range(aCount):
        libpin.SetPwmDuty(aPin, i % 100)

@_TimerDecorator
def TestFunc(aCount, aStr):
    for i in range(aCount):
        EmptyFunc(aStr)

def TestAll(aCount, aPin):
    Result = {}
    TimeStart = libpin.GetTicks()

    Result['Cpu_MHz']     = int(machine.freq() / 1000000)
    Result['Sum']         = TestSum(aCount, 0) 
    Result['Json']        = TestJson(aCount, '{ "Data": "1234567890", "Arr":[1,2,3,4,5] }') 
    Result['Func']        = TestFunc(aCount, '{ "Data": "1234567890", "Arr":[1,2,3,4,5] }') 
    Result['SetPin']      = TestSetPin(aCount, aPin) 
    Result['SetPwmDuty']  = TestSetPwmDuty(aCount, aPin) 
    Result['Total']       = libtime.GetTicks() - TimeStart 
    return Result
