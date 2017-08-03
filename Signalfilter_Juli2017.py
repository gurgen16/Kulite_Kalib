'''
Created on 27.06.2017

@author: Schneider
'''

###################       USER  INPUT      #############################################################################
ASDFolderPath = "P:/FVV - Radialverdichter/09_Studenten/HIWI_Schneider/Kulitedaten_Rauschen"
FileNameList = ["N100PI520TV3LSDE229_0_001_MITTEL.asd"]
#FileNameList=[]
FilePathCalibrationSheet='P:/FVV - Radialverdichter/09_Studenten/HIWI_Schneider/Auswertung Kulites/CalibrationData.dat'
Pu=99982                # Ambient pressure [Pa]

#########################################################################################################################
def GetCalibrationData(KulitesName):
    CalibrationRefFileList = open(FilePathCalibrationSheet).readlines()
    CalibrationVec.append(int(1))
    for name in KulitesName:                                        # Every value for each Kulite is converted from mV->Pa with calibration Data     
        for i in range(1,len(CalibrationRefFileList)):              
            if int(CalibrationRefFileList[i].split("\t")[0])==int(name):                    # Search for Kulite number in calibration sheet and assign sensitivity
                CalibrationVec.append(round(float(CalibrationRefFileList[i].split("\t")[1]),4))      # Create vector with sensitivity data
    CalibrationVec.append(int(1))                                                         # Trigger signal is not converted from mV-->Pa
    if len(CalibrationVec)!=NumOfColumn:                                                    # Error if not all sensitivities are given in calibration sheet
        print "Not all Kulites sensitivities are given in file:\n "+FilePathCalibrationSheet+"\nProgramm will quit.\nCheck calibration file and also file format[KulitesNr+'\t'+value]!"
        quit()  
# --------------------------------------------------------------------------------------------------------------------------------------        
def GetKulitesName(RefFileList,NumKulites):
    for i in range(len(RefFileList)):
        if patternKULITENUM.search(RefFileList[i]):     # Get row in data sheet where Kulite-names are given
            num=i
            break
    for k in range(NumKulites):
        KulitesName.append(str(int(RefFileList[num].split("\t")[k+1].split("(")[0]))) # Get the name of every Kulite
    return(KulitesName);      


#################################################      PROGRMM START        ##########################################################
import numpy as np
import re
import time
import os
import glob
import scipy.signal as signal
from scipy import signal

print "START"
StartTime=time.time()

os.chdir(ASDFolderPath)                            # If FileNameList is empty get all asd-files from FolderPath
if not FileNameList:                                   
    for file in glob.glob("*.asd"):
        if not file.endswith("mod.asd"):            # Do not load modified asd files
            FileNameList.append(file)
os.chdir("../")


for CurrentFile in FileNameList:                    # Loop for every file name in FileNameList
    Header=""
    KulitesName=[]
    CalibrationVec=[]
    patternKULITENUM= re.compile('Kanal+\t+([a-zA-Z0-9_.-]+)')      # Search command to find the number(names) of used Kulites
    
    #------------------------------- Open .asd-file and  ---------------------------------------------------- 
    FilePath=ASDFolderPath + "/" + CurrentFile
    RefFileList = open(FilePath).readlines()
    NumOfColumn = 1 + RefFileList[20].count("\t")                   # Get number of columns
    NumOfKulites=NumOfColumn-2                                      # Get number of kulites
    KulitesName = GetKulitesName(RefFileList, NumOfKulites)
    #------------------------------- Delete empty rows and header ---------------------------------------------------- 
    for i in range(len(RefFileList)-1,0,-1):                # delete empty rows
        if RefFileList[i]=="\n":
            del RefFileList[i]
        else:
            break
    for i in range(len(RefFileList)):                       # Get first row with measurement data                    
        if RefFileList[0].startswith("0"):                  
            break
        else:
            Header+=(RefFileList[0])                        # Solve header in buffer, because header does not change for modified .asd-file
            del RefFileList[0]  
    
    #------------------------------- Matrix initialization -----------------------------------------------------------------
    NumOfRows=len(RefFileList)                              # Get number of rows
    GetCalibrationData(KulitesName)
    FilterOutMatrix=np.zeros((NumOfRows,NumOfColumn))       # 2D-Array [Time][filtered kulite signal]
    DataMatrix=[]
    
    for line in RefFileList:
        DataMatrix.append(line.replace(",", ".").split())  # Change comma to dot and separate different columns
    
    #------------------------------- Write data in python array -------------------------------------------------------
    for j in range(NumOfRows):
        FilterOutMatrix[j][0]=float(DataMatrix[j][0])     
        FilterOutMatrix[j][-1]=float(DataMatrix[j][-1]) 
        
    #------------------------------- Apply filter-------------------------------------------------------
    for i in range(NumOfKulites):
        CurrentKLData=np.zeros(NumOfRows)                               # Filter is applied for every single kulite.signal
        for j in range(NumOfRows):
            CurrentKLData[j]=DataMatrix[j][i+1]                         # Therefore data of every kulite is written in 1D-Array
        b, a = signal.ellip(4, 0.01, 120, 0.125)  #MIC:120   0.125             #Testen: Wn=0.55           # Filter to be applied.
        # scipy.signal.ellip(N, rp, rs, Wn) 
            # N:  The order of the filter.
            # rp: The maximum ripple [Ueberschwingung der Uebertragungsfunktion] allowed below unity gain in the passband. Specified in decibels, as a positive number.
            # rs: The minimum attenuation required in the stop band. Specified in decibels, as a positive number.
            # Wn: A scalar or length-2 sequence giving the critical frequencies. For elliptic filters, this is the point in the transition band at which the gain first drops below -rp. 
            #     For digital filters, Wn is normalized from 0 to 1, where 1 is the Nyquist frequency, pi radians/sample. (Wn is thus in half-cycles / sample.) For analog filters, Wn is an angular frequency (e.g. rad/s).
            #         eg: Wn=0,125 --> f=f_Nyquist*0,125=8f_Ny --> frequencies below 8*f_Ny are filtered
        FilterOutput = signal.filtfilt(b, a, CurrentKLData, padlen=50)  # filtered signal is presolved in FilterOutput
        for j in range(NumOfRows):
            FilterOutMatrix[j][i+1]=FilterOutput[j]                     # filtered Data is written in FilterOutMatrix which contains filtered data from all kulites
    
     #--------------------------   Write output file       -----------------------------------------------
    fobj_out = open(ASDFolderPath+"/"+CurrentFile.split(".asd")[0]+"_mod.asd","w")    # open .dat-file and write new .asd file
    fobj_out.write(Header)                                                      # Assume header from old .asd file
    for j in range(NumOfRows):                                                  # Add filtered data
        for i in range(NumOfColumn):
            fobj_out.write(str(float(FilterOutMatrix[j][i])).replace(".", ","))
            if not i==(NumOfColumn-1):
                fobj_out.write("\t")                                            # Separate data of kulites with tab
        fobj_out.write("\n")                                                    # Separate data for new time step with new line
    fobj_out.close()

###########################################################   GET EXECUTION TIME ########################################################
ExMIN, ExSEC= divmod(time.time()-StartTime, 60)                 # Get executed time in minutes and seconds                  
print "Execution time: "+str(ExMIN)+" minutes and "+str(ExSEC)+" seconds."
print "ENDE"