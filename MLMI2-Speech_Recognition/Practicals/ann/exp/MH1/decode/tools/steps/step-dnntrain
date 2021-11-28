#!/usr/bin/env python3
# coding=utf-8

############################################################
# Step3: mono-/xwtri- state target ANN-HMMs training
############################################################

import sys
import argparse

cmdparser = argparse.ArgumentParser(description = 'DNN training step setup stage')
cmdparser.add_argument('-VERBOSE', '-v', help = 'Set logging level: ERROR (default), WARNING (-v), INFO (-vv), DEBUG (-vvv)', action = 'count', default = 0)
cmdparser.add_argument('-TOOLS', '-TOOLSDIR', help = 'Use specified dir rather than default TIMITTOOLS', type = str, action = 'store', default = None)
cmdparser.add_argument('-GPUID', help = 'Specify the GPU id (otherwise use CPU training)', type = int, action = 'store', default = None)
cmdparser.add_argument('-MODELINI', help = 'Input model config ini file', type = str, action = 'store', default = None)
cmdparser.add_argument('SYS', help = 'Input system environment file', type = str, action = 'store')
cmdparser.add_argument('MLF', help = 'Input MLF file path', type = str, action = 'store')
cmdparser.add_argument('HMM', help = 'Input HMM model macro file', type = str, action = 'store')
cmdparser.add_argument('LST', help = 'Input HMM model list file', type = str, action = 'store')
cmdparser.add_argument('TGT', help = 'Output target dirs file', type = str, action = 'store')
cmdargs = cmdparser.parse_args()

import os.path
if cmdargs.TOOLS is not None:
	sys.path.append(os.path.abspath(cmdargs.TOOLS))
else:
	sys.path.append('%s/../' % os.path.abspath(os.path.split(sys.argv[0])[0]))
import pyhtk
import subprocess

# set step id
pyhtk.setLoggingConfig(cmdargs.VERBOSE)
pyhtk.setScriptStepID(sys.argv[0])
# check input & setup output
startdir = pyhtk.getCurrentDir()
if cmdargs.TOOLS is not None:
	pyhtk.checkInputDir(cmdargs.TOOLS)
	if not pyhtk.checkIsAbsPath(cmdargs.TOOLS): cmdargs.TOOLS = pyhtk.joinPaths(pyhtk.getCurrentDir(), cmdargs.TOOLS)
if cmdargs.MODELINI is not None:
	pyhtk.checkInputFile(cmdargs.MODELINI)
	if not pyhtk.checkIsAbsPath(cmdargs.MODELINI): cmdargs.MODELINI = pyhtk.joinPaths(pyhtk.getCurrentDir(), cmdargs.MODELINI)
pyhtk.checkInputFile(cmdargs.SYS)
if not pyhtk.checkIsAbsPath(cmdargs.SYS):
	cmdargs.SYS = pyhtk.joinPaths(pyhtk.getCurrentDir(), cmdargs.SYS)
pyhtk.checkInputFile(cmdargs.MLF)
if not pyhtk.checkIsAbsPath(cmdargs.MLF):
	cmdargs.MLF = pyhtk.joinPaths(pyhtk.getCurrentDir(), cmdargs.MLF)
pyhtk.checkInputFile(cmdargs.HMM)
if not pyhtk.checkIsAbsPath(cmdargs.HMM):
	cmdargs.HMM = pyhtk.joinPaths(pyhtk.getCurrentDir(), cmdargs.HMM)
pyhtk.checkInputFile(cmdargs.LST)
if not pyhtk.checkIsAbsPath(cmdargs.LST):
	cmdargs.LST = pyhtk.joinPaths(pyhtk.getCurrentDir(), cmdargs.LST)
#if not pyhtk.checkIsAbsPath(cmdargs.TGT): cmdargs.TGT = pyhtk.joinPaths(pyhtk.getCurrentDir(), cmdargs.TGT)
pyhtk.checkOutputDir(cmdargs.TGT, False)
# cache the commands
pyhtk.cacheCommand(sys.argv, cmdargs.TGT)
# change current dir
pyhtk.changeDir(cmdargs.TGT)

# a temporary solution to define the paths of the tools & scripts
HHED = 'tools/htkbin/HHEd'
HNTRAINSGD = 'tools/htkbin/HNTrainSGD'
if cmdargs.GPUID is not None: HNTRAINSGD = 'tools/htkbin/HNTrainSGD.GPU'
COPYDNN = 'tools/scripts/copydnn.py'
if pyhtk.checkExists('/opt/intel/composerxe/bin/compilervars.csh'):
	os.system('source /opt/intel/composerxe/bin/compilervars.csh intel64')
	#pyhtk.exe('source /opt/intel/composerxe/bin/compilervars.csh intel64')

