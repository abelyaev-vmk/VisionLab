%% FindDirection
% Computes direction to the specified point of the image.
%% Syntax
%   out_directionArray = FindDirection(in_imgPointArray, in_matrix);
%% Description
% FindDirection function computes unnormalized direction from the camera
% center to some point that projects to the specified point of the image.
%
% * out_directionArray is an array of directions in the 3xN format, where N
% is a number of vectors;
% * in_imgPointArray is an array of homogeneous or heterogeneous points on
% the image is the 3xN or 2xN format, where N is a number of points;
% * in_matrix is the camera projection matrix.
%% Background
% If X is camera location, D is the required direction, P is the projection
% matrix, x is the input image point 
% P * (X + D) = x;
% P * X = 0; -- for details see findCameraLocation function
% P * D = x;
% D(4) = 0; -- it is a vector
%% Example
%% See also

function out_directionArray = FindDirection(in_imgPointArray, in_matrix)

    if (size(in_imgPointArray, 1) == 2)
        % heterogeneous coordinates
        in_imgPointArray = het2hom(in_imgPointArray);
    end
    A = in_matrix(:, 1 : 3);
    out_directionArray = A \ in_imgPointArray;
end