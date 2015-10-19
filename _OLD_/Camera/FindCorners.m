function corners = FindCorners( image_path, matr, save_path )
%FINDCORNERS Summary of this function goes here
%   Detailed explanation goes here
    image = imread(image_path);
    iSize = size(image);
    oldCorners = [iSize(1), 1; iSize(1), iSize(2); 1, iSize(2); 1, 1]';
    corners = Img2World(oldCorners, matr, [0,0,1,0]);
    corners(:, 1) = corners(:, 1) / corners(4, 1);
    corners(:, 2) = corners(:, 2) / corners(4, 2);
    corners(:, 3) = corners(:, 3) / corners(4, 3);
    corners(:, 4) = corners(:, 4) / corners(4, 4);
    display(corners);
    Rx = inv([1 0 0; 0 0 -1; 0 1 0]);
    hRx = cat(2, cat(1, Rx, [0 0 0]), [0; 0; 0; 1]);
    corners(:, 1) = hRx * corners(:, 1);
    corners(:, 2) = hRx * corners(:, 2);
    corners(:, 3) = hRx * corners(:, 3);
    corners(:, 4) = hRx * corners(:, 4);
    output = fopen(save_path, 'w');
    for i = 1:4
        for j = 1:3
            fprintf(output, '%4.4f\n', corners(j, i)); 
        end
    end
    fclose(output);
end

