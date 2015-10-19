function matrix = CoordinatesConvertion(name)
    xml = xmlread(name);
    camera = xml.getElementsByTagName('Camera').item(0);
    ext = camera.getElementsByTagName('Extrinsic').item(0);
    [mTx, mTy, mTz, mRx, mRy, mRz] = extrinsicAttributes;
    ox = TurnOX(mRx);
    oy = TurnOY(mRy);
    oz = TurnOZ(mRz);
    matrix = ox * oy * oz;
    SaveMatrix(matrix, 'View.txt'); 
    
    
    function [tx, ty, tz, rx, ry, rz] = ...
            extrinsicAttributes()
        eAtr = ext.getAttributes;
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
    
    
end

function oxt = TurnOX(fi)
    oxt = [1, 0, 0, 0; 0, cos(fi), sin(fi), 0; 0, -sin(fi), cos(fi), 0; 0, 0, 0, 1];
end

function oyt = TurnOY(fi)
    oyt = [cos(fi) 0 sin(fi) 0; 0 1 0 0; -sin(fi) 0 cos(fi) 0; 0 0 0 1];
end

function ozt = TurnOZ(fi)
    ozt = [cos(fi) sin(fi) 0 0; -sin(fi) cos(fi) 0 0; 0 0 1 0; 0 0 0 1];
end

function CC(x,y,z)
    matr = TurnOX(x) * TurnOY(y) * TurnOZ(z);
end

    
