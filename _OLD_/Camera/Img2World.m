%% Img2World
% computes world coordinates of the specified image point
%% Syntax
%   [out_pointArray] = Img2World(in_imgPointArray, in_matrix, in_plane);
%% Description
% Img2World function computes world coordinates of the specified image
% point. The result point lies in the specified plane.
%
% * out_pointArray is an array of the world points in the homogeneous
% coordinates in the 4xN format, where N is a number of points.
% * in_imgPointArray is an array of image points in the homogeneous or
% heterogeneous coordinates in the 3xN or 2xN format, where N is a number
% of points.
% * in_plane is a row vector of plane parameters
%% Background
% X is the intersection, x is its projection, P is the projection matrix,
% A is a row vector of plane parameters. 
% x = P * X
% A * X = 0
%% Example
%% See also

function out_pointArray = Img2World(in_imgPointArray, in_matrix, in_plane)

    nPoints = size(in_imgPointArray, 2);
    if (size(in_imgPointArray, 1) == 2)
        % heterogeneous coordinates
        in_imgPointArray = Het2Hom(in_imgPointArray);
    end
 
    A = cat(1, in_matrix, in_plane);
    b = cat(1, in_imgPointArray, zeros(1, nPoints));
    out_pointArray = A \ b;
    disp(A)
end

