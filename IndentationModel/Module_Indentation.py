#--------------------------------------------------------------------------------------------------

from abaqusConstants import *

#--------------------------------------------------------------------------------------------------

class General_Analysis(object):

    #-----------------------------------------------------------------------

    def __init__(self):

        return(None)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createElasticMaterials(self,*args,**kwargs):

        self.indType = kwargs.get('indType','Rigid' )
        self.taMatName = kwargs.get('taMatName','a-SiO2')
        self.taMatYM = kwargs.get('taMatYM',70.0e3)
        self.taMatPR = kwargs.get('taMatPR',0.15)
        self.taMatDens = kwargs.get('taMatDens',2.20e-9)
        self.taMatRayDamp = kwargs.get('taMatRayDamp',(0.0,0.0))

        #Indenter: Linear-Elastic
        if self.indType == 'Deformable':

            self.indMatName = kwargs.get('indMatName','Diamond')

            if self.indMatName == 'Diamond':

                self.indMatYM = 1220e3
                self.indMatPR = 0.20
                self.indMatDens = 3.52e-9
                # self.indMatDens = 1.00e-9 #why this reduction in indenter density?

            elif self.indMatName == 'Sapphire':

                self.indMatYM = 345e3
                self.indMatPR = 0.29
                self.indMatDens = 3.98e-9
                # self.indMatDens = 1.00e-9 #why this reduction in indenter density?

            else:

                if self.indMatName.endswith(' (Specify Below)'): self.indMatName = self.indMatName.rstrip(' (Specify Below)')

                self.indMatYM = kwargs.get('indMatYM',0.0)
                self.indMatPR = kwargs.get('indMatPR',0.0)
                self.indMatDens = kwargs.get('indMatDens',0.0)

            self.mdb.models['Model-1'].Material(name='Elastic_'+self.indMatName)
            self.mdb.models['Model-1'].materials['Elastic_'+self.indMatName].Elastic(table=((self.indMatYM, self.indMatPR), ))
            self.mdb.models['Model-1'].materials['Elastic_'+self.indMatName].Density(table=((self.indMatDens, ), ))
            self.mdb.models['Model-1'].HomogeneousSolidSection(name='Elastic_'+self.indMatName, material='Elastic_'+self.indMatName, thickness=None)

        else:

            self.indMatName = None
            self.indMatYM = None
            self.indMatPR = None
            self.indMatDens = None

        #Test Article: Linear-Elastic
        self.mdb.models['Model-1'].Material(name='Elastic_'+self.taMatName)
        self.mdb.models['Model-1'].materials['Elastic_'+self.taMatName].Elastic(table=((self.taMatYM, self.taMatPR), ))
        self.mdb.models['Model-1'].materials['Elastic_'+self.taMatName].Density(table=((self.taMatDens, ), ))
        if self.analysisType.startswith('Explicit'): self.mdb.models['Model-1'].materials['Elastic_'+self.taMatName].Damping(alpha=self.taMatRayDamp[0], beta=self.taMatRayDamp[1])
        self.mdb.models['Model-1'].HomogeneousSolidSection(name='Elastic_'+self.taMatName, material='Elastic_'+self.taMatName, thickness=None)

        return(self.indMatName,self.indMatYM,self.indMatPR,self.indMatDens)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createPlasticMaterials(self,*args,**kwargs):

        self.taMatPlast = kwargs.get('taMatPlast','vonMises')

        self.taMatYSmin = kwargs.get('taMatYSmin',7.50e3)

        self.taMatGTNrd = kwargs.get('taMatGTNrd',1.0)
        self.taMatGTNq = kwargs.get('taMatGTNq',(1.0,1.0,1.0))

        self.taMatKerm = kwargs.get('taMatKerm',(6500.0, -11500.0, 100000.0))

        self.taMatMoln = kwargs.get('taMatMoln',(5.0, 5700.0, 5000.0, -3000.0, -0.196, 3.0, 4.0, -20000.0, 7000.0))

        self.taMatDPCap = kwargs.get('taMatDPCap',(6500.0, 0.001, 1.75, 11500.0, 0.05, 1.0))
        self.taMatDPCapHard = kwargs.get('taMatDPCapHard',((11500.0, 0.0), (12500.0, 0.01)))

        # matPostYielding = kwargs.get('matPostYielding',[1.00,0.10])

        if self.taMatPlast == 'vonMises':

            self.mdb.models['Model-1'].Material(name=self.taMatPlast+'_'+self.taMatName)
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Elastic(table=((self.taMatYM, self.taMatPR), ))
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Density(table=((self.taMatDens, ), ))
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Plastic(table=((self.taMatYSmin, 0.0),))

        elif self.taMatPlast == 'Gurson-Tvergaard-Needleman Porous Metal Plasticity' or self.taMatPlast == 'GTN-pmp':

            self.taMatPlast = 'GTN-pmp'

            self.mdb.models['Model-1'].Material(name=self.taMatPlast+'_'+self.taMatName)
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Elastic(table=((self.taMatYM, self.taMatPR), ))
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Density(table=((self.taMatDens, ), ))
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Plastic(table=((self.taMatYSmin, 0.0),))
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].PorousMetalPlasticity(relativeDensity=self.taMatGTNrd, table=(self.taMatGTNq, ))

        elif self.taMatPlast == 'Drucker-Prager Cap wHardening' or self.taMatPlast == 'DP-Cap':

            self.tamatPlast = 'DP-Cap'

            self.mdb.models['Model-1'].Material(name=self.taMatPlast+'_'+self.taMatName)
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Elastic(table=((self.taMatYM, self.taMatPR), ))
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Density(table=((self.taMatDens, ), ))
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].CapPlasticity(table=(self.taMatDPCap, ))
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].capPlasticity.CapHardening(table=self.taMatDPCapHard)

        elif self.taMatPlast == 'Elliptical (Kermouche,2008)' or self.taMatPlast == 'Kerm2008':

            self.taMatPlast = 'Kerm2008'

            self.mdb.models['Model-1'].Material(name=self.taMatPlast+'_'+self.taMatName)
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Density(table=((self.taMatDens, ), ))
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Depvar(n=9)
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].UserMaterial(mechanicalConstants=([self.taMatYM,self.taMatPR] + list(self.taMatKerm)))

        elif self.taMatPlast == 'Drucker-Prager-Cap (Molnar,2017)' or self.taMatPlast == 'Moln2017':

            self.taMatPlast = 'Moln2017'

            self.mdb.models['Model-1'].Material(name=self.taMatPlast+'_'+self.taMatName)
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Density(table=((self.taMatDens, ), ))
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].Depvar(n=11)
            self.mdb.models['Model-1'].materials[self.taMatPlast+'_'+self.taMatName].UserMaterial(mechanicalConstants=([self.taMatYM,self.taMatPR] + list(self.taMatMoln)))

        self.mdb.models['Model-1'].HomogeneousSolidSection(name=self.taMatPlast+'_'+self.taMatName, material=self.taMatPlast+'_'+self.taMatName, thickness=None)

        # # #Test Article Plasticity: simple yield hardening/softening added to all materials with a 'plastic' attribute
        # # matPostYieldingTable = ((self.matYSmin, 0.0), (matPostYielding[0]*self.matYSmin, matPostYielding[1]), (matPostYielding[0]*self.matYSmin, 1.0))

        # # for self.taMatNameIter in  self.mdb.models['Model-1'].materials.keys():

            # # if hasattr(self.mdb.models['Model-1'].materials[self.taMatNameIter], 'plastic'):

                # # self.mdb.models['Model-1'].Material(name='PostYield_' + self.taMatNameIter,  objectToCopy=self.mdb.models['Model-1'].materials[self.taMatNameIter])

                # # self.mdb.models['Model-1'].materials['PostYield_' + self.taMatNameIter].Plastic(table=matPostYieldingTable)

                # # self.mdb.models['Model-1'].HomogeneousSolidSection(name='PostYield_' + self.taMatNameIter.rstrip('Material'), material='PostYield_' + self.taMatNameIter , thickness=None)

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createSteps(self,*args,**kwargs):

        self.stepTime = args[0]

        self.fieldIntervals = kwargs.get('fieldIntervals',100)
        self.historyIntervals = kwargs.get('historyIntervals',100)
        self.bulkViscosity = kwargs.get('bulkViscosity',[0.06,0.06,0.06,0.06])

        from caeModules import step

        if self.analysisType.startswith('Standard'):

            if self.analysisType.endswith('- Static'):

                self.mdb.models['Model-1'].StaticStep(name='Loading', previous='Initial',
                    maxNumInc=10000, stabilizationMagnitude=0.0002, timePeriod=self.stepTime[0],
                    stabilizationMethod=DISSIPATED_ENERGY_FRACTION,
                    continueDampingFactors=False, adaptiveDampingRatio=0.05, initialInc=self.stepTime[0]*1e-05,
                    minInc=1e-15, matrixSolver=DIRECT, matrixStorage=UNSYMMETRIC, nlgeom=ON)

                self.mdb.models['Model-1'].StaticStep(name='Unloading', previous='Loading',
                    maxNumInc=10000, stabilizationMagnitude=0.0002, timePeriod=self.stepTime[2],
                    stabilizationMethod=DISSIPATED_ENERGY_FRACTION,
                    continueDampingFactors=False, adaptiveDampingRatio=0.05, initialInc=self.stepTime[2]*1e-05,
                    minInc=1e-15, matrixSolver=DIRECT, matrixStorage=UNSYMMETRIC)

            elif self.analysisType.endswith('- Quasi-Static'):

                if self.stepTime[1] > 0.0:

                    self.mdb.models['Model-1'].ImplicitDynamicsStep(name='Loading', previous='Initial',
                        maxNumInc=10000, application=QUASI_STATIC, initialInc=self.stepTime[0]*1e-05, minInc=1e-15, timePeriod=self.stepTime[0],
                        nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF,
                        matrixStorage=UNSYMMETRIC, nlgeom=ON)

                    self.mdb.models['Model-1'].ImplicitDynamicsStep(name='Dwell-Loaded', previous='Loading',
                        maxNumInc=10000, application=QUASI_STATIC, initialInc=self.stepTime[1]*1e-05, minInc=1e-15, timePeriod=self.stepTime[1],
                        nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF,
                        matrixStorage=UNSYMMETRIC, nlgeom=ON)

                    self.mdb.models['Model-1'].ImplicitDynamicsStep(name='Unloading', previous='Dwell-Loaded',
                        maxNumInc=10000, application=QUASI_STATIC, initialInc=self.stepTime[2]*1e-05, minInc=1e-15, timePeriod=self.stepTime[2],
                        nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF,
                        matrixStorage=UNSYMMETRIC)

                else:

                    self.mdb.models['Model-1'].ImplicitDynamicsStep(name='Loading', previous='Initial',
                        maxNumInc=10000, application=QUASI_STATIC, initialInc=self.stepTime[0]*1e-05, minInc=1e-15, timePeriod=self.stepTime[0],
                        nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF,
                        matrixStorage=UNSYMMETRIC, nlgeom=ON)

                    self.mdb.models['Model-1'].ImplicitDynamicsStep(name='Unloading', previous='Loading',
                        maxNumInc=10000, application=QUASI_STATIC, initialInc=self.stepTime[2]*1e-05, minInc=1e-15, timePeriod=self.stepTime[2],
                        nohaf=OFF, amplitude=RAMP, alpha=DEFAULT, initialConditions=OFF,
                        matrixStorage=UNSYMMETRIC)

            else: raise ValueError('Analysis type chosen is not valid.')

            print self.jobName

            if self.jobName.endswith('_pre'):

                print('Here!')

                del self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1']
                self.mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(numIntervals=self.historyIntervals)

                regionDef1=self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                regionDef2=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Base_Set']
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Force_Combo_A', createStepName='Loading', variables=('U', ), numIntervals=self.historyIntervals, timeMarks=ON, region=regionDef1, sectionPoints=DEFAULT, rebar=EXCLUDE)
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Force_Combo_B', createStepName='Loading', variables=('RF', ), numIntervals=self.historyIntervals, timeMarks=ON, region=regionDef2, sectionPoints=DEFAULT, rebar=EXCLUDE)

            else:

                self.mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(numIntervals=self.historyIntervals)

                if self.indType == 'Rigid':

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                    self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'COORD'), region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.fieldIntervals, timeMarks=ON)

                elif self.indType == 'Deformable':

                    # self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'COORD'), region=MODEL, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.fieldIntervals, timeMarks=ON)

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                    self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'COORD'), region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.fieldIntervals, timeMarks=ON)

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Indenter-1'].sets['Set-1']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='F-Output-2', createStepName='Loading', variables=('LE', 'U', 'COORD'),
                        numIntervals=self.fieldIntervals, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                if self.taMatPlast == 'GTN-pmp':

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Mat_Plastic_Set']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='Plastic_Zone', createStepName='Loading', variables=('PE', 'PEEQ', 'VVF','VVFG','VVFN', 'RD'),
                        numIntervals=self.fieldIntervals, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                else:

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Mat_Plastic_Set']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='Plastic_Zone', createStepName='Loading', variables=('PE', 'PEEQ', 'RD'),
                        numIntervals=self.fieldIntervals, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                self.mdb.models['Model-1'].FieldOutputRequest(name='Contact_Results', createStepName='Loading', variables=('CSTRESS', 'CDISP', 'CFORCE'), numIntervals=self.fieldIntervals, timeMarks=ON)

                # regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                # self.mdb.models['Model-1'].FieldOutputRequest(name='Elemental_Energies_Volumes', createStepName='Loading', variables=('ENER', 'ELEN', 'ELEDEN', 'EVOL', 'IVOL'),
                    # numIntervals=self.fieldIntervals, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                regionDef1=self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                regionDef2=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Base_Set']
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Force_Combo_A', createStepName='Loading', variables=('U', ), numIntervals=self.historyIntervals, timeMarks=ON, region=regionDef1, sectionPoints=DEFAULT, rebar=EXCLUDE)
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Force_Combo_B', createStepName='Loading', variables=('RF', ), numIntervals=self.historyIntervals, timeMarks=ON, region=regionDef2, sectionPoints=DEFAULT, rebar=EXCLUDE)

            self.mdb.models['Model-1'].SmoothStepAmplitude(name='Std-Indent-Smooth', timeSpan=STEP, data=((0.0, 0.0), (self.stepTime[0], 1.0)))
            self.mdb.models['Model-1'].SmoothStepAmplitude(name='Std-Remove-Smooth', timeSpan=STEP, data=((0.0, 1.0), (self.stepTime[2], 0.0)))

            self.mdb.models['Model-1'].TabularAmplitude(name='Std-Indent-Tabular', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (self.stepTime[0], 1.0)))
            self.mdb.models['Model-1'].TabularAmplitude(name='Std-Remove-Tabular', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 1.0), (self.stepTime[2], 0.0)))

            #Gives up after 20 unconverged iterations (instead of 5)
            self.mdb.models['Model-1'].steps['Loading'].control.setValues(allowPropagation=OFF, resetDefaultValues=OFF, timeIncrementation=(4.0, 8.0, 9.0, 16.0, 10.0, 4.0, 12.0, 20.0, 6.0, 3.0, 50.0))

        elif self.analysisType.startswith('Explicit'):

            if self.stepTime[1] > 0.0:

                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Loading', previous='Initial', timePeriod=self.stepTime[0])
                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Dwell-Loaded', previous='Loading', timePeriod=self.stepTime[1])
                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Unloading', previous='Dwell-Loaded', timePeriod=self.stepTime[2])

                self.mdb.models['Model-1'].steps['Loading'].setValues(linearBulkViscosity=self.bulkViscosity[0])
                self.mdb.models['Model-1'].steps['Dwell-Loaded'].setValues(linearBulkViscosity=self.bulkViscosity[1])
                self.mdb.models['Model-1'].steps['Unloading'].setValues(linearBulkViscosity=self.bulkViscosity[2])

                self.mdb.models['Model-1'].steps['Loading'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)
                self.mdb.models['Model-1'].steps['Dwell-Loaded'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)
                self.mdb.models['Model-1'].steps['Unloading'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)

            else:

                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Loading', previous='Initial', timePeriod=self.stepTime[0])
                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Unloading', previous='Loading', timePeriod=self.stepTime[2])

                self.mdb.models['Model-1'].steps['Loading'].setValues(linearBulkViscosity=self.bulkViscosity[0])
                self.mdb.models['Model-1'].steps['Unloading'].setValues(linearBulkViscosity=self.bulkViscosity[2])

                self.mdb.models['Model-1'].steps['Loading'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)
                self.mdb.models['Model-1'].steps['Unloading'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)

            if self.stepTime[3] > 0.0:

                self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Dwell-Unloaded', previous='Unloading', timePeriod=self.stepTime[3])
                self.mdb.models['Model-1'].steps['Dwell-Unloaded'].setValues(linearBulkViscosity=self.bulkViscosity[3])
                self.mdb.models['Model-1'].steps['Dwell-Unloaded'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)

            if self.analysisType.endswith('Mass Scaling'):

                self.mdb.models['Model-1'].steps['Loading'].setValues(massScaling=((SEMI_AUTOMATIC, MODEL, THROUGHOUT_STEP, 0.0, 1.0, BELOW_MIN, 100, 0, 0.0, 0.0, 0, None), ))

            if self.jobName.endswith('_pre'):

                del self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1']
                self.mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(numIntervals=self.historyIntervals)

                regionDef1=self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                regionDef2=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Base_Set']
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Part_A', createStepName='Loading', variables=('U', 'RF'), numIntervals=self.historyIntervals, timeMarks=ON, region=regionDef1, sectionPoints=DEFAULT, rebar=EXCLUDE)
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Part_B', createStepName='Loading', variables=('U', 'RF'), numIntervals=self.historyIntervals, timeMarks=ON, region=regionDef2, sectionPoints=DEFAULT, rebar=EXCLUDE)

            else:

                self.mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(numIntervals=self.historyIntervals)

                if self.indType == 'Rigid':

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                    self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'V', 'A', 'COORD'), region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.fieldIntervals, timeMarks=ON)

                elif self.indType == 'Deformable':

                    # self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'V', 'A', 'COORD'), region=MODEL, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.fieldIntervals, timeMarks=ON)

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                    self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'LE', 'U', 'V', 'A', 'COORD'), region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE, numIntervals=self.fieldIntervals, timeMarks=ON)

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Indenter-1'].sets['Set-1']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='F-Output-2', createStepName='Loading', variables=('LE', 'U', 'V', 'A', 'COORD'),
                        numIntervals=self.fieldIntervals, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                if self.taMatPlast == 'GTN-pmp':

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Mat_Plastic_Set']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='Plastic_Zone', createStepName='Loading', variables=('PE', 'PEEQ', 'DENSITY', 'VVF','VVFG','VVFN'),
                        numIntervals=self.fieldIntervals, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                else:

                    regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Mat_Plastic_Set']
                    self.mdb.models['Model-1'].FieldOutputRequest(name='Plastic_Zone', createStepName='Loading', variables=('PE', 'PEEQ', 'DENSITY'),
                        numIntervals=self.fieldIntervals, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                self.mdb.models['Model-1'].FieldOutputRequest(name='Contact_Results', createStepName='Loading', variables=('CSTRESS', 'CDISP', 'CFORCE', 'FSLIPR', 'FSLIP'), numIntervals=self.fieldIntervals, timeMarks=ON)

                # regionDef=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Set-1']
                # self.mdb.models['Model-1'].FieldOutputRequest(name='Elemental_Energies_Volumes', createStepName='Loading', variables=('ENER', 'ELEN', 'ELEDEN', 'EDCDEN', 'EDT', 'EVOL'),
                    # numIntervals=self.fieldIntervals, timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

                regionDef1=self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                regionDef2=self.mdb.models['Model-1'].rootAssembly.allInstances['Test_Article-1'].sets['Base_Set']
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Part_A', createStepName='Loading', variables=('U', 'RF'), numIntervals=self.historyIntervals, timeMarks=ON, region=regionDef1, sectionPoints=DEFAULT, rebar=EXCLUDE)
                self.mdb.models['Model-1'].FieldOutputRequest(name='Reaction_Part_B', createStepName='Loading', variables=('U', 'RF'), numIntervals=self.historyIntervals, timeMarks=ON, region=regionDef2, sectionPoints=DEFAULT, rebar=EXCLUDE)

            self.mdb.models['Model-1'].SmoothStepAmplitude(name='Exp-Indent-Smooth', timeSpan=STEP, data=((0.0, 0.0), (self.stepTime[0], 1.0)))
            self.mdb.models['Model-1'].SmoothStepAmplitude(name='Exp-Remove-Smooth', timeSpan=STEP, data=((0.0, 1.0), (self.stepTime[2], 0.0)))

            self.mdb.models['Model-1'].TabularAmplitude(name='Exp-Indent-Tabular', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (self.stepTime[0], 1.0)))
            self.mdb.models['Model-1'].TabularAmplitude(name='Exp-Remove-Tabular', timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 1.0), (self.stepTime[2], 0.0)))

        else: raise ValueError('Analysis type chosen is not valid.')

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createRemeshing(self,*args,**kwargs):

        self.remeshingParameters = kwargs.get('remeshingParameters',[1,2])

        if self.analysisType.startswith('Explicit'):

            self.mdb.models['Model-1'].AdaptiveMeshControl(name='Adaptive_Mesh_Control')
            # self.mdb.models['Model-1'].adaptiveMeshControls['Adaptive_Mesh_Control'].setValues(smoothingPriority=GRADED,smoothingAlgorithm=GEOMETRY_ENHANCED)
            self.mdb.models['Model-1'].adaptiveMeshControls['Adaptive_Mesh_Control'].setValues(smoothingPriority=UNIFORM) #"Improved Aspect Ratio"
            self.mdb.models['Model-1'].adaptiveMeshControls['Adaptive_Mesh_Control'].setValues(smoothingAlgorithm=ANALYSIS_PRODUCT_DEFAULT)

            region=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].sets['Remeshing_Set']
            self.mdb.models['Model-1'].steps['Loading'].AdaptiveMeshDomain(region=region, controls='Adaptive_Mesh_Control')

            self.mdb.models['Model-1'].adaptiveMeshControls['Adaptive_Mesh_Control'].setValues(volumetricSmoothingWeight=0.50, laplacianSmoothingWeight=0.50, equipotentialSmoothingWeight=0.00)
            self.mdb.models['Model-1'].steps['Loading'].adaptiveMeshDomains['Loading'].setValues(frequency=self.remeshingParameters[0], meshSweeps=self.remeshingParameters[1])

            if self.taType.endswith('Pillar'):

                region=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].sets['Remeshing_Set']
                self.mdb.models['Model-1'].steps['Unloading'].AdaptiveMeshDomain(region=region, controls='Adaptive_Mesh_Control')

                self.mdb.models['Model-1'].adaptiveMeshControls['Adaptive_Mesh_Control'].setValues(volumetricSmoothingWeight=0.50, laplacianSmoothingWeight=0.50, equipotentialSmoothingWeight=0.00)
                self.mdb.models['Model-1'].steps['Unloading'].adaptiveMeshDomains['Unloading'].setValues(frequency=self.remeshingParameters[0], meshSweeps=self.remeshingParameters[1])



        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createPredefinedField(self,*args,**kwargs):

        self.biaxialPrestress = args[0]

        if self.analysisType.startswith('Standard'):

            #The standard solver may not work yet, top may rise...

            a = self.mdb.models['Model-1'].rootAssembly
            region = a.instances['Test_Article-1'].sets['Set-1']
            self.mdb.models['Model-1'].Stress(name='Bi-Axial Pre-Stress', region=region,
                distributionType=UNIFORM, sigma11=self.biaxialPrestress, sigma22=0.0, sigma33=self.biaxialPrestress, sigma12=0.0, sigma13=0.0, sigma23=0.0)

        elif self.analysisType.startswith('Explicit'):

            self.mdb.models['Model-1'].ExplicitDynamicsStep(name='Pre-Stress', previous='Initial', timePeriod=self.stepTime[0])
            self.mdb.models['Model-1'].steps['Pre-Stress'].setValues(linearBulkViscosity=self.bulkViscosity[0])
            self.mdb.models['Model-1'].steps['Pre-Stress'].setValues(timeIncrementationMethod=AUTOMATIC_EBE, scaleFactor=1.0, maxIncrement=None)
            self.mdb.models['Model-1'].steps['Pre-Stress'].setValues(massScaling=((SEMI_AUTOMATIC, MODEL, THROUGHOUT_STEP, 0.0, 1.0, BELOW_MIN, 100, 0, 0.0, 0.0, 0, None), ))

            self.mdb.models['Model-1'].fieldOutputRequests['Contact_Results'].move('Loading', 'Pre-Stress')
            self.mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].move('Loading', 'Pre-Stress')
            self.mdb.models['Model-1'].fieldOutputRequests['F-Output-2'].move('Loading', 'Pre-Stress')
            self.mdb.models['Model-1'].fieldOutputRequests['Plastic_Zone'].move('Loading', 'Pre-Stress')
            self.mdb.models['Model-1'].fieldOutputRequests['Reaction_Part_A'].move('Loading', 'Pre-Stress')
            self.mdb.models['Model-1'].fieldOutputRequests['Reaction_Part_B'].move('Loading', 'Pre-Stress')
            self.mdb.models['Model-1'].historyOutputRequests['H-Output-1'].move('Loading', 'Pre-Stress')

            a = self.mdb.models['Model-1'].rootAssembly
            region = a.instances['Test_Article-1'].surfaces['OD_Surf']
            self.mdb.models['Model-1'].Pressure(name='Pre-Stress_Pressure',
                createStepName='Pre-Stress', region=region, distributionType=UNIFORM,
                field='', magnitude=self.biaxialPrestress, amplitude='Exp-Indent-Smooth')

            region = a.instances['Test_Article-1'].sets['Top_Set']
            self.mdb.models['Model-1'].DisplacementBC(name='TA_Top_Axial-Fixed_BC',
                createStepName='Initial', region=region, u1=UNSET, u2=0.0, ur3=UNSET,
                amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
            self.mdb.models['Model-1'].boundaryConditions['TA_Top_Axial-Fixed_BC'].deactivate('Loading')
            self.mdb.models['Model-1'].boundaryConditions['TA_Bottom_Axial-Fixed_BC'].move('Initial', 'Loading')

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createJob(self,*args,**kwargs):

        self.jobname = args[0]
        self.numCPU = args[1]

        self.jobSubmit = kwargs.get('jobSubmit',False)
        self.inpFile = kwargs.get('inpFile',False)

        from caeModules import job

        import os

        self.mdb.Job(name=self.jobname, model='Model-1', description='',
            type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
            memory=90, memoryUnits=PERCENTAGE, explicitPrecision=SINGLE,
            nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF,
            contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='',
            resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=self.numCPU,
            activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=self.numCPU)

        # self.mdb.jobs[self.jobname].setValues(explicitPrecision=DOUBLE)

        # if self.taMatPlast == 'Kerm2008': self.mdb.jobs[self.jobname].setValues(userSubroutine='C:\\Abaqus\\Temp\\kermouche2008.for')
        # if self.taMatPlast == 'Moln2017': self.mdb.jobs[self.jobname].setValues(userSubroutine='C:\\Abaqus\\Temp\\molnar2017.for')

        if self.taMatPlast == 'Kerm2008': self.mdb.jobs[self.jobname].setValues(userSubroutine='%s\\abaqus_plugins\\MicroIndentModel\\kermouche2008.for' %(os.path.expanduser('~')))
        if self.taMatPlast == 'Moln2017': self.mdb.jobs[self.jobname].setValues(userSubroutine='%s\\abaqus_plugins\\MicroIndentModel\\molnar2017.for' %(os.path.expanduser('~')))

        if self.jobSubmit:

            self.mdb.jobs[self.jobname].submit(consistencyChecking=OFF)

        elif self.inpFile:

            self.mdb.jobs[self.jobname].writeInput(consistencyChecking=OFF)

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def setView(self,*args,**kwargs):

        from abaqus import session

        a = self.mdb.models['Model-1'].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        if self.mdb.models['Model-1'].parts['Test_Article'].space == AXISYMMETRIC: session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
        else: session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
        session.viewports['Viewport: 1'].view.fitView()
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
        session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=ON)

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def expectedDepthForce(self,*args,**kwargs):

        self.jobName = args[0]
        self.indenterForce = args[1]

        import sys

        from subprocess import call

        print('Predicting Indenter Depth for Force (%s) in Job (%s)...' %(self.indenterForce,self.jobName))

        print >> sys.__stdout__, ('Predicting Indenter Depth for Force (%s) in Job (%s)...' %(self.indenterForce,self.jobName))

        call([r'C:\SIMULIA\Commands\abaqus.bat','python',r'C:\Abaqus\WorkingFiles\Mio\Mio_Local_RF_Output_rev2019-03-28a.py',self.jobName,self.analysisType])

        if self.analysisType.startswith('Standard'):

            csvName = r'C:\Abaqus\Mio\TransferOutbound' + '\\' + self.jobName + '_pre_RF_Work' + '_Base' + '.csv'

        elif self.analysisType.startswith('Explicit'):

            csvName = r'C:\Abaqus\Mio\TransferOutbound' + '\\' + self.jobName + '_pre_RF_Work' + '_Ind' + '.csv'

        import csv

        with open(csvName, 'rb') as tempFile:

            tempReader = csv.reader(tempFile)

            for row in tempReader:

                if row[0] == 'Loading':

                    print('Step: %s, Disp: %s, Force: %s' %(row[0],row[16],row[22]))

                    print self.indenterForce

                    if float(row[22]) > self.indenterForce:

                        highValues = [float(row[16]),float(row[22])]

                        break

                    lowValues = [float(row[16]),float(row[22])]

        try: indenterDepth = ((highValues[0]-lowValues[0])/(highValues[1]-lowValues[1])) * (self.indenterForce-lowValues[1]) + lowValues[0]
        except: raise ValueError('The pre_upg_RF_Work.csv needs to have values at greater depth; redo pre-analysis with greater depth.')

        print >> sys.__stdout__, ('Predicted Indenter Depth: %s um' %(indenterDepth))

        return(indenterDepth)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def expectedDepthEnergy(self,*args,**kwargs): #This function is in-work, hasn't been fully tested yet!

        self.jobName = args[0]
        self.inputEnergy = args[1]

        import sys

        from subprocess import call

        print('Predicting Indenter Depth for Energy (%s) in Job (%s)...' %(self.inputEnergy,self.jobName))

        print >> sys.__stdout__, ('Predicting Indenter Depth for Energy (%s) in Job (%s)...' %(self.inputEnergy,self.jobName))

        call([r'C:\SIMULIA\Commands\abaqus.bat','python',r'C:\Abaqus\WorkingFiles\Mio\Mio_Local_RF_Output_rev2018-11-21a.py',self.jobName])

        csvName = r'C:\Abaqus\Mio\TransferOutbound' + '\\' + self.jobName + '_pre_RF_Work' + '_Ind' + '.csv'

        import csv

        with open(csvName, 'rb') as tempFile:

            tempReader = csv.reader(tempFile)

            for row in tempReader:

                if row[0] == 'Loading':

                    # print('Step: %s, Disp: %s, Energy: %s' %(row[0],row[15],row[13]))

                    # print self.inputEnergy

                    if float(row[13]) > self.inputEnergy:

                        highValues = [float(row[15]),float(row[13])]

                        break

                    lowValues = [float(row[15]),float(row[13])]

        try: indenterDepth = ((highValues[0]-lowValues[0])/(highValues[1]-lowValues[1])) * (self.inputEnergy-lowValues[1]) + lowValues[0]
        except: raise ValueError('The pre_upg_RF_Work.csv needs to have values at greater depth; redo pre-analysis with greater depth.')

        print('Predicted Indenter Depth: %s um' %(indenterDepth))

        return(indenterDepth)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

