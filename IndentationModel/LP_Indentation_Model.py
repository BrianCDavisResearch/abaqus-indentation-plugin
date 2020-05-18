#-----------------------------------------------------------------------

def default_system_units(*args,**kwargs):

    #-----------------------------------------------------------------------

    #------------------------------------------
    #Base Units for Micro-Indenter Analyses
    #------------------------------------------

    #Mass -> milligram mg (kg*10^-6)
    #Time -> millisecond ms (s*10^-3)
    #Length -> micrometer um (m*10^-6)

    #------------------------------------------
    #Derived Units for Micro-Indenter Analyses
    #------------------------------------------

    #Force -> microNewtons (mg*um/ms^2 = N*10^-6 = uN)
    #Pressure -> MegaPascals (uN/um^2 = Pa*10^6 = MPa)
    #Density -> milligram / micrometer^3 (kg/m^3 = (mg/um^3)*10^-12)
    #Energy -> picoJoule (uN*um = J*10^-12 = pJ)

    #-----------------------------------------------------------------------

    print('\n\n#------------------------------------------')
    print('#Base Units for Micro-Indenter Analyses')
    print('#------------------------------------------')
    print('\n')
    print('#Mass -> milligram mg (kg*10^-6)')
    print('#Time -> millisecond ms (s*10^-3)')
    print('#Length -> micrometer um (m*10^-6)')
    print('\n')
    print('#------------------------------------------')
    print('#Derived Units for Micro-Indenter Analyses')
    print('#------------------------------------------')
    print('\n')
    print('#Force -> microNewtons (mg*um/ms^2 = N*10^-6 = uN)')
    print('#Pressure -> MegaPascals (uN/um^2 = Pa*10^6 = MPa)')
    print('#Density -> milligram / micrometer^3 (kg/m^3 = (mg/um^3)*10^-12)')
    print('#Energy -> picoJoule (uN*um = J*10^-12 = pJ)\n\n')

    #-----------------------------------------------------------------------


    #-----------------------------------------------------------------------

    #------------------------------------------
    #Base Units for Nano-Indenter Analyses
    #------------------------------------------

    #------------------------------------------
    #Derived Units for Nano-Indenter Analyses
    #------------------------------------------

    #-----------------------------------------------------------------------

    return(0)

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

