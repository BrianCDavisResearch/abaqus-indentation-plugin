# Do not edit this file or it may not load correctly
# if you try to open it with the RSG Dialog Builder.

# Note: thisDir is defined by the Activator class when
#       this file gets exec'd

from rsg.rsgGui import *
from abaqusConstants import INTEGER, FLOAT
dialogBox = RsgDialog(title='Indentation: Output (Axisymmetric Conical Equivalent)', kernelModule='LP_Indentation_Output', kernelFunction='output_plugin_prescript', includeApplyBtn=True, includeSeparator=True, okBtnText='OK', applyBtnText='Apply', execDir=thisDir)
RsgTabBook(name='TabBook_1', p='DialogBox', layout='0')
RsgTabItem(name='TabItem_4', p='TabBook_1', text='Output Scripts')
RsgVerticalFrame(name='VFrame_3', p='TabItem_4', layout='0', pl=10, pr=10, pt=10, pb=10)
RsgSeparator(p='VFrame_3')
RsgHorizontalFrame(name='HFrame_8', p='VFrame_3', layout='0', pl=0, pr=0, pt=0, pb=0)
RsgFileTextField(p='HFrame_8', ncols=50, labelText='ODB File Name', keyword='odbPath', default='', patterns='ODB Files (*.odb)')
RsgSeparator(p='VFrame_3')
RsgLabel(p='VFrame_3', text='Output Scripts', useBoldFont=True)
RsgSeparator(p='VFrame_3')
RsgHorizontalFrame(name='HFrame_12', p='VFrame_3', layout='0', pl=10, pr=0, pt=0, pb=0)
RsgIcon(p='HFrame_12', fileName=r'iconPermaCheck.png')
RsgLabel(p='HFrame_12', text='Force and Work-Energy vs. Displacement', useBoldFont=False)
RsgHorizontalFrame(name='HFrame_13', p='VFrame_3', layout='0', pl=10, pr=0, pt=0, pb=0)
RsgVerticalFrame(name='VFrame_10', p='HFrame_13', layout='0', pl=1, pr=0, pt=0, pb=0)
RsgSeparator(p='VFrame_10')
RsgCheckButton(p='VFrame_10', text=' Energy Summations (Whole Model)', keyword='boolEnergy', default=True)
RsgCheckButton(p='VFrame_10', text='Orthogonal Normal Stress Profiles (centerline and surface)', keyword='boolOrthoStress', default=True)
RsgCheckButton(p='VFrame_10', text='Surface Topology', keyword='boolSurfTop', default=True)
RsgSeparator(p='VFrame_10')
RsgCheckButton(p='VFrame_10', text='Indent Volumes', keyword='boolIndVol', default=True)
RsgCheckButton(p='VFrame_10', text='Contact Force Vector', keyword='boolContVect', default=True)
RsgCheckButton(p='VFrame_10', text='Normalizer Variables', keyword='boolNorm', default=True)
RsgSeparator(p='VFrame_10')
RsgCheckButton(p='VFrame_10', text='Stress Invariants (centerline and surface)', keyword='boolInvStress', default=False)
RsgCheckButton(p='VFrame_10', text='Density or Relative Density (centerline and surface)', keyword='boolDensity', default=False)
RsgSeparator(p='VFrame_10')
RsgCheckButton(p='VFrame_10', text='Stress Invariants (entire results-zone)', keyword='boolAreaInvariants', default=False)
RsgCheckButton(p='VFrame_10', text='S22, Lateral Crack Driving Stress (entire results-zone)', keyword='boolAreaS22', default=False)
RsgCheckButton(p='VFrame_10', text='Plastic Deformation (entire results-zone)', keyword='boolAreaPlastic', default=False)
RsgHorizontalFrame(name='HFrame_14', p='VFrame_10', layout='0', pl=18, pr=0, pt=0, pb=0)
RsgTextField(p='HFrame_14', fieldType='Float', ncols=10, labelText='PEEQ Threshold', keyword='limitPEEQ', default='1e-05')
RsgSeparator(p='VFrame_3')
RsgTabItem(name='TabItem_3', p='TabBook_1', text='Units')
RsgVerticalFrame(name='VFrame_4', p='TabItem_3', layout='0', pl=10, pr=10, pt=10, pb=10)
RsgLabel(p='VFrame_4', text='The default values for this analysis are given in the following units:', useBoldFont=False)
RsgSeparator(p='VFrame_4')
RsgLabel(p='VFrame_4', text='Base Units', useBoldFont=True)
RsgSeparator(p='VFrame_4')
RsgLabel(p='VFrame_4', text='Mass -> milligram:     mg = kg*10^-6', useBoldFont=False)
RsgLabel(p='VFrame_4', text='Time -> millisecond:     ms = s*10^-3', useBoldFont=False)
RsgLabel(p='VFrame_4', text='Length -> micrometer:     um = m*10^-6', useBoldFont=False)
RsgSeparator(p='VFrame_4')
RsgLabel(p='VFrame_4', text='Derrived Units', useBoldFont=True)
RsgSeparator(p='VFrame_4')
RsgLabel(p='VFrame_4', text='Force -> microNewtons:     mg*um/ms^2 = N*10^-6 = uN', useBoldFont=False)
RsgLabel(p='VFrame_4', text='Pressure -> MegaPascals:     uN/um^2 = Pa*10^6 = MPa', useBoldFont=False)
RsgLabel(p='VFrame_4', text='Density -> milligram / micrometer^3:     mg/um^3', useBoldFont=False)
RsgLabel(p='VFrame_4', text='Energy -> picoJoule:     uN*um = J*10^-12 = pJ', useBoldFont=False)
RsgSeparator(p='VFrame_4')
RsgLabel(p='VFrame_4', text='Convenient Density Conversions', useBoldFont=True)
RsgSeparator(p='VFrame_4')
RsgLabel(p='VFrame_4', text='1 kg/m^3 = 1*10^-12 mg/um^3', useBoldFont=False)
RsgLabel(p='VFrame_4', text='1 g/cm^3 = 1*10^-9 mg/um^3', useBoldFont=False)
RsgTabItem(name='TabItem_2', p='TabBook_1', text='About')
RsgVerticalFrame(name='VFrame_5', p='TabItem_2', layout='0', pl=10, pr=10, pt=10, pb=10)
RsgLabel(p='VFrame_5', text='Author: Brian C. Davis', useBoldFont=False)
RsgLabel(p='VFrame_5', text='Institution: Colorado School of Mines', useBoldFont=False)
RsgLabel(p='VFrame_5', text='bridavis@mines.edu', useBoldFont=False)
RsgLabel(p='VFrame_5', text='brian.campbell.davis@gmail.com', useBoldFont=False)
dialogBox.show()