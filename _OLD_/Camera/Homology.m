function Homology(xml_path, in_img_path, out_path)
    img = imread(in_img_path);
    [width, height, ~] = size(img);
    matr = XmlToMatr(xml_path);
    hor = FindHorizon(matr);
    k = -hor(2) / hor(1);
    b = -hor(3) / hor(1);
    min_x = 200;
    min_y = 200;
    max_x = width;
    max_y = height;
    oldPoints = [min_x min_x max_x max_x; min_y max_y min_y max_y];
%     oldPoints = [min_y min_y max_y max_y; min_x max_x min_x max_x];
%     oldPoints = [min_x max_x min_x max_x; min_y min_y max_y max_y];
    newPoints = Img2World(oldPoints, matr, [0 0 1 0]);
    for i=1:4  
        newPoints(:, i) = newPoints(:,i) / newPoints(4,i);
    end
    H = HomographySolve(oldPoints, newPoints(1:2, :));
    points = zeros((max_x - min_x + 1) * (max_y - min_y + 1), 2);
    l = 1;
    for i=min_x:max_x
        for j=min_y:max_y
            if OnGround(j, i)
                points(l,1) = i;
                points(l,2) = j;
                l = l + 1;
            end
        end
    end
%     
%     [xArray, yArray] = meshgrid(min_x : max_x, min_y : max_y);
%     mask = OnGround(xArray, yArray);
%     xArray = xArray(mask);
%     yArray = yArray(mask);
%     points = cat(2, xArray, yArray);
    
    newPoints = HomographyTransform(points', H);
    Xmin = min(newPoints(1,:));
    Xmax = max(newPoints(1,:));
    Ymin = min(newPoints(2,:));
    Ymax = max(newPoints(2,:));
    newWidth = Xmax - Xmin;
    newHeight = Ymax - Ymin;
    diff = 6000 / max(newWidth, newHeight);
    newWidth = fix(newWidth * diff);
    newHeight = fix(newHeight * diff);
    newPoints(1,:) = (newPoints(1,:) - Xmin) * diff;
    newPoints(2,:) = (newPoints(2,:) - Ymin) * diff;
    newImage = zeros(newHeight, newWidth, 3);
    l = 1;
    for i=min_x:max_x
        for j=min_y:max_y
            if OnGround(j, i)
                p = fix(newPoints(:,l)) + 1;
                newImage(p(2), p(1), 1:3) = img(i,j,1:3);
%                 newImage(p(2), p(1), 1:3) = img(points(l, 1),points(l, 2),1:3);
                l = l + 1;
            end
        end
    end
    
%     image(newImage);
    imwrite(newImage / 255, out_path);
    
    function og = OnGround(x, y)
        og = y < k * x + b;
    end
    
end

