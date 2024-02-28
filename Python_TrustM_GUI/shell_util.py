import subprocess
import os
from subprocess import PIPE


def convertInputToHex(input_str, req_length):
    converted_output = ""
    # convert input to hex
    # L has to be stripped due to some weird python convention
    # [2:] as the first two are the hex prefix, 0x
    try:
        converted_output += ((hex(int(input_str, 16)))[2:]).strip("L")
    except ValueError:
        return 0
    # if input is still too short, pad with zeroes
    # if too long, truncate to appropriate length
    diff_length = req_length - len(converted_output)
    if (diff_length > 0):
        while (diff_length > 0):
            converted_output += "0"
            diff_length -= 1
    return converted_output[:req_length]


def checkDir():
    workingDir = "./working_space/"
    if not os.path.exists(workingDir):
        os.makedirs(workingDir)
    os.chdir(workingDir)
    return


# Executes the supplied shell script on the command line
def execShellScript(fullpath):
    output = ""
    try:
        print(input)
        output = subprocess.check_output([sh, str(fullpath)], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
        print("ERROR")
        print(output)
    return(output)


# Executes the supplied command parameters with OpenSSL
def execCLI(cmd):
    output = ""
    try:
        print((">>> ", " ".join(cmd)))
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
        print("ERROR")
        print(output)
    return(output)

# def execCLI2(cmd):
#     print((">>> ", " ".join(cmd)))
#     output = subprocess.run(cmd, capture_output=True, text=True)
#     return(output.stdout)
# 
# def execCLI3(cmd):
# #     print((">>> ", " ".join(cmd)))
#     proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
#     out, err = proc.communicate() 
#     return(out)

# ~ def createProcess(cmd, file):
    # ~ output = ""
    # ~ try:
        # ~ output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

    # ~ except subprocess.CalledProcessError as e:
        # ~ output = e.output
        # ~ print("ERROR")
        # ~ print(output)
        
    # ~ return(output)
    
def createProcess(cmd):
    output = ""
    try:
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError as e:
        output = e.output
        print("ERROR")
        print(output)

    return output
    
    
def createProcess2(cmd, file):
    output = ""
    try:
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError as e:
        output = e.output
        print("ERROR")
        print(output)

    return output


def createProcess_PIPE(cmd, file):
    output = ""
    try:
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        output = e.output
        print("ERROR")
        print(output)
    return(output)
