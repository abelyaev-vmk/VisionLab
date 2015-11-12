%% GETCALIBRATIONMATRIXFROMXML Summary of this function goes here
% Computes camera's calibration matrix from .xml file
%% Syntax
% calibrationMatrix = GetCalibrationMatrixFromXml(xml_path, xml_type)
%% Description
% GetCalibrationMatrixFromXml computes camera's calibration matrix from 
% xml_path file with specified type xml_type
%
% * calibrationMatrix is a camera's calibration matrix 3x4
% * xml_path is a path to .xml file
% * xml_type is a type of .xml file
%       xml_type = 'q', if data is in the form of quaternion
%       xml_type = 'd', if data is in the normal form
%
% 
% **quaternion form: 
%  <Camera name="camera">
%   <InternalCalibration dk1="" dk2="" dp1="" dp2="" 
%                        flx="" fly="" ppx="" ppy="" s=""/>
%   <ExternalCalibration rw="" rx="" ry="" rz="" tx="" ty="" tz=""/>
%  </Camera>
%  , where
%     dk1, dk2 = DistortionK1, DistortionK2
%     dp1, dp2 = DistortionP1, DistortionP2
%     flx, fly = FocalLengthX, FocalLengthY
%     ppx, ppy = PrinciplePointX, PrinciplePointY
%     s = Skew
%     rw, rx, ry, rz = RotationW, RotationX, RotationY, RotationZ
%     tx, ty, tz = TranslationX, TranslationY, TranslationZ
% 
% **normal form:
%  <Camera name="">
%   <Geometry width="" height="" ncx="" nfx="" dx="" dy="" dpx="" dpy=""/>
%   <Intrinsic focal="" kappa1="" cx="" cy="" sx=""/>
%   <Extrinsic tx="" ty="" tz="" rx="" ry="" rz=""/>
%  </Camera>
%  , where 
%     width, height - size of image
%     ncx - number of sensor elements in camera's x direction (in sels),
%     nfx - number of pixels in frame grabber's x direction (in pixels),
%     dx  - X dimension of camera's sensor element (in mm/sel),
%     dy  - Y dimension of camera's sensor element (in mm/sel),
%     dpx - effective X dimension of pixel in frame grabber (in mm/pixel), and
%     dpy - effective Y dimension of pixel in frame grabber (in mm/pixel).
%     focal  - effective focal length of the pin-hole camera,
%     kappa1 - 1st order radial lens distortion coefficient,
%     Cx, Cy - coordinates of center of radial lens distortion -and-
%              the piercing point of the camera coordinate frame's
%              Z axis with the camera's sensor plane,
%     sx  - scale factor to account for any uncertainty in the
%           framegrabber's resampling of the horizontal scanline.
%     Rx, Ry, Rz - rotation angles for the transform between the
%                  world and camera coordinate frames,
%     Tx, Ty, Tz - translational components for the transform between the
%                  world and camera coordinate frames.

%% See also
% GetCalibrationMatrixFromXml


function calibrationMatrix = GetCalibrationMatrixFromXml( xml_path, xml_type )
    xml = xmlread(xml_path);
    camera = xml.getElementsByTagName('Camera').item(0);
    if xml_type == 'd'
        calibrationMatrix = normalXml;
    else
        if xml_type == 'q'
            calibrationMatrix = quaternionXml;
        else
            display('Invalid xml_type');
        end
    end


    function matr = normalXml()
        geometry = camera.getElementsByTagName('Geometry').item(0);
        Intrinsic = camera.getElementsByTagName('Intrinsic').item(0);
        Extrinsic = camera.getElementsByTagName('Extrinsic').item(0);
        [mImgWidth, mImgHeight, mNcx, mNfx, mDx, mDy, mDpx, mDpy] = ...
            geometryAttributes;
        [mFocal, mKappal, mCx, mCy, mSx] = intrinsicAttributes;
        [mTx, mTy, mTz, mRx, mRy, mRz] = extrinsicAttributes;
        matr = getFullMatrix();
        
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

        function matr = getFullMatrix()
            matr = getOKMatrix * ...
                [mFocal, 0, 0; 0, mFocal, 0; 0, 0, 1] ...
                * getIKMatrix;
            disp(getOKMatrix * ...
                [mFocal, 0, 0; 0, mFocal, 0; 0, 0, 1])
            disp(getIKMatrix)
      
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