class ASym_Analysis(General_Analysis):

    #-----------------------------------------------------------------------

    def __init__(self,*args,**kwargs):

        return(None)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createInteractions(self,*args,**kwargs):

        self.indenterType = args[0]
        self.indenterMass = args[1]
        self.contactFriction = args[2]
        self.contactType = args[3]

        from caeModules import interaction

        if self.indenterType == 'Rigid':

            a = self.mdb.models['Model-1'].rootAssembly
            region2=a.instances['Indenter-1'].surfaces['Contact_Master_Surf']
            a = self.mdb.models['Model-1'].rootAssembly
            region1=a.sets['mSet-1']
            self.mdb.models['Model-1'].RigidBody(name='Analytic_Rigid', refPointRegion=region1, surfaceRegion=region2)

            a = self.mdb.models['Model-1'].rootAssembly
            region=a.sets['mSet-1']
            self.mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(name='Indenter_Point_Mass', region=region, mass=self.indenterMass, alpha=0.0, composite=0.0)

        elif self.indenterType == 'Deformable':

            a = self.mdb.models['Model-1'].rootAssembly
            region1=a.sets['mSet-1']
            region2=a.instances['Indenter-1'].sets['Top_Set']
            self.mdb.models['Model-1'].Coupling(name='Indenter_Coupling', controlPoint=region1,
                surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
                localCsys=None, u1=ON, u2=ON, ur3=ON)

        else: print('Indenter type selected is not valid.')

        self.mdb.models['Model-1'].ContactProperty('FrictionCoeff_' + ('%0.2f'%self.contactFriction).replace('.','-'))
        self.mdb.models['Model-1'].interactionProperties['FrictionCoeff_' + ('%0.2f'%self.contactFriction).replace('.','-')].NormalBehavior(pressureOverclosure=HARD, allowSeparation=ON, constraintEnforcementMethod=DEFAULT)
        self.mdb.models['Model-1'].interactionProperties['FrictionCoeff_' + ('%0.2f'%self.contactFriction).replace('.','-')].TangentialBehavior(formulation=FRICTIONLESS)

        self.mdb.models['Model-1'].interactionProperties['FrictionCoeff_' + ('%0.2f'%self.contactFriction).replace('.','-')].TangentialBehavior(
            formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, pressureDependency=OFF, temperatureDependency=OFF, dependencies=0,
            table=((self.contactFriction, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, fraction=0.005, elasticSlipStiffness=None)

        if self.analysisType.startswith('Standard'):

            if self.contactType == 'Surface':

                a = self.mdb.models['Model-1'].rootAssembly
                region1=a.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                region2=a.instances['Test_Article-1'].surfaces['Slave_Contact_Surf']
                self.mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='Surface_Contact',
                    createStepName='Initial', master=region1, slave=region2, sliding=FINITE,
                    thickness=ON, contactTracking=ONE_CONFIG, interactionProperty='FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-'), adjustMethod=NONE,
                    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

            elif self.contactType == 'Node':

                a = self.mdb.models['Model-1'].rootAssembly
                region1=a.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                region2=a.instances['Test_Article-1'].sets['Node_Contact_Set']
                self.mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='Indenter_Node_Contact',
                    createStepName='Initial', master=region1, slave=region2, sliding=FINITE,
                    enforcement=NODE_TO_SURFACE, thickness=OFF,
                    interactionProperty='FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-'), surfaceSmoothing=NONE,
                    adjustMethod=NONE, smooth=0.2, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

            elif self.contactType == 'General':

                self.mdb.models['Model-1'].ContactStd(name='General Contact', createStepName='Initial')
                self.mdb.models['Model-1'].interactions['General Contact'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)
                self.mdb.models['Model-1'].interactions['General Contact'].contactPropertyAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, SELF, 'FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-')), ))
                r12=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].surfaces['Slave_Contact_Surf']
                self.mdb.models['Model-1'].interactions['General Contact'].masterSlaveAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, r12, MASTER), ))

            else: raise ValueError('Contact type chosen is not valid.')

        elif self.analysisType.startswith('Explicit'):

            if self.contactType == 'Surface':

                a = self.mdb.models['Model-1'].rootAssembly
                region1=a.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                a = self.mdb.models['Model-1'].rootAssembly
                region2=a.instances['Test_Article-1'].surfaces['Slave_Contact_Surf']

                self.mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Indenter_Surf_Contact',
                    createStepName='Initial', master = region1, slave = region2, mechanicalConstraint=KINEMATIC, sliding=FINITE,
                    interactionProperty='FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-'), initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
                # self.mdb.models['Model-1'].interactions['Indenter_Surf_Contact'].setValues(mechanicalConstraint=PENALTY)

            elif self.contactType == 'Node':

                a = self.mdb.models['Model-1'].rootAssembly
                region1=a.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                region2=a.instances['Test_Article-1'].sets['Node_Contact_Set']
                self.mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Indenter_Node_Contact', createStepName='Initial', master = region1, slave = region2,
                    mechanicalConstraint=KINEMATIC, sliding=FINITE, interactionProperty='FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-'), initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
                # self.mdb.models['Model-1'].interactions['Indenter_Node_Contact'].setValues(mechanicalConstraint=PENALTY) #Node and Penalty together are the worst for noise

            elif self.contactType == 'General':

                self.mdb.models['Model-1'].ContactExp(name='General Contact', createStepName='Initial')
                self.mdb.models['Model-1'].interactions['General Contact'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)
                self.mdb.models['Model-1'].interactions['General Contact'].contactPropertyAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, SELF, 'FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-')), ))
                r12=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].surfaces['Slave_Contact_Surf']
                self.mdb.models['Model-1'].interactions['General Contact'].masterSlaveAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, r12, MASTER), ))

            else: raise ValueError('Contact type chosen is not valid.')

        else: raise ValueError('Analysis type chosen is not valid.')

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createLoadsBCs(self,*args,**kwargs):

        self.controlType = args[0]

        self.indenterDepth = kwargs.get('indenterDepth',0.0)
        self.indenterForce = kwargs.get('indenterForce',0.0)
        self.indenterVelocity = kwargs.get('indenterVelocity',0.0)
        self.ampFunction = kwargs.get('ampFunction','Tabular')

        from caeModules import load

        a = self.mdb.models['Model-1'].rootAssembly
        region = a.instances['Test_Article-1'].sets['Center-Line_Set']
        self.mdb.models['Model-1'].DisplacementBC(name='TA_Center-Line_BC', createStepName='Initial',
            region=region, u1=SET, u2=UNSET, ur3=UNSET, amplitude=UNSET,
            distributionType=UNIFORM, fieldName='', localCsys=None)

        a = self.mdb.models['Model-1'].rootAssembly
        region = a.instances['Test_Article-1'].sets['Base_Set']
        self.mdb.models['Model-1'].DisplacementBC(name='TA_Bottom_Axial-Fixed_BC',
            createStepName='Initial', region=region, u1=UNSET, u2=SET, ur3=UNSET,
            amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

        if self.indenterType == 'Deformable':

            a = self.mdb.models['Model-1'].rootAssembly
            region = a.instances['Indenter-1'].sets['Center-Line_Set']
            self.mdb.models['Model-1'].DisplacementBC(name='Ind_Center-Line_BC', createStepName='Initial',
                region=region, u1=SET, u2=UNSET, ur3=UNSET, amplitude=UNSET,
                distributionType=UNIFORM, fieldName='', localCsys=None)

        if self.analysisType.startswith('Standard'):

            if self.controlType == 'Force':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=SET, ur3=SET,
                    fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Loading', u2=FREED)
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Unloading', u2=0.0)

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].ConcentratedForce(name='Indenter_Force', createStepName='Loading', region=region, cf2=-self.indenterForce, amplitude='Std-Indent-%s'%(self.ampFunction), distributionType=UNIFORM, field='', localCsys=None)
                self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Unloading', cf2=-self.indenterForce, amplitude='Std-Remove-%s'%(self.ampFunction))

            elif self.controlType == 'Displacement':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=SET, ur3=SET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Loading', u2=-self.indenterDepth, amplitude='Std-Indent-%s'%(self.ampFunction))
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Unloading', u2=-self.indenterDepth, amplitude='Std-Remove-%s'%(self.ampFunction))

            elif self.controlType == 'InitialVelocity':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].VelocityBC(name='Initial_Velocity', createStepName='Loading', region=region, v1=UNSET, v2=-self.indenterVelocity, vr3=UNSET, amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')

            else: pass

        elif self.analysisType.startswith('Explicit'):

            self.ampFunction = 'Smooth'

            if self.controlType == 'Force':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET,fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].ConcentratedForce(name='Indenter_Force', createStepName='Loading', region=region, cf2=-self.indenterForce, amplitude='Exp-Indent-%s'%(self.ampFunction), distributionType=UNIFORM, field='', localCsys=None)
                try:
                    self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Dwell-Loaded', cf2=-self.indenterForce)
                except:
                    pass
                self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Unloading', cf2=-self.indenterForce, amplitude='Exp-Remove-%s'%(self.ampFunction))
                try:
                    self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Dwell-Loaded', cf2=0.0)
                except:
                    pass

            elif self.controlType == 'Displacement':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=SET, ur3=SET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Loading', u2=-self.indenterDepth, amplitude='Exp-Indent-%s'%(self.ampFunction))
                try:
                    self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Dwell-Loaded', u2=0.0)
                except:
                    pass
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Unloading', u2=-self.indenterDepth, amplitude='Exp-Remove-%s'%(self.ampFunction))
                try:
                    self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Dwell-Unloaded', u2=0.0)
                except:
                    pass

            elif self.controlType == 'InitialVelocity':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].VelocityBC(name='Initial_Velocity',
                    createStepName='Loading', region=region, v1=UNSET, v2=-self.indenterVelocity, vr3=UNSET, amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')

            else: pass

        else: pass

        return(0)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

class ASym_Indenter_Analysis(ASym_Analysis):

    #-----------------------------------------------------------------------

    def __init__(self,*args,**kwargs):

        self.taType = args[0]
        self.analysisType = args[1]
        self.jobName = args[2]

        from abaqus import Mdb

        print('\n\n\n')

        self.mdb = Mdb()

        return(None)

    #-----------------------------------------------------------------------

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
        p.Surface(side1Edges=edges, name='Slave_Contact_Surf')
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
        p.SectionAssignment(region=region, sectionName = self.taMatPlast+'_'+self.taMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
        region = p.sets['Mat_Elastic_Set']
        p.SectionAssignment(region=region, sectionName='Elastic_'+self.taMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

        from caeModules import mesh

        if self.analysisType.startswith('Standard'):

            elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=STANDARD)

        elif self.analysisType.startswith('Explicit'):

            elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)

        else: raise ValueError('Analysis type chosen is not valid.')

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

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createIndenter(self,*args,**kwargs):

        import numpy as np

        self.iAng = np.radians(args[0])

        self.iRad = kwargs.get('indRadius',0.0)
        self.iFlat = kwargs.get('indFlat',0.0)
        indMeshMultiples = kwargs.get('indMeshMultiples',[1.0,10.0])

        #Characteristic Indenter Size (hypotenuse of sharp indenter)
        # self.charIndSize = 1.5 * self.articlePart[1]*self.taL
        self.charIndSize = 0.75 * self.articlePart[1]*self.taL

        from caeModules import part, mesh

        #Analytic Rigid Indenter
        if self.indType == 'Rigid':

            if self.iRad == 0.0:

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

            else: raise ValueError('Indenter Dimensions are not valid.')

        #Discrete Deformable Indenter
        elif self.indType == 'Deformable':

            fineMeshSize = indMeshMultiples[0] * self.meshSize
            coarseMeshSize = indMeshMultiples[1] * self.meshSize

            if self.iRad == 0.0:

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

                s = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                side1Edges = s.getSequenceFromMask(mask=('[#2 ]', ), )
                p.Surface(side1Edges=side1Edges, name='Contact_Master_Surf')

                p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                p.seedPart(size=coarseMeshSize, deviationFactor=0.1, minSizeFactor=0.1)

                pickedEdges1 = p.edges.getSequenceFromMask(mask=('[#5 ]', ), )
                p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, minSize=fineMeshSize, maxSize=coarseMeshSize, constraint=FINER)
                pickedEdges = p.edges.getSequenceFromMask(mask=('[#2 ]', ), )
                p.seedEdgeBySize(edges=pickedEdges, size=fineMeshSize, deviationFactor=0.1, constraint=FINER)

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

                    s = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                    side1Edges = s.getSequenceFromMask(mask=('[#e ]', ), )
                    p.Surface(side1Edges=side1Edges, name='Contact_Master_Surf')

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.seedPart(size=coarseMeshSize, deviationFactor=0.1, minSizeFactor=0.1)

                    pickedEdges1 = p.edges.getSequenceFromMask(mask=('[#11 ]', ), )
                    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, minSize=fineMeshSize, maxSize=coarseMeshSize, constraint=FINER)
                    pickedEdges = p.edges.getSequenceFromMask(mask=('[#e ]', ), )
                    p.seedEdgeBySize(edges=pickedEdges, size=fineMeshSize, deviationFactor=0.1, constraint=FINER)

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

                    s = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                    side1Edges = s.getSequenceFromMask(mask=('[#6 ]', ), )
                    p.Surface(side1Edges=side1Edges, name='Contact_Master_Surf')

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.seedPart(size=coarseMeshSize, deviationFactor=0.1, minSizeFactor=0.1)

                    pickedEdges1 = p.edges.getSequenceFromMask(mask=('[#9 ]', ), )
                    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, minSize=fineMeshSize, maxSize=coarseMeshSize, constraint=FINER)
                    pickedEdges = p.edges.getSequenceFromMask(mask=('[#6 ]', ), )
                    p.seedEdgeBySize(edges=pickedEdges, size=fineMeshSize, deviationFactor=0.1, constraint=FINER)

            e = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
            # print e.getBoundingBox()
            edges = e.findAt(((5e-6, e.getBoundingBox()['high'][1], 0.0), ))
            p.Set(edges=edges, name='Top_Set')
            edges = e.findAt(((0.0, 5e-6, 0.0), ))
            xVerts = p.vertices.findAt(((0.0, e.getBoundingBox()['high'][1], 0.0), ))
            p.Set(edges=edges, xVertices=xVerts, name='Center-Line_Set')

            f = self.mdb.models['Model-1'].parts['Deformable_Indenter'].faces
            pickedRegions = f.getSequenceFromMask(mask=('[#1 ]', ), )

            # p.setMeshControls(regions=pickedRegions, elemShape=QUAD)
            p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED)

            if self.analysisType.startswith('Standard'):

                # elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=STANDARD)

            elif self.analysisType.startswith('Explicit'):

                # elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=EXPLICIT)

            faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
            pickedRegions =(faces, )
            p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
            p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
            p.generateMesh()

            # if (self.indMatName is not None) and (not self.indMatName == 'None'):

            p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
            f = p.faces
            faces = f.findAt(((5e-6, 5e-4, 0.0), ))
            region = p.Set(faces=faces, name='Set-1')
            p.SectionAssignment(region=region, sectionName='Elastic_'+self.indMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createAssembly(self,*args,**kwargs):

        self.indenterType = args[0]

        self.indenterOffset = kwargs.get('indenterOffset',0.0)

        from math import cos

        from caeModules import assembly

        a = self.mdb.models['Model-1'].rootAssembly
        a.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, -1.0))
        # a.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, 1.0)) #Points Axial Z Axis "down"

        p = self.mdb.models['Model-1'].parts['Test_Article']
        a.Instance(name='Test_Article-1', part=p, dependent=ON)

        if self.indenterType == 'Rigid':

            p = self.mdb.models['Model-1'].parts['Analytic_Indenter']
            a.Instance(name='Indenter-1', part=p, dependent=ON)
            a = self.mdb.models['Model-1'].rootAssembly
            a.translate(instanceList=('Indenter-1', ), vector=(0.0, self.indenterOffset, 0.0))

        elif self.indenterType == 'Deformable':

            p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
            a.Instance(name='Indenter-1', part=p, dependent=ON)
            a = self.mdb.models['Model-1'].rootAssembly
            a.translate(instanceList=('Indenter-1', ), vector=(0.0, self.indenterOffset, 0.0))

        else: print('Indenter type selected is not valid.')

        if self.indenterType == 'Rigid':

            rp1Coord = (0.0,self.charIndSize*cos(self.iAng) + self.indenterOffset)

        elif self.indenterType == 'Deformable':

            tempYcoord = []

            for node in a.instances['Indenter-1'].nodes: tempYcoord.append(node.coordinates[1])

            rp1Coord = (0.0,max(tempYcoord))

        a = self.mdb.models['Model-1'].rootAssembly
        a.ReferencePoint(point=(rp1Coord[0], rp1Coord[1], 0.0))
        refPoints1=(self.mdb.models['Model-1'].rootAssembly.referencePoints[6], )
        a.Set(referencePoints=refPoints1, name='mSet-1')

        return(0)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

