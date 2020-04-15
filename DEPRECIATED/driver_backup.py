import subprocess
import numpy as np
import os
import sys
out = subprocess.Popen(['wc', '-l', sys.argv[1]],  
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT)
stdout,stderr = out.communicate()
length = stdout.split()[0]
counter = 0
pdb = open(sys.argv[1], "r")
result = open("result.txt", "w+")
for lines in pdb:
    counter += 1
    if lines == "ENDMDL\n":
        break
numFrame = int(int(length) / counter)
resultArray = np.zeros(numFrame, dtype=str)
for frame in range(1, numFrame + 1):
    os.system("head -n " + str(frame * counter) + " " + sys.argv[1] + " | tail -n " + str(counter) + " > out.pdb")
    #os.system("/Applications/Chimera.app/Contents/MacOS/chimera --script chimScript.py --nogui | tail -n 2 | head -n 1 > temp")
    os.system("chimera --script chimScript.py --nogui | tail -n 2 | head -n 1 > temp")
    with open("temp", "r") as file: 
        resultTemp = file.read()
        result.write(resultTemp)
pdb.close()
result.close()
