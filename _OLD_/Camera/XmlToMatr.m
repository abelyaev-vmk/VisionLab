function matr = XmlToMatr( xml_path )
    xml = xmlread(xml_path);
    camera = xml.getElementsByTagName('Camera').item(0);
    namestr = char(camera.getAttributes.item(0));
    name = namestr(7:end-1);
    geometry = camera.getElementsByTagName('Geometry').item(0);
    Intrinsic = camera.getElementsByTagName('Intrinsic').item(0);
    Extrinsic = camera.getElementsByTagName('Extrinsic').item(0);
    
    [mImgWidth, mImgHeight, mNcx, mNfx, mDx, mDy, mDpx, mDpy] = ...
        geometryAttributes;
    
    [mFocal, mKappal, mCx, mCy, mSx] = intrinsicAttributes;
    
    [mTx, mTy, mTz, mRx, mRy, mRz] = extrinsicAttributes;
    
    pointW = [200; 200; 0; 1];
    
    Rt = getIKMatrix();
    pointC = Rt * pointW;
    pointC(:) = pointC(:) / pointC(3);
    pointU = [mFocal, 0, 0; 0, mFocal, 0; 0, 0, 1] * pointC;
    pointI = getOKMatrix * pointU;
    cPoint = checkPoint;
    
% % % % % % % %     
    matr = getFullMatrix;
% % % % % % % %     
    
    
    function [width, height, ncx, nfx, dx, dy, dpx, dpy] = ...
            geometryAttributes()
        gAtr = geometry.getAttributes;
        t = char(gAtr.item(0));
        dpx = str2double(t(6:end-1));
        t = char(gAtr.item(1));
        dpy = str2double(t(6:end-1));
        t = char(gAtr.item(2));
        dx = str2double(t(5:end-1));
        t = char(gAtr.item(3));
        dy = str2double(t(5:end-1));
        t = char(gAtr.item(4));
        height = str2double(t(9:end-1));
        t = char(gAtr.item(5));
        ncx = str2double(t(6:end-1));
        t = char(gAtr.item(6));
        nfx = str2double(t(6:end-1));
        t = char(gAtr.item(7));
        width = str2double(t(8:end-1));
    end
    
    function [focal, kappal, cx, cy, sx] = ...
            intrinsicAttributes()
        iAtr = Intrinsic.getAttributes;
        t = char(iAtr.item(0));
        cx = str2double(t(5:end-1));
        t = char(iAtr.item(1));
        cy = str2double(t(5:end-1));
        t = char(iAtr.item(2));
        focal = str2double(t(8:end-1));
        t = char(iAtr.item(3));
        kappal = str2double(t(9:end-1));
        t = char(iAtr.item(4));
        sx = str2double(t(5:end-1));
    end

    function [tx, ty, tz, rx, ry, rz] = ...
            extrinsicAttributes()
        eAtr = Extrinsic.getAttributes;
        t = char(eAtr.item(0));
        rx = str2double(t(5:end-1));
        t = char(eAtr.item(1));
        ry = str2double(t(5:end-1));
        t = char(eAtr.item(2));
        rz = str2double(t(5:end-1));
        t = char(eAtr.item(3));
        tx = str2double(t(5:end-1));
        t = char(eAtr.item(4));
        ty = str2double(t(5:end-1));
        t = char(eAtr.item(5));
        tz = str2double(t(5:end-1));
    end
    
    function matr = getIKMatrix()
        matr = zeros(3,4);
        
        sa = sin(mRx);
        ca = cos(mRx);
        sb = sin(mRy);
        cb = cos(mRy);
        sg = sin(mRz);
        cg = cos(mRz);

        matr(1,1) = cb * cg;
        matr(1,2) = cg * sa * sb - ca * sg;
        matr(1,3) = sa * sg + ca * cg * sb;
        matr(2,1) = cb * sg;
        matr(2,2) = sa * sb * sg + ca * cg;
        matr(2,3) = ca * sb * sg - cg * sa;
        matr(3,1) = -sb;
        matr(3,2) = cb * sa;
        matr(3,3) = ca * cb;

%         mCposx = -(mTx*matr(1,1) + mTy*matr(2,1) + mTz*matr(3,1));
%         mCposy = -(mTx*matr(1,2) + mTy*matr(2,2) + mTz*matr(3,2));
%         mCposz = -(mTx*matr(1,3) + mTy*matr(2,3) + mTz*matr(3,3));
        
        mCposx = mTx;
        mCposy = mTy;
        mCposz = mTz;
        
        matr(1,4) = mCposx;
        matr(2,4) = mCposy;
        matr(3,4) = mCposz;
    end

    function matr = getOKMatrix()
        matr = zeros(3,3);
        matr(1,1) = mSx / mDpx;
        matr(1,3) = mCx;
        matr(2,2) = 1 / mDpy;
        matr(2,3) = mCy;
        matr(3,3) = 1;
    end

    function point = checkPoint()
        m = getIKMatrix();
        xc = m(1,1) * pointW(1) + m(1,2) * pointW(2) ...
            + m(1,3) * pointW(3) + m(1,4);
        yc = m(2,1) * pointW(1) + m(2,2) * pointW(2) ...
            + m(2,3) * pointW(3) + m(2,4);
        zc = m(3,1) * pointW(1) + m(3,2) * pointW(2) ...
            + m(3,3) * pointW(3) + m(3,4);
        
        xu = mFocal * xc / zc;
        yu = mFocal * yc / zc;
        
        point(1) = xu * mSx / mDpx + mCx;
        point(2) = yu / mDpy + mCy;
        point(3) = 1;
    end

    function matr = getFullMatrix()
        matr = getOKMatrix * ...
            [mFocal, 0, 0; 0, mFocal, 0; 0, 0, 1] ...
            * getIKMatrix;
    end

end
