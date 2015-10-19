%% DRAWHORIZONTANDLINES. Summary of this function goes here
% Display image and draw horizont line and users lines on it
%% Syntax
% DrawHorizontAndLines(calibrationMatrix, in_image, lines)
%% Description
% DrawHorizontAndLines display image and draw green horizont line and blue  
% users lines on it
% 
% * calibrationMatrix is a camera's calibration matrix 3x4
% * in_image is an image to be displayed. It can be a path to image, or
%   array NxMx3
% * lines is an array Kx4, where K is a number of lines, and 4 is a
%   concantenation [x1 y1 x2 y2] of two line's points. It can be absent
% 
%% Example 
% DrawHorizontAndLines(calibrationMatrix, imageArray);
% DrawHorizontAndLines(calibrationMatrix, 'image_path.jpg', ...
%                      [0 0 10 30; 1 2 100 200]);
% 
%% See Also
% DrawHorizontAndLines

function DrawHorizontAndLines(calibrationMatrix, in_image, lines)
    if ischar(in_image)
        imageToDisplay = imread(in_image);
    else
        imageToDisplay = in_image;
    end
    xlabel('x'); ylabel('y');
    image(imageToDisplay);
    hold on;
    x = 1:10000;
    horizont = FindHorizon(calibrationMatrix);
    k_hor = -horizont(1) / horizont(2);
    b_hor = -horizont(3) / horizont(2);
    y_hor = k_hor * x + b_hor;
    line(x, y_hor, 'COLOR', 'GREEN');
    
    if nargin == 3
        if size(lines, 2) ~= 4
            display('Invalid lines type')
            return;
        end
        for i = 1:size(lines, 1)
            k = (lines(i, 2) - lines(i, 4)) / (lines(i, 1) - lines(i, 3));
            b = lines(i, 2) - k * lines(i, 1);
            y = k * x + b;
            line(x, y, 'COLOR', 'BLUE');
        end
    end
end

