#-----------------------------------------------------------------------

def run_output_script(outp):

    print('\n\nRunning Abaqus Python Script: Sharp Indentation Output...\n')

    #-----------------------------------------------------------------------
    #Loading modules
    #-----------------------------------------------------------------------
    from imp import load_source
    importedLibrary = load_source('Lib_Indenter_Combo', outp['moduleName'])
    from abaqusConstants import CENTROID
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    clSetName = 'RESULTS_CL_SET'            #Depricated: 'RES_THETA0_SET'
    surfSetName = 'RESULTS_SURF_SET'        #Depricated: 'RES_THETA90_SET'
    rfSetName = 'BASE_SET'                  #Depricated: 'RESULTS_RF_SET'
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    if outp['directoryMethod']:

        from os import listdir

        outp['odbPath'] = [(outp['odbDirectory']+'\\'+fileName) for fileName in listdir(outp['odbDirectory']) if fileName.endswith('.odb')]

    else:

        outp['odbPath'] = [outp['odbPath']]

    outp['indenterOutput'] = []             #Creates a list of ODB files (allows for requesting outputs from multiple ODBs)

    for i in range(len(outp['odbPath'])):

        outp['indenterOutput'].append(importedLibrary.Indentation_Output(outp['odbPath'][i],readOnly=True))
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    for i in range(len(outp['indenterOutput'])):

        # #-----------------------------------------------------------------------
        # #This line prints all the results keys for field outputs
        # for key in outp['indenterOutput'][i].odb.steps[outp['indenterOutput'][i].odb.steps.keys()[-2]].frames[-1].fieldOutputs.keys(): print key
        # #-----------------------------------------------------------------------
        # #This line prints the step names for output database processing
        # print('\nLoad Step Name: "%s", Unload Step Name: "%s"\n' %(outp['indenterOutput'][i].odb.steps.keys()[-2],outp['indenterOutput'][i].odb.steps.keys()[-1]))
        # #-----------------------------------------------------------------------

        #-----------------------------------------------------------------------
        #This outputs the reaction force, displacement, and work from their multiplication; along with the "history" internal energy and work values, for comparisson to experimental data
        #The errorFlag indicates whether or not the analyses finished and the full set of output scripts can be run (on a properly finished analysis)
        #-----------------------------------------------------------------------

        if outp['indenterOutput'][i].odb.steps[outp['indenterOutput'][i].odb.steps.keys()[0]].procedure.endswith('EXPLICIT'):

            errorFlag = outp['indenterOutput'][i].WorkForceDist(instanceNameRF=None,nodeSetNameRF='MSET-1',instanceNameU=None,nodeSetNameU='MSET-1',fileNameSuffix='_Ind')

        else:

            errorFlag = outp['indenterOutput'][i].WorkForceDist(instanceNameRF='TEST_ARTICLE-1',nodeSetNameRF='BASE_SET',instanceNameU=None,nodeSetNameU='MSET-1',fileNameSuffix='_Base')

        #-----------------------------------------------------------------------

        if not errorFlag and not outp['odbPath'][i].endswith('_pre.odb'):

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

            if outp['boolAreaPlastic']:

                # This creates a list of element centroid locations which have a max absolute PE strain above a specified limit (it shows you the plasticly deformed zone)
                outp['indenterOutput'][i].UnsortedPlasticZone(stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],frameNumber=-1,instanceName='TEST_ARTICLE-1',setName='MAT_PLASTIC_SET', resultName='PE', specialLocation=CENTROID, limitPE=1e-05, limitType='lower', writeCSV=True)

            if outp['boolAreaS22']:

                # This outputs Stress Components which have a max absolute PE strain below a specified limit (it is useful for finding a max. S22 outside the center-line and surface)
                outp['indenterOutput'][i].UnsortedPlasticZone(stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],frameNumber=-1,instanceName='TEST_ARTICLE-1',setName='MAT_PLASTIC_SET', resultName='S22', limitResult=50.0, limitTypeResult='lower', specialLocation=CENTROID, limitPE=2e-03, limitType='upper', writeCSV=True)

            # outp['indenterOutput'][i].NoCoordResults(stepName=outp['indenterOutput'][i].odb.steps.keys()[-1],instanceName='TEST_ARTICLE-1',setName='MAT_PLASTIC_SET', resultName='PE', includePE=True, writeCSV=True)

            #-----------------------------------------------------------------------

        else:

            print('\n\nSkipping full processing of incomplete analysis odb:\n     %s\n\n' %(outp['odbPath'][i]))

    if outp['odbDirectory'] == r'C:\Abaqus\Mio\TransferInbound':

        from subprocess import call

        call(['python', r'C:\Abaqus\WorkingFiles\Mio\Mio_Local_Sort_oldODB_Files_rev2018-09-12a.py'])

    return(0)

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

