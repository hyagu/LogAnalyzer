import glob
import re
import os
import sys

BOOT_PATH=".\Boot_*"
LOGCAT_PATH="\logcat.*"
FILTERTXT="filter.txt"
OUTPUTFILE_DIR=".\\analyzed\\"
OUTPUTFILE_NAME="analyzed"
OUTPUTFILE_EXT=".txt"
#reason from HometesterLogcat.c StartUpApp.c tombstone.cpp env_common.c
BOOTREASON={'Cold Boot',\
            'NONE',\
            'CrashBoot',\
            'Recovery',\
            'kernel_panic',\
            'reboot',\
            'watchdog',\
            'RC Key',\
            'LKB Key',\
            'Alarm',\
            'CEC',\
            'WOWLAN',\
            'WOLAN',\
            'UART',\
            'SCART',\
            '319753mute'}
VERSIONFILE="version.txt"


def main():
    bootPath = getBootPath(BOOT_PATH)
    logs = {}
    
    for bP in bootPath:
        logs[bP] = getLogcatPath(bP)
        logs[bP].sort(key=useExtForSort)

    if os.path.isfile(FILTERTXT):
        pattern = getRegexPattern()
    else:
        print "no "+FILTERTXT
        pattern = None

    print ("start parsing")
    f = open(OUTPUTFILE_NAME+OUTPUTFILE_EXT,'w')

    #if not os.path.exists(OUTPUTFILE_DIR):
    #    os.makedirs(OUTPUTFILE_DIR)
    
    for bP in bootPath:
        print "\n----------"+bP[2:]+"----------"

        f.write('--------------------\n')
        reason = getBootReason(bP)
        f.write(bP[2:]+'\n')
        f.write('Boot Reason = '+reason+'\n')
        print 'Boot Reason = '+reason
        
        version = getBootVersion(bP)
        f.write(version)
        print version
        f.write('--------------------\n')

        if pattern != None:
            for log in logs[bP]:
                print ("\nparsing..."+log),
                with open(log,'rb') as infile:
                    for line in infile:
                        if testPattern(line,pattern):
                            print ("."),
                            f.write(line)
        
    print ("\nwrite to "+f.name)
    f.close()
    return

def useExtForSort(f):
    n,e= os.path.splitext(f)
    if e[1:] == "txt" :
        return sys.maxint #last one
    else:
        return int(e[1:])

def getBootPath(path):
    return glob.glob(path)

def getBootReason(path):
    for br in BOOTREASON:
        if os.path.isfile(path+'\\'+br+'.txt'):
            return br
    return "unknow"

def getBootVersion(path):
	verPath=path+'\\'+VERSIONFILE
	if os.path.isfile(verPath):
		with open(path+'\\'+VERSIONFILE) as f:
			return f.readline()
	else:
		return "no version"

def getLogcatPath(path):
    lc_path=path+LOGCAT_PATH
    return glob.glob(lc_path) 

def getRegexPattern():
    f = list()
    with open(FILTERTXT) as infile:
        for line in infile:
            if line.strip():
                f.append(line.rstrip()) 
    return f

def testPattern(line,pattern):
    ret = None
    for p in pattern:
        if re.search(p,line):
            ret = True
            
    return ret


if __name__ == "__main__":
    main()

