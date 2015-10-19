function image = Interpolate(size, points)
%PIXELINTERPOLATION Summary of this function goes here
%   Detailed explanation goes here
    image = uint8(zeros([size, 3]));
%     image(2:size(1) - 1, 2:size(2) - 1, :) = sum(points(2:size(1) - 1, 2:size(2) - 1, :, 2:4) / sum(points(2:size(1) - 1, 2:size(2) - 1, :, 1)));
    for x = 2:size(1) - 1
        for y = 2:size(2) - 1
            sum = 0;
            for i = 1:4
                if points(x, y, i, 1) ~= 1
                    sum = sum + points(x, y, i, 1);
                    image(x, y, :) = points(x, y, i, 2:4) * points(x, y, i, 1);
                end
                if sum ~= 0
                    image(x, y, :) = image(x, y, :) / sum;
                end
            end
        end
        display(x);
    end
end

