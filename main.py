

def callProgramWithTerminalCommands(command):
    import subprocess
    subprocess.call(command, shell=True)
    
def waitTillProgramIsDone(command):
    import subprocess
    subprocess.call(command, shell=True)
    while True:
        if subprocess.call(command, shell=True) == 0:
            break
        else:
            continue

if __name__ == '__main__':
    waitTillProgramIsDone('python detect.py --weights best.pt --source input')
    print('Done')
    