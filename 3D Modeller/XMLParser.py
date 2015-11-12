import xml.etree.ElementTree as ET
import numpy as np


def define_type(root):
    for child in root:
        if child.tag == 'Intrinsic':
            return 2
    return 1


def get_data_from_xml(source='', xml_type=-1):
    if not source:
        return
    tree = ET.parse(source=source)
    root = tree.getroot()
    internal, external, geometry = {}, {}, {}
    xml_type = define_type(root)
    if xml_type == 1:
        for child in root:
            at = child.attrib
            if child.tag == 'InternalCalibration':
                internal['dk'] = np.array(map(float, [at['dk1'], at['dk2']]))
                internal['dp'] = np.array(map(float, [at['dp1'], at['dp2']]))
                internal['fl'] = np.array(map(float, [at['flx'], at['fly']]))
                internal['pp'] = np.array(map(float, [at['ppx'], at['ppy']]))
                internal['s'] = float(at['s'])
            if child.tag == 'ExternalCalibration':
                external['pos'] = np.array(map(float, [at['tx'], at['ty'], at['tz']]))
                external['rot'] = np.array(map(float, [at['rx'], at['ry'], at['rz'], at['rw']]))
    if xml_type == 2:
        for child in root:
            at = child.attrib
            if child.tag == 'Intrinsic':
                internal['focal'] = float(at['focal'])
                internal['kappa'] = float(at['kappa1'])
                internal['c'] = np.array(map(float, [at['cx'], at['cy']]))
                internal['sx'] = float(at['sx'])
            if child.tag == 'Geometry':
                geometry['size'] = np.array(map(float, [at['width'], at['height']]))
                geometry['ncx'] = float(at['ncx'])
                geometry['nfx'] = float(at['nfx'])
                geometry['d'] = np.array(map(float, [at['dx'], at['dy']]))
                geometry['dp'] = np.array(map(float, [at['dpx'], at['dpy']]))
            if child.tag == 'Extrinsic':
                external['pos'] = np.array(map(float, [at['tx'], at['ty'], at['tz']]))
                external['rot'] = np.array(map(float, [at['rx'], at['ry'], at['rz']]))
    return xml_type, internal, external, geometry

if __name__ == '__main__':
    print get_data_from_xml(source='SOURCE-2.xml', xml_type=1)
    print get_data_from_xml(source='SOURCE.xml', xml_type=2)
