%% Het2Hom
% converts homogeneous coordinates to heterogeneous ones
%% Syntax
%   out_pointArray = Het2Hom(in_pointArray);
%% Description
% Het2Hom function converts heterogeneous coordinates to homogeneous ones
%
% * _out_pointArray_ is the output array of homogeneous points in the MxN
% format, where M is a number of dimensions and N is a number of points.
% * _in_pointArray_ is the input array of heterogeneous points in the MxN
% format, where M is a number of dimensions and N is a number of points.
%% Example
%   homPoint = [2; 2];
%   hetPoint = Het2Hom(homPoint);
%% See also
% het2hom

function out_pointArray = Het2Hom(in_pointArray)
    nPoints = size(in_pointArray, 2);
    out_pointArray = cat(1, in_pointArray, ones(1, nPoints));
end