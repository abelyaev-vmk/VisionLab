im=imread('frame_0000.jpg');
h1=figure;
x=[0 1];
%%[X,Y] = meshgrid(x);
X = [0 1; 0.25 0.75];
Y = [0 0; 0.5 1];
Z = zeros(2);
s=surf(X,Y,Z);
xlabel('x');
ylabel('y');
zlabel('z');
set(s,'CData',im,'FaceColor','texturemap')