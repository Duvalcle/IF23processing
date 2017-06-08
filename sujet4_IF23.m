clear;
close;

a = 6378137;
b = 6356752.314245179497563967;
f = 1/298.257223563;
epsilon = 10^-5;
%f = (a-b)/a;

%b = ( 1- f)*a;
e = sqrt(2*f - f^2);
% %test 1
lambda = (4*pi)/180
phi = (20*pi)/180
h = 200
lambda0 = (4+ 20/60 + 20/3600)*pi/180;
phi0 = (4+ 20/60 + 20/3600)*pi/180;
h0 = 0;

% %algorithme 1
% N = a/(sqrt(1-e^2*sin(phi)^2));
% x = (N+h)*cos(phi)*cos(lambda)
% y = (N+h)*cos(phi)*sin(lambda)
% z = (N*(1-e^2)+h)*sin(phi)
% 
% 
% 
% %algorithme 2 
% lambda2 = atan(y/x);
% h2 = 0;
% N2 = a;
% p = sqrt(x^2+y^2);
% 
% sinusPhi2 = (z/(N2*(1-e^2)+h));
% phi2 = atan((z+e^2*N2*sinusPhi2)/p);
% N2 = a/(sqrt(1-e^2*sinusPhi2^2));
% hi = (p/cos(phi2)) - N2;
% hprev = 0;
% 
% while(norm(hi-hprev) > epsilon)
%     hprev = hi;
%     sinusPhi2 = (z/(N2*(1-e^2)+h));
%     phi2 = atan((z+e^2*N2*sinusPhi2)/p);
%     N2 = a/(sqrt(1-e^2*sinusPhi2^2));
%     hi = (p/cos(phi2)) - N2;
%     
% end
% lambda2
% phi2
% hi
% 
% 
% %algorithme 3
% N0 = a/(sqrt(1-e^2*sin(phi0)^2));
% Xl = [-sin(lambda0) cos(lambda0) 0; -sin(phi0)*cos(lambda0) -sin(phi0)*sin(lambda0)  cos(phi0); cos(phi0)*cos(lambda0) cos(phi0)*sin(lambda0) sin(phi0)] * [x-N0*cos(phi0)*cos(lambda0); y-N0*cos(phi0)*sin(lambda0); z-N0*(1-e^2)*sin(phi0)]
% 
% 
% % algorithme 4 
% Xf = [N0*cos(phi0)*cos(lambda0); N0*cos(phi0)*sin(lambda0); N0*(1-e^2)*sin(phi0)] + [-sin(lambda0) cos(lambda0) 0; -sin(phi0)*cos(lambda0) -sin(phi0)*sin(lambda0)  cos(phi0); cos(phi0)*cos(lambda0) cos(phi0)*sin(lambda0) sin(phi0)]' * Xl;
% 
% Xf


%question 2
x = -2430601.289;
y=-4702442.706;
z=-3546587.345;

% %algorithme 2 
lambda2 = atan(y/x);
h2 = 0;
N = a;
p = sqrt(x^2+y^2);

sinusPhi2 = (z/(N*(1-e^2)+h));
phi2 = atan((z+e^2*N*sinusPhi2)/p);
N = a/(sqrt(1-e^2*sinusPhi2^2));
hi = (p/cos(phi2)) - N;
hprev = 0;

while(norm(hi-hprev) > epsilon)
    hprev = hi;
    sinusPhi2 = (z/(N*(1-e^2)+h));
    phi2 = atan((z+e^2*N*sinusPhi2)/p);
    N = a/(sqrt(1-e^2*sinusPhi2^2));
    hi = (p/cos(phi2)) - N;
    
end
lambda2
phi2
hi


%algorithme 1
N = a/(sqrt(1-e^2*sin(phi2)^2));
xs = (N+h)*cos(phi2)*cos(lambda2)
ys = (N+h)*cos(phi2)*sin(lambda2)
zs = (N*(1-e^2)+h)*sin(phi2)


