#!/usr/bin/python

import json
import urllib2
import hashlib
import os
import sys
import subprocess
import shutil
import re

inputPath = './input/'
urlFile = './url.json'
linkFile = './link.json'
binPath = './bin/'
RABCDAsmPath = './tools/WinRABCDAsm/RABCDAsm/'
patchPath = './patch/'
outputPath = './output/'
tempPath = './temp/'
verbose = False

def info(str, level=1):
    if level == 0:
        print '\n=== {info} ===\n'.format(info = str)
    elif level == 1:
        print '    ',str
    else:
        print '        ',str

def debug(str):
    if not verbose:
        return
    print '    debug:'+str

def getMd5(filePath, chunkSize = 32*1024): # 32KB at a time
    fileObj = open(filePath,'rb')
    md5 = hashlib.md5()
    i=0
    while True:
        data = fileObj.read(chunkSize)
        i=i+1
        if not data:
            break
        debug('Got chunk {num} size: {len}'.format(
            num = i,
            len = len(data)
            ))
        md5.update(data)
        debug('Updated chunk {num} into hash'.format(num = i))
    fileObj.close()
    return md5.hexdigest()

def download(url, filePath, chunkSize = 10*1024, timeOut = 30):
    #10KB at a time
    #30s time out
    debug('Downloading '+url)
    nObj = urllib2.urlopen(url, None, timeOut)
    fObj = open(filePath, 'wb')
    i=0
    while True:
        data = nObj.read(chunkSize)
        i=i+1
        if not data:
            break
        debug('Got chunk {num} size: {len}'.format(
            num = i,
            len = len(data)
            ))
        fObj.write(data)
        debug('Wrote chunk {num} into {file}'.format(
            num = i,
            file = filePath
            ))
    fObj.close()
    nObj.close()

