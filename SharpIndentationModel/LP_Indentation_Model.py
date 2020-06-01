#-----------------------------------------------------------------------

def default_system_units(*args,**kwargs):

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

    return(0)

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

def run_input_script(inp):

    print('\n\nRunning Abaqus Python Script: Sharp Indentation Model...\n')

    #-----------------------------------------------------------------------
    # Changing options if a "PreSolve" is being performed
    #-----------------------------------------------------------------------
    if inp['anPreSolve']:

        inp['outpFieldInt'] = 100

        inp['meshDivider'] = 25.0

        inp['bcType'] = 'Displacement'

        inp['anJobName'] = inp['anJobName'] + '_pre'
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Loading module and making class instance
    #-----------------------------------------------------------------------
    import numpy as np
    from imp import load_source
    importedLibrary = load_source('Lib_Indenter_Combo', inp['anModuleName'])
    if inp['partTaType'] == 'AsymIndent': indenter = importedLibrary.ASym_Indenter_Analysis(inp['partTaType'],inp['anType'],inp['anJobName'])
    elif inp['partTaType'] == 'QsymIndent': indenter = importedLibrary.QSym_Indenter_Analysis(inp['partTaType'],inp['anType'],inp['anJobName'])
    elif inp['partTaType'] == 'HsymIndent': indenter = importedLibrary.HSym_Indenter_Analysis(inp['partTaType'],inp['anType'],inp['anJobName'])
    elif inp['partTaType'] == 'AsymPillar': indenter = importedLibrary.ASym_Pillar_Analysis(inp['partTaType'],inp['anType'],inp['anJobName'])
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Analysis options which vary based on analysis type
    #-----------------------------------------------------------------------
    if inp['anType'].startswith('Standard'):

        inp['anBulkViscosity'] = None

        inp['anTimeInc'] = None

        inp['contType'] = 'Node'

        inp['meshRemeshing'] = None

    elif inp['anType'].startswith('Explicit'):

        inp['contType'] = 'Surface'

        inp['matTaRayDamp'] = (0.020,0.0)       # Default: (0.020,0.0) , Other: (0.100,0.0)
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Alternative control types which require a "anPreSolve" to predict depth
    #-----------------------------------------------------------------------
    if inp['bcType'] == 'Force':

        inp['bcIndDepth'] = indenter.expectedDepthForce(inp['anJobName'],inp['indenterForce'])     # Function for "pre-solve" defining indenter force vs. depth

    elif inp['bcType'] == 'Energy':

        inp['bcIndDepth'] = indenter.expectedDepthEnergy(inp['anJobName'],indenterEnergy)          # Function for "pre-solve" defining indenter energy vs. depth

    elif inp['bcType'] == 'InitialVelocity':

        inp['bcIndDepth'] = indenter.expectedDepthVelocity(inp['anJobName'],indenterVelocity)      # This function has not been made
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Group of default options which are used if not specified earlier
    #-----------------------------------------------------------------------
    if not ('anBulkViscosity' in dict(inp)): inp['anBulkViscosity'] = (0.06,0.06,0.06,0.06)

    if not ('anCSVfileName' in dict(inp)): inp['anCSVfileName'] = None

    if not ('anTimeInc' in dict(inp)): inp['anTimeInc'] = 1.0e-00

    if not ('anTimeStep' in dict(inp)): inp['anTimeStep'] = (10.0e3,0.0e3,10.0e3,0.0e3)

    if not ('bcIndOffset' in dict(inp)): inp['bcIndOffset'] = 0.0

    if not ('bcTaPreStress' in dict(inp)): inp['bcTaPreStress'] = None

    if not ('matIndDensity' in dict(inp)): inp['matIndDensity'] = None

    if not ('matIndEYM' in dict(inp)): inp['matIndEYM'] = None

    if not ('matIndEPR' in dict(inp)): inp['matIndEPR'] = None

    if not ('matIndName' in dict(inp)): inp['matIndName'] = None

    if not ('matTaPsDPCap' in dict(inp)): inp['matTaPsDPCap'] = None

    if not ('matTaPsDPCapHard' in dict(inp)): inp['matTaPsDPCapHard'] = None

    if not ('matTaPsGTNq' in dict(inp)): inp['matTaPsGTNq'] = None

    if not ('matTaPsGTNrd' in dict(inp)): inp['matTaPsGTNrd'] = None

    if not ('matTaPsKerm' in dict(inp)): inp['matTaPsKerm'] = None

    if not ('matTaPsMoln' in dict(inp)): inp['matTaPsMoln'] = None

    if not ('matTaPsVM' in dict(inp)): inp['matTaPsVM'] = None

    if not ('matTaRayDamp' in dict(inp)): inp['matTaRayDamp'] = None

    if not ('meshAspectRatio' in dict(inp)): inp['meshAspectRatio'] = 1.0

    if not ('meshMultiples' in dict(inp)): inp['meshMultiples'] = (1.0, inp['meshDivider'], 3.0, 2.0)

    if not ('meshPartitions' in dict(inp)): inp['meshPartitions'] = (0.0,0.050,0.100,0.200,1.000)   # (unitless) fraction of OAL for refined mesh partitions

    if not ('meshRemeshing' in dict(inp)): inp['meshRemeshing'] = (1,2)

    if not ('partTaScale' in dict(inp)): inp['partTaScale'] = 1.0

    if not ('partTaSize' in dict(inp)): inp['partTaSize'] = 100.0 * inp['bcIndDepth']
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Calculations which are dependent on indenter depth
    #-----------------------------------------------------------------------
    tempEstIndentRadius = inp['bcIndDepth'] * np.tan(np.radians(inp['partIndDAngle']))

    tempEstContactLength = inp['bcIndDepth'] / np.cos(np.radians(inp['partIndDAngle']))

    tempFineMeshSize = inp['bcIndDepth'] / inp['meshDivider']

    if ('partIndMassAlt' in dict(inp)):

        print('Alternate Indenter Mass found: partIndMassAlt = %s' %(inp['partIndMassAlt']))

        inp['partIndMass'] = inp['partIndMassAlt']

        del inp['partIndMassAlt']

    else:

        tempIndenterMass = (3.51e-9) * (1.0/3.0)*np.pi*(1.0*inp['bcIndDepth'])**3.0 * (np.tan(np.radians(inp['partIndDAngle'])))**2.0 # (mg) mass of diamond in cone with height indent depth

        inp['partIndMass'] = 1e-01 * tempIndenterMass               # Scales indenter mass to cut back on noise in the system

    if ('partIndRadiusFraction' in dict(inp)): # Defines indenter tip radius as a fraction of indent depth

        print('Indenter Radius-by-Fraction found: partIndRadiusFraction = %s' %(inp['partIndRadiusFraction']))

        inp['partIndRadius'] = inp['partIndRadiusFraction']*inp['bcIndDepth']

        del inp['partIndRadiusFraction']
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Printing basic indent calculations
    #-----------------------------------------------------------------------
    print('Indenter mass: %0.3E (mg/um3)' %(inp['partIndMass']))
    print('Estimated Indent Depth: %.2f (um)' %(inp['bcIndDepth']))
    print('Estimated Indent Radius: %.2f (um)' %(tempEstIndentRadius))
    print('Estimated Contact Length: %.2f (um)' %(tempEstContactLength))
    print('Radial Size of Results-Zone: %.2f (um)' %(inp['partTaSize'] * inp['meshPartitions'][1]))
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Running class methods which build the model
    #-----------------------------------------------------------------------
    inp['matIndName'],inp['matIndEYM'],inp['matIndEPR'],inp['matIndDensity'] = indenter.createElasticMaterials(partIndType=inp['partIndType'],matTaName=inp['matTaName'],matTaEYM=inp['matTaEYM'],matTaEPR=inp['matTaEPR'],matTaDensity=inp['matTaDensity'],matTaRayDamp=inp['matTaRayDamp'],matIndName=inp['matIndName'],matIndEYM=inp['matIndEYM'],matIndEPR=inp['matIndEPR'],matIndDensity=inp['matIndDensity'])

    indenter.createPlasticMaterials(matTaPsModel=inp['matTaPsModel'],matTaPsVM=inp['matTaPsVM'],matTaPsGTNrd=inp['matTaPsGTNrd'],matTaPsGTNq=inp['matTaPsGTNq'],matTaPsDPCap=inp['matTaPsDPCap'],matTaPsDPCapHard=inp['matTaPsDPCapHard'],matTaPsKerm=inp['matTaPsKerm'],matTaPsMoln=inp['matTaPsMoln'])

    if inp['matTaPsModel'] != 'vonMises' and inp['matTaPsModel'] != 'GTN-pmp':

        inp['matTaPsVM'] = None

    if inp['matTaPsModel'] != 'GTN-pmp':

        inp['matTaPsGTNrd'] = None
        inp['matTaPsGTNq'] = None

    if inp['matTaPsModel'] != 'DP-Cap':

        inp['matTaPsDPCap'] = None
        inp['matTaPsDPCapH'] = None

    if inp['matTaPsModel'] != 'Kerm2008':

        inp['matTaPsKerm'] = None

    if inp['matTaPsModel'] != 'Moln2017':

        inp['matTaPsMoln'] = None

    #----line of re-editing----

    if inp['partTaType'] == 'AsymIndent':

        indenter.createCylindricalTestArticle(inp['partTaScale']*inp['partTaSize'],inp['partTaScale']*inp['partTaSize'],inp['meshPartitions'],tempFineMeshSize,inp['meshMultiples'],inp['meshAspectRatio'])

        indenter.createIndenter(inp['partIndDAngle'],partIndRadius=inp['partIndRadius'],partIndFlat=inp['partIndFlat'])

    elif inp['partTaType'] == 'QsymIndent':

        indenter.createQuarterTestArticle(inp['partTaScale']*inp['partTaSize'],inp['partTaScale']*inp['partTaSize'],inp['meshPartitions'],tempFineMeshSize,inp['meshMultiples'],inp['meshAspectRatio'])

        indenter.createQuarterIndenter(inp['partIndDAngle'],partIndRadius=inp['partIndRadius'],partIndFlat=inp['partIndFlat'])

    elif inp['partTaType'] == 'HsymIndent':

        indenter.createHalfTestArticle(inp['partTaScale']*inp['partTaSize'],inp['partTaScale']*inp['partTaSize'],inp['meshPartitions'],tempFineMeshSize,inp['meshMultiples'],inp['meshAspectRatio'])

        indenter.createHalfIndenter(inp['partIndDAngle'],partIndRadius=inp['partIndRadius'],partIndFlat=inp['partIndFlat'])

    elif inp['partTaType'] == 'CsymIndent':

        print("This isn't ready yet!")

    elif inp['partTaType'] == 'Full3DIndent':

        print("This isn't ready yet!")

    elif inp['partTaType'] == 'AsymPillar':

        indenter.createPillarTestArticle()

        indenter.createPillarIndenter()

    #-----------------------------------------------------------------

    indenter.createAssembly(inp['partIndType'])

    indenter.createInteractions(inp['partIndType'],inp['partIndMass'],inp['contFriciton'],inp['contType'])

    indenter.createSteps(inp['anTimeStep'],outpFieldInt=inp['outpFieldInt'],outpHistInt=inp['outpHistInt'],anBulkViscosity=inp['anBulkViscosity'])

    indenter.createLoadsBCs('Displacement',bcIndDepth=inp['bcIndDepth'])

    if inp['bcTaPreStress'] is not None and inp['bcTaPreStress'] != 0.0: indenter.createPredefinedField(inp['bcTaPreStress'])

    indenter.createRemeshing(remeshingParameters=inp['meshRemeshing'])

    indenter.createJob(inp['anJobName'],inp['anCPUs'],inpFile=inp['anCSV'])

    try: indenter.setView()
    except: print('Warning: Unable to set CAE view settings.')
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Writes input variables to CSV file: "All-Inputs"
    #-----------------------------------------------------------------------
    import csv

    if ('anCSV' in dict(inp)) and inp['anCSV']: tempCSVinputsName = inp['anJobName'] + '_upg_All-Inputs' + '.csv'
    else: tempCSVinputsName = inp['anJobName'] + '_All-Inputs' + '.csv'

    with open(tempCSVinputsName, 'wb') as tempFile:

        csvWriter = csv.writer(tempFile)

        for key,value in sorted(inp.items()): csvWriter.writerow([key,value])
    #-----------------------------------------------------------------------

    return(0)

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

