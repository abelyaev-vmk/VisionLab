function CloseProjection( matr )
    image = imread('TownCenter2.jpg');
    iSize = size(image);
    oldCorners = [iSize(1), 1; iSize(1), iSize(2); 1, iSize(2); 1, 1]';
    cameraLocation = FindCameraLocation(matr);
    planeHeight = cameraLocation(3) - 1;
    plane = [0, 0, 1, -planeHeight];
    newCorners = Img2World(oldCorners, matr, plane);
    for i = 1:4
        newCorners(:, i) = newCorners(:, i) / newCorners(4, i)
    end
end