class General_Output(object):

    #-----------------------------------------------------------------------

    def __init__(self):

        return(None)

    #-----------------------------------------------------------------------

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

        import csv

        csvName = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'WholeModelHistory' + '.csv')

        tempFile = open(csvName, 'wb')

        with open(csvName, 'wb') as tempFile:

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

                    # print tempRow

                    csvWriter.writerow(tempRow)

        print('Writing CSV File: %s\n\n\n' %(csvName))

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def ContactForceVector(self,*args,**kwargs):

        writeCSV = kwargs.get('writeCSV', True)

        from numpy import arctan,degrees

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

            # print totalContactForceVector

        for i in range(len(sortedCSHEARF)):

            totalContactForceVector[0] = totalContactForceVector[0] + sortedCSHEARF[i][3]

            totalContactForceVector[1] = totalContactForceVector[1] + sortedCSHEARF[i][4]

            # print totalContactForceVector

        for i in range(len(totalContactForceVector)):

            totalContactForceVector[2] = arctan(totalContactForceVector[0]/totalContactForceVector[1])

            totalContactForceVector[3] = degrees(totalContactForceVector[2])

            totalContactForceVector[4] = arctan(totalContactForceVector[1]/totalContactForceVector[0])

            totalContactForceVector[5] = degrees(totalContactForceVector[4])

        if writeCSV:

            import csv

            titleRow = ['CFORCE1','CFORCE2','ANGLEvert(rad)','ANGLEvert(deg)','ANGLEhoriz(rad)','ANGLEhoriz(deg)','contactRadius']

            csvName = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'CFORCE' + '.csv')

            print('Writing CSV File: %s\n\n\n' %(csvName))

            tempFile = open(csvName, 'wb')

            with open(csvName, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                csvWriter.writerow([totalContactForceVector[0],totalContactForceVector[1],totalContactForceVector[2],totalContactForceVector[3],totalContactForceVector[4],totalContactForceVector[5],contactRadius])

        return(totalContactForceVector)

    #-----------------------------------------------------------------------

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

        # print self.odb.steps[stepName].frames[frameNumber].fieldOutputs.keys()

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

            from numpy import zeros

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
                else: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + [resultSet.name] + list(resultPE.componentLabels)

            else:

                if resultSet.componentLabels: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + list(resultSet.componentLabels)
                else: titleRow = ['elementLabel'] + list(coordSet.componentLabels) + [resultSet.name]

            #print resultSet.values[0]

            coordSetNodes = []

            for i in range(len(coordSet.values)):

                coordSetNodes.append(coordSet.values[i].nodeLabel)

            #print coordSetNodes

            unsortedResults = []

            for i in range(len(elementSet.elements)):

                tempNodeCount = 0

                tempCoordSum = zeros(len(coordSet.values[0].data))

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
                            except AttributeError: unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + [resultSet.values[m].data] + resultPE.values[m].data.tolist() )

                        else:

                            try: unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + resultSet.values[m].data.tolist())
                            except AttributeError: unsortedResults.append([elementSet.elements[i].label] + tempCoordSum.tolist() + [resultSet.values[m].data])

        if sortedResults: finalResults = sorted(unsortedResults, key=lambda unsortedResults: unsortedResults[abs(sortDirection)], reverse=reverse)
        else: finalResults = unsortedResults

        #for i in range(len(finalResults)): print finalResults[i]

        if writeCSV:

            import csv

            if resultName.startswith('CNORMF'): resultName = 'CNORMF'
            if resultName.startswith('CSHEARF'): resultName = 'CSHEARF'

            csvName = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + resultName + '_' + stepName + '_' + instanceName + '-' + setName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(csvName))

            tempFile = open(csvName, 'wb')

            with open(csvName, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                for i in range(len(finalResults)):

                    csvWriter.writerow(finalResults[i])

        return(finalResults)

    #-----------------------------------------------------------------------

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

        # print self.odb.steps[stepName].frames[frameNumber].fieldOutputs.keys()

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

            from numpy import zeros

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

        #for i in range(len(finalResults)): print finalResults[i]

        if writeCSV:

            import csv

            if resultName.startswith('CNORMF'): resultName = 'CNORMF'
            if resultName.startswith('CSHEARF'): resultName = 'CSHEARF'

            csvName = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + resultName + '_' + stepName + '_' + instanceName + '-' + setName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(csvName))

            tempFile = open(csvName, 'wb')

            with open(csvName, 'wb') as tempFile:

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

        from os import chdir

        from odbAccess import openOdb, OdbError

        from subprocess import call

        odbName = odbPath.split('/')[-1].split('\\')[-1]
        print("Opening ODB: %s \n\n\n" %(odbName))
        chdir(odbPath.rstrip(odbName))

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

                    call("abaqus -upgrade -job %s -odb %s" %(str(odbName)[:-4]+'_upg',str(odbName)[:-4]), shell=True)

                    odbName = str(odbName)[:-4]+'_upg.odb'

                    self.odb = openOdb(odbName, readOnly=readOnly)

                except OdbError:

                    print('Error: Could not open ODB file - (%s)' %(odbPath))
                    exit()

        # print self.odb

        return(None)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def WorkForceDist(self,*args,**kwargs):

        instanceNameRF = kwargs.get('instanceNameRF', None)
        nodeSetNameRF = kwargs.get('nodeSetNameRF', None)

        instanceNameU = kwargs.get('instanceNameU', None)
        nodeSetNameU = kwargs.get('nodeSetNameU', None)

        fileNameSuffix = kwargs.get('fileNameSuffix', '')

        print('Running Work-Force-Distance Routine:\n')

        from numpy import degrees, arctan

        import csv

        if instanceNameRF and nodeSetNameRF: nodeSetRF = self.odb.rootAssembly.instances[instanceNameRF].nodeSets[nodeSetNameRF]
        elif nodeSetNameRF: nodeSetRF = self.odb.rootAssembly.nodeSets[nodeSetNameRF]
        else: print('Error: No Reaction Force Node Set Selected.')

        if instanceNameU and nodeSetNameU: nodeSetU = self.odb.rootAssembly.instances[instanceNameU].nodeSets[nodeSetNameU]
        elif nodeSetNameU: nodeSetU = self.odb.rootAssembly.nodeSets[nodeSetNameU]
        else: print('Error: No Distance Node Set Selected.')

        headerRow = ['Step', 'Frame', 'Step Time', 'RF1', 'RF2', 'RF-Angle', 'U1', 'U2', 'frameWork1', 'frameWork2', 'totalWork1', 'totalWork2','RF2Calc(mN)=ALLIE/Disp(mN)', 'ALLIE', 'ALLWK','','negU2(um)','RF2(mN)','K(mN/um)','Ewk(nJ)','','negU2(nm)','RF2(uN)','K(uN/nm)','Ewk(pJ)']
        csvName = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'RF_Work' + fileNameSuffix + '.csv')

        tempFile = open(csvName, 'wb')

        with open(csvName, 'wb') as tempFile:

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

                    try: Angle12 = degrees(arctan(totalRF2/totalRF1))

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

        print('Writing CSV File: %s\n\n\n' %(csvName))

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def VolumeDispCyl(self,*args,**kwargs):

        '''Indent Volume Displacements: This function doesn't work that great, because it depends on where it "stops" counting at the edge of the plastic zone'''

        sortedNodeSet = self.GeneralResults(sortedResults=True,sortDirection=1,stepName='Unloading',instanceName='TEST_ARTICLE-1',setName='RESULTS_SURF_SET', resultName='COORD', writeCSV=False)

        xLimit = kwargs.get('xLimit', None)
        writeCSV = kwargs.get('writeCSV', True)

        import csv

        from numpy import pi

        volNegSum = 0.0

        volPosSum = 0.0

        volTotSum = 0.0

        for i in range(len(sortedNodeSet)-1):

            # print sortedNodeSet[i][2]

            # #The top equation should be "half" the value

            # volInc = ((sortedNodeSet[i][2]+sortedNodeSet[i+1][2])/2.0) * (sortedNodeSet[i+1][1]-sortedNodeSet[i][1])   *    pi * ((sortedNodeSet[i][1]+sortedNodeSet[i+1][1])/2.0)

            volInc = 0.5 * (sortedNodeSet[i][2]+sortedNodeSet[i+1][2]) * (sortedNodeSet[i+1][1]-sortedNodeSet[i][1])   *    pi * (sortedNodeSet[i][1]+sortedNodeSet[i+1][1])

            # print volInc

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

            csvName = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'iVol' + '.csv')

            print('Writing CSV File: %s\n\n\n' %(csvName))

            tempFile = open(csvName, 'wb')

            with open(csvName, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow + ['Calculations Stopped at x=%s'%(sortedNodeSet[i][1])])

                csvWriter.writerow([volNegSum,volPosSum,volTotSum])

                # csvWriter.writerow(['Calculations Stopped at x=%s'%(sortedNodeSet[i][1])])

        return([volNegSum,volPosSum,volTotSum])

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def NormalizerVariables(self,*args,**kwargs):

        '''This function is currently in work. It is intended to get numerous "normalizer" values and put them in a csv'''

        #-----------------------------------------------------------------------

        writeCSV = kwargs.get('writeCSV', True)

        #-----------------------------------------------------------------------

        import csv

        from numpy import pi

        normalVars = {}

        #-----------------------------------------------------------------------

        normalVars['maxRF2_Total'] = self.maxRF2

        #-----------------------------------------------------------------------
        sortedElementSet = self.GeneralResults(sortedResults=True,sortDirection=-1,stepName='Loading',instanceName='TEST_ARTICLE-1',setName='RESULTS_SURF_SET', resultName='PE', writeCSV=False)

        # for value in sortedElementSet: print value

        for value in sortedElementSet:

            if abs(max(value[3:6])) > 1e-4:
            # if value[3] > 1e-4:

                normalVars['plasticEdge_IndentX'] = value[1]

                break

        if ('plasticEdge_IndentX' not in dict(normalVars)): normalVars['plasticEdge_IndentX'] = None

        print('Indent X-dir; Plastic Edge Location: %s\n' %(normalVars['plasticEdge_IndentX']))
        #-----------------------------------------------------------------------
        sortedElementSet = self.GeneralResults(sortedResults=True,sortDirection=2,stepName='Loading',instanceName='TEST_ARTICLE-1',setName='RESULTS_CL_SET', resultName='PE', writeCSV=False)

        # for value in sortedElementSet: print value

        for value in sortedElementSet:

            if abs(max(value[3:6])) > 1e-4:
            # if value[3] > 1e-4:

                normalVars['plasticEdge_IndentY'] = value[2]

                break

        if ('plasticEdge_IndentY' not in dict(normalVars)): normalVars['plasticEdge_IndentY'] = None

        print('Indent Y-dir; Plastic Edge Location: %s\n' %(normalVars['plasticEdge_IndentY']))
        #-----------------------------------------------------------------------
        sortedElementSet = self.GeneralResults(sortedResults=True,sortDirection=-1,stepName='Unloading',instanceName='TEST_ARTICLE-1',setName='RESULTS_SURF_SET', resultName='PE', writeCSV=False)

        # for value in sortedElementSet: print value

        for value in sortedElementSet:

            if abs(max(value[3:6])) > 1e-4:
            # if value[3] > 1e-4::

                normalVars['plasticEdge_RemoveX'] = value[1]

                break

        if ('plasticEdge_RemoveX' not in dict(normalVars)): normalVars['plasticEdge_RemoveX'] = None

        print('Remove X-dir; Plastic Edge Location: %s\n' %(normalVars['plasticEdge_RemoveX']))
        #-----------------------------------------------------------------------
        sortedElementSet = self.GeneralResults(sortedResults=True,sortDirection=2,stepName='Unloading',instanceName='TEST_ARTICLE-1',setName='RESULTS_CL_SET', resultName='PE', writeCSV=False)

        # for value in sortedElementSet: print value

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

        # for value in sortedElementSet: print value

        normalVars['indentDepth_IndentY'] = sortedElementSet[-1][-1]
        #-----------------------------------------------------------------------
        sortedElementSet = self.GeneralResults(sortedResults=True,sortDirection=2,stepName='Unloading',instanceName='TEST_ARTICLE-1',setName='RESULTS_CL_SET', resultName='COORD', writeCSV=False)

        # for value in sortedElementSet: print value

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
        sortedCoordSet = self.GeneralResults(sortedResults=True,sortDirection=2,stepName='Unloading',instanceName='TEST_ARTICLE-1',setName='RESULTS_SURF_SET', resultName='COORD', writeCSV=False)

        for value in sortedCoordSet:

            if value[0] == tempNode:

                normalVars['contactEdge_RemoveX'] = value[1]

                break

        print('Remove X-dir; Contact Edge Location: %s\n' %(normalVars['contactEdge_RemoveX']))
        #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        try: normalVars['plasticZoneHeight_IndentY'] = normalVars['plasticEdge_IndentY'] - normalVars['indentDepth_IndentY']
        except: normalVars['plasticZoneHeight_IndentY'] = None
        try: normalVars['plasticZoneHeight_RemoveY'] = normalVars['plasticEdge_RemoveY'] - normalVars['indentDepth_RemoveY']
        except: normalVars['plasticZoneHeight_RemoveY'] = None
        #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        for key in normalVars.keys(): print('Key: %s  Value: %s\n' %(key,normalVars[key]))

        if writeCSV:

            import csv

            csvName = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'normVars' + '.csv')

            print('Writing CSV File: %s\n\n\n' %(csvName))

            tempFile = open(csvName, 'wb')

            with open(csvName, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                for key in normalVars.keys():

                    csvWriter.writerow([key,normalVars[key]])

        return(normalVars)

    #-----------------------------------------------------------------------

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

        # print self.odb.steps[stepName].frames[frameNumber].fieldOutputs.keys()

        try: self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].nodeLabel
        except: return(1)

        if self.odb.steps[stepName].frames[frameNumber].fieldOutputs[resultName].values[0].elementLabel:

            from numpy import zeros

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

            #print coordSetNodes

            unsortedResults = []

            for i in range(len(elementSet.elements)):

                tempNodeCount = 0

                tempCoordSum = zeros(len(coordSet.values[0].data))

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

        #for i in range(len(finalResults)): print finalResults[i]

        if writeCSV:

            import csv

            if resultName.startswith('CNORMF'): resultName = 'CNORMF'
            if resultName.startswith('CSHEARF'): resultName = 'CSHEARF'

            csvName = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + resultName + '_Invariants_' + stepName + '_' + instanceName + '-' + setName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(csvName))

            tempFile = open(csvName, 'wb')

            with open(csvName, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                for i in range(len(finalResults)):

                    csvWriter.writerow(finalResults[i])

        return(finalResults)

    #-----------------------------------------------------------------------

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

        import csv

        frameId = self.odb.steps[stepName].frames[frameNumber].frameId

        #-----------------------------------------------------------------------

        from numpy import zeros

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

        import numpy as np

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

        #for i in range(len(finalResults)): print finalResults[i]

        if writeCSV:

            csvName = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + 'Invariants' + '_' + stepName + '_' + instanceName + '-' + setName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(csvName))

            tempFile = open(csvName, 'wb')

            with open(csvName, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                for i in range(len(finalResults)):

                    csvWriter.writerow(finalResults[i])

        return(finalResults)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def UnsortedPlasticZone(self,*args,**kwargs):

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

        from numpy import zeros

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

        # for result in customResults: print result

        #-----------------------------------------------------------------------

        coordSetNodes = []

        for i in range(len(coordSet.values)):

            coordSetNodes.append(coordSet.values[i].nodeLabel)

        # print coordSetNodes

        #-----------------------------------------------------------------------

        unsortedResults = []

        for i in range(len(customResults)):

            tempNodeCount = 0

            tempCoordSum = zeros(len(coordSet.values[0].data))

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

            import csv

            csvName = self.odb.path.split('\\')[-1].split('/')[-1].replace('.odb', '_' + resultName + '_' + 'PlasticZone' + '_' + ('%1.0E'%(limitPE)).rstrip('0').rstrip('.') + '_' + stepName + '.csv')

            print('Writing CSV File: %s\n\n\n' %(csvName))

            titleRow = list(coordSet.componentLabels) + ['Element Label','Element Connectivity'] + ['ElementLabel'] + list(resultSet.componentLabels) + list(resultPE.componentLabels)

            tempFile = open(csvName, 'wb')

            with open(csvName, 'wb') as tempFile:

                csvWriter = csv.writer(tempFile)

                csvWriter.writerow(titleRow)

                for i in range(len(unsortedResults)):

                    csvWriter.writerow(unsortedResults[i])

        return(unsortedResults)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

# End of Plugin: Extra Modules Next

#--------------------------------------------------------------------------------------------------

class Sym_Analysis(General_Analysis):

    #-----------------------------------------------------------------------

    def __init__(self,*args,**kwargs):

        return(None)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createInteractions(self,*args,**kwargs):

        self.indenterType = args[0]
        self.indenterMass = args[1]
        self.contactFriction = args[2]
        self.contactType = args[3]

        from caeModules import interaction

        if self.indenterType == 'Rigid':

            # print self.mdb.models['Model-1'].parts['Rigid_Indenter'].type

            if self.mdb.models['Model-1'].parts['Rigid_Indenter'].type == DISCRETE_RIGID_SURFACE:

                a = self.mdb.models['Model-1'].rootAssembly
                region2=a.instances['Indenter-1'].sets['Set-1']
                region1=a.sets['mSet-1']
                self.mdb.models['Model-1'].RigidBody(name='Discrete_Rigid', refPointRegion=region1, bodyRegion=region2)

                a = self.mdb.models['Model-1'].rootAssembly
                region=a.sets['mSet-1']
                self.mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(name='Indenter_Point_Mass', region=region, mass=self.indenterMass, alpha=0.0, composite=0.0)

            else:

                a = self.mdb.models['Model-1'].rootAssembly
                region2=a.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                a = self.mdb.models['Model-1'].rootAssembly
                region1=a.sets['mSet-1']
                self.mdb.models['Model-1'].RigidBody(name='Analytic_Rigid', refPointRegion=region1, surfaceRegion=region2)

                a = self.mdb.models['Model-1'].rootAssembly
                region=a.sets['mSet-1']
                self.mdb.models['Model-1'].rootAssembly.engineeringFeatures.PointMassInertia(name='Indenter_Point_Mass', region=region, mass=self.indenterMass, alpha=0.0, composite=0.0)

        elif self.indenterType == 'Deformable':

            a = self.mdb.models['Model-1'].rootAssembly
            region1=a.sets['mSet-1']
            region2=a.instances['Indenter-1'].sets['Top_Set']
            self.mdb.models['Model-1'].Coupling(name='Indenter_Coupling', controlPoint=region1,
                surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
                localCsys=None, u1=ON, u2=ON, ur3=ON)

        else: print('Indenter type selected is not valid.')

        self.mdb.models['Model-1'].ContactProperty('FrictionCoeff_' + ('%0.2f'%self.contactFriction).replace('.','-'))
        self.mdb.models['Model-1'].interactionProperties['FrictionCoeff_' + ('%0.2f'%self.contactFriction).replace('.','-')].NormalBehavior(pressureOverclosure=HARD, allowSeparation=ON, constraintEnforcementMethod=DEFAULT)
        self.mdb.models['Model-1'].interactionProperties['FrictionCoeff_' + ('%0.2f'%self.contactFriction).replace('.','-')].TangentialBehavior(formulation=FRICTIONLESS)

        self.mdb.models['Model-1'].interactionProperties['FrictionCoeff_' + ('%0.2f'%self.contactFriction).replace('.','-')].TangentialBehavior(
            formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, pressureDependency=OFF, temperatureDependency=OFF, dependencies=0,
            table=((self.contactFriction, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, fraction=0.005, elasticSlipStiffness=None)

        if self.analysisType.startswith('Standard'):

            if self.contactType == 'Surface':

                a = self.mdb.models['Model-1'].rootAssembly
                region1=a.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                region2=a.instances['Test_Article-1'].surfaces['Slave_Contact_Surf']
                self.mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='Surface_Contact',
                    createStepName='Initial', master=region1, slave=region2, sliding=FINITE,
                    thickness=ON, contactTracking=ONE_CONFIG, interactionProperty='FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-'), adjustMethod=NONE,
                    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

            elif self.contactType == 'Node':

                a = self.mdb.models['Model-1'].rootAssembly
                region1=a.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                region2=a.instances['Test_Article-1'].sets['Node_Contact_Set']
                self.mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='Indenter_Node_Contact',
                    createStepName='Initial', master=region1, slave=region2, sliding=FINITE,
                    enforcement=NODE_TO_SURFACE, thickness=OFF,
                    interactionProperty='FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-'), surfaceSmoothing=NONE,
                    adjustMethod=NONE, smooth=0.2, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

            elif self.contactType == 'General':

                self.mdb.models['Model-1'].ContactStd(name='General Contact', createStepName='Initial')
                self.mdb.models['Model-1'].interactions['General Contact'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)
                self.mdb.models['Model-1'].interactions['General Contact'].contactPropertyAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, SELF, 'FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-')), ))
                r12=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].surfaces['Slave_Contact_Surf']
                self.mdb.models['Model-1'].interactions['General Contact'].masterSlaveAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, r12, MASTER), ))

            else: raise ValueError('Contact type chosen is not valid.')

        elif self.analysisType.startswith('Explicit'):

            if self.contactType == 'Surface':

                a = self.mdb.models['Model-1'].rootAssembly
                region1=a.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                a = self.mdb.models['Model-1'].rootAssembly
                region2=a.instances['Test_Article-1'].surfaces['Slave_Contact_Surf']

                self.mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Indenter_Surf_Contact',
                    createStepName='Initial', master = region1, slave = region2, mechanicalConstraint=KINEMATIC, sliding=FINITE,
                    interactionProperty='FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-'), initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
                # self.mdb.models['Model-1'].interactions['Indenter_Surf_Contact'].setValues(mechanicalConstraint=PENALTY)

            elif self.contactType == 'Node':

                a = self.mdb.models['Model-1'].rootAssembly
                region1=a.instances['Indenter-1'].surfaces['Contact_Master_Surf']
                region2=a.instances['Test_Article-1'].sets['Node_Contact_Set']
                self.mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Indenter_Node_Contact', createStepName='Initial', master = region1, slave = region2,
                    mechanicalConstraint=KINEMATIC, sliding=FINITE, interactionProperty='FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-'), initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
                # self.mdb.models['Model-1'].interactions['Indenter_Node_Contact'].setValues(mechanicalConstraint=PENALTY) #Node and Penalty together are the worst for noise

            elif self.contactType == 'General':

                self.mdb.models['Model-1'].ContactExp(name='General Contact', createStepName='Initial')
                self.mdb.models['Model-1'].interactions['General Contact'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)
                self.mdb.models['Model-1'].interactions['General Contact'].contactPropertyAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, SELF, 'FrictionCoeff_'+('%0.2f'%self.contactFriction).replace('.','-')), ))
                r12=self.mdb.models['Model-1'].rootAssembly.instances['Test_Article-1'].surfaces['Slave_Contact_Surf']
                self.mdb.models['Model-1'].interactions['General Contact'].masterSlaveAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, r12, MASTER), ))

            else: raise ValueError('Contact type chosen is not valid.')

        else: raise ValueError('Analysis type chosen is not valid.')

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createLoadsBCs(self,*args,**kwargs):

        self.controlType = args[0]

        self.indenterDepth = kwargs.get('indenterDepth',0.0)
        self.indenterForce = kwargs.get('indenterForce',0.0)
        self.indenterVelocity = kwargs.get('indenterVelocity',0.0)
        self.ampFunction = kwargs.get('ampFunction','Tabular')

        from caeModules import load

        a = self.mdb.models['Model-1'].rootAssembly
        region = a.instances['Test_Article-1'].sets['xSim_Set']
        self.mdb.models['Model-1'].XsymmBC(name='TA_xSym_BC', createStepName='Initial', region=region, localCsys=None)

        try:
            region = a.instances['Test_Article-1'].sets['zSim_Set']
            self.mdb.models['Model-1'].ZsymmBC(name='TA_zSym_BC', createStepName='Initial', region=region, localCsys=None)
        except:
            pass

        try:
            region = a.instances['Test_Article-1'].sets['Center-Line_Set']
            self.mdb.models['Model-1'].DisplacementBC(name='TA_Center-Line_BC',
                createStepName='Initial', region=region, u1=SET, u2=UNSET, u3=SET, ur1=SET,
                ur2=SET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                localCsys=None)
        except:
            pass

        region = a.instances['Test_Article-1'].sets['Base_Set']
        self.mdb.models['Model-1'].DisplacementBC(name='TA_Bottom_Axial-Fixed_BC',
            createStepName='Initial', region=region, u1=UNSET, u2=SET, ur3=UNSET,
            amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

        if self.indenterType == 'Deformable':

            pass

            # a = self.mdb.models['Model-1'].rootAssembly
            # region = a.instances['Indenter-1'].sets['Center-Line_Set']
            # self.mdb.models['Model-1'].DisplacementBC(name='Ind_Center-Line_BC', createStepName='Initial',
                # region=region, u1=SET, u2=UNSET, ur3=UNSET, amplitude=UNSET,
                # distributionType=UNIFORM, fieldName='', localCsys=None)

        if self.analysisType.startswith('Standard'):

            if self.controlType == 'Force':

                pass

                # region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                # self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=SET, ur3=SET,
                    # fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
                # self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Loading', u2=FREED)
                # self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Unloading', u2=0.0)

                # region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                # self.mdb.models['Model-1'].ConcentratedForce(name='Indenter_Force', createStepName='Loading', region=region, cf2=-self.indenterForce, amplitude='Std-Indent-%s'%(self.ampFunction), distributionType=UNIFORM, field='', localCsys=None)
                # self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Unloading', cf2=-self.indenterForce, amplitude='Std-Remove-%s'%(self.ampFunction))

            elif self.controlType == 'Displacement':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Loading', u2=-self.indenterDepth, amplitude='Std-Indent-%s'%(self.ampFunction))
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Unloading', u2=-self.indenterDepth, amplitude='Std-Remove-%s'%(self.ampFunction))

            elif self.controlType == 'InitialVelocity':

                pass

                # region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                # self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                # region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                # self.mdb.models['Model-1'].VelocityBC(name='Initial_Velocity', createStepName='Loading', region=region, v1=UNSET, v2=-self.indenterVelocity, vr3=UNSET, amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')

            else: pass

        elif self.analysisType.startswith('Explicit'):

            self.ampFunction = 'Smooth'

            if self.controlType == 'Force':

                pass

                # region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                # self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET,fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                # region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                # self.mdb.models['Model-1'].ConcentratedForce(name='Indenter_Force', createStepName='Loading', region=region, cf2=-self.indenterForce, amplitude='Exp-Indent-%s'%(self.ampFunction), distributionType=UNIFORM, field='', localCsys=None)
                # try:
                    # self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Dwell-Loaded', cf2=-self.indenterForce)
                # except:
                    # pass
                # self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Unloading', cf2=-self.indenterForce, amplitude='Exp-Remove-%s'%(self.ampFunction))
                # try:
                    # self.mdb.models['Model-1'].loads['Indenter_Force'].setValuesInStep(stepName='Dwell-Loaded', cf2=0.0)
                # except:
                    # pass

            elif self.controlType == 'Displacement':

                region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Loading', u2=-self.indenterDepth, amplitude='Exp-Indent-%s'%(self.ampFunction))
                try:
                    self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Dwell-Loaded', u2=0.0)
                except:
                    pass
                self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Unloading', u2=-self.indenterDepth, amplitude='Exp-Remove-%s'%(self.ampFunction))
                try:
                    self.mdb.models['Model-1'].boundaryConditions['Indenter-Position_BC'].setValuesInStep(stepName='Dwell-Unloaded', u2=0.0)
                except:
                    pass

            elif self.controlType == 'InitialVelocity':

                pass

                # region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                # self.mdb.models['Model-1'].DisplacementBC(name='Indenter-Position_BC', createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                # region = self.mdb.models['Model-1'].rootAssembly.sets['mSet-1']
                # self.mdb.models['Model-1'].VelocityBC(name='Initial_Velocity',
                    # createStepName='Loading', region=region, v1=UNSET, v2=-self.indenterVelocity, vr3=UNSET, amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')

            else: pass

        else: pass

        return(0)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

class QSym_Indenter_Analysis(Sym_Analysis):

    #-----------------------------------------------------------------------

    def __init__(self,*args,**kwargs):

        self.taType = args[0]
        self.analysisType = args[1]
        self.jobName = args[2]

        from abaqus import Mdb

        print('\n\n\n')

        self.mdb = Mdb()

        return(None)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createQuarterTestArticle(self,*args,**kwargs):

        self.taL = args[0]
        self.taH = args[1]
        self.articlePart = args[2]
        self.meshSize = args[3]
        self.meshMultiples = args[4]
        self.meshAspectRatio = args[5]

        meshAdjustment = 5.0

        meshSize0 = self.meshSize
        meshSize1 = meshSize0 * self.meshMultiples[0] * meshAdjustment
        meshSize2 = meshSize1 * self.meshMultiples[1] / meshAdjustment
        meshSize3 = meshSize2 * self.meshMultiples[2]
        meshSize4 = meshSize3 * self.meshMultiples[3]

        from caeModules import part

        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.rectangle(point1=(0.0, 0.0), point2=(self.taL, -self.taH))
        self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='QSym_Test_Article_Sketch')
        s.unsetPrimaryObject()
        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.sketchOptions.setValues(gridOrigin=(0.0, 0.0))
        s.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['QSym_Test_Article_Sketch'])
        p = self.mdb.models['Model-1'].Part(name='Test_Article', dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.BaseSolidExtrude(sketch=s, depth=self.taL)
        s.unsetPrimaryObject()
        p = self.mdb.models['Model-1'].parts['Test_Article']
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        cells = p.cells.findAt(((0.0,0.0,0.0),))
        p.Set(cells=cells, name='Set-1')
        faces = p.faces.findAt(((5e-6,0.0,5e-6),))
        p.Set(faces=faces, name='Top_Set')
        faces = p.faces.findAt(((5e-6,-self.taH,5e-6),))
        p.Set(faces=faces, name='Base_Set')
        faces = p.faces.findAt(((0.0,-5e-6,5e-6),))
        p.Set(faces=faces, name='xSim_Set')
        faces = p.faces.findAt(((5e-6,-5e-6,0.0),))
        p.Set(faces=faces, name='zSim_Set')
        edges = p.edges.findAt(((0.0,-5e-6,0.0),))
        p.Set(edges=edges, name='Center-Line_Set')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=self.articlePart[1]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=self.articlePart[2]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=self.articlePart[3]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.articlePart[1]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.articlePart[2]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.articlePart[3]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-self.articlePart[1]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-self.articlePart[2]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-self.articlePart[3]*self.taL)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        pickedCells = p.cells.getSequenceFromMask(mask=('[#1 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[14], cells=pickedCells)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        pickedCells = p.cells.getSequenceFromMask(mask=('[#1 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[15], cells=pickedCells)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        pickedCells = p.cells.getSequenceFromMask(mask=('[#2 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[16], cells=pickedCells)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        pickedCells = p.cells.getSequenceFromMask(mask=('[#f ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[11], cells=pickedCells)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        pickedCells = p.cells.getSequenceFromMask(mask=('[#78 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[12], cells=pickedCells)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        pickedCells = p.cells.getSequenceFromMask(mask=('[#78 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[13], cells=pickedCells)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        pickedCells = p.cells.getSequenceFromMask(mask=('[#ffff ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[8], cells=pickedCells)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        pickedCells = p.cells.getSequenceFromMask(mask=('[#7fff8000 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[9], cells=pickedCells)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        pickedCells = p.cells.getSequenceFromMask(mask=('[#7fff8000 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[10], cells=pickedCells)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        side1Faces = p.faces.findAt(((5e-6,0.0,5e-6),))
        p.Surface(side1Faces=side1Faces, name='Slave_Contact_Surf')
        edges = p.edges.findAt(((0.0,-5e-6,0.0),))
        p.Set(edges=edges, name='Results_CL_Set')
        edges = p.edges.findAt(((0.0,0.0,5e-6),))
        p.Set(edges=edges, name='Results_Surf_Set')
        cells = p.cells.findAt(((0.0,0.0,0.0),))
        p.Set(cells=cells, name='Remeshing_Set')
        p.Set(cells=cells, name='Mat_Plastic_Set')
        p.Set(cells=cells, name='Node_Contact_Set')
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#ffffffff #efffffff ]', ), )
        p.Set(cells=cells, name='Mat_Elastic_Set')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        region = p.sets['Mat_Plastic_Set']
        p.SectionAssignment(region=region, sectionName = self.taMatPlast+'_'+self.taMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
        region = p.sets['Mat_Elastic_Set']
        p.SectionAssignment(region=region, sectionName='Elastic_'+self.taMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

        from caeModules import mesh

        #Mesh Seeds for non-biased mesh
        e = self.mdb.models['Model-1'].parts['Test_Article'].edges

        pickedEdges = e.getSequenceFromMask(mask=('[#0:4 #2 #0 #1880000 #740000 #1000 #2c ]', ), )
        p.seedEdgeBySize(edges=pickedEdges, size=meshSize1, deviationFactor=0.1, constraint=FINER)

        pickedEdges = e.getSequenceFromMask(mask=('[#0:2 #280000 #bc065200 #80 #0 #420009 #24030400 #a0310808 #200 ]', ), )
        p.seedEdgeBySize(edges=pickedEdges, size=meshSize2, deviationFactor=0.1, constraint=FINER)

        pickedEdges = e.getSequenceFromMask(mask=('[#8001ffff #390100fc #c00101 #2000003 #8010000 #4c000000 #10010024 #90007011 #138c4083 #400 ]', ), )
        p.seedEdgeBySize(edges=pickedEdges, size=meshSize3, deviationFactor=0.1, constraint=FINER)

        pickedEdges = e.getSequenceFromMask(mask=('[#56a80000 #c4f4ff01 #530150d4 #f008a0 #d7d8e860 #3fff7fb #cc002a80 #20003cc #4c000640 #1d1 ]', ), )
        p.seedEdgeBySize(edges=pickedEdges, size=meshSize4, deviationFactor=0.1, constraint=FINER)

        #Mesh Seeds for biased mesh
        e = self.mdb.models['Model-1'].parts['Test_Article'].edges

        pickedEdges1 = e.getSequenceFromMask(mask=('[#0:6 #2140000 #80000 #2010 #2 ]', ), )
        pickedEdges2 = e.getSequenceFromMask(mask=('[#0:4 #105 #0:2 #800000 #4 ]', ), )
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=meshSize1, maxSize=meshSize2, constraint=FINER)

        pickedEdges1 = e.getSequenceFromMask(mask=('[#0:2 #80000400 #88004 #0 #b0000000 #200002 #48000800', ' #428000 ]', ), )
        pickedEdges2 = e.getSequenceFromMask(mask=('[#0:2 #140200 #40012100 #60208 ]', ), )
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=meshSize2, maxSize=meshSize3, constraint=FINER)

        pickedEdges1 = e.getSequenceFromMask(mask=('[#29560000 #20a0000 #4000022 #8 #0:2 #2000d550 #1008022', ' #120 #800 ]', ), )
        pickedEdges2 = e.getSequenceFromMask(mask=('[#0 #2 #2802a808 #1000450 #20001410 #804 ]', ), )
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=meshSize3, maxSize=meshSize4, constraint=FINER)

        #Mesh Type - Free, Structured, Sweep
        p = self.mdb.models['Model-1'].parts['Test_Article']
        c = p.cells
        pickedRegions = c.getSequenceFromMask(mask=('[#ffffffff:2 ]', ), )
        p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
        pickedRegions = c.getSequenceFromMask(mask=('[#0 #10000000 ]', ), )
        p.setMeshControls(regions=pickedRegions, elemShape=HEX, technique=SWEEP, algorithm=ADVANCING_FRONT)

        if self.analysisType.startswith('Standard'):

            elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
            elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)

        elif self.analysisType.startswith('Explicit'):

            elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT, kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
            elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)

        cells = c.getSequenceFromMask(mask=('[#ffffffff:2 ]', ), )
        pickedRegions =(cells, )
        p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))

        p.generateMesh()

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createQuarterIndenter(self,*args,**kwargs):

        import numpy as np

        self.iAng = np.radians(args[0])

        self.iRad = kwargs.get('indRadius',0.0)
        self.iFlat = kwargs.get('indFlat',0.0)
        indMeshMultiples = kwargs.get('indMeshMultiples',[1.0,10.0])

        #Characteristic Indenter Size (hypotenuse of sharp indenter)
        # self.charIndSize = 1.5 * self.articlePart[1]*self.taL
        self.charIndSize = 1.0 * self.articlePart[2]*self.taL

        from caeModules import part, mesh

        #Analytic Rigid Indenter
        if self.indType == 'Rigid':

            if self.iRad == 0.0:

                print('Creating Sharp Tip Analytic Indenter\n')

                s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
                g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                s.setPrimaryObject(option=STANDALONE)
                s.Line(point1=(-self.charIndSize, 0.0), point2=(self.charIndSize, 0.0))
                p = self.mdb.models['Model-1'].Part(name='Rigid_Indenter', dimensionality=THREE_D, type=ANALYTIC_RIGID_SURFACE)
                p.AnalyticRigidSurfExtrude(sketch=s, depth=2.0*self.charIndSize)
                self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Rigid_Indenter_Sketch')
                s.unsetPrimaryObject()

                p = self.mdb.models['Model-1'].parts['Rigid_Indenter']
                s = p.faces
                side2Faces = s.getSequenceFromMask(mask=('[#1 ]', ), )
                p.Surface(side2Faces=side2Faces, name='Contact_Master_Surf')

            elif self.iRad > 0.0:

                if self.iFlat > 0.0:

                    print('Creating Flat + Radius Tip Analytic Indenter\n')

                    pass

                else:

                    print('Creating Radius Tip Analytic Indenter\n')

                    pass

            else: raise ValueError('Indenter Dimensions are not valid.')

        #Discrete Deformable Indenter
        elif self.indType == 'Deformable':

            fineMeshSize = indMeshMultiples[0] * self.meshSize
            coarseMeshSize = indMeshMultiples[1] * self.meshSize

            if self.iRad == 0.0:

                print('Creating Sharp Tip Deformable Indenter\n')

                pass

            elif self.iRad > 0.0:

                if self.iFlat > 0.0:

                    print('Creating Flat + Radius Tip Deformable Indenter\n')

                    pass

                else:

                    print('Creating Radius Tip Deformable Indenter\n')

                    pass

            pass

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createAssembly(self,*args,**kwargs):

        self.indenterType = args[0]

        self.indenterOffset = kwargs.get('indenterOffset',0.0)

        from math import cos

        from caeModules import assembly

        a = self.mdb.models['Model-1'].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        a.Instance(name='Test_Article-1', part=p, dependent=ON)

        if self.indenterType == 'Rigid':

            p = self.mdb.models['Model-1'].parts['Rigid_Indenter']
            a.Instance(name='Indenter-1', part=p, dependent=ON)
            a = self.mdb.models['Model-1'].rootAssembly
            a.translate(instanceList=('Indenter-1', ), vector=(0.0, self.indenterOffset, 0.0))

            a = self.mdb.models['Model-1'].rootAssembly
            a.rotate(instanceList=('Indenter-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(-1.0, 0.0, 1.0), angle=22.0)

        elif self.indenterType == 'Deformable':

            p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
            a.Instance(name='Indenter-1', part=p, dependent=ON)
            a = self.mdb.models['Model-1'].rootAssembly
            a.translate(instanceList=('Indenter-1', ), vector=(0.0, self.indenterOffset, 0.0))

        else: print('Indenter type selected is not valid.')

        if self.indenterType == 'Rigid':

            rp1Coord = (0.0,self.charIndSize*cos(self.iAng) + self.indenterOffset)

        elif self.indenterType == 'Deformable':

            tempYcoord = []

            for node in a.instances['Indenter-1'].nodes: tempYcoord.append(node.coordinates[1])

            rp1Coord = (0.0,max(tempYcoord))

        a = self.mdb.models['Model-1'].rootAssembly
        a.ReferencePoint(point=(rp1Coord[0], rp1Coord[1], 0.0))
        refPoints1=(self.mdb.models['Model-1'].rootAssembly.referencePoints[6], )
        a.Set(referencePoints=refPoints1, name='mSet-1')

        return(0)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

class HSym_Indenter_Analysis(Sym_Analysis):

    #-----------------------------------------------------------------------

    def __init__(self,*args,**kwargs):

        self.taType = args[0]
        self.analysisType = args[1]
        self.jobName = args[2]

        from abaqus import Mdb

        print('\n\n\n')

        self.mdb = Mdb()

        return(None)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createHalfTestArticle(self,*args,**kwargs):

        self.taL = args[0]
        self.taH = args[1]
        self.articlePart = args[2]
        self.meshSize = args[3]
        self.meshMultiples = args[4]
        self.meshAspectRatio = args[5]

        meshAdjustment = 5.0

        meshSize0 = self.meshSize
        meshSize1 = meshSize0 * self.meshMultiples[0] * meshAdjustment
        meshSize2 = meshSize1 * self.meshMultiples[1] / meshAdjustment
        meshSize3 = meshSize2 * self.meshMultiples[2]
        meshSize4 = meshSize3 * self.meshMultiples[3]

        from caeModules import part

        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.rectangle(point1=(0.0, 0.0), point2=(self.taL, -self.taH))
        self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='QSym_Test_Article_Sketch')
        s.unsetPrimaryObject()
        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.sketchOptions.setValues(gridOrigin=(0.0, 0.0))
        s.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['QSym_Test_Article_Sketch'])
        p = self.mdb.models['Model-1'].Part(name='Test_Article', dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.BaseSolidExtrude(sketch=s, depth=2.0*self.taL)
        s.unsetPrimaryObject()
        p = self.mdb.models['Model-1'].parts['Test_Article']
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        cells = p.cells.findAt(((0.0,0.0,0.0),))
        p.Set(cells=cells, name='Set-1')
        faces = p.faces.findAt(((5e-6,0.0,5e-6),))
        p.Set(faces=faces, name='Top_Set')
        faces = p.faces.findAt(((5e-6,-self.taH,5e-6),))
        p.Set(faces=faces, name='Base_Set')
        faces = p.faces.findAt(((0.0,-5e-6,5e-6),))
        p.Set(faces=faces, name='xSim_Set')
        # edges = p.edges.findAt(((0.0,-5e-6,0.0),))
        # p.Set(edges=edges, name='Center-Line_Set') #commenting removes the constraint on this line

        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.taL+self.articlePart[1]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.taL+self.articlePart[2]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.taL+self.articlePart[3]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.taL-self.articlePart[1]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.taL-self.articlePart[2]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.taL-self.articlePart[3]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=self.articlePart[1]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=self.articlePart[2]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=self.articlePart[3]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-self.articlePart[1]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-self.articlePart[2]*self.taL)
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-self.articlePart[3]*self.taL)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        pickedCells = p.cells.getSequenceFromMask(mask=('[#1 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[6], cells=pickedCells)
        pickedCells = p.cells.getSequenceFromMask(mask=('[#1 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[7], cells=pickedCells)
        pickedCells = p.cells.getSequenceFromMask(mask=('[#2 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[8], cells=pickedCells)
        pickedCells = p.cells.getSequenceFromMask(mask=('[#1 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[9], cells=pickedCells)
        pickedCells = p.cells.getSequenceFromMask(mask=('[#10 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[10], cells=pickedCells)
        pickedCells = p.cells.getSequenceFromMask(mask=('[#1 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[11], cells=pickedCells)
        pickedCells = p.cells.getSequenceFromMask(mask=('[#1 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[12], cells=pickedCells)

        pickedCells = p.cells.getSequenceFromMask(mask=('[#ff ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[13], cells=pickedCells)
        pickedCells = p.cells.getSequenceFromMask(mask=('[#7f80 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[14], cells=pickedCells)
        pickedCells = p.cells.getSequenceFromMask(mask=('[#7f80 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[15], cells=pickedCells)

        pickedCells = p.cells.getSequenceFromMask(mask=('[#ffffffff ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[16], cells=pickedCells)
        pickedCells = p.cells.getSequenceFromMask(mask=('[#7fffffff #80000000 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[17], cells=pickedCells)
        pickedCells = p.cells.getSequenceFromMask(mask=('[#7fffffff #40000000 ]', ), )
        p.PartitionCellByDatumPlane(datumPlane=p.datums[18], cells=pickedCells)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        side1Faces = p.faces.findAt(((5e-6,0.0,self.taL-5e-6),),((5e-6,0.0,self.taL+5e-6),))
        p.Surface(side1Faces=side1Faces, name='Slave_Contact_Surf')
        edges = p.edges.findAt(((0.0,-5e-6,self.taL),))
        p.Set(edges=edges, name='Results_CL_Set')
        edges = p.edges.findAt(((0.0,0.0,self.taL-5e-6),),((0.0,0.0,self.taL+5e-6),))
        p.Set(edges=edges, name='Results_Surf_Set')
        cells = p.cells.findAt(((0.0,0.0,self.taL-5e-6),),((0.0,0.0,self.taL+5e-6),))
        p.Set(cells=cells, name='Remeshing_Set')
        p.Set(cells=cells, name='Mat_Plastic_Set')
        p.Set(cells=cells, name='Node_Contact_Set')
        cells = p.cells.getSequenceFromMask(mask=('[#ffffffff:3 #ff3fffff ]', ), )
        p.Set(cells=cells, name='Mat_Elastic_Set')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        region = p.sets['Mat_Plastic_Set']
        p.SectionAssignment(region=region, sectionName = self.taMatPlast+'_'+self.taMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
        region = p.sets['Mat_Elastic_Set']
        p.SectionAssignment(region=region, sectionName='Elastic_'+self.taMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

        from caeModules import mesh

        #Mesh Seeds for non-biased mesh
        e = self.mdb.models['Model-1'].parts['Test_Article'].edges

        pickedEdges = e.getSequenceFromMask(mask=('[#0:9 #1501400 #0 #6000 #0 #20000000 #1c01e000', ' #83 #20000000 #8000 ]', ), )
        p.seedEdgeBySize(edges=pickedEdges, size=meshSize1, deviationFactor=0.1, constraint=FINER)

        pickedEdges = e.getSequenceFromMask(mask=('[#0:3 #288028 #8800aa2 #20200 #0 #20033880 #c1000008 #2002001 #1813 #8052 #8 #80800010 #40000581 #90000d08', ' #41808 ]', ), )
        p.seedEdgeBySize(edges=pickedEdges, size=meshSize2, deviationFactor=0.1, constraint=FINER)

        pickedEdges = e.getSequenceFromMask(mask=('[#ffffffff #c8000000 #c30013ff #100000c0 #10040000 #10003040 #30013 #40240 #c710094 #40008020 #308300c4 #802a8 #2010044 #26080c4 #460202 #fe060 #10440 ]', ), )
        p.seedEdgeBySize(edges=pickedEdges, size=meshSize3, deviationFactor=0.1, constraint=FINER)

        pickedEdges = e.getSequenceFromMask(mask=('[#0 #156aaad4 #383bc800 #8e422e02 #c2239008 #c9b84829 #7e7cdb8c #1ad8003f #2088ff62 #98020082 #ce7ce500 #b7c00000 #dcfcfe02 #1c167f03 #82b81058 #200014 #c3eae111 #4eef ]', ), )
        p.seedEdgeBySize(edges=pickedEdges, size=meshSize4, deviationFactor=0.1, constraint=FINER)

        # #Mesh Seeds for biased mesh
        # e = self.mdb.models['Model-1'].parts['Test_Article'].edges

        # pickedEdges1 = e.getSequenceFromMask(mask=('[#0:6 #2140000 #80000 #2010 #2 ]', ), )
        # pickedEdges2 = e.getSequenceFromMask(mask=('[#0:4 #105 #0:2 #800000 #4 ]', ), )
        # p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=meshSize1, maxSize=meshSize2, constraint=FINER)

        # pickedEdges1 = e.getSequenceFromMask(mask=('[#0:2 #80000400 #88004 #0 #b0000000 #200002 #48000800', ' #428000 ]', ), )
        # pickedEdges2 = e.getSequenceFromMask(mask=('[#0:2 #140200 #40012100 #60208 ]', ), )
        # p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=meshSize2, maxSize=meshSize3, constraint=FINER)

        # pickedEdges1 = e.getSequenceFromMask(mask=('[#29560000 #20a0000 #4000022 #8 #0:2 #2000d550 #1008022', ' #120 #800 ]', ), )
        # pickedEdges2 = e.getSequenceFromMask(mask=('[#0 #2 #2802a808 #1000450 #20001410 #804 ]', ), )
        # p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=meshSize3, maxSize=meshSize4, constraint=FINER)

        #Mesh Type - Free, Structured, Sweep
        p = self.mdb.models['Model-1'].parts['Test_Article']
        c = p.cells
        pickedRegions = c.getSequenceFromMask(mask=('[#ffffffff:4 ]', ), )
        p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
        pickedRegions = c.getSequenceFromMask(mask=('[#0:3 #c00000 ]', ), )
        p.setMeshControls(regions=pickedRegions, elemShape=HEX, technique=SWEEP, algorithm=ADVANCING_FRONT)

        if self.analysisType.startswith('Standard'):

            elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
            elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)

        elif self.analysisType.startswith('Explicit'):

            elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT, kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
            elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)

        cells = c.getSequenceFromMask(mask=('[#ffffffff:4 ]', ), )
        pickedRegions =(cells, )
        p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))

        p.generateMesh()

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createHalfIndenter(self,*args,**kwargs):

        import numpy as np

        self.iAng = np.radians(args[0])

        self.iRad = kwargs.get('indRadius',0.0)
        self.iFlat = kwargs.get('indFlat',0.0)
        indMeshMultiples = kwargs.get('indMeshMultiples',[1.0,10.0])

        #Characteristic Indenter Size (hypotenuse of sharp indenter)
        # self.charIndSize = 1.5 * self.articlePart[1]*self.taL
        self.charIndSize = 1.0 * self.articlePart[1]*self.taL

        from caeModules import part, mesh

        #Discrete Rigid Indenter
        if self.indType == 'Rigid':

            if self.iRad == 0.0:

                print('Creating Sharp Tip Analytic Indenter\n')

                p = self.mdb.models['Model-1'].parts['Test_Article']
                s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=2.0*self.charIndSize)
                g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                s.setPrimaryObject(option=STANDALONE)
                s.Line(point1=(0.0, 0.0), point2=(0.0, self.charIndSize))
                s.VerticalConstraint(entity=g[2], addUndoState=False)
                s.Line(point1=(0.0, self.charIndSize), point2=(self.charIndSize, self.charIndSize))
                s.HorizontalConstraint(entity=g[3], addUndoState=False)
                s.Line(point1=(self.charIndSize, self.charIndSize), point2=(0.0, 0.0))
                s.FixedConstraint(entity=v[0])
                s.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(0.5*self.charIndSize,1.1*self.charIndSize), value=self.charIndSize)
                s.AngularDimension(line1=g[2], line2=g[4], textPoint=(0.5*self.charIndSize,self.charIndSize), value=68.0)
                p = self.mdb.models['Model-1'].Part(name='Rigid_Indenter', dimensionality=THREE_D, type=DISCRETE_RIGID_SURFACE)
                p.BaseSolidExtrude(sketch=s, depth=2.0*self.charIndSize)
                s.unsetPrimaryObject()
                self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Rigid_Indenter_Sketch')
                s.unsetPrimaryObject()

                p = self.mdb.models['Model-1'].parts['Rigid_Indenter']
                f, e = p.faces, p.edges
                t = p.MakeSketchTransform(sketchPlane=f[1], sketchUpEdge=e[4],
                    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(self.charIndSize/2.0, self.charIndSize/2.475086848, self.charIndSize))
                s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1363.36, gridSpacing=34.08, transform=t)
                g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                # s.setPrimaryObject(option=SUPERIMPOSE)
                # p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
                s.Line(point1=(0.0, -self.charIndSize/2.0), point2=(self.charIndSize, self.charIndSize/2.0))
                s.Line(point1=(self.charIndSize, self.charIndSize/2.0), point2=(self.charIndSize, -self.charIndSize/2.0))
                s.Line(point1=(self.charIndSize, -self.charIndSize/2.0), point2=(0.0, -self.charIndSize/2.0))
                f, e = p.faces, p.edges
                p.CutExtrude(sketchPlane=f[1], sketchUpEdge=e[4], sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=OFF)
                s.unsetPrimaryObject()
                del self.mdb.models['Model-1'].sketches['__profile__']

                p = self.mdb.models['Model-1'].parts['Rigid_Indenter']
                f, e = p.faces, p.edges
                t = p.MakeSketchTransform(sketchPlane=f[3], sketchUpEdge=e[8],
                    sketchPlaneSide=SIDE1, sketchOrientation=LEFT, origin=(self.charIndSize/2.0, self.charIndSize/2.475086848, self.charIndSize))
                s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1363.36, gridSpacing=34.08, transform=t)
                g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
                # s.setPrimaryObject(option=SUPERIMPOSE)
                # p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
                s.Line(point1=(0.0, -self.charIndSize/2.0), point2=(-self.charIndSize, self.charIndSize/2.0))
                s.Line(point1=(-self.charIndSize, self.charIndSize/2.0), point2=(-self.charIndSize, -self.charIndSize/2.0))
                s.Line(point1=(-self.charIndSize, -self.charIndSize/2.0), point2=(0.0, -self.charIndSize/2.0))
                f, e = p.faces, p.edges
                p.CutExtrude(sketchPlane=f[3], sketchUpEdge=e[8], sketchPlaneSide=SIDE1, sketchOrientation=LEFT, sketch=s, flipExtrudeDirection=OFF)
                s.unsetPrimaryObject()
                del self.mdb.models['Model-1'].sketches['__profile__']

                p = self.mdb.models['Model-1'].parts['Rigid_Indenter']
                v1 = p.vertices
                p.DatumPlaneByThreePoints(point1=v1[2], point2=v1[1], point3=v1[0])

                f = self.mdb.models['Model-1'].parts['Rigid_Indenter'].faces
                p.Mirror(mirrorPlane=f[0], keepOriginal=ON)

                c = self.mdb.models['Model-1'].parts['Rigid_Indenter'].cells
                p.RemoveCells(cellList = c[0:1])

                f = self.mdb.models['Model-1'].parts['Rigid_Indenter'].faces
                pickedFaces = f.getSequenceFromMask(mask=('[#f ]', ), )
                d = self.mdb.models['Model-1'].parts['Rigid_Indenter'].datums
                p.PartitionFaceByDatumPlane(datumPlane=d[4], faces=pickedFaces)

                f = self.mdb.models['Model-1'].parts['Rigid_Indenter'].faces
                faces = f.getSequenceFromMask(mask=('[#3f ]', ), )
                p.Set(faces=faces, name='Set-1')

                s = self.mdb.models['Model-1'].parts['Rigid_Indenter'].faces
                side1Faces = s.getSequenceFromMask(mask=('[#24 ]', ), )
                p.Surface(side1Faces=side1Faces, name='Contact_Master_Surf')

                p = self.mdb.models['Model-1'].parts['Rigid_Indenter']
                p.seedPart(size=self.meshMultiples[0]*1.0, deviationFactor=0.1, minSizeFactor=0.1)
                p.generateMesh()

            elif self.iRad > 0.0:

                if self.iFlat > 0.0:

                    print('Creating Flat + Radius Tip Analytic Indenter\n')

                    #might just be a change on the 2-D sketch, with updates after to pick the right surfaces...

                    pass

                else:

                    print('Creating Radius Tip Analytic Indenter\n')

                    pass

            else: raise ValueError('Indenter Dimensions are not valid.')

        #Discrete Deformable Indenter
        elif self.indType == 'Deformable':

            fineMeshSize = indMeshMultiples[0] * self.meshSize
            coarseMeshSize = indMeshMultiples[1] * self.meshSize

            if self.iRad == 0.0:

                print('Creating Sharp Tip Deformable Indenter\n')

                pass

            elif self.iRad > 0.0:

                if self.iFlat > 0.0:

                    print('Creating Flat + Radius Tip Deformable Indenter\n')

                    pass

                else:

                    print('Creating Radius Tip Deformable Indenter\n')

            # e = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
            # # print e.getBoundingBox()
            # edges = e.findAt(((5e-6, e.getBoundingBox()['high'][1], 0.0), ))
            # p.Set(edges=edges, name='Top_Set')
            # edges = e.findAt(((0.0, 5e-6, 0.0), ))
            # xVerts = p.vertices.findAt(((0.0, e.getBoundingBox()['high'][1], 0.0), ))
            # p.Set(edges=edges, xVertices=xVerts, name='Center-Line_Set')

            # f = self.mdb.models['Model-1'].parts['Deformable_Indenter'].faces
            # pickedRegions = f.getSequenceFromMask(mask=('[#1 ]', ), )

            # # p.setMeshControls(regions=pickedRegions, elemShape=QUAD)
            # p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED)

            # if self.analysisType.startswith('Standard'):

                # # elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                # elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                # elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=STANDARD)

            # elif self.analysisType.startswith('Explicit'):

                # # elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                # elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                # elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=EXPLICIT)

            # faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
            # pickedRegions =(faces, )
            # p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
            # p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
            # p.generateMesh()

            # # if (self.indMatName is not None) and (not self.indMatName == 'None'):

            # p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
            # f = p.faces
            # faces = f.findAt(((5e-6, 5e-4, 0.0), ))
            # region = p.Set(faces=faces, name='Set-1')
            # p.SectionAssignment(region=region, sectionName='Elastic_'+self.indMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

        return(0)

    #-----------------------------------------------------------------------

    def createAssembly(self,*args,**kwargs):

        self.indenterType = args[0]

        self.indenterOffset = kwargs.get('indenterOffset',0.0)

        from math import cos

        from caeModules import assembly

        a = self.mdb.models['Model-1'].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        a.Instance(name='Test_Article-1', part=p, dependent=ON)
        a.translate(instanceList=('Test_Article-1', ), vector=(0.0, 0.0, -self.taL))

        if self.indenterType == 'Rigid':

            p = self.mdb.models['Model-1'].parts['Rigid_Indenter']
            a.Instance(name='Indenter-1', part=p, dependent=ON)
            a.translate(instanceList=('Indenter-1', ), vector=(0.0, 0.0, -self.charIndSize))
            a.rotate(instanceList=('Indenter-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 1.0, 0.0), angle=-45.0)

        elif self.indenterType == 'Deformable':

            pass

        else: print('Indenter type selected is not valid.')

        if self.indenterType == 'Rigid':

            a = self.mdb.models['Model-1'].rootAssembly
            v = a.instances['Indenter-1'].vertices
            a.ReferencePoint(point=v[0])
            a = self.mdb.models['Model-1'].rootAssembly
            r = a.referencePoints
            refPoints1=(r[6], )
            a.Set(referencePoints=refPoints1, name='mSet-1')

        # elif self.indenterType == 'Deformable':

            # tempYcoord = []

            # for node in a.instances['Indenter-1'].nodes: tempYcoord.append(node.coordinates[1])

            # rp1Coord = (0.0,max(tempYcoord))

        # a = self.mdb.models['Model-1'].rootAssembly
        # a.ReferencePoint(point=(rp1Coord[0], rp1Coord[1], 0.0))
        # refPoints1=(self.mdb.models['Model-1'].rootAssembly.referencePoints[6], )
        # a.Set(referencePoints=refPoints1, name='mSet-1')

        return(0)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

#Next is "CSym" cylindrical symmetry with specified angle (for wedge elements on center-line)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------

# End of Indentation: Specialty Non-Indentation Modules Next

#--------------------------------------------------------------------------------------------------

class ASym_Pillar_Analysis(ASym_Analysis):

    #-----------------------------------------------------------------------

    def __init__(self,*args,**kwargs):

        self.taType = args[0]
        self.analysisType = args[1]
        self.jobName = args[2]

        from abaqus import Mdb

        print('\n\n\n')

        self.mdb = Mdb()

        return(None)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createPillarTestArticle(self,*args,**kwargs):

        self.meshMultiplier = kwargs.get('meshMultiplier',2.0)

        #Initial Top Diameter (um)
        self.topDiameter = kwargs.get('topDiameter',4.3483)
        #Initial Bump Diameter (um)
        self.bumpDiameter = kwargs.get('bumpDiameter',4.5639)
        #Initial Waist Diameter (um)
        self.waistDiameter = kwargs.get('waistDiameter',3.9383)
        #Initial Foot Diameter (um)
        self.footDiameter = kwargs.get('footDiameter',4.2705)
        #Initial Trench Diameter (um)
        self.trenchDiameter = kwargs.get('trenchDiameter',5.2658)
        #Initial Total Height (um)
        self.totalHeight = kwargs.get('totalHeight',6.2910)
        #Initial Bump Height (um)
        self.bumpHeight = kwargs.get('bumpHeight',5.6976)
        #Initial Waist Height (um)
        self.waistHeight = kwargs.get('waistHeight',0.8021)
        #Estimated Left Trench Depth (um)
        self.leftTrenchDepth = kwargs.get('leftTrenchDepth',0.0508)
        #Estimated Right Trench Depth (um)
        self.rightTrenchDepth = kwargs.get('rightTrenchDepth',0.0602)

        #Average Estimated Trench Depth (um)
        self.averageTrenchDepth = (self.leftTrenchDepth+self.rightTrenchDepth) / 2.0

        from math import tan, radians

        #-----------------------------------------------------------------------

        self.articlePart = (0.0,0.05,0.100,0.200,1.000)
        self.meshMultiples = (10.0, 10.0, 2.0, 2.0)
        self.meshAspectRatio = 1.0

        self.taL = 6.0 * 10.0 * self.waistDiameter
        self.taH = self.taL
        self.meshSize = self.topDiameter / (self.meshMultiplier*100.0)

        meshSize0 = self.meshSize
        meshSize1 = meshSize0 * self.meshMultiples[0]
        meshSize2 = meshSize1 * self.meshMultiples[1]
        meshSize3 = meshSize2 * self.meshMultiples[2]
        meshSize4 = meshSize3 * self.meshMultiples[3]

        from caeModules import part

        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.rectangle(point1=(0.0, 0.0), point2=(self.taL, -self.taH))
        self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Pillar_Test_Article_Sketch')
        s.unsetPrimaryObject()

        #-----------------------------------------------------------------------

        self.terminalHeight = 0.750*self.waistHeight      
        self.terminalPoint = (self.waistDiameter/2.0+(self.waistHeight-self.terminalHeight)*tan(radians(3.0)), self.terminalHeight)

        s.Line(point1=(0.0, 0.0), point2=(0.0, self.totalHeight))
        s.Line(point1=(0.0, self.totalHeight), point2=(self.topDiameter/2.0, self.totalHeight))
        s.Line(point1=(self.topDiameter/2.0, self.totalHeight), point2=(self.bumpDiameter/2.0, self.bumpHeight))
        s.Line(point1=(self.bumpDiameter/2.0, self.bumpHeight), point2=(self.waistDiameter/2.0, self.waistHeight))
        s.Line(point1=(self.waistDiameter/2.0, self.waistHeight), point2=self.terminalPoint)

        # s.Arc3Points(point1=self.terminalPoint, point2=((self.trenchDiameter/2.0), 0.0), point3=(((self.waistDiameter/2.0+self.waistHeight*np.tan(np.radians(3.0)))+(self.trenchDiameter/2.0))/2.0, -self.averageTrenchDepth))
        s.Spline(points=(self.terminalPoint, (((self.waistDiameter/2.0+self.waistHeight*tan(radians(3.0)))+(self.trenchDiameter/2.0))/2.0, -self.averageTrenchDepth), ((self.trenchDiameter/2.0), 0.0)))


        s.autoTrimCurve(curve1=g[5], point1=(self.waistDiameter/2.0, 0.0))
        s.autoTrimCurve(curve1=g[12], point1=((self.trenchDiameter/2.0)-5e-6, 0.0))

        # self.innerTrenchRadius = 0.1
        # self.outerTrenchRadius = 0.1

        # s.FilletByRadius(radius=self.innerTrenchRadius, curve1=g[10], nearPoint1=(self.waistDiameter/2.0+self.waistHeight*np.tan(np.radians(3.0)), 0.0), curve2=g[11], nearPoint2=(((self.waistDiameter/2.0+self.waistHeight*np.tan(np.radians(3.0)))+(self.trenchDiameter/2.0))/2.0, -self.averageTrenchDepth))
        # s.FilletByRadius(radius=self.outerTrenchRadius, curve1=g[11], nearPoint1=(((self.waistDiameter/2.0+self.waistHeight*np.tan(np.radians(3.0)))+(self.trenchDiameter/2.0))/2.0, -self.averageTrenchDepth), curve2=g[13], nearPoint2=((self.trenchDiameter/2.0), 0.0))

        #-----------------------------------------------------------------------

        s1 = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.sketchOptions.setValues(viewStyle=AXISYM)
        s1.ConstructionLine(point1=(0.0, -0.5), point2=(0.0, 0.5))
        s1.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['Pillar_Test_Article_Sketch'])

        p = self.mdb.models['Model-1'].Part(name='Test_Article', dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
        p = self.mdb.models['Model-1'].parts['Test_Article']
        p.BaseShell(sketch=s1)
        s1.unsetPrimaryObject()
        p = self.mdb.models['Model-1'].parts['Test_Article']
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        faces = p.faces.findAt(((0.0,0.0,0.0),))
        p.Set(faces=faces, name='Set-1')
        edges = p.edges.findAt(((0.0,-5e-6,0.0),),((0.0,5e-6,0.0),))
        p.Set(edges=edges, name='Center-Line_Set')
        edges = p.edges.findAt(((5e-6,self.totalHeight,0.0),),((self.bumpDiameter/2.0, self.bumpHeight,0.0),))
        p.Set(edges=edges, name='Top_Set')
        p.Surface(side1Edges=edges, name='Slave_Contact_Surf')
        edges = p.edges.findAt(((5e-6,-self.taH,0.0),))
        p.Set(edges=edges, name='Base_Set')
        edges = p.edges.findAt(((self.taL,-5e-6,0.0),))
        p.Set(edges=edges, name='OD_Set')
        p.Surface(side1Edges=edges, name='OD_Surf')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        f, e, d1 = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.5,gridSpacing=0.01, transform=t)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
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
        edges = p.edges.findAt(((0.0,-5e-6,0.0),),((0.0,5e-6,0.0),))
        p.Set(edges=edges, name='Results_CL_Set')
        edges = p.edges.findAt(((5e-6,self.totalHeight,0.0),),((self.bumpDiameter/2.0, self.bumpHeight,0.0),))
        p.Set(edges=edges, name='Results_Surf_Set')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        faces = p.faces.findAt(((0.0,0.0,0.0),))
        p.Set(faces=faces, name='Mat_Plastic_Set')
        p.Set(faces=faces, name='Node_Contact_Set')
        faces = p.faces.findAt(((self.taL,0.0,0.0),),((0.0,-self.taH,0.0),),((self.taL,-self.taH,0.0),))
        p.Set(faces=faces, name='Mat_Elastic_Set')

        p = self.mdb.models['Model-1'].parts['Test_Article']

        f, e, d = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f.findAt(coordinates=(0.0, 0.0, 0.0), normal=(0.0, 0.0, 1.0)), sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=100.0, gridSpacing=1.0, transform=t)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

        p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        s.Line(point1=(0.0, -self.totalHeight/2.0), point2=(self.articlePart[1]*self.taL, -self.totalHeight/2.0))
        s.Line(point1=(1.5*self.trenchDiameter/2.0, 0.0), point2=(1.5*self.trenchDiameter/2.0, -self.articlePart[1]*self.taH))
        f = p.faces
        pickedFaces = f.findAt(((5e-06, 0.0, 0.0), ))
        e, d = p.edges, p.datums
        p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
        s.unsetPrimaryObject()
        del self.mdb.models['Model-1'].sketches['__profile__']

        p = self.mdb.models['Model-1'].parts['Test_Article']
        f, e, d1 = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.5,gridSpacing=0.01, transform=t)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
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
        p.SectionAssignment(region=region, sectionName = self.taMatPlast+'_'+self.taMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
        region = p.sets['Mat_Elastic_Set']
        p.SectionAssignment(region=region, sectionName='Elastic_'+self.taMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

        p = self.mdb.models['Model-1'].parts['Test_Article']
        faces = p.faces.findAt(((0.0,0.0,0.0),))
        p.Set(faces=faces, name='Remeshing_Set')

        from caeModules import mesh

        if self.analysisType.startswith('Standard'):

            elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=STANDARD)

        elif self.analysisType.startswith('Explicit'):

            elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)

        else: raise ValueError('Analysis type chosen is not valid.')

        p = self.mdb.models['Model-1'].parts['Test_Article']
        faces = p.faces.getSequenceFromMask(mask=('[#ffff ]', ), )
        pickedRegions =(faces, )
        try: p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
        except: p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))

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

        #---New Pillar-Specific Stuff-----------------------------------------------------------------
        p = self.mdb.models['Model-1'].parts['Test_Article']
        e = p.edges
        pickedEdges1 = e.getSequenceFromMask(mask=('[#0 #8024 ]', ), )
        pickedEdges2 = e.getSequenceFromMask(mask=('[#0 #8 ]', ), )
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, end2Edges=pickedEdges2, minSize=meshSize0, maxSize=meshSize1, constraint=FINER)
        pickedEdges = e.getSequenceFromMask(mask=('[#0 #7fd0 ]', ), )
        p.seedEdgeBySize(edges=pickedEdges, size=meshSize0, deviationFactor=0.1, constraint=FINER)

        #Extra Trench Refinement
        p = self.mdb.models['Model-1'].parts['Test_Article']
        e = p.edges
        pickedEdges = e.getSequenceFromMask(mask=('[#0 #f00 ]', ), )
        p.seedEdgeBySize(edges=pickedEdges, size=meshSize0/2.0, deviationFactor=0.1, constraint=FINER)
        pickedEdges2 = e.getSequenceFromMask(mask=('[#0 #1080 ]', ), )
        p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges2, minSize=meshSize0/2.0, maxSize=meshSize0, constraint=FINER)

        #Different Mesh Techniques
        f = self.mdb.models['Model-1'].parts['Test_Article'].faces
        pickedRegions = f.getSequenceFromMask(mask=('[#4000 ]', ), )
        p.setMeshControls(regions=pickedRegions, elemShape=QUAD)
        pickedRegions = f.getSequenceFromMask(mask=('[#2000 ]', ), )
        p.setMeshControls(regions=pickedRegions, allowMapped=False)
        pickedRegions = f.getSequenceFromMask(mask=('[#7037f ]', ), )
        p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED, technique=STRUCTURED)

        p.generateMesh()

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createPillarIndenter(self,*args,**kwargs):

        import numpy as np

        self.iAng = np.radians(kwargs.get('indDemiAngle',0.0))
        self.iRad = kwargs.get('indRadius',self.topDiameter/10.0)
        self.iFlat = kwargs.get('indFlat',self.topDiameter*1.5)
        indMeshMultiples = kwargs.get('indMeshMultiples',[1.0,10.0])

        #Characteristic Indenter Size (hypotenuse of sharp indenter)
        self.charIndSize = 0.75 * self.articlePart[1]*self.taL

        from caeModules import part, mesh

        #Analytic Rigid Indenter
        if self.indType == 'Rigid':

            if self.iRad == 0.0:

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

            else: raise ValueError('Indenter Dimensions are not valid.')

        #Discrete Deformable Indenter
        elif self.indType == 'Deformable':

            fineMeshSize = indMeshMultiples[0] * self.meshSize
            coarseMeshSize = indMeshMultiples[1] * self.meshSize

            if self.iRad == 0.0:

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

                s = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                side1Edges = s.getSequenceFromMask(mask=('[#2 ]', ), )
                p.Surface(side1Edges=side1Edges, name='Contact_Master_Surf')

                p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                p.seedPart(size=coarseMeshSize, deviationFactor=0.1, minSizeFactor=0.1)

                pickedEdges1 = p.edges.getSequenceFromMask(mask=('[#5 ]', ), )
                p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, minSize=fineMeshSize, maxSize=coarseMeshSize, constraint=FINER)
                pickedEdges = p.edges.getSequenceFromMask(mask=('[#2 ]', ), )
                p.seedEdgeBySize(edges=pickedEdges, size=fineMeshSize, deviationFactor=0.1, constraint=FINER)

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

                    s = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                    side1Edges = s.getSequenceFromMask(mask=('[#e ]', ), )
                    p.Surface(side1Edges=side1Edges, name='Contact_Master_Surf')

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.seedPart(size=coarseMeshSize, deviationFactor=0.1, minSizeFactor=0.1)

                    pickedEdges1 = p.edges.getSequenceFromMask(mask=('[#11 ]', ), )
                    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, minSize=fineMeshSize, maxSize=coarseMeshSize, constraint=FINER)
                    pickedEdges = p.edges.getSequenceFromMask(mask=('[#e ]', ), )
                    p.seedEdgeBySize(edges=pickedEdges, size=fineMeshSize, deviationFactor=0.1, constraint=FINER)

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

                    s = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
                    side1Edges = s.getSequenceFromMask(mask=('[#6 ]', ), )
                    p.Surface(side1Edges=side1Edges, name='Contact_Master_Surf')

                    p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
                    p.seedPart(size=coarseMeshSize, deviationFactor=0.1, minSizeFactor=0.1)

                    pickedEdges1 = p.edges.getSequenceFromMask(mask=('[#9 ]', ), )
                    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, minSize=fineMeshSize, maxSize=coarseMeshSize, constraint=FINER)
                    pickedEdges = p.edges.getSequenceFromMask(mask=('[#6 ]', ), )
                    p.seedEdgeBySize(edges=pickedEdges, size=fineMeshSize, deviationFactor=0.1, constraint=FINER)

            e = self.mdb.models['Model-1'].parts['Deformable_Indenter'].edges
            # print e.getBoundingBox()
            edges = e.findAt(((5e-6, e.getBoundingBox()['high'][1], 0.0), ))
            p.Set(edges=edges, name='Top_Set')
            edges = e.findAt(((0.0, 5e-6, 0.0), ))
            xVerts = p.vertices.findAt(((0.0, e.getBoundingBox()['high'][1], 0.0), ))
            p.Set(edges=edges, xVertices=xVerts, name='Center-Line_Set')

            f = self.mdb.models['Model-1'].parts['Deformable_Indenter'].faces
            pickedRegions = f.getSequenceFromMask(mask=('[#1 ]', ), )

            # p.setMeshControls(regions=pickedRegions, elemShape=QUAD)
            p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED)

            if self.analysisType.startswith('Standard'):

                # elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=STANDARD)

            elif self.analysisType.startswith('Explicit'):

                # elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
                elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=EXPLICIT)

            faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
            pickedRegions =(faces, )
            p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
            p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
            p.generateMesh()

            p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
            f = p.faces
            faces = f.findAt(((5e-6, 5e-4, 0.0), ))
            region = p.Set(faces=faces, name='Set-1')
            p.SectionAssignment(region=region, sectionName='Elastic_'+self.indMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

        return(0)

    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------

    def createAssembly(self,*args,**kwargs):

        self.indenterType = args[0]

        self.indenterOffset = kwargs.get('indenterOffset',self.totalHeight)

        from math import cos

        from caeModules import assembly

        a = self.mdb.models['Model-1'].rootAssembly
        a.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, -1.0))

        p = self.mdb.models['Model-1'].parts['Test_Article']
        a.Instance(name='Test_Article-1', part=p, dependent=ON)

        if self.indenterType == 'Rigid':

            p = self.mdb.models['Model-1'].parts['Analytic_Indenter']
            a.Instance(name='Indenter-1', part=p, dependent=ON)
            a = self.mdb.models['Model-1'].rootAssembly
            a.translate(instanceList=('Indenter-1', ), vector=(0.0, self.indenterOffset, 0.0))

        elif self.indenterType == 'Deformable':

            p = self.mdb.models['Model-1'].parts['Deformable_Indenter']
            a.Instance(name='Indenter-1', part=p, dependent=ON)
            a = self.mdb.models['Model-1'].rootAssembly
            a.translate(instanceList=('Indenter-1', ), vector=(0.0, self.indenterOffset, 0.0))

        else: print('Indenter type selected is not valid.')

        if self.indenterType == 'Rigid':

            rp1Coord = (0.0,self.charIndSize*cos(self.iAng) + self.indenterOffset)

        elif self.indenterType == 'Deformable':

            tempYcoord = []

            for node in a.instances['Indenter-1'].nodes: tempYcoord.append(node.coordinates[1])

            rp1Coord = (0.0,max(tempYcoord))

        a = self.mdb.models['Model-1'].rootAssembly
        a.ReferencePoint(point=(rp1Coord[0], rp1Coord[1], 0.0))
        refPoints1=(self.mdb.models['Model-1'].rootAssembly.referencePoints[6], )
        a.Set(referencePoints=refPoints1, name='mSet-1')

        return(0)

    #-----------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------









# from abaqus import session
# session.viewports['Viewport: 1'].setValues(displayedObject=self.mdb.models['Model-1'].parts['Test_Article'])
# session.viewports['Viewport: 1'].view.setValues(nearPlane=835.25, farPlane=1546.51, width=883.161, height=391.953, cameraPosition=(-637.305, 506.812, -455.828), cameraUpVector=(0.639476, 0.597057, 0.484348), cameraTarget=(154.965, -165.983, 158.396))
# session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
# session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(meshTechnique=ON)
# session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=OFF)
# raise ValueError("We're done for now!")












    # #-----------------------------------------------------------------------

    # def createCylindricalTestArticle(self,*args,**kwargs):

        # self.taL = args[0]
        # self.taH = args[1]
        # self.articlePart = args[2]
        # self.meshSize = args[3]
        # self.meshMultiples = args[4]
        # self.meshAspectRatio = args[5]

        # meshSize0 = self.meshSize
        # meshSize1 = meshSize0 * self.meshMultiples[0]
        # meshSize2 = meshSize1 * self.meshMultiples[1]
        # meshSize3 = meshSize2 * self.meshMultiples[2]
        # meshSize4 = meshSize3 * self.meshMultiples[3]

        # from caeModules import part

        # s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
        # g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        # s.setPrimaryObject(option=STANDALONE)
        # s.rectangle(point1=(0.0, 0.0), point2=(self.taL, -self.taH))
        # self.mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', toName='Cylindrical_Test_Article_Sketch')
        # s.unsetPrimaryObject()

        # s1 = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
        # g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        # s1.sketchOptions.setValues(viewStyle=AXISYM)
        # s1.setPrimaryObject(option=STANDALONE)
        # s1.ConstructionLine(point1=(0.0, -0.5), point2=(0.0, 0.5))
        # s1.retrieveSketch(sketch=self.mdb.models['Model-1'].sketches['Cylindrical_Test_Article_Sketch'])

        # p = self.mdb.models['Model-1'].Part(name='Test_Article', dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # p.BaseShell(sketch=s1)
        # s1.unsetPrimaryObject()
        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # del self.mdb.models['Model-1'].sketches['__profile__']

        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # faces = p.faces.findAt(((0.0,0.0,0.0),))
        # p.Set(faces=faces, name='Set-1')
        # edges = p.edges.findAt(((0.0,-5e-6,0.0),))
        # p.Set(edges=edges, name='Center-Line_Set')
        # edges = p.edges.findAt(((5e-6,0.0,0.0),))
        # p.Set(edges=edges, name='Top_Set')
        # p.Surface(side1Edges=edges, name='Slave_Contact_Surf')
        # edges = p.edges.findAt(((5e-6,-self.taH,0.0),))
        # p.Set(edges=edges, name='Base_Set')
        # edges = p.edges.findAt(((self.taL,-5e-6,0.0),))
        # p.Set(edges=edges, name='OD_Set')
        # p.Surface(side1Edges=edges, name='OD_Surf')

        # pickedRegions = p.faces.findAt(((0.0,0.0,0.0),))
        # p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED, technique=FREE, algorithm=MEDIAL_AXIS)

        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # f, e, d1 = p.faces, p.edges, p.datums
        # t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        # s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.5,gridSpacing=0.01, transform=t)
        # g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        # s.setPrimaryObject(option=SUPERIMPOSE)
        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        # s.Line(point1=(self.articlePart[1]*self.taL, 0.0), point2=(self.articlePart[1]*self.taL, -self.taH))
        # s.Line(point1=(0.0, -self.articlePart[1]*self.taH), point2=(self.taL, -self.articlePart[1]*self.taH))
        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # f = p.faces
        # pickedFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
        # e1, d2 = p.edges, p.datums
        # p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
        # s.unsetPrimaryObject()
        # del self.mdb.models['Model-1'].sketches['__profile__']

        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # edges = p.edges.findAt(((0.0,-5e-6,0.0),))
        # p.Set(edges=edges, name='Results_CL_Set')
        # edges = p.edges.findAt(((5e-6,0.0,0.0),))
        # p.Set(edges=edges, name='Results_Surf_Set')

        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # faces = p.faces.findAt(((0.0,0.0,0.0),))
        # p.Set(faces=faces, name='Remeshing_Set')
        # p.Set(faces=faces, name='Mat_Plastic_Set')
        # p.Set(faces=faces, name='Node_Contact_Set')
        # faces = p.faces.findAt(((self.taL,0.0,0.0),),((0.0,-self.taH,0.0),),((self.taL,-self.taH,0.0),))
        # p.Set(faces=faces, name='Mat_Elastic_Set')

        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # f, e, d1 = p.faces, p.edges, p.datums
        # t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        # s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.5,gridSpacing=0.01, transform=t)
        # g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        # s.setPrimaryObject(option=SUPERIMPOSE)
        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        # s.Line(point1=(self.articlePart[2]*self.taL, 0.0), point2=(self.articlePart[2]*self.taL, -self.taH))
        # s.Line(point1=(0.0, -self.articlePart[2]*self.taH), point2=(self.taL, -self.articlePart[2]*self.taH))
        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # f = p.faces
        # pickedFaces = p.faces.findAt(((self.taL,0.0,0.0),),((0.0,-self.taH,0.0),),((self.taL,-self.taH,0.0),))
        # e1, d2 = p.edges, p.datums
        # p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
        # s.unsetPrimaryObject()
        # del self.mdb.models['Model-1'].sketches['__profile__']

        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # f, e, d1 = p.faces, p.edges, p.datums
        # t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
        # s = self.mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=0.5,gridSpacing=0.01, transform=t)
        # g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        # s.setPrimaryObject(option=SUPERIMPOSE)
        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        # s.Line(point1=(self.articlePart[3]*self.taL, 0.0), point2=(self.articlePart[3]*self.taL, -self.taH))
        # s.Line(point1=(0.0, -self.articlePart[3]*self.taH), point2=(self.taL, -self.articlePart[3]*self.taH))
        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # f = p.faces
        # pickedFaces = p.faces.findAt(((self.taL,0.0,0.0),),((self.taL,-(self.articlePart[1]*self.taH+5e-6),0.0),),((self.taL,-self.taH,0.0),),((0.0,-self.taH,0.0),),((self.articlePart[1]*self.taL+5e-6,-self.taH,0.0),))
        # e1, d2 = p.edges, p.datums
        # p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
        # s.unsetPrimaryObject()
        # del self.mdb.models['Model-1'].sketches['__profile__']

        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # region = p.sets['Mat_Plastic_Set']
        # p.SectionAssignment(region=region, sectionName = self.taMatPlast+'_'+self.taMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
        # region = p.sets['Mat_Elastic_Set']
        # p.SectionAssignment(region=region, sectionName='Elastic_'+self.taMatName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

        # from caeModules import mesh

        # if self.analysisType.startswith('Standard'):

            # elemType1 = mesh.ElemType(elemCode=CAX4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            # elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=STANDARD)

        # elif self.analysisType.startswith('Explicit'):

            # elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
            # elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)

        # else: raise ValueError('Analysis type chosen is not valid.')

        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # faces = p.faces.getSequenceFromMask(mask=('[#ffff ]', ), )
        # pickedRegions =(faces, )
        # try: p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
        # except: p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))

        # p = self.mdb.models['Model-1'].parts['Test_Article']
        # p.seedPart(size=meshSize1, deviationFactor=0.1, minSizeFactor=0.1)

        # pickedEdges1 = p.edges.getByBoundingBox(xMin=-5e6,yMin=-(self.articlePart[1]*self.taH+5e-6),xMax=5e6,yMax=-(self.articlePart[1]*self.taH-5e-6))
        # pickedEdges2 = p.edges.getByBoundingBox(xMin=self.articlePart[1]*self.taL-5e-6,yMin=-5e6,xMax=self.articlePart[1]*self.taL+5e-6,yMax=5e6)
        # p.seedEdgeBySize(edges=pickedEdges1+pickedEdges2, size=meshSize1, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        # p.Set(edges=pickedEdges1+pickedEdges2, name='Mesh_1_Edge_Seeds')

        # pickedEdges1 = p.edges.getByBoundingBox(xMin=-5e6,yMin=-(self.articlePart[2]*self.taH+5e-6),xMax=5e6,yMax=-(self.articlePart[2]*self.taH-5e-6))
        # pickedEdges2 = p.edges.getByBoundingBox(xMin=self.articlePart[2]*self.taL-5e-6,yMin=-5e6,xMax=self.articlePart[2]*self.taL+5e-6,yMax=5e6)
        # p.seedEdgeBySize(edges=pickedEdges1+pickedEdges2, size=meshSize2, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        # p.Set(edges=pickedEdges1+pickedEdges2, name='Mesh_2_Edge_Seeds')

        # pickedEdges1 = p.edges.getByBoundingBox(xMin=self.articlePart[3]*self.taL-5e-6,yMin=-(self.articlePart[3]*self.taH+5e-6),xMax=self.articlePart[3]*self.taL+5e-6,yMax=5e-6)
        # pickedEdges2 = p.edges.getByBoundingBox(xMin=-5e-6,yMin=-(self.articlePart[3]*self.taH+5e-6),xMax=self.articlePart[3]*self.taL+5e-6,yMax=-(self.articlePart[3]*self.taH-5e-6))
        # p.seedEdgeBySize(edges=pickedEdges1+pickedEdges2, size=meshSize3, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        # p.Set(edges=pickedEdges1+pickedEdges2, name='Mesh_3_Edge_Seeds')

        # pickedEdges1 = p.edges.getByBoundingBox(xMin=self.taL-5e-6,yMin=-(self.taH+5e-6),xMax=self.taL+5e-6,yMax=5e-6)
        # pickedEdges2 = p.edges.getByBoundingBox(xMin=-5e-6,yMin=-(self.taH+5e-6),xMax=self.taL+5e-6,yMax=-(self.taH-5e-6))
        # p.seedEdgeBySize(edges=pickedEdges1+pickedEdges2, size=meshSize4, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)
        # p.Set(edges=pickedEdges1+pickedEdges2, name='Mesh_4_Edge_Seeds')

        # #Horizontal 1 -> 2
        # end1Edges = p.edges.findAt(((self.articlePart[1]*self.taL+5e-6,-self.articlePart[1]*self.taH,0.0),))
        # end2Edges = p.edges.findAt(((self.articlePart[1]*self.taL+5e-6,0.0,0.0),))
        # p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize1, maxSize=meshSize2, constraint=FINER)
        # p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=end2Edges, minSize=meshSize1, maxSize=meshSize2, constraint=FINER)

        # #Vertical 1 -> 2
        # end1Edges = p.edges.findAt(((0.0,-(self.articlePart[1]*self.taH+5e-6),0.0),))
        # end1Edges = end1Edges + p.edges.findAt(((self.articlePart[1]*self.taL,-(self.articlePart[1]*self.taH+5e-6),0.0),))
        # p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize1, maxSize=meshSize2, constraint=FINER)

        # #Horizontal 2 -> 3
        # end1Edges = p.edges.findAt(((self.articlePart[2]*self.taL+5e-6,-self.articlePart[2]*self.taH,0.0),))
        # end1Edges = end1Edges + p.edges.findAt(((self.articlePart[2]*self.taL+5e-6,-self.articlePart[1]*self.taH,0.0),))
        # end2Edges = p.edges.findAt(((self.articlePart[2]*self.taL+5e-6,0.0,0.0),))
        # p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize2, maxSize=meshSize3, constraint=FINER)
        # p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=end2Edges, minSize=meshSize2, maxSize=meshSize3, constraint=FINER)

        # #Vertical 2 -> 3
        # end1Edges = p.edges.findAt(((0.0,-(self.articlePart[2]*self.taH+5e-6),0.0),))
        # end1Edges = end1Edges + p.edges.findAt(((self.articlePart[1]*self.taL,-(self.articlePart[2]*self.taH+5e-6),0.0),))
        # end1Edges = end1Edges + p.edges.findAt(((self.articlePart[2]*self.taL,-(self.articlePart[2]*self.taH+5e-6),0.0),))
        # p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize2, maxSize=meshSize3, constraint=FINER)

        # #Horizontal 3 -> 4
        # end1Edges = p.edges.findAt(((self.articlePart[3]*self.taL+5e-6,-self.articlePart[3]*self.taH,0.0),))
        # end1Edges = end1Edges + p.edges.findAt(((self.articlePart[3]*self.taL+5e-6,-self.articlePart[2]*self.taH,0.0),))
        # end1Edges = end1Edges + p.edges.findAt(((self.articlePart[3]*self.taL+5e-6,-self.articlePart[1]*self.taH,0.0),))
        # end2Edges = p.edges.findAt(((self.articlePart[3]*self.taL+5e-6,0.0,0.0),))
        # p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize3, maxSize=meshSize4, constraint=FINER)
        # p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=end2Edges, minSize=meshSize3, maxSize=meshSize4, constraint=FINER)

        # #Vertical 3 -> 4
        # end1Edges = p.edges.findAt(((0.0,-(self.articlePart[3]*self.taH+5e-6),0.0),))
        # end1Edges = end1Edges + p.edges.findAt(((self.articlePart[1]*self.taL,-(self.articlePart[3]*self.taH+5e-6),0.0),))
        # end1Edges = end1Edges + p.edges.findAt(((self.articlePart[2]*self.taL,-(self.articlePart[3]*self.taH+5e-6),0.0),))
        # end1Edges = end1Edges + p.edges.findAt(((self.articlePart[3]*self.taL,-(self.articlePart[3]*self.taH+5e-6),0.0),))
        # p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=end1Edges, minSize=meshSize3, maxSize=meshSize4, constraint=FINER)

        # pickedRegions = f.findAt(((self.articlePart[1]*self.taL+5e-6, 0.0, 0.0), ), ((0.0, -(self.articlePart[1]*self.taH+5e-6), 0.0), ))
        # p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED, technique=FREE, algorithm=ADVANCING_FRONT, allowMapped=True)

        # pickedRegions = f.findAt(((self.articlePart[1]*self.taL+5e-6, -(self.articlePart[1]*self.taH+5e-6), 0.0), ))
        # p.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED, technique=FREE, algorithm=ADVANCING_FRONT, allowMapped=False)

        # #---New Stuff-----------------------------------------------------------------
        # f = self.mdb.models['Model-1'].parts['Test_Article'].faces
        # pickedRegions = f.findAt(((5e-6, -5e-6, 0.0), ))
        # p.setMeshControls(regions=pickedRegions, technique=SWEEP)

        # e = self.mdb.models['Model-1'].parts['Test_Article'].edges
        # pickedEdges = e.findAt(((self.articlePart[0]*self.taL, -5e-6, 0.0), ), ((0.0, -5e-6, 0.0), ))
        # p.seedEdgeBySize(edges=pickedEdges, size=1.0*meshSize0, deviationFactor=0.1, minSizeFactor=0.1, constraint=FINER)

        # if not self.meshAspectRatio == 1.0:

            # e = self.mdb.models['Model-1'].parts['Test_Article'].edges
            # pickedEdges1 = e.findAt(((0.0, -5e-6, 0.0), ))
            # p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, minSize=meshSize0/2.0, maxSize=meshSize0, constraint=FINER)
            # pickedEdges1 = e.findAt(((self.articlePart[0]*self.taL, -5e-6, 0.0), ))
            # p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, minSize=meshSize0/2.0, maxSize=meshSize0, constraint=FINER)

        # p.generateMesh()

        # return(0)

    # #-----------------------------------------------------------------------