def input_rsg_plugin_prescript(*args,**kwargs):

    print('\n\nRunning Abaqus RSG Plugin: Sharp Indentation Model...\n')

    import os

    #-----------------------------------------------------------------------
    # Creating "inp" dictionary and specifying module location and importing values from plugin kwargs
    #-----------------------------------------------------------------------
    inp = {}
    inp['anModuleName'] = '%s\\abaqus_plugins\\SharpIndentation\\Module_AbaqusFEA_Indentation.py' %(os.path.expanduser('~'))
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Importing values to "inp" dictionary from plugin kwargs
    #----------------------------------------------------------------------
    inp['partTaType'] = str(kwargs.get('partTaType','AsymIndent'))

    inp['anType'] = str(kwargs.get('anType','Standard - Quasi-Static'))

    inp['partIndType'] = str(kwargs.get('partIndType','Deformable'))
    inp['partIndDAngle'] = float(kwargs.get('partIndDAngle',70.3))
    inp['partIndRadius'] = float(kwargs.get('partIndRadius',0.0))
    inp['partIndFlat'] = float(kwargs.get('partIndFlat',0.0))

    inp['bcIndDepth'] = float(kwargs.get('bcIndDepth',5.0))
    inp['contFriciton'] = float(kwargs.get('contFriciton',0.0))

    inp['meshDivider'] = float(kwargs.get('meshDivider',50.0))
    inp['partTaScale'] = float(kwargs.get('partTaScale',1.0))

    inp['taMeshR1'] = int(kwargs.get('taMeshR1',1))
    inp['taMeshR2'] = int(kwargs.get('taMeshR2',2))
    inp['meshRemeshing'] = [inp['taMeshR1'],inp['taMeshR2']]
    del inp['taMeshR1']; del inp['taMeshR2'];

    inp['matIndName'] = str(kwargs.get('matIndName','Diamond'))
    inp['matIndEYM'] = float(kwargs.get('matIndEYM',1220e3))
    inp['matIndEPR'] = float(kwargs.get('matIndEPR',0.20))
    inp['matIndDensity'] = float(kwargs.get('matIndDensity',3.52e-9))

    inp['matTaName'] = str(kwargs.get('matTaName','a-SiO2'))
    inp['matTaEYM'] = float(kwargs.get('matTaEYM',70.0e3))
    inp['matTaEPR'] = float(kwargs.get('matTaEPR',0.15))
    inp['matTaDensity'] = float(kwargs.get('matTaDensity',2.20e-9))

    inp['matTaPsModel'] = str(kwargs.get('matTaPsModel','DP-Cap'))

    inp['matTaPsDPCap0'] = float(kwargs.get('matTaPsDPCap0',5500.0))
    inp['matTaPsDPCap1'] = float(kwargs.get('matTaPsDPCap1',10.0))
    inp['matTaPsDPCap2'] = float(kwargs.get('matTaPsDPCap2',0.85))
    inp['matTaPsDPCap3'] = float(kwargs.get('matTaPsDPCap3',0.0))
    inp['matTaPsDPCap4'] = float(kwargs.get('matTaPsDPCap4',0.01))
    inp['matTaPsDPCap5'] = float(kwargs.get('matTaPsDPCap5',1.0))

    inp['matTaPsDPCap'] =  (inp['matTaPsDPCap0'], inp['matTaPsDPCap1'], inp['matTaPsDPCap2'], inp['matTaPsDPCap3'], inp['matTaPsDPCap4'], inp['matTaPsDPCap5'])
    inp['matTaPsDPCapHard'] = ((4750.0, 0.0),(8000.0, 0.005),(9800.0, 0.0123),(12000.0, 0.0427),(13600.0, 0.0735),(14600.0, 0.117),(15500.0, 0.135),(18100.0, 0.1655),(20000.0, 0.188),(25000.0, 0.195),(50000.0, 0.196)) #Hardening from Molnar 2017, Rouxel 2008, and Deschamps 2013
    del inp['matTaPsDPCap0']; del inp['matTaPsDPCap1']; del inp['matTaPsDPCap2']; del inp['matTaPsDPCap3']; del inp['matTaPsDPCap4']; del inp['matTaPsDPCap5'];

    inp['matTaPsVM'] = float(kwargs.get('matTaPsVM',7.50e3))
    inp['matTaPsGTNrd'] = float(kwargs.get('matTaPsGTNrd',0.85))
    inp['matTaPsGTNq1'] = float(kwargs.get('matTaPsGTNq1',0.90))
    inp['matTaPsGTNq2'] = float(kwargs.get('matTaPsGTNq2',0.90))

    inp['matTaPsGTNq'] = (inp['matTaPsGTNq1'],inp['matTaPsGTNq2'],inp['matTaPsGTNq1']**2.0)
    del inp['matTaPsGTNq1']; del inp['matTaPsGTNq2'];

    inp['taMatK1'] = float(kwargs.get('taMatK1',6500.0))
    inp['taMatK2'] = float(kwargs.get('taMatK2',-11500.0))
    inp['taMatK3'] = float(kwargs.get('taMatK3',100000.0))

    inp['matTaPsKerm'] = (inp['taMatK1'],inp['taMatK2'],inp['taMatK3'])
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

    inp['matTaPsMoln'] = (inp['taMatM1'],inp['taMatM2'],inp['taMatM3'],inp['taMatM4'],inp['taMatM5'],inp['taMatM6'],inp['taMatM7'],inp['taMatM8'],inp['taMatM9'])
    del inp['taMatM1']; del inp['taMatM2']; del inp['taMatM3']; del inp['taMatM4']; del inp['taMatM5']; del inp['taMatM6']; del inp['taMatM7']; del inp['taMatM8']; del inp['taMatM9'];

    inp['outpFieldInt'] = int(kwargs.get('outpFieldInt',50))
    inp['outpHistInt'] = int(kwargs.get('outpHistInt',50))

    inp['anJobName'] = str(kwargs.get('anJobName','Sharp_Indentation'))
    inp['anCPUs'] = int(kwargs.get('anCPUs',4))
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Bring the dictionary in-line with other methods (so "Inputs" csv is consistent)
    #-----------------------------------------------------------------------
    inp['bcType'] = 'Displacement'
    inp['anCSV'] = False
    inp['anPreSolve'] = False
    #-----------------------------------------------------------------------

    run_input_script(inp)

    return(0)

