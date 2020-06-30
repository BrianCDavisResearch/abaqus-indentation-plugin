#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Copyright 2020 Brian C. Davis
#--------------------------------------------------------------------------------------------------

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

    #-----------------------------------------------------------------------

    def __init__(self, owner):

        AFXForm.__init__(self, owner)

        self.cmd = AFXGuiCommand(self, 'plugin_prescript', 'LP_Indentation_Results')

        self.odbPath = AFXStringKeyword(self.cmd, 'odbPath', isRequired=True, defaultValue=None)
        self.odbReadOnly = AFXBoolKeyword(self.cmd, 'odbReadOnly', isRequired=True, defaultValue=True)

        self.boolEnergy = AFXBoolKeyword(self.cmd, 'boolEnergy', isRequired=True, defaultValue=True)

        self.boolOrthoStress = AFXBoolKeyword(self.cmd, 'boolOrthoStress', isRequired=True, defaultValue=True)
        self.boolInvStress = AFXBoolKeyword(self.cmd, 'boolInvStress', isRequired=True, defaultValue=True)
        self.boolDensity = AFXBoolKeyword(self.cmd, 'boolDensity', isRequired=True, defaultValue=True)

        self.boolSurfTop = AFXBoolKeyword(self.cmd, 'boolSurfTop', isRequired=True, defaultValue=True)
        self.boolIndVol = AFXBoolKeyword(self.cmd, 'boolIndVol', isRequired=True, defaultValue=True)
        self.boolContVect = AFXBoolKeyword(self.cmd, 'boolContVect', isRequired=True, defaultValue=True)
        self.boolNorm = AFXBoolKeyword(self.cmd, 'boolNorm', isRequired=True, defaultValue=True)

        self.boolAreaInvariants = AFXBoolKeyword(self.cmd, 'boolAreaInvariants', isRequired=True, defaultValue=False)
        self.boolAreaS22 = AFXBoolKeyword(self.cmd, 'boolAreaS22', isRequired=True, defaultValue=False)
        self.boolAreaPlastic = AFXBoolKeyword(self.cmd, 'boolAreaPlastic', isRequired=True, defaultValue=False)
        self.limitPE = AFXFloatKeyword(self.cmd, 'limitPE', isRequired=True, defaultValue=1e-05)

        return(None)

    #-----------------------------------------------------------------------

    def getFirstDialog(self):

        return(SharpIndentationResultsDB(self))

    #-----------------------------------------------------------------------

#-----------------------------------------------------------------------

import os

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()

#-----------------------------------------------------------------------
# Registration of GUI Menu Buttons and GUI Toolbox Buttons
#-----------------------------------------------------------------------

pluginDesc = i18n.tr('A very simple description...') #################################
# pluginDesc = pluginDesc.replace("%ABSDIR%", absDir)

absPath = os.path.abspath(__file__) ################################
absDir  = os.path.dirname(absPath) ################################
helpUrl = os.path.join(absDir, 'plate-help.html') #link to YouTube account? ################################

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

resultsIcon = FXXPMIcon(getAFXApp(), iconSharpIndentationResults)

toolset.registerGuiMenuButton(
    object=SharpIndentationResults(toolset), buttonText=i18n.tr('Sharp Indentation|Results: Post-Processor'),
    kernelInitString='import LP_Indentation_Results', icon=resultsIcon, version='0.1', author='Brian C. Davis',
    applicableModules = ['Part', 'Property', 'Assembly', 'Step', 'Interaction', 'Load', 'Mesh', 'Job'],
    description=pluginDesc, helpUrl=helpUrl)

toolset.registerGuiToolButton('Sharp Indentation',
    object=SharpIndentationResults(toolset), buttonText=i18n.tr('\tSharp Indentation\nProcess Results'),
    kernelInitString='import LP_Indentation_Results', icon=resultsIcon, version='0.1', author='Brian C. Davis',
    applicableModules = ['Part', 'Property', 'Assembly', 'Step', 'Interaction', 'Load', 'Mesh', 'Job'],
    description=pluginDesc, helpUrl=helpUrl)

#-----------------------------------------------------------------------