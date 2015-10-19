%% FindLineIntersection
% computes intersection of 2 lines in 2D space.
%% Syntax
% out_pointArray = FindLineIntersection(in_firstArray, in_secondArray);
%% Description
% FindLineIntersection computes intersection of 2 lines in 2D space -- line
% in the _in_firstArray_ and the corresponded line in the _in_secondArray_.
%
% * out_pointArray is an array of point homogeneous coordinates in 3xN
% format, where N is a number of points.
% * in_firstArray is the first array of line parameters in the Nx3 format,
% where N is a number of lines. N should be equal to number of lines in
% _in_secondArray_ or be equal to 1, then function computes intersection of
% the specified line with all other lines.
% _in_secondArray_ is the second array of line parameters in the Nx3
% format, where N is a number of lines
%% Background
% l1, l2 are the corresponded line parameters
% l1 * x = 0;
% l2 * x = 0;
% x(3) = 1; -- normalization constraint
%% Example
%   line1 = [1, 0, 0];
%   line2 = [0, 1, 0];
%   point = FindLineIntersection(line1, line2);
%% See also

function out_pointArray = FindLineIntersection(in_firstArray, in_secondArray)

    nLines = size(in_secondArray, 1);
    
    nFirstLines = size(in_firstArray, 1);
    if (nFirstLines == 1)
        idxArray = ones(1, nLines);
    else
        assert(nLines == nFirstLines);
        idxArray = 1 : nLines;
    end
    
    out_pointArray = zeros(3, nLines);
    for iLine = 1 : nLines
        firstParams = in_firstArray(idxArray(iLine), :);
        secondParams = in_secondArray(iLine, :);
        A = cat(1, firstParams, secondParams, [0, 0, 1]);
        b = [0; 0; 1];
        out_pointArray(:, iLine) = A \ b;
    end
end