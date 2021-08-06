from midiutil.MidiFile import MIDIFile
import os

#instrument parameter is an integer value from the GM1 Sound Set
map = {
'C1':24,'C2':36,'C3':48,'C4':60,'C5':72,'C6':84,'C7':96,'C8':108,
'c1':25,'c2':37,'c3':49,'c4':61,'c5':73,'c6':85,'c7':97,

'D1':26,'D2':38,'D3':50,'D4':62,'D5':74,'D6':86,'D7':98,
'd1':27,'d2':39,'d3':51,'d4':63,'d5':75,'d6':87,'d7':99,

'E1':28,'E2':40,'E3':52,'E4':64,'E5':76,'E6':88,'E7':100,

'F1':29,'F2':41,'F3':53,'F4':65,'F5':77,'F6':89,'F7':101,
'f1':30,'f2':42,'f3':54,'f4':66,'f5':78,'f6':90,'f7':102,

'G1':31,'G2':43,'G3':55,'G4':67,'G5':79,'G6':91,'G7':103,
'g1':32,'g2':44,'g3':56,'g4':68,'g5':80,'g6':92,'g7':104,

'A1':33,'A2':45,'A3':57,'A4':69,'A5':81,'A6':93,'A7':105,
'a1':34,'a2':46,'a3':58,'a4':70,'a5':82,'a6':94,'a7':106,

'B1':35,'B2':47,'B3':59,'B4':71,'B5':83,'B6':95,'B7':107}


def musicReader(input, output, instrument, x=0.27):
    # input += ".txt"
    # output += ".txt"
    file = open(input,"r")
    writeFile = open(output+".txt","w")
    # writePreFile = open("musicTextPreFinal3.txt","w")
    x=0

    musicString1 = file.read()

    #Tens place 1 refers to left hand, 2 means right hand
    #The units place is for the octave
    musicNotes = {11:"",12:"",13:"",14:"",15:"",16:"",17:"",
                  21:"",22:"",23:"",24:"",25:"",26:"",27:"",
                  31:"",32:"",33:"",34:"",35:"",36:"",37:"",
                  41:"",42:"",43:"",44:"",45:"",46:"",47:"",
                  51:"",52:"",53:"",54:"",55:"",56:"",57:"",
                  61:"",62:"",63:"",64:"",65:"",66:"",67:""}

    flags = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0}
    #Flag to check if the octant is already present in the block

    """
                RH:5|--c--d--e-----------f--e--|
                RH:4|-----------------g--------|
                LH:4|--------------c-----------|
                LH:3|--------c--g--------------|"""

    # print(flags[5])
    # 0 --> No note
    # 1 --> 1 note
    # 2 --> 2 notes/repeats twice

    for block in musicString1.split("\n\n"):
        for line in block.split("\n"):
            if len(line)==32:
                octant = line[3]
                pos = 3
            else:
                octant = line[0]
                pos = 0
            # print(octant)
            flags[octant] += 1

            musicNotes[int(str(flags[octant])+str(octant))] += line[pos+2:-1]


    # If iter1 has 0 flag then fill both 11 and 21
    # else if iter2 has 1 flag fill just 21

        for octant in flags.keys():

            if flags[octant] == 0:
                musicNotes[int("1"+str(octant))] += "-"*26
                musicNotes[int("2"+str(octant))] += "-"*26
                musicNotes[int("3"+str(octant))] += "-"*26
                musicNotes[int("4"+str(octant))] += "-"*26
                musicNotes[int("5"+str(octant))] += "-"*26
                musicNotes[int("6"+str(octant))] += "-"*26

            if flags[octant] == 1:
                musicNotes[int("2"+str(octant))] += "-"*26
                musicNotes[int("3"+str(octant))] += "-"*26
                musicNotes[int("4"+str(octant))] += "-"*26
                musicNotes[int("5"+str(octant))] += "-"*26
                musicNotes[int("6"+str(octant))] += "-"*26

            if flags[octant] == 2:
                musicNotes[int("3"+str(octant))] += "-"*26
                musicNotes[int("4"+str(octant))] += "-"*26
                musicNotes[int("5"+str(octant))] += "-"*26
                musicNotes[int("6"+str(octant))] += "-"*26

            if flags[octant] == 3:
                musicNotes[int("4"+str(octant))] += "-"*26
                musicNotes[int("5"+str(octant))] += "-"*26
                musicNotes[int("6"+str(octant))] += "-"*26

            if flags[octant] == 4:
                musicNotes[int("5"+str(octant))] += "-"*26
                musicNotes[int("6"+str(octant))] += "-"*26

            if flags[octant] == 5:
                musicNotes[int("6"+str(octant))] += "-"*26

        # print("Flags Values -->",list(flags.values()))
        flags = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0} #Reset the flags to 0
        # print("Line Done")

    # print(musicNotes,"\n")
    #{"11":"---c----D-------", "12":"-----c-a-A--a---", ..}
    strr = ""
    for key in list(musicNotes.keys())[:]:
        strr+=str(key)[1]+"|"+musicNotes[key]+"\n"
        # print(len(s))

    # writePreFile.write("\n".join(str(musicNotes).split("', ")))
    # writePreFile.write(str(musicNotes))
    writeFile.write(strr)
    writeFile.close()
    writeFile = open(output+".txt","r")
    strFile = writeFile.read()



myMIDI = MIDIFile(2)
    myMIDI.addProgramChange(0, 0, 0, 0)
    # Flute 75, Sitar 104, Acoustic Guitar 24,25, violin 40, Xylophone 13, Electric Piano 4, Cello 42, Pan Flute 75, Drum 114, Kalimba 108
    myMIDI.addProgramChange(0, 1, 0, instrument)
    track = 1
    time = 0
    # myMIDI.changeNoteTuning(0, tuning, tuningProgam=0)
    myMIDI.addTrackName (track,time,output)
    myMIDI.addTempo (track,time,120)
    #tempo = 120
    channel = 0
    volume = 100

    strFile = strFile.swapcase()

    i = 2
    notes_time = []
    max_i = len((strFile.splitlines())[0])-1
    t = 0

    while i<=max_i :
        for line in strFile.splitlines() :
            if (line[i]!='-') :
                note = line[i]+line[0]
                pitch = map[note]
                notes_time.append(pitch)
            else :
                note = 'X'  #can be anything
                pitch = 0
                notes_time.append(pitch)
        i=i+1
        #print (notes_time)

        volume = 100
        for j in notes_time :
            if (j==0) :
                myMIDI.addNote (track,channel,j,t,1,0)
            else :
                myMIDI.addNote (track,channel,j,t,1,volume)
        t = t+x #average estimated delay .... 5 dashes ~ 1 second
        notes_time = []


    binfile = open(output+".mid","wb")
    myMIDI.writeFile(binfile)
    myMIDI.writeFile(binfile)
    binfile.close()


    file.close()
    writeFile.close()

    os.chdir(cwd)
    os.remove(output+".txt")
    
