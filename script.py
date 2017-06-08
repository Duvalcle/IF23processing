
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
a = 6378137
b = 6356752.314245179497563967
f = 1/298.257223563
epsilon = 0.00001
e = np.sqrt(2*f - np.power(f,2.0))

#Donnees du TP question 1
mylambda = (4*np.pi)/180
phi = (20*np.pi)/180
h = 200
vect_ellipse = np.matrix([[mylambda], [phi], [h]])

lambda0 = (4+ 20/60 + 20/3600)*np.pi/180
phi0 = (4+ 20/60 + 20/3600)*np.pi/180
h0 = 0
N0 = a/(np.sqrt(1-np.power(e,2)*np.power(np.sin(phi0),2)));


x2 = -2430601.289
y2 = -4702442.706
z2 = -3546587.345

print 'Donnees : '
print 'Lambda = ', mylambda
print 'Phi = ', phi
print 'h = ', h

#Transformation M(Lambda,Phi,h) => M(x,y,z)
print 'Transfo => x,y,z'
def transfo_ellipse_xyz(vect):
    N = a/(np.sqrt(1-np.power(e,2)*np.power(np.sin(vect.item(1)),2)))
    x = (N+h)*np.cos(vect.item(1))*np.cos(vect.item(0))
    y = (N+h)*np.cos(vect.item(1))*np.sin(vect.item(0))
    z = (N*(1-np.power(e,2))+vect.item(2))*np.sin(vect.item(1))
    matrice = np.matrix([[x],[y],[z]])
    return matrice

print 'x,y,z = ', transfo_ellipse_xyz(vect_ellipse)


#Transformation M(x,y,z) => M(Lambda,Phi,h)
print 'Transfo 2 x,y,z => '

def transfo_xyz_ellipse(x, y, z):
    mlambda = np.arctan(y/x);
    h2 = 0;
    N2 = a;
    p = np.sqrt(np.power(x,2)+np.power(y,2));

    sinusmphi = (z/(N2*(1-np.power(e,2))+h));
    mphi = np.arctan((z+np.power(e,2)*N2*sinusmphi)/p);
    N2 = a/(np.sqrt(1-np.power(e,2)*np.power(sinusmphi,2)));
    hi = (p/np.cos(mphi)) - N2;
    hprev = 0;

    while abs(hi-hprev) > epsilon :
        hprev = hi
        sinusmphi = (z/(N2*(1-np.power(e,2))+h))
        mphi = np.arctan((z+np.power(e,2)*N2*sinusmphi)/p)
        N2 = a/(np.sqrt(1-np.power(e,2)*np.power(sinusmphi,2)))
        hi = (p/np.cos(mphi)) - N2
    return (mlambda, mphi, hi)

(lambda2, phi2, h)=transfo_xyz_ellipse(x1, y1, z1)
print 'Lambda = ', lambda2
print 'Phi = ', phi2
print 'h = ', h

M = np.matrix([[-np.sin(lambda0), np.cos(lambda0), 0], \
 [-np.sin(phi0)*np.cos(lambda0), -np.sin(phi0)*np.sin(lambda0),  np.cos(phi0)], \
 [np.cos(phi0)*np.cos(lambda0), np.cos(phi0)*np.sin(lambda0), np.sin(phi0)]])
print 'OK'

print 'Transfo 3 (Geocentrique => Local)'
#transfo 3
def transfo_geo_local(x, y, z):
    Xl = M * np.matrix([[x-N0*np.cos(phi0)*np.cos(lambda0)], [y-N0*np.cos(phi0)*np.sin(lambda0)], [z-N0*(1-np.power(e,2))*np.sin(phi0)]])
    return Xl

print transfo_geo_local(x2,y2,z2)

#Transfo 4 local => Geocentrique
def transfo_local_geo(Xl):
    return np.matrix([[N0*np.cos(phi0)*np.cos(lambda0)], [N0*np.cos(phi0)*np.sin(lambda0)], [N0*(1-np.power(e,2))*np.sin(phi0)]]) + M.T * Xl;

print 'Xdepart :',np.matrix([[x2],[y2], [z2]])
print 'Xfinal :',transfo_local_geo(transfo_geo_local(x2,y2,z2))

print 'Question 2\n'
(temp1, temp2, temp3)=transfo_xyz_ellipse(x2, y2, z2)
print transfo_ellipse_xyz(temp1, temp2, temp3)
