function [ camera_matr, plane_matr ] = ConvertionMatrixes(fi)
%CONVERTIONMATRIXES Summary of this function goes here
%   Xp || Xc, Yp || -Zc, Zp || Yc
    base = [1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1];
    camera_matr = CoordinatesConvertion(fi(1), fi(2), fi(3), base);
    plane_matr = CoordinatesConvertion(0, 0, 0.5, base) * camera_matr;

end