def run_input_script(inp):

    print('\n\nRunning Abaqus Python Model-Building Script...\n')

    #-----------------------------------------------------------------------
    #Changing options if a "preSolve" is being performed
    #-----------------------------------------------------------------------
    if ('preSolve' in dict(inp)):

        if inp['preSolve']:

            inp['fieldIntervals'] = 100

            inp['meshDivider'] = 25.0

            inp['controlType'] = 'Displacement'

            inp['jobName'] = inp['jobName'] + '_pre'
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Loading modules and making class instance
    #-----------------------------------------------------------------------
    import numpy as np
    from imp import load_source
    importedLibrary = load_source('Lib_Indenter_Combo', inp['moduleName'])
    if inp['taType'] == 'AsymIndent': indenter = importedLibrary.ASym_Indenter_Analysis(inp['taType'],inp['analysisType'],inp['jobName'])
    elif inp['taType'] == 'QsymIndent': indenter = importedLibrary.QSym_Indenter_Analysis(inp['taType'],inp['analysisType'],inp['jobName'])
    elif inp['taType'] == 'HsymIndent': indenter = importedLibrary.HSym_Indenter_Analysis(inp['taType'],inp['analysisType'],inp['jobName'])
    elif inp['taType'] == 'AsymPillar': indenter = importedLibrary.ASym_Pillar_Analysis(inp['taType'],inp['analysisType'],inp['jobName'])
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Analysis options which vary based on analysis type
    #-----------------------------------------------------------------------
    if inp['analysisType'].startswith('Standard'):

        inp['contactType'] = 'Node'

    elif inp['analysisType'].startswith('Explicit'):

        inp['contactType'] = 'Surface'

        inp['taMatRayDamp'] = (0.020,0.0)

        # inp['taMatRayDamp'] = (0.100,0.0)
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Alternative control types which require a "preSolve" to predict depth
    #-----------------------------------------------------------------------
    if ('controlType' in dict(inp)):

        if inp['controlType'] == 'Force':

            inp['indenterDepth'] = indenter.expectedDepthForce(inp['jobName'],inp['indenterForce'])            #Function for "pre-solve" defining indenter force vs. depth

        elif inp['controlType'] == 'Energy':

            inp['indenterDepth'] = indenter.expectedDepthEnergy(inp['jobName'],indenterEnergy)          #Function for "pre-solve" defining indenter energy vs. depth

        elif inp['controlType'] == 'InitialVelocity':

            inp['indenterDepth'] = indenter.expectedDepthVelocity(inp['jobName'],indenterVelocity)      #This function has not been made
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Group of default options which are used if not specified earlier
    #-----------------------------------------------------------------------
    if not ('taSize' in dict(inp)): inp['taSize'] = 100.0 * inp['indenterDepth']

    if not ('taScale' in dict(inp)): inp['taScale'] = 1.0

    if not ('taPart' in dict(inp)): inp['taPart'] = (0.0,0.050,0.100,0.200,1.000)                   #(unitless) fraction of OAL for refined mesh partitions

    if not ('meshAspectRatio' in dict(inp)): inp['meshAspectRatio'] = 1.0

    if not ('meshMultiples' in dict(inp)): inp['meshMultiples'] = (1.0, inp['meshDivider'], 3.0, 2.0)

    if not ('bulkViscosity' in dict(inp)): inp['bulkViscosity'] = (0.06,0.06,0.06,0.06)

    if not ('indenterOffset' in dict(inp)): inp['indenterOffset'] = 0.0

    if not ('taMatRayDamp' in dict(inp)): inp['taMatRayDamp'] = None

    if not ('incrementTime' in dict(inp)): inp['incrementTime'] = None

    if not ('stepTime' in dict(inp)): inp['stepTime'] = (10.0e3,0.0e3,10.0e3,0.0e3)

    if not ('taMeshRefine' in dict(inp)): inp['taMeshRefine'] = (1,2)

    if not ('indMatName' in dict(inp)): inp['indMatName'] = None

    if not ('indMatDens' in dict(inp)): inp['indMatDens'] = None

    if not ('indMatYM' in dict(inp)): inp['indMatYM'] = None

    if not ('indMatPR' in dict(inp)): inp['indMatPR'] = None
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Calculations which are dependent on indenter depth
    #-----------------------------------------------------------------------
    tempEstIndentRadius = inp['indenterDepth'] * np.tan(np.radians(inp['indDemiAngle']))

    tempEstContactLength = inp['indenterDepth'] / np.cos(np.radians(inp['indDemiAngle']))

    tempFineMeshSize = inp['indenterDepth'] / inp['meshDivider']

    if ('altIndenterMass' in dict(inp)):

        print('altIndenterMass found: %s mg' %(inp['altIndenterMass']))

        inp['indenterMass'] = inp['altIndenterMass']

    else:

        tempIndenterMass = (3.51e-9) * (1.0/3.0)*np.pi*(1.0*inp['indenterDepth'])**3.0 * (np.tan(np.radians(inp['indDemiAngle'])))**2.0 #(mg) mass of diamond in cone with height indent depth

        inp['indenterMass'] = 1e-01 * tempIndenterMass                                              #Scales indenter mass to cut back on noise in the system

    if ('indRadiusFraction' in dict(inp)):

        print('indRadiusFraction found: %s um' %(inp['indRadiusFraction']))

        inp['indRadius'] = inp['indRadiusFraction']*inp['indenterDepth']
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Printing basic analytic indent calculations
    #-----------------------------------------------------------------------
    print('Indenter mass: %0.3E (mg/um3)' %(inp['indenterMass']))
    print('Estimated Analytic Indent Depth: %.2f (um)' %(inp['indenterDepth']))
    print('Estimated Analytic Indent Radius: %.2f (um)' %(tempEstIndentRadius))
    print('Estimated Analytic Contact Length: %.2f (um)' %(tempEstContactLength))
    print('Radius of First Partition: %.2f (um)' %(inp['taSize'] * inp['taPart'][1]))
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Running class methods which build the model
    #-----------------------------------------------------------------------
    inp['indMatName'],inp['indMatYM'],inp['indMatPR'],inp['indMatDens'] = indenter.createElasticMaterials(indType=inp['indType'],taMatName=inp['taMatName'],taMatYM=inp['taMatYM'],taMatPR=inp['taMatPR'],taMatDens=inp['taMatDens'],taMatRayDamp=inp['taMatRayDamp'],indMatName=inp['indMatName'],indMatYM=inp['indMatYM'],indMatPR=inp['indMatPR'],indMatDens=inp['indMatDens'])

    indenter.createPlasticMaterials(taMatPlast=inp['taMatPlast'],taMatYSmin=inp['taMatYSmin'],taMatGTNrd=inp['taMatGTNrd'],taMatGTNq=inp['taMatGTNq'],taMatDPCap=inp['taMatDPCap'],taMatDPCapHard=inp['taMatDPCapHard'],taMatKerm=inp['taMatKerm'],taMatMoln=inp['taMatMoln'])

    #----line of re-editing----

    if inp['taType'] == 'AsymIndent':

        indenter.createCylindricalTestArticle(inp['taScale']*inp['taSize'],inp['taScale']*inp['taSize'],inp['taPart'],tempFineMeshSize,inp['meshMultiples'],inp['meshAspectRatio'])

        indenter.createIndenter(inp['indDemiAngle'],indRadius=inp['indRadius'],indFlat=inp['indFlat'])

    elif inp['taType'] == 'QsymIndent':

        indenter.createQuarterTestArticle(inp['taScale']*inp['taSize'],inp['taScale']*inp['taSize'],inp['taPart'],tempFineMeshSize,inp['meshMultiples'],inp['meshAspectRatio'])

        indenter.createQuarterIndenter(inp['indDemiAngle'],indRadius=inp['indRadius'],indFlat=inp['indFlat'])

    elif inp['taType'] == 'HsymIndent':

        indenter.createHalfTestArticle(inp['taScale']*inp['taSize'],inp['taScale']*inp['taSize'],inp['taPart'],tempFineMeshSize,inp['meshMultiples'],inp['meshAspectRatio'])

        indenter.createHalfIndenter(inp['indDemiAngle'],indRadius=inp['indRadius'],indFlat=inp['indFlat'])

    elif inp['taType'] == 'CsymIndent':

        print("This isn't ready yet!")    

    elif inp['taType'] == 'Full3DIndent':

        print("This isn't ready yet!")

    elif inp['taType'] == 'AsymPillar':

        indenter.createPillarTestArticle()

        indenter.createPillarIndenter()

    #-----------------------------------------------------------------

    indenter.createAssembly(inp['indType'])

    indenter.createInteractions(inp['indType'],inp['indenterMass'],inp['contactFriction'],inp['contactType'])

    indenter.createSteps(inp['stepTime'],fieldIntervals=inp['fieldIntervals'],historyIntervals=inp['historyIntervals'],bulkViscosity=inp['bulkViscosity'])

    indenter.createLoadsBCs('Displacement',indenterDepth=inp['indenterDepth'])

    indenter.createRemeshing(remeshingParameters=inp['taMeshRefine'])

    indenter.createJob(inp['jobName'],inp['numCPU'])

    if ('biaxialPrestress' in dict(inp)) and not inp['biaxialPrestress'] == 0.0: indenter.createPredefinedField(inp['biaxialPrestress'])

    try: indenter.setView()
    except: print('Warning: Unable to set CAE view settings.')
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Writing inputs to CSV file
    #-----------------------------------------------------------------------
    import csv

    if ('csvMethod' in dict(inp)) and inp['csvMethod']: inp['csvName'] = inp['jobName'] + '_upg_All-Inputs' + '.csv'
    else: inp['csvName'] = inp['jobName'] + '_All-Inputs' + '.csv'

    with open(inp['csvName'], 'wb') as tempFile:

        csvWriter = csv.writer(tempFile)

        for key,value in sorted(inp.items()): csvWriter.writerow([key,value])
    #-----------------------------------------------------------------------

    return(0)

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

