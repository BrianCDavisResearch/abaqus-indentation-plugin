#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Brian C. Davis
#
#-----------------------------------------------------------------------

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

#-----------------------------------------------------------------------

class SharpIndentationResultsDB(AFXDataDialog): #This is the gui window, it looks like all variables are attributes of "form"

    #-----------------------------------------------------------------------

    def __init__(self, form):

        AFXDataDialog.__init__(self, form, i18n.tr('Sharp Indentation Output'), self.OK|self.APPLY|self.DEFAULTS|self.CANCEL)
                              
        AFXNote(self, i18n.tr('This is my custom plugin "Output Workbench".'))                              

        hf = FXHorizontalFrame(self, LAYOUT_FILL_X, 0,0,0,0, 0,0,0,0)

        import time

        gb = FXGroupBox(hf, i18n.tr('Parameters %s'%(time.clock())), LAYOUT_FILL_Y|FRAME_GROOVE)
        va = AFXVerticalAligner(gb)
        AFXTextField(va, 12, i18n.tr('Name:'), form.nameKw, 0)
        AFXTextField(va, 12, i18n.tr('Width (w):'), form.widthKw, 0)
        AFXTextField(va, 12, i18n.tr('Height (h):'), form.heightKw, 0)
        AFXTextField(va, 12, i18n.tr('Radius (r):'), form.radiusKw, 0)

        gb = FXGroupBox(hf, i18n.tr('Diagram'), LAYOUT_FILL_Y|FRAME_GROOVE)
        icon = FXXPMIcon(getAFXApp(), plateData_Dep) #ASCII image pulled here as "plateData_Dep"
        FXLabel(gb, '', icon, pl=0, pr=0, pt=0, pb=0)

        return(None)

    #-----------------------------------------------------------------------

#-----------------------------------------------------------------------