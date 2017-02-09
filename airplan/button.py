#---VladVons@gmail.com
# 06.02.17
#---


import machine

cPioBtnFlash = 0
cPioBtnPush  = 4


class TButton:
    def __init__(self, aPin, aOnPress):
        print('TButton.init', aPin);

        self.Pin     = aPin
        self.OnPress = aOnPress

        Obj = machine.Pin(aPin, machine.Pin.IN)
        Obj.irq(trigger = machine.Pin.IRQ_FALLING, handler = self.OnPress)
