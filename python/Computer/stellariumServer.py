import socks, threading, angles, time, struct

class stellariumServer(threading.Thread):
    def __init__(self, sock):
        self.sock = sock
        self.Ra = 0.0
        self.Dec = 0.0
        self.NewRa = 0.0
        self.NewDec = 0.0
        self.alive = True
        self.coordsLocked = False
        threading.Thread.__init__(self)
        
    def run(self):
        print "Starting server..."
        self.sendCoords()
        try:
            while(self.alive and self.sock.alive):
                if (self.Ra != self.NewRa or self.Dec != self.NewDec):
                    self.sendCoords()
        except Exception as e:
            print "Server exception ", e.message
        
        self.stop()

    def updateCoords(self, Ra, Dec):
        if(not self.coordsLocked):
            self.coordsLocked = True
            self.NewRa = Ra
            self.NewDec = Dec
            self.coordsLocked = False
    
    def sendCoords(self):
        if (not self.coordsLocked):
            self.coordsLocked = True
            #Ra = angles.Angle(r=float(self.NewRa))
            #print "Ra: ", Ra
            #Dec = angles.Angle(r=float(self.NewDec))
            #print "Dec: ", Dec
            #print "RaInt: %d, DecInt: %d" % (RaInt, DecInt)
            self.Ra = self.NewRa
            self.Dec = self.NewDec
            # Ok to unlock now
            self.coordsLocked = False
            #[RaInt,DecInt] = self.angleToStellarium(Ra, Dec)
            #data = struct.pack("3iIii", 24, 0, time.time(), RaInt, DecInt, 0)
            data = struct.pack("3iIii", 24, 0, time.time(), self.Ra, self.Dec, 0)
            self.sock.sendData(data)
        
    def angleToStellarium(self,Ra,Dec):
        return [int(Ra.h*(2147483648/12.0)), int(Dec.d*(1073741824/90.0))]
        
    def stop(self):
        self.alive = False
        self.sock.close()
        
