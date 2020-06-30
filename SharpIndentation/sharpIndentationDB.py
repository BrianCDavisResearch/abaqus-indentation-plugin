#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Copyright 2020 Brian C. Davis
#--------------------------------------------------------------------------------------------------

from abaqusGui import *
# from sharpIndentationIcons import plateData_Dep
import i18n

#-----------------------------------------------------------------------

class SharpIndentationModelDB(AFXDataDialog):

    #-----------------------------------------------------------------------

    def __init__(self,form):

        AFXDataDialog.__init__(self, form, i18n.tr('Sharp Indentation Model'), self.OK|self.APPLY|self.DEFAULTS|self.CANCEL)

        self.form = form

        AFXNote(self, i18n.tr('This is my custom plugin "Model Workbench".'))

        hf = FXHorizontalFrame(self, LAYOUT_FILL_X, 0,0,0,0, 0,0,0,0)

        import time

        gb = FXGroupBox(hf, i18n.tr('Time: %s'%(time.clock())), LAYOUT_FILL_Y|FRAME_GROOVE)
        va = AFXVerticalAligner(gb)

        FXCheckButton(va, 'This is checkbox #1', form.checkbox1)

        self.nameField = AFXTextField(va, 12, i18n.tr('Name:'), form.nameKw, 0)
        AFXTextField(va, 12, i18n.tr('Width (w):'), form.widthKw, 0)
        # AFXTextField(va, 12, i18n.tr('Height (h):'), form.heightKw, 0)
        # AFXTextField(va, 12, i18n.tr('Radius (r):'), form.radiusKw, 0)

        # gb = FXGroupBox(hf, i18n.tr('Diagram'), LAYOUT_FILL_Y|FRAME_GROOVE)
        # icon = FXXPMIcon(getAFXApp(), plateData_Dep) #ASCII image pulled here as "plateData_Dep"
        # FXLabel(gb, '', icon, pl=0, pr=0, pt=0, pb=0)

        # print >> sys.__stdout__, self

        # print >> sys.__stdout__, dir(self)

        return(None)

    def processUpdates(self):

        if self.form.checkbox1.getValue() == False:

            self.nameField.disable()

        else:

            self.nameField.enable()

        return(None)

    #-----------------------------------------------------------------------

#-----------------------------------------------------------------------