def output_rsg_plugin_prescript(*args,**kwargs):

    print('\n\nRunning Abaqus RSG Plugin: Sharp Indentation Output...\n')

    import os

    from abaqus import session

    #-----------------------------------------------------------------------

    outp = {}

    outp['moduleName'] = '%s\\abaqus_plugins\\SharpIndentation\\Module_AbaqusFEA_Indentation.py' %(os.path.expanduser('~'))

    outp['directoryMethod'] = bool(kwargs.get('directoryMethod',False))
    outp['odbDirectory'] = str(kwargs.get('odbDirectory',r'C:\Abaqus\Temp'))
    outp['odbPath'] = str(kwargs.get('odbPath',None))

    outp['boolEnergy'] = bool(kwargs.get('boolEnergy',False))
    outp['boolOrthoStress'] = bool(kwargs.get('boolOrthoStress',False))
    outp['boolSurfTop'] = bool(kwargs.get('boolSurfTop',False))

    outp['boolIndVol'] = bool(kwargs.get('boolIndVol',False))
    outp['boolContVect'] = bool(kwargs.get('boolContVect',False))
    outp['boolNorm'] = bool(kwargs.get('boolNorm',False))

    outp['boolLode'] = bool(kwargs.get('boolLode',False))
    outp['boolInvStress'] = bool(kwargs.get('boolInvStress',False))
    outp['boolDensity'] = bool(kwargs.get('boolDensity',False))

    outp['boolAreaInvariants'] = bool(kwargs.get('boolAreaInvariants',False))
    outp['boolAreaPlastic'] = bool(kwargs.get('boolAreaPlastic',False))
    outp['limitPE'] = float(kwargs.get('limitPE',1e-05))
    outp['boolAreaS22'] = bool(kwargs.get('boolAreaS22',False))

    closeODBool = str(kwargs.get('closeODBool',False))

    #-----------------------------------------------------------------------

    run_output_script(outp)

    if closeODBool:

        try: session.odbs[outp['odbPath'][-1]].close()
        except: print('Failed to close odb file: %s'%(outp['odbPath'][-1]))

    return(0)

#-----------------------------------------------------------------------

# End of Plugin

#-----------------------------------------------------------------------

def main(*args,**kwargs):

    outp = {}

    outp['moduleName'] = r'C:\Abaqus\Module_AbaqusFEA_Indentation.py'

    #-----------------------------------------------------------------------
    # Directory or Individual File: comment out all directories to run on individual file
    #-----------------------------------------------------------------------
    outp['odbDirectory'] = r'C:\Abaqus\Temp'
    # outp['odbDirectory'] = r'C:\Abaqus\Mio\TransferInbound'
    #-----------------------------------------------------------------------
    # outp['odbPath'] = r'C:\Abaqus\Temp\Indentation-Test_01-01.odb'
    #-----------------------------------------------------------------------

    #-----------------------------------------------------------------------
    outp['boolEnergy'] = True
    outp['boolContVect'] = True
    outp['boolOrthoStress'] = True
    outp['boolSurfTop'] = True
    #-----------------------------------------------------------------------
    outp['boolIndVol'] = True
    outp['boolNorm'] = True
    #-----------------------------------------------------------------------
    outp['boolDensity'] = True
    outp['boolInvStress'] = True
    #-----------------------------------------------------------------------
    outp['boolAreaInvariants'] = False
    outp['boolAreaPlastic'] = False
    outp['boolAreaS22'] = False
    #-----------------------------------------------------------------------

    outp['limitPE'] = None #Sets the PE limit, currently, just for plugin.

    if 'odbDirectory' in outp.keys():

        outp['directoryMethod'] = True

    else:

        outp['directoryMethod'] = False

        outp['odbDirectory'] = None

    run_output_script(outp)

    return(0)

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

if __name__ == "__main__":

    from sys import exit, argv

    main(argv)