function m = RotateMatrix(matr, R)
%ROTATEMATRIX Summary of this function goes here
%   Detailed explanation goes here
    display(matr);
%     m = (matr' * R)';
    m = matr * R;
end

