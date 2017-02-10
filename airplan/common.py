cLogSHow = True
#cLogSHow = False


def Log(*aParam):
    if (cLogSHow):
        print("Log: %s" % list(aParam))
