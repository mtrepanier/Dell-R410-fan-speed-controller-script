"""
Python fan controller for Dell R410 based on CPU temperature.

Created by perryclements/r410-fancontroller Github

Based on original script by marcusvb/r710-fancontroller on Github

"""
from subprocess import Popen, PIPE, STDOUT
import time
import string

Tcase = 68    # Tcase, maximum temperature allowed at the processor Integrated Heat Spreader (IHS).

sleepTime = 30
celcius = 'C'
floatDot = '.'

#Do a command and return the stdout of proccess
def sendcommand(cmdIn):
    p = Popen(cmdIn, shell=True, executable="/bin/bash", stdin=PIPE, stdout=PIPE, universal_newlines = True, stderr=STDOUT, close_fds=True)
    return p.stdout.read()

#Do a ipmi command, setup for the default command.
def ipmicmd(cmdIn):
    return sendcommand("ipmitool " + cmdIn)

#Gets the CPU tempertures from lm-sensors, returns the maximum.
def getcputemp():
    cmd = sendcommand('sensors  -u | grep "input"')
    indexes = [pos for pos, char in enumerate(cmd) if char == floatDot]
    cputemperatures = []
    for loc in indexes:
        temp = cmd[int(loc) - 2] + cmd[int(loc) - 1]
        cputemperatures.append(int(temp))

    #return the maximum cpu temperature
    return max(cputemperatures)

    #return the average cpu temperature
    #return sum(cputemperatures) / int(len(cputemperatures))

#Check if controller was in automode, if so we override to manual.
def checkstatus(status):
    if (status == 5):
        ipmicmd("raw 0x30 0x30 0x01 0x00")

#Main checking function which checks temperatures to the default set above.
def checktemps(status):
    maxCpuT = getcputemp()

    if (maxCpuT <= 56):
        if (status != 1):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x10")
            print("Cpu at: " + str(maxCpuT) + " celcius, Fan set to 2700 RPM", flush=True)
        status = 1

    elif(maxCpuT > 56 and maxCpuT <= 58):
        if (status != 2):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x13")
            print("Cpu at: " + str(maxCpuT) + " celcius, Fan set to 3400 RPM", flush=True)
        status = 2

    elif(maxCpuT > 58 and maxCpuT <= 62):
        if (status != 3):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x15")
            print("Cpu at: " + str(maxCpuT) + " celcius, Fan set to 3700 RPM", flush=True)
        status = 3

    elif(maxCpuT > 62 and maxCpuT <= 66):
        if (status != 4):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x19")
            print("Cpu at: " + str(maxCpuT) + " celcius, Fan set to 4600 RPM", flush=True)
        status = 4
    
    elif(maxCpuT > 66 and maxCpuT <= 70):
        if (status != 5):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x21")
            print("Cpu at: " + str(maxCpuT) + " celcius, Fan set to 6000 RPM", flush=True)
        status = 5
    
    elif(maxCpuT > 70 and maxCpuT <= 74):
        if (status != 6):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x23")
            print("Cpu at: " + str(maxCpuT) + " celcius, Fan set to 6500 RPM", flush=True)
        status = 6

    elif(maxCpuT > 74 and maxCpuT <= 78):
        if (status != 7):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x26")
            print("Cpu at: " + str(maxCpuT) + " celcius, Fan set to 7200 RPM", flush=True)
        status = 7

    elif(maxCpuT > 78 and maxCpuT <= 82):
        if (status != 8):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x34")
            print("Cpu at: " + str(maxCpuT) + " celcius, Fan set to 7920 RPM", flush=True)
        status = 8

    elif(maxCpuT > 82 and maxCpuT <= 85):
        if (status != 9):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x36")
            print("Cpu at: " + str(maxCpuT) + " celcius, Fan set to 10320 RPM", flush=True)
        status = 9

    else:
        if (status != 10):
            ipmicmd("raw 0x30 0x30 0x01 0x01")
            print("Cpu at: " + str(maxCpuT) + " celcius, Fan set to auto/loud mode, Server it too hot")
        status = 10

    # print("Cpu at: " + str(maxCpuT) + " celcius,  Fan status =" + str(status),flush=True)
    return status

#Main running function.
def main():
    status = 10
    while True:
        time.sleep(sleepTime)
        status = checktemps(status)
        print("Sleeping for " + str(sleepTime))
if __name__ == '__main__':
    main()