def input_plugin_prescript(*args,**kwargs):

    print('\n\nRunning Abaqus Python Model-Building Plugin...\n')

    import os

    #-----------------------------------------------------------------------
    #Creating "inp" dictionary and specifying module location and importing values from plugin kwargs
    #-----------------------------------------------------------------------
    inp = {}
    inp['moduleName'] = '%s\\abaqus_plugins\\IndentationModel\\Module_Indentation.py' %(os.path.expanduser('~'))
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Importing values to "inp" dictionary from plugin kwargs
    #----------------------------------------------------------------------
    inp['taType'] = str(kwargs.get('taType','AsymIndent'))

    inp['analysisType'] = str(kwargs.get('analysisType','Standard - Quasi-Static'))

    inp['indType'] = str(kwargs.get('indType','Deformable'))
    inp['indDemiAngle'] = float(kwargs.get('indDemiAngle',70.3))
    inp['indRadius'] = float(kwargs.get('indRadius',0.0))
    inp['indFlat'] = float(kwargs.get('indFlat',0.0))

    inp['indenterDepth'] = float(kwargs.get('indenterDepth',5.0))
    inp['contactFriction'] = float(kwargs.get('contactFriction',0.0))

    inp['meshDivider'] = float(kwargs.get('meshDivider',50.0))
    inp['taScale'] = float(kwargs.get('taScale',1.0))

    inp['taMeshR1'] = int(kwargs.get('taMeshR1',1))
    inp['taMeshR2'] = int(kwargs.get('taMeshR2',2))
    inp['taMeshRefine'] = [inp['taMeshR1'],inp['taMeshR2']]
    del inp['taMeshR1']; del inp['taMeshR2'];

    inp['indMatName'] = str(kwargs.get('indMatName','Diamond'))
    inp['indMatYM'] = float(kwargs.get('indMatYM',1220e3))
    inp['indMatPR'] = float(kwargs.get('indMatPR',0.20))
    inp['indMatDens'] = float(kwargs.get('indMatDens',3.52e-9))

    inp['taMatName'] = str(kwargs.get('taMatName','a-SiO2'))
    inp['taMatYM'] = float(kwargs.get('taMatYM',70.0e3))
    inp['taMatPR'] = float(kwargs.get('taMatPR',0.15))
    inp['taMatDens'] = float(kwargs.get('taMatDens',2.20e-9))

    inp['taMatPlast'] = str(kwargs.get('taMatPlast','DP-Cap'))

    inp['taMatDPCap0'] = float(kwargs.get('taMatDPCap0',5500.0))
    inp['taMatDPCap1'] = float(kwargs.get('taMatDPCap1',10.0))
    inp['taMatDPCap2'] = float(kwargs.get('taMatDPCap2',0.85))
    inp['taMatDPCap3'] = float(kwargs.get('taMatDPCap3',0.0))
    inp['taMatDPCap4'] = float(kwargs.get('taMatDPCap4',0.01))
    inp['taMatDPCap5'] = float(kwargs.get('taMatDPCap5',1.0))

    inp['taMatDPCap'] =  (inp['taMatDPCap0'], inp['taMatDPCap1'], inp['taMatDPCap2'], inp['taMatDPCap3'], inp['taMatDPCap4'], inp['taMatDPCap5'])
    inp['taMatDPCapHard'] = ((4750.0, 0.0),(8000.0, 0.005),(9800.0, 0.0123),(12000.0, 0.0427),(13600.0, 0.0735),(14600.0, 0.117),(15500.0, 0.135),(18100.0, 0.1655),(20000.0, 0.188),(25000.0, 0.195),(50000.0, 0.196)) #Hardening from Molnar 2017, Rouxel 2008, and Deschamps 2013
    del inp['taMatDPCap0']; del inp['taMatDPCap1']; del inp['taMatDPCap2']; del inp['taMatDPCap3']; del inp['taMatDPCap4']; del inp['taMatDPCap5'];

    inp['taMatYSmin'] = float(kwargs.get('taMatYSmin',7.50e3))
    inp['taMatGTNrd'] = float(kwargs.get('taMatGTNrd',0.85))
    inp['taMatGTNq1'] = float(kwargs.get('taMatGTNq1',0.90))
    inp['taMatGTNq2'] = float(kwargs.get('taMatGTNq2',0.90))

    inp['taMatGTNq'] = (inp['taMatGTNq1'],inp['taMatGTNq2'],inp['taMatGTNq1']**2.0)
    del inp['taMatGTNq1']; del inp['taMatGTNq2'];

    inp['taMatK1'] = float(kwargs.get('taMatK1',6500.0))
    inp['taMatK2'] = float(kwargs.get('taMatK2',-11500.0))
    inp['taMatK3'] = float(kwargs.get('taMatK3',100000.0))

    inp['taMatKerm'] = (inp['taMatK1'],inp['taMatK2'],inp['taMatK3'])
    del inp['taMatK1']; del inp['taMatK2']; del inp['taMatK3'];

    inp['taMatM1'] = float(kwargs.get('taMatM1',5.0))
    inp['taMatM2'] = float(kwargs.get('taMatM2',5700.0))
    inp['taMatM3'] = float(kwargs.get('taMatM3',5000.0))
    inp['taMatM4'] = float(kwargs.get('taMatM4',-3000.0))
    inp['taMatM5'] = float(kwargs.get('taMatM5',-0.196))
    inp['taMatM6'] = float(kwargs.get('taMatM6',3.0))
    inp['taMatM7'] = float(kwargs.get('taMatM7',4.0))
    inp['taMatM8'] = float(kwargs.get('taMatM8',-20000.0))
    inp['taMatM9'] = float(kwargs.get('taMatM9',7000.0))

    inp['taMatMoln'] = (inp['taMatM1'],inp['taMatM2'],inp['taMatM3'],inp['taMatM4'],inp['taMatM5'],inp['taMatM6'],inp['taMatM7'],inp['taMatM8'],inp['taMatM9'])
    del inp['taMatM1']; del inp['taMatM2']; del inp['taMatM3']; del inp['taMatM4']; del inp['taMatM5']; del inp['taMatM6']; del inp['taMatM7']; del inp['taMatM8']; del inp['taMatM9'];

    inp['fieldIntervals'] = int(kwargs.get('fieldIntervals',50))
    inp['historyIntervals'] = int(kwargs.get('historyIntervals',50))

    inp['jobName'] = str(kwargs.get('jobName','Sharp_Indentation'))
    inp['numCPU'] = int(kwargs.get('numCPU',4))
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Bring the dictionary in-line with other methods (so "Inputs" csv is consistent)
    #-----------------------------------------------------------------------
    inp['controlType'] = 'Displacement'
    inp['csvMethod'] = False
    inp['csvFileNames'] = None
    inp['preSolve'] = False
    #-----------------------------------------------------------------------

    run_input_script(inp)
    
    return(0)
    
