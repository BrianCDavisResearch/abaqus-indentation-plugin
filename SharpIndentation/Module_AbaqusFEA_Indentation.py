#--------------------------------------------------------------------------------------------------
# Copyright 2020 Brian C. Davis
#--------------------------------------------------------------------------------------------------

from abaqusConstants import *

import csv, os, numpy as np, subprocess, sys

#--------------------------------------------------------------------------------------------------

class General_Analysis(object):

    #-----------------------------------------------------------------------

    def __init__(self):

        return(None)

    #-----------------------------------------------------------------------

    def createElasticMaterials(self,*args,**kwargs):

        self.partIndType = kwargs.get('partIndType',None)

        self.matIndDensity = kwargs.get('matIndDensity',None)
        self.matIndEPR = kwargs.get('matIndEPR',None)
        self.matIndEYM = kwargs.get('matIndEYM',None)
        self.matIndName = kwargs.get('matIndName',None)

        self.matTaDensity = kwargs.get('matTaDensity',None)
        self.matTaEPR = kwargs.get('matTaEPR',None)
        self.matTaEYM = kwargs.get('matTaEYM',None)
        self.matTaName = kwargs.get('matTaName',None)
        self.matTaRayDamp = kwargs.get('matTaRayDamp',None)

        if self.partIndType == 'Deformable':

            self.mdb.models['Model-1'].Material(name='Elastic_'+self.matIndName)
            self.mdb.models['Model-1'].materials['Elastic_'+self.matIndName].Elastic(table=((self.matIndEYM, self.matIndEPR), ))
            self.mdb.models['Model-1'].materials['Elastic_'+self.matIndName].Density(table=((self.matIndDensity, ), ))

            self.mdb.models['Model-1'].HomogeneousSolidSection(name='Elastic_'+self.matIndName, material='Elastic_'+self.matIndName, thickness=None)

        else:

            self.matIndName = None
            self.matIndEPR = None
            self.matIndEYM = None
            self.matIndDensity = None

        self.mdb.models['Model-1'].Material(name='Elastic_'+self.matTaName)
        self.mdb.models['Model-1'].materials['Elastic_'+self.matTaName].Elastic(table=((self.matTaEYM, self.matTaEPR), ))
        self.mdb.models['Model-1'].materials['Elastic_'+self.matTaName].Density(table=((self.matTaDensity, ), ))

        if self.anSolverType.startswith('Explicit'):

            self.mdb.models['Model-1'].materials['Elastic_'+self.matTaName].Damping(alpha=self.matTaRayDamp[0], beta=self.matTaRayDamp[1])

        self.mdb.models['Model-1'].HomogeneousSolidSection(name='Elastic_'+self.matTaName, material='Elastic_'+self.matTaName, thickness=None)

        return(None)

    #-----------------------------------------------------------------------

    def createPlasticMaterials(self,*args,**kwargs):

        self.matTaPsModel = kwargs.get('matTaPsModel',None)

        self.matTaPsVM = kwargs.get('matTaPsVM',None)
        self.matTaPsGTNrd = kwargs.get('matTaPsGTNrd',None)
        self.matTaPsGTNq = kwargs.get('matTaPsGTNq',None)

        self.matTaPsDPCap = kwargs.get('matTaPsDPCap',None)
        self.matTaPsDPCapHard = kwargs.get('matTaPsDPCapHard',None)

        self.matTaPsKerm = kwargs.get('matTaPsKerm',None)
        self.matTaPsMoln = kwargs.get('matTaPsMoln',None)

        if self.matTaPsModel.startswith('von'):

            self.matTaPsModel = 'vonMises'

            self.mdb.models['Model-1'].Material(name=self.matTaPsModel+'_'+self.matTaName)
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Elastic(table=((self.matTaEYM, self.matTaEPR), ))
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Density(table=((self.matTaDensity, ), ))
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Plastic(table=((self.matTaPsVM, 0.0),))

        elif self.matTaPsModel.startswith('PMP') or self.matTaPsModel == 'GTN-pmp':

            self.matTaPsModel = 'PMP'

            self.mdb.models['Model-1'].Material(name=self.matTaPsModel+'_'+self.matTaName)
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Elastic(table=((self.matTaEYM, self.matTaEPR), ))
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Density(table=((self.matTaDensity, ), ))
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Plastic(table=((self.matTaPsVM, 0.0),))
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].PorousMetalPlasticity(relativeDensity=self.matTaPsGTNrd, table=(self.matTaPsGTNq, ))

        elif self.matTaPsModel.startswith('DPC'):

            self.matTaPsModel = 'DPC'

            self.mdb.models['Model-1'].Material(name=self.matTaPsModel+'_'+self.matTaName)
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Elastic(table=((self.matTaEYM, self.matTaEPR), ))
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Density(table=((self.matTaDensity, ), ))
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].CapPlasticity(table=(self.matTaPsDPCap, ))

            if self.matTaPsDPCapHard is None:

                self.matTaPsDPCapHard = ((self.matTaPsDPCap[0]*self.matTaPsDPCap[2],0.0),(2.0*self.matTaPsDPCap[0]*self.matTaPsDPCap[2],1.0),)

            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].capPlasticity.CapHardening(table=self.matTaPsDPCapHard)

        elif self.matTaPsModel.startswith('Kerm'):

            self.matTaPsModel = 'Kermouche2008'

            self.mdb.models['Model-1'].Material(name=self.matTaPsModel+'_'+self.matTaName)
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Density(table=((self.matTaDensity, ), ))
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Depvar(n=9)
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].UserMaterial(mechanicalConstants=([self.matTaEYM,self.matTaEPR] + list(self.matTaPsKerm)))

        elif self.matTaPsModel.startswith('Moln'):

            self.matTaPsModel = 'Molnar2017'

            self.mdb.models['Model-1'].Material(name=self.matTaPsModel+'_'+self.matTaName)
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Density(table=((self.matTaDensity, ), ))
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Depvar(n=11)
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].UserMaterial(mechanicalConstants=([self.matTaEYM,self.matTaEPR] + list(self.matTaPsMoln)))

        elif self.matTaPsModel.startswith('Linear'):

            self.matTaPsModel = 'LinYMsub'

            self.mdb.models['Model-1'].Material(name=self.matTaPsModel+'_'+self.matTaName)
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Density(table=((self.matTaDensity, ), ))

            ############ User Material still in work ############
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].Depvar(n=1)
            self.mdb.models['Model-1'].materials[self.matTaPsModel+'_'+self.matTaName].UserMaterial(mechanicalConstants=(70.0e3, -4.006, 0.15, 7.00e3, 0.0, 7.10e3, 0.1, 7.50e3, 0.5))

        self.mdb.models['Model-1'].HomogeneousSolidSection(name=self.matTaPsModel+'_'+self.matTaName, material=self.matTaPsModel+'_'+self.matTaName, thickness=None)

        return(None)

    #-----------------------------------------------------------------------

    def createSteps(self,*args,**kwargs):

        self.anJobName = kwargs.get('anJobName',None)
        self.anTimeStep = kwargs.get('anTimeStep',None)
        self.anBulkViscosity = kwargs.get('anBulkViscosity',None)

        self.outpFieldInt = kwargs.get('outpFieldInt',None)
        self.outpHistInt = kwargs.get('outpHistInt',None)

        self.initStdIncFactor = kwargs.get('initStdIncFactor',1e-03)

        from caeModules import step

        if self.anSolverType.startswith('Standard'):

            if self.anSolverType.endswith('Static'):

                self.mdb.models['Model-1'].StaticStep(name='Loading', previous='Initial',
                    maxNumInc=10000, stabilizationMagnitude=0.0002, timePeriod=self.anTimeStep[0],
                    stabilizationMethod=DISSIPATED_ENERGY_FRACTION,
                    continueDampingFactors=False, adaptiveDampingRatio=0.05, initialInc=self.anTimeStep[0]*self.initStdIncFactor,
                    minInc=1e-15, matrixSolver=DIRECT, matrixStorage=UNSYMMETRIC, nlgeom=ON)

                self.mdb.models['Model-1'].StaticStep(name='Unloading', previous='Loading',
                    maxNumInc=10000, stabilizationMagnitude=0.0002, timePeriod=self.anTimeStep[2],
                    stabilizationMethod=DISSIPATED_ENERGY_FRACTION,
                    continueDampingFactors=False, adaptiveDampingRatio=0.05, initialInc=self.anTimeStep[2]*self.initStdIncFactor,
                    minInc=1e-15, matrixSolver=DIRECT, matrixStorage=UNSYMMETRIC)

            elif self.anSolverType.endswith('Quasi-Static'):

                if self.anTimeStep[1] > 0.0:

                    self.mdb.models['Model-1'].ImplicitDynamicsStep(name='Loading', previous='Initial',
                        maxNumInc=10000, application=QUASI_STATIC, initialInc=self.anTimeStep[0]*self.initStdIncFactor, minInc=1e-15, timePeriod=self.anTimeStep[0],
                        nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF, matrixStorage=UNSYMMETRIC, nlgeom=ON)

                    self.mdb.models['Model-1'].ImplicitDynamicsStep(name='Dwell-Loaded', previous='Loading',
                        maxNumInc=10000, application=QUASI_STATIC, initialInc=self.anTimeStep[1]*self.initStdIncFactor, minInc=1e-15, timePeriod=self.anTimeStep[1],
                        nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF, matrixStorage=UNSYMMETRIC, nlgeom=ON)

                    self.mdb.models['Model-1'].ImplicitDynamicsStep(name='Unloading', previous='Dwell-Loaded',
                        maxNumInc=10000, application=QUASI_STATIC, initialInc=self.anTimeStep[2]*self.initStdIncFactor, minInc=1e-15, timePeriod=self.anTimeStep[2],
                        nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF, matrixStorage=UNSYMMETRIC)

                else:

                    self.mdb.models['Model-1'].ImplicitDynamicsStep(name='Loading', previous='Initial',
                        maxNumInc=10000, application=QUASI_STATIC, initialInc=self.anTimeStep[0]*self.initStdIncFactor, minInc=1e-15, timePeriod=self.anTimeStep[0],
                        nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF, matrixStorage=UNSYMMETRIC, nlgeom=ON)

                    self.mdb.models['Model-1'].ImplicitDynamicsStep(name='Unloading', previous='Loading',
                        maxNumInc=10000, application=QUASI_STATIC, initialInc=self.anTimeStep[2]*self.initStdIncFactor, minInc=1e-15, timePeriod=self.anTimeStep[2],
                        nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF, matrixStorage=UNSYMMETRIC)

            if self.anJobName.endswith('_pre'):

                print('"Pre-test" option selected.')

                del self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1']
                self.mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(numIntervals=self.outpHistInt)

                regionDef1=self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                regionDef2=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Base_Set']
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Ind', createStepName='Loading', variables=('U', 'RF'), numIntervals=self.outpHistInt, timeMarks=ON, region=regionDef1, sectionPoints=DEFAULT, rebar=EXCLUDE)
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Base', createStepName='Loading', variables=('RF', ), numIntervals=self.outpHistInt, timeMarks=ON, region=regionDef2, sectionPoints=DEFAULT, rebar=EXCLUDE)

            else:

                self.mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(numIntervals=self.outpHistInt)

                if self.partIndType == 'Rigid':

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                    self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'COORD'), region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.outpFieldInt, timeMarks=ON)

                elif self.partIndType == 'Deformable':

                    # self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'COORD'), region=MODEL, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.outpFieldInt, timeMarks=ON)

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                    self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'COORD'), region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.outpFieldInt, timeMarks=ON)

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Indenter-1'].sets['Set-1']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='F-Output-2', createStepName='Loading', variables=('LE', 'U', 'COORD'),
                        numIntervals=self.outpFieldInt, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                if self.matTaPsModel.startswith('PMP'):

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Mat_Plastic_Set']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='Plastic_Zone', createStepName='Loading', variables=('PE', 'PEEQ', 'VVF','VVFG','VVFN', 'RD'),
                        numIntervals=self.outpFieldInt, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                elif self.matTaPsModel.startswith('DPC'):

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Mat_Plastic_Set']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='Plastic_Zone', createStepName='Loading', variables=('PE', 'PEEQ', 'PEQC'),
                        numIntervals=self.outpFieldInt, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                elif self.matTaPsModel.startswith('Kerm') or self.matTaPsModel.startswith('Moln') or self.matTaPsModel.endswith('sub'):

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Mat_Plastic_Set']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='User-Output', createStepName='Loading', variables=('SDV', 'ESDV', 'FV', 'UVARM', 'STATUS', 'EACTIVE'),
                        numIntervals=self.outpFieldInt, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                else:

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Mat_Plastic_Set']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='Plastic_Zone', createStepName='Loading', variables=('PE', 'PEEQ'),
                        numIntervals=self.outpFieldInt, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                self.mdb.models['Model-1'].FieldOutputRequest(name='Contact_Results', createStepName='Loading', variables=('CSTRESS', 'CDISP', 'CFORCE'), numIntervals=self.outpFieldInt, timeMarks=ON)

                # regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                # self.mdb.models['Model-1'].FieldOutputRequest(name='Elemental_Energies_Volumes', createStepName='Loading', variables=('ENER', 'ELEN', 'ELEDEN', 'EVOL', 'IVOL'),
                    # numIntervals=self.outpFieldInt, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                regionDef1=self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                regionDef2=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Base_Set']
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Ind', createStepName='Loading', variables=('U', 'RF'), numIntervals=self.outpHistInt, timeMarks=ON, region=regionDef1, sectionPoints=DEFAULT, rebar=EXCLUDE)
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Base', createStepName='Loading', variables=('RF', ), numIntervals=self.outpHistInt, timeMarks=ON, region=regionDef2, sectionPoints=DEFAULT, rebar=EXCLUDE)

            self.mdb.models['Model-1'].SmoothStepAmplitude(name='Std-Indent-Smooth', timeSpan=STEP, data=((0.0, 0.0), (self.anTimeStep[0], 1.0)))
            self.mdb.models['Model-1'].SmoothStepAmplitude(name='Std-Remove-Smooth', timeSpan=STEP, data=((0.0, 1.0), (self.anTimeStep[2], 0.0)))

            self.mdb.models['Model-1'].TabularAmplitude(name='Std-Indent-Tabular', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (self.anTimeStep[0], 1.0)))
            self.mdb.models['Model-1'].TabularAmplitude(name='Std-Remove-Tabular', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 1.0), (self.anTimeStep[2], 0.0)))

            #Gives up after 20 unconverged iterations (instead of 5)
            self.mdb.models['Model-1'].steps['Loading'].control.setValues(allowPropagation=OFF, resetDefaultValues=OFF, timeIncrementation=(4.0, 8.0, 9.0, 16.0, 10.0, 4.0, 12.0, 20.0, 6.0, 3.0, 50.0))

        elif self.anSolverType.startswith('Explicit'):

            if self.anTimeStep[1] > 0.0:

                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Loading', previous='Initial', timePeriod=self.anTimeStep[0])
                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Dwell-Loaded', previous='Loading', timePeriod=self.anTimeStep[1])
                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Unloading', previous='Dwell-Loaded', timePeriod=self.anTimeStep[2])

                self.mdb.models['Model-1'].steps['Loading'].setValues(linearBulkViscosity=self.anBulkViscosity[0])
                self.mdb.models['Model-1'].steps['Dwell-Loaded'].setValues(linearBulkViscosity=self.anBulkViscosity[1])
                self.mdb.models['Model-1'].steps['Unloading'].setValues(linearBulkViscosity=self.anBulkViscosity[2])

                self.mdb.models['Model-1'].steps['Loading'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)
                self.mdb.models['Model-1'].steps['Dwell-Loaded'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)
                self.mdb.models['Model-1'].steps['Unloading'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)

            else:

                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Loading', previous='Initial', timePeriod=self.anTimeStep[0])
                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Unloading', previous='Loading', timePeriod=self.anTimeStep[2])

                self.mdb.models['Model-1'].steps['Loading'].setValues(linearBulkViscosity=self.anBulkViscosity[0])
                self.mdb.models['Model-1'].steps['Unloading'].setValues(linearBulkViscosity=self.anBulkViscosity[2])

                self.mdb.models['Model-1'].steps['Loading'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)
                self.mdb.models['Model-1'].steps['Unloading'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)

            if self.anTimeStep[3] > 0.0:

                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Dwell-Unloaded', previous='Unloading', timePeriod=self.anTimeStep[3])
                self.mdb.models['Model-1'].steps['Dwell-Unloaded'].setValues(linearBulkViscosity=self.anBulkViscosity[3])
                self.mdb.models['Model-1'].steps['Dwell-Unloaded'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)

            if self.anSolverType.endswith('Mass Scaling'):

                self.mdb.models['Model-1'].steps['Loading'].setValues(massScaling=((SEMI_AUTOMATIC, MODEL, THROUGHOUT_STEP, 0.0, 1.0, BELOW_MIN, 100, 0, 0.0, 0.0, 0, None), ))

            if self.anJobName.endswith('_pre'):

                del self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1']
                self.mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(numIntervals=self.outpHistInt)

                regionDef1=self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                regionDef2=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Base_Set']
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Ind', createStepName='Loading', variables=('U', 'RF'), numIntervals=self.outpHistInt, timeMarks=ON, region=regionDef1, sectionPoints=DEFAULT, rebar=EXCLUDE)
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Base', createStepName='Loading', variables=('RF', ), numIntervals=self.outpHistInt, timeMarks=ON, region=regionDef2, sectionPoints=DEFAULT, rebar=EXCLUDE)

            else:

                self.mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(numIntervals=self.outpHistInt)

                if self.partIndType == 'Rigid':

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                    self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'V', 'A', 'COORD'), region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.outpFieldInt, timeMarks=ON)

                elif self.partIndType == 'Deformable':

                    # self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'V', 'A', 'COORD'), region=MODEL, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.outpFieldInt, timeMarks=ON)

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                    self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'V', 'A', 'COORD'), region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.outpFieldInt, timeMarks=ON)

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Indenter-1'].sets['Set-1']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='F-Output-2', createStepName='Loading', variables=('LE', 'U', 'V', 'A', 'COORD'),
                        numIntervals=self.outpFieldInt, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                if self.matTaPsModel.startswith('PMP'):

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Mat_Plastic_Set']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='Plastic_Zone', createStepName='Loading', variables=('PE', 'PEEQ', 'DENSITY', 'VVF','VVFG','VVFN'),
                        numIntervals=self.outpFieldInt, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                elif self.matTaPsModel.startswith('DPC'):

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Mat_Plastic_Set']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='Plastic_Zone', createStepName='Loading', variables=('PE', 'PEEQ', 'PEQC', 'DENSITY'),
                        numIntervals=self.outpFieldInt, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                else:

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Mat_Plastic_Set']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='Plastic_Zone', createStepName='Loading', variables=('PE', 'PEEQ', 'DENSITY'),
                        numIntervals=self.outpFieldInt, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                self.mdb.models['Model-1'].FieldOutputRequest(name='Contact_Results', createStepName='Loading', variables=('CSTRESS', 'CDISP', 'CFORCE', 'FSLIPR', 'FSLIP'), numIntervals=self.outpFieldInt, timeMarks=ON)

                # regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                # self.mdb.models['Model-1'].FieldOutputRequest(name='Elemental_Energies_Volumes', createStepName='Loading', variables=('ENER', 'ELEN', 'ELEDEN', 'EDCDEN', 'EDT', 'EVOL'),
                    # numIntervals=self.outpFieldInt, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                regionDef1=self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                regionDef2=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Base_Set']
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Ind', createStepName='Loading', variables=('U', 'RF'), numIntervals=self.outpHistInt, timeMarks=ON, region=regionDef1, sectionPoints=DEFAULT, rebar=EXCLUDE)
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Base', createStepName='Loading', variables=('RF', ), numIntervals=self.outpHistInt, timeMarks=ON, region=regionDef2, sectionPoints=DEFAULT, rebar=EXCLUDE)

            self.mdb.models['Model-1'].SmoothStepAmplitude(name='Exp-Indent-Smooth', timeSpan=STEP, data=((0.0, 0.0), (self.anTimeStep[0], 1.0)))
            self.mdb.models['Model-1'].SmoothStepAmplitude(name='Exp-Remove-Smooth', timeSpan=STEP, data=((0.0, 1.0), (self.anTimeStep[2], 0.0)))

            self.mdb.models['Model-1'].TabularAmplitude(name='Exp-Indent-Tabular', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (self.anTimeStep[0], 1.0)))
            self.mdb.models['Model-1'].TabularAmplitude(name='Exp-Remove-Tabular', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 1.0), (self.anTimeStep[2], 0.0)))

        return(None)

    #-----------------------------------------------------------------------

    def createRemeshing(self,*args,**kwargs):

        self.meshRemeshing = kwargs.get('meshRemeshing',None)

        if self.anSolverType.startswith('Explicit'):

            self.mdb.models['Model-1'].AdaptiveMeshControl(name='Adaptive_Mesh_Control')
            # self.mdb.models['Model-1'].adaptiveMeshControls['Adaptive_Mesh_Control'].setValues(smoothingPriority=GRADED, smoothingAlgorithm=GEOMETRY_ENHANCED)
            self.mdb.models['Model-1'].adaptiveMeshControls['Adaptive_Mesh_Control'].setValues(smoothingPriority=UNIFORM, smoothingAlgorithm=ANALYSIS_PRODUCT_DEFAULT) # "Improved Aspect Ratio"
            self.mdb.models['Model-1'].adaptiveMeshControls['Adaptive_Mesh_Control'].setValues(volumetricSmoothingWeight=0.50, laplacianSmoothingWeight=0.50, equipotentialSmoothingWeight=0.00)

            region=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].sets['Remeshing_Set']

            self.mdb.models['Model-1'].steps['Loading'].AdaptiveMeshDomain(region=region, controls='Adaptive_Mesh_Control')
            self.mdb.models['Model-1'].steps['Loading'].adaptiveMeshDomains['Loading'].setValues(frequency=self.meshRemeshing[0], meshSweeps=self.meshRemeshing[1])

            if (self.meshRemeshing[0] == 1) and (self.meshRemeshing[1] >= 10):

                self.mdb.models['Model-1'].steps['Unloading'].AdaptiveMeshDomain(region=region, controls='Adaptive_Mesh_Control')
                self.mdb.models['Model-1'].steps['Unloading'].adaptiveMeshDomains['Unloading'].setValues(frequency=self.meshRemeshing[0], meshSweeps=self.meshRemeshing[1])

        return(None)

    #-----------------------------------------------------------------------

    def createPredefinedField(self,*args,**kwargs):

        self.bcTaPreStress = kwargs.get('bcTaPreStress',None)

        self.ampFunction = kwargs.get('ampFunction','Tabular') #Currently, only the default is used.

        if self.anSolverType.startswith('Standard'):

            if False: #selects between "explicit method" of creating a step for applying pre-stress, or "standard method" of applying pre-stress as an initial condition

                if self.anSolverType.endswith('- Static'):

                    self.mdb.models['Model-1'].StaticStep(name='Pre-Stress', previous='Initial',
                        maxNumInc=10000, stabilizationMagnitude=0.0002, timePeriod=self.anTimeStep[0],
                        stabilizationMethod=DISSIPATED_ENERGY_FRACTION,
                        continueDampingFactors=False, adaptiveDampingRatio=0.05, initialInc=self.anTimeStep[0]*1e-05,
                        minInc=1e-15, matrixSolver=DIRECT, matrixStorage=UNSYMMETRIC, nlgeom=ON)

                elif self.anSolverType.endswith('- Quasi-Static'):

                    self.mdb.models['Model-1'].ImplicitDynamicsStep(name='Pre-Stress', previous='Initial',
                        maxNumInc=10000, application=QUASI_STATIC, initialInc=self.anTimeStep[0]*1e-05, minInc=1e-15, timePeriod=self.anTimeStep[0],
                        nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF,
                        matrixStorage=UNSYMMETRIC, nlgeom=ON)

                self.mdb.models['Model-1'].fieldOutputRequests['Contact_Results'].move('Loading', 'Pre-Stress')
                self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].move('Loading', 'Pre-Stress')
                self.mdb.models['Model-1'].fieldOutputRequests['Plastic_Zone'].move('Loading', 'Pre-Stress')
                self.mdb.models['Model-1'].fieldOutputRequests['Reaction_Part_A'].move('Loading', 'Pre-Stress')
                self.mdb.models['Model-1'].fieldOutputRequests['Reaction_Part_B'].move('Loading', 'Pre-Stress')
                self.mdb.models['Model-1'].historyOutputRequests['H-Output-1'].move('Loading', 'Pre-Stress')

                a = self.mdb.models['Model-1'].rootAssembly
                region = a.instances['Test_Article-1'].surfaces['OD_Surf']
                self.mdb.models['Model-1'].Pressure(name='Pre-Stress_Pressure',
                    createStepName='Pre-Stress', region=region, distributionType=UNIFORM,
                    field='', magnitude=self.bcTaPreStress, amplitude='Std-Indent-%s'%(self.ampFunction))

                region = a.instances['Test_Article-1'].sets['Top_Set']
                self.mdb.models['Model-1'].DisplacementBC(name='TA_Top_Axial-Fixed_BC',
                    createStepName='Initial', region=region, u1=UNSET, u2=0.0, ur3=UNSET,
                    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
                self.mdb.models['Model-1'].boundaryConditions['TA_Top_Axial-Fixed_BC'].deactivate('Loading')
                self.mdb.models['Model-1'].boundaryConditions['TA_Bottom_Axial-Fixed_BC'].move('Initial', 'Loading')

            else:

                a = self.mdb.models['Model-1'].rootAssembly
                region = a.instances['Test_Article-1'].sets['Set-1']
                self.mdb.models['Model-1'].Stress(name='Bi-Axial Pre-Stress', region=region,
                    distributionType=UNIFORM, sigma11=self.bcTaPreStress, sigma22=0.0, sigma33=self.bcTaPreStress, sigma12=0.0, sigma13=0.0, sigma23=0.0)

        elif self.anSolverType.startswith('Explicit'):

            self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Pre-Stress', previous='Initial', timePeriod=self.anTimeStep[0])
            self.mdb.models['Model-1'].steps['Pre-Stress'].setValues(linearBulkViscosity=self.anBulkViscosity[0])
            self.mdb.models['Model-1'].steps['Pre-Stress'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)
            self.mdb.models['Model-1'].steps['Pre-Stress'].setValues(massScaling=((SEMI_AUTOMATIC, MODEL, THROUGHOUT_STEP, 0.0, 1.0, BELOW_MIN, 100, 0, 0.0, 0.0, 0, None), ))

            self.mdb.models['Model-1'].fieldOutputRequests['Contact_Results'].move('Loading', 'Pre-Stress')
            self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].move('Loading', 'Pre-Stress')
            self.mdb.models['Model-1'].fieldOutputRequests['Plastic_Zone'].move('Loading', 'Pre-Stress')
            self.mdb.models['Model-1'].fieldOutputRequests['Reaction_Part_A'].move('Loading', 'Pre-Stress')
            self.mdb.models['Model-1'].fieldOutputRequests['Reaction_Part_B'].move('Loading', 'Pre-Stress')
            self.mdb.models['Model-1'].historyOutputRequests['H-Output-1'].move('Loading', 'Pre-Stress')

            a = self.mdb.models['Model-1'].rootAssembly
            region = a.instances['Test_Article-1'].surfaces['OD_Surf']
            self.mdb.models['Model-1'].Pressure(name='Pre-Stress_Pressure',
                createStepName='Pre-Stress', region=region, distributionType=UNIFORM,
                field='', magnitude=self.bcTaPreStress, amplitude='Exp-Indent-Smooth')

            region = a.instances['Test_Article-1'].sets['Top_Set']
            self.mdb.models['Model-1'].DisplacementBC(name='TA_Top_Axial-Fixed_BC',
                createStepName='Initial', region=region, u1=UNSET, u2=0.0, ur3=UNSET,
                amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
            self.mdb.models['Model-1'].boundaryConditions['TA_Top_Axial-Fixed_BC'].deactivate('Loading')
            self.mdb.models['Model-1'].boundaryConditions['TA_Bottom_Axial-Fixed_BC'].move('Initial', 'Loading')

        return(None)

    #-----------------------------------------------------------------------

    def createJob(self,*args,**kwargs):

        self.anJobName = kwargs.get('anJobName',None)
        self.anCPUs = kwargs.get('anCPUs',None)
        self.anFortranfileName = kwargs.get('anFortranfileName',None)

        doublePrecision = kwargs.get('doublePrecision',False)
        jobSubmit = kwargs.get('jobSubmit',False)
        inpFile = kwargs.get('inpFile',False)

        from caeModules import job

        self.mdb.Job(name=self.anJobName, model='Model-1', description='',
            type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
            memory=90, memoryUnits=PERCENTAGE, explicitPrecision=SINGLE,
            nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF,
            contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='',
            resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=self.anCPUs,
            activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=self.anCPUs)

        if (self.anFortranfileName is not None) and (self.anFortranfileName != ''):

            self.mdb.jobs[self.anJobName].setValues(userSubroutine=self.anFortranfileName)

        if doublePrecision:

            self.mdb.jobs[self.anJobName].setValues(explicitPrecision=DOUBLE)

        if jobSubmit:

            self.mdb.jobs[self.anJobName].submit(consistencyChecking=OFF)

            # self.mdb.job.waitForCompletion()

        elif inpFile:

            self.mdb.jobs[self.anJobName].writeInput(consistencyChecking=OFF)

            if True: # Needs to updated with an additional boolean variable...

                with open(os.path.join(os.getcwd(),self.anJobName+'.inp'), 'r') as tempFile: fileData = tempFile.read()

                fileData = fileData.replace('LE, S', 'COORD, LE, S')

                with open(os.path.join(os.getcwd(),self.anJobName+'.inp'), 'w') as tempFile: tempFile.write(fileData)

        return(None)

    #-----------------------------------------------------------------------

    def setView(self,*args,**kwargs):

        from abaqus import session

        a = self.mdb.models['Model-1'].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        if self.mdb.models['Model-1'].parts['Test_Article'].space == AXISYMMETRIC: session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
        else: session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
        session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
        session.viewports['Viewport: 1'].view.fitView()
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
        session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=ON)

        return(None)

    #-----------------------------------------------------------------------

    def expectedDepthForce(self,*args,**kwargs):

        self.anJobName = kwargs.get('anJobName',None)
        self.bcIndForce = kwargs.get('bcIndForce',None)

        print('Predicting Indenter Depth for Force (%s) in Job (%s)...' %(self.bcIndForce,self.anJobName))
        sys.__stdout__.write('Predicting Indenter Depth for Force (%s) in Job (%s)...' %(self.bcIndForce,self.anJobName))

        tempCSVname = [tempFileName for tempFileName in os.listdir(os.getcwd()) if (tempFileName.endswith('.csv')) and ((self.anJobName+'_pre_RF_Work_Ind' in tempFileName) or (self.anJobName+'_pre_upg_RF_Work_Ind' in tempFileName))][0]

        with open(tempCSVname, 'rb') as tempFile:

            tempReader = csv.reader(tempFile)

            for row in tempReader:

                if row[0] == 'Loading':

                    print('Step: %s, Disp: %s, Force: %s' %(row[0],row[16],row[22]))

                    print('  Desired Force: %s'%(self.bcIndForce))

                    if float(row[22]) > self.bcIndForce:

                        highValues = [float(row[16]),float(row[22])]

                        break

                    lowValues = [float(row[16]),float(row[22])]

        try:

            bcIndDepth = ((highValues[0]-lowValues[0])/(highValues[1]-lowValues[1])) * (self.bcIndForce-lowValues[1]) + lowValues[0]

        except:

            raise ValueError('The pre-analysis must have a greater depth.')
            sys.__stdout__.write('The pre-analysis must have a greater depth.')

        print('Predicted Indenter Depth: %s' %(bcIndDepth))
        sys.__stdout__.write('Predicted Indenter Depth: %s' %(bcIndDepth))

        return(bcIndDepth)

    #-----------------------------------------------------------------------

    def expectedDepthEnergy(self,*args,**kwargs):

        self.anJobName = kwargs.get('anJobName',None)
        self.bcIndEnergy = kwargs.get('bcIndEnergy',None)

        print('Predicting Indenter Depth for Energy (%s) in Job (%s)...' %(self.bcIndEnergy,self.anJobName))
        sys.__stdout__.write('Predicting Indenter Depth for Energy (%s) in Job (%s)...' %(self.bcIndEnergy,self.anJobName))

        tempCSVname = [tempFileName for tempFileName in os.listdir(os.getcwd()) if (tempFileName.endswith('.csv')) and ((self.anJobName+'_pre_RF_Work_Ind' in tempFileName) or (self.anJobName+'_pre_upg_RF_Work_Ind' in tempFileName))][0]

        with open(tempCSVname, 'rb') as tempFile:

            tempReader = csv.reader(tempFile)

            for row in tempReader:

                if row[0] == 'Loading':

                    print('Step: %s, Disp: %s, Energy: %s' %(row[0],row[16],row[24]))

                    print('  Desired Energy: %s'%(self.bcIndEnergy))

                    if float(row[24]) > self.bcIndEnergy:

                        highValues = [float(row[16]),float(row[24])]

                        break

                    lowValues = [float(row[16]),float(row[24])]

        try:

            bcIndDepth = ((highValues[0]-lowValues[0])/(highValues[1]-lowValues[1])) * (self.bcIndEnergy-lowValues[1]) + lowValues[0]

        except:

            raise ValueError('The pre-analysis must have a greater depth.')
            sys.__stdout__.write('The pre-analysis must have a greater depth.')

        print('Predicted Indenter Depth: %s' %(bcIndDepth))
        sys.__stdout__.write('Predicted Indenter Depth: %s' %(bcIndDepth))

        return(bcIndDepth)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

