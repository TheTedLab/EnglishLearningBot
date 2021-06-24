import subprocess


def opusToWav(sourceFile: str, resultFile: str):
    options = '--force-wav'
    cmd = 'opusdec.exe ' + options + ' ' + sourceFile + ' ' + resultFile
    subprocess.run(cmd)
