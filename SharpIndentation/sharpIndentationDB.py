#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Copyright 2020 Brian C. Davis
#--------------------------------------------------------------------------------------------------

from abaqusGui import *
from sharpIndentationIcons import iconIndenterGeometry
import i18n

#-----------------------------------------------------------------------

class SharpIndentationModelDB(AFXDataDialog):

    #-----------------------------------------------------------------------

    def __init__(self,form):

        self.form = form

        AFXDataDialog.__init__(self, self.form, i18n.tr('Sharp Indentation Model'), self.OK|self.APPLY|self.DEFAULTS|self.CANCEL)

        tb = FXTabBook(self, tgt=None, sel=0, opts=TABBOOK_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)

        #-----------------------------------------------------------------------

        tb0 = FXTabItem(tb, i18n.tr('Model Inputs'), ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        hfModel_0 = FXHorizontalFrame(tb, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+5, pt=DEFAULT_SPACING+5, pb=DEFAULT_SPACING+5, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        #-----------------------------------------------------------------------

        vfModel_1 = FXVerticalFrame(hfModel_0, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        gbModel_11 = FXGroupBox(vfModel_1, i18n.tr('Analysis Type'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        comboBox = AFXComboBox(gbModel_11, 0, 3, '', tgt=self.form.anType, sel=0, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        comboBox.appendItem('Standard - Static')
        comboBox.appendItem('Standard - Quasi-Static')
        comboBox.appendItem('Explicit - Mass Scaling')
        gbModel_11.setLayoutHints(LAYOUT_FILL_X)

        hfModel_21 = FXHorizontalFrame(vfModel_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        gbModel_211 = FXGroupBox(hfModel_21, i18n.tr('Boundary Conditions'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vaModel_211 = AFXVerticalAligner(gbModel_211, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        AFXTextField(vaModel_211, 7, 'Indenter Depth', tgt=self.form.bcIndDepth, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        AFXTextField(vaModel_211, 7, 'Contact Friction', tgt=self.form.contFriciton, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        gbModel_111 = FXGroupBox(hfModel_21, i18n.tr('Results Intervals'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vaModel1 = AFXVerticalAligner(gbModel_111, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        AFXTextField(vaModel1, 4, 'Field', tgt=self.form.outpFieldInt, sel=0, opts=AFXTEXTFIELD_INTEGER, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        AFXTextField(vaModel1, 4, 'History', tgt=self.form.outpHistInt, sel=0, opts=AFXTEXTFIELD_INTEGER, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        # vaModel1.setLayoutHints(LAYOUT_FILL_X)

        hfModel_11 = FXHorizontalFrame(vfModel_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        gbModel_212 = FXGroupBox(hfModel_11, i18n.tr('Advanced Options'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vaModel_212 = AFXVerticalAligner(gbModel_212, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        AFXTextField(vaModel_212, 4, 'Mesh Refinement', tgt=self.form.meshDivider, sel=0, opts=AFXTEXTFIELD_INTEGER, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        AFXTextField(vaModel_212, 4, 'Test Article Scale', tgt=self.form.partTaScale, sel=0, opts=AFXTEXTFIELD_INTEGER, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        self.remesh0 = FXGroupBox(hfModel_11, i18n.tr('Adaptive Remeshing'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vaModel_112 = AFXVerticalAligner(self.remesh0, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        self.remesh1 = AFXTextField(vaModel_112, 4, 'Frequency', tgt=self.form.meshRemeshing1, sel=0, opts=AFXTEXTFIELD_INTEGER, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.remesh2 = AFXTextField(vaModel_112, 4, 'Sweeps', tgt=self.form.meshRemeshing2, sel=0, opts=AFXTEXTFIELD_INTEGER, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        gbModel_113 = FXGroupBox(vfModel_1, i18n.tr('Job Name and Parallelization'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        AFXTextField(gbModel_113, 40, '', tgt=self.form.anJobName, sel=0, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        AFXTextField(gbModel_113, 4, 'Parallel CPUs', tgt=self.form.anCPUs, sel=0, opts=AFXTEXTFIELD_INTEGER, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        gbModel_113.setLayoutHints(LAYOUT_FILL_X)

        #-----------------------------------------------------------------------

        vfModel_2 = FXVerticalFrame(hfModel_0, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        gbModel_213 = FXGroupBox(vfModel_2, i18n.tr('Indenter Geometry'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        hfModel_22 = FXHorizontalFrame(gbModel_213, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vaModel_213 = AFXVerticalAligner(hfModel_22, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING+5)
        AFXTextField(vaModel_213, 7, 'Phi: Demi-Angle (deg)', tgt=self.form.partIndDAngle, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        AFXTextField(vaModel_213, 7, 'Ri: Tip-Radius (um)', tgt=self.form.partIndRadius, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        AFXTextField(vaModel_213, 7, 'Rf: Tip-Flat (um)', tgt=self.form.partIndFlat, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        vaModel_213.setLayoutHints(LAYOUT_CENTER_Y)

        # import os
        # tempIcon = afxCreatePNGIcon('%s\\abaqus_plugins\\SharpIndentation\\icon_Model.png' %(os.path.expanduser('~')))
        tempIcon = FXXPMIcon(getAFXApp(), iconIndenterGeometry)
        FXLabel(hfModel_22, '', tempIcon)

        self.gbModel_214 = FXGroupBox(vfModel_2, i18n.tr('Build Model from "All-Inputs" CSV file'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        self.hfModel_215 = FXHorizontalFrame(self.gbModel_214, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        self.anRerunCSVButton = FXCheckButton(self.hfModel_215, '', tgt=self.form.anRerunCSV, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.anRerunCSVButton.setLayoutHints(LAYOUT_CENTER_Y)
        self.anRerunCSVfileNameField = AFXTextField(self.hfModel_215, 40, '', tgt=self.form.anRerunCSVfileName, sel=0, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        fileDialog = FileDialogBox(self.form,type='csv')
        self.anRerunCSVfileNameButton = FXButton(self.hfModel_215, text=i18n.tr('Select File'), tgt=fileDialog, sel=AFXMode.ID_ACTIVATE)
        self.gbModel_214.setLayoutHints(LAYOUT_FILL_X)

        self.anRerunCSVfileNameField.disable()
        self.anRerunCSVfileNameButton.disable()

        #-----------------------------------------------------------------------

        tb2 = FXTabItem(tb, i18n.tr('Material Properties'), ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        hfModel_2 = FXHorizontalFrame(tb, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+5, pt=DEFAULT_SPACING+5, pb=DEFAULT_SPACING+5, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        #-----------------------------------------------------------------------

        vfModel_3 = FXVerticalFrame(hfModel_2, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING+14)

        gbModel_31 = FXGroupBox(vfModel_3, i18n.tr('Indenter Type and Material'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        hfModel_42 = FXHorizontalFrame(gbModel_31, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING+5, hs=DEFAULT_SPACING+43, vs=DEFAULT_SPACING)

        self.indTypeComboBox = AFXComboBox(hfModel_42, 0, 2, '', tgt=self.form.partIndType, sel=0, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.indTypeComboBox.appendItem('Rigid')
        self.indTypeComboBox.appendItem('Deformable')

        self.indMatComboBox = AFXComboBox(hfModel_42, 0, 3, '', tgt=self.form.matIndNamePre, sel=0, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.indMatComboBox.appendItem('Diamond')
        self.indMatComboBox.appendItem('Sapphire')
        self.indMatComboBox.appendItem('Other')

        vaModel_31 = AFXVerticalAligner(gbModel_31, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        self.indMatTextBox0 = AFXTextField(vaModel_31, 15, "Material Name", tgt=self.form.matIndName, sel=0, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.indMatTextBox1 = AFXTextField(vaModel_31, 15, "Young's Modulus (MPa)", tgt=self.form.matIndEYM, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.indMatTextBox2 = AFXTextField(vaModel_31, 15, "Poisson's Ratio", tgt=self.form.matIndEPR, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.indMatTextBox3 = AFXTextField(vaModel_31, 15, "Density (mg/um^3)", tgt=self.form.matIndDensity, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        gbModel_33 = FXGroupBox(vfModel_3, i18n.tr('Test Article Material'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # vaModel_32a = AFXVerticalAligner(gbModel_33, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # self.taMatTextBox0 = AFXTextField(vaModel_32a, 27, 'Name', tgt=self.form.matTaName, sel=0, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        vaModel_32 = AFXVerticalAligner(gbModel_33, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        self.taMatTextBox0 = AFXTextField(vaModel_32, 15, 'Name', tgt=self.form.matTaName, sel=0, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatTextBox1 = AFXTextField(vaModel_32, 15, "Young's Modulus (MPa)", tgt=self.form.matTaEYM, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatTextBox2 = AFXTextField(vaModel_32, 15, "Poisson's Ratio", tgt=self.form.matTaEPR, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatTextBox3 = AFXTextField(vaModel_32, 15, "Density (mg/um^3)", tgt=self.form.matTaDensity, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)


        vfModel_4 = FXVerticalFrame(hfModel_2, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        gbModel_41 = FXGroupBox(vfModel_4, i18n.tr('Test Article Plasticity'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING+0)
        # gbModel_41.setLayoutHints(LAYOUT_FILL_X)
        self.indTypeComboBox = AFXComboBox(gbModel_41, 0, 7, '', tgt=self.form.matTaPsModel, sel=0, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.indTypeComboBox.appendItem('von Mises')
        self.indTypeComboBox.appendItem('PMP')
        self.indTypeComboBox.appendItem('DPC')
        self.indTypeComboBox.appendItem('DPC (Bruns et al. 2020)')
        self.indTypeComboBox.appendItem('DPC (Davis et al. 2020)')
        self.indTypeComboBox.appendItem('Kermouche et al. 2008 (Fortran Subroutine)')
        self.indTypeComboBox.appendItem('Molnar et al. 2017 (Fortran Subroutine)')

        self.gbModel_42 = FXGroupBox(gbModel_41, i18n.tr('von Mises and Porous Metal Plasticity (PMP)'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        hfModel_42 = FXHorizontalFrame(self.gbModel_42, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING+5, vs=DEFAULT_SPACING)
        self.taMatPlst11 = AFXTextField(hfModel_42, 7, 'YSmin', tgt=self.form.matTaPsVM, sel=0, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD+10, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst12 = AFXTextField(hfModel_42, 5, 'Relative Density', tgt=self.form.matTaPsGTNrd, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst13 = AFXTextField(hfModel_42, 5, 'q1', tgt=self.form.matTaPsGTNq1, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst14 = AFXTextField(hfModel_42, 5, 'q2', tgt=self.form.matTaPsGTNq2, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        self.gbModel_43 = FXGroupBox(gbModel_41, i18n.tr('Drucker-Prager Cap (DPC)'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        hfModel_43 = FXHorizontalFrame(self.gbModel_43, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        self.taMatPlst21 = AFXTextField(hfModel_43, 8, '', tgt=self.form.matTaPsDPCap0, sel=0, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst22 = AFXTextField(hfModel_43, 8, '', tgt=self.form.matTaPsDPCap1, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst23 = AFXTextField(hfModel_43, 8, '', tgt=self.form.matTaPsDPCap2, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst24 = AFXTextField(hfModel_43, 8, '', tgt=self.form.matTaPsDPCap3, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst25 = AFXTextField(hfModel_43, 8, '', tgt=self.form.matTaPsDPCap4, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst26 = AFXTextField(hfModel_43, 8, '', tgt=self.form.matTaPsDPCap5, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        self.gbModel_44 = FXGroupBox(gbModel_41, i18n.tr('Kermouche et al. 2008'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        hfModel_44 = FXHorizontalFrame(self.gbModel_44, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        self.taMatPlst31 = AFXTextField(hfModel_44, 10, '', tgt=self.form.matTaPsKerm1, sel=0, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst32 = AFXTextField(hfModel_44, 10, '', tgt=self.form.matTaPsKerm2, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst33 = AFXTextField(hfModel_44, 10, '', tgt=self.form.matTaPsKerm3, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        self.gbModel_45 = FXGroupBox(gbModel_41, i18n.tr('Molnar et al. 2017'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        hfModel_45 = FXHorizontalFrame(self.gbModel_45, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        self.taMatPlst41 = AFXTextField(hfModel_45, 4, '', tgt=self.form.matTaPsMoln1, sel=0, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst42 = AFXTextField(hfModel_45, 5, '', tgt=self.form.matTaPsMoln2, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst43 = AFXTextField(hfModel_45, 5, '', tgt=self.form.matTaPsMoln3, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst44 = AFXTextField(hfModel_45, 5, '', tgt=self.form.matTaPsMoln4, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst45 = AFXTextField(hfModel_45, 6, '', tgt=self.form.matTaPsMoln5, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst46 = AFXTextField(hfModel_45, 4, '', tgt=self.form.matTaPsMoln6, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst47 = AFXTextField(hfModel_45, 4, '', tgt=self.form.matTaPsMoln7, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst48 = AFXTextField(hfModel_45, 7, '', tgt=self.form.matTaPsMoln8, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.taMatPlst49 = AFXTextField(hfModel_45, 5, '', tgt=self.form.matTaPsMoln9, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        self.gbModel_46 = FXGroupBox(gbModel_41, i18n.tr('Fortran Subroutine File'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        self.hfModel_46 = FXHorizontalFrame(self.gbModel_46, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        self.subFileField = AFXTextField(self.hfModel_46, 50, '', tgt=self.form.anFortranfileName, sel=0, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        fileDialog = FileDialogBox(self.form,type='sub')
        self.subFileButton = FXButton(self.hfModel_46, text=i18n.tr('Select File'), tgt=fileDialog, sel=AFXMode.ID_ACTIVATE)

        #-----------------------------------------------------------------------
        # "The default inputs for this analysis are given in the following units"

        tbUnits0 = FXTabItem(tb, i18n.tr('Units'), ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        vfUnits1 = FXVerticalFrame(tb, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+10, pr=DEFAULT_SPACING+10, pt=DEFAULT_SPACING+10, pb=DEFAULT_SPACING+10, hs=DEFAULT_SPACING+10, vs=DEFAULT_SPACING+10)

        hfUnits1 = FXHorizontalFrame(vfUnits1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING+20, vs=0)

        gbUnits1 = FXGroupBox(hfUnits1, i18n.tr('Base Units'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+5, pt=DEFAULT_SPACING+19, pb=DEFAULT_SPACING+19, hs=DEFAULT_SPACING+5, vs=DEFAULT_SPACING+5)
        FXLabel(gbUnits1, i18n.tr('Mass -> milligram:     mg = kg*10^-6'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits1, i18n.tr('Time -> millisecond:     ms = s*10^-3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits1, i18n.tr('Length -> micrometer:     um = m*10^-6'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        gbUnits2 = FXGroupBox(hfUnits1, i18n.tr('Derrived Units'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+5, pt=DEFAULT_SPACING+5, pb=DEFAULT_SPACING+5, hs=DEFAULT_SPACING+5, vs=DEFAULT_SPACING+5)
        FXLabel(gbUnits2, i18n.tr('Force -> microNewtons:     mg*um/ms^2 = N*10^-6 = uN'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits2, i18n.tr('Pressure -> MegaPascals:     uN/um^2 = Pa*10^6 = MPa'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits2, i18n.tr('Density -> milligram / micrometer^3:     mg/um^3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits2, i18n.tr('Energy -> picoJoule:     uN*um = J*10^-12 = pJ'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        gbUnits3 = FXGroupBox(vfUnits1, i18n.tr('Density Conversions'), opts=FRAME_GROOVE, x=0, y=-20, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+5, pt=DEFAULT_SPACING+5, pb=DEFAULT_SPACING+5, hs=DEFAULT_SPACING+5, vs=DEFAULT_SPACING+5)
        FXLabel(gbUnits3, i18n.tr('1 kg/m^3 = 1*10^-12 mg/um^3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits3, i18n.tr('1 g/cm^3 = 1*10^-9 mg/um^3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        #-----------------------------------------------------------------------

        tbAbout0 = FXTabItem(tb, i18n.tr('About'), ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        vfAbout1 = FXVerticalFrame(tb, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+10, pr=DEFAULT_SPACING+10, pt=DEFAULT_SPACING+10, pb=DEFAULT_SPACING+10, hs=DEFAULT_SPACING+10, vs=DEFAULT_SPACING+10)

        gbAbout1 = FXGroupBox(vfAbout1, i18n.tr(''), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+5, pt=DEFAULT_SPACING+5, pb=DEFAULT_SPACING+5, hs=DEFAULT_SPACING+5, vs=DEFAULT_SPACING+5)
        FXLabel(gbAbout1, i18n.tr('Sharp Indentation Model Plugin'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('Version: 0.0.1 (Beta)'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('License: GNU GPL v3.0'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('https://www.gnu.org/licenses/gpl-3.0.en.html'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('Author: Brian C. Davis'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('Institution: Colorado School of Mines'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('bridavis@mines.edu'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('brian.campbell.davis@gmail.com'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('GitHub: https://github.com/BrianCDavisResearch/abaqus-indentation-plugin'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        #-----------------------------------------------------------------------

        # print >> sys.__stdout__, dir(gbModel_211)
        # print >> sys.__stdout__, self.form.cmd
        # print >> sys.__stdout__, self.form.cmd.getObjectName()
        # print >> sys.__stdout__, self.form.cmd.getObjectName().endswith('Model')
        # print >> sys.__stdout__, self.form.cmd.getObjectName().endswith('Results')
        # print >> sys.__stdout__, dir(self.form.cmd)

        return(None)

    #-----------------------------------------------------------------------

    def processUpdates(self):

        #-----------------------------------------------------------------------

        if self.form.anType.getValue() == 'Explicit - Mass Scaling':

            self.remesh0.enable()
            self.remesh1.enable()
            self.remesh2.enable()

        else:

            self.remesh0.disable()
            self.remesh1.disable()
            self.remesh2.disable()

        #-----------------------------------------------------------------------

        if self.anRerunCSVButton.getCheck() == True:

            self.anRerunCSVfileNameField.enable()
            self.anRerunCSVfileNameButton.enable()

        else:

            self.anRerunCSVfileNameField.disable()
            self.anRerunCSVfileNameButton.disable()

        #-----------------------------------------------------------------------

        if self.form.partIndType.getValue() == 'Rigid':

            self.indMatComboBox.disable()
            self.indMatTextBox0.disable()
            self.indMatTextBox1.disable()
            self.indMatTextBox2.disable()
            self.indMatTextBox3.disable()

        elif self.form.partIndType.getValue() == 'Deformable':

            self.indMatComboBox.enable()
            self.indMatTextBox0.enable()
            self.indMatTextBox1.enable()
            self.indMatTextBox2.enable()
            self.indMatTextBox3.enable()

        #-----------------------------------------------------------------------

        # print >> sys.__stdout__, '%s:%s'%(self.form.matIndNamePre.getValue(),self.indMatComboBox.getItemText(self.indMatComboBox.getCurrentItem()))

        if self.form.matIndNamePre.getValue() != self.indMatComboBox.getItemText(self.indMatComboBox.getCurrentItem()):

            if self.indMatComboBox.getItemText(self.indMatComboBox.getCurrentItem()) == 'Diamond':

                self.form.matIndNamePre.setValue('Diamond')
                self.form.matIndName.setValue('Diamond')
                self.form.matIndEYM.setValue(1050e3)
                self.form.matIndEPR.setValue(0.20)
                self.form.matIndDensity.setValue(3.52e-9)

            elif self.indMatComboBox.getItemText(self.indMatComboBox.getCurrentItem()) == 'Sapphire':

                self.form.matIndNamePre.setValue('Sapphire')
                self.form.matIndName.setValue('Sapphire')
                self.form.matIndEYM.setValue(345e3)
                self.form.matIndEPR.setValue(0.29)
                self.form.matIndDensity.setValue(3.98e-9)

            elif self.indMatComboBox.getItemText(self.indMatComboBox.getCurrentItem()) == 'Other':

                self.form.matIndNamePre.setValue('Other')
                self.form.matIndName.setValue('Other')

        #-----------------------------------------------------------------------

        if self.form.matTaPsModel.getValue() == 'von Mises' or self.form.matTaPsModel.getValue() == 'PMP':

            self.gbModel_42.enable()
            self.taMatPlst11.enable()

        else:

            self.gbModel_42.disable()
            self.taMatPlst11.disable()

        if self.form.matTaPsModel.getValue() == 'PMP':

            self.taMatPlst12.enable()
            self.taMatPlst13.enable()
            self.taMatPlst14.enable()

        else:

            self.taMatPlst12.disable()
            self.taMatPlst13.disable()
            self.taMatPlst14.disable()

        if self.form.matTaPsModel.getValue() == 'DPC':

            self.gbModel_43.enable()
            self.taMatPlst21.enable()
            self.taMatPlst22.enable()
            self.taMatPlst23.enable()
            self.taMatPlst24.enable()
            self.taMatPlst25.enable()
            self.taMatPlst26.enable()

        else:

            self.gbModel_43.disable()
            self.taMatPlst21.disable()
            self.taMatPlst22.disable()
            self.taMatPlst23.disable()
            self.taMatPlst24.disable()
            self.taMatPlst25.disable()
            self.taMatPlst26.disable()

        if self.form.matTaPsModel.getValue() == 'DPC (Bruns et al. 2020)':

            self.gbModel_43.enable()
            self.form.matTaPsDPCap0.setValue(7500.0)
            self.form.matTaPsDPCap1.setValue(1e-04)
            self.form.matTaPsDPCap2.setValue(1.066)
            self.form.matTaPsDPCap3.setValue(0.0)
            self.form.matTaPsDPCap4.setValue(0.0)
            self.form.matTaPsDPCap5.setValue(1.0)

        if self.form.matTaPsModel.getValue() == 'DPC (Davis et al. 2020)':

            self.gbModel_43.enable()
            self.form.matTaPsDPCap0.setValue(5500.0)
            self.form.matTaPsDPCap1.setValue(10.0)
            self.form.matTaPsDPCap2.setValue(0.85)
            self.form.matTaPsDPCap3.setValue(0.0)
            self.form.matTaPsDPCap4.setValue(0.01)
            self.form.matTaPsDPCap5.setValue(1.0)

        if self.form.matTaPsModel.getValue() == 'Kermouche et al. 2008 (Fortran Subroutine)':

            self.gbModel_44.enable()
            self.taMatPlst31.enable()
            self.taMatPlst32.enable()
            self.taMatPlst33.enable()

        else:

            self.gbModel_44.disable()
            self.taMatPlst31.disable()
            self.taMatPlst32.disable()
            self.taMatPlst33.disable()

        if self.form.matTaPsModel.getValue() == 'Molnar et al. 2017 (Fortran Subroutine)':

            self.gbModel_45.enable()
            self.taMatPlst41.enable()
            self.taMatPlst42.enable()
            self.taMatPlst43.enable()
            self.taMatPlst44.enable()
            self.taMatPlst45.enable()
            self.taMatPlst46.enable()
            self.taMatPlst47.enable()
            self.taMatPlst48.enable()
            self.taMatPlst49.enable()

        else:

            self.gbModel_45.disable()
            self.taMatPlst41.disable()
            self.taMatPlst42.disable()
            self.taMatPlst43.disable()
            self.taMatPlst44.disable()
            self.taMatPlst45.disable()
            self.taMatPlst46.disable()
            self.taMatPlst47.disable()
            self.taMatPlst48.disable()
            self.taMatPlst49.disable()

        if self.form.matTaPsModel.getValue().startswith('Kermouche') or self.form.matTaPsModel.getValue().startswith('Molnar'):

            self.gbModel_46.enable()
            self.hfModel_46.enable()
            self.subFileField.enable()
            self.subFileButton.enable()

        else:

            self.gbModel_46.disable()
            self.hfModel_46.disable()
            self.subFileField.disable()
            self.subFileButton.disable()

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

        fileDialog = FileDialogBox(self.form,type='odb')
        FXButton(hf1, text=i18n.tr('Select File(s)'), tgt=fileDialog, sel=AFXMode.ID_ACTIVATE)

        gb2 = FXGroupBox(vf1, i18n.tr('Python Results Scripts'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING, pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        hf2 = FXHorizontalFrame(gb2, LAYOUT_FILL_X, 0,0,0,0, 0,0,0,0)
        tempText = i18n.tr('')
        self.boolWorkForceButton = FXCheckButton(hf2, tempText, tgt=None, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD+10, pb=DEFAULT_PAD)
        self.boolWorkForceButton.setCheck(state=True)
        self.boolWorkForceButton.disable()
        FXLabel(hf2, i18n.tr('Force and Work Energy vs. Displacement (Required)'), pl=DEFAULT_PAD-3, pr=DEFAULT_PAD, pt=DEFAULT_PAD+9, pb=DEFAULT_PAD)

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

        hf3a = FXHorizontalFrame(gb2, LAYOUT_FILL_X, 0,0,0,0, 0,0,0,0)
        FXLabel(hf3a, i18n.tr('PE Limit'), pl=DEFAULT_PAD+20, pr=DEFAULT_PAD, pt=DEFAULT_PAD+3, pb=DEFAULT_PAD)
        self.S22limitPEfield = AFXTextField(hf3a, 10, '', tgt=self.form.boolAreaS22limitPE, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.S22limitPEfield.disable()
        FXLabel(hf3a, i18n.tr('S22 Limit'), pl=DEFAULT_PAD+20, pr=DEFAULT_PAD, pt=DEFAULT_PAD+3, pb=DEFAULT_PAD)
        self.S22limitfield = AFXTextField(hf3a, 10, '', tgt=self.form.boolAreaS22limit, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.S22limitfield.disable()

        tempText = i18n.tr('Plastic Deformation (entire results-zone)')
        self.boolAreaPlasticButton = FXCheckButton(gb2, tempText, tgt=self.form.boolAreaPlastic, sel=0, opts=CHECKBUTTON_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        hf3b = FXHorizontalFrame(gb2, LAYOUT_FILL_X, 0,0,0,0, 0,0,0,0)
        FXLabel(hf3b, i18n.tr('PE Limit'), pl=DEFAULT_PAD+20, pr=DEFAULT_PAD, pt=DEFAULT_PAD+3, pb=DEFAULT_PAD)
        self.PlasticlimitPEfield = AFXTextField(hf3b, 10, '', tgt=self.form.boolAreaPlasticlimitPE, sel=0, opts=AFXTEXTFIELD_FLOAT, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        self.PlasticlimitPEfield.disable()

        #-----------------------------------------------------------------------

        tbUnits0 = FXTabItem(tb, i18n.tr('Units'), ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        vfUnits1 = FXVerticalFrame(tb, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+10, pr=DEFAULT_SPACING+10, pt=DEFAULT_SPACING+10, pb=DEFAULT_SPACING+10, hs=DEFAULT_SPACING+10, vs=DEFAULT_SPACING+10)

        gbUnits1 = FXGroupBox(vfUnits1, i18n.tr('Base Units'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+5, pt=DEFAULT_SPACING+5, pb=DEFAULT_SPACING+5, hs=DEFAULT_SPACING+5, vs=DEFAULT_SPACING+5)
        FXLabel(gbUnits1, i18n.tr('Mass -> milligram:     mg = kg*10^-6'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits1, i18n.tr('Time -> millisecond:     ms = s*10^-3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits1, i18n.tr('Length -> micrometer:     um = m*10^-6'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        gbUnits2 = FXGroupBox(vfUnits1, i18n.tr('Derrived Units'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+5, pt=DEFAULT_SPACING+5, pb=DEFAULT_SPACING+5, hs=DEFAULT_SPACING+5, vs=DEFAULT_SPACING+5)
        FXLabel(gbUnits2, i18n.tr('Force -> microNewtons:     mg*um/ms^2 = N*10^-6 = uN'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits2, i18n.tr('Pressure -> MegaPascals:     uN/um^2 = Pa*10^6 = MPa'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits2, i18n.tr('Density -> milligram / micrometer^3:     mg/um^3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits2, i18n.tr('Energy -> picoJoule:     uN*um = J*10^-12 = pJ'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        gbUnits3 = FXGroupBox(vfUnits1, i18n.tr('Density Conversions'), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+5, pt=DEFAULT_SPACING+5, pb=DEFAULT_SPACING+5, hs=DEFAULT_SPACING+5, vs=DEFAULT_SPACING+5)
        FXLabel(gbUnits3, i18n.tr('1 kg/m^3 = 1*10^-12 mg/um^3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbUnits3, i18n.tr('1 g/cm^3 = 1*10^-9 mg/um^3'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        #-----------------------------------------------------------------------

        tbAbout0 = FXTabItem(tb, i18n.tr('About'), ic=None, opts=TAB_TOP_NORMAL, x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        vfAbout1 = FXVerticalFrame(tb, opts=0, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+10, pr=DEFAULT_SPACING+10, pt=DEFAULT_SPACING+10, pb=DEFAULT_SPACING+10, hs=DEFAULT_SPACING+10, vs=DEFAULT_SPACING+10)

        gbAbout1 = FXGroupBox(vfAbout1, i18n.tr(''), opts=FRAME_GROOVE, x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING+5, pr=DEFAULT_SPACING+5, pt=DEFAULT_SPACING+5, pb=DEFAULT_SPACING+5, hs=DEFAULT_SPACING+5, vs=DEFAULT_SPACING+5)
        FXLabel(gbAbout1, i18n.tr('Sharp Indentation Results Plugin'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('Version: 0.0.1 (Beta)'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('License: GNU GPL v3.0'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('https://www.gnu.org/licenses/gpl-3.0.en.html'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('Author: Brian C. Davis'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('Institution: Colorado School of Mines'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('bridavis@mines.edu'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('brian.campbell.davis@gmail.com'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        FXLabel(gbAbout1, i18n.tr('GitHub: https://github.com/BrianCDavisResearch/abaqus-indentation-plugin'), pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        #-----------------------------------------------------------------------

        return(None)

    #-----------------------------------------------------------------------

    def processUpdates(self):

        if self.boolAreaS22Button.getCheck() == True:

            self.S22limitPEfield.enable()
            self.S22limitfield.enable()

        else:

            self.S22limitPEfield.disable()
            self.S22limitfield.disable()

        if self.boolAreaPlasticButton.getCheck() == True:

            self.PlasticlimitPEfield.enable()

        else:

            self.PlasticlimitPEfield.disable()

        return(None)

    #-----------------------------------------------------------------------

#-----------------------------------------------------------------------

class FileDialogBox(FXObject):

    #-----------------------------------------------------------------------

    def __init__(self, form, **kwargs):

        self.form = form

        tempType = kwargs.get('type',None)

        FXObject.__init__(self)

        # print >> sys.__stdout__, self.form.cmd.getObjectName().endswith('Model')
        # print >> sys.__stdout__, self.form.cmd.getObjectName().endswith('Results')

        if tempType == 'csv':

            FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, FileDialogBox.csvDialogBox)

        elif tempType == 'sub':

            FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, FileDialogBox.subDialogBox)

        elif tempType == 'odb':

            FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, FileDialogBox.odbDialogBox)

        return(None)

    #-----------------------------------------------------------------------

    def csvDialogBox(self, sender, sel, ptr):

        tempDialog = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select "All-Inputs" CSV File', self.form.anRerunCSVfileName, self.form.anRerunCSVfileNameReadOnly, AFXSELECTFILE_EXISTING, '"All-Inputs" CSV File (*All-Inputs.csv)\nAll Files (*)', AFXIntTarget(0))

        tempDialog.create()

        tempDialog.showModal()

        return(None)

    #-----------------------------------------------------------------------

    def subDialogBox(self, sender, sel, ptr):

        tempDialog = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select Subroutine File', self.form.anFortranfileName, self.form.anFortranReadOnly, AFXSELECTFILE_EXISTING, 'Fortran Subroutine File (*.f,*.for)\nAll Files (*)', AFXIntTarget(0))

        tempDialog.create()

        tempDialog.showModal()

        return(None)

    #-----------------------------------------------------------------------

    def odbDialogBox(self, sender, sel, ptr):

        tempDialog = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select ODB File(s)', self.form.odbPath, self.form.odbReadOnly, AFXSELECTFILE_MULTIPLE_ALL, 'Abaqus ODB Files (*.odb)\nAll Files (*)', AFXIntTarget(0))

        tempDialog.create()

        tempDialog.showModal()

        return(None)

    #-----------------------------------------------------------------------

#-----------------------------------------------------------------------