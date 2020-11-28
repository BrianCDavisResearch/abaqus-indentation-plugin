#--------------------------------------------------------------------------------------------------
# Copyright 2020 Brian C. Davis
#--------------------------------------------------------------------------------------------------

import imp, os, subprocess

#-----------------------------------------------------------------------

def default_system_units():

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

def results_script(outp):

    print('\n\nRunning Abaqus Python Script: Sharp Indentation Results...\n')

    #-----------------------------------------------------------------------
    #Loading modules
    #-----------------------------------------------------------------------
    try: from abaqus import session
    except ImportError: pass
    try: from abaqusConstants import CENTROID
    except ImportError: pass
    #-----------------------------------------------------------------------
    importedLibrary = imp.load_source('Lib_Indenter_Combo', outp['moduleName'])
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    clSetName = 'RESULTS_CL_SET'            #Depricated: 'RES_THETA0_SET'
    surfSetName = 'RESULTS_SURF_SET'        #Depricated: 'RES_THETA90_SET'
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    if os.path.isdir(outp['odbPath'][0]):

        outp['odbFileNames'] = [(outp['odbPath'][0]+'\\'+fileName) for fileName in os.listdir(outp['odbPath'][0]) if fileName.endswith('.odb')]

    elif os.path.isfile(outp['odbPath'][0]):

        outp['odbFileNames'] = outp['odbPath']

    else:

        print('Warning - Could not find a file or directory at path location:')
        print('  %s\n\n'%(outp['odbPath'][0]))

        outp['odbFileNames'] = []

    outp['indenterOutput'] = []                                 # Creates a list of ODB files (opens all first, allowing for requesting outputs from multiple ODBs)

    for i in range(len(outp['odbFileNames'])):

        outp['indenterOutput'].append(importedLibrary.Indentation_Output(outp['odbFileNames'][i],readOnly=True))

        # #-----------------------------------------------------------------------
        # #These lines print important imforation about the ODB file: step names and field output result keys
        # #-----------------------------------------------------------------------
        # print('\nLoad Step Name: "%s", Unload Step Name: "%s"\n' %(outp['indenterOutput'][i].odb.steps.keys()[-2],outp['indenterOutput'][i].odb.steps.keys()[-1]))
        # for key in outp['indenterOutput'][i].odb.steps[outp['indenterOutput'][i].odb.steps.keys()[-2]].frames[-1].fieldOutputs.keys(): print(key)
        # #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        #This outputs the reaction force, displacement, and work from their multiplication; along with the "history" internal energy and work values, for comparisson to experimental data
        #The errorFlag indicates whether or not the analyses finished and the full set of output scripts can be run (on a properly finished analysis)
        #-----------------------------------------------------------------------

        errorFlag1 = outp['indenterOutput'][i].WorkForceDist(instanceNameRF=None,nodeSetNameRF='MSET-1',instanceNameU=None,nodeSetNameU='MSET-1',fileNameSuffix='_Ind')
        errorFlag2 = outp['indenterOutput'][i].WorkForceDist(instanceNameRF='TEST_ARTICLE-1',nodeSetNameRF='BASE_SET',instanceNameU=None,nodeSetNameU='MSET-1',fileNameSuffix='_Base')

        # if outp['indenterOutput'][i].odb.steps[outp['indenterOutput'][i].odb.steps.keys()[0]].procedure.endswith('EXPLICIT'):

        #     errorFlag = outp['indenterOutput'][i].WorkForceDist(instanceNameRF=None,nodeSetNameRF='MSET-1',instanceNameU=None,nodeSetNameU='MSET-1',fileNameSuffix='_Ind')

        # else:

        #     errorFlag = outp['indenterOutput'][i].WorkForceDist(instanceNameRF='TEST_ARTICLE-1',nodeSetNameRF='BASE_SET',instanceNameU=None,nodeSetNameU='MSET-1',fileNameSuffix='_Base')

        #-----------------------------------------------------------------------

        if (not errorFlag1) and (not errorFlag2) and (not outp['odbFileNames'][i].endswith('_pre.odb')):

            #-----------------------------------------------------------------------
            # The following class methods are the "basic" csv outputs of indentation
            #-----------------------------------------------------------------------

            if outp['boolEnergy']:

                #Outputs "whole model" energy history-output variables to a CSV file (has the option to create some extra columns for ratios between energies)
                outp['indenterOutput'][i].WholeModelHistory(ratioValues=True)

            if outp['boolContVect']:

                #Calculates contact force vector components (x,y) at max. load (max. depth)
                outp['indenterOutput'][i].ContactForceVector()

            if outp['boolOrthoStress']:

                #Outputs orthogonal normal stress results (with optional PE columns) on the centerline and top surface  (reported at element centroid location)
                outp['indenterOutput'][i].GeneralResults(sortedResults=True,sortDirection=-2,stepName=outp['indenterOutput'][i].odb.steps.keys()[-2],instanceName='TEST_ARTICLE-1',setName=clSetName, resultName='S', specialLocation=CENTROID, includePE=True, writeCSV=True)
                outp['indenterOutput'][i].GeneralResults(sortedResults=True,sortDirection=-2,stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],instanceName='TEST_ARTICLE-1',setName=clSetName, resultName='S', specialLocation=CENTROID, includePE=True, writeCSV=True)
                outp['indenterOutput'][i].GeneralResults(sortedResults=True,sortDirection=1,stepName=outp['indenterOutput'][i].odb.steps.keys()[-2],instanceName='TEST_ARTICLE-1',setName=surfSetName, resultName='S', specialLocation=CENTROID, includePE=True, writeCSV=True)
                outp['indenterOutput'][i].GeneralResults(sortedResults=True,sortDirection=1,stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],instanceName='TEST_ARTICLE-1',setName=surfSetName, resultName='S', specialLocation=CENTROID, includePE=True, writeCSV=True)

            if outp['boolSurfTop']:

                #Outputs surface topology of the test article, for a visual plot of the divot shape
                outp['indenterOutput'][i].GeneralResults(sortedResults=True,sortDirection=1,stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],instanceName='TEST_ARTICLE-1',setName=surfSetName, resultName='U', writeCSV=True)

            #-----------------------------------------------------------------------
            # The following class methods are specific to indentation
            #-----------------------------------------------------------------------

            if outp['boolIndVol']:

                #Calculates indent volume, pileup volume, and total volume after the load has been removed (doesn't work that well)
                outp['indenterOutput'][i].VolumeDispCyl()

            if outp['boolNorm']:

                #Outputs "normalizer" variables to a CSV file (these variables are used in plotting to make dimensionless axes)
                outp['indenterOutput'][i].NormalizerVariables(writeCSV=True)

            #-----------------------------------------------------------------------
            # The following class methods are the "additional" csv outputs of indentation
            #-----------------------------------------------------------------------

            if outp['boolDensity']:

                if 'RD' in outp['indenterOutput'][i].odb.steps[outp['indenterOutput'][i].odb.steps.keys()[-2]].frames[-1].fieldOutputs.keys():

                    densityResult = 'RD'

                elif 'DENSITY' in outp['indenterOutput'][i].odb.steps[outp['indenterOutput'][i].odb.steps.keys()[-2]].frames[-1].fieldOutputs.keys():

                    densityResult = 'DENSITY'

                elif 'PEQC4' in outp['indenterOutput'][i].odb.steps[outp['indenterOutput'][i].odb.steps.keys()[-2]].frames[-1].fieldOutputs.keys():

                    densityResult = 'PEQC4'

                else:

                    densityResult = None

                if densityResult is not None:

                    outp['indenterOutput'][i].DensityGeneralResults(sortedResults=True,sortDirection=-2,stepName=outp['indenterOutput'][i].odb.steps.keys()[-2],instanceName='TEST_ARTICLE-1',setName=clSetName, resultName=densityResult, specialLocation=CENTROID, includePE=True, writeCSV=True)
                    outp['indenterOutput'][i].DensityGeneralResults(sortedResults=True,sortDirection=-2,stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],instanceName='TEST_ARTICLE-1',setName=clSetName, resultName=densityResult, specialLocation=CENTROID, includePE=True, writeCSV=True)
                    outp['indenterOutput'][i].DensityGeneralResults(sortedResults=True,sortDirection=1,stepName=outp['indenterOutput'][i].odb.steps.keys()[-2],instanceName='TEST_ARTICLE-1',setName=surfSetName, resultName=densityResult, specialLocation=CENTROID, includePE=True, writeCSV=True)
                    outp['indenterOutput'][i].DensityGeneralResults(sortedResults=True,sortDirection=1,stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],instanceName='TEST_ARTICLE-1',setName=surfSetName, resultName=densityResult, specialLocation=CENTROID, includePE=True, writeCSV=True)

            if outp['boolInvStress']:

                #Outputs principal stress results (with additional invariants and optional PE columns on the centerline and top surface (elements MUST HAVE one integration point)
                outp['indenterOutput'][i].StressInvariantResults(sortedResults=True,sortDirection=-2,stepName=outp['indenterOutput'][i].odb.steps.keys()[-2],instanceName='TEST_ARTICLE-1',setName=clSetName, specialLocation=CENTROID, includePE=True, writeCSV=True)
                outp['indenterOutput'][i].StressInvariantResults(sortedResults=True,sortDirection=-2,stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],instanceName='TEST_ARTICLE-1',setName=clSetName, specialLocation=CENTROID, includePE=True, writeCSV=True)
                outp['indenterOutput'][i].StressInvariantResults(sortedResults=True,sortDirection=1,stepName=outp['indenterOutput'][i].odb.steps.keys()[-2],instanceName='TEST_ARTICLE-1',setName=surfSetName, specialLocation=CENTROID, includePE=True, writeCSV=True)
                outp['indenterOutput'][i].StressInvariantResults(sortedResults=True,sortDirection=1,stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],instanceName='TEST_ARTICLE-1',setName=surfSetName, specialLocation=CENTROID, includePE=True, writeCSV=True)

            #-----------------------------------------------------------------------
            # These "additional" csv outputs take a long time to run, because they are for an area, not just a line
            #-----------------------------------------------------------------------

            if outp['boolAreaInvariants']:

                # This outputs the Stress Invariants, which is useful in making an Abaqus Rendulic Plane scatter plot (optional PE columns)
                outp['indenterOutput'][i].UnsortedStressInvariants(stepName=outp['indenterOutput'][i].odb.steps.keys()[-2],instanceName='TEST_ARTICLE-1',setName='MAT_PLASTIC_SET', resultName='S', includePE=True, writeCSV=True)
                outp['indenterOutput'][i].UnsortedStressInvariants(stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],instanceName='TEST_ARTICLE-1',setName='MAT_PLASTIC_SET', resultName='S', includePE=True, writeCSV=True)

            if outp['boolAreaS22']:

                 # This outputs Stress Components which have a max absolute PE strain below a specified limit (it is useful for finding a max. S22 outside the center-line and surface)
                outp['indenterOutput'][i].UnsortedResultsZone(stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],frameNumber=-1,instanceName='TEST_ARTICLE-1',setName='MAT_PLASTIC_SET', resultName='S22', limitResult=outp['boolAreaS22limit'], limitTypeResult='lower', specialLocation=CENTROID, limitPE=outp['boolAreaS22limitPE'], limitType='upper', writeCSV=True)

            if outp['boolAreaPlastic']:

                # This creates a list of element centroid locations which have a max absolute PE strain above a specified limit (it shows you the plasticly deformed zone)
                outp['indenterOutput'][i].UnsortedResultsZone(stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],frameNumber=-1,instanceName='TEST_ARTICLE-1',setName='MAT_PLASTIC_SET', resultName='PE', specialLocation=CENTROID, limitPE=outp['boolAreaPlasticlimitPE'], limitType='lower', writeCSV=True)

            # outp['indenterOutput'][i].NoCoordResults(stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],instanceName='TEST_ARTICLE-1',setName='MAT_PLASTIC_SET', resultName='PE', includePE=True, writeCSV=True)

            #-----------------------------------------------------------------------

        else:

            print('\n\nSkipping full processing of either "pre-analysis" or incomplete analysis, odb:\n     %s\n\n' %(outp['odbFileNames'][i]))

        if outp['closeODBool']:

            try:

                session.odbs[outp['odbFileNames'][i]].close()

            except UnboundLocalError:

                try:

                    outp['indenterOutput'][i].odb.close()

                except Exception:

                    print('Failed to close odb file: %s'%(outp['odbFileNames'][i]))

    del outp['indenterOutput']

    if outp['odbPath'][0] == outp['remoteLocalDir']:

        psCommand = 'python ' + r'C:\Abaqus\Module_AbaqusShell_Commands.py ' '--MioLocalSort'

        print('\n\n Running powershell command: "%s"\n\n' %(psCommand))

        psProcess = subprocess.Popen(['powershell.exe', '-Command', psCommand], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        psOutput = psProcess.communicate()[0]

        print(psOutput.decode('ascii'))

    print('\n\n...Completed Abaqus Python Script: Sharp Indentation Results.\n\n')

    return(None)

#-----------------------------------------------------------------------

def plugin_prescript(**kwargs):

    print('\n\nRunning Abaqus Plugin: Sharp Indentation Results...\n')

    #-----------------------------------------------------------------------

    outp = {}

    outp['moduleName'] = '%s\\abaqus_plugins\\SharpIndentation\\Module_AbaqusFEA_Indentation.py' %(os.path.expanduser('~'))

    #-----------------------------------------------------------------------

    outp['odbPath'] = str(kwargs.get('odbPath',None)).split(',')

    outp['boolEnergy'] = bool(kwargs.get('boolEnergy',False))

    outp['boolOrthoStress'] = bool(kwargs.get('boolOrthoStress',False))
    outp['boolInvStress'] = bool(kwargs.get('boolInvStress',False))
    outp['boolDensity'] = bool(kwargs.get('boolDensity',False))

    outp['boolSurfTop'] = bool(kwargs.get('boolSurfTop',False))
    outp['boolIndVol'] = bool(kwargs.get('boolIndVol',False))
    outp['boolContVect'] = bool(kwargs.get('boolContVect',False))
    outp['boolNorm'] = bool(kwargs.get('boolNorm',False))

    outp['boolAreaInvariants'] = bool(kwargs.get('boolAreaInvariants',False))
    outp['boolAreaS22'] = bool(kwargs.get('boolAreaS22',False))
    outp['boolAreaS22limitPE'] = float(kwargs.get('boolAreaS22limitPE',None))
    outp['boolAreaS22limit'] = float(kwargs.get('boolAreaS22limit',None))
    outp['boolAreaPlastic'] = bool(kwargs.get('boolAreaPlastic',False))
    outp['boolAreaPlasticlimitPE'] = float(kwargs.get('boolAreaPlasticlimitPE',None))

    outp['closeODBool'] = True

    outp['remoteLocalDir'] = None

    #-----------------------------------------------------------------------
    results_script(outp)
    #-----------------------------------------------------------------------

    return(None)

#-----------------------------------------------------------------------

# End of Plugin

#-----------------------------------------------------------------------