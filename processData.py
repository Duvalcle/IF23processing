import serial
import matplotlib.pyplot as plt
import numpy as np
import math
#import scipy

# GPSMesssage=Year,Month,Day,DateAge,HourMinutesSecondes,TimeAge,Satellites,
#             AgeSat,Longitude,Latitude,AgeLocation,Altitude,AgeAltitude,
#             HDOP,AgeHDOP,SentencesWithFix,FailedChecksum,PassedChecksum\n
#f = open('exemple','r')
#for line in f:
#    print(line(12))
#DataAge : nb milis depuis derniere mise a jour de l heure

#Faire la moyenne des estimations GPS en repere local
#Calcul de lecartype et de la variance a partir de cette position (std)
#Matrice de covariance (3,3)
#Coefficient de correlation cor coef
#var
#periode de 24h et quelques minutes faire les mesures toujours au meme moment de la journee


###------------------------------------------------------------###
###---                  Acquisition                         ---###
###------------------------------------------------------------###
ser = serial.Serial('/dev/ttyUSB0', 9600)  # open serial port
print(ser.name)         # check which port was really used
#Variables used for recording
bool_received = 0
time_list = []
hdop_list = []
Longitude_list = []
Latitude_list = []
Altitude_list = []
matrice_list =[]
for line in ser:
    if bool_received == 0:
            print "Reception of Data ..."
            bool_received = 1
    split_list = line.split(',')
    if split_list[0] != 'END\r\n':
        #'Y : ', split_list[0], 'M : ', split_list[1] ,'D : ', split_list[2],\
        if int(split_list[6]) < 10:
            split_list[6]='0'+split_list[6]
        time_list.append(split_list[4]+split_list[5]+split_list[6])
        Longitude_list.append(split_list[10])
        Latitude_list.append(split_list[11])
        Altitude_list.append(split_list[13])
        hdop_list.append(split_list[15])

        #print split_list[4],'h',split_list[5],',',split_list[6], ' : ', \
        #'Nb Sat : ', split_list[8], '; Long : ', split_list[10], '; Lat : ', split_list[11],\
        #'; Alt : ', split_list[13]

    else:
        break
#print 'T : ',time_list
#print 'Long :',Longitude_list
#print 'Lat :', Latitude_list
#print 'Alt :', Altitude_list
#print 'HDOP :',hdop_list
###------------------------------------------------------------###
###---                  Processing                          ---###
###------------------------------------------------------------###
a = 6378137
b = 6356752.314245179497563967
f = 1/298.257223563
epsilon = 0.00001
e = np.sqrt(2*f - np.power(f,2.0))

lambda0 = (4+ 20/60 + 20/3600)*np.pi/180
phi0 = (4+ 20/60 + 20/3600)*np.pi/180
h0 = 0
N0 = a/(np.sqrt(1-np.power(e,2)*np.power(np.sin(phi0),2)));
M = np.matrix([[-np.sin(lambda0), np.cos(lambda0), 0], \
 [-np.sin(phi0)*np.cos(lambda0), -np.sin(phi0)*np.sin(lambda0),  np.cos(phi0)], \
 [np.cos(phi0)*np.cos(lambda0), np.cos(phi0)*np.sin(lambda0), np.sin(phi0)]])

xl_list = []
yl_list = []
zl_list = []


#transformation repere local
def transfo_ellipse_xyz(vect):
    #vect doit contenir Lambda, Phi, h
    N = a/(np.sqrt(1-np.power(e,2)*np.power(np.sin(vect.item(1)),2.0)))
    x = (N+vect.item(2))*np.cos(vect.item(1))*np.cos(vect.item(0))
    y = (N+vect.item(2))*np.cos(vect.item(1))*np.sin(vect.item(0))
    z = (N*(1-np.power(e,2))+vect.item(2))*np.sin(vect.item(1))
    matrice = np.matrix([[x],[y],[z]])
    return matrice
def transfo_geo_local(vect):
    Xl = M * np.matrix([[vect.item(0)-N0*np.cos(phi0)*np.cos(lambda0)], [vect.item(1)-N0*np.cos(phi0)*np.sin(lambda0)], [vect.item(2)-N0*(1-np.power(e,2))*np.sin(phi0)]])
    return Xl

matrice_list.append(np.matrix([[float(Longitude_list[0])],[float(Latitude_list[0])],[float(Altitude_list[0])]]))
matrice_list[0]=transfo_geo_local(transfo_ellipse_xyz(matrice_list[0]))
matrice_cov=np.matrix([[matrice_list[0].item(0)],[matrice_list[0].item(1)],[matrice_list[0].item(2)]])
xl_list.append(matrice_list[0].item(0))
yl_list.append(matrice_list[0].item(1))
zl_list.append(matrice_list[0].item(2))

for i in range(1,len(Longitude_list)):
    vector = np.matrix([[float(Longitude_list[i])],[float(Latitude_list[i])],[float(Altitude_list[i])]])
    matrice_list.append(vector)
    matrice_list[i]=transfo_geo_local(transfo_ellipse_xyz(matrice_list[i]))
    xl_list.append(matrice_list[i].item(0))
    yl_list.append(matrice_list[i].item(1))
    zl_list.append(matrice_list[i].item(2))
    matrice_cov = np.concatenate((matrice_cov,[[matrice_list[i].item(0)],[matrice_list[i].item(1)],[matrice_list[i].item(2)]]), axis=1)

#ecart-type et variance et moyenne

meanX = np.mean(xl_list)
meanY = np.mean(yl_list)
meanZ = np.mean(zl_list)
ecarTypeX = np.std(xl_list)
ecarTypeY = np.std(yl_list)
ecarTypeZ = np.std(zl_list)

print "X local: ", meanX
print "Y local: ", meanY
print "Z local: ", meanZ

print "ecarTypeX :", ecarTypeX
print "ecarTypeY s", ecarTypeY
print "ecarTypeZ s", ecarTypeZ

matrice_cov=np.cov(matrice_cov)
print "Matrice de covariance :\n",matrice_cov
#print "Liste", matrice_list

#plt.plot(time_list, Altitude_list)
plt.plot(xl_list, yl_list,'+')
plt.show()

#ser.write(b'hello')     # write a string

#def

#f.close()
ser.close()
