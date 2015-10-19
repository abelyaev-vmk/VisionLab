function HorizontIntersect( matr, img_path, COLOR )
%HORIZONTINTERSECT Summary of this function goes here
%   Detailed explanation goes here
    horizont = FindHorizon(matr);
%     TownCenter2
    points1 = [1 531, 1159 1];
    points2 = [765 1080, 1801 1];
    
% % VIEW007
%     points1 = [401 199 610 139];
%     points2 = [657 182 704 129];
    
    k1 = (points1(2) - points1(4)) / (points1(1) - points1(3));
    b1 = points1(2) - k1 * points1(1);
%     points2 = [1080, 765; 1, 1801];
%     points2(1:2:3) = 1081 - points2(1:2:3);
    k2 = (points2(2) - points2(4)) / (points2(1) - points2(3));
    b2 = points2(2) - k2 * points2(1);

    
    
    
    
    x = 1:10000;
    y1 = k1 * x + b1;
    y2 = k2 * x + b2;
     xlabel('x');
    ylabel('y');
    img = imread(img_path);
    image(img);
    
    line(x, y1, 'COLOR', 'RED');
    hold on;
   
    line(x, y2);
    
    k_hor = -(horizont(1) / horizont(2));
    b_hor = -horizont(3) / horizont(2);
%     b_hor = 0;
    
    y_hor = k_hor * x + b_hor;
    line(x, y_hor, 'Color', COLOR);
    
%     plot(points1(1), points1(2), points1(3), points1(4), '-');
end

