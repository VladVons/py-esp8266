import machine
import ujson
#
import api


def EmptyFunc(aData):
    return aData

def TestSum(aCount):
    TimeStart = api.GetTicks()
    Sum = 0
    for i in range(aCount):
        Sum += i * 3
    return  api.GetTicks() - TimeStart

def TestJson(aCount, aStr):
    TimeStart = api.GetTicks()
    for i in range(aCount):
        Obj = ujson.loads(aStr)
        ujson.dumps(Obj)
    return api.GetTicks() - TimeStart

def TestSetPin(aCount, aPin):
    TimeStart = api.GetTicks()
    for i in range(aCount):
        api.SetPin(aPin, i % 2)
    return api.GetTicks() - TimeStart

def TestSetPwmDuty(aCount, aPin):
    TimeStart = api.GetTicks()
    for i in range(aCount):
        api.SetPwmDuty(aPin, i % 100)
    return api.GetTicks() - TimeStart

def TestFunc(aCount, aStr):
    TimeStart = api.GetTicks()
    for i in range(aCount):
        EmptyFunc(aStr)
    return api.GetTicks() - TimeStart

def TestAll(aCount, aPin):
    Result = {}
    TimeStart = api.GetTicks()

    Result['Cpu_MHz']     = int(machine.freq() / 1000000)
    Result['Sum']         = TestSum(aCount) 
    Result['Json']        = TestJson(aCount, '{"Data": "1234567890"}') 
    Result['Func']        = TestFunc(aCount, '{"Data": "1234567890"}') 
    Result['SetPin']      = TestSetPin(aCount, aPin) 
    Result['SetPwmDuty']  = TestSetPwmDuty(aCount, aPin) 
    Result['Total']       = api.GetTicks() - TimeStart 
    return Result
