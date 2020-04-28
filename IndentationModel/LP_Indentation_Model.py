#-----------------------------------------------------------------------

def print_system_units(*args,**kwargs):

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

def run_plugin_master(*args,**kwargs):

    print('\n\nRunning Abaqus Python Model-Building Plugin...\n')

    import os

    #-----------------------------------------------------------------------

    inp = {}

    inp['moduleName'] = '%s\\abaqus_plugins\\IndentationModel\\Module_Indentation.py' %(os.path.expanduser('~'))

    #-----------------------------------------------------------------------

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

    # #-----------------------------------------------------------------------
    # odbBool = bool(kwargs.get('odbBool',False))
    # odbFileName = str(kwargs.get('odbFileName',''))
    # energyHistoryBool = bool(kwargs.get('energyHistoryBool',True))
    # workForceDistBool = bool(kwargs.get('workForceDistBool',True))
    # sortedStressBool = bool(kwargs.get('sortedStressBool',True))
    # #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Bring the dictionary in-line with other methods (so "Inputs" csv is consistent)
    #-----------------------------------------------------------------------
    inp['controlType'] = 'Displacement'
    inp['csvMethod'] = False
    inp['csvFileNames'] = None
    inp['preSolve'] = False
    #-----------------------------------------------------------------------

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
    indenter = importedLibrary.ASym_Indenter_Analysis(inp['taType'],inp['analysisType'],inp['jobName'])     
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
    #Writing inputs to CSV file
    #-----------------------------------------------------------------------
    import csv

    if ('csvMethod' in dict(inp)) and inp['csvMethod']: inp['csvName'] = inp['jobName'] + '_upg_Inputs' + '.csv'
    else: inp['csvName'] = inp['jobName'] + '_Inputs' + '.csv'

    with open(inp['csvName'], 'wb') as tempFile:

        csvWriter = csv.writer(tempFile)

        for key,value in sorted(inp.items()): csvWriter.writerow([key,value])
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    #Running class methods which build the model
    #-----------------------------------------------------------------------
    indenter.createElasticMaterials(indType=inp['indType'],taMatName=inp['taMatName'],taMatYM=inp['taMatYM'],taMatPR=inp['taMatPR'],taMatDens=inp['taMatDens'],taMatRayDamp=inp['taMatRayDamp'],indMatName=inp['indMatName'],indMatYM=inp['indMatYM'],indMatPR=inp['indMatPR'],indMatDens=inp['indMatDens'])

    indenter.createPlasticMaterials(taMatPlast=inp['taMatPlast'],taMatYSmin=inp['taMatYSmin'],taMatGTNrd=inp['taMatGTNrd'],taMatGTNq=inp['taMatGTNq'],taMatDPCap=inp['taMatDPCap'],taMatDPCapHard=inp['taMatDPCapHard'],taMatKerm=inp['taMatKerm'],taMatMoln=inp['taMatMoln'])

    #----line of re-editing----

    indenter.createCylindricalTestArticle(inp['taScale']*inp['taSize'],inp['taScale']*inp['taSize'],inp['taPart'],tempFineMeshSize,inp['meshMultiples'],inp['meshAspectRatio'])

    indenter.createIndenter(inp['indDemiAngle'],indRadius=inp['indRadius'],indFlat=inp['indFlat'])

    indenter.createAssembly(inp['indType'],indenterOffset=0.0)

    indenter.createInteractions(inp['indType'],inp['indenterMass'],inp['contactFriction'],inp['contactType'])

    indenter.createSteps(inp['stepTime'],fieldIntervals=inp['fieldIntervals'],historyIntervals=inp['historyIntervals'],bulkViscosity=inp['bulkViscosity'])

    indenter.createLoadsBCs('Displacement',indenterDepth=inp['indenterDepth'])

    indenter.createRemeshing(remeshingParameters=inp['taMeshRefine'])

    indenter.createJob(inp['jobName'],inp['numCPU'])

    if ('biaxialPrestress' in dict(inp)) and not inp['biaxialPrestress'] == 0.0: indenter.createPredefinedField(inp['biaxialPrestress'])

    # mdb.jobs[inp['jobName']].writeInput(consistencyChecking=OFF)

    # mdb.jobs[inp['jobName']].submit(consistencyChecking=OFF)

    try: indenter.setView()
    except: print('Warning: Unable to set CAE view settings.')

    return(0)

#-----------------------------------------------------------------------
