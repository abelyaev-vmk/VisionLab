function P0 = calibr()

FocalLengthX = 2696.35888671875000000000;
FocalLengthY = 2696.35888671875000000000;
PrincipalPointX = 959.50000000000000000000;
PrincipalPointY = 539.50000000000000000000;
Skew = 0.00000000000000000000;
TranslationX = -0.05988363921642303467;
TranslationY = 3.83331298828125000000;
TranslationZ = 12.39112186431884765625;
RotationX = 0.69724917918208628720;
RotationY = -0.43029624469563848566;
RotationZ = 0.28876888503799524877;
RotationW = 0.49527896681027261394;
DistortionK1 = -0.60150605440139770508;
DistortionK2 = 4.70203733444213867188;
DistortionP1 = -0.00047452122089453042;
DistortionP2 = -0.00782289821654558182;

SaveXml(FocalLengthX, FocalLengthY, PrincipalPointX, PrincipalPointY, ...
    Skew, TranslationX, TranslationY, TranslationZ, ...
    RotationX, RotationY, RotationZ, RotationW, ...
    DistortionK1, DistortionK2, DistortionP1, DistortionP2);

K = [FocalLengthX, tan(Skew) * FocalLengthY, PrincipalPointX;
  0, FocalLengthY, PrincipalPointY;
  0, 0, 1];

% K = [FocalLengthY, tan(Skew) * FocalLengthX, PrincipalPointY;
%   0, FocalLengthX, PrincipalPointX;
%   0, 0, 1];

%  K([1, 2], :) = K([1, 2], :) / 2;

alpha = 1 / RotationW;
direction = [RotationX; RotationY; RotationZ];
direction = direction ./ sum(direction .* direction);

R_x = [0 -direction(3) direction(2); direction(3) 0 -direction(1);
  -direction(2) direction(1) 0];

R = eye(3) + sin(alpha) * R_x + (1 - cos(alpha)) * R_x * R_x;

t = [TranslationX; TranslationY; TranslationZ];
P = K * [R,  t];
% P = K * [R', -R' * t];

qx = RotationX;
qy = RotationY;
qz = RotationZ;
qw = RotationW;

% http://stackoverflow.com/questions/1556260/convert-quaternion-rotation-to-rotation-matrix
R1 = [1.0 - 2.0*qy*qy - 2.0*qz*qz, ...
    2.0*qx*qy - 2.0*qz*qw, ...
    2.0*qx*qz + 2.0*qy*qw;...
	2.0*qx*qy + 2.0*qz*qw, ...
    1.0 - 2.0*qx*qx - 2.0*qz*qz, ...
    2.0*qy*qz - 2.0*qx*qw;...
	2.0*qx*qz - 2.0*qy*qw, ...
    2.0*qy*qz + 2.0*qx*qw, ...
    1.0 - 2.0*qx*qx - 2.0*qy*qy];

% P1 = K * [R1, t];
% P2 = K * [R1', t];
% P3 = K * [R1', -R1' * t];
P4 = K * [R1, -R1 * t]; % I used this equation

SaveMatrix([R1, -R1 * t], 'proj.txt');
display([R1, -R1 * t]);
% 
% P0 = P1
% P0 = P2
% P0 = P3
P0 = P4;



% dlmwrite('sandbox/P.txt', P);
% dlmwrite('sandbox/P.txt', P4);


    function SaveXml(FLX, FLY, PPX, PPY, S, TX, TY, TZ, ...
            RX, RY, RZ, RW, DK1, DK2, DP1, DP2)
        docNode = com.mathworks.xml.XMLUtils.createDocument('Camera');
        camera = docNode.getDocumentElement;
        camera.setAttribute('name', 'camera');
        iC = docNode.createElement('InternalCalibration');
        iC.setAttribute('flx', num2str(FLX));
        iC.setAttribute('fly', num2str(FLY));
        iC.setAttribute('ppx', num2str(PPX));
        iC.setAttribute('ppy', num2str(PPY));
        iC.setAttribute('s', num2str(S));
        iC.setAttribute('dk1', num2str(DK1));
        iC.setAttribute('dk2', num2str(DK2));
        iC.setAttribute('dp1', num2str(DP1));
        iC.setAttribute('dp2', num2str(DP2));
        eC = docNode.createElement('ExternalCalibration');
        eC.setAttribute('tx', num2str(TX));
        eC.setAttribute('ty', num2str(TY));
        eC.setAttribute('tz', num2str(TZ));
        eC.setAttribute('rx', num2str(RX));
        eC.setAttribute('ry', num2str(RY));
        eC.setAttribute('rz', num2str(RZ));
        eC.setAttribute('rw', num2str(RW));
        camera.appendChild(iC);
        camera.appendChild(eC);
        xmlwrite('camera_quaternon.xml', docNode);
    end








end
% R_x = [1, 0, 0; 0, cos(RotationX) -sin(RotationX);
%   0, sin(RotationX), cos(RotationX)];
% R_y = [cos(RotationY), 0, sin(RotationY); 0, 1, 0;
%   -sin(RotationY), 0, cos(RotationY)];
% R_z = [cos(RotationZ), -sin(RotationZ), 0;
%   sin(RotationZ), cos(RotationZ), 0; 0, 0, 1];
% 
% R = R_x * R_y * R_z;
% 
% t = [TranslationX; TranslationY; TranslationZ];
% 
% P = K * [R', -R' * t];






