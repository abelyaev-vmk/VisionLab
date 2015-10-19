 function  TowerCenterStreetHomology(image_path, save_path, temp_path)
%TOWERCENTERSTREETHOMOLOGY Summary of this function goes here
%   Detailed explanation goes here
    image = imread(image_path);
    imageSize = size(image);
    temp_image(:,:,:) = image;
    
    %points from left down
    points = [673 0; 0 1319; 2 1907; 975 1485];
    %koefficients for directs
    for i = 1:4
        k(i) = (points(i, 2) - points(rem(i + 1, 5) + fix(i / 4), 2)) ...
            / (points(i, 1) - points(rem(i + 1, 5) + fix(i / 4), 1));
        b(i) = points(i, 2) - k(i) * points(i, 1);
        z(i) = k(i) > 0;
    end
    %points of new image
%     small_image = uint8(zeros(600, 400, 3));
    sizeX = 600; sizeY = 400;
%     дл€ интерпол€ции используем четыре ближайших пиксел€ и их рассто€ние
    points_matrix = uint8(zeros(sizeX, sizeY, 4, 4));
    points_matrix(:, :, :, 1) = 1;
    newPoints = [600 1; 1 1; 1 400; 600 400];
    H = HomographySolve(transpose(points), transpose(newPoints));
%     koordinates = [];
    for i = 1:imageSize(1)
        for j = 1:imageSize(2)
            if ~Inside(i, j)
                temp_image(i, j, :) = [0, 0, 0];
            end
            if Inside(i, j)
                p = HomographyTransform([i; j], H);
                upX = ceil(p(1));
                downX = fix(p(1));
                upY = ceil(p(2));
                downY = fix(p(2));
                distLD = distance(p, [downX, downY]);
                distLU = distance(p, [downX, upY]);
                distRU = distance(p, [upX, upY]);
                distRD = distance(p, [upX, downY]);
                if points_matrix(downX, downY, 1, 1) < distLD
                    points_matrix(downX, downY, 1, 1) = distLD;
                    points_matrix(downX, downY, 1, 2:4) = image(i, j, :);
                end
                if points_matrix(downX, upY, 2, 1) < distLU
                    points_matrix(downX, upY, 2, 1) = distLU;
                    points_matrix(downX, upY, 2, 2:4) = image(i, j, :);
                end
                if points_matrix(upX, upY, 3, 1) < distRU
                    points_matrix(upX, upY, 3, 1) = distRU;
                    points_matrix(upX, upY, 3, 2:4) = image(i, j, :);
                end
                if points_matrix(upX, downY, 4, 1) < distRD
                    points_matrix(upX, downY, 4, 1) = distRD;
                    points_matrix(upX, downY, 4, 2:4) = image(i, j, :);
                end
            end
%             if Inside(i, j)
%                 p = round(HomographyTransform([i; j], H));
%                 %display(p);
%                 small_image(p(1) + 1, p(2) + 1, :) = image(i, j, :);
%             end
% %             if Inside(i, j)
% %                 koordinates(end + 1, :) = [i, j];
% %             end
        end
        display(i);
    end
%     newKoordinates = HomographyTransform(transpose(koordinates), H);
%     small_image = Interpolate([500, 500, 3], newKoordinates, koordinates, image);
%     imwrite(small_image, save_path);
    new_image = Interpolate([sizeX, sizeY], points_matrix);
    imwrite(new_image, save_path);
    imwrite(temp_image, temp_path);
        
    function ins = Inside(x, y)
        ld = (points(1, 2) == points(2, 2) && y > points(1, 2)) || y > k(1) * x + b(1);
        ud = (points(2, 1) == points(3, 1) && x > points(2, 1)) || x > (y - b(2)) / k(2);
        rd = (points(3, 2) == points(4, 2) && y < points(3, 2)) || y < k(3) * x + b(3);
        dd = (points(4, 1) == points(1, 1) && x < points(1, 1)) || x < (y - b(4)) / k(4);
        ins = ud && ld && rd && dd;      
    end

    function dist = distance(p1, p2)
        dist = sqrt((p1(1) - p2(1)) ^ 2 + (p1(2) - p2(2)) ^ 2);
    end
    
end