class ASym_Analysis(General_Analysis):

    #-----------------------------------------------------------------------

    def __init__(self,*args,**kwargs):

        return(None)

    #-----------------------------------------------------------------------

    def createInteractions(self,*args,**kwargs):

        self.contFriciton = kwargs.get('contFriciton',None)
        self.contType = kwargs.get('contType',None)

        self.partIndType = kwargs.get('partIndType',None)
        self.partIndMass = kwargs.get('partIndMass',None)

        from caeModules import interaction

        if self.partIndType == 'Rigid':

            region1=self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
            region2=self.mdb.models['Model-1'].rootAssembly.instances['Indenter-1'].surfaces['Contact_Master_Surf']
            self.mdb.models['Model-1'].RigidBody(name='Analytic_Rigid', refPointRegion=region1, surfaceRegion=region2)

            region=self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
            self.mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(name='Indenter_Point_Mass', region=region, mass=self.partIndMass, alpha=0.0, composite=0.0)

        elif self.partIndType == 'Deformable':

            region1=self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
            region2=self.mdb.models['Model-1'].rootAssembly.instances['Indenter-1'].sets['Top_Set']
            self.mdb.models['Model-1'].Coupling(name='Indenter_Coupling', controlPoint=region1,
                surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
                localCsys=None, u1=ON, u2=ON, ur3=ON)

        self.mdb.models['Model-1'].ContactProperty('FrictionCoeff_' + ('%0.2f'%self.contFriciton).replace('.','-'))
        self.mdb.models['Model-1'].interactionProperties['FrictionCoeff_' + ('%0.2f'%self.contFriciton).replace('.','-')].NormalBehavior(pressureOverclosure=HARD, allowSeparation=ON, constraintEnforcementMethod=DEFAULT)
        self.mdb.models['Model-1'].interactionProperties['FrictionCoeff_' + ('%0.2f'%self.contFriciton).replace('.','-')].TangentialBehavior(formulation=FRICTIONLESS)

        self.mdb.models['Model-1'].interactionProperties['FrictionCoeff_' + ('%0.2f'%self.contFriciton).replace('.','-')].TangentialBehavior(
            formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, pressureDependency=OFF, temperatureDependency=OFF, dependencies=0,
            table=((self.contFriciton, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, fraction=0.005, elasticSlipStiffness=None)

        if self.anSolverType.startswith('Standard'):

            if self.contType == 'Surface':

                region1=self.mdb.models['Model-1'].rootAssembly.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                region2=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].surfaces['Contact_Slave_Surf']
                self.mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='Surface_Contact',
                    createStepName='Initial', master=region1, slave=region2, sliding=FINITE,
                    thickness=ON, contactTracking=ONE_CONFIG, interactionProperty='FrictionCoeff_'+('%0.2f'%self.contFriciton).replace('.','-'), adjustMethod=NONE,
                    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

            elif self.contType == 'Node':

                region1=self.mdb.models['Model-1'].rootAssembly.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                region2=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].sets['Node_Contact_Set']
                self.mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='Indenter_Node_Contact',
                    createStepName='Initial', master=region1, slave=region2, sliding=FINITE,
                    enforcement=NODE_TO_SURFACE, thickness=OFF,
                    interactionProperty='FrictionCoeff_'+('%0.2f'%self.contFriciton).replace('.','-'), surfaceSmoothing=NONE,
                    adjustMethod=NONE, smooth=0.2, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

            elif self.contType == 'General':

                self.mdb.models['Model-1'].ContactStd(name='General Contact', createStepName='Initial')
                self.mdb.models['Model-1'].interactions['General Contact'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)
                self.mdb.models['Model-1'].interactions['General Contact'].contactPropertyAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, SELF, 'FrictionCoeff_'+('%0.2f'%self.contFriciton).replace('.','-')), ))
                r12=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].surfaces['Contact_Slave_Surf']
                self.mdb.models['Model-1'].interactions['General Contact'].masterSlaveAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, r12, MASTER), ))

        elif self.anSolverType.startswith('Explicit'):

            if self.contType == 'Surface':

                region1=self.mdb.models['Model-1'].rootAssembly.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                region2=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].surfaces['Contact_Slave_Surf']
                self.mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Indenter_Surf_Contact',
                    createStepName='Initial', master = region1, slave = region2, mechanicalConstraint=KINEMATIC, sliding=FINITE,
                    interactionProperty='FrictionCoeff_'+('%0.2f'%self.contFriciton).replace('.','-'), initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

            elif self.contType == 'Node':

                region1=self.mdb.models['Model-1'].rootAssembly.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                region2=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].sets['Node_Contact_Set']
                self.mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Indenter_Node_Contact', createStepName='Initial', master = region1, slave = region2,
                    mechanicalConstraint=KINEMATIC, sliding=FINITE, interactionProperty='FrictionCoeff_'+('%0.2f'%self.contFriciton).replace('.','-'), initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

            elif self.contType == 'General':

                self.mdb.models['Model-1'].ContactExp(name='General Contact', createStepName='Initial')
                self.mdb.models['Model-1'].interactions['General Contact'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)
                self.mdb.models['Model-1'].interactions['General Contact'].contactPropertyAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, SELF, 'FrictionCoeff_'+('%0.2f'%self.contFriciton).replace('.','-')), ))
                r12=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].surfaces['Contact_Slave_Surf']
                self.mdb.models['Model-1'].interactions['General Contact'].masterSlaveAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, r12, MASTER), ))

        if self.anGeomType == 'AsymPillar':

            if self.anSolverType.startswith('Standard'):

                a = self.mdb.models['Model-1'].rootAssembly
                region=a.instances['Test_Article-1'].surfaces['Self_Contact_Surf']
                self.mdb.models['Model-1'].SelfContactStd(name='Test_Article_Self_Contact', createStepName='Initial', surface=region, interactionProperty='FrictionCoeff_0-00', thickness=ON)
                # self.mdb.models['Model-1'].interactions['Test_Article_Self_Contact'].setValues(enforcement=NODE_TO_SURFACE, thickness=OFF, smooth=0.2, supplementaryContact=SELECTIVE)
                # self.mdb.models['Model-1'].interactions['Test_Article_Self_Contact'].setValues(enforcement=NODE_TO_SURFACE, thickness=OFF, smooth=0.2, supplementaryContact=NEVER)
                self.mdb.models['Model-1'].interactions['Test_Article_Self_Contact'].setValues(enforcement=NODE_TO_SURFACE, thickness=OFF, smooth=0.2, supplementaryContact=ALWAYS)

            elif self.anSolverType.startswith('Explicit'):

                pass ############### Not done yet (not necessary yet)

        return(None)

    #-----------------------------------------------------------------------

    def createLoadsBCs(self,*args,**kwargs):

        self.bcType = kwargs.get('bcType',None)

        self.bcIndDepth = kwargs.get('bcIndDepth',None)
        self.bcIndForce = kwargs.get('bcIndForce',None)
        self.bcIndVelocity = kwargs.get('bcIndVelocity',None)

        self.ampFunction = kwargs.get('ampFunction','Tabular') #Currently, only the default is used.

        from caeModules import load

        region = self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].sets['Center-Line_Set']
        self.mdb.models['Model-1'].DisplacementBC(name='TA_Center-Line_BC', createStepName='Initial',
            region=region, u1=SET, u2=UNSET, ur3=UNSET, amplitude=UNSET,
            distributionType=UNIFORM, fieldName='', localCsys=None)

        region = self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].sets['Base_Set']
        self.mdb.models['Model-1'].DisplacementBC(name='TA_Bottom_Axial-Fixed_BC',
            createStepName='Initial', region=region, u1=UNSET, u2=SET, ur3=UNSET,
            amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

        if self.partIndType == 'Deformable':

            region = self.mdb.models['Model-1'].rootAssembly.instances['Indenter-1'].sets['Center-Line_Set']
            self.mdb.models['Model-1'].DisplacementBC(name='Ind_Center-Line_BC', createStepName='Initial',
                region=region, u1=SET, u2=UNSET, ur3=UNSET, amplitude=UNSET,
                distributionType=UNIFORM, fieldName='', localCsys=None)

        if self.anSolverType.startswith('Standard'):

            if self.bcType == 'Force':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=SET, ur3=SET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Loading', u2=FREED)
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Unloading', u2=0.0)

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].ConcentratedForce(name='Indenter_Force', createStepName='Loading', region=region, cf2=-self.bcIndForce, amplitude='Std-Indent-%s'%(self.ampFunction), distributionType=UNIFORM, field='', localCsys=None)
                self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Unloading', cf2=-self.bcIndForce, amplitude='Std-Remove-%s'%(self.ampFunction))

            elif self.bcType == 'Displacement':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=SET, ur3=SET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Loading', u2=-self.bcIndDepth, amplitude='Std-Indent-%s'%(self.ampFunction))
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Unloading', u2=-self.bcIndDepth, amplitude='Std-Remove-%s'%(self.ampFunction))

            elif self.bcType == 'InitialVelocity':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].VelocityBC(name='Initial_Velocity', createStepName='Loading', region=region, v1=UNSET, v2=-self.bcIndVelocity, vr3=UNSET, amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')

        elif self.anSolverType.startswith('Explicit'):

            self.ampFunction = 'Smooth'

            if self.bcType == 'Force':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET,fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
                self.mdb.models['Model-1'].ConcentratedForce(name='Indenter_Force', createStepName='Loading', region=region, cf2=-self.bcIndForce, amplitude='Exp-Indent-%s'%(self.ampFunction), distributionType=UNIFORM, field='', localCsys=None)

                try: self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Dwell-Loaded', cf2=-self.bcIndForce)
                except: pass

                self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Unloading', cf2=-self.bcIndForce, amplitude='Exp-Remove-%s'%(self.ampFunction))

                try: self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Dwell-Loaded', cf2=0.0)
                except: pass

            elif self.bcType == 'Displacement':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=SET, ur3=SET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Loading', u2=-self.bcIndDepth, amplitude='Exp-Indent-%s'%(self.ampFunction))

                try: self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Dwell-Loaded', u2=0.0)
                except: pass

                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Unloading', u2=-self.bcIndDepth, amplitude='Exp-Remove-%s'%(self.ampFunction))

                try: self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Dwell-Unloaded', u2=0.0)
                except: pass

            elif self.bcType == 'InitialVelocity':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
                self.mdb.models['Model-1'].VelocityBC(name='Initial_Velocity', createStepName='Loading', region=region, v1=UNSET, v2=-self.bcIndVelocity, vr3=UNSET, amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')

        return(None)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

class ASym_Indenter_Analysis(ASym_Analysis):

    #-----------------------------------------------------------------------

    def __init__(self,*args,**kwargs):

        self.anGeomType = args[0]
        self.anSolverType = args[1]

        from abaqus import Mdb

        self.mdb = Mdb()

        return(None)

    #-----------------------------------------------------------------------

    def createCylindricalTestArticle(self,*args,**kwargs):

        self.taL = args[0]
        self.taH = args[1]
        self.articlePart = args[2]
        self.meshSize = args[3]
        self.meshMultiples = args[4]
        self.meshAspectRatio = args[5]

        meshSize0 = self.meshSize
        meshSize1 = meshSize0 * self.meshMultiples[0]
        meshSize2 = meshSize1 * self.meshMultiples[1]
        meshSize3 = meshSize2 * self.meshMultiples[2]
        meshSize4 = meshSize3 * self.meshMultiples[3]

        from caeModules import part

        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.rectangle(point1=(0.0, 0.0), point2=(self.taL, -self.taH))
        self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Cylindrical_Test_Article_Sketch')
        s.unsetPrimaryObject()

        s1 = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.sketchOptions.setValues(viewStyle=AXISYM)
        s1.setPrimaryObject(option=STANDALONE)
        s1.ConstructionLine(point1=(0.0, -0.5), point2=(0.0, 0.5))
        s1.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['Cylindrical_Test_Article_Sketch'])

        p = self.mdb.models['Model-1'].Part(name='Test_Article', dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.BaseShell(sketch=s1)
        s1.unsetPrimaryObject()
        p = self.mdb.models['Model-1'].parts['Test_Article']
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        faces = p.faces.findAt(((0.0,0.0,0.0),))
        p.Set(faces=faces, name='Set-1')
        edges = p.edges.findAt(((0.0,-5e-6,0.0),))
        p.Set(edges=edges, name='Center-Line_Set')
        edges = p.edges.findAt(((5e-6,0.0,0.0),))
        p.Set(edges=edges, name='Top_Set')
        p.Surface(side1Edges=edges, name='Contact_Slave_Surf')
        edges = p.edges.findAt(((5e-6,-self.taH,0.0),))
        p.Set(edges=edges, name='Base_Set')
        edges = p.edges.findAt(((self.taL,-5e-6,0.0),))
        p.Set(edges=edges, name='OD_Set')
        p.Surface(side1Edges=edges, name='OD_Surf')

        pickedRegions = p.faces.findAt(((0.0,0.0,0.0),))
        p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED, technique=FREE, algorithm=MEDIAL_AXIS)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        f, e, d1 = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.5,gridSpacing=0.01, transform=t)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        s.Line(point1=(self.articlePart[1]*self.taL, 0.0), point2=(self.articlePart[1]*self.taL, -self.taH))
        s.Line(point1=(0.0, -self.articlePart[1]*self.taH), point2=(self.taL, -self.articlePart[1]*self.taH))
        p = self.mdb.models['Model-1'].parts['Test_Article']
        f = p.faces
        pickedFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
        e1, d2 = p.edges, p.datums
        p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
        s.unsetPrimaryObject()
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        edges = p.edges.findAt(((0.0,-5e-6,0.0),))
        p.Set(edges=edges, name='Results_CL_Set')
        edges = p.edges.findAt(((5e-6,0.0,0.0),))
        p.Set(edges=edges, name='Results_Surf_Set')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        faces = p.faces.findAt(((0.0,0.0,0.0),))
        p.Set(faces=faces, name='Remeshing_Set')
        p.Set(faces=faces, name='Mat_Plastic_Set')
        p.Set(faces=faces, name='Node_Contact_Set')
        faces = p.faces.findAt(((self.taL,0.0,0.0),),((0.0,-self.taH,0.0),),((self.taL,-self.taH,0.0),))
        p.Set(faces=faces, name='Mat_Elastic_Set')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        f, e, d1 = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.5,gridSpacing=0.01, transform=t)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        s.Line(point1=(self.articlePart[2]*self.taL, 0.0), point2=(self.articlePart[2]*self.taL, -self.taH))
        s.Line(point1=(0.0, -self.articlePart[2]*self.taH), point2=(self.taL, -self.articlePart[2]*self.taH))
        p = self.mdb.models['Model-1'].parts['Test_Article']
        f = p.faces
        pickedFaces = p.faces.findAt(((self.taL,0.0,0.0),),((0.0,-self.taH,0.0),),((self.taL,-self.taH,0.0),))
        e1, d2 = p.edges, p.datums
        p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
        s.unsetPrimaryObject()
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        f, e, d1 = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.5,gridSpacing=0.01, transform=t)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        s.Line(point1=(self.articlePart[3]*self.taL, 0.0), point2=(self.articlePart[3]*self.taL, -self.taH))
        s.Line(point1=(0.0, -self.articlePart[3]*self.taH), point2=(self.taL, -self.articlePart[3]*self.taH))
        p = self.mdb.models['Model-1'].parts['Test_Article']
        f = p.faces
        pickedFaces = p.faces.findAt(((self.taL,0.0,0.0),),((self.taL,-(self.articlePart[1]*self.taH+5e-6),0.0),),((self.taL,-self.taH,0.0),),((0.0,-self.taH,0.0),),((self.articlePart[1]*self.taL+5e-6,-self.taH,0.0),))
        e1, d2 = p.edges, p.datums
        p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
        s.unsetPrimaryObject()
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        region = p.sets['Mat_Plastic_Set']
        p.SectionAssignment(region=region, sectionName = self.matTaPsModel+'_'+self.matTaName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
        region = p.sets['Mat_Elastic_Set']
        p.SectionAssignment(region=region, sectionName='Elastic_'+self.matTaName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

        from caeModules import mesh

        if self.anSolverType.startswith('Standard'):

            elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=STANDARD)

        elif self.anSolverType.startswith('Explicit'):

            elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        faces = p.faces.getSequenceFromMask(mask=('[#ffff ]', ), )
        pickedRegions =(faces, )
        try: p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
        except: p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))

        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.seedPart(size=meshSize1, deviationFactor=0.1, minSizeFactor=0.1)

        pickedEdges1 = p.edges.getByBoundingBox(xMin=-5e6,yMin=-(self.articlePart[1]*self.taH+5e-6),xMax=5e6,yMax=-(self.articlePart[1]*self.taH-5e-6))
        pickedEdges2 = p.edges.getByBoundingBox(xMin=self.articlePart[1]*self.taL-5e-6,yMin=-5e6,xMax=self.articlePart[1]*self.taL+5e-6,yMax=5e6)
        p.seedEdgeBySize(edges=pickedEdges1+pickedEdges2, size=meshSize1, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        p.Set(edges=pickedEdges1+pickedEdges2, name='Mesh_1_Edge_Seeds')

        pickedEdges1 = p.edges.getByBoundingBox(xMin=-5e6,yMin=-(self.articlePart[2]*self.taH+5e-6),xMax=5e6,yMax=-(self.articlePart[2]*self.taH-5e-6))
        pickedEdges2 = p.edges.getByBoundingBox(xMin=self.articlePart[2]*self.taL-5e-6,yMin=-5e6,xMax=self.articlePart[2]*self.taL+5e-6,yMax=5e6)
        p.seedEdgeBySize(edges=pickedEdges1+pickedEdges2, size=meshSize2, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        p.Set(edges=pickedEdges1+pickedEdges2, name='Mesh_2_Edge_Seeds')

        pickedEdges1 = p.edges.getByBoundingBox(xMin=self.articlePart[3]*self.taL-5e-6,yMin=-(self.articlePart[3]*self.taH+5e-6),xMax=self.articlePart[3]*self.taL+5e-6,yMax=5e-6)
        pickedEdges2 = p.edges.getByBoundingBox(xMin=-5e-6,yMin=-(self.articlePart[3]*self.taH+5e-6),xMax=self.articlePart[3]*self.taL+5e-6,yMax=-(self.articlePart[3]*self.taH-5e-6))
        p.seedEdgeBySize(edges=pickedEdges1+pickedEdges2, size=meshSize3, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        p.Set(edges=pickedEdges1+pickedEdges2, name='Mesh_3_Edge_Seeds')

        pickedEdges1 = p.edges.getByBoundingBox(xMin=self.taL-5e-6,yMin=-(self.taH+5e-6),xMax=self.taL+5e-6,yMax=5e-6)
        pickedEdges2 = p.edges.getByBoundingBox(xMin=-5e-6,yMin=-(self.taH+5e-6),xMax=self.taL+5e-6,yMax=-(self.taH-5e-6))
        p.seedEdgeBySize(edges=pickedEdges1+pickedEdges2, size=meshSize4, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        p.Set(edges=pickedEdges1+pickedEdges2, name='Mesh_4_Edge_Seeds')

        #Horizontal 1 -> 2
        end1Edges = p.edges.findAt(((self.articlePart[1]*self.taL+5e-6,-self.articlePart[1]*self.taH,0.0),))
        end2Edges = p.edges.findAt(((self.articlePart[1]*self.taL+5e-6,0.0,0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize1, maxSize=meshSize2, constraint=FINER)
        p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=end2Edges, minSize=meshSize1, maxSize=meshSize2, constraint=FINER)

        #Vertical 1 -> 2
        end1Edges = p.edges.findAt(((0.0,-(self.articlePart[1]*self.taH+5e-6),0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[1]*self.taL,-(self.articlePart[1]*self.taH+5e-6),0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize1, maxSize=meshSize2, constraint=FINER)

        #Horizontal 2 -> 3
        end1Edges = p.edges.findAt(((self.articlePart[2]*self.taL+5e-6,-self.articlePart[2]*self.taH,0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[2]*self.taL+5e-6,-self.articlePart[1]*self.taH,0.0),))
        end2Edges = p.edges.findAt(((self.articlePart[2]*self.taL+5e-6,0.0,0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize2, maxSize=meshSize3, constraint=FINER)
        p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=end2Edges, minSize=meshSize2, maxSize=meshSize3, constraint=FINER)

        #Vertical 2 -> 3
        end1Edges = p.edges.findAt(((0.0,-(self.articlePart[2]*self.taH+5e-6),0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[1]*self.taL,-(self.articlePart[2]*self.taH+5e-6),0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[2]*self.taL,-(self.articlePart[2]*self.taH+5e-6),0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize2, maxSize=meshSize3, constraint=FINER)

        #Horizontal 3 -> 4
        end1Edges = p.edges.findAt(((self.articlePart[3]*self.taL+5e-6,-self.articlePart[3]*self.taH,0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[3]*self.taL+5e-6,-self.articlePart[2]*self.taH,0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[3]*self.taL+5e-6,-self.articlePart[1]*self.taH,0.0),))
        end2Edges = p.edges.findAt(((self.articlePart[3]*self.taL+5e-6,0.0,0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize3, maxSize=meshSize4, constraint=FINER)
        p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=end2Edges, minSize=meshSize3, maxSize=meshSize4, constraint=FINER)

        #Vertical 3 -> 4
        end1Edges = p.edges.findAt(((0.0,-(self.articlePart[3]*self.taH+5e-6),0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[1]*self.taL,-(self.articlePart[3]*self.taH+5e-6),0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[2]*self.taL,-(self.articlePart[3]*self.taH+5e-6),0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[3]*self.taL,-(self.articlePart[3]*self.taH+5e-6),0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize3, maxSize=meshSize4, constraint=FINER)

        pickedRegions = f.findAt(((self.articlePart[1]*self.taL+5e-6, 0.0, 0.0), ), ((0.0, -(self.articlePart[1]*self.taH+5e-6), 0.0), ))
        p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED, technique=FREE, algorithm=ADVANCING_FRONT, allowMapped=True)

        pickedRegions = f.findAt(((self.articlePart[1]*self.taL+5e-6, -(self.articlePart[1]*self.taH+5e-6), 0.0), ))
        p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED, technique=FREE, algorithm=ADVANCING_FRONT, allowMapped=False)

        #---New Stuff-----------------------------------------------------------------
        f = self.mdb.models['Model-1'].parts['Test_Article'].faces
        pickedRegions = f.findAt(((5e-6, -5e-6, 0.0), ))
        p.setMeshControls(regions=pickedRegions, technique=SWEEP)

        e = self.mdb.models['Model-1'].parts['Test_Article'].edges
        pickedEdges = e.findAt(((self.articlePart[0]*self.taL, -5e-6, 0.0), ), ((0.0, -5e-6, 0.0), ))
        p.seedEdgeBySize(edges=pickedEdges, size=1.0*meshSize0, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)

        if not self.meshAspectRatio == 1.0:

            e = self.mdb.models['Model-1'].parts['Test_Article'].edges
            pickedEdges1 = e.findAt(((0.0, -5e-6, 0.0), ))
            p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, minSize=meshSize0/2.0, maxSize=meshSize0, constraint=FINER)
            pickedEdges1 = e.findAt(((self.articlePart[0]*self.taL, -5e-6, 0.0), ))
            p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, minSize=meshSize0/2.0, maxSize=meshSize0, constraint=FINER)

        p.generateMesh()

        return(None)

    #-----------------------------------------------------------------------

    def createAlternateCylindricalTestArticle(self,*args,**kwargs):

        self.taL = args[0]
        self.taH = args[1]
        self.articlePart = args[2]
        self.meshSize = args[3]
        self.meshMultiples = args[4]
        self.meshAspectRatio = args[5]

        meshSize0 = self.meshSize
        meshSize1 = meshSize0 * self.meshMultiples[0]
        meshSize2 = meshSize1 * self.meshMultiples[1]
        meshSize3 = meshSize2 * self.meshMultiples[2]
        meshSize4 = meshSize3 * self.meshMultiples[3]

        from caeModules import part

        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.rectangle(point1=(0.0, 0.0), point2=(self.taL, -self.taH))
        self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Cylindrical_Test_Article_Sketch')
        s.unsetPrimaryObject()

        s1 = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.sketchOptions.setValues(viewStyle=AXISYM)
        s1.setPrimaryObject(option=STANDALONE)
        s1.ConstructionLine(point1=(0.0, -0.5), point2=(0.0, 0.5))
        s1.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['Cylindrical_Test_Article_Sketch'])

        p = self.mdb.models['Model-1'].Part(name='Test_Article', dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.BaseShell(sketch=s1)
        s1.unsetPrimaryObject()
        p = self.mdb.models['Model-1'].parts['Test_Article']
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        faces = p.faces.findAt(((0.0,0.0,0.0),))
        p.Set(faces=faces, name='Set-1')
        p.Set(faces=faces, name='Mat_Elastic_Set')
        edges = p.edges.findAt(((0.0,-5e-6,0.0),))
        p.Set(edges=edges, name='Center-Line_Set')
        edges = p.edges.findAt(((5e-6,0.0,0.0),))
        p.Set(edges=edges, name='Top_Set')
        p.Surface(side1Edges=edges, name='Contact_Slave_Surf')
        edges = p.edges.findAt(((5e-6,-self.taH,0.0),))
        p.Set(edges=edges, name='Base_Set')
        edges = p.edges.findAt(((self.taL,-5e-6,0.0),))
        p.Surface(side1Edges=edges, name='OD_Surf')

        from caeModules import mesh

        if self.anSolverType.startswith('Standard'):

            elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=STANDARD)

        elif self.anSolverType.startswith('Explicit'):

            elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        # faces = p.faces.getSequenceFromMask(mask=('[#ffff ]', ), )
        faces = p.faces.findAt(((5e-6,-5e-6,0.0),))
        pickedRegions =(faces, )
        try: p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
        except: p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))

        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.seedPart(size=meshSize1, deviationFactor=0.1, minSizeFactor=0.1)

        pickedRegions = p.faces.findAt(((5e-6,-5e-6,0.0),))
        p.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=FREE, algorithm=MEDIAL_AXIS, minTransition=OFF)
        # p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED, technique=FREE, algorithm=MEDIAL_AXIS)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        f, e, d1 = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.5,gridSpacing=0.01, transform=t)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        s.Line(point1=(self.articlePart[3]*self.taL, 0.0), point2=(self.articlePart[3]*self.taL, -self.taH))
        s.Line(point1=(0.0, -self.articlePart[3]*self.taH), point2=(self.taL, -self.articlePart[3]*self.taH))
        p = self.mdb.models['Model-1'].parts['Test_Article']
        f = p.faces
        pickedFaces = p.faces.findAt(((5e-6,-5e-6,0.0),))
        e1, d2 = p.edges, p.datums
        p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
        s.unsetPrimaryObject()
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        f, e, d1 = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.5,gridSpacing=0.01, transform=t)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        s.Line(point1=(self.articlePart[2]*self.taL, 0.0), point2=(self.articlePart[2]*self.taL, -self.taH))
        s.Line(point1=(0.0, -self.articlePart[2]*self.taH), point2=(self.taL, -self.articlePart[2]*self.taH))
        p = self.mdb.models['Model-1'].parts['Test_Article']
        f = p.faces
        pickedFaces = p.faces.findAt(((5e-6,-5e-6,0.0),))
        e1, d2 = p.edges, p.datums
        p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
        s.unsetPrimaryObject()
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        f, e, d1 = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.5,gridSpacing=0.01, transform=t)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        s.Line(point1=(self.articlePart[1]*self.taL, 0.0), point2=(self.articlePart[1]*self.taL, -self.taH))
        s.Line(point1=(0.0, -self.articlePart[1]*self.taH), point2=(self.taL, -self.articlePart[1]*self.taH))
        p = self.mdb.models['Model-1'].parts['Test_Article']
        f = p.faces
        pickedFaces = p.faces.findAt(((5e-6,-5e-6,0.0),))
        e1, d2 = p.edges, p.datums
        p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
        s.unsetPrimaryObject()
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        edges = p.edges.findAt(((0.0,-5e-6,0.0),))
        p.Set(edges=edges, name='Results_CL_Set')
        edges = p.edges.findAt(((5e-6,0.0,0.0),))
        p.Set(edges=edges, name='Results_Surf_Set')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        faces = p.faces.findAt(((0.0,0.0,0.0),))
        p.Set(faces=faces, name='Remeshing_Set')
        p.Set(faces=faces, name='Mat_Plastic_Set')
        p.Set(faces=faces, name='Node_Contact_Set')
        faces = f.getSequenceFromMask(mask=('[#3fe ]', ), )
        p.Set(faces=faces, name='Mat_Elastic_Set')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        edges = p.edges.findAt(((0.0,-5e-6,0.0),),((5e-6,0.0,0.0),),((5e-6,-self.articlePart[1]*self.taL,0.0),),((self.articlePart[1]*self.taL,-5e-6,0.0),))
        p.seedEdgeBySize(edges=edges, size=meshSize1, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        p.Set(edges=edges, name='Mesh_1_Edge_Seeds')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        edges1 = p.edges.findAt(((self.articlePart[2]*self.taL,-5e-6,0.0),),((self.articlePart[2]*self.taL,-self.articlePart[2]*self.taL+5e-6,0.0),))
        edges2 = p.edges.findAt(((5e-6,-self.articlePart[2]*self.taL,0.0),),((self.articlePart[2]*self.taL-5e-6,-self.articlePart[2]*self.taL,0.0),))
        p.seedEdgeBySize(edges=edges1+edges2, size=meshSize2, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        p.Set(edges=edges1+edges2, name='Mesh_2_Edge_Seeds')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        edges1 = p.edges.findAt(((self.articlePart[3]*self.taL,-5e-6,0.0),),((self.articlePart[3]*self.taL,-self.articlePart[3]*self.taL+5e-6,0.0),))
        edges2 = p.edges.findAt(((5e-6,-self.articlePart[3]*self.taL,0.0),),((self.articlePart[3]*self.taL-5e-6,-self.articlePart[3]*self.taL,0.0),))
        p.seedEdgeBySize(edges=edges1+edges2, size=meshSize3, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        p.Set(edges=edges1+edges2, name='Mesh_3_Edge_Seeds')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        edges1 = p.edges.findAt(((self.taL,-5e-6,0.0),),((self.taL,-self.taL+5e-6,0.0),))
        edges2 = p.edges.findAt(((5e-6,-self.taL,0.0),),((self.taL-5e-6,-self.taL,0.0),))
        p.seedEdgeBySize(edges=edges1+edges2, size=meshSize4, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        p.Set(edges=edges1+edges2, name='Mesh_4_Edge_Seeds')

        #Horizontal 1 -> 2
        end1Edges = p.edges.findAt(((self.articlePart[1]*self.taL+5e-6,-self.articlePart[1]*self.taH,0.0),))
        end2Edges = p.edges.findAt(((self.articlePart[1]*self.taL+5e-6,0.0,0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize1, maxSize=meshSize2, constraint=FINER)
        p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=end2Edges, minSize=meshSize1, maxSize=meshSize2, constraint=FINER)

        #Vertical 1 -> 2
        end1Edges = p.edges.findAt(((0.0,-(self.articlePart[1]*self.taH+5e-6),0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[1]*self.taL,-(self.articlePart[1]*self.taH+5e-6),0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize1, maxSize=meshSize2, constraint=FINER)

        #Horizontal 2 -> 3
        end1Edges = p.edges.findAt(((self.articlePart[2]*self.taL+5e-6,-self.articlePart[2]*self.taH,0.0),))
        end2Edges = p.edges.findAt(((self.articlePart[2]*self.taL+5e-6,0.0,0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize2, maxSize=meshSize3, constraint=FINER)
        p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=end2Edges, minSize=meshSize2, maxSize=meshSize3, constraint=FINER)

        #Vertical 2 -> 3
        end1Edges = p.edges.findAt(((0.0,-(self.articlePart[2]*self.taH+5e-6),0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[2]*self.taL,-(self.articlePart[2]*self.taH+5e-6),0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize2, maxSize=meshSize3, constraint=FINER)

        #Horizontal 3 -> 4
        end1Edges = p.edges.findAt(((self.articlePart[3]*self.taL+5e-6,-self.articlePart[3]*self.taH,0.0),))
        end2Edges = p.edges.findAt(((self.articlePart[3]*self.taL+5e-6,0.0,0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize3, maxSize=meshSize4, constraint=FINER)
        p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=end2Edges, minSize=meshSize3, maxSize=meshSize4, constraint=FINER)

        #Vertical 3 -> 4
        end1Edges = p.edges.findAt(((0.0,-(self.articlePart[3]*self.taH+5e-6),0.0),))
        end1Edges = end1Edges + p.edges.findAt(((self.articlePart[3]*self.taL,-(self.articlePart[3]*self.taH+5e-6),0.0),))
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize3, maxSize=meshSize4, constraint=FINER)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        pickedRegions = p.faces.findAt(((0.0,0.0,0.0),))
        p.setMeshControls(regions=pickedRegions, technique=SWEEP)
        pickedRegions = p.faces.findAt(((self.articlePart[1]*self.taL+5e-6,0.0,0.0),),((0.0,-self.articlePart[1]*self.taL-5e-6,0.0),),((self.articlePart[1]*self.taL+5e-6,-self.articlePart[1]*self.taL-5e-6,0.0),))
        p.setMeshControls(regions=pickedRegions, algorithm=ADVANCING_FRONT)
        # pickedRegions = p.faces.findAt(((self.articlePart[3]*self.taL+5e-6,0.0,0.0),),((0.0,-self.articlePart[3]*self.taL-5e-6,0.0),),((self.articlePart[3]*self.taL+5e-6,-self.articlePart[3]*self.taL-5e-6,0.0),))
        pickedRegions = p.faces.findAt(((self.articlePart[3]*self.taL+5e-6,0.0,0.0),),((0.0,-self.articlePart[3]*self.taL-5e-6,0.0),))
        p.setMeshControls(regions=pickedRegions, algorithm=ADVANCING_FRONT, allowMapped=False)

        p.generateMesh()

        return(None)

    #-----------------------------------------------------------------------

    def createIndenter(self,*args,**kwargs):

        self.partIndDAngle = kwargs.get('partIndDAngle',None)
        self.iRad = kwargs.get('partIndRadius',None)
        self.iFlat = kwargs.get('partIndFlat',None)

        indMeshMultiples = kwargs.get('indMeshMultiples',[1.0,100.0])
        charIndSizeFactor = kwargs.get('charIndSizeFactor',0.5)

        from caeModules import part, mesh

        self.iAng = np.radians(self.partIndDAngle)

        if self.partIndType == 'Rigid':

            self.charIndSize = 1.00 * self.articlePart[1]*self.taL

            if (self.iRad is None) or (self.iRad == 0.0):

                print('Creating Sharp Tip Analytic Indenter\n')

                s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                s.setPrimaryObject(option=STANDALONE)
                s.ConstructionLine(point1=(0.0, 10.0), point2=(0.0, -10.0))
                s.Line(point1=(0.0, 0.0), point2=(self.charIndSize*np.sin(self.iAng),self.charIndSize*np.cos(self.iAng)))
                self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Analytic_Indenter_Sketch')
                s.unsetPrimaryObject()

                s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                s.sketchOptions.setValues(viewStyle=AXISYM)
                s.setPrimaryObject(option=STANDALONE)
                s.ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
                s.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['Analytic_Indenter_Sketch'])

                p = self.mdb.models['Model-1'].Part(name='Analytic_Indenter', dimensionality=AXISYMMETRIC, type=ANALYTIC_RIGID_SURFACE)
                p = self.mdb.models['Model-1'].parts['Analytic_Indenter']
                p.AnalyticRigidSurf2DPlanar(sketch=s)
                s.unsetPrimaryObject()
                p = self.mdb.models['Model-1'].parts['Analytic_Indenter']
                del self.mdb.models['Model-1'].sketches['__profile__']

                p = self.mdb.models['Model-1'].parts['Analytic_Indenter']
                s = p.edges
                side2Edges = s.getSequenceFromMask(mask=('[#1 ]', ), )
                p.Surface(side2Edges=side2Edges, name='Contact_Master_Surf')

            elif self.iRad > 0.0:

                if self.iFlat > 0.0:

                    print('Creating Flat + Radius Tip Analytic Indenter\n')

                    self.iRadAng = np.pi/2.0 - self.iAng

                    s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                    s.setPrimaryObject(option=STANDALONE)
                    s.ConstructionLine(point1=(0.0, 10.0), point2=(0.0, -10.0))

                    s.Line(point1=(0.0, 0.0), point2=(self.iFlat,0.0))
                    s.ArcByCenterEnds(center=(0.0+self.iFlat, self.iRad), point1=(0.0+self.iFlat, 0.0), point2=(self.iRad*np.sin(self.iRadAng)+self.iFlat, self.iRad*(1.0-np.cos(self.iRadAng))), direction=COUNTERCLOCKWISE)
                    s.Line(point1=(self.iRad*np.sin(self.iRadAng)+self.iFlat, self.iRad*(1.0-np.cos(self.iRadAng))), point2=(self.iRad*np.sin(self.iRadAng)+self.charIndSize*np.sin(self.iAng)+self.iFlat, self.iRad*(1.0-np.cos(self.iRadAng))+self.charIndSize*np.cos(self.iAng)))

                    self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Analytic_Indenter_Sketch')
                    s.unsetPrimaryObject()

                    s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                    s.sketchOptions.setValues(viewStyle=AXISYM)
                    s.setPrimaryObject(option=STANDALONE)
                    s.ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
                    s.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['Analytic_Indenter_Sketch'])

                    p = self.mdb.models['Model-1'].Part(name='Analytic_Indenter', dimensionality=AXISYMMETRIC, type=ANALYTIC_RIGID_SURFACE)
                    p = self.mdb.models['Model-1'].parts['Analytic_Indenter']
                    p.AnalyticRigidSurf2DPlanar(sketch=s)
                    s.unsetPrimaryObject()
                    p = self.mdb.models['Model-1'].parts['Analytic_Indenter']
                    del self.mdb.models['Model-1'].sketches['__profile__']

                    p = self.mdb.models['Model-1'].parts['Analytic_Indenter']
                    s = p.edges
                    side2Edges = s.getSequenceFromMask(mask=('[#3 ]', ), )
                    p.Surface(side2Edges=side2Edges, name='Contact_Master_Surf')

                else:

                    print('Creating Radius Tip Analytic Indenter\n')

                    self.iRadAng = np.pi/2.0 - self.iAng

                    s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                    s.setPrimaryObject(option=STANDALONE)
                    s.ConstructionLine(point1=(0.0, 10.0), point2=(0.0, -10.0))
                    s.ArcByCenterEnds(center=(0.0, self.iRad), point1=(0.0, 0.0), point2=(self.iRad*np.sin(self.iRadAng), self.iRad*(1.0-np.cos(self.iRadAng))), direction=COUNTERCLOCKWISE)
                    s.Line(point1=(self.iRad*np.sin(self.iRadAng), self.iRad*(1.0-np.cos(self.iRadAng))), point2=(self.iRad*np.sin(self.iRadAng)+self.charIndSize*np.sin(self.iAng), self.iRad*(1.0-np.cos(self.iRadAng))+self.charIndSize*np.cos(self.iAng)))
                    self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Analytic_Indenter_Sketch')
                    s.unsetPrimaryObject()

                    s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                    s.sketchOptions.setValues(viewStyle=AXISYM)
                    s.setPrimaryObject(option=STANDALONE)
                    s.ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
                    s.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['Analytic_Indenter_Sketch'])

                    p = self.mdb.models['Model-1'].Part(name='Analytic_Indenter', dimensionality=AXISYMMETRIC, type=ANALYTIC_RIGID_SURFACE)
                    p = self.mdb.models['Model-1'].parts['Analytic_Indenter']
                    p.AnalyticRigidSurf2DPlanar(sketch=s)
                    s.unsetPrimaryObject()
                    p = self.mdb.models['Model-1'].parts['Analytic_Indenter']
                    del self.mdb.models['Model-1'].sketches['__profile__']

                    p = self.mdb.models['Model-1'].parts['Analytic_Indenter']
                    s = p.edges
                    side2Edges = s.getSequenceFromMask(mask=('[#3 ]', ), )
                    p.Surface(side2Edges=side2Edges, name='Contact_Master_Surf')

        elif self.partIndType == 'Deformable':

            self.charIndSize = charIndSizeFactor * self.taL             #Characteristic Indenter Size (hypotenuse of sharp indenter)

            fineMeshSize = indMeshMultiples[0] * self.meshSize
            coarseMeshSize = indMeshMultiples[1] * self.meshSize

            if (self.iRad is None) or (self.iRad == 0.0):

                print('Creating Sharp Tip Deformable Indenter\n')

                s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                s.setPrimaryObject(option=STANDALONE)
                s.ConstructionLine(point1=(0.0, 10.0), point2=(0.0, -10.0))
                s.Line(point1=(0.0, 0.0), point2=(self.charIndSize*np.sin(self.iAng),self.charIndSize*np.cos(self.iAng)))
                s.Line(point1=(self.charIndSize*np.sin(self.iAng),self.charIndSize*np.cos(self.iAng)), point2=(self.charIndSize*np.sin(self.iAng),1.2*self.charIndSize*np.cos(self.iAng)))
                s.Line(point1=(0.0, 0.0), point2=(0.0,1.2*self.charIndSize*np.cos(self.iAng)))
                s.Line(point1=(0.0,1.2*self.charIndSize*np.cos(self.iAng)), point2=(self.charIndSize*np.sin(self.iAng),1.2*self.charIndSize*np.cos(self.iAng)))
                self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Discrete_Indenter_Sketch')
                s.unsetPrimaryObject()

                s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                s.sketchOptions.setValues(viewStyle=AXISYM)
                s.setPrimaryObject(option=STANDALONE)
                s.ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
                s.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['Discrete_Indenter_Sketch'])
                p = self.mdb.models['Model-1'].Part(name='Deformable_Indenter', dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
                p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                p.BaseShell(sketch=s)
                s.unsetPrimaryObject()
                del self.mdb.models['Model-1'].sketches['__profile__']

                #-----------------------------------------------------------------------

                s = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                side1Edges = s.getSequenceFromMask(mask=('[#2 ]', ), )
                p.Surface(side1Edges=side1Edges, name='Contact_Master_Surf')

                e = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                # print(e.getBoundingBox())
                edges = e.findAt(((5e-6, e.getBoundingBox()['high'][1], 0.0), ))
                p.Set(edges=edges, name='Top_Set')
                edges = e.findAt(((0.0, 5e-6, 0.0), ))
                xVerts = p.vertices.findAt(((0.0, e.getBoundingBox()['high'][1], 0.0), ))
                p.Set(edges=edges, xVertices=xVerts, name='Center-Line_Set')

                p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                faces = p.faces.findAt(((5e-6, 5e-4, 0.0), ))
                region = p.Set(faces=faces, name='Set-1')
                p.SectionAssignment(region=region, sectionName='Elastic_'+self.matIndName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

                p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.50 * self.articlePart[1]*self.taL)
                pickedFaces = p.faces.getSequenceFromMask(mask=('[#1 ]', ), )
                p.PartitionFaceByDatumPlane(datumPlane=p.datums[6], faces=pickedFaces)

                p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.25 * self.articlePart[1]*self.taL)
                pickedFaces = p.faces.getSequenceFromMask(mask=('[#1 ]', ), )
                p.PartitionFaceByDatumPlane(datumPlane=p.datums[8], faces=pickedFaces)

                #----New method for meshing deformable indenters------------------------

                p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                p.seedPart(size=fineMeshSize, deviationFactor=0.1, minSizeFactor=0.1)
                pickedEdges = p.edges.getSequenceFromMask(mask=('[#f ]', ), )
                p.seedEdgeBySize(edges=pickedEdges, size=fineMeshSize, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
                pickedEdges1 = p.edges.getSequenceFromMask(mask=('[#c0 ]', ), )
                pickedEdges2 = p.edges.getSequenceFromMask(mask=('[#10 ]', ), )
                p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=fineMeshSize, maxSize=coarseMeshSize, constraint=FINER)
                pickedEdges = p.edges.getSequenceFromMask(mask=('[#320 ]', ), )
                p.seedEdgeBySize(edges=pickedEdges, size=coarseMeshSize, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)

                #-----------------------------------------------------------------------

            elif self.iRad > 0.0:

                if self.iFlat > 0.0:

                    print('Creating Flat + Radius Tip Deformable Indenter\n')

                    self.iRadAng = np.pi/2.0 - self.iAng

                    s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                    s.setPrimaryObject(option=STANDALONE)
                    s.ConstructionLine(point1=(0.0, 10.0), point2=(0.0, -10.0))

                    s.Line(point1=(0.0, 0.0), point2=(self.iFlat,0.0))
                    s.ArcByCenterEnds(center=(0.0+self.iFlat, self.iRad), point1=(0.0+self.iFlat, 0.0), point2=(self.iRad*np.sin(self.iRadAng)+self.iFlat, self.iRad*(1.0-np.cos(self.iRadAng))), direction=COUNTERCLOCKWISE)
                    s.Line(point1=(self.iRad*np.sin(self.iRadAng)+self.iFlat, self.iRad*(1.0-np.cos(self.iRadAng))), point2=(self.iRad*np.sin(self.iRadAng)+self.charIndSize*np.sin(self.iAng)+self.iFlat, self.iRad*(1.0-np.cos(self.iRadAng))+self.charIndSize*np.cos(self.iAng)))
                    s.Line(point1=(self.iRad*np.sin(self.iRadAng)+self.charIndSize*np.sin(self.iAng)+self.iFlat, self.iRad*(1.0-np.cos(self.iRadAng))+self.charIndSize*np.cos(self.iAng)), point2=(self.iRad*np.sin(self.iRadAng)+self.charIndSize*np.sin(self.iAng)+self.iFlat, self.iRad*(1.0-np.cos(self.iRadAng))+1.2*self.charIndSize*np.cos(self.iAng)))
                    s.Line(point1=(0.0,0.0), point2=(0.0, self.iRad*(1.0-np.cos(self.iRadAng))+1.2*self.charIndSize*np.cos(self.iAng)))
                    s.Line(point1=(0.0, self.iRad*(1.0-np.cos(self.iRadAng))+1.2*self.charIndSize*np.cos(self.iAng)), point2=(self.iRad*np.sin(self.iRadAng)+self.charIndSize*np.sin(self.iAng)+self.iFlat, self.iRad*(1.0-np.cos(self.iRadAng))+1.2*self.charIndSize*np.cos(self.iAng)))

                    self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Discrete_Indenter_Sketch')
                    s.unsetPrimaryObject()

                    s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                    s.sketchOptions.setValues(viewStyle=AXISYM)
                    s.setPrimaryObject(option=STANDALONE)
                    s.ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
                    s.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['Discrete_Indenter_Sketch'])
                    p = self.mdb.models['Model-1'].Part(name='Deformable_Indenter', dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.BaseShell(sketch=s)
                    s.unsetPrimaryObject()
                    del self.mdb.models['Model-1'].sketches['__profile__']

                    #-----------------------------------------------------------------------

                    s = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                    side1Edges = s.getSequenceFromMask(mask=('[#e ]', ), )
                    p.Surface(side1Edges=side1Edges, name='Contact_Master_Surf')

                    e = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                    # print(e.getBoundingBox())
                    edges = e.findAt(((5e-6, e.getBoundingBox()['high'][1], 0.0), ))
                    p.Set(edges=edges, name='Top_Set')
                    edges = e.findAt(((0.0, 5e-6, 0.0), ))
                    xVerts = p.vertices.findAt(((0.0, e.getBoundingBox()['high'][1], 0.0), ))
                    p.Set(edges=edges, xVertices=xVerts, name='Center-Line_Set')

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    faces = p.faces.findAt(((5e-6, 5e-4, 0.0), ))
                    region = p.Set(faces=faces, name='Set-1')
                    p.SectionAssignment(region=region, sectionName='Elastic_'+self.matIndName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.50 * self.articlePart[1]*self.taL)
                    pickedFaces = p.faces.getSequenceFromMask(mask=('[#1 ]', ), )
                    p.PartitionFaceByDatumPlane(datumPlane=p.datums[6], faces=pickedFaces)

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.25 * self.articlePart[1]*self.taL)
                    pickedFaces = p.faces.getSequenceFromMask(mask=('[#1 ]', ), )
                    p.PartitionFaceByDatumPlane(datumPlane=p.datums[8], faces=pickedFaces)

                    #----New method for meshing deformable indenters------------------------

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.seedPart(size=fineMeshSize, deviationFactor=0.1, minSizeFactor=0.1)
                    pickedEdges = p.edges.getSequenceFromMask(mask=('[#3f ]', ), )
                    p.seedEdgeBySize(edges=pickedEdges, size=fineMeshSize, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
                    pickedEdges1 = p.edges.getSequenceFromMask(mask=('[#300 ]', ), )
                    pickedEdges2 = p.edges.getSequenceFromMask(mask=('[#40 ]', ), )
                    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=fineMeshSize, maxSize=coarseMeshSize, constraint=FINER)
                    pickedEdges = p.edges.getSequenceFromMask(mask=('[#c80 ]', ), )
                    p.seedEdgeBySize(edges=pickedEdges, size=coarseMeshSize, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)

                    #-----------------------------------------------------------------------

                else:

                    print('Creating Radius Tip Deformable Indenter\n')

                    self.iRadAng = np.pi/2.0 - self.iAng

                    s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                    s.setPrimaryObject(option=STANDALONE)
                    s.ConstructionLine(point1=(0.0, 10.0), point2=(0.0, -10.0))
                    s.ArcByCenterEnds(center=(0.0, self.iRad), point1=(0.0, 0.0), point2=(self.iRad*np.sin(self.iRadAng), self.iRad*(1.0-np.cos(self.iRadAng))), direction=COUNTERCLOCKWISE)
                    s.Line(point1=(self.iRad*np.sin(self.iRadAng), self.iRad*(1.0-np.cos(self.iRadAng))), point2=(self.iRad*np.sin(self.iRadAng)+self.charIndSize*np.sin(self.iAng), self.iRad*(1.0-np.cos(self.iRadAng))+self.charIndSize*np.cos(self.iAng)))
                    s.Line(point1=(self.iRad*np.sin(self.iRadAng)+self.charIndSize*np.sin(self.iAng), self.iRad*(1.0-np.cos(self.iRadAng))+self.charIndSize*np.cos(self.iAng)), point2=(self.iRad*np.sin(self.iRadAng)+self.charIndSize*np.sin(self.iAng), self.iRad*(1.0-np.cos(self.iRadAng))+1.2*self.charIndSize*np.cos(self.iAng)))
                    s.Line(point1=(0.0,0.0), point2=(0.0, self.iRad*(1.0-np.cos(self.iRadAng))+1.2*self.charIndSize*np.cos(self.iAng)))
                    s.Line(point1=(0.0, self.iRad*(1.0-np.cos(self.iRadAng))+1.2*self.charIndSize*np.cos(self.iAng)), point2=(self.iRad*np.sin(self.iRadAng)+self.charIndSize*np.sin(self.iAng), self.iRad*(1.0-np.cos(self.iRadAng))+1.2*self.charIndSize*np.cos(self.iAng)))
                    self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Discrete_Indenter_Sketch')
                    s.unsetPrimaryObject()

                    s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
                    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                    s.sketchOptions.setValues(viewStyle=AXISYM)
                    s.setPrimaryObject(option=STANDALONE)
                    s.ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
                    s.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['Discrete_Indenter_Sketch'])
                    p = self.mdb.models['Model-1'].Part(name='Deformable_Indenter', dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.BaseShell(sketch=s)
                    s.unsetPrimaryObject()
                    del self.mdb.models['Model-1'].sketches['__profile__']

                    #-----------------------------------------------------------------------

                    s = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                    side1Edges = s.getSequenceFromMask(mask=('[#6 ]', ), )
                    p.Surface(side1Edges=side1Edges, name='Contact_Master_Surf')

                    e = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                    # print e.getBoundingBox()
                    edges = e.findAt(((5e-6, e.getBoundingBox()['high'][1], 0.0), ))
                    p.Set(edges=edges, name='Top_Set')
                    edges = e.findAt(((0.0, 5e-6, 0.0), ))
                    xVerts = p.vertices.findAt(((0.0, e.getBoundingBox()['high'][1], 0.0), ))
                    p.Set(edges=edges, xVertices=xVerts, name='Center-Line_Set')

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    faces = p.faces.findAt(((5e-6, 5e-4, 0.0), ))
                    region = p.Set(faces=faces, name='Set-1')
                    p.SectionAssignment(region=region, sectionName='Elastic_'+self.matIndName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.50 * self.articlePart[1]*self.taL)
                    pickedFaces = p.faces.getSequenceFromMask(mask=('[#1 ]', ), )
                    p.PartitionFaceByDatumPlane(datumPlane=p.datums[6], faces=pickedFaces)

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.25 * self.articlePart[1]*self.taL)
                    pickedFaces = p.faces.getSequenceFromMask(mask=('[#1 ]', ), )
                    p.PartitionFaceByDatumPlane(datumPlane=p.datums[8], faces=pickedFaces)

                    #----New method for meshing deformable indenters------------------------

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.seedPart(size=fineMeshSize, deviationFactor=0.1, minSizeFactor=0.1)
                    pickedEdges = p.edges.getSequenceFromMask(mask=('[#1f ]', ), )
                    p.seedEdgeBySize(edges=pickedEdges, size=fineMeshSize, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
                    pickedEdges1 = p.edges.getSequenceFromMask(mask=('[#180 ]', ), )
                    pickedEdges2 = p.edges.getSequenceFromMask(mask=('[#20 ]', ), )
                    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=fineMeshSize, maxSize=coarseMeshSize, constraint=FINER)
                    pickedEdges = p.edges.getSequenceFromMask(mask=('[#640 ]', ), )
                    p.seedEdgeBySize(edges=pickedEdges, size=coarseMeshSize, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)

                    #-----------------------------------------------------------------------

            f = self.mdb.models['Model-1'].parts['Deformable_Indenter'].faces
            pickedRegions = f.getSequenceFromMask(mask=('[#1 ]', ), )
            p.setMeshControls(regions=pickedRegions, elemShape=QUAD, allowMapped=True)

            if self.anSolverType.startswith('Standard'):

                elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=STANDARD)

            elif self.anSolverType.startswith('Explicit'):

                elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=EXPLICIT)

            faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
            pickedRegions =(faces, )
            p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

            p.generateMesh()

        return(None)

    #-----------------------------------------------------------------------

    def createAssembly(self,*args,**kwargs):

        self.partIndType = kwargs.get('partIndType',None)

        self.bcIndOffset = kwargs.get('bcIndOffset',0.0)

        from caeModules import assembly

        self.mdb.models['Model-1'].rootAssembly.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, -1.0))

        self.mdb.models['Model-1'].rootAssembly.Instance(name='Test_Article-1', part=self.mdb.models['Model-1'].parts['Test_Article'], dependent=ON)

        if self.partIndType == 'Rigid':

            self.mdb.models['Model-1'].rootAssembly.Instance(name='Indenter-1', part=self.mdb.models['Model-1'].parts['Analytic_Indenter'], dependent=ON)
            self.mdb.models['Model-1'].rootAssembly.translate(instanceList=('Indenter-1', ), vector=(0.0, self.bcIndOffset, 0.0))

            rp1Coord = (0.0,self.charIndSize*np.cos(self.iAng) + self.bcIndOffset)

        elif self.partIndType == 'Deformable':

            self.mdb.models['Model-1'].rootAssembly.Instance(name='Indenter-1', part=self.mdb.models['Model-1'].parts['Deformable_Indenter'], dependent=ON)
            self.mdb.models['Model-1'].rootAssembly.translate(instanceList=('Indenter-1', ), vector=(0.0, self.bcIndOffset, 0.0))

            tempYcoord = []
            for node in self.mdb.models['Model-1'].rootAssembly.instances['Indenter-1'].nodes: tempYcoord.append(node.coordinates[1])
            rp1Coord = (0.0,max(tempYcoord))

        self.mdb.models['Model-1'].rootAssembly.ReferencePoint(point=(rp1Coord[0], rp1Coord[1], 0.0))
        refPoints1=(self.mdb.models['Model-1'].rootAssembly.referencePoints[6], )
        self.mdb.models['Model-1'].rootAssembly.Set(referencePoints=refPoints1, name='mSet-1')

        return(None)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

class General_Output(object):

    #-----------------------------------------------------------------------

    def __init__(self):

        return(None)

    #-----------------------------------------------------------------------

    def WholeModelHistory(self,*args,**kwargs):

        ratioValues = kwargs.get('ratioValues', False)

        headerRow = ['Step','Step Time','Total Time']

        for key in self.odb.steps[self.odb.steps.keys()[-1]].historyRegions['Assembly ASSEMBLY'].historyOutputs.keys():

            headerRow.append(key)

        if ratioValues:

            headerRow.append('ALLPD/ALLIE')
            headerRow.append('ALLSE/ALLIE')

        print('Energy Histories - Header Row:\n%s\n' %(headerRow))

        resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'WholeModelHistory' + '.csv')

        tempFile = open(resCSVname, 'wb')

        with open(resCSVname, 'wb') as tempFile:

            csvWriter = csv.writer(tempFile)

            csvWriter.writerow(headerRow)

            for stepName in self.odb.steps.keys():

                print('Processing Step: %s\n' %(stepName))

                try: len(self.odb.steps[stepName].historyRegions['Assembly ASSEMBLY'].historyOutputs['ALLIE'].data)
                except: break

                for i in range(len(self.odb.steps[stepName].historyRegions['Assembly ASSEMBLY'].historyOutputs['ALLIE'].data)):

                    for key in self.odb.steps[stepName].historyRegions['Assembly ASSEMBLY'].historyOutputs.keys():

                        tempData = self.odb.steps[stepName].historyRegions['Assembly ASSEMBLY'].historyOutputs[key].data[i]

                        if key == self.odb.steps[stepName].historyRegions['Assembly ASSEMBLY'].historyOutputs.keys()[0]:

                            tempRow = [stepName, tempData[0], tempData[0]+self.odb.steps[stepName].totalTime]

                        tempRow.append(tempData[1])

                        if ratioValues:

                            if key == 'ALLIE': tempALLIE = self.odb.steps[stepName].historyRegions['Assembly ASSEMBLY'].historyOutputs[key].data[i][1]

                            if key == 'ALLPD': tempALLPD = self.odb.steps[stepName].historyRegions['Assembly ASSEMBLY'].historyOutputs[key].data[i][1]

                            if key == 'ALLSE': tempALLSE = self.odb.steps[stepName].historyRegions['Assembly ASSEMBLY'].historyOutputs[key].data[i][1]

                    if ratioValues:

                        try:

                            tempRow.append(tempALLPD/tempALLIE)
                            tempRow.append(tempALLSE/tempALLIE)

                        except:

                            tempRow.append(0.0)
                            tempRow.append(0.0)

                    # print(tempRow)

                    csvWriter.writerow(tempRow)

        print('Writing CSV File: %s\n\n\n' %(resCSVname))

        return(0)

    #-----------------------------------------------------------------------

    def ContactForceVector(self,*args,**kwargs):

        writeCSV = kwargs.get('writeCSV', True)

        for key in self.odb.steps['Loading'].frames[-1].fieldOutputs.keys():

            if key.startswith('CNORMF'): keyCNORMF = key

            if key.startswith('CSHEARF'): keyCSHEARF = key

        sortedCNORMF = self.GeneralResults(sortedResults=True,sortDirection=1,stepName='Loading',instanceName='TEST_ARTICLE-1',setName='RESULTS_SURF_SET', resultName=keyCNORMF, writeCSV=False)

        sortedCSHEARF = self.GeneralResults(sortedResults=True,sortDirection=1,stepName='Loading',instanceName='TEST_ARTICLE-1',setName='RESULTS_SURF_SET', resultName=keyCSHEARF, writeCSV=False)

        for i in range(len(sortedCNORMF)):

            if sortedCNORMF[i][3] > 0.0 or sortedCNORMF[i][3] > 0.0:

                contactRadius = sortedCNORMF[i][1]

        totalContactForceVector = [0.0,0.0,0.0,0.0,0.0,0.0]

        for i in range(len(sortedCNORMF)):

            totalContactForceVector[0] = totalContactForceVector[0] + sortedCNORMF[i][3]

            totalContactForceVector[1] = totalContactForceVector[1] + sortedCNORMF[i][4]

            # print(totalContactForceVector)

        for i in range(len(sortedCSHEARF)):

            totalContactForceVector[0] = totalContactForceVector[0] + sortedCSHEARF[i][3]

            totalContactForceVector[1] = totalContactForceVector[1] + sortedCSHEARF[i][4]

            # print(totalContactForceVector)

        for i in range(len(totalContactForceVector)):

            totalContactForceVector[2] = np.arctan(totalContactForceVector[0]/totalContactForceVector[1])

            totalContactForceVector[3] = np.degrees(totalContactForceVector[2])

            totalContactForceVector[4] = np.arctan(totalContactForceVector[1]/totalContactForceVector[0])

            totalContactForceVector[5] = np.degrees(totalContactForceVector[4])

        if writeCSV:

            titleRow = ['CFORCE1','CFORCE2','ANGLEvert(rad)','ANGLEvert(deg)','ANGLEhoriz(rad)','ANGLEhoriz(deg)','contactRadius']

            resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'CFORCE' + '.csv')

            print('Writing CSV File: %s\n\n\n' %(resCSVname))

            tempFile = open(resCSVname, 'wb')

            with open(resCSVname, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                csvWriter.writerow([totalContactForceVector[0],totalContactForceVector[1],totalContactForceVector[2],totalContactForceVector[3],totalContactForceVector[4],totalContactForceVector[5],contactRadius])

        return(totalContactForceVector)

    #-----------------------------------------------------------------------

    def GeneralResults(self,*args,**kwargs):

        sortedResults = kwargs.get('sortedResults', False)
        sortDirection = kwargs.get('sortDirection', 1)
        stepName = kwargs.get('stepName', 'Initial')
        frameNumber = kwargs.get('frameNumber', -1)
        instanceName = kwargs.get('instanceName', None)
        setName = kwargs.get('setName', None)
        resultName = kwargs.get('resultName', 'COORD')
        specialLocation = kwargs.get('specialLocation', None)
        includePE =  kwargs.get('includePE', False)
        writeCSV = kwargs.get('writeCSV', True)

        if sortDirection > 0: reverse = False
        elif sortDirection < 0: reverse = True

        try: self.odb.steps[stepName].frames[frameNumber].frameId
        except: return(1)

        frameId = self.odb.steps[stepName].frames[frameNumber].frameId

        unsortedResultSet = []

        #-----------------------------------------------------------------------

        # print(self.odb.steps[stepName].frames[frameNumber].fieldOutputs.keys())

        try: self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].nodeLabel
        except: return(1)

        if self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].nodeLabel:

            print('Running Sorting Routine:')
            print('  Part Instance: %s , nodeSet: %s' %(instanceName, setName))
            print('  Step Name: %s , Frame Index: %s, Frame Id: %s' %(stepName,frameNumber,frameId))
            print('  Data Key: %s , Sort Direciton: %s\n' %(resultName, sortDirection))

            nodeSet = self.odb.rootAssembly.instances[instanceName].nodeSets[setName]

            coordSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['COORD'].getSubset(region=nodeSet)

            resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=nodeSet)

            if includePE:

                if 'PEEQ' in self.odb.steps[stepName].frames[frameNumber].fieldOutputs.keys():

                    presentPEEQ = True

                    resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)

                    resultPEEQ = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PEEQ'].getSubset(region=elementSet)

                    titleRow = ['nodeLabel'] + list(coordSet.componentLabels) + list(resultSet.componentLabels) + [resultPE.name] + [resultPEEQ.name]

                else:

                    presentPEEQ = False

                    resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)

                    titleRow = ['nodeLabel'] + list(coordSet.componentLabels) + list(resultSet.componentLabels) + [resultPE.name]

            else:

                titleRow = ['nodeLabel'] + list(coordSet.componentLabels) + list(resultSet.componentLabels)

            #for i in range(len(nodeSet.nodes)): print('%s, %s, %s' %(nodeSet.nodes[i].label,coordSet.values[i].nodeLabel,resultSet.values[i].nodeLabel))

            unsortedResults = []

            for i in range(len(nodeSet.nodes)):

                if includePE:

                    if presentPEEQ:

                        unsortedResults.append([nodeSet.nodes[i].label] + coordSet.values[i].data.tolist() + resultSet.values[i].data.tolist() + resultPE.values[i].data.tolist() + [resultPEEQ.values[i].data])

                    else:

                        unsortedResults.append([nodeSet.nodes[i].label] + coordSet.values[i].data.tolist() + resultSet.values[i].data.tolist() + resultPE.values[i].data.tolist())

                else:

                    unsortedResults.append([nodeSet.nodes[i].label] + coordSet.values[i].data.tolist() + resultSet.values[i].data.tolist())

        elif self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].elementLabel:

            print('Running Sorting Routine:')
            print('  Part Instance: %s , elementSet: %s' %(instanceName, setName))
            print('  Step Name: %s , Frame Index: %s, Frame Id: %s' %(stepName,frameNumber,frameId))
            print('  Data Key: %s , Sort Direciton: %s\n' %(resultName, sortDirection))

            nodeSet = self.odb.rootAssembly.instances[instanceName].nodeSets[setName]

            elementSet = self.odb.rootAssembly.instances[instanceName].elementSets[setName]

            coordSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['COORD'].getSubset(region=nodeSet)

            if specialLocation is not None: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=elementSet,position=specialLocation)
            else: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=elementSet)

            if includePE:

                if 'PEEQ' in self.odb.steps[stepName].frames[frameNumber].fieldOutputs.keys():

                    presentPEEQ = True

                    if specialLocation is not None:

                        resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet,position=specialLocation)
                        resultPEEQ = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PEEQ'].getSubset(region=elementSet,position=specialLocation)

                    else:

                        resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)
                        resultPEEQ = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PEEQ'].getSubset(region=elementSet)

                    if resultSet.componentLabels: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + list(resultSet.componentLabels) + list(resultPE.componentLabels) + [resultPEEQ.name]
                    else: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + [resultSet.name] + list(resultPE.componentLabels) + [resultPEEQ.name]

                else:

                    presentPEEQ = False

                    if specialLocation is not None: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet,position=specialLocation)
                    else: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)

                    if resultSet.componentLabels: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + list(resultSet.componentLabels) + list(resultPE.componentLabels)
                    else: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + [resultSet.name] + list(resultPE.componentLabels)

            else:

                if resultSet.componentLabels: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + list(resultSet.componentLabels)
                else: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + [resultSet.name]

            #print(resultSet.values[0])

            coordSetNodes = []

            for i in range(len(coordSet.values)):

                coordSetNodes.append(coordSet.values[i].nodeLabel)

            #print(coordSetNodes)

            unsortedResults = []

            for i in range(len(elementSet.elements)):

                tempNodeCount = 0

                tempCoordSum = np.zeros(len(coordSet.values[0].data))

                for j in range(len(elementSet.elements[i].connectivity)):

                    if elementSet.elements[i].connectivity[j] in coordSetNodes:

                        tempNodeCount += 1

                        for n in range(len(tempCoordSum)):

                            tempCoordSum[n] += coordSet.values[coordSetNodes.index(elementSet.elements[i].connectivity[j])].data[n]

                for n in range(len(tempCoordSum)):

                    tempCoordSum[n] = tempCoordSum[n] / float(tempNodeCount)

                for m in range(len(resultSet.values)):

                    if resultSet.values[m].elementLabel == elementSet.elements[i].label:

                        if includePE:

                            if presentPEEQ:

                                try:

                                    unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + resultSet.values[m].data.tolist() + resultPE.values[m].data.tolist() + [resultPEEQ.values[m].data] )

                                except AttributeError:

                                    unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + [resultSet.values[m].data] + resultPE.values[m].data.tolist() + [resultPEEQ.values[m].data] )

                            else:

                                try: unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + resultSet.values[m].data.tolist() + resultPE.values[m].data.tolist() )
                                except AttributeError: unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + [resultSet.values[m].data] + resultPE.values[m].data.tolist() )

                        else:

                            try: unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + resultSet.values[m].data.tolist())
                            except AttributeError: unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + [resultSet.values[m].data])

        if sortedResults: finalResults = sorted(unsortedResults, key=lambda unsortedResults: unsortedResults[abs(sortDirection)], reverse=reverse)
        else: finalResults = unsortedResults

        #for i in range(len(finalResults)): print(finalResults[i])

        if writeCSV:

            if resultName.startswith('CNORMF'): resultName = 'CNORMF'
            if resultName.startswith('CSHEARF'): resultName = 'CSHEARF'

            resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + resultName + '_' + stepName + '_' + instanceName + '-' + setName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(resCSVname))

            tempFile = open(resCSVname, 'wb')

            with open(resCSVname, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                for i in range(len(finalResults)):

                    csvWriter.writerow(finalResults[i])

        return(finalResults)

    #-----------------------------------------------------------------------

    def NoCoordResults(self,*args,**kwargs): #Currently unused

        stepName = kwargs.get('stepName', 'Initial')
        frameNumber = kwargs.get('frameNumber', -1)
        instanceName = kwargs.get('instanceName', None)
        setName = kwargs.get('setName', None)
        resultName = kwargs.get('resultName', 'COORD')
        specialLocation = kwargs.get('specialLocation', None)
        includePE =  kwargs.get('includePE', False)
        writeCSV = kwargs.get('writeCSV', True)

        try: self.odb.steps[stepName].frames[frameNumber].frameId
        except: return(1)

        frameId = self.odb.steps[stepName].frames[frameNumber].frameId

        unsortedResultSet = []

        #-----------------------------------------------------------------------

        # print(self.odb.steps[stepName].frames[frameNumber].fieldOutputs.keys())

        try: self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].nodeLabel
        except: return(1)

        if self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].nodeLabel:

            print('Running Sorting Routine:')
            print('  Part Instance: %s , nodeSet: %s' %(instanceName, setName))
            print('  Step Name: %s , Frame Index: %s, Frame Id: %s' %(stepName,frameNumber,frameId))
            print('  Data Key: %s\n' %(resultName))

            nodeSet = self.odb.rootAssembly.instances[instanceName].nodeSets[setName]

            resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=nodeSet)

            if includePE:

                resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)

                titleRow = ['nodeLabel'] + list(resultSet.componentLabels) + [resultPE.name]

            else:

                titleRow = ['nodeLabel'] + list(resultSet.componentLabels)

            #for i in range(len(nodeSet.nodes)): print('%s, %s' %(nodeSet.nodes[i].label,resultSet.values[i].nodeLabel))

            unsortedResults = []

            for i in range(len(nodeSet.nodes)):

                if includePE:

                    unsortedResults.append([nodeSet.nodes[i].label] + resultSet.values[i].data.tolist() + resultPE.values[i].data.tolist())

                else:

                    unsortedResults.append([nodeSet.nodes[i].label] + resultSet.values[i].data.tolist())

        elif self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].elementLabel:

            print('Running Sorting Routine:')
            print('  Part Instance: %s , elementSet: %s' %(instanceName, setName))
            print('  Step Name: %s , Frame Index: %s, Frame Id: %s' %(stepName,frameNumber,frameId))
            print('  Data Key: %s\n' %(resultName))

            nodeSet = self.odb.rootAssembly.instances[instanceName].nodeSets[setName]

            elementSet = self.odb.rootAssembly.instances[instanceName].elementSets[setName]

            if specialLocation is not None: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=elementSet,position=specialLocation)
            else: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=elementSet)

            if includePE:

                if specialLocation is not None: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet,position=specialLocation)
                else: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)

                if resultSet.componentLabels: titleRow = ['elementLabel'] + list(resultSet.componentLabels) + list(resultPE.componentLabels)
                else: titleRow = ['elementLabel'] + [resultSet.name] + list(resultPE.componentLabels)

            else:

                if resultSet.componentLabels: titleRow = ['elementLabel'] + list(resultSet.componentLabels)
                else: titleRow = ['elementLabel'] + [resultSet.name]

            unsortedResults = []

            for m in range(len(resultSet.values)):

                if includePE:

                    try: unsortedResults.append([resultSet.values[m].elementLabel] + resultSet.values[m].data.tolist() + resultPE.values[m].data.tolist() )
                    except AttributeError: unsortedResults.append([resultSet.values[m].elementLabel] + [resultSet.values[m].data] + resultPE.values[m].data.tolist() )

                else:

                    try: unsortedResults.append([resultSet.values[m].elementLabel] + resultSet.values[m].data.tolist())
                    except AttributeError: unsortedResults.append([resultSet.values[m].elementLabel] + [resultSet.values[m].data])

        finalResults = unsortedResults

        #for i in range(len(finalResults)): print(finalResults[i])

        if writeCSV:

            if resultName.startswith('CNORMF'): resultName = 'CNORMF'
            if resultName.startswith('CSHEARF'): resultName = 'CSHEARF'

            resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + resultName + '_' + stepName + '_' + instanceName + '-' + setName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(resCSVname))

            tempFile = open(resCSVname, 'wb')

            with open(resCSVname, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                for i in range(len(finalResults)):

                    csvWriter.writerow(finalResults[i])

        return(finalResults)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

class Indentation_Output(General_Output):

    #-----------------------------------------------------------------------

    def __init__ (self,*args,**kwargs):

        odbPath = args[0]

        readOnly = kwargs.get('readOnly', True)

        from odbAccess import openOdb, OdbError

        odbName = odbPath.split('/')[-1].split('\\')[-1]
        print("Opening ODB: %s \n\n\n" %(odbName))
        os.chdir(odbPath.rstrip(odbName))

        try:

            session.odbs[odbPath].close()
            self.odb = session.openOdb(odbName, readOnly=readOnly)

            try:

                o1 = session.odbs[odbPath]
                session.viewports['Viewport: 1'].setValues(displayedObject=o1)
                session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
                session.viewports['Viewport: 1'].view.fitView()

            except: pass

        except KeyError:

            try:

                self.odb = session.openOdb(odbName, readOnly=readOnly)

            except OdbError:

                raise NameError('ODB file does not exist - (%s)' %(odbPath))
                print('Error: ODB file does not exist - (%s)' %(odbPath))

            try:

                o1 = session.odbs[odbPath]
                session.viewports['Viewport: 1'].setValues(displayedObject=o1)
                session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
                session.viewports['Viewport: 1'].view.fitView()

            except: pass

        except NameError:

            try:

                self.odb = openOdb(odbName, readOnly=readOnly)

            except OdbError:

                print('Error: Could not open ODB file - (%s)' %(odbPath))

                print('  \nODB possibly from older version: attempting to upgrade to current release\n\n')

                try:

                    subprocess.call("abaqus -upgrade -job %s -odb %s" %(str(odbName)[:-4]+'_upg',str(odbName)[:-4]), shell=True)

                    odbName = str(odbName)[:-4]+'_upg.odb'

                    self.odb = openOdb(odbName, readOnly=readOnly)

                except OdbError:

                    print('Error: Could not open ODB file - (%s)' %(odbPath))
                    exit()

        # print(self.odb)

        return(None)

    #-----------------------------------------------------------------------

    def WorkForceDist(self,*args,**kwargs):

        instanceNameRF = kwargs.get('instanceNameRF', None)
        nodeSetNameRF = kwargs.get('nodeSetNameRF', None)

        instanceNameU = kwargs.get('instanceNameU', None)
        nodeSetNameU = kwargs.get('nodeSetNameU', None)

        fileNameSuffix = kwargs.get('fileNameSuffix', '')

        print('Running Work-Force-Distance Routine:\n')

        if instanceNameRF and nodeSetNameRF: nodeSetRF = self.odb.rootAssembly.instances[instanceNameRF].nodeSets[nodeSetNameRF]
        elif nodeSetNameRF: nodeSetRF = self.odb.rootAssembly.nodeSets[nodeSetNameRF]
        else: print('Error: No Reaction Force Node Set Selected.')

        if instanceNameU and nodeSetNameU: nodeSetU = self.odb.rootAssembly.instances[instanceNameU].nodeSets[nodeSetNameU]
        elif nodeSetNameU: nodeSetU = self.odb.rootAssembly.nodeSets[nodeSetNameU]
        else: print('Error: No Distance Node Set Selected.')

        headerRow = ['Step', 'Frame', 'Step Time', 'RF1', 'RF2', 'RF-Angle', 'U1', 'U2', 'frameWork1', 'frameWork2', 'totalWork1', 'totalWork2','RF2Calc(mN)=ALLIE/Disp(mN)', 'ALLIE', 'ALLWK','','negU2(um)','RF2(mN)','K(mN/um)','Ewk(nJ)','','negU2(nm)','RF2(uN)','K(uN/nm)','Ewk(pJ)']
        resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'RF_Work' + fileNameSuffix + '.csv')

        tempFile = open(resCSVname, 'wb')

        with open(resCSVname, 'wb') as tempFile:

            csvWriter = csv.writer(tempFile)

            csvWriter.writerow(headerRow)

            totalWork1 = 0.0
            totalWork2 = 0.0

            prevRF1 = 0.0
            prevRF2 = 0.0

            prevU1 = 0.0
            prevU2 = 0.0

            prevALLIE = 0.0
            prevRF2calc = 0.0
            RF2calc = 0.0

            self.maxRF2 = 0.0

            for step in self.odb.steps.values():

                print('Processing Step: %s\n' %(step.name))

                i = 0

                try:
                    step.frames[-1]
                except:
                    return(1)

                for frame in step.frames:

                    totalRF1 = 0.0
                    totalRF2 = 0.0

                    rfSet = frame.fieldOutputs['RF'].getSubset(region=nodeSetRF)

                    for rfValue in rfSet.values:

                        totalRF1 = totalRF1 + rfValue.data[0]
                        totalRF2 = totalRF2 + rfValue.data[1]

                    if fileNameSuffix == '_Ind': totalRF2 = -totalRF2 #Changes sign on the reaction force on the "Ind"enter end (Other method is on the "Base" of the test article)

                    try: Angle12 = np.degrees(np.arctan(totalRF2/totalRF1))

                    except:

                        if totalRF2 > 0.0: Angle12 = 90.0
                        elif totalRF2 < 0.0: Angle12 = -90.0
                        else: Angle12 = 'NA'

                    uSet = frame.fieldOutputs['U'].getSubset(region=nodeSetU)

                    for uValue in uSet.values:

                        U1 = uValue.data[0]
                        U2 = uValue.data[1]

                    try:
                        historyIntEnergy = self.odb.steps[step.name].historyRegions['Assembly ASSEMBLY'].historyOutputs['ALLIE'].data[i][1]
                    except:
                        return(1)

                    try:
                        historyWork = self.odb.steps[step.name].historyRegions['Assembly ASSEMBLY'].historyOutputs['ALLWK'].data[i][1]
                    except:
                        return(1)

                    #-----------------------------------------------------------------------
                    #Trapezoid Method for discrete integration.
                    #-----------------------------------------------------------------------
                    #Calculating work from force and distance
                    frameWork1 = - ( prevRF1*(U1-prevU1) + 0.5*(totalRF1-prevRF1)*(U1-prevU1) ) #negatvie sign assumes that displacement and reaction force are in opposite directions
                    frameWork2 = - ( prevRF2*(U2-prevU2) + 0.5*(totalRF2-prevRF2)*(U2-prevU2) ) #negatvie sign assumes that displacement and reaction force are in opposite directions

                    totalWork1 = totalWork1 + frameWork1
                    totalWork2 = totalWork2 + frameWork2
                    #-----------------------------------------------------------------------
                    #Calculating force from energy and distance (best for analyses with lots of damping)
                    ALLIE = historyIntEnergy

                    try:
                        RF2calc = -((2.0*(ALLIE-prevALLIE)/(U2-prevU2)) + prevRF2calc)
                    except:
                        RF2calc = prevRF2calc
                    #-----------------------------------------------------------------------
                    #Calculating stiffness (spring constant) from discrete slope (i.e.derrivative) of the Force vs. Disp curve
                    try: kStiff = -(totalRF2-prevRF2)/(U2-prevU2) #negatvie sign assumes that displacement and reaction force are in opposite directions
                    except FloatingPointError: kStiff = 0.0
                    #-----------------------------------------------------------------------

                    #-----------------------------------------------------------------------
                    prevRF1 = totalRF1
                    prevRF2 = totalRF2

                    prevU1 = U1
                    prevU2 = U2

                    prevALLIE = ALLIE
                    prevRF2calc = RF2calc
                    #-----------------------------------------------------------------------

                    #-----------------------------------------------------------------------
                    #Keeping Max totalRF2
                    #-----------------------------------------------------------------------
                    if totalRF2 > self.maxRF2: self.maxRF2 = totalRF2
                    #-----------------------------------------------------------------------

                    csvWriter.writerow([step.name, frame.frameId, frame.frameValue, totalRF1, totalRF2, Angle12, U1, U2, frameWork1, frameWork2, totalWork1, totalWork2, RF2calc/1e3, historyIntEnergy, historyWork, '', -U2, totalRF2/1e3, kStiff/1e3, historyWork/1e3, '', -U2*1e3, totalRF2, kStiff/1e3, historyWork])

                    i += 1

        print('Writing CSV File: %s\n\n\n' %(resCSVname))

        return(0)

    #-----------------------------------------------------------------------

    def VolumeDispCyl(self,*args,**kwargs):

        '''Indent Volume Displacements: This function doesn't work that great, because it depends on where it "stops" counting at the edge of the plastic zone'''

        sortedNodeSet = self.GeneralResults(sortedResults=True,sortDirection=1,stepName='Unloading',instanceName='TEST_ARTICLE-1',setName='RESULTS_SURF_SET', resultName='COORD', writeCSV=False)

        xLimit = kwargs.get('xLimit', None)
        writeCSV = kwargs.get('writeCSV', True)

        volNegSum = 0.0
        volPosSum = 0.0
        volTotSum = 0.0

        for i in range(len(sortedNodeSet)-1):

            # print(sortedNodeSet[i][2])

            # #The top equation should be "half" the value

            # volInc = ((sortedNodeSet[i][2]+sortedNodeSet[i+1][2])/2.0) * (sortedNodeSet[i+1][1]-sortedNodeSet[i][1])   *    np.pi * ((sortedNodeSet[i][1]+sortedNodeSet[i+1][1])/2.0)

            volInc = 0.5 * (sortedNodeSet[i][2]+sortedNodeSet[i+1][2]) * (sortedNodeSet[i+1][1]-sortedNodeSet[i][1])   *    np.pi * (sortedNodeSet[i][1]+sortedNodeSet[i+1][1])

            # print(volInc)

            volTotSum += volInc

            if volInc < 0.0:

                volNegSum += volInc

            elif volInc > 0.0:

                volPosSum += volInc

            else: print('Warning: Found a zero volume in the trapazoid rule summation')

            if xLimit and sortedNodeSet[i+1][1] > xLimit: break
            if not xLimit and abs(sortedNodeSet[i][2]) < 0.005 and abs(sortedNodeSet[i+1][2]) < 0.005: break

        if writeCSV:

            titleRow = ['negVol','posVol','totVol']

            resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'iVol' + '.csv')

            print('Writing CSV File: %s\n\n\n' %(resCSVname))

            tempFile = open(resCSVname, 'wb')

            with open(resCSVname, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow + ['Calculations Stopped at x=%s'%(sortedNodeSet[i][1])])

                csvWriter.writerow([volNegSum,volPosSum,volTotSum])

                # csvWriter.writerow(['Calculations Stopped at x=%s'%(sortedNodeSet[i][1])])

        return([volNegSum,volPosSum,volTotSum])

    #-----------------------------------------------------------------------

    def NormalizerVariables(self,*args,**kwargs):

        '''This function is currently in work. It is intended to get numerous "normalizer" values and put them in a csv'''

        writeCSV = kwargs.get('writeCSV', True)

        normalVars = {}

        #-----------------------------------------------------------------------

        normalVars['maxRF2_Total'] = self.maxRF2

        #-----------------------------------------------------------------------
        sortedElementSet = self.GeneralResults(sortedResults=True,sortDirection=-1,stepName='Loading',instanceName='TEST_ARTICLE-1',setName='RESULTS_SURF_SET', resultName='PE', writeCSV=False)

        # for value in sortedElementSet: print(value)

        for value in sortedElementSet:

            if abs(max(value[3:6])) > 1e-4:
            # if value[3] > 1e-4:

                normalVars['plasticEdge_IndentX'] = value[1]

                break

        if ('plasticEdge_IndentX' not in dict(normalVars)): normalVars['plasticEdge_IndentX'] = None

        print('Indent X-dir; Plastic Edge Location: %s\n' %(normalVars['plasticEdge_IndentX']))
        #-----------------------------------------------------------------------
        sortedElementSet = self.GeneralResults(sortedResults=True,sortDirection=2,stepName='Loading',instanceName='TEST_ARTICLE-1',setName='RESULTS_CL_SET', resultName='PE', writeCSV=False)

        # for value in sortedElementSet: print(value)

        for value in sortedElementSet:

            if abs(max(value[3:6])) > 1e-4:
            # if value[3] > 1e-4:

                normalVars['plasticEdge_IndentY'] = value[2]

                break

        if ('plasticEdge_IndentY' not in dict(normalVars)): normalVars['plasticEdge_IndentY'] = None

        print('Indent Y-dir; Plastic Edge Location: %s\n' %(normalVars['plasticEdge_IndentY']))
        #-----------------------------------------------------------------------
        sortedElementSet = self.GeneralResults(sortedResults=True,sortDirection=-1,stepName='Unloading',instanceName='TEST_ARTICLE-1',setName='RESULTS_SURF_SET', resultName='PE', writeCSV=False)

        # for value in sortedElementSet: print(value)

        for value in sortedElementSet:

            if abs(max(value[3:6])) > 1e-4:
            # if value[3] > 1e-4::

                normalVars['plasticEdge_RemoveX'] = value[1]

                break

        if ('plasticEdge_RemoveX' not in dict(normalVars)): normalVars['plasticEdge_RemoveX'] = None

        print('Remove X-dir; Plastic Edge Location: %s\n' %(normalVars['plasticEdge_RemoveX']))
        #-----------------------------------------------------------------------
        sortedElementSet = self.GeneralResults(sortedResults=True,sortDirection=2,stepName='Unloading',instanceName='TEST_ARTICLE-1',setName='RESULTS_CL_SET', resultName='PE', writeCSV=False)

        # for value in sortedElementSet: print(value)

        for value in sortedElementSet:

            if abs(max(value[3:6])) > 1e-4:
            # if value[3] > 1e-4:

                normalVars['plasticEdge_RemoveY'] = value[2]

                break

        if ('plasticEdge_RemoveY' not in dict(normalVars)): normalVars['plasticEdge_RemoveY'] = None

        print('Remove Y-dir; Plastic Edge Location: %s\n' %(normalVars['plasticEdge_RemoveY']))
        #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        #Indent Depth @ loading and unloading
        #-----------------------------------------------------------------------
        sortedElementSet = self.GeneralResults(sortedResults=True,sortDirection=2,stepName='Loading',instanceName='TEST_ARTICLE-1',setName='RESULTS_CL_SET', resultName='COORD', writeCSV=False)

        # for value in sortedElementSet: print(value)

        normalVars['indentDepth_IndentY'] = sortedElementSet[-1][-1]
        #-----------------------------------------------------------------------
        sortedElementSet = self.GeneralResults(sortedResults=True,sortDirection=2,stepName='Unloading',instanceName='TEST_ARTICLE-1',setName='RESULTS_CL_SET', resultName='COORD', writeCSV=False)

        # for value in sortedElementSet: print(value)

        normalVars['indentDepth_RemoveY'] = sortedElementSet[-1][-1]
        #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        for key in self.odb.steps['Loading'].frames[-1].fieldOutputs.keys():

            if key.startswith('CNORMF'): keyCNORMF = key

        sortedCNORMF = self.GeneralResults(sortedResults=True,sortDirection=-1,stepName='Loading',instanceName='TEST_ARTICLE-1',setName='RESULTS_SURF_SET', resultName=keyCNORMF, writeCSV=False)

        for value in sortedCNORMF:

            if value[3] > 1e-4 or value[4] > 1e-4:

                tempNode = value[0]

                normalVars['contactEdge_IndentX'] = value[1]

                break

        print('Indent X-dir; Contact Edge Location: %s\n' %(normalVars['contactEdge_IndentX']))
        #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        nodeSet = self.odb.rootAssembly.instances['TEST_ARTICLE-1'].nodeSets['RESULTS_SURF_SET']

        coordSet = self.odb.steps['Unloading'].frames[-1].fieldOutputs['COORD'].getSubset(region=nodeSet)

        for value in coordSet.values:

            if value.nodeLabel == tempNode:

                normalVars['contactEdge_RemoveX'] = value.data.item(0)

                break

        print('Remove X-dir; Contact Edge Location: %s\n' %(normalVars['contactEdge_RemoveX']))
        #-----------------------------------------------------------------------

        # #-----------------------------------------------------------------------
        # sortedCoordSet = self.GeneralResults(sortedResults=True,sortDirection=2,stepName='Unloading',instanceName='TEST_ARTICLE-1',setName='RESULTS_SURF_SET', resultName='COORD', writeCSV=False)

        # for value in sortedCoordSet:

        #     if value[0] == tempNode:

        #         normalVars['contactEdge_RemoveX'] = value[1]

        #         break

        # print('Remove X-dir; Contact Edge Location: %s\n' %(normalVars['contactEdge_RemoveX']))
        # #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        try: normalVars['plasticZoneHeight_IndentY'] = normalVars['plasticEdge_IndentY'] - normalVars['indentDepth_IndentY']
        except: normalVars['plasticZoneHeight_IndentY'] = None
        try: normalVars['plasticZoneHeight_RemoveY'] = normalVars['plasticEdge_RemoveY'] - normalVars['indentDepth_RemoveY']
        except: normalVars['plasticZoneHeight_RemoveY'] = None
        #-----------------------------------------------------------------------
        try: normalVars['calculated_Hardness'] = normalVars['maxRF2_Total'] / (np.pi * (normalVars['contactEdge_RemoveX'])**2.0)
        except: normalVars['calculated_Hardness'] = None
        #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        for key in normalVars.keys(): print('Key: %s  Value: %s\n' %(key,normalVars[key]))

        if writeCSV:

            resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'normVars' + '.csv')

            print('Writing CSV File: %s\n\n\n' %(resCSVname))

            tempFile = open(resCSVname, 'wb')

            with open(resCSVname, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                for key in normalVars.keys():

                    csvWriter.writerow([key,normalVars[key]])

        return(normalVars)

    #-----------------------------------------------------------------------

    def StressInvariantResults(self,*args,**kwargs):

        sortedResults = kwargs.get('sortedResults', False)
        sortDirection = kwargs.get('sortDirection', 1)
        stepName = kwargs.get('stepName', 'Initial')
        frameNumber = kwargs.get('frameNumber', -1)
        instanceName = kwargs.get('instanceName', None)
        setName = kwargs.get('setName', None)
        resultName = kwargs.get('resultName', 'S')
        specialLocation = kwargs.get('specialLocation', None)
        includePE =  kwargs.get('includePE', False)
        writeCSV = kwargs.get('writeCSV', True)

        if sortDirection > 0: reverse = False
        elif sortDirection < 0: reverse = True

        try: self.odb.steps[stepName].frames[frameNumber].frameId
        except: return(1)

        frameId = self.odb.steps[stepName].frames[frameNumber].frameId

        unsortedResultSet = []

        #-----------------------------------------------------------------------

        # print(self.odb.steps[stepName].frames[frameNumber].fieldOutputs.keys())

        try: self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].nodeLabel
        except: return(1)

        if self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].elementLabel:

            print('Running Sorting Routine:')
            print('  Part Instance: %s , elementSet: %s' %(instanceName, setName))
            print('  Step Name: %s , Frame Index: %s, Frame Id: %s' %(stepName,frameNumber,frameId))
            print('  Data Key: %s , Sort Direciton: %s\n' %(resultName, sortDirection))

            nodeSet = self.odb.rootAssembly.instances[instanceName].nodeSets[setName]

            elementSet = self.odb.rootAssembly.instances[instanceName].elementSets[setName]

            coordSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['COORD'].getSubset(region=nodeSet)

            if specialLocation is not None: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=elementSet,position=specialLocation)
            else: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=elementSet)

            if includePE:

                if specialLocation is not None: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet,position=specialLocation)
                else: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)

                titleRow = ['elementLabel'] + list(coordSet.componentLabels) + ['maxPrincipal', 'midPrincipal', 'minPrincipal', 'press', 'mises'] + list(resultPE.componentLabels)

            else:

                titleRow = ['elementLabel'] + list(coordSet.componentLabels) + ['maxPrincipal', 'midPrincipal', 'minPrincipal', 'press', 'mises']

            coordSetNodes = []

            for i in range(len(coordSet.values)):

                coordSetNodes.append(coordSet.values[i].nodeLabel)

            #print(coordSetNodes)

            unsortedResults = []

            for i in range(len(elementSet.elements)):

                tempNodeCount = 0

                tempCoordSum = np.zeros(len(coordSet.values[0].data))

                for j in range(len(elementSet.elements[i].connectivity)):

                    if elementSet.elements[i].connectivity[j] in coordSetNodes:

                        tempNodeCount += 1

                        for n in range(len(tempCoordSum)):

                            tempCoordSum[n] += coordSet.values[coordSetNodes.index(elementSet.elements[i].connectivity[j])].data[n]

                for n in range(len(tempCoordSum)):

                    tempCoordSum[n] = tempCoordSum[n] / float(tempNodeCount)

                for m in range(len(resultSet.values)):

                    tempInvariantData = []

                    if resultSet.values[m].elementLabel == elementSet.elements[i].label:

                        tempInvariantData.append(resultSet.values[m].maxPrincipal)
                        tempInvariantData.append(resultSet.values[m].midPrincipal)
                        tempInvariantData.append(resultSet.values[m].minPrincipal)
                        tempInvariantData.append(resultSet.values[m].press)
                        tempInvariantData.append(resultSet.values[m].mises)

                        if includePE:

                            unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + tempInvariantData + resultPE.values[i].data.tolist() )

                        else:

                            unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + tempInvariantData)

        if sortedResults: finalResults = sorted(unsortedResults, key=lambda unsortedResults: unsortedResults[abs(sortDirection)], reverse=reverse)
        else: finalResults = unsortedResults

        #for i in range(len(finalResults)): print(finalResults[i])

        if writeCSV:

            if resultName.startswith('CNORMF'): resultName = 'CNORMF'
            if resultName.startswith('CSHEARF'): resultName = 'CSHEARF'

            resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + resultName + '_Invariants_' + stepName + '_' + instanceName + '-' + setName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(resCSVname))

            tempFile = open(resCSVname, 'wb')

            with open(resCSVname, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                for i in range(len(finalResults)):

                    csvWriter.writerow(finalResults[i])

        return(finalResults)

    #-----------------------------------------------------------------------

    def UnsortedStressInvariants(self,*args,**kwargs):

        stepName = kwargs.get('stepName', 'Initial')
        frameNumber = kwargs.get('frameNumber', -1)
        instanceName = kwargs.get('instanceName', None)
        setName = kwargs.get('setName', None)
        resultName = kwargs.get('resultName', 'S')
        specialLocation = kwargs.get('specialLocation', None)
        includePE =  kwargs.get('includePE', False)
        writeCSV = kwargs.get('writeCSV', True)

        frameId = self.odb.steps[stepName].frames[frameNumber].frameId

        #-----------------------------------------------------------------------

        print('Running Unsorted Results Routine:')
        print('  Part Instance: %s , elementSet: %s' %(instanceName, setName))
        print('  Step Name: %s , Frame Index: %s, Frame Id: %s\n' %(stepName,frameNumber,frameId))

        elementSet = self.odb.rootAssembly.instances[instanceName].elementSets[setName]

        resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=elementSet)

        if specialLocation is not None: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=elementSet,position=specialLocation)
        else: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=elementSet)

        if includePE:

            if specialLocation is not None: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet,position=specialLocation)
            else: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)

            titleRow = ['elementLabel'] + ['maxPrincipal', 'midPrincipal', 'minPrincipal', 'press', 'mises'] + list(resultPE.componentLabels)

        else:

            titleRow = ['elementLabel'] + ['maxPrincipal', 'midPrincipal', 'minPrincipal', 'press', 'mises']

        unsortedResults = []

        for m in range(len(resultSet.values)):

            tempInvariantData = []

            tempInvariantData.append(resultSet.values[m].maxPrincipal)
            tempInvariantData.append(resultSet.values[m].midPrincipal)
            tempInvariantData.append(resultSet.values[m].minPrincipal)
            tempInvariantData.append(resultSet.values[m].press)
            tempInvariantData.append(resultSet.values[m].mises)

            if includePE:

                unsortedResults.append([resultSet.values[m].elementLabel] + tempInvariantData + resultPE.values[m].data.tolist() )

            else:

                unsortedResults.append([resultSet.values[m].elementLabel] + tempInvariantData)

        finalResults = unsortedResults

        #for i in range(len(finalResults)): print(finalResults[i])

        if writeCSV:

            resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'Invariants' + '_' + stepName + '_' + instanceName + '-' + setName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(resCSVname))

            tempFile = open(resCSVname, 'wb')

            with open(resCSVname, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                for i in range(len(finalResults)):

                    csvWriter.writerow(finalResults[i])

        return(finalResults)

    #-----------------------------------------------------------------------

    def UnsortedResultsZone(self,*args,**kwargs): # Uses the updated numpy.array method (instead of lists)

        stepName = kwargs.get('stepName', 'Initial')
        frameNumber = kwargs.get('frameNumber', -1)
        instanceName = kwargs.get('instanceName', None)
        setName = kwargs.get('setName', None)
        resultName = kwargs.get('resultName', 'PE')
        limitResult = kwargs.get('limitResult', None)
        limitTypeResult = kwargs.get('limitTypeResult', 'lower')
        specialLocation = kwargs.get('specialLocation', None)
        limitPE = kwargs.get('limitPE', 1e-05)
        limitTypePE = kwargs.get('limitType', 'lower')
        writeCSV = kwargs.get('writeCSV', True)

        print('Running Unsorted Results Routine:')
        print('  Part Instance: %s , elementSet: %s' %(instanceName, setName))
        print('  Step Name: %s , Frame Index: %s, Frame Id: %s' %(stepName,frameNumber,self.odb.steps[stepName].frames[frameNumber].frameId))
        print('  Data Key: %s\n' %(resultName))

        #-----------------------------------------------------------------------

        resultCategory = resultName.rstrip('1').rstrip('2').rstrip('3')

        nodeSet = self.odb.rootAssembly.instances[instanceName].nodeSets[setName]

        elementSet = self.odb.rootAssembly.instances[instanceName].elementSets[setName]

        coordSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['COORD'].getSubset(region=nodeSet)

        if len(self.odb.steps[stepName].frames[frameNumber].fieldOutputs['COORD'].getSubset(region=elementSet).values) > 0:

            coordElementSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['COORD'].getSubset(region=elementSet)

        else:

            coordSetNodes = np.array([value.nodeLabel for value in coordSet.values])

        if specialLocation is not None:

            resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultCategory].getSubset(region=elementSet,position=specialLocation)

            resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet,position=specialLocation)

        else:

            resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultCategory].getSubset(region=elementSet)

            resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)

        #-----------------------------------------------------------------------
        # This is the filtered elemental results section, where selections are made before sorting occurs
        # It gets results and uses np.nan (to keep) and np.inf (to delete) rows that are outside the filter criteria
        #-----------------------------------------------------------------------

        # filteredResults = np.zeros(( len(elementSet.elements), len(np.zeros(len(coordSet.componentLabels)).tolist()) + 1 + len(resultSet.values[0].data.tolist()) + len(resultPE.values[0].data.tolist()) + 1 ))
        filteredResults = np.zeros(( len(elementSet.elements), len(coordSet.componentLabels) + 1 + len(resultSet.values[0].data.tolist()) + len(resultPE.values[0].data.tolist()) + 1 ))

        for i in range(len(elementSet.elements)):

            if resultName in resultSet.componentLabels: # Components

                minResult = maxResult = resultSet.values[i].data[resultSet.componentLabels.index(resultName)]

            else: # Categories

                minResult = min(resultSet.values[i].data)
                maxResult = max(resultSet.values[i].data)

            minPE = abs(min(resultPE.values[i].data,key=abs))
            maxPE = abs(max(resultPE.values[i].data,key=abs))

            filteredResults[i] = np.array(np.zeros(len(coordSet.componentLabels)).tolist() + [resultSet.values[i].elementLabel] + resultSet.values[i].data.tolist() + resultPE.values[i].data.tolist() + [np.nan])

            # If statement are to eliminate entries if they are true
            #   (for results categories, all entries must violate the limit to be eliminated)
            #   (for PE category, any entry can violate the limit to be eliminated)

            if limitTypeResult == 'lower' and maxResult < limitResult:

                filteredResults[i,-1] = np.inf

            if limitTypeResult == 'upper' and minResult > limitResult:

                filteredResults[i,-1] = np.inf

            if limitTypePE == 'lower' and minPE < limitPE:

                filteredResults[i,-1] = np.inf

            if limitTypePE == 'upper' and maxPE > limitPE:

                filteredResults[i,-1] = np.inf

            if not ( filteredResults[i,-1] == np.inf ):

                if 'coordElementSet' in locals():

                    filteredResults[i,0:len(coordElementSet.values[i].data.tolist())] = coordElementSet.values[i].data.tolist()

                else:

                    # #-----------------------------------------------------------------------

                    # connectedNodes = elementSet.elements[i].connectivity
                    # numConnectedNodes = len(connectedNodes)
                    # numComponents = len(coordSet.componentLabels)

                    # tempCoords = np.zeros(numComponents)

                    # for j in range(len(connectedNodes)):

                    #     tempCoords[0:numComponents] = tempCoords[0:numComponents] + ( np.array(coordSet.values[coordSetNodes.index(connectedNodes[j])].data) / float(len(connectedNodes)) )

                    # # print(tempCoords)

                    # filteredResults[i,0:numComponents] = tempCoords

                    # #-----------------------------------------------------------------------

                    #-----------------------------------------------------------------------

                    tempNodeCount = 0

                    tempElementCoords = np.zeros(len(coordSet.values[0].data))

                    for j in range(len(elementSet.elements[i].connectivity)):

                        for k in range(len(coordSet.values)):

                            if elementSet.elements[i].connectivity[j] == coordSet.values[k].nodeLabel:

                                for n in range(len(tempElementCoords)):

                                    tempElementCoords[n] = tempElementCoords[n] + ( coordSet.values[k].data[n] / float(len(elementSet.elements[i].connectivity)) )

                                tempNodeCount += 1

                                break

                        if tempNodeCount == len(elementSet.elements[i].connectivity):

                            break

                    filteredResults[i,0:len(coordSet.componentLabels)] = np.array(tempElementCoords)

                    #-----------------------------------------------------------------------

        filteredResults = filteredResults[np.isnan(filteredResults).any(axis=1)]

        #-----------------------------------------------------------------------

        if writeCSV:

            resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + resultName + '_' + 'ResultsZone' + '_' + ('%1.0E'%(limitPE)).rstrip('0').rstrip('.') + '_' + stepName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(resCSVname))

            titleRow = list(coordSet.componentLabels) + ['Element Label'] + list(resultSet.componentLabels) + list(resultPE.componentLabels)

            tempFile = open(resCSVname, 'wb')

            with open(resCSVname, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                for i in range(filteredResults.shape[0]):

                    csvWriter.writerow(filteredResults[i].tolist()[0:-1])

        return(filteredResults)

    #-----------------------------------------------------------------------

    def DensityGeneralResults(self,*args,**kwargs):

        sortedResults = kwargs.get('sortedResults', False)
        sortDirection = kwargs.get('sortDirection', 1)
        stepName = kwargs.get('stepName', 'Initial')
        frameNumber = kwargs.get('frameNumber', -1)
        instanceName = kwargs.get('instanceName', None)
        setName = kwargs.get('setName', None)
        resultName = kwargs.get('resultName', 'COORD')
        specialLocation = kwargs.get('specialLocation', None)
        includePE =  kwargs.get('includePE', False)
        writeCSV = kwargs.get('writeCSV', True)

        if sortDirection > 0: reverse = False
        elif sortDirection < 0: reverse = True

        try: self.odb.steps[stepName].frames[frameNumber].frameId
        except: return(1)

        frameId = self.odb.steps[stepName].frames[frameNumber].frameId

        unsortedResultSet = []

        #-----------------------------------------------------------------------

        # print(self.odb.steps[stepName].frames[frameNumber].fieldOutputs.keys())

        try: self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].nodeLabel
        except: return(1)

        if self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].nodeLabel:

            print('Running Sorting Routine:')
            print('  Part Instance: %s , nodeSet: %s' %(instanceName, setName))
            print('  Step Name: %s , Frame Index: %s, Frame Id: %s' %(stepName,frameNumber,frameId))
            print('  Data Key: %s , Sort Direciton: %s\n' %(resultName, sortDirection))

            nodeSet = self.odb.rootAssembly.instances[instanceName].nodeSets[setName]

            coordSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['COORD'].getSubset(region=nodeSet)

            resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=nodeSet)

            calculatedSet = []

            if includePE:

                resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)

                titleRow = ['nodeLabel'] + list(coordSet.componentLabels) + list(resultSet.componentLabels) + [resultPE.name]

            else:

                titleRow = ['nodeLabel'] + list(coordSet.componentLabels) + list(resultSet.componentLabels)

            #for i in range(len(nodeSet.nodes)): print('%s, %s, %s' %(nodeSet.nodes[i].label,coordSet.values[i].nodeLabel,resultSet.values[i].nodeLabel))

            unsortedResults = []

            for i in range(len(nodeSet.nodes)):

                if includePE:

                    unsortedResults.append([nodeSet.nodes[i].label] + coordSet.values[i].data.tolist() + resultSet.values[i].data.tolist() + resultPE.values[i].data.tolist())

                else:

                    unsortedResults.append([nodeSet.nodes[i].label] + coordSet.values[i].data.tolist() + resultSet.values[i].data.tolist())

        elif self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].elementLabel:

            print('Running Sorting Routine:')
            print('  Part Instance: %s , elementSet: %s' %(instanceName, setName))
            print('  Step Name: %s , Frame Index: %s, Frame Id: %s' %(stepName,frameNumber,frameId))
            print('  Data Key: %s , Sort Direciton: %s\n' %(resultName, sortDirection))

            nodeSet = self.odb.rootAssembly.instances[instanceName].nodeSets[setName]

            elementSet = self.odb.rootAssembly.instances[instanceName].elementSets[setName]

            coordSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['COORD'].getSubset(region=nodeSet)

            if specialLocation is not None: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=elementSet,position=specialLocation)
            else: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].getSubset(region=elementSet)

            if includePE:

                if specialLocation is not None: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet,position=specialLocation)
                else: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)

                if resultSet.componentLabels: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + list(resultSet.componentLabels) + list(resultPE.componentLabels)
                else: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + [resultSet.name] + ['normDp']+ list(resultPE.componentLabels)

            else:

                if resultSet.componentLabels: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + list(resultSet.componentLabels)
                else: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + [resultSet.name] + ['normDp']

            # for result in resultSet.values: print(result.data)

            #Normalized Change in Density Calculations

            if resultName == 'RD' or resultName == 'DENSITY':

                initialRD = self.odb.steps['Loading'].frames[0].fieldOutputs[resultName].getSubset(region=elementSet).values[0].data

                # print(initialRD)

                normDpSet = []

                for result in resultSet.values:

                    normDpSet.append((result.data-initialRD)/initialRD)

            elif resultName == 'PEQC4':

                normDpSet = []

                for result in resultSet.values:

                    normDpSet.append(np.exp(-result.data) - 1.0)

            #print(resultSet.values[0])

            coordSetNodes = []

            for i in range(len(coordSet.values)):

                coordSetNodes.append(coordSet.values[i].nodeLabel)

            #print(coordSetNodes)

            unsortedResults = []

            for i in range(len(elementSet.elements)):

                tempNodeCount = 0

                tempCoordSum = np.zeros(len(coordSet.values[0].data))

                for j in range(len(elementSet.elements[i].connectivity)):

                    if elementSet.elements[i].connectivity[j] in coordSetNodes:

                        tempNodeCount += 1

                        for n in range(len(tempCoordSum)):

                            tempCoordSum[n] += coordSet.values[coordSetNodes.index(elementSet.elements[i].connectivity[j])].data[n]

                for n in range(len(tempCoordSum)):

                    tempCoordSum[n] = tempCoordSum[n] / float(tempNodeCount)

                for m in range(len(resultSet.values)):

                    if resultSet.values[m].elementLabel == elementSet.elements[i].label:

                        if includePE:

                            try: unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + resultSet.values[m].data.tolist() + resultPE.values[m].data.tolist() )
                            except AttributeError: unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + [resultSet.values[m].data] + [normDpSet[m]] + resultPE.values[m].data.tolist() )

                        else:

                            try: unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + resultSet.values[m].data.tolist())
                            except AttributeError: unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + [resultSet.values[m].data] + [normDpSet[m]])

        if sortedResults: finalResults = sorted(unsortedResults, key=lambda unsortedResults: unsortedResults[abs(sortDirection)], reverse=reverse)
        else: finalResults = unsortedResults

        #for i in range(len(finalResults)): print(finalResults[i])

        if writeCSV:

            if resultName.startswith('CNORMF'): resultName = 'CNORMF'
            if resultName.startswith('CSHEARF'): resultName = 'CSHEARF'

            resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + resultName + '_' + stepName + '_' + instanceName + '-' + setName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(resCSVname))

            tempFile = open(resCSVname, 'wb')

            with open(resCSVname, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                for i in range(len(finalResults)):

                    csvWriter.writerow(finalResults[i])

        return(finalResults)

    #-----------------------------------------------------------------------

    def UnsortedResultsZone_Deprecated(self,*args,**kwargs):

        stepName = kwargs.get('stepName', 'Initial')
        frameNumber = kwargs.get('frameNumber', -1)
        instanceName = kwargs.get('instanceName', None)
        setName = kwargs.get('setName', None)
        resultName = kwargs.get('resultName', 'PE')
        limitResult = kwargs.get('limitResult', None)
        limitTypeResult = kwargs.get('limitTypeResult', 'lower')
        specialLocation = kwargs.get('specialLocation', None)
        limitPE = kwargs.get('limitPE', 1e-05)
        limitTypePE = kwargs.get('limitType', 'lower')
        writeCSV = kwargs.get('writeCSV', True)

        frameId = self.odb.steps[stepName].frames[frameNumber].frameId

        resultCategory = resultName.rstrip('1').rstrip('2').rstrip('3')

        unsortedResultSet = []

        #-----------------------------------------------------------------------

        print('Running Unsorted Results Routine:')
        print('  Part Instance: %s , elementSet: %s' %(instanceName, setName))
        print('  Step Name: %s , Frame Index: %s, Frame Id: %s' %(stepName,frameNumber,frameId))
        print('  Data Key: %s\n' %(resultName))

        nodeSet = self.odb.rootAssembly.instances[instanceName].nodeSets[setName]

        elementSet = self.odb.rootAssembly.instances[instanceName].elementSets[setName]

        coordSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['COORD'].getSubset(region=nodeSet)

        resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultCategory].getSubset(region=elementSet)

        if specialLocation is not None: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultCategory].getSubset(region=elementSet,position=specialLocation)
        else: resultSet = self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultCategory].getSubset(region=elementSet)

        if specialLocation is not None: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet,position=specialLocation)
        else: resultPE = self.odb.steps[stepName].frames[frameNumber].fieldOutputs['PE'].getSubset(region=elementSet)

        #-----------------------------------------------------------------------
        #This is the custom elemental results section, where selections are made before sorting occurs
        #-----------------------------------------------------------------------

        customResults = []

        if limitResult is not None:

            if limitTypeResult == 'lower' and limitTypePE == 'lower':

                for i in range(len(resultPE.values)):

                    if resultSet.values[i].data[resultSet.componentLabels.index(resultName)] > limitResult and abs(max(resultPE.values[i].data,key=abs)) > limitPE:

                        customResults.append([elementSet.elements[i].label,elementSet.elements[i].connectivity,resultSet.values[i].elementLabel] + resultSet.values[i].data.tolist() + resultPE.values[i].data.tolist())

            elif limitTypeResult == 'lower' and limitTypePE == 'upper':

                for i in range(len(resultPE.values)):

                    if resultSet.values[i].data[resultSet.componentLabels.index(resultName)] > limitResult and abs(max(resultPE.values[i].data,key=abs)) < limitPE:

                        customResults.append([elementSet.elements[i].label,elementSet.elements[i].connectivity,resultSet.values[i].elementLabel] + resultSet.values[i].data.tolist() + resultPE.values[i].data.tolist())

            elif limitTypeResult == 'upper' and limitTypePE == 'lower':

                for i in range(len(resultPE.values)):

                    if resultSet.values[i].data[resultSet.componentLabels.index(resultName)] < limitResult and abs(max(resultPE.values[i].data,key=abs)) > limitPE:

                        customResults.append([elementSet.elements[i].label,elementSet.elements[i].connectivity,resultSet.values[i].elementLabel] + resultSet.values[i].data.tolist() + resultPE.values[i].data.tolist())

            elif limitTypeResult == 'upper' and limitTypePE == 'upper':

                for i in range(len(resultPE.values)):

                    if resultSet.values[i].data[resultSet.componentLabels.index(resultName)] < limitResult and abs(max(resultPE.values[i].data,key=abs)) < limitPE:

                        customResults.append([elementSet.elements[i].label,elementSet.elements[i].connectivity,resultSet.values[i].elementLabel] + resultSet.values[i].data.tolist() + resultPE.values[i].data.tolist())

        else:

            if limitTypePE == 'lower':

                for i in range(len(resultPE.values)):

                    if abs(max(resultPE.values[i].data,key=abs)) > limitPE:

                        customResults.append([elementSet.elements[i].label,elementSet.elements[i].connectivity,resultSet.values[i].elementLabel] + resultSet.values[i].data.tolist() + resultPE.values[i].data.tolist())

            elif limitTypePE == 'upper':

                for i in range(len(resultPE.values)):

                    if abs(max(resultPE.values[i].data,key=abs)) < limitPE:

                        customResults.append([elementSet.elements[i].label,elementSet.elements[i].connectivity,resultSet.values[i].elementLabel] + resultSet.values[i].data.tolist() + resultPE.values[i].data.tolist())

            else:

                return(1)

        # for result in customResults: print(result)

        #-----------------------------------------------------------------------

        coordSetNodes = []

        for i in range(len(coordSet.values)):

            coordSetNodes.append(coordSet.values[i].nodeLabel)

        # print(coordSetNodes)

        #-----------------------------------------------------------------------

        unsortedResults = []

        for i in range(len(customResults)):

            tempNodeCount = 0

            tempCoordSum = np.zeros(len(coordSet.values[0].data))

            for j in range(len(customResults[i][1])):

                if customResults[i][1][j] in coordSetNodes:

                    tempNodeCount += 1

                    for n in range(len(tempCoordSum)):

                        tempCoordSum[n] += coordSet.values[coordSetNodes.index(customResults[i][1][j])].data[n]

            for n in range(len(tempCoordSum)):

                tempCoordSum[n] = tempCoordSum[n] / float(tempNodeCount)

            unsortedResults.append(tempCoordSum.tolist() + customResults[i])

        #-----------------------------------------------------------------------

        if writeCSV:

            resCSVname = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + resultName + '_' + 'ResultsZone' + '_' + ('%1.0E'%(limitPE)).rstrip('0').rstrip('.') + '_' + stepName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(resCSVname))

            titleRow = list(coordSet.componentLabels) + ['Element Label','Element Connectivity'] + ['ElementLabel'] + list(resultSet.componentLabels) + list(resultPE.componentLabels)

            tempFile = open(resCSVname, 'wb')

            with open(resCSVname, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                for i in range(len(unsortedResults)):

                    csvWriter.writerow(unsortedResults[i])

        return(unsortedResults)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

# End of Plugin

#--------------------------------------------------------------------------------------------------