%% FindCameraDirection
% computes direction of the camera view.
%% Syntax
%   out_direction = FindCameraDirection(in_matrix);
%% Description
% FindCameraDirection computes direction of the camera view.
%
% * _out_direction_ is a direction of the camers view in the 3x1 format.
% * _in_matrix_ is the camera projection matrix.
%% Background
%% Example
%% See also
%

function out_direction = FindCameraDirection(in_matrix)
    out_direction = in_matrix(3, 1 : 3)';
end
