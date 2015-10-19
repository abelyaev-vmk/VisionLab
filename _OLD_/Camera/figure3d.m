width = 720;
height = 576;

matr = XmlToMatr('View_007.xml');
pos = Hom2Het(FindCameraLocation(matr));
dir = FindCameraDirection(matr);
oldPoints = [1 1 width width; 1 height 1 height];
newPoints = Hom2Het(Img2World(oldPoints, matr, [0 0 1 0]));

lines = bsxfun(@minus, newPoints, pos);

figure;
hold on;
xlabel('x');
ylabel('y');
zlabel('z');

for i=1:4
    x = [newPoints(1,i), pos(1)];
    y = [newPoints(2,i), pos(2)];
    z = [newPoints(3,i), pos(3)];
    
    plot3(x,y,z);
end

dirLine = cat(2, pos, pos + 10000 * dir);

plot3(dirLine(1, :), dirLine(2, :), dirLine(3, :));