# load sys file variables
syslines = pyhtk.parseShellBLE(cmdargs.SYS)
pyhtk.writeOneTextFile(syslines, 'sys.ini', True)
htesys = pyhtk.HTEArgsIniReader('sys.ini')
htesys.parseHTEIniFile()
sysargs = htesys.getArgs()
if sysargs.FEATYPE.startswith('mfc'):
	sysargs.includeOneArg('FEAKIND', 'MFCC' + sysargs.FEADIFF)
elif sysargs.FEATYPE.startswith('plp'):
	sysargs.includeOneArg('FEAKIND', 'PLP' + sysargs.FEADIFF)
elif sysargs.FEATYPE.startswith('fbk'):
	sysargs.includeOneArg('FEAKIND', 'FBANK' + sysargs.FEADIFF)
else:
	pyhtk.printError('Unknown feature type %s' % sysargs.FEATYPE)
if cmdargs.MODELINI is None:
	cmdargs.MODELINI = pyhtk.joinPaths(startdir, '../tools/htefiles/DNN-7L.ReLU.%s.ini' % sysargs.FEAKIND)
	#cmdargs.MODELINI = pyhtk.joinPaths(startdir, '../tools/htefiles/DNN-7L.sigmoid.%s.ini' % sysargs.FEAKIND)

# copy the resourcs
if cmdargs.TOOLS is None:
	cmdargs.TOOLS = sysargs.TIMITTOOLS
pyhtk.slinkItem(cmdargs.TOOLS, 'tools')
pyhtk.slinkItem(sysargs.TIMITLIB, 'lib')
pyhtk.copyItem(cmdargs.SYS, 'environment')
pyhtk.copyItem('lib/cfgs/basic%s.cfg' % sysargs.FEADIFF, 'basic.cfg')
pyhtk.copyItem(cmdargs.MLF, 'train.mlf')
pyhtk.copyItem(cmdargs.HMM, 'proto/work/MMF')
pyhtk.copyItem(cmdargs.LST, 'hmms.mlist')

# setup the initial model
def genHMMSetProtoFromIni(inipath, cfgpath, protodir, workdir):
	pyhtk.printMessage('Generate proto: %s -> %s/MMF' % (inipath, protodir))
	# check if input feature type from setup stage and ini files are consistent
	def checkInputObs(inipath, someobs, someargs):
		if someobs.getInputObservationType() != someargs.FEAKIND or someobs.getInputObservationDim(0) != int(someargs.FEADIM):
			pyhtk.printError('Feature kind or dim in %s not match to the setup stage' % inipath)
	# load training args from ini
	[cfgargs, setdict] = pyhtk.HTKConfigIniReader(inipath).parseNeuralNetFrameTraining()
	curargs = pyhtk.HTEArgs(sysargs).includeArgs(cfgargs).includeArgs(cmdargs)
	# write config file
	cfglines = pyhtk.convertDict2Assgin(setdict)
	if curargs.GPUID is not None: cfglines.append('GPUID = %s' % curargs.GPUID)
	pyhtk.writeOneTextFile(cfglines, cfgpath, False)
	# produce model definition args from ini and write NMF file
	hmmset = pyhtk.HTKModelIniReader(inipath).getHiddenMarkovModelSet()
	checkInputObs(curargs.MODELINI, hmmset.getHMMInputObservation(), sysargs)
	pyhtk.HTKModelWriter(hmmset, '%s/NMF' % workdir, '', False).writeModelSet(True)
	# get layer list
	curargs.includeOneArg('LAYERNAMES', sorted(hmmset.getLayerTable().keys()))
	curargs.includeOneArg('LAYERTABLE', sorted(hmmset.getLayerTable()))
	# write hed file for connection and run HHEd
	pyhtk.writeOneTextFile(['SW 1 %s' % sysargs.FEADIM, 'SK %s' % sysargs.FEAKIND, 'CH %s/NMF /dev/null %s <HYBRID>' % (workdir, hmmset.getNeuralNetOutputLayer().getFullName())], '%s/connect.hed' % protodir, False)
	pyhtk.exe('%s -B -A -D -V -T 1 -H %s -M %s %s %s' % (HHED, 'proto/work/MMF', protodir, '%s/connect.hed' % protodir, 'hmms.mlist'), '%s/LOG' % protodir)
	return curargs
