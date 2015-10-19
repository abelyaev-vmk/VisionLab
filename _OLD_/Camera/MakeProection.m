function pr = MakeProection( image_path, cameraMatrix_path )
    PrincipalPointX = 959.5;
    PrincipalPointY = 539.5;
    FocalLengthX = 2696.35888671875;
    FocalLengthY = 2696.35888671875;
    FocalLength = sqrt(FocalLengthX ^ 2 + FocalLengthY ^ 2);
    
    image = imread(image_path);
    imageSize = size(image);
    matr = TxtToMatr(cameraMatrix_path);
    location = FindCameraLocation(matr);
    direction = FindCameraDirection(matr);
    corners = [imageSize(1), 0; 0, 0; 0, imageSize(2); imageSize(1), imageSize(2)];
    cornersInfo = zeros(4, 2);
    for i = 1:4
        cornersInfo(i, :) = PixelInfo(corners(i, :));
    end
    display(cornersInfo(2,2));
    
    
    function info = PixelInfo(pixel)
        x = pixel(1); y = pixel(2);
        distanceToCenter = sqrt((PrincipalPointX - x) ^ 2 + (PrincipalPointY - y) ^ 2);
        dst = sqrt(FocalLength ^ 2 + distanceToCenter ^ 2);
        angle = atan(distanceToCenter / FocalLength);
        info = [dst, angle];
    end
end

