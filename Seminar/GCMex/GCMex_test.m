% Test script for GCMex
% Caution. All incoming parameters shoul have the types specified in
% this example. GCMex would crash if parameters have different types

images = cell(2, 1);
images{1} = uint8([255 255 255 0]');
images{2} = uint8([0 255 255 255]');

unary = ...
 [0 0 0 1;
  1 0 0 0];

pairwise = ...
 [0 1 0 0;
  1 0 1 0;
  0 1 0 1;
  0 0 1 0];

[labels energyBefore energyAfter] = GCMex(zeros(4, 1), unary, sparse(pairwise), ...
  single(zeros(2)), 0, int32(2), images);