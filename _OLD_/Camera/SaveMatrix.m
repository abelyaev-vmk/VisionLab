function SaveMatrix( matr, save_path )
%SAVEMATRIX Summary of this function goes here
%   Detailed explanation goes here
    mSize = size(matr);
    output = fopen(save_path, 'w');
    for i = 1:mSize(1) * mSize(2)
        fprintf(output, '%4.4f ', matr(i));
    end
    fclose(output);
end

