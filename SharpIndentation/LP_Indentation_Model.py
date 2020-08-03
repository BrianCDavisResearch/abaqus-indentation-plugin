#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Copyright 2020 Brian C. Davis
#--------------------------------------------------------------------------------------------------

def default_system_units(*args,**kwargs):

    print('\n\n')
    print('#------------------------------------------')
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
    print('#Energy -> picoJoule (uN*um = J*10^-12 = pJ)')
    print('\n\n')

    return(None)

#-----------------------------------------------------------------------

def model_script(inp):

    print('\n\nRunning Abaqus Python Script: Sharp Indentation Model...\n')

    #-----------------------------------------------------------------------
    # Loading module and making class instance
    #-----------------------------------------------------------------------
    import imp, numpy as np
    # from imp import load_source
    importedLibrary = imp.load_source('Lib_Indenter_Combo', inp['anModuleFileName'])
    #-----------------------------------------------------------------------
    if inp['partTaType'] == 'AsymIndent': indenter = importedLibrary.ASym_Indenter_Analysis(inp['partTaType'],inp['anType'])
    elif inp['partTaType'] == 'QsymIndent': indenter = importedLibrary.QSym_Indenter_Analysis(inp['partTaType'],inp['anType'])
    elif inp['partTaType'] == 'HsymIndent': indenter = importedLibrary.HSym_Indenter_Analysis(inp['partTaType'],inp['anType'])
    elif inp['partTaType'] == 'AsymPillar': indenter = importedLibrary.ASym_Pillar_Analysis(inp['partTaType'],inp['anType'])
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Analysis options which vary based on Analysis Type and Boundary Condition Type
    #-----------------------------------------------------------------------
    if inp['anPreSolve']:

        inp['outpFieldInt'] = 100

        inp['meshDivider'] = 25.0

        inp['bcType'] = 'Displacement'

        inp['anJobName'] = inp['anJobName'] + '_pre'

    #-----------------------------------------------------------------------

    if inp['bcType'] == 'Force':

        inp['bcIndDepth'] = indenter.expectedDepthForce(anJobName=inp['anJobName'],bcIndForce=inp['bcIndForce'])        # Function for "pre-solve" with indenter force vs. depth

    elif inp['bcType'] == 'Energy':

        inp['bcIndDepth'] = indenter.expectedDepthEnergy(anJobName=inp['anJobName'],bcIndEnergy=inp['bcIndEnergy'])     # Function for "pre-solve" with indenter energy vs. depth

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
    # Default options which are used if not specified earlier
    #-----------------------------------------------------------------------
    if not ('anBulkViscosity' in dict(inp)): inp['anBulkViscosity'] = (0.06,0.06,0.06,0.06)

    if not ('anCSVfileName' in dict(inp)): inp['anCSVfileName'] = None

    if not ('anRemoteLocalDir' in dict(inp)): inp['anRemoteLocalDir'] = None

    if not ('anRerunCSV' in dict(inp)): inp['anRerunCSV'] = False

    if not ('anRerunCSVfileName' in dict(inp)): inp['anRerunCSVfileName'] = None

    if not ('anFortranfileName' in dict(inp)): inp['anFortranfileName'] = None

    if not ('anTimeInc' in dict(inp)): inp['anTimeInc'] = 1.0e-00

    if not ('anTimeStep' in dict(inp)): inp['anTimeStep'] = (10.0e3,0.0e3,10.0e3,0.0e3)

    if not ('bcIndEnergy' in dict(inp)): inp['bcIndEnergy'] = None

    if not ('bcIndForce' in dict(inp)): inp['bcIndForce'] = None

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

    print('Indenter mass: %0.3E (mg/um3)' %(inp['partIndMass']))
    print('Estimated Contact Surface Radial Length: %.2f (um)' %(tempEstContactLength))
    print('Estimated Indent Depth: %.2f (um)' %(inp['bcIndDepth']))
    print('Estimated Indent Radius: %.2f (um)' %(tempEstIndentRadius))
    print('Radial Size of Results-Zone: %.2f (um)' %(inp['partTaSize'] * inp['meshPartitions'][1]))
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Configuring & Cleaning up Material Properties
    #-----------------------------------------------------------------------
    if (not inp['matTaPsModel'].startswith('von')) and (not inp['matTaPsModel'].startswith('PMP')):

        inp['matTaPsVM'] = None

    if not inp['matTaPsModel'].startswith('PMP'):

        inp['matTaPsGTNrd'] = None
        inp['matTaPsGTNq'] = None

    if not inp['matTaPsModel'].startswith('DPC'):

        inp['matTaPsDPCap'] = None
        inp['matTaPsDPCapHard'] = None

    if not inp['matTaPsModel'].startswith('Kerm'):

        inp['matTaPsKerm'] = None

    if not inp['matTaPsModel'].startswith('Moln'):

        inp['matTaPsMoln'] = None
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Running class methods which build the model
    #-----------------------------------------------------------------------
    indenter.createElasticMaterials(partIndType=inp['partIndType'],matIndDensity=inp['matIndDensity'],matIndEPR=inp['matIndEPR'],matIndEYM=inp['matIndEYM'],matIndName=inp['matIndName'],matTaDensity=inp['matTaDensity'],matTaEPR=inp['matTaEPR'],matTaEYM=inp['matTaEYM'],matTaName=inp['matTaName'],matTaRayDamp=inp['matTaRayDamp'])

    indenter.createPlasticMaterials(matTaPsModel=inp['matTaPsModel'],matTaPsVM=inp['matTaPsVM'],matTaPsGTNrd=inp['matTaPsGTNrd'],matTaPsGTNq=inp['matTaPsGTNq'],matTaPsDPCap=inp['matTaPsDPCap'],matTaPsDPCapHard=inp['matTaPsDPCapHard'],matTaPsKerm=inp['matTaPsKerm'],matTaPsMoln=inp['matTaPsMoln'])

    #-----------------------------------------------------------------

    if inp['partTaType'] == 'AsymIndent':

        indenter.createCylindricalTestArticle(inp['partTaScale']*inp['partTaSize'],inp['partTaScale']*inp['partTaSize'],inp['meshPartitions'],tempFineMeshSize,inp['meshMultiples'],inp['meshAspectRatio'])

        # indenter.createAlternateCylindricalTestArticle(inp['partTaScale']*inp['partTaSize'],inp['partTaScale']*inp['partTaSize'],inp['meshPartitions'],tempFineMeshSize,inp['meshMultiples'],inp['meshAspectRatio'])

        indenter.createIndenter(partIndDAngle=inp['partIndDAngle'],partIndRadius=inp['partIndRadius'],partIndFlat=inp['partIndFlat'])

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

    indenter.createAssembly(partIndType=inp['partIndType'])

    indenter.createInteractions(contFriciton=inp['contFriciton'],contType=inp['contType'],partIndType=inp['partIndType'],partIndMass=inp['partIndMass'])

    indenter.createSteps(anJobName=inp['anJobName'],anTimeStep=inp['anTimeStep'],anBulkViscosity=inp['anBulkViscosity'],outpFieldInt=inp['outpFieldInt'],outpHistInt=inp['outpHistInt'])

    indenter.createLoadsBCs(bcType='Displacement',bcIndDepth=inp['bcIndDepth'])

    if (inp['bcTaPreStress'] is not None) and (inp['bcTaPreStress'] != 0.0):

        indenter.createPredefinedField(bcTaPreStress=inp['bcTaPreStress'])

    indenter.createRemeshing(meshRemeshing=inp['meshRemeshing'])

    indenter.createJob(anJobName=inp['anJobName'],anCPUs=inp['anCPUs'],anFortranfileName=inp['anFortranfileName'],jobSubmit=False,inpFile=inp['anCSV'])

    try: indenter.setView()
    except: print('Warning: Unable to set CAE view settings.')
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    # Writes input variables to CSV file: "All-Inputs"
    #-----------------------------------------------------------------------
    import csv

    if inp['anCSV']: tempCSVinputsName = inp['anJobName'] + '_upg_All-Inputs.csv'
    else: tempCSVinputsName = inp['anJobName'] + '_All-Inputs.csv'

    with open(tempCSVinputsName, 'wb') as tempFile:

        csvWriter = csv.writer(tempFile)

        for key,value in sorted(inp.items()): csvWriter.writerow([key,value])
    #-----------------------------------------------------------------------

    return(None)

