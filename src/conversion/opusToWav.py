import subprocess


def opus_to_wav(source_file: str, result_file: str):
    options = '--force-wav'
    cmd = '../conversion/opusdec.exe ' + options + ' ' + source_file + ' ' + result_file
    print(cmd)
    subprocess.run(cmd)