#-----------------------------------------------------------------------

# End of Plugin

#-----------------------------------------------------------------------

def input_csv_prescript(inp):

    import os, csv

    os.chdir(r"C:\Abaqus\Mio\TransferOutbound")

    print >> sys.__stdout__, ('\n')

    for fileName in inp['csvFileNames']:

        with open(fileName, 'rb') as tempFile:

            csvReader = csv.reader(tempFile)

            dataKeys = next(csvReader)

            for csvRow in csvReader:

                for i in range(len(dataKeys)):

                    if dataKeys[i] == 'taMatKerm': #Do for other 'multiple' method entries.
                        
                        inp['taMatKerm'] = [float(entry) for entry in csvRow[i].lstrip('(').rstrip(')').split(',')]    

                    elif dataKeys[i].startswith('M'):#depricated "M for Multiple" method...  ...maybe by looking for tuples...

                        inp[dataKeys[i].lstrip('M')] = tuple(float(item) for item in csvRow[i].split(','))

                    else:

                        try: inp[dataKeys[i]] = float(csvRow[i])
                        except: inp[dataKeys[i]] = csvRow[i]

                    print >> sys.__stdout__, ('Data Key: %s; Value: %s'%(dataKeys[i],inp[dataKeys[i]]))

                print >> sys.__stdout__, ('\n')

                run_input_script(inp)

    from subprocess import call

    call(['python', r'C:\Abaqus\WorkingFiles\Mio\Mio_Local_Generate_Slurm_Files_rev2018-09-12a.py'])

    os.chdir(r"C:\Abaqus\Temp")

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

