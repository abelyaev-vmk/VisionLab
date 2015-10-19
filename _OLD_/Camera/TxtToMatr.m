function matr = TxtToMatr( matr_path )
    [a, b, c, d] = textread(matr_path, '%f, %f, %f, %f');
    m = [0, 0, 0; 0, 0, 0; 0, 0, 0; 0, 0, 0];
    for i = 1:3
        point = 4 * (i - 1) + 1;
        m(point) = a(i);
        m(point + 1) = b(i);
        m(point + 2) = c(i);
        m(point + 3) = d(i);
    end
    matr = transpose(m);
end

