import serial
import matplotlib.pyplot as plt #modul d'affichage
import numpy as np #module de calcul
import math
###------------------------------------------------------------###
###---                  Acquisition                         ---###
###------------------------------------------------------------###
ser = serial.Serial('/dev/ttyUSB0', 9600)  # open serial port
print(ser.name)         # check which port was really used
#Variables used for recording
bool_received = 0
time_list = [] #List wich will contain time of the samples
hdop_list = [] #List wich will contain HDOP
Longitude_list = [] #List wich will contain Longitude for each sample
Latitude_list = [] #List wich will contain Latitude for each sample
Altitude_list = [] #List wich will contain Altitude for each sample
matrice_list =[] #List wich will contain X,Y,Z local for each sample
nb_sat_list =[] #List wich will contain the number of satellites for each sample
for line in ser: #Listing of the lines in the serial port
    #print the first time to wanr the user that data is transmitting via the serial port
    if bool_received == 0:
            print "Reception of Data ..."
            bool_received = 1
    split_list = line.split(',') #Seperation of the received string for further process
    if split_list[0] != 'END\r\n': #Xhile it is not the end of the file do :
        #Recalibration of th clock : add a 0 if secconds, minutes or hours ar less than 10
        #The goal is to have always the same format : HHMMSS
        if int(split_list[6]) < 10:
            split_list[6]='0'+split_list[6]
        if int(split_list[5]) < 10:
            split_list[5]='0'+split_list[5]
        if int(split_list[4]) < 10:
            split_list[4]='0'+split_list[4]
        time_list.append(split_list[4]+split_list[5]+split_list[6]) #Adding the time in the appropriate list
        Longitude_list.append(float(split_list[10])*np.pi/180) #Adding the Longitude in the appropriate list
        Latitude_list.append(float(split_list[11])*np.pi/180) #Adding the Latitude in the appropriate list
        Altitude_list.append(float(split_list[13])) #Adding the Altitude in the appropriate list
        hdop_list.append(split_list[15]) #Adding the HDOP in the appropriate list
        nb_sat_list.append(split_list[8]) #Adding the number of satellites in the appropriate list
    else: #End of the file
        ser.close() 
        break
###------------------------------------------------------------###
###---                  Processing                          ---###
###------------------------------------------------------------###
#Ellipsoide RGF93 parameters
a = 6378137.0
b = 6356752.314245179497563967
f = 1/298.257222101
e = np.sqrt(2*f - np.power(f,2.0))

#Paramaters used for M matrix (global2local)
lambda0 = (4+ 20.0/60 + 20.0/3600)*np.pi/180
phi0 = (20+ 20.0/60 + 20.0/3600)*np.pi/180
h0 = 0
N0 = a/(np.sqrt(1-np.power(e,2)*np.power(np.sin(phi0),2)));
M = np.matrix([[-np.sin(lambda0), np.cos(lambda0), 0], \
 [-np.sin(phi0)*np.cos(lambda0), -np.sin(phi0)*np.sin(lambda0),  np.cos(phi0)], \
 [np.cos(phi0)*np.cos(lambda0), np.cos(phi0)*np.sin(lambda0), np.sin(phi0)]])

xl_list = [] #List wich will contain X local for each sample
yl_list = [] #List wich will contain Y local for each sample
zl_list = [] #List wich will contain Z local for each sample

#transformation repere local
def polaire2carth(vect):
    #vect is a vector and as to be like  [Lambda, Phi, h] 1 column, 3 rows
    N = a/(np.sqrt(1-np.power(e,2)*np.power(np.sin(vect.item(1)),2.0)))
    x = (N+vect.item(2))*np.cos(vect.item(1))*np.cos(vect.item(0))
    y = (N+vect.item(2))*np.cos(vect.item(1))*np.sin(vect.item(0))
    z = (N*(1-np.power(e,2))+vect.item(2))*np.sin(vect.item(1))
    matrice = np.matrix([[x],[y],[z]])
    return matrice
