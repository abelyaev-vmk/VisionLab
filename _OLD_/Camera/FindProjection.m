%% FindProjection
% computes projection of the input vector to the specified plane
%% Syntax
%   out_vectorArray = FindProjection(in_vectorArray, in_plane);
%% Description
% FindProjection function computes projection of the input vector to the
% specified plane
%
% * _out_vectorArray_ is an array of output projections in the MxN format,
% where M is a number of dimensions and N is number of vectors;
% * _in_vectorArray_ is an array of input vectors in the MxN format, where
% M is a number of dimensions and N is number of vectors;
% * _in_plane_ is a plane to project the input vectors.
%% Background
% If r is the original vector, p is its projection, n is a normal to the
% plane
% (n, p) = 0; -- projection lies in the plane
% exists a such that p + a * n = r;
%% Example
%   plane = [0, 0, 1, 0];
%   vector = [1; 1; 1];
%   projection = FindProjection(vector, plane);
%% See also

function out_vectorArray = FindProjection(in_vectorArray, in_plane)
    
    nVectors = size(in_vectorArray, 2);
    n = in_plane(1, 1 : 3)';
    
    A = cat(2, n', 0);
    A = cat(1, A, cat(2, eye(3, 3), n));
    
    b = cat(1, zeros(1, nVectors), in_vectorArray);
    
    x = A \ b;
    out_vectorArray = x(1 : 3, :);
end