#-----------------------------------------------------------------------

def plugin_prescript(*args,**kwargs):

    print('\n\nRunning Abaqus Plugin: Sharp Indentation Model...\n')

    import os

    #-----------------------------------------------------------------------

    inp = {}

    inp['anModuleFileName'] = '%s/abaqus_plugins/SharpIndentation/Module_AbaqusFEA_Indentation.py' %(os.path.expanduser('~'))

    inp['anRerunCSV'] = bool(kwargs.get('anRerunCSV',None))
    inp['anRerunCSVfileName'] = str(kwargs.get('anRerunCSVfileName',None))

    #-----------------------------------------------------------------------

    if inp['anRerunCSV']:

        import csv

        multiVarNames = ['anBulkViscosity','anTimeStep','meshMultiples','meshPartitions','meshRemeshing','matTaPsKerm','matTaPsMoln','matTaPsDPCap','matTaPsDPCapHard','matTaPsGTNq']

        intVarNames = ['anCPUs','outpFieldInt','outpHistInt']

        with open(inp['anRerunCSVfileName'], 'rb') as tempFile:

            csvReader = csv.reader(tempFile)

            for csvRow in csvReader:

                if (csvRow[0] == 'anModuleFileName') or (csvRow[0] == 'anRerunCSV') or (csvRow[0] == 'anRerunCSVfileName'):

                    pass

                elif csvRow[0] == 'anJobName':

                    inp[csvRow[0]] = csvRow[1] + '-Rerun'

                elif csvRow[1] == '':

                    inp[csvRow[0]] = None

                elif csvRow[0] in multiVarNames:

                    if csvRow[0] == 'matTaPsDPCapHard':

                        tempInput = csvRow[1][2:-2].split('), (')

                        tempList = []

                        for tempValue in tempInput:

                            tempList.append((float(tempValue.split(',')[0]),float(tempValue.split(',')[1])))

                        inp[csvRow[0]] = tuple(tempList)

                    elif csvRow[0] == 'meshRemeshing':

                        tempList = [int(entry) for entry in csvRow[1].lstrip('(').rstrip(')').split(',')]

                    else:

                        tempList = [float(entry) for entry in csvRow[1].lstrip('(').rstrip(')').split(',')]

                    inp[csvRow[0]] = tuple(tempList)

                elif (csvRow[1] == 'True') or (csvRow[1] == 'TRUE'):

                    inp[csvRow[0]] = True

                elif (csvRow[1] == 'False') or (csvRow[1] == 'FALSE'):

                    inp[csvRow[0]] = False

                elif csvRow[0] in intVarNames:

                    try: inp[csvRow[0]] = int(csvRow[1])
                    except: inp[csvRow[0]] = csvRow[1]

                else:

                    try: inp[csvRow[0]] = float(csvRow[1])
                    except: inp[csvRow[0]] = csvRow[1]

    else:

        # inp['anBulkViscosity']
        inp['anCPUs'] = int(kwargs.get('anCPUs',None))
        # inp['anCSV']
        # inp['anCSVfileName']
        inp['anFortranfileName'] = str(kwargs.get('anFortranfileName',None))
        inp['anJobName'] = str(kwargs.get('anJobName',None))
        # inp['anModuleFileName']
        # inp['anPreSolve']
        # inp['anTimeInc']
        # inp['anTimeStep']
        inp['anType'] = str(kwargs.get('anType',None))

        inp['bcIndDepth'] = float(kwargs.get('bcIndDepth',None))
        # inp['bcIndForce']
        # inp['bcIndOffset']
        # inp['bcTaPreStress']
        # inp['bcType']

        inp['contFriciton'] = float(kwargs.get('contFriciton',None))
        # inp['contType']

        inp['matIndDensity'] = float(kwargs.get('matIndDensity',None))
        inp['matIndEPR'] = float(kwargs.get('matIndEPR',None))
        inp['matIndEYM'] = float(kwargs.get('matIndEYM',None))
        inp['matIndName'] = str(kwargs.get('matIndName',None))

        inp['matTaDensity'] = float(kwargs.get('matTaDensity',None))
        inp['matTaEPR'] = float(kwargs.get('matTaEPR',None))
        inp['matTaEYM'] = float(kwargs.get('matTaEYM',None))
        inp['matTaName'] = str(kwargs.get('matTaName',None))

        inp['matTaPsModel'] = str(kwargs.get('matTaPsModel',None))

        inp['matTaPsVM'] = float(kwargs.get('matTaPsVM',None))

        inp['matTaPsGTNq1'] = float(kwargs.get('matTaPsGTNq1',None))
        inp['matTaPsGTNq2'] = float(kwargs.get('matTaPsGTNq2',None))
        inp['matTaPsGTNrd'] = float(kwargs.get('matTaPsGTNrd',None))
        inp['matTaPsGTNq'] = (inp['matTaPsGTNq1'],inp['matTaPsGTNq2'],inp['matTaPsGTNq1']**2.0)
        del inp['matTaPsGTNq1']; del inp['matTaPsGTNq2'];

        inp['matTaPsDPCap0'] = float(kwargs.get('matTaPsDPCap0',None))
        inp['matTaPsDPCap1'] = float(kwargs.get('matTaPsDPCap1',None))
        inp['matTaPsDPCap2'] = float(kwargs.get('matTaPsDPCap2',None))
        inp['matTaPsDPCap3'] = float(kwargs.get('matTaPsDPCap3',None))
        inp['matTaPsDPCap4'] = float(kwargs.get('matTaPsDPCap4',None))
        inp['matTaPsDPCap5'] = float(kwargs.get('matTaPsDPCap5',None))
        inp['matTaPsDPCap'] =  (inp['matTaPsDPCap0'], inp['matTaPsDPCap1'], inp['matTaPsDPCap2'], inp['matTaPsDPCap3'], inp['matTaPsDPCap4'], inp['matTaPsDPCap5'])
        # inp['matTaPsDPCapHard'] = ((4750.0, 0.0),(8000.0, 0.005),(9800.0, 0.0123),(12000.0, 0.0427),(13600.0, 0.0735),(14600.0, 0.117),(15500.0, 0.135),(18100.0, 0.1655),(20000.0, 0.188),(25000.0, 0.195),(50000.0, 0.196)) #Hardening from Molnar 2017, Rouxel 2008, and Deschamps 2013
        del inp['matTaPsDPCap0']; del inp['matTaPsDPCap1']; del inp['matTaPsDPCap2']; del inp['matTaPsDPCap3']; del inp['matTaPsDPCap4']; del inp['matTaPsDPCap5'];

        inp['matTaPsKerm1'] = float(kwargs.get('matTaPsKerm1',None))
        inp['matTaPsKerm2'] = float(kwargs.get('matTaPsKerm2',None))
        inp['matTaPsKerm3'] = float(kwargs.get('matTaPsKerm3',None))
        inp['matTaPsKerm'] = (inp['matTaPsKerm1'],inp['matTaPsKerm2'],inp['matTaPsKerm3'])
        del inp['matTaPsKerm1']; del inp['matTaPsKerm2']; del inp['matTaPsKerm3'];

        inp['matTaPsMoln1'] = float(kwargs.get('matTaPsMoln1',None))
        inp['matTaPsMoln2'] = float(kwargs.get('matTaPsMoln2',None))
        inp['matTaPsMoln3'] = float(kwargs.get('matTaPsMoln3',None))
        inp['matTaPsMoln4'] = float(kwargs.get('matTaPsMoln4',None))
        inp['matTaPsMoln5'] = float(kwargs.get('matTaPsMoln5',None))
        inp['matTaPsMoln6'] = float(kwargs.get('matTaPsMoln6',None))
        inp['matTaPsMoln7'] = float(kwargs.get('matTaPsMoln7',None))
        inp['matTaPsMoln8'] = float(kwargs.get('matTaPsMoln8',None))
        inp['matTaPsMoln9'] = float(kwargs.get('matTaPsMoln9',None))
        inp['matTaPsMoln'] = (inp['matTaPsMoln1'],inp['matTaPsMoln2'],inp['matTaPsMoln3'],inp['matTaPsMoln4'],inp['matTaPsMoln5'],inp['matTaPsMoln6'],inp['matTaPsMoln7'],inp['matTaPsMoln8'],inp['matTaPsMoln9'])
        del inp['matTaPsMoln1']; del inp['matTaPsMoln2']; del inp['matTaPsMoln3']; del inp['matTaPsMoln4']; del inp['matTaPsMoln5']; del inp['matTaPsMoln6']; del inp['matTaPsMoln7']; del inp['matTaPsMoln8']; del inp['matTaPsMoln9'];

        # inp['matTaRayDamp']

        # inp['meshAspectRatio']
        inp['meshDivider'] = float(kwargs.get('meshDivider',None))
        # inp['meshMultiples']
        # inp['meshPartitions']

        inp['meshRemeshing1'] = int(kwargs.get('meshRemeshing1',None))
        inp['meshRemeshing2'] = int(kwargs.get('meshRemeshing2',None))
        inp['meshRemeshing'] = (inp['meshRemeshing1'],inp['meshRemeshing2'])
        del inp['meshRemeshing1']; del inp['meshRemeshing2'];

        inp['outpFieldInt'] = int(kwargs.get('outpFieldInt',None))
        inp['outpHistInt'] = int(kwargs.get('outpHistInt',None))

        inp['partIndDAngle'] = float(kwargs.get('partIndDAngle',None))
        inp['partIndFlat'] = float(kwargs.get('partIndFlat',None))
        # inp['partIndMass']
        inp['partIndRadius'] = float(kwargs.get('partIndRadius',None))
        inp['partIndType'] = str(kwargs.get('partIndType',None))

        inp['partTaScale'] = float(kwargs.get('partTaScale',None))
        # inp['partTaSize']
        # inp['partTaType']
        #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        # Bring the dictionary in-line with other methods (so "Inputs" csv is consistent)
        #-----------------------------------------------------------------------
        inp['anCSV'] = False
        inp['anPreSolve'] = False
        inp['bcType'] = 'Displacement'
        inp['partTaType'] = 'AsymIndent'
        #-----------------------------------------------------------------------
        if inp['partIndType'] == 'Rigid':

            inp['matIndDensity'] = None
            inp['matIndEPR'] = None
            inp['matIndEYM'] = None
            inp['matIndName'] = None
        #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        # DPC Hardening Pre-Script (limited options)
        #-----------------------------------------------------------------------
        if inp['matTaPsModel'] == 'DPC (Davis et al. 2020)':

            #--------------------------fitting Molnar 2017------------------------------------
            # inp['matTaPsDPCap'] =  (5500.0, 10.0, 0.85, 0.0, 0.01, 1.0)
            inp['matTaPsDPCapHard'] = ((4750.0, 0.0),(8000.0, 0.005),(9800.0, 0.0123),(12000.0, 0.0427),(13600.0, 0.0735),(14600.0, 0.117),(15500.0, 0.135),(18100.0, 0.1655),(20000.0, 0.188),(25000.0, 0.195),(50000.0, 0.196)) #Hardening from Molnar 2017, Rouxel 2008, and Deschamps 2013

        elif inp['matTaPsModel'] == 'DPC (Bruns et al. 2020)':

            import numpy as np
            # inp['matTaPsDPCap'] =  (7500.0, 1e-04, 1.066, 0.000, 0.0, 1.0)
            inp['matTaPsDPCapHard'] = [[8000.0,0.00]]
            tempAlpha = 21.0; tempBeta = 4059.0; tempP0 = 1.7
            for pValue in np.linspace(9.0,25.0,17):
                normDp = ( ((tempAlpha)/(1.0+tempBeta*np.exp(-pValue/tempP0))) - ((tempAlpha)/(1.0+tempBeta)) ) / 100.0
                epsilonPV = np.abs(np.log((1.0)/(normDp+1.0)))
                inp['matTaPsDPCapHard'].append([pValue*1e3,epsilonPV])
        #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    model_script(inp)
    #-----------------------------------------------------------------------

    return(None)

#-----------------------------------------------------------------------

# End of Plugin

#-----------------------------------------------------------------------