def global2local(vect):
    #vect is a vector and as to be like  [x, y, z] 1 column, 3 rows
    Xl = M * np.matrix([[vect.item(0)-N0*np.cos(phi0)*np.cos(lambda0)], [vect.item(1)-N0*np.cos(phi0)*np.sin(lambda0)], [vect.item(2)-N0*(1-np.power(e,2))*np.sin(phi0)]])
    return Xl

#Equivalent of a do while loop :
#Initialization
matrice_list.append(np.matrix([[float(Longitude_list[0])],[float(Latitude_list[0])],[float(Altitude_list[0])]]))
matrice_list[0]=global2local(polaire2carth(matrice_list[0])) #Actualisation Lambda phi, h to xl, yl, zl (changeing the coordinate system)
matrice_cov=np.matrix([[matrice_list[0].item(0)],[matrice_list[0].item(1)],[matrice_list[0].item(2)]]) #Transformation of the list into a matrix
#Useful to apply the mean of the list and standard deviation (std)
xl_list.append(matrice_list[0].item(0))
yl_list.append(matrice_list[0].item(1))
zl_list.append(matrice_list[0].item(2))

for i in range(1,len(Longitude_list)):
    #Same as in Init bloc
    vector = np.matrix([[float(Longitude_list[i])],[float(Latitude_list[i])],[float(Altitude_list[i])]])
    matrice_list.append(vector)
    matrice_list[i]=global2local(polaire2carth(matrice_list[i]))
    xl_list.append(matrice_list[i].item(0))
    yl_list.append(matrice_list[i].item(1))
    zl_list.append(matrice_list[i].item(2))
    matrice_cov = np.concatenate((matrice_cov,[[matrice_list[i].item(0)],[matrice_list[i].item(1)],[matrice_list[i].item(2)]]), axis=1) #Concatenate in order to obtain the matrix

###----------------------------------------###
###--- standard deviation, Mean and Vary --###
###----------------------------------------###
#Local coordinates
meanX = np.mean(xl_list)
meanY = np.mean(yl_list)
meanZ = np.mean(zl_list)
#Polar coordinates
meanLong = np.mean(Longitude_list)
meanLat = np. mean(Latitude_list)
meanAlt = np.mean(Altitude_list)
ecarTypeX = np.std(xl_list) #Standard deviation on X
ecarTypeY = np.std(yl_list) #Standard deviation on Y
ecarTypeZ = np.std(zl_list) #Standard deviation on Z

#Print to the screen elements
print "HDOP :", hdop_list
print "NB Satellites :", nb_sat_list
print "TIme list :",time_list
print "Longitude moyenne", meanLong
print "Latitude moyenne", meanLat
print "Altitude moyenne", meanAlt
print "X local moyen: ", meanX
print "Y local moyen: ", meanY
print "Z local moyen: ", meanZ

print "ecarTypeX :", ecarTypeX
print "ecarTypeY :", ecarTypeY
print "ecarTypeZ :", ecarTypeZ

matrice_corrcoef = np.corrcoef(matrice_cov) #Pearson Correlation coefficient process
matrice_cov=np.cov(matrice_cov) #Covary beetween parameters
print "Matrice de covariance :\n",matrice_cov
print "Coefficient de correlation :\n",matrice_corrcoef

plt.title('x,y repere local Batiment') #You have to change the title in correlation with the file you receive
plt.xlabel('X local')
plt.ylabel('Ylocal')
plt.plot(xl_list, yl_list,'+')
plt.show()
plt.subplot(211)
plt.xlabel('Time')
plt.ylabel('HDOP values')
plt.title('Batiment')
plt.plot(time_list, hdop_list)
plt.yticks(np.arange(60,260,20))
plt.subplot(212)
plt.plot(time_list, nb_sat_list)
plt.xlabel('Time HHMMSS')
plt.yticks(np.arange(5, 12))
plt.ylabel('Nb_satellites')
plt.show()
