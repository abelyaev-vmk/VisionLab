%% FindVanishingPoint
% computes vanishing point in the specified direction.
%% Syntax
%   out_pointArray = FindVanishingPoint(in_matrinx, in_directionArray)
%% Description
% FindVanishingPoint function computes vanishing point in the specified
% direction.
%
% * _out_pointArray_ is an array of vanishing points in homogeneous
% coordinates in the 3xN format, where N is a number of points;
% * _in_matrix_ is a camera projection matrix;
% * _in_directionArray_ is an array of the input directions in the format
% 3xN where N is a number of points;
%% Background
% d is the specified direction (assume D = cat(1, d, 0)).
% vanishing point: x = P * (X + alpha * D) when alpha goes to infinity
% for all X.
% x = P * D;
%% Example
%% See also
% FindHorizon

function out_pointArray = FindVanishingPoint(in_matrix, in_directionArray)

    if (size(in_directionArray, 1) ~= 3)
        error('directions should be specified in the matrix of size 3xN');
    end
    out_pointArray = in_matrix(:, 1 : 3) * in_directionArray;
end
