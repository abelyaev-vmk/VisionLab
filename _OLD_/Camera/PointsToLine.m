%% PointsToLine
% computes parameters of line that goes through two input 2D points.
%% Syntax
%   out_params = PointToLine(in_pointArray);
%% Description
% PointsToLine function computes parameters of line that goes through two
% input 2D points. 
%
% * _out_params_ is the result line parameters in the 1x3 format;
% * _in_pointArray_ is an array of 2D points in homogeneous or
% heterogeneous coordinates in the 3X2 or 2x2 format store as a column
% vectors.
%% Background
% l is line parameters row vector, x1 and x2 are points.
% l * x1 = 0;
% l * x2 = 0;
% l(3) = 1; -- normalization constraint
%% Example
%   point1 = [1; 0];
%   point2 = [0; 1];
%   line = pointToLine(cat(2, point1, point2));
%% See also
%

function out_params = PointsToLine(in_pointArray)
    if (size(in_pointArray, 1) == 2)
        % heterogeneous coordinates
        in_pointArray = Het2Hom(in_pointArray);
    end
    A = cat(2, in_pointArray, [0; 0; 1]);
    out_params = [0, 0, 1] / A;
end
