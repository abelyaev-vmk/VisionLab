%% See Also
% TextureToSurface

function TextureToSurface(imagePath, xmlPath, xmlType)
%% 
    F = figure;
    xlabel('x');
    ylabel('y');
    zlabel('z');
    img = imread(imagePath);
    matr = GetCalibrationMatrixFromXml(xmlPath, xmlType);

%% Trapezium
%     x1 = 0; x2 = 1;
%     x3 = 0.25; x4 = 0.75;
%     y1 = 0; y2 = 0;
%     y3 = 1; y4 = 1;
    iSize = size(img);
    oldCorners = [iSize(1), 1; 1, 1; 1, iSize(2); iSize(1), iSize(2)]';
    corners = Img2World(oldCorners, matr, [0,0,1,0]);
    corners(:, 1) = corners(:, 1) / corners(4, 1);
    corners(:, 2) = corners(:, 2) / corners(4, 2);
    corners(:, 3) = corners(:, 3) / corners(4, 3);
    corners(:, 4) = corners(:, 4) / corners(4, 4);
    x1 = corners(1, 1); y1 = corners(2, 1);
    x2 = corners(1, 2); y2 = corners(2, 2);
    x3 = corners(1, 3); y3 = corners(2, 3);
    x4 = corners(1, 4); y4 = corners(2, 4);
    X = [x1 x2; x3 x4] * 10^4;
    Y = [y1 y2; y3 y4] * 10^4;
    Z = zeros(2);
    s = surf(X, Y, Z);
    set(s, 'CData', img, 'FaceColor', 'texturemap');
    
end

