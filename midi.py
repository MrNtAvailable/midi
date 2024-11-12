import struct


class Event():
    def __init__(self, delta, typeEvent):
        self.delta = delta
        self.type = typeEvent

    def getType(self):
        return self.type

    def getDelta(self):
        return self.delta

#Other Event Definitions go here

class TextEvent(Event):
        def __init__(self, delta, text, typeOf):
            super().__init__(delta, typeOf)
            self.text = text

class DataEvent(Event):
        def __init__(self, delta, num, den, clksPerClk, quarNote):
            super().__init__(delta, "TimeSig")
            self.num = num
            self.den = den
            self.clksPerClk = clksPerClk
            self.quarNote = quarNote
class smpteOffset:
        def __init__(self, delta, hr, mn, se, fr, ff):
            super().__init__(delta, "smpteOffset")
            self.hr = hr
            self.mn = mn
            self.se = se
            self.fr = fr
            self.ff = ff
        
class NoteEvent(Event): #On and off events

    def __init__(self, state, channel, note, veloc, delta):
        super().__init__(delta, "Note")
        self.state = state
        self.channel = channel
        self.note = note
        self.veloc = veloc

    def getNoteData(self)
        return (self.on, self.note, self.delta, self.veloc)

class Track():
    def __init__(self):
        self.name = None
        self.events = []
        
    def setName(self, name):
        self.name = name
        
    def getName(self):
        return self.name

    def setInstr(self, text):
        self.instr = text

    def getInstr(self):
        return self.instr
    
    def addEvent(self, event):
        self.events.append(event)
        
    def getEvent(self, eventNum):
        return self.events[eventNum]

    def getEvents(self, typeOf = "Note"):
        out = []
        for event in self.events:
            if event.getType() == typeOf:
                out.append(event)
        return out
    
    def getAllEvents(self):
        return self.events

    def setData(self, num, den, clksPerClk, quarNote):
        self.num = num
        self.den = den
        self.clksPerClk = clksPerClk
        self.quarNote = quarNote

class MidiFile():
    def __init__(self, file)
        self.file = open(file, "rb")
        self.tracks = []
        
    def getFile(self):
        return self.file
    
    def setFormat(self, formatNum):
        self.format = formatNum
        
    def setNumTracks(self, num):
        self.numTracks = num

    def setLength(self, length):
        self.length = length
        
    def addTrack(self, track)
        self.tracks.append(track)

    def setTicks(self, ticks)
        self.ticks = ticks
        
    def getTrackNames(self)
        names = []
        for tracks in self.tracks:
            names.append(tracks.getName())
        return names
    
    def getTracks(self)
        return self.tracks

    
def variableLength(f):  #Variable length data is stored in byte chuncks with the LSB being a continuation bit. If it is one another byte of the data follows and if zero that this byte is the last byte
                        #The final seven bits actually hold the integer data
    while True: # Delta Time Read
                delta = ""
                delta_in = f.read(1) #Reads delta byte
                delta += delta_in[1:7] #Adds last seven bits to current delta
                if delta_in[0] == 0: #Checks to see if continuation bit, byte[0], is 0, therefore break
                    return int(delta, base=2) #Translates to integer

def readFile(fileName):
    file = MidiFile(fileName)   #Creates MidiFile Object
    tracksCount = 0         #Tracks how many tracks have been parsed
    with file.getFile() as f: 

        header = f.read(4)

        if header != b'MThd':
            raise ValueError("Not a valid MIDI file")
            return(-1)

        length = struct.unpack(">I", f.read(4))[0]

        if length != 6:
            raise ValueError("Header length not correct")
            return(-1)

        formatNum, numTracks, ticks = struct.unpack(">HHH", f.read(6))

        file.setFormat(formatNum)
        file.setNumTracks(numTracks)
        file.setTicks(ticks)

        while True:
            trk = trackRead(f)            
            f.addTrack(trk)
            tracksCount += 1
            if(tracksCount == numTracks):
                break
            
    return file

def trackRead(f): #Track Read       
    trk = Track()
    header = f.read(4)

    if header != b'MTrk':
    raise ValueError("Not a valid track"):
        return(-1)

    trk.setLength(struct.unpack(">I", f.read(4))[0])

    while readTrackEvent(f, trk)

    return trk

def readTrackEvent(f, trk):
    delta = variableLength(f)
    event = f.read(1)
    match event[0:3]:
        case b'\xF': 
            match event[4:7]:
                case b'\xF': #Meta-Event
                    event = f.read(1)
                    match event:
                        case b'\x00':
                        case b'\x01': #Text Event
                            length = variableLength(f)
                            trk.addEvent(TextEvent(delta, f.read(length).decode('ascii'), "Text")
                        case b'\x02': 
                        case b'\x03': #Set Track Name
                            length = variableLength(f)
                            trk.setName(f.read(length).decode('ascii'))
                        case b'\x04': #Set Instrument
                            length = variableLength(f)
                            trk.setInstr(f.read(length).decode('ascii'))
                        case b'\x05': #Lyric Event
                            length = variableLength(f)
                            trk.addEvent(TextEvent(delta, f.read(length).decode('ascii'), "Lyric")
                        case b'\x06': #Text Marker
                            length = variableLength(f)
                            trk.addEvent(TextEvent(delta, f.read(length).decode('ascii'), "Marker")
                        case b'\x07': #Cue Point
                            length = variableLength(f)
                            trk.addEvent(TextEvent(delta, f.read(length).decode('ascii'), "Cue")
                        case b'\x20':
                            length = int(f.read(1),base=2)
                            trk.addEvent(TextEvent(delta, f.read(length).decode('ascii'), "ChannelPrefix")
                        case b'\x2F':
                            f.read(1)
                            trk.addEvent(Event(delta, "EOT")
                        case b'\x51':
                            length = int(f.read(1), base=2)
                            tempo = int(f.read(3), base=2)
                        case b'\x54':
                        case b'\x58':
                            length = int(f.read(1), base=2)
                            num = int(f.read(1), base=2)
                            den = int(f.read(1), base=2)
                            cPC = int(f.read(1), base=2)
                            quar = int(f.read(1), base=2)
                            trk.addEvent(DataEvent(delta, num, den, cPC, quar)) # num, den, clksPerClk, quarNote 
                        case b'\x59':
                        case b'\x7F':
        case b'\x8': #Note Off
            channel = int(event[4:7],base=2)
            noteNum = int(f.read(1), base=2)
            velocity = int(f.read(1), base=2)
            trk.addEvent(NoteEvent(0, channel, noteNum, velocity, delta))
        case b'\x9': #Note On
            channel = int(event[4:7],base=2)
            noteNum = int(f.read(1), base=2)
            velocity = int(f.read(1), base=2)
            trk.addEvent(NoteEvent(1, channel, noteNum, velocity, delta))
          
                