def confirm(prompt, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n:
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y:
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """

    if prompt is None:
        raise Exception('Not valid prompt')

    if resp:
        prompt = '%s %s/%s: ' % (prompt, 'Y', 'n')
    else:
        prompt = '%s %s/%s: ' % (prompt, 'N', 'y')

    while True:
        ans = raw_input(prompt)
        print ''
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

def abcexport(filePath):
    abcFilePath = filePath[:-4]+'-0.abc'
    p = subprocess.Popen(
        [binPath+'abcexport', filePath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
    stdout, stderr = p.communicate()
    if len(stdout)>0 or len(stderr)>0:
        raise Exception([stdout,stderr,p.returncode])
    return abcFilePath

def rabcdasm(abcFilePath):
    opcodePath = abcFilePath[:-4]
    p = subprocess.Popen(
        [binPath+'rabcdasm', abcFilePath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
    stdout, stderr = p.communicate()
    if len(stdout)>0 or len(stderr)>0:
        raise Exception([stdout,stderr,p.returncode])
    return opcodePath

def rabcasm(opcodePath):
    matches = re.search('([^\/]+)\/?$',opcodePath)
    if not matches:
        raise Exception('Invalid opcode path: '+opcodePath)
    asasmFile = opcodePath+'/'+matches.group(1)+'.main.asasm'
    newAbcFile = asasmFile[:-6]+'.abc'
    p = subprocess.Popen(
        [binPath+'rabcasm', asasmFile],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
    stdout, stderr = p.communicate()
    if len(stdout)>0 or len(stderr)>0:
        raise Exception([stdout,stderr,p.returncode])
    return newAbcFile

def abcreplace(file, abcFile):
    p = subprocess.Popen(
        [binPath+'abcreplace', file, '0', abcFile],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
    stdout, stderr = p.communicate()
    if len(stdout)>0 or len(stderr)>0:
        raise Exception([stdout,stderr,p.returncode])

def swfbinreplace(file, index, replace):
    p = subprocess.Popen(
        [binPath+'swfbinreplace', file, index, replace],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
    stdout, stderr = p.communicate()
    if len(stdout)>0 or len(stderr)>0:
        raise Exception([stdout,stderr,p.returncode])

def patch(opcodePath,patchPath):
    if not os.path.exists(patchPath) :
        debug(patchPath+' not exists')
        return False

    absPatchPath = os.path.abspath(patchPath)
    absBinPath = os.path.abspath(binPath)
    p = subprocess.Popen(
        absBinPath+'\patch -u -p1 < '+absPatchPath,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd = opcodePath
        )
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception([stdout,stderr,p.returncode])
    return True

def clean(path):
    for fileName in os.listdir(path) :
        if(fileName[0]!='.'):
            filePath = path+fileName
            debug('Removing '+fileName)
            if os.path.isdir(filePath):
                shutil.rmtree(filePath)
            else:
                os.remove(filePath)
            continue
def mklink(link, target):
    absLink = os.path.abspath(link)
    absTarget = os.path.abspath(target)
    debug(
        'Linking : {link} ==> {target}'.format(
            link = absLink,
            target = absTarget
            )
        )
    if not os.path.exists(absTarget):
        raise Exception('Error when making link, target not exists: '+absTarget)
    if os.path.islink(absTarget) :
        mklink(absLink, os.readlink(absTarget))
    else:
        p = subprocess.Popen(
            'mklink {link} {target}'.format(
                link = absLink,
                target = absTarget
                ),
            shell=True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
        )
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise Exception([stdout,stderr,p.returncode])
    return True

info('Making symbolic link',0)
linkObj = open(linkFile)
links = json.load(linkObj)
for linkName in links:
    if not os.path.exists(binPath+linkName):
        linkFile = binPath+linkName
        targetFile = RABCDAsmPath+linkName
        info('Linking {link} ==> {target}'.format(link=linkFile, target=targetFile))
        mklink(binPath+linkName, RABCDAsmPath+linkName)
info('Preparing SWF files',0)
if confirm('Do you want to update the swf files?') :
    urlObj = open(urlFile)
    urls = json.load(urlObj)
    for name in urls:
        url = urls[name]
        filePath = '{inputPath}{name}'.format(
              inputPath = inputPath
            , name = name
            )
        info('Download: {url} ==> {location}'.format(
            url = url,
            location = filePath
            ))
        download(url, filePath)

info('Cleaning '+tempPath, 0)
clean(tempPath)

info('Processing SWF files',0)
prompt = '''
    Flash Players get updated frequently, so the patches inside "patch"
    folder may be outdated and not suitable for the current version.
    Applying these patches can lead to all kinds of unpredictable bugs.
    Do you still want to proceed?
    '''
if not confirm(prompt):
    sys.exit()

for fileName in os.listdir(inputPath) :
    filePath = inputPath+fileName
    newFilePath = tempPath + fileName

    patchFile = patchPath + fileName + '.patch'

    shutil.copy(filePath, newFilePath)
    info(filePath +' copied to '+ newFilePath)
    abcFilePath = abcexport(newFilePath)
    info('Abc file created: ' + abcFilePath)

    opcodePath = rabcdasm(abcFilePath)
    info('Abc file Disassembled: '+ abcFilePath)

    if not patch(opcodePath, patchFile) == True:
        info('Failed to apply patch: '+ patchFile)
        os.remove(newFilePath)
        continue
    info('Patch applied: '+patchFile)

    newAbcFile = rabcasm(opcodePath)
    info('New abc file generated: '+newAbcFile)

    abcreplace(newFilePath, newAbcFile)
    info('SWF file generated: '+newFilePath)

    shutil.move(newFilePath, outputPath+fileName)
    info('SWF file move to output: '+newFilePath)

info('Replacing bin in SWF files',0)
for fileName in os.listdir(inputPath) :
    matches = re.search('^(.*)\.(\d+)\.replace\.swf$', fileName)
    if matches:
        swfFile = outputPath+matches.group(1)
        replaceFile = outputPath+fileName
        index = matches.group(2)
        info('Replacing {swfFile} ({index}): {replaceFile}'.format(
                swfFile = swfFile,
                index = index,
                replaceFile = replaceFile
            ))
        swfbinreplace(swfFile, index, replaceFile)

info('Cleaning '+tempPath, 0)
clean(tempPath)