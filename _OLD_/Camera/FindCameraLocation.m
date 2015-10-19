%% FindCameraLocation
% computes location of the camera in the world coordinates.
%% Syntax
%   out_point = FindCameraLocation(in_matrix);
%% Description
% FindCameraLocation function computes location fo the camera in the world
% coordinates.
%
% * out_point is the camera location in the homogeneous coordinates in the
% 4x1 format;
% * in_matrix is a camera projection matrix;
%% Background
% if X - camera location, then for all D, a such that D(4) = 0, exists k
% such that k * P * (X + D) = P * (X + a * D); -- all points on the line,
% that goes through the camera center, projects to the same image point.
% (k - 1) * P * X = (a - k) * P * D;
% If D and a are arbitrary then P * X = 0 and k = a;
% X(4) = 1; -- additional normalization constraint
%% Example
%% See also
%

function out_point = FindCameraLocation(in_matrix)
    A = cat(1, in_matrix, [0, 0, 0, 1]);
    b = [0; 0; 0; 1];
    out_point = A \ b;
end
