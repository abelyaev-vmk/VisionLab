function TestFunction( matr )
    image = imread('TownCenter2.jpg');
    iSize = size(image);
    mas = zeros(2, iSize(1) * iSize(2));
    for x = 1:iSize(1)
        for y = 1:iSize(2)
           mas(:, iSize(1)*(y-1) + x) = [x, y];
        end
        display(x);
    end
    loc = FindCameraLocation(matr);
    arr = Img2World(mas, matr, [0,0,1,0]);
    
    corner1 = value(iSize(1), 1);
    corner1(:) = corner1(:) / corner1(4)
    corner2 = value(iSize(1), iSize(2));
    corner2(:) = corner2(:) / corner2(4)
    corner3 = value(1, iSize(2));
    corner3(:) = corner3(:) / corner3(4)
    corner4 = value(1, 1);
    corner4(:) = corner4(:) / corner4(4)
    
    return;
    dist12 = distance(corner1, corner2);
    dist23 = distance(corner2, corner3);
    dist34 = distance(corner3, corner4);
    dist41 = distance(corner4, corner1);
    semiPerimeter = 0.5 * (dist12 + dist23 + dist34 + dist41);
    squad = sqrt((semiPerimeter - dist12) * (semiPerimeter - dist23) * ...
                 (semiPerimeter - dist34) * (semiPerimeter - dist41));
    
    pixelSquad = squad / (iSize(1) * iSize(2));
    
%     параллельные прямые переходят в параллельные, а значит получим
%     параллелограмм
    
    aspectRatio = dist41 / dist12; % X/Y
    pixelSideY = sqrt(pixelSquad / aspectRatio);
    pixelSideX = pixelSideY * aspectRatio;
    
    
    
    
    sizeX = dist41 / pixelSideX;
    new_size = fix([sizeX, sizeX / aspectRatio, 3]);
    H = HomographySolve([corner1(1:2)'; corner2(1:2)'; ...
                         corner3(1:2)'; corner4(1:2)']', ...
                        [new_size(1), 1; new_size(1), new_size(2); ...
                         1, new_size(2); 1, 1]');
    new_points = HomographyTransform(arr(1:2,:), H);
    new_image = uint8(zeros(new_size));
    for x = 1:iSize(1)
        for y = 1:iSize(2)
%             p = ceil(new_points(:, iSize(1) * (y - 1) + x));
            p = ceil(value(x, y) * sizeX);
            new_image(p(1), p(2), :) = image(x, y, :);
        end
        display(x);
    end
    
    imwrite(new_image, 'TEST_7.jpg');
    
    function v = value(x, y)
        v = arr(:, iSize(1) * (y - 1) + x);
    end
    
    function dist = distance(p1, p2)
        dist = sqrt((p1(1) - p2(1)) ^ 2 + (p1(2) - p2(2)) ^ 2);
    end
    
end

