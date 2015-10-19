%% Hom2Het
% converts homogeneous coordinates to heterogeneous ones
%% Syntax
%   out_pointArray = Hom2Het(in_pointArray);
%% Description
% Hom2Het function converts homogeneous coordinates to heterogeneous ones
%
% * _out_pointArray_ is the output array of heterogeneous points in the MxN
% format, where M is a number of dimensions and N is a number of points.
% * _in_pointArray_ is the input array of homogeneous points in the MxN
% format, where M is a number of dimensions and N is a number of points.
%% Example
%   homPoint = [1; 1; 0.5];
%   hetPoint = Hom2Het(homPoint);
%% See also
% het2hom

function out_pointArray = Hom2Het(in_pointArray)
    out_pointArray =...
        bsxfun(@rdivide, in_pointArray(1 : end - 1, :), in_pointArray(end, :));
end
