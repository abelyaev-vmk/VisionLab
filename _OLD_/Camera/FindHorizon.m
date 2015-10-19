%% FindHorizon
% computes parameters of the horizon
%% Syntax
%   out_params = FindHorizon(in_matrix);
%% Description
% FindHorizon function computes parameters of the horizon line.
%
% * _out_params_ is a parameters of the horizon line in 1x3 format;
% * _in_matrix_ is the camera projection matrix.
%% Background
% horizon is a line that goes through two vanishing points corresponded to
% directions [1; 0; 0] and [0; 1; 0]. 
%% Example
%% See also
% FindVanishingPoint

function out_params = FindHorizon(in_matrix)
    directionArray = [1, 0; 0, 1; 0, 0];
    pointArray = FindVanishingPoint(in_matrix, directionArray);
    out_params = PointsToLine(pointArray);
end