class SharpIndentationResultsDB(AFXDataDialog):

    #-----------------------------------------------------------------------

    def __init__(self, form):

        self.form = form

        AFXDataDialog.__init__(self, self.form, i18n.tr('Sharp Indentation Results'), self.OK|self.APPLY|self.DEFAULTS|self.CANCEL)

        tb = FXTabBook(self, tgt=None, sel=0, opts=TABBOOK_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)

        #-----------------------------------------------------------------------

        tb0 = FXTabItem(tb, i18n.tr('Output Scripts'), ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        vf1 = FXVerticalFrame(tb, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+7, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        gb1 = FXGroupBox(vf1, i18n.tr('ODB File Selection'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        hf1 = FXHorizontalFrame(gb1, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        AFXTextField(hf1, 39, '', tgt=self.form.odbPath, sel=0, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        fileDialog = FileDialogBox(self.form)
        FXButton(hf1, text=i18n.tr('Select File(s)'), tgt=fileDialog, sel=AFXMode.ID_ACTIVATE)

        gb2 = FXGroupBox(vf1, i18n.tr('Python Results Scripts'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        hf2 = FXHorizontalFrame(gb2, LAYOUT_FILL_X, 0,0,0,0, 0,0,0,0)
        tempText = i18n.tr('')
        self.boolWorkForceButton = FXCheckButton(hf2, tempText, tgt=None, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD+10, pb=DEFAULT_PAD)
        self.boolWorkForceButton.setCheck(state=True)
        self.boolWorkForceButton.disable()
        FXLabel(hf2, i18n.tr('Force and Work Energy vs. Displacement (Required)'), pl=DEFAULT_PAD-3, pr=DEFAULT_PAD, pt=DEFAULT_PAD+10, pb=DEFAULT_PAD)

        tempText = i18n.tr('Energy Summations (Whole Model "History")')
        self.boolEnergyButton = FXCheckButton(gb2, tempText, tgt=self.form.boolEnergy, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        tempText = i18n.tr('Orthogonal Normal Stress Profiles (centerline and surface)')
        self.boolOrthoStressButton = FXCheckButton(gb2, tempText, tgt=self.form.boolOrthoStress, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD+10, pb=DEFAULT_PAD)

        tempText = i18n.tr('Stress Invariants (centerline and surface)')
        self.boolInvStressButton = FXCheckButton(gb2, tempText, tgt=self.form.boolInvStress, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        tempText = i18n.tr('Densification: RD,DENSITY,PEQC4 (centerline and surface)')
        self.boolDensityButton = FXCheckButton(gb2, tempText, tgt=self.form.boolDensity, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        tempText = i18n.tr('Surface Topography')
        self.boolSurfTopButton = FXCheckButton(gb2, tempText, tgt=self.form.boolSurfTop, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD+10, pb=DEFAULT_PAD)

        tempText = i18n.tr('Indent Volumes')
        self.boolIndVolButton = FXCheckButton(gb2, tempText, tgt=self.form.boolIndVol, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        tempText = i18n.tr('Contact Forces')
        self.boolContVectButton = FXCheckButton(gb2, tempText, tgt=self.form.boolContVect, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        tempText = i18n.tr('Normalizer Variables')
        self.boolNormButton = FXCheckButton(gb2, tempText, tgt=self.form.boolNorm, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        tempText = i18n.tr('Stress Invariants (entire results-zone)')
        self.boolAreaInvariantsButton = FXCheckButton(gb2, tempText, tgt=self.form.boolAreaInvariants, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD+10, pb=DEFAULT_PAD)

        tempText = i18n.tr('S22, Lateral Crack Driving Stress (entire results-zone)')
        self.boolAreaS22Button = FXCheckButton(gb2, tempText, tgt=self.form.boolAreaS22, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        tempText = i18n.tr('Plastic Deformation (entire results-zone)')
        self.boolAreaPlasticButton = FXCheckButton(gb2, tempText, tgt=self.form.boolAreaPlastic, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        hf3 = FXHorizontalFrame(gb2, LAYOUT_FILL_X, 0,0,0,0, 0,0,0,0)
        FXLabel(hf3, i18n.tr('PE Limit'), pl=DEFAULT_PAD+20, pr=DEFAULT_PAD, pt=DEFAULT_PAD+3, pb=DEFAULT_PAD)
        self.limitPEField = AFXTextField(hf3, 10, '', tgt=self.form.limitPE, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.limitPEField.disable()

        #-----------------------------------------------------------------------

        tb2 = FXTabItem(tb, i18n.tr('Units'), ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        vf3 = FXVerticalFrame(tb, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+7, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        gb3 = FXGroupBox(vf3, i18n.tr('Base Units'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        FXLabel(gb3, i18n.tr('Mass -> milligram:     mg = kg*10^-6'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gb3, i18n.tr('Time -> millisecond:     ms = s*10^-3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gb3, i18n.tr('Length -> micrometer:     um = m*10^-6'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        gb4 = FXGroupBox(vf3, i18n.tr('Derrived Units'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        FXLabel(gb4, i18n.tr('Force -> microNewtons:     mg*um/ms^2 = N*10^-6 = uN'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gb4, i18n.tr('Pressure -> MegaPascals:     uN/um^2 = Pa*10^6 = MPa'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gb4, i18n.tr('Density -> milligram / micrometer^3:     mg/um^3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gb4, i18n.tr('Energy -> picoJoule:     uN*um = J*10^-12 = pJ'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        gb5 = FXGroupBox(vf3, i18n.tr('Density Conversions'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        FXLabel(gb5, i18n.tr('1 kg/m^3 = 1*10^-12 mg/um^3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gb5, i18n.tr('1 g/cm^3 = 1*10^-9 mg/um^3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        #-----------------------------------------------------------------------

        tb4 = FXTabItem(tb, i18n.tr('About'), ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        vf5 = FXVerticalFrame(tb, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+7, pt=DEFAULT_SPACING+5, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        gb7 = FXGroupBox(vf5, i18n.tr(''), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        FXLabel(gb7, i18n.tr('Author: Brian C. Davis'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gb7, i18n.tr('Institution: Colorado School of Mines'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gb7, i18n.tr('bridavis@mines.edu'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gb7, i18n.tr('brian.campbell.davis@gmail.com'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        #-----------------------------------------------------------------------

        return(None)

    #-----------------------------------------------------------------------

    def processUpdates(self):

        if self.boolAreaPlasticButton.getCheck() == True:

            self.limitPEField.enable()

        else:

            self.limitPEField.disable()

        return(None)

    #-----------------------------------------------------------------------

#-----------------------------------------------------------------------

class FileDialogBox(FXObject):

    #-----------------------------------------------------------------------

    def __init__(self, form):

        self.form = form

        FXObject.__init__(self)

        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, FileDialogBox.odbDialogBox)

        return(None)

    #-----------------------------------------------------------------------

    def odbDialogBox(self, sender, sel, ptr):

        tempDialog = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select an ODB File or Directory', self.form.odbPath, self.form.odbReadOnly, AFXSELECTFILE_MULTIPLE_ALL, 'Abaqus ODB Files (*.odb)', AFXIntTarget(0))

        tempDialog.create()

        tempDialog.showModal()

        return(None)

    #-----------------------------------------------------------------------

#-----------------------------------------------------------------------
