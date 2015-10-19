function TMP(num)
    if num == 1
        matr = XmlToMatr('View_007.xml');
        image(imread('frame_0000.jpg'));
    else
        matr = tmp_calibration;
        image(imread('TownCenter2.jpg'))
    end
%     image(imread('TownCenter2.jpg'));
%    image(imread('frame_0000.jpg'));
    hold on;
    iPoint = [500; 500];
    wPoint = Img2World(iPoint, matr, [0 0 1 0]);
    wxPoint = wPoint;
    wxPoint(1) = wxPoint(1) + 10;
    wyPoint = wPoint;
    wyPoint(2) = wyPoint(2) + 10;
    ixPoint = matr * wxPoint;
    iyPoint = matr * wyPoint;
    ixPoint = Hom2Het(ixPoint);
    iyPoint = Hom2Het(iyPoint);
    line([iPoint(1), ixPoint(1)], [iPoint(2), ixPoint(2)], 'COLOR', 'BLUE');
    line([iPoint(1), iyPoint(1)], [iPoint(2), iyPoint(2)], 'COLOR', 'GREEN');
end

