
import serial
import math
import numpy as np
import scipy

# GPSMesssage=YearMonthDay,DateAge,HourMinutesSecondes,TimeAge,Satellites,
#             AgeSat,Longitude,Latitude,AgeLocation,Altitude,AgeAltitude,
#             HDOP,AgeHDOP,SentencesWithFix,FailedChecksum,PassedChecksum\n
#f = open('exemple','r')
#for line in f:
#    print(line(12))
#ser = serial.Serial('/dev/ttyUSB0', 19200)  # open serial port
#print(ser.name)         # check which port was really used
#ser.write(b'hello')     # write a string

#def

#f.close()
#ser.close()

print("Traitement")
## Traitement Matlab
#Parametres de l ellipse
a = 6378137.0
b = 6356752.314245179497563967
f = 1/298.257223563
#f = 1/298.257222101
epsilon = 0.00001
e = np.sqrt(2*f - np.power(f,2.0))

#Donnees du TP question 1
#mylambda = (4*np.pi)/180
#phi = (20*np.pi)/180
#h = 200
mylambda = float((4+ 3.0/60)*np.pi/180)
phi = float((48+ 18.0/60 + 22.0/3600)*np.pi/180)
h = 105.557
vect_ellipse = np.matrix([[mylambda], [phi], [h]])

lambda0 = (4+ 20.0/60 + 20.0/3600)*np.pi/180
phi0 = (20+ 20.0/60 + 20.0/3600)*np.pi/180
h0 = 0
N0 = a/(np.sqrt(1-np.power(e,2)*np.power(np.sin(phi0),2)));


x2 = -2430601.829
y2 = -4702442.706
z2 = -3546587.345

print 'Donnees : '
print 'Lambda = ', mylambda
print 'Phi = ', phi
print 'h = ', h

#Transformation M(Lambda,Phi,h) => M(x,y,z)
print 'Transfo => x,y,z'
def transfo_ellipse_xyz(vect):
    #vect doit contenir Lambda, Phi, h
    N = a/(np.sqrt(1-np.power(e,2)*np.power(np.sin(vect.item(1)),2)))
    x = (N+h)*np.cos(vect.item(1))*np.cos(vect.item(0))
    y = (N+h)*np.cos(vect.item(1))*np.sin(vect.item(0))
    z = (N*(1-np.power(e,2))+vect.item(2))*np.sin(vect.item(1))
    matrice = np.matrix([[x],[y],[z]])
    return matrice

vect_xyz = transfo_ellipse_xyz(vect_ellipse)
print 'x,y,z = \n', vect_xyz


#Transformation M(x,y,z) => M(Lambda,Phi,h)
print 'Transfo 2 x,y,z => '

def transfo_xyz_ellipse(vect):
    #vect doit contenir x,y,z
    mlambda = np.arctan2(vect.item(1),vect.item(0));
    hi = 0;
    N2 = a;
    p = np.sqrt(np.power(vect.item(0),2)+np.power(vect.item(1),2));

    sinusmphi = (vect.item(2)/(N2*(1-np.power(e,2))+hi));
    mphi = np.arctan((vect.item(2)+np.power(e,2)*N2*sinusmphi)/p);
    N2 = a/(np.sqrt(1-np.power(e,2)*np.power(sinusmphi,2)));
    hi = (p/np.cos(mphi)) - N2;
    hprev = 0;

    while abs(hi-hprev) > epsilon :
        hprev = hi
        sinusmphi = (vect.item(2)/(N2*(1-np.power(e,2))+hi))
        mphi = np.arctan((vect.item(2)+np.power(e,2)*N2*sinusmphi)/p)
        N2 = a/(np.sqrt(1-np.power(e,2)*np.power(sinusmphi,2)))
        hi = (p/np.cos(mphi)) - N2
    matrice = np.matrix([[mlambda],[mphi],[hi]])
    return matrice

print 'Lambda, Phi, h = \n', transfo_xyz_ellipse(vect_xyz)


M = np.matrix([[-np.sin(lambda0), np.cos(lambda0), 0], \
 [-np.sin(phi0)*np.cos(lambda0), -np.sin(phi0)*np.sin(lambda0),  np.cos(phi0)], \
 [np.cos(phi0)*np.cos(lambda0), np.cos(phi0)*np.sin(lambda0), np.sin(phi0)]])
#print 'OK'

#print 'Transfo 3 (Geocentrique => Local)'
#transfo 3
def global2local(vect):
    Xl = M * np.matrix([[vect.item(0)-N0*np.cos(phi0)*np.cos(lambda0)], [vect.item(1)-N0*np.cos(phi0)*np.sin(lambda0)], [vect.item(2)-N0*(1-np.power(e,2))*np.sin(phi0)]])
    return Xl
#print transfo_geo_local(x2,y2,z2)

#Transfo 4 local => Geocentrique
def transfo_local_geo(Xl):
    return np.matrix([[N0*np.cos(phi0)*np.cos(lambda0)], [N0*np.cos(phi0)*np.sin(lambda0)], [N0*(1-np.power(e,2))*np.sin(phi0)]]) + M.T * Xl;

#print 'Xdepart :',np.matrix([[x2],[y2], [z2]])
#print 'Xfinal :',transfo_local_geo(transfo_geo_local(x2,y2,z2))
print 'RESULTAT :',global2local(vect_xyz)
print 'Question 2\n'
vecteurxyz=transfo_xyz_ellipse(np.matrix([[x2], [y2], [z2]]))
print 'lambda, phi, h = \n',vecteurxyz
print 'x, y, z = \n', transfo_ellipse_xyz(vecteurxyz)
