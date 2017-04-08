LogLevel = 1

def Log(aLevel, *aParam):
    if (aLevel <= LogLevel):
        print('LogLevel %d: %s%s' % (aLevel, ' ' * aLevel, list(aParam)))