%                 mCposx = -(mTx*matr(1,1) + mTy*matr(2,1) + mTz*matr(3,1));
%                 mCposy = -(mTx*matr(1,2) + mTy*matr(2,2) + mTz*matr(3,2));
%                 mCposz = -(mTx*matr(1,3) + mTy*matr(2,3) + mTz*matr(3,3));

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
        end    
    end

    function matr = quaternionXml()
        iC = camera.getElementsByTagName('InternalCalibration').item(0);
        eC = camera.getElementsByTagName('ExternalCalibration').item(0);
        [cFlx, cFly, cPpx, cPpy, cS, cDk1, cDk2, cDp1, cDp2] = internalAttributes;
        [cTx, cTy, cTz, cRx, cRy, cRz, cRw] = externalAttributes;
        matr = getMatrix();
        
        function [flx, fly, ppx, ppy, s, dk1, dk2, dp1, dp2] = ...
                internalAttributes()
            iAtr = iC.getAttributes;
            t = char(iAtr.item(0));
            dk1 = str2double(t(6:end-1));
            t = char(iAtr.item(1));
            dk2 = str2double(t(6:end-1));
            t = char(iAtr.item(2));
            dp1 = str2double(t(6:end-1));
            t = char(iAtr.item(3));
            dp2 = str2double(t(6:end-1));
            t = char(iAtr.item(4));
            flx = str2double(t(6:end-1));
            t = char(iAtr.item(5));
            fly = str2double(t(6:end-1));
            t = char(iAtr.item(6));
            ppx = str2double(t(6:end-1));
            t = char(iAtr.item(7));
            ppy = str2double(t(6:end-1));
            t = char(iAtr.item(8));
            s = str2double(t(4:end-1));
        end
        
        function [tx, ty, tz, rx, ry, rz, rw] = ...
                externalAttributes()
            eAtr = eC.getAttributes;
            t = char(eAtr.item(0));
            rw = str2double(t(5:end-1));
            t = char(eAtr.item(1));
            rx = str2double(t(5:end-1));
            t = char(eAtr.item(2));
            ry = str2double(t(5:end-1));
            t = char(eAtr.item(3));
            rz = str2double(t(5:end-1));
            t = char(eAtr.item(4));
            tx = str2double(t(5:end-1));
            t = char(eAtr.item(5));
            ty = str2double(t(5:end-1));
            t = char(eAtr.item(6));
            tz = str2double(t(5:end-1));
        end
        
        function matr = getMatrix()
            K = [cFlx, tan(cS) * cFly, cPpx;
                 0, cFly, cPpy;
                 0, 0, 1]
%             alpha = 1 / cRw;
%             direction = [cRx; cRy; cRz];
%             direction = direction ./ sun(direction .* direction);
%             R_x = [0 -direction(3) direction(2);
%                    direction(3) 0 -direction(1);
%                    -direction(2) direction(1) 0];
%             R = eye(3) + sin(alpha) * R_x + (1 - cos(alpha)) * R_x * R_x;
            t = [cTx; cTy; cTz];
            R = [1.0 - 2.0 * (cRy ^ 2 + cRz ^ 2), ...
                 2.0 * (cRx * cRy - cRz * cRw), ...
                 2.0 * (cRx * cRz + cRy * cRw); ...
                 2.0 * (cRx * cRy + cRz * cRw), ...
                 1.0 - 2.0 * (cRx ^ 2 + cRz ^ 2), ...
                 2.0 * (cRy * cRz - cRx * cRw); ...
                 2.0 * (cRx * cRz - cRy * cRw), ...
                 2.0 * (cRy * cRz + cRx * cRw), ...
                 1.0 - 2.0 * (cRx ^ 2 + cRy ^ 2)]
             disp([R, -R * t]);
            matr = K * [R, -R * t];
        end
        
    end
end

