%% FindVerticalVanishingPoint
% computes location of the vertical vanishing point
%% Syntax
%   out_point = FindVerticalVanishingPoint(in_matrix);
%% Description
% FindVerticalVanishingPoint functions computes location of the vertical
% vanishing point in the homogeneous coordinates.
%
% * _out_point_ is the vertical vanishing point in the 3x1 format;
% * _in_matrix_ is a camera projection matrix.
%% Background
% vertical vanishing point is a vanishing point in the [0; 0; 1] direction.
%% Example
%% See also
% FindVanishingPoint

function out_point = FindVerticalVanishingPoint(in_matrix)
    out_point = FindVanishingPoint(in_matrix, [0; 0; 1]);
end
