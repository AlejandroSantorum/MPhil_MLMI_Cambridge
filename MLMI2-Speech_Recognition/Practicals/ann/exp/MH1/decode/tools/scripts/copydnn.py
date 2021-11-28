#!/usr/bin/env python3
# coding=utf-8
# author: cz277@cam.ac.uk

import sys
import argparse

cmdparser = argparse.ArgumentParser(description = 'Copy all DNN parameters with identical names between MMFs')
cmdparser.add_argument('-VERBOSE', '-v', help = 'Set logging level: ERROR (default), WARNING (-v), INFO (-vv), DEBUG (-vvv)', action = 'count', default = 0)
cmdparser.add_argument('-WORKDIR', help = 'Change to another work dir', type = str, action = 'store', default = None)
cmdparser.add_argument('-STEPID', help = 'Step id for logging', type = str, action = 'store', default = None)
cmdparser.add_argument('-BINARY', '-B', help = 'Output binary MMF', action = 'store_true', default = False)
cmdparser.add_argument('-EQUAL', help = 'Matrix/vectors need to be identical in size', action = 'store_true', default = False)
cmdparser.add_argument('SMMF', help = 'Input source MMF for parameter copying', type = str, action = 'store')
cmdparser.add_argument('TMMF', help = 'Input target MMF for parameter copying', type = str, action = 'store')
cmdparser.add_argument('OMMF', help = 'Output MMF', type = str, action = 'store')
cmdargs = cmdparser.parse_args()

import os
if cmdargs.WORKDIR != None: os.chdir(cmdargs.WORKDIR)
sys.path.append('%s/tools' % os.getcwd())
import pyhtk

# set step id and check each input arguments
pyhtk.setLoggingConfig(cmdargs.VERBOSE)
if cmdargs.STEPID is not None:
	pyhtk.setScriptStepID(cmdargs.STEPID)
pyhtk.checkInputFile(cmdargs.SMMF)
pyhtk.checkInputFile(cmdargs.TMMF)
pyhtk.checkOutputFile(cmdargs.OMMF)

# load the input MMFs and copy the parameters
shmmset = pyhtk.HTKModelReader(cmdargs.SMMF, '').getHiddenMarkovModelSet()
thmmset = pyhtk.HTKModelReader(cmdargs.TMMF, '').getHiddenMarkovModelSet()
pyhtk.copyMacroParameters('V', shmmset, thmmset, cmdargs.EQUAL)
pyhtk.copyMacroParameters('M', shmmset, thmmset, cmdargs.EQUAL)

# write out the MMF
pyhtk.HTKModelWriter(thmmset, cmdargs.OMMF, '', cmdargs.BINARY).writeModelSet(False)


