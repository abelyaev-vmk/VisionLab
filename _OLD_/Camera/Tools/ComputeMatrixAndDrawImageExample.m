%% COMPUTEMATRIXANDDRAWIMAGEEXAMPLE. Summary of this function goes here
% Compute camera's calibration matrix and draw horizont and some lines on
% image from Example files
%% Syntax
% ComputeMatrixAndDrawImageExample(example_number)
%% Descriptiom
% ComputeMatrixAndDrawImageExample compute camera's calibration matrix from
% example .xml file, draw green horizont line on example image and draw
% some extra blue lines
% * example_number is a number of example, it can be 1 (for quaternion 
%   data) or 2 (for normal data)
% 
%% Example
% ComputeMatrixAndDrawImageExample(1);
% ComputeMatrixAndDrawImageExample(2);
% 
%% See Also
% ComputeMatrixAndDrawImageExample

function ComputeMatrixAndDrawImageExample(example_number)
    if example_number == 1
        calibrationMatrix = GetCalibrationMatrixFromXml(...
            'Example_quaternion.xml', 'q');
        image = imread('Example_quaternion.jpg');
        line1 = [1 531, 1159 1];
        line2 = [765 1080, 1801 1];
        DrawHorizontAndLines(calibrationMatrix, image, [line1; line2]);
    else
        calibrationMatrix = GetCalibrationMatrixFromXml(...
            'Example_normaldata.xml', 'd');
        line1 = [401 199 610 139];
        line2 = [657 182 704 129];
        DrawHorizontAndLines(calibrationMatrix, ...
            'Example_normaldata.jpg', [line1; line2]);
    end
end

