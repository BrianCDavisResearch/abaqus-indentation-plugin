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

        self.cmd = AFXGuiCommand(self, 'plugin_prescript', 'LP_Indentation_Model')

        #-----------------------------------------------------------------------

        self.anSolverType = AFXStringKeyword(self.cmd, 'anSolverType', isRequired=True, defaultValue='Standard - Quasi-Static')

        self.bcIndDepth = AFXFloatKeyword(self.cmd, 'bcIndDepth', isRequired=True, defaultValue=3.0)
        self.contFriciton = AFXFloatKeyword(self.cmd, 'contFriciton', isRequired=True, defaultValue=0.0)

        self.outpFieldInt = AFXIntKeyword(self.cmd, 'outpFieldInt', isRequired=True, defaultValue=50)
        self.outpHistInt = AFXIntKeyword(self.cmd, 'outpHistInt', isRequired=True, defaultValue=50)

        self.meshDivider = AFXIntKeyword(self.cmd, 'meshDivider', isRequired=True, defaultValue=50)
        self.partTaScale = AFXIntKeyword(self.cmd, 'partTaScale', isRequired=True, defaultValue=1)

        self.meshRemeshing1 = AFXIntKeyword(self.cmd, 'meshRemeshing1', isRequired=True, defaultValue=1)
        self.meshRemeshing2 = AFXIntKeyword(self.cmd, 'meshRemeshing2', isRequired=True, defaultValue=2)

        self.anJobName = AFXStringKeyword(self.cmd, 'anJobName', isRequired=True, defaultValue='Sharp_Indentation_Plugin')
        self.anCPUs = AFXIntKeyword(self.cmd, 'anCPUs', isRequired=True, defaultValue=4)

        self.partIndDAngle = AFXFloatKeyword(self.cmd, 'partIndDAngle', isRequired=True, defaultValue=70.3)
        self.partIndFlat = AFXFloatKeyword(self.cmd, 'partIndFlat', isRequired=True, defaultValue=0.0)
        self.partIndRadius = AFXFloatKeyword(self.cmd, 'partIndRadius', isRequired=True, defaultValue=0.0)

        self.anRerunCSV = AFXBoolKeyword(self.cmd, 'anRerunCSV', isRequired=True, defaultValue=False)
        self.anRerunCSVfileName = AFXStringKeyword(self.cmd, 'anRerunCSVfileName', isRequired=True, defaultValue='')
        self.anRerunCSVfileNameReadOnly = AFXBoolKeyword(self.cmd, 'anRerunCSVfileNameReadOnly', isRequired=False, defaultValue=True)

        #-----------------------------------------------------------------------

        self.partIndType = AFXStringKeyword(self.cmd, 'partIndType', isRequired=True, defaultValue='Rigid')

        self.matIndNamePre = AFXStringKeyword(self.cmd, 'matIndNamePre', isRequired=False, defaultValue='Diamond')
        self.matIndName = AFXStringKeyword(self.cmd, 'matIndName', isRequired=True, defaultValue='Diamond')
        self.matIndEYM = AFXFloatKeyword(self.cmd, 'matIndEYM', isRequired=True, defaultValue=1050e3)
        self.matIndEPR = AFXFloatKeyword(self.cmd, 'matIndEPR', isRequired=True, defaultValue=0.20)
        self.matIndDensity = AFXFloatKeyword(self.cmd, 'matIndDensity', isRequired=True, defaultValue=3.52e-9)

        self.matTaName = AFXStringKeyword(self.cmd, 'matTaName', isRequired=True, defaultValue='Fused_Silica')
        self.matTaEYM = AFXFloatKeyword(self.cmd, 'matTaEYM', isRequired=True, defaultValue=70.0e3)
        self.matTaEPR = AFXFloatKeyword(self.cmd, 'matTaEPR', isRequired=True, defaultValue=0.15)
        self.matTaDensity = AFXFloatKeyword(self.cmd, 'matTaDensity', isRequired=True, defaultValue=2.20e-9)

        self.matTaPsModel = AFXStringKeyword(self.cmd, 'matTaPsModel', isRequired=True, defaultValue='von Mises')

        self.matTaPsVM = AFXFloatKeyword(self.cmd, 'matTaPsVM', isRequired=True, defaultValue=7.50e3)
        self.matTaPsGTNrd = AFXFloatKeyword(self.cmd, 'matTaPsGTNrd', isRequired=True, defaultValue=0.85)
        self.matTaPsGTNq1 = AFXFloatKeyword(self.cmd, 'matTaPsGTNq1', isRequired=True, defaultValue=0.90)
        self.matTaPsGTNq2 = AFXFloatKeyword(self.cmd, 'matTaPsGTNq2', isRequired=True, defaultValue=0.90)

        self.matTaPsDPCap0 = AFXFloatKeyword(self.cmd, 'matTaPsDPCap0', isRequired=True, defaultValue=5500.0)
        self.matTaPsDPCap1 = AFXFloatKeyword(self.cmd, 'matTaPsDPCap1', isRequired=True, defaultValue=10.0)
        self.matTaPsDPCap2 = AFXFloatKeyword(self.cmd, 'matTaPsDPCap2', isRequired=True, defaultValue=0.85)
        self.matTaPsDPCap3 = AFXFloatKeyword(self.cmd, 'matTaPsDPCap3', isRequired=True, defaultValue=0.0)
        self.matTaPsDPCap4 = AFXFloatKeyword(self.cmd, 'matTaPsDPCap4', isRequired=True, defaultValue=0.01)
        self.matTaPsDPCap5 = AFXFloatKeyword(self.cmd, 'matTaPsDPCap5', isRequired=True, defaultValue=1.0)

        self.matTaPsKerm1 = AFXFloatKeyword(self.cmd, 'matTaPsKerm1', isRequired=True, defaultValue=6500.0)
        self.matTaPsKerm2 = AFXFloatKeyword(self.cmd, 'matTaPsKerm2', isRequired=True, defaultValue=-11500.0)
        self.matTaPsKerm3 = AFXFloatKeyword(self.cmd, 'matTaPsKerm3', isRequired=True, defaultValue=100000.0)

        self.matTaPsMoln1 = AFXFloatKeyword(self.cmd, 'matTaPsMoln1', isRequired=True, defaultValue=5.0)
        self.matTaPsMoln2 = AFXFloatKeyword(self.cmd, 'matTaPsMoln2', isRequired=True, defaultValue=5700.0)
        self.matTaPsMoln3 = AFXFloatKeyword(self.cmd, 'matTaPsMoln3', isRequired=True, defaultValue=5000.0)
        self.matTaPsMoln4 = AFXFloatKeyword(self.cmd, 'matTaPsMoln4', isRequired=True, defaultValue=-3000.0)
        self.matTaPsMoln5 = AFXFloatKeyword(self.cmd, 'matTaPsMoln5', isRequired=True, defaultValue=-0.196)
        self.matTaPsMoln6 = AFXFloatKeyword(self.cmd, 'matTaPsMoln6', isRequired=True, defaultValue=3.0)
        self.matTaPsMoln7 = AFXFloatKeyword(self.cmd, 'matTaPsMoln7', isRequired=True, defaultValue=4.0)
        self.matTaPsMoln8 = AFXFloatKeyword(self.cmd, 'matTaPsMoln8', isRequired=True, defaultValue=-20000.0)
        self.matTaPsMoln9 = AFXFloatKeyword(self.cmd, 'matTaPsMoln9', isRequired=True, defaultValue=7000.0)

        self.anFortranfileName = AFXStringKeyword(self.cmd, 'anFortranfileName', isRequired=True, defaultValue='')
        self.anFortranReadOnly = AFXBoolKeyword(self.cmd, 'anFortranReadOnly', isRequired=False, defaultValue=True)

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
        self.boolAreaS22limitPE = AFXFloatKeyword(self.cmd, 'boolAreaS22limitPE', isRequired=True, defaultValue=2e-03)
        self.boolAreaS22limit = AFXFloatKeyword(self.cmd, 'boolAreaS22limit', isRequired=True, defaultValue=50.0)
        self.boolAreaPlastic = AFXBoolKeyword(self.cmd, 'boolAreaPlastic', isRequired=True, defaultValue=False)
        self.boolAreaPlasticlimitPE = AFXFloatKeyword(self.cmd, 'boolAreaPlasticlimitPE', isRequired=True, defaultValue=1e-05)

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
helpUrl = os.path.join(absDir, 'plate-help.html') #link to YouTube account? Yes! ################################

