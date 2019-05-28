# morsecoding.py                                                               
# by Tibor Borbás - borbi.tibor@outlook.hu                                     
# Date: 2017.04.11.                                                            
# Description:                                                                 
# Encrypt or decrypt a given text file with morse codes.       
# Capable to load different codetables made by the user.
# Converting morse code from text file to audio file.
# Further development in exception handling and functionality planned.
# Usage: morsecoding.py [-h] [-d SrcFile DestFile | -e SrcFile DestFile | -s SrcFile DestFile]
#                       [-c CodeFile] [-t] [-v]
#
# Encrypt or decrypt the given text file with morse codes.
#
# optional arguments:
#   -h, --help           show this help message and exit
#   -d SrcFile DestFile  Decrypt the given textfile.
#   -e SrcFile DestFile  Encrypt the given textfile.
#   -s SrcFile DestFile  Convert morse code to .wav file.
#   -c CodeFile          Load user defined codetable.
#   -t                   Show current morse codetable.
#   -v                   Version information.
#-------------------------------------------------------------------------------
__author__ = "Tibor Borbás"
__copyright__ = "Copyright 2017, Morse code project"
__credits__ = ["Tibor Borbás"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Tibor Borbás"
__email__ = "borbi.tibor@outlook.hu"
__status__ = "Development"

# imports
import argparse
import wave
import math
import struct

# Separators used to separate characters and words.
shortgap = '000'
medgap = '0000000'

# Codetable: default is the international morse codetable. It can be replaced with the -c option.
CTable = [['a','10111'],['b','111010101'],['c','11101011101'],['d','1110101'],
          ['e','1'],['f','101011101'],['g','111011101'],['h','1010101'],['i','101'],
          ['j','1011101110111'],['k','111010111'],['l','101110101'],['m','1110111'],
          ['n','11101'],['o','11101110111'],['p','10111011101'],['q','1110111010111'],
          ['r','1011101'],['s','10101'],['t','111'],['u','1010111'],['v','101010111'],
          ['w','101110111'],['x','11101010111'],['y','1110101110111'],['z','11101110101'],
          ['1','10111011101110111'],['2','101011101110111'],['3','1010101110111'],
          ['4','10101010111'],['5','101010101'],['6','11101010101'],['7','1110111010101'],
          ['8','111011101110101'],['9','11101110111011101'],['0','1110111011101110111'],
          ['.','10111010111010111'],[',','1110111010101110111'],['?','101011101110101'],
          ["'",'1011101110111011101'],['!','1110101110101110111'],['/','1110101011101'],
          ['(','111010111011101'],[')','1110101110111010111'],[':','11101110111010101'],
          [';','11101011101011101'],['=','1110101010111'],['+','1011101011101'],
          ['-','111010101010111'],['"','101110101011101'],['@','10111011101011101']]

# ----------------------------------Functions-----------------------------------

# Encrypt character
def ecryptchar(letter):
    checker = False
    for i in range(len(CTable)):
        if letter.lower() == CTable[i][0]:
            checker = True
            return CTable[i][1]
    if not checker:return '#'

# Decrypt character
def decryptchar(letter):
    checker = False
    for i in range(len(CTable)):
        if letter.lower() == CTable[i][1]:
            checker = True
            return CTable[i][0]
    if not checker:return '#'

# Encrypt word
def ecryptword(lline):
    result = ''
    for i in range(len(lline)):
        result = result + ecryptchar(lline[i])
        if i < (len(lline)-1):result = result + shortgap
    return result

# Decrypt word
def decryptword(lline):
    result = ''
    letters = lline.split(shortgap)
    for i in range(len(letters)):
        result = result + decryptchar(letters[i])
    return result

# ------------------------------THE MAIN PROGRAM--------------------------------

# Establish an argumentparser to handle arguments from the commandline.
# Commandline arguments: -h, --help             Show help menu
#                        -d SrcFile DestFile    Decrypt source file to destination file
#                        -e SrcFile DestFile    Encrypt source file to destination file
#                        -s SrcFile DestFile	Convert morse code to .wav file
#                        -c CodeFile            Load user defined codetable
#                        -t                     Show current morse codetable
#                        -v                     Version information
parser = argparse.ArgumentParser(description='Encrypt or decrypt the given text file with morse codes.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-d',action='store',dest='decrypt',nargs=2,metavar=('SrcFile','DestFile'),help='Decrypt the given textfile.')
group.add_argument('-e',action='store',dest='encrypt',nargs=2,metavar=('SrcFile','DestFile'),help='Encrypt the given textfile.')
group.add_argument('-s',action='store',dest='convert',nargs=2,metavar=('SrcFile','DestFile'),help='Convert morse code to .wav file.')
parser.add_argument('-c',action='store',dest='codefile',metavar='CodeFile',help='Load user defined codetable.')
parser.add_argument('-t',action='store_true',dest='switch',default=False,help='Show current morse codetable')
parser.add_argument('-v',action='version',version='morsecoding 0.1',help='Version information.')
args = parser.parse_args()

# Load new morse codetable if given. If not, the default builtin (CTable) codetable is used.
if args.codefile:
    CTable = []
    try:CTFile = open(args.codefile,encoding = 'utf-8')
    except IOError:
        print("Can't open codetable!")
        exit()
    while True:
        try:strinline = CTFile.readline().strip('\n')
        except IOError:
            print("Can't read from codetable file!")
            CTFile.close()
            exit()
        if strinline == '':break
        oneline = strinline.split(' ')
        CTable.append(oneline)
    CTFile.close()
    print('Codetable imported!')

# Encrypt the given source file to the destination file.
if args.encrypt:
    try:OutFile = open(args.encrypt[1],'w',encoding = 'utf-8')
    except IOError:
        print("Can't open destination file!")
        exit()
    try:InFile = open(args.encrypt[0],encoding = 'utf-8')
    except IOError:
        print("Can't open source file!")
        OutFile.close()
        exit()
    while True:
        try:strinline = InFile.readline().strip('\n')
        except IOError:
            print("Can't read source file!")
            InFile.close()
            OutFile.close()
            exit()
        if strinline == '':break
        oneline = strinline.split(' ')
        for i in range(len(oneline)):
            try:OutFile.write(ecryptword(oneline[i]))
            except IOError:
                print("Can't write to destination file!")
                OutFile.close()
                InFile.close()
                exit()
            if i < (len(oneline)-1):
                try:OutFile.write(medgap)
                except IOError:
                    print("Can't write to destination file!")
                    OutFile.close()
                    InFile.close()
                    exit()
    InFile.close()
    OutFile.close()
    print('File successfully encrypted to {}!'.format(args.encrypt[1]))

# Decrypt the given source file to the destination file.
if args.decrypt:
    try:OutFile = open(args.decrypt[1],'w',encoding = 'utf-8')
    except IOError:
        print("Can't open destination file!")
        exit()
    try:InFile = open(args.decrypt[0],encoding = 'utf-8')
    except IOError:
        print("Can't open source file!")
        OutFile.close()
        exit()
    while True:
        try:strinline = InFile.readline().strip('\n')
        except IOError:
            print("Can't read source file!")
            InFile.close()
            OutFile.close()
            exit()
        if strinline == '':break
        oneline = strinline.split(medgap)
        for i in range(len(oneline)):
            try:OutFile.write(decryptword(oneline[i])+' ')
            except IOError:
                print("Can't write to destination file!")
                InFile.close()
                OutFile.close()
                exit()
    InFile.close()
    OutFile.close()
    print('File successfully decrypted to {}!'.format(args.decrypt[1]))

# Convert the given morse code in a text file to .wav file
if args.convert:
    HighC = 5230           # in Hertz
    TiDuration = 0.5      # in sec - Ti is always one time unit long (20 wpm)
    TaDuration = 1.5      # in sec - Ta is always three time unit long (20 wpm)
    morsewords = []
    try:wavefile = wave.open(args.convert[1],'w')
    except wave.Error:
        print("Can't write to destination file!")
        exit()
    wavefile.setnchannels(1)
    wavefile.setsampwidth(2)
    wavefile.setframerate(44100)
    try:InFile = open(args.convert[0],encoding = 'utf-8')
    except IOError:
        print("Can't open source file!")
        wavefile.close()
        exit()
    morsewords = InFile.readline().strip('\n').split(medgap)
    for i in range(len(morsewords)):
        for j in range(len(morsewords[i])):
            if morsewords[i][j] == '0':
                for k in range(int(TiDuration*44100.0)):
                    value = int(32767.0*math.cos(HighC*math.pi*float(k)/float(44100.0)))
                    packeddata = struct.pack('h',value)
                    wavefile.writeframes(packeddata)
            if morsewords[i][j] == '1':
                for k in range(int(TaDuration*44100.0)):
                    value = int(32767.0*math.cos(HighC*math.pi*float(k)/float(44100.0)))
                    packeddata = struct.pack('h',value)
                    wavefile.writeframes(packeddata)
    InFile.close()
    wavefile.close()
    
# Print to screen the currently used morse codetable replacing '111' to '-' and '1' to '.'(CTable)
if args.switch:
    for i in range(len(CTable)):
        codeline = CTable[i][1]
        codeline = codeline.replace('111','-').replace('1','.').replace('0','')
        print(' {} {}'.format(CTable[i][0],codeline))
    
# If no argument is given: print out 'No argument was given! For more information please use -h option!'
if not args.decrypt and not args.encrypt and not args.convert and not args.codefile and not args.switch:
    print('No argument was given!\nFor more information please use -h option!')
