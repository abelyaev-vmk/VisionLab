function homographyImage = Homography(xml_path, in_img_path, out_path)
    outputSize = 1000;
    pixelSizeStart = 1;
    pixelSizeEnd = 3;
    img = imread(in_img_path);
    [height, width, ~] = size(img);
    matr = XmlToMatr(xml_path);
    hor = FindHorizon(matr);
    pos = FindCameraLocation(matr);
    k = -hor(2) / hor(1);
    b = -hor(3) / hor(1);
    min_h = 200;
    max_h = height;
    min_w = 1;
    max_w = width;
    oldPoints = [min_h min_h max_h max_h; min_w max_w max_w min_w];
    %%%
    oldPoints = oldPoints([2,1], :);
    %%%
    newPoints = Img2World(oldPoints, matr, [0 0 1 0]);
    newPoints = newPoints * [1/newPoints(4,1) 0 0 0;...
        0 1/newPoints(4,2) 0 0; 0 0 1/newPoints(4,3) 0; ...
        0 0 0 1/newPoints(4,4)];
    H = HomographySolve(oldPoints, newPoints(1:2, :));
    [hArr, wArr] = meshgrid(min_h:max_h, min_w:max_w);
    points = reshape(cat(2, hArr, wArr), [], 2)';
    %%%
    points = points([2,1], :);
    %%%
    planePoints = HomographyTransform(points, H);
    distances = distance(newPoints(1:2,:));
    Dmax = max(distances);
    Dmin = min(distances);
    Ddiff = Dmax - Dmin;
    Hmin = min(planePoints(1,:));
    Hmax = max(planePoints(1,:));
    Wmin = min(planePoints(2,:));
    Wmax = max(planePoints(2,:));
    newHeight = Hmax - Hmin;
    newWidth = Wmax - Wmin;
    Sdiff = outputSize / max(newHeight, newWidth);
    planePoints(1,:) = (planePoints(1,:) - Hmin) * Sdiff;
    planePoints(2,:) = (planePoints(2,:) - Wmin) * Sdiff;
    newHeight = fix(newHeight * Sdiff);
    newWidth = fix(newWidth * Sdiff);
    homographyImage = zeros(newHeight, newWidth, 3);
    for i=1:size(points,2)
        p = fix(planePoints(:, i)) + 1;

%%%!!!!!!! LINEAL FUNCTION NEEDED!!!

        now_size = round(2 * (distance(planePoints(:,i)) - Dmin) / Ddiff)
        
%%%%!!!!!
        color = img(points(2, i), points(1, i), :);
        pixelsH = max(1,p(2)-now_size):min(newHeight, p(2)+now_size);
        pixelsW = max(1,p(1)-now_size):min(newWidth, p(1)+now_size);
        homographyImage(pixelsH, pixelsW, 1) = color(1);
        homographyImage(pixelsH, pixelsW, 2) = color(2);
        homographyImage(pixelsH, pixelsW, 3) = color(3);
            
%         now_size = round(2 * (distance(planePoints(:,i)) - Dmin) / Ddiff);
%         now_size = 0;
%         SetPixel(p, img(points(2, i), points(1, i), :), now_size);
    end
    imwrite(homographyImage / 255, out_path);
    
    function SetPixel(point, color, size)
%         pixels = [max(1,point(2) - size):min(point(2) + size, newHeight),...
%             max(1,point(1) - size):min(point(1) + size, newWidth)]
        pixels = [max(1,point(1) - size):min(point(1) + size, newWidth),...
            max(1,point(2) - size):min(point(2) + size, newHeight)]
        homographyImage(pixels, 1) = color(1);
        homographyImage(pixels, 2) = color(2);
        homographyImage(pixels, 3) = color(3);
    end

    function dist = distance(vector)
        dist = sqrt((vector(1,:) - pos(1)).^2 + (vector(2,:) - pos(2)).^2);
    end
end