modelIcon = FXXPMIcon(getAFXApp(), iconSharpIndentationModel)

toolset.registerGuiMenuButton(
    object=SharpIndentationModel(toolset), buttonText=i18n.tr('Sharp Indentation|Model: Pre-Processor'),
    kernelInitString='import LP_Indentation_Model', icon=modelIcon, version='0.1', author='Brian C. Davis',
    applicableModules = ['Part', 'Property', 'Assembly', 'Step', 'Interaction', 'Load', 'Mesh', 'Optimization','Job','Visualization','Sketch'],
    description=pluginDesc, helpUrl=helpUrl)

toolset.registerGuiToolButton('Sharp Indentation',
    object=SharpIndentationModel(toolset), buttonText=i18n.tr('\tSharp Indentation\nBuild a Model'),
    kernelInitString='import LP_Indentation_Model', icon=modelIcon, version='0.1', author='Brian C. Davis',
    applicableModules = ['Part', 'Property', 'Assembly', 'Step', 'Interaction', 'Load', 'Mesh', 'Optimization','Job','Visualization','Sketch'],
    description=pluginDesc, helpUrl=helpUrl)

#-----------------------------------------------------------------------

resultsIcon = FXXPMIcon(getAFXApp(), iconSharpIndentationResults)

toolset.registerGuiMenuButton(
    object=SharpIndentationResults(toolset), buttonText=i18n.tr('Sharp Indentation|Results: Post-Processor'),
    kernelInitString='import LP_Indentation_Results', icon=resultsIcon, version='0.1', author='Brian C. Davis',
    applicableModules = ['Part', 'Property', 'Assembly', 'Step', 'Interaction', 'Load', 'Mesh', 'Optimization','Job','Visualization','Sketch'],
    description=pluginDesc, helpUrl=helpUrl)

toolset.registerGuiToolButton('Sharp Indentation',
    object=SharpIndentationResults(toolset), buttonText=i18n.tr('\tSharp Indentation\nProcess Results'),
    kernelInitString='import LP_Indentation_Results', icon=resultsIcon, version='0.1', author='Brian C. Davis',
    applicableModules = ['Part', 'Property', 'Assembly', 'Step', 'Interaction', 'Load', 'Mesh', 'Optimization','Job','Visualization','Sketch'],
    description=pluginDesc, helpUrl=helpUrl)

#-----------------------------------------------------------------------