#     randomly initialise one NMF
def initNMFRandomly(curargs, protodir, initdir):
	pyhtk.printMessage('Random initialisation: %s -> %s' % ('%s/MMF' % protodir, '%s/MMF' % initdir))
	inittype = curargs.INITIALISATION.split('RANDOM:')[-1]
	if inittype == 'HHED':
		hedlines = []
		for eachname in curargs.LAYERNAMES:
			hedlines.append('EL ~L "%s"' % eachname)
		pyhtk.writeOneTextFile(hedlines, '%s/randinit.hed' % initdir, False)
		pyhtk.exe('%s -B -A -D -V -T 1 -H %s -M %s %s %s' % (HHED, '%s/MMF' % protodir, initdir, '%s/randinit.hed' % initdir, 'hmms.mlist'), '%s/LOG' % initdir)
	else:
		for eachname in curargs.LAYERNAMES:
			pyhtk.randomiseOneLayer(curargs.LAYERTABLE[eachname], inittype)
#     generate one HNTrainSGD command
def genCommandHNTrainSGD(curargs, traincfg, indir, outdir):
	options = [HNTRAINSGD, '-B -A -D -V -T 3', '-C basic.cfg', '-C %s' % traincfg]
	options.append('-S lib/flists/dnn.train.scp')
	options.append('-N lib/flists/dnn.cv.scp')
	options.append('-l LABEL')
	options.append('-I train.mlf')
	options.append('-H %s/MMF' % indir)
	if pyhtk.checkExists('%s/UPDATE' % indir): options.append('-H %s/UPDATE' % indir)
	options.append('-M %s' % outdir)
	options.append('hmms.mlist')
	options.append('> %s/LOG' % outdir)
	return ' '.join(options)

# get finetune args
pyhtk.printMessage('Generate init model for finetuning')
ftargs = genHMMSetProtoFromIni(cmdargs.MODELINI, 'finetune.cfg', 'proto', 'proto/work')

# get pretrain args
argslist = []
# to pretrain according to HTE ini file(s) initialisation field(s)
if not ftargs.INITIALISATION.startswith('RANDOM:'):
	pyhtk.printMessage('Generate init models for pretraining')
	inilist = []
	inipath = ftargs.INITIALISATION
	pyhtk.printDebug('Back trace pretraining HTE files')
	while not inipath.startswith('RANDOM:'):
		if not pyhtk.checkIsAbsPath(inipath): inipath = pyhtk.joinPaths(startdir, inipath)
		inilist.insert(0, inipath)
		[cfgargs, setdict] = pyhtk.HTKConfigIniReader(inipath).parseNeuralNetFrameTraining()
		inipath = cfgargs.INITIALISATION
	for idx in range(0, len(inilist)):
		curargs = genHMMSetProtoFromIni(inilist[idx], 'pretrain%d.cfg' % idx, 'pretrain/hmm%d/init/work' % idx, 'pretrain/hmm%d/init/work' % idx)
		argslist.append(curargs)
	for idx in range(0, len(argslist)):
		argslist[idx].INITIALISATION = argslist[0].INITIALISATION
		initNMFRandomly(argslist[idx], 'pretrain/hmm%d/init/work' % idx, 'pretrain/hmm%d/init' % idx)
	# set the random initialisation scheme
	ftargs.INITIALISATION = argslist[-1].INITIALISATION

# randomly initialise hmm0/init/work/MMF
initNMFRandomly(ftargs, 'proto', 'hmm0/init/work')

# do the pretraing
if len(argslist) > 0: pyhtk.printMessage('Proceed pretraining commands')
for idx in range(0, len(argslist)):
	curdir = 'pretrain/hmm%d' % idx
	cmdlines = []
	if idx != 0:
		pyhtk.exe('%s -vv -STEPID %s -BINARY -EQUAL %s/MMF %s/init/MMF %s/init/MMF' % (COPYDNN, pyhtk.getScriptStepID(), 'pretrain/hmm%d' % (idx - 1), curdir, curdir))
	pyhtk.exe(genCommandHNTrainSGD(argslist[idx], 'pretrain%d.cfg' % idx, '%s/init' % curdir, curdir))


# do the finetuning
pyhtk.printMessage('Proceed finetuning')
if not pyhtk.checkExists('hmm0/init/MMF'):
	if len(argslist) != 0:
		pyhtk.exe('%s -vv -STEPID %s -BINARY -EQUAL pretrain/hmm%d/MMF hmm0/init/work/MMF hmm0/init/MMF' % (COPYDNN, pyhtk.getScriptStepID(), len(argslist) - 1))
	else:
		pyhtk.slinkItem('hmm0/init/work/MMF', 'hmm0/init/MMF')
	pyhtk.exe(genCommandHNTrainSGD(ftargs, 'finetune.cfg', 'hmm0/init', 'hmm0'))
	
