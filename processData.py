import serial
import matplotlib.pyplot as plt
import numpy as np
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


ser = serial.Serial('/dev/ttyUSB0', 9600)  # open serial port
print(ser.name)         # check which port was really used
#Variables used for recording
time_list = []
hdop_list = []
Longitude_list = []
Latitude_list = []
Altitude_list = []
for line in ser:
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
print 'T : ',time_list
print 'Long :',Longitude_list
print 'Lat :', Latitude_list
print 'Alt :', Altitude_list
print 'HDOP :',hdop_list

plt.plot(time_list, Altitude_list)
plt.plot(Longitude_list, Latitude_list,'+')
plt.show()

#ser.write(b'hello')     # write a string

#def

#f.close()
ser.close()