def main(args):

    #-----------------------------------------------------------------------
    # try: session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
    try: session.journalOptions.setValues(replayGeometry=COMPRESSEDINDEX, recoverGeometry=COMPRESSEDINDEX)
    except: pass
    #-----------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Setting up input "inp" dictionary and defining module file
    #---------------------------------------------------------------------------------
    inp = {}
    inp['moduleName'] = r'C:\Abaqus\Module_Indentation.py'
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Analysis Type, Output Frequencies, Step Controls, Solver Cores, Jobname
    #---------------------------------------------------------------------------------
    # inp['analysisType'] = 'Standard - Static'
    # inp['analysisType'] = 'Standard - Quasi-Static'
    inp['analysisType'] = 'Explicit - Mass Scaling'
    #---------------------------------------------------------------------------------
    # inp['stepTime'] = (10.0e3,0.0e3,10.0e3,0.0e3)   #(ms) Step times for Indent, Dwell-Loaded, Remove, Dwell-Unloaded steps (Dwell is ignored for Standard)
    inp['fieldIntervals'] = 50                      #(Unitless) Integer number of field results #1
    inp['historyIntervals'] = 50                    #(Unitless) Integer number of history results #50
    inp['incrementTime'] = 1.0e-00                  #(ms) Target increment time for explicit mass scaling technique
    inp['numCPU'] = 8                               # Number of parallel CPUs used by solver
    #---------------------------------------------------------------------------------
    inp['jobName'] = 'Indentation-Test_01-01'
    # inp['jobName'] = 'Pillar-Test_01-01'
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Indenter: Type
    #---------------------------------------------------------------------------------
    # inp['indType'] = 'Deformable'
    inp['indType'] = 'Rigid'
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Indenter: Geometry (and friction coefficient)
    #---------------------------------------------------------------------------------
    inp['indDemiAngle'] = 70.3            #(degrees) Conical Equivalents: 42.3 (Cube-Corner), 56.3 (Middle), 70.3 (Vickers)
    inp['indRadius'] = 0.000              #(um) 0.0 creates a "Sharp Tip" Indenter (0.3 creates a 300nm radius indenter - "MicroStarTech")
    inp['indFlat'] = 0.000                #(um) creates a flat point which has a radius into the angled indenter surface
    # inp['indRadiusFraction'] = 0.00     #(um) 0.0 creates a "Sharp Tip" Indenter (variable defines indenter radius as a fraction of indent depth)
    #---------------------------------------------------------------------------------
    inp['contactFriction'] = 0.00              #(unitless)
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Indenter: Linear-Elastic Material Properties
    #---------------------------------------------------------------------------------
    inp['indMatName'] = 'Diamond'                   #Only used for Deformable Indenters; Options: 'Diamond', 'Sapphire', or Other (where you must specify a name and property values)
    # inp['indMatName'] = 'Sapphire'
    #---------------------------------------------------------------------------------
    # inp['indMatName'] = 'Custom'
    # inp['indMatDens'] = 1.00e-9
    # inp['indMatYM'] = 1000e3
    # inp['indMatPR'] = 0.15
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Test Article: Type
    #---------------------------------------------------------------------------------
    inp['taType'] = 'AsymIndent'
    # inp['taType'] = 'QsymIndent'
    # inp['taType'] = 'HsymIndent'
    # inp['taType'] = 'CsymIndent'
    #---------------------------------------------------------------------------------
    # inp['taType'] = 'AsymPillar'
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Test Article: Meshing and Re-Meshing
    #---------------------------------------------------------------------------------
    inp['meshDivider'] = 50.0           #Default: 50.0
    inp['taMeshRefine'] = (1,2)         #For explicit analyses, remeshing parameters: [frequency,meshSweeps] "[1,2]" works for Vickers Equivalent
    # inp['taMeshRefine'] = (1,20)      #For explicit analyses, remeshing parameters: [frequency,meshSweeps] "[1,20]" works for Cube-Corner Equivalent
    # inp['taMeshRefine'] = (1,20)         #For explicit analyses, remeshing parameters: [frequency,meshSweeps] "[1,20]" works for the Pillar (must be on remove too!)
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Boundary Condition (i.e. Work Input Controls)
    #---------------------------------------------------------------------------------
    inp['controlType'] = 'Displacement'
    inp['indenterDepth'] = 1.580                #(um) Default: 3.000, Pillar Default: 1.000
    #---------------------------------------------------------------------------------
    # inp['controlType'] = 'Force'
    # inp['indenterForce'] = 1e6                #(uN)
    #---------------------------------------------------------------------------------
    # inp['biaxialPrestress'] = 100.0           #(MPa)
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Test Article: Linear-Elastic Material Properties
    #---------------------------------------------------------------------------------
    #Test Material: Amorphous Si02 (Fused Silica)
    inp['taMatName'] = 'a-SiO2'
    #---------------------------------------------------------------------------------
    #Elastic Properties and Density from: (Rouxel, Yoshida, 2017)
    inp['taMatYM'] = 70.0e3           #Young's Modulus (MPa)
    inp['taMatPR'] = 0.15             #Poisson's Ratio (Unitless)
    inp['taMatDens'] = 2.20e-9        #Density (mg/um^3) or (kg/m^3 * 10^-12) or (g/cm^3 * 10^-9)
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Test Article: Plastic Material Model and Parameters
    #---------------------------------------------------------------------------------
    # inp['taMatPlast'] = 'vonMises'
    inp['taMatPlast'] = 'GTN-pmp'         #'Gurson-Tvergaard-Needleman Porous Metal Plasticity'
    # inp['taMatPlast'] = 'DP-Cap'          #'Drucker-Prager Cap wHardening'
    # inp['taMatPlast'] = 'Kerm2008'        #'Elliptical (Kermouche,2008)'
    # inp['taMatPlast'] = 'Moln2017'        #'Drucker-Prager-Cap (Molnar,2017)'
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Fortran Subroutine Inputs for 'Elliptical (Kermouche,2008)' and 'Drucker-Prager-Cap (Molnar,2017)' Material
    inp['taMatKerm'] = (6500.0, -11500.0, 100000.0)
    inp['taMatMoln'] = (5.0, 5700.0, 5000.0, -3000.0, -0.196, 3.0, 4.0, -20000.0, 7000.0)
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #"DP-Cap" Material: Drucker-Prager Cap w/Hardening Parameters
    #---------------------------------------------------------------------------------

    # #------------------------fitting Kermouche 2008-----------------------------------
    # inp['taMatDPCap'] = (6500.0, 0.001, 1.75, 0.0, 0.05, 1.0)
    # inp['taMatDPCapHard'] = ((5600.0, 0.0),(8000.0, 0.005),(9800.0, 0.0123),(12000.0, 0.0427),(13600.0, 0.0735),(14600.0, 0.117),(15500.0, 0.135),(18100.0, 0.1655),(20000.0, 0.188),(25000.0, 0.195),(50000.0, 0.196)) #Hardening from Molnar 2017, Rouxel 2008, and Deschamps 2013
    # #---------------------------------------------------------------------------------

    # #------------------------fitting Molnar 2017--------------------------------------
    # inp['taMatDPCap'] = (5300.0, 12.0, 1.05, 0.0, 0.05, 1.0)
    # inp['taMatDPCapHard'] = ((5000.0, 0.0),(8000.0, 0.005),(9800.0, 0.0123),(12000.0, 0.0427),(13600.0, 0.0735),(14600.0, 0.117),(15500.0, 0.135),(18100.0, 0.1655),(20000.0, 0.188),(25000.0, 0.195),(50000.0, 0.196)) #Hardening from Molnar 2017, Rouxel 2008, and Deschamps 2013
    # #---------------------------------------------------------------------------------

    #------------------------fitting Molnar 2017 (again)------------------------------
    inp['taMatDPCap'] =  (5500.0, 10.0, 0.85, 0.0, 0.01, 1.0)
    inp['taMatDPCapHard'] = ((4750.0, 0.0),(8000.0, 0.005),(9800.0, 0.0123),(12000.0, 0.0427),(13600.0, 0.0735),(14600.0, 0.117),(15500.0, 0.135),(18100.0, 0.1655),(20000.0, 0.188),(25000.0, 0.195),(50000.0, 0.196)) #Hardening from Molnar 2017, Rouxel 2008, and Deschamps 2013
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #"GTN-pmp" Material: Yield strength and Gurson-Tvegaard-Needlemean Parameters
    #---------------------------------------------------------------------------------

    #------------------------fitting Kermouche 2008-----------------------------------
    inp['taMatYSmin'] = 7.50e3                  #Yield Strength (MPa)
    inp['taMatGTNrd'] = 0.85                    #Relative Density (Unitless) 0.0 < RD <= 1.0 (if RD=1.0 then it's Von Mises) #These values fit the initial Molnar yield surface
    inp['taMatGTNq'] = (0.90,0.90,0.90**2.0)    #q-Parameters (Unitless) these are scaling factors: q1,q2,q3 (the proper value for q3 is q3 = q1**2.0) #These values fit the initial Molnar yield surface
    #---------------------------------------------------------------------------------

    # #------------------------fitting Molnar 2017-----------Force vs. Depth doesn't match on this one---------------------------
    # inp['taMatYSmin'] = 7.50e3                    #(MPa)
    # inp['taMatGTNrd'] = 0.80               #(Unitless) 0.0 < RD <= 1.0 (if RD=1.0 then it's Von Mises) #These values fit the initial Molnar yield surface
    # inp['taMatGTNq'] = [1.40,1.10,1.40**2.0]     #(Unitless) these are scaling factors: q1,q2,q3 (the proper value for q3 is q3 = q1**2.0) #These values fit the initial Molnar yield surface
    # #---------------------------------------------------------------------------------

    # #------------------------fitting Molnar 2017--------------------------------------
    # inp['taMatYSmin'] = 8.75e3                    #(MPa)
    # inp['taMatGTNrd'] = 0.95               #(Unitless) 0.0 < RD <= 1.0 (if RD=1.0 then it's Von Mises) #These values fit the initial Molnar yield surface
    # inp['taMatGTNq'] = [7.50,1.10,7.50**2.0]     #(Unitless) these are scaling factors: q1,q2,q3 (the proper value for q3 is q3 = q1**2.0) #These values fit the initial Molnar yield surface
    # #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #CSV File Section (activate for parametric studies which read inputs from CSV files)
    #Don't do two csv files at once, it causes errors in variable overwriting.
    #---------------------------------------------------------------------------------
    inp['csvMethod'] = False
    inp['preSolve'] = False
    inp['csvFileNames'] = []
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    inp['csvFileNames'].append(r'C:\Abaqus\WorkingFiles\csvInputDecks\A_Test_Junk.csv')
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # inp['csvFileNames'].append(r'C:\Abaqus\WorkingFiles\csvInputDecks\pub01b_BuiltInMat_2019-11-26a.csv')
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Calls the functions which build the FEA model
    #---------------------------------------------------------------------------------
    if inp['csvMethod']: input_csv_prescript(inp)
    else: run_input_script(inp)

    return(0)

#-----------------------------------------------------------------------

if __name__ == "__main__":

    from sys import exit, argv

    # exit(main(argv))

    main(argv)

#-----------------------------------------------------------------------