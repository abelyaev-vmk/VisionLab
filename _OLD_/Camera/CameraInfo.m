function CameraInfo(matrix_path, save_path)
%CAMERAINFO Summary of this function goes here
%   Write camera info into the file
    matr = TxtToMatr(matrix_path);
    location = FindCameraLocation(matr)
    direction = FindCameraDirection(matr)
    output = fopen(save_path, 'w')
    fprintf(output, '%4.4f %4.4f %4.4f %4.4f\n', location(1), location(2), location(3), location(4));
    fprintf(output, '%4.4f %4.4f %4.4f', direction(1), direction(2), direction(3));
    fclose(output);
end

