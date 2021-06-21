import subprocess

sourceFile = 'oggFiles/2.ogg'
resultFile = 'wavFiles/2.wav'
options = '--force-wav'

cmd = 'opusdec.exe ' + options + ' ' + sourceFile + ' ' + resultFile
subprocess.run(cmd)