#-----------------------------------------------------------------------

# End of Plugin

#-----------------------------------------------------------------------

def input_csv_prescript(inp):

    print('\n\nRunning Abaqus Python Script: CSV Pre-Script for Sharp Indentation Model...\n')

    multiVarNames = ['anBulkViscosity','anTimeStep','meshMultiples','meshPartitions','meshRemeshing','matTaPsKerm','matTaPsMoln','matTaPsDPCap','matTaPsDPCapH','matTaPsGTNq']

    import os, csv

    os.chdir(r"C:\Abaqus\Mio\TransferOutbound")

    print >> sys.__stdout__, ('\n')

    for fileName in inp['anCSVfileName']:

        with open(fileName, 'rb') as tempFile:

            csvReader = csv.reader(tempFile)

            dataKeys = next(csvReader)

            for csvRow in csvReader:

                for i in range(len(dataKeys)):

                    if dataKeys[i] in multiVarNames:

                        inp[dataKeys[i]] = [float(entry) for entry in csvRow[i].lstrip('(').rstrip(')').split(',')]

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

def main(*args,**kwargs):

    import numpy as np

    #-----------------------------------------------------------------------
    # Controls how "abaqus.rpy" reports geometry selections: coordinates or index
    #-----------------------------------------------------------------------
    # try: session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
    try: session.journalOptions.setValues(replayGeometry=COMPRESSEDINDEX, recoverGeometry=COMPRESSEDINDEX)
    except: pass
    #-----------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # Setting up input "inp" dictionary and defining module file
    #---------------------------------------------------------------------------------
    inp = {}
    inp['anModuleName'] = r'C:\Abaqus\Module_AbaqusFEA_Indentation.py'
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # Analysis Type, Output Frequencies, Step Controls, Solver Cores, Jobname
    #---------------------------------------------------------------------------------
    # inp['anType'] = 'Standard - Static'
    inp['anType'] = 'Standard - Quasi-Static'
    # inp['anType'] = 'Explicit - Mass Scaling'
    #---------------------------------------------------------------------------------
    # inp['anTimeStep'] = (10.0e3,0.0e3,10.0e3,0.0e3)   # (ms) Step times for Indent, Dwell-Loaded, Remove, Dwell-Unloaded steps (Dwell is ignored for Standard)
    # inp['anTimeInc'] = 1.0e-00                        # (ms) Target increment time for explicit mass scaling technique
    inp['outpFieldInt'] = 50                            # (Unitless) Integer number of field results #1
    inp['outpHistInt'] = 50                             # (Unitless) Integer number of history results #50
    inp['anCPUs'] = 8                                   # Number of parallel CPUs used by solver
    #---------------------------------------------------------------------------------
    inp['anJobName'] = 'Indentation-Test_01-01'
    # inp['anJobName'] = 'Pillar-Test_01-01'
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    #Indenter: Geometry (and friction coefficient)
    #---------------------------------------------------------------------------------
    inp['partIndDAngle'] = 70.3                 # (degrees) Conical Equivalents: 42.3 (Cube-Corner), 56.3 (Middle), 70.3 (Vickers)
    inp['partIndRadius'] = 0.000                # (um) 0.0 creates a "Sharp Tip" Indenter (0.3 creates a 300nm radius indenter - "MicroStarTech")
    inp['partIndFlat'] = 0.000                  # (um) creates a flat point which has a radius into the angled indenter surface
    #---------------------------------------------------------------------------------
    inp['contFriciton'] = 0.00                  # (unitless)
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # Indenter: Type & Linear-Elastic Material Properties
    #---------------------------------------------------------------------------------
    inp['partIndType'] = 'Rigid'
    # inp['partIndType'] = 'Deformable'
    #---------------------------------------------------------------------------------
    # inp['matIndName'] = 'Diamond'             # Material name(s) for deformable indenters
    # inp['matIndName'] = 'Sapphire'
    #---------------------------------------------------------------------------------
    # inp['matIndName'] = 'Custom'
    # inp['matIndDensity'] = 1.00e-9
    # inp['matIndEYM'] = 1000e3
    # inp['matIndEPR'] = 0.15
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # Test Article: Type
    #---------------------------------------------------------------------------------
    inp['partTaType'] = 'AsymIndent'
    # inp['partTaType'] = 'QsymIndent'
    # inp['partTaType'] = 'HsymIndent'
    # inp['partTaType'] = 'CsymIndent'
    #---------------------------------------------------------------------------------
    # inp['partTaType'] = 'AsymPillar'
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # Test Article: Meshing and Re-Meshing
    #---------------------------------------------------------------------------------
    inp['meshDivider'] = 50.0                   # Default: 50.0
    # inp['meshRemeshing'] = (1,20)               # Explicit Adaptive Remeshing: Default (1,2) for Vickers, (1,20) for Cube-Corner & Pillar
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # Boundary Condition (i.e. Work Input Controls)
    #---------------------------------------------------------------------------------
    inp['bcType'] = 'Displacement'
    inp['bcIndDepth'] = 3.000                   # (um) Default: 3.000, Pillar Default: 1.000
    #---------------------------------------------------------------------------------
    # inp['bcType'] = 'Force'
    # inp['indenterForce'] = 1e6                  # (uN)
    #---------------------------------------------------------------------------------
    # inp['bcTaPreStress'] = 100.0                # (MPa) Bi-axial Pre-Stress in Test Article
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # Test Article: Linear-Elastic Material Properties
    #---------------------------------------------------------------------------------
    inp['matTaName'] = 'a-SiO2'
    #---------------------------------------------------------------------------------
    # Amorphous Si02 (Fused Silica) Elastic Properties and Density from: (Rouxel, Yoshida, 2017)
    inp['matTaEYM'] = 70.0e3                    # Young's Modulus (MPa)
    inp['matTaEPR'] = 0.15                      # Poisson's Ratio (Unitless)
    inp['matTaDensity'] = 2.20e-9               # Density (mg/um^3) or (kg/m^3 * 10^-12) or (g/cm^3 * 10^-9)
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # Test Article: Plastic Material Model and Parameters
    #---------------------------------------------------------------------------------
    # inp['matTaPsModel'] = 'vonMises'
    # inp['matTaPsModel'] = 'GTN-pmp'             # 'Gurson-Tvergaard-Needleman Porous Metal Plasticity'
    inp['matTaPsModel'] = 'DP-Cap'              # 'Drucker-Prager Cap wHardening'
    # inp['matTaPsModel'] = 'Kerm2008'            # 'Elliptical (Kermouche,2008)'
    # inp['matTaPsModel'] = 'Moln2017'            # 'Drucker-Prager-Cap (Molnar,2017)'
    #---------------------------------------------------------------------------------

    # #---------------------------------------------------------------------------------
    # # Fortran Subroutine Inputs for 'Elliptical (Kermouche,2008)' and 'Drucker-Prager-Cap (Molnar,2017)' Material
    # inp['matTaPsKerm'] = (6500.0, -11500.0, 100000.0)
    # inp['matTaPsMoln'] = (5.0, 5700.0, 5000.0, -3000.0, -0.196, 3.0, 4.0, -20000.0, 7000.0)
    # #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # "GTN-pmp" Material: Yield strength and Gurson-Tvegaard-Needlemean Parameters
    #---------------------------------------------------------------------------------

    # #------------------------fitting Kermouche 2008-----------------------------------
    # inp['matTaPsVM'] = 7.50e3                  # Yield Strength (MPa)
    # inp['matTaPsGTNrd'] = 0.85                    # Relative Density (Unitless) 0.0 < RD <= 1.0 (if RD=1.0 then it's Von Mises) #These values fit the initial Molnar yield surface
    # inp['matTaPsGTNq'] = (0.90,0.90,0.90**2.0)    # q-Parameters (Unitless) these are scaling factors: q1,q2,q3 (the proper value for q3 is q3 = q1**2.0) #These values fit the initial Molnar yield surface
    # #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # "DP-Cap" Material: Drucker-Prager Cap w/Hardening Parameters
    #---------------------------------------------------------------------------------

    # #------------------------fitting Kermouche 2008-----------------------------------
    # inp['matTaPsDPCap'] = (6500.0, 0.001, 1.75, 0.0, 0.05, 1.0)
    # inp['matTaPsDPCapHard'] = ((5600.0, 0.0),(8000.0, 0.005),(9800.0, 0.0123),(12000.0, 0.0427),(13600.0, 0.0735),(14600.0, 0.117),(15500.0, 0.135),(18100.0, 0.1655),(20000.0, 0.188),(25000.0, 0.195),(50000.0, 0.196)) #Hardening from Molnar 2017, Rouxel 2008, and Deschamps 2013
    # #---------------------------------------------------------------------------------

    #--------------------------fitting Molnar 2017------------------------------------
    inp['matTaPsDPCap'] =  (5500.0, 10.0, 0.85, 0.0, 0.01, 1.0)
    inp['matTaPsDPCapHard'] = ((4750.0, 0.0),(8000.0, 0.005),(9800.0, 0.0123),(12000.0, 0.0427),(13600.0, 0.0735),(14600.0, 0.117),(15500.0, 0.135),(18100.0, 0.1655),(20000.0, 0.188),(25000.0, 0.195),(50000.0, 0.196)) #Hardening from Molnar 2017, Rouxel 2008, and Deschamps 2013
    #---------------------------------------------------------------------------------

    # #------------------------fitting Bruns 2020---------------------------------------
    # inp['matTaPsDPCap'] =  (7500.0, 1e-04, 1.067, 0.000, 0.0, 1.0)
    # inp['matTaPsDPCapHard'] = ((8000.0, 0.000),(9800.0, 0.0123),(12000.0, 0.0427),(13600.0, 0.0735),(14600.0, 0.117),(15500.0, 0.135),(18100.0, 0.1655),(20000.0, 0.188),(25000.0, 0.195),(50000.0, 0.196)) #Hardening from Molnar 2017, Rouxel 2008, and Deschamps 2013
    # #---------------------------------------------------------------------------------

    # #------------------------replicating Bruns 2020---------------------------------------
    # inp['matTaPsDPCap'] =  (7500.0, 1e-04, 1.066, 0.000, 0.0, 1.0)
    # inp['matTaPsDPCapHard'] = [[8000.0,0.00]]
    # tempAlpha = 21.0; tempBeta = 4059.0; tempP0 = 1.7
    # for pValue in np.linspace(9.0,30.0,22):
        # # print pValue
        # normDp = ( ((tempAlpha)/(1.0+tempBeta*np.exp(-pValue/tempP0))) - ((tempAlpha)/(1.0+tempBeta)) ) / 100.0
        # # print normDp
        # epsilonPV = np.abs(np.log((1.0)/(normDp+1.0)))
        # # print epsilonPV
        # inp['matTaPsDPCapHard'].append([pValue*1e3,epsilonPV])
    # for value in inp['matTaPsDPCapHard']: print value
    # #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # CSV File Section (activate for parametric studies which read inputs from CSV files)
    #---------------------------------------------------------------------------------
    inp['anCSV'] = False
    inp['anPreSolve'] = False
    #---------------------------------------------------------------------------------
    if inp['anCSV']: inp['anCSVfileName'] = [r'C:\Abaqus\WorkingFiles\csvInputDecks\Test_MultiRun_File_01-01.csv']
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # Calls the functions which build the FEA model
    #---------------------------------------------------------------------------------
    if inp['anCSV']: input_csv_prescript(inp)
    else: run_input_script(inp)

    return(0)

#-----------------------------------------------------------------------

if __name__ == "__main__":

    from sys import exit, argv

    main(argv)