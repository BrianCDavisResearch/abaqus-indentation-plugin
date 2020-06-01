#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Brian C. Davis
#
#-----------------------------------------------------------------------

from abaqusGui import *
from sharpIndentationDB import SharpIndentationModelDB , SharpIndentationResultsDB
from sharpIndentationIcons import iconSharpIndentationModel , iconSharpIndentationResults
import i18n

#-----------------------------------------------------------------------

class SharpIndentationModel(AFXForm):

    def __init__(self, owner):

        AFXForm.__init__(self, owner)    

        self.cmd = AFXGuiCommand(self, 'default_system_units', 'LP_Indentation_Model')

        #-----------------------------------------------------------------------

        # AFXBoolKeyword(command, name, booleanType=ON_OFF, isRequired=False, defaultValue=False)
        self.checkbox1 = AFXBoolKeyword(self.cmd, 'testing', defaultValue=True)

        self.nameKw = AFXStringKeyword(self.cmd, 'name', TRUE)
        self.widthKw = AFXFloatKeyword(self.cmd, 'width', TRUE)
        # self.heightKw = AFXFloatKeyword(self.cmd, 'height', TRUE)
        # self.radiusKw = AFXFloatKeyword(self.cmd, 'radius', TRUE)

        return(None)

    #-----------------------------------------------------------------------

    def getFirstDialog(self):

        return(SharpIndentationModelDB(self))

    #-----------------------------------------------------------------------

#-----------------------------------------------------------------------

class SharpIndentationResults(AFXForm):

    def __init__(self, owner):

        AFXForm.__init__(self, owner)

        self.cmd = AFXGuiCommand(self, 'main', 'LP_Indentation_Output')

        #-----------------------------------------------------------------------

        self.nameKw = AFXStringKeyword(self.cmd, 'name', TRUE)
        self.widthKw = AFXFloatKeyword(self.cmd, 'width', TRUE)
        self.heightKw = AFXFloatKeyword(self.cmd, 'height', TRUE)
        self.radiusKw = AFXFloatKeyword(self.cmd, 'radius', TRUE)

        return(None)

    #-----------------------------------------------------------------------

    def getFirstDialog(self):

        return(SharpIndentationResultsDB(self))

    #-----------------------------------------------------------------------

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

import os

absPath = os.path.abspath(__file__)
absDir  = os.path.dirname(absPath)
helpUrl = os.path.join(absDir, 'plate-help.html')

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()

pluginDesc = i18n.tr('A very simple description...')
# pluginDesc = pluginDesc.replace("%ABSDIR%", absDir)

#-----------------------------------------------------------------------

modelIcon = FXXPMIcon(getAFXApp(), iconSharpIndentationModel)

toolset.registerGuiMenuButton(
    object=SharpIndentationModel(toolset), buttonText=i18n.tr('Sharp Indentation|Model: Pre-Processor'),
    kernelInitString='import LP_Indentation_Model', icon=modelIcon, version='0.1', author='Brian C. Davis',
    applicableModules = ['Part', 'Property', 'Assembly', 'Step', 'Interaction', 'Load', 'Mesh', 'Job'],
    description=pluginDesc, helpUrl=helpUrl)

toolset.registerGuiToolButton('Sharp Indentation',
    object=SharpIndentationModel(toolset), buttonText=i18n.tr('\tSharp Indentation\nBuild a Model'),
    kernelInitString='import LP_Indentation_Model', icon=modelIcon, version='0.1', author='Brian C. Davis',
    applicableModules = ['Part', 'Property', 'Assembly', 'Step', 'Interaction', 'Load', 'Mesh', 'Job'],
    description=pluginDesc, helpUrl=helpUrl)

#-----------------------------------------------------------------------

resultsIcon = FXXPMIcon(getAFXApp(), iconSharpIndentationOutput)

toolset.registerGuiMenuButton(
    object=SharpIndentationResults(toolset), buttonText=i18n.tr('Sharp Indentation|Results: Post-Processor'),
    kernelInitString='import LP_Indentation_Output', icon=resultsIcon, version='0.1', author='Brian C. Davis',
    applicableModules = ['Part', 'Property', 'Assembly', 'Step', 'Interaction', 'Load', 'Mesh', 'Job'],
    description=pluginDesc, helpUrl=helpUrl)

toolset.registerGuiToolButton('Sharp Indentation',
    object=SharpIndentationResults(toolset), buttonText=i18n.tr('\tSharp Indentation\nProcess Results'),
    kernelInitString='import LP_Indentation_Output', icon=resultsIcon, version='0.1', author='Brian C. Davis',
    applicableModules = ['Part', 'Property', 'Assembly', 'Step', 'Interaction', 'Load', 'Mesh', 'Job'],
    description=pluginDesc, helpUrl=helpUrl)

#-----------------------------------------------------------------------