N_border, S_border = 110, 5
E_border, W_border = 7, 7
NS_border = N_border + S_border
EW_border = E_border + W_border
LD_edge = [S_border, E_border]
imgTownCenterPath = 'SOURCE-2.jpg'

GUI_header = '#:import east GUI_consts.E_border\n' \
             '#:import south GUI_consts.S_border\n' \
             '\n<GUILayout>:\n\tid: Layout\n\tcanvas:\n'

GUI_text_input = '\n\n\tTextInput:' \
                 '\n\t\tid: ImgPathInput' \
                 '\n\t\tsize: 200, 30' \
                 '\n\t\tcenter_x: east + self.width / 2' \
                 '\n\t\ttop: Layout.top' \
                 '\n\t\ttext: '

GUI_objects = '\n\n\tiButton:' \
              '\n\t\tid: BOpen' \
              '\n\t\tname: "BOpen"' \
              '\n\t\tsize: 95, 60' \
              '\n\t\tright: ImgPathInput.center_x - 5' \
              '\n\t\ttop: root.height - ImgPathInput.height - 10' \
              '\n\t\ttext: "OPEN"' \
              '\n\n\tiButton:' \
              '\n\t\tid: BReset' \
              '\n\t\tname: "BReset"' \
              '\n\t\tsize: 95, 60' \
              '\n\t\ttop: BOpen.top' \
              '\n\t\tright: BOpen.right + self.width + 10' \
              '\n\t\ttext: "RESET"' \
              '\n\n\tiButton:' \
              '\n\t\tid: BParallel' \
              '\n\t\tname: "BParallel"' \
              '\n\t\tsize: 100, 60 + 30 + 10' \
              '\n\t\ttop: Layout.top' \
              '\n\t\tright: BReset.right + 10 + self.width' \
              '\n\t\ttext: "Parallel lines\\n(0)"' \
              '\n\n\tiButton:' \
              '\n\t\tid: BPerpendicular' \
              '\n\t\tname: "BPerpendicular"' \
              '\n\t\tsize: 140, 100' \
              '\n\t\ttop: Layout.top' \
              '\n\t\tright: BParallel.right + 10 + self.width' \
              '\n\t\ttext: "Perpendicular lines\\n(0)"' \
              '\n\n\tiButton:' \
              '\n\t\tid: BWall' \
              '\n\t\tname: "BWall"' \
              '\n\t\tsize: 100, 47' \
              '\n\t\ttop: Layout.top' \
              '\n\t\tright: BPerpendicular.right + 10 + self.width' \
              '\n\t\ttext: "Walls (0)"' \
              '\n\n\tiButton:' \
              '\n\t\tid: BGround' \
              '\n\t\tname: "BGround"' \
              '\n\t\tsize: 100, 47' \
              '\n\t\ttop: Layout.top - 6 - BWall.height' \
              '\n\t\tright: BWall.right' \
              '\n\t\ttext: "Ground (None)"' \
              '\n\n\tiButton:' \
              '\n\t\tid: BSky' \
              '\n\t\tname: "BSky"' \
              '\n\t\tsize: 100, 100' \
              '\n\t\ttop: Layout.top' \
              '\n\t\tright: BWall.right + 10 + self.width' \
              '\n\t\ttext: "Sky (None)"' \
              '\n\n\tiButton:' \
              '\n\t\tid: BSave' \
              '\n\t\tname: "BSave"' \
              '\n\t\tsize: 100, 47' \
              '\n\t\ttop: Layout.top' \
              '\n\t\tright: BSky.right + 10 + self.width' \
              '\n\t\ttext: "Save data"' \
              '\n\n\tiButton:' \
              '\n\t\tid: BLoad' \
              '\n\t\tname: "BLoad"' \
              '\n\t\tsize: BSave.size' \
              '\n\t\ttop: Layout.top - 6 - BSave.height' \
              '\n\t\tright: BSave.right' \
              '\n\t\ttext: "Load data"' \
              '\n\n\tiButton:' \
              '\n\t\tid: BQuit' \
              '\n\t\tname: "BQuit"' \
              '\n\t\tsize: 96, 47' \
              '\n\t\ttop: Layout.top' \
              '\n\t\tright: BLoad.right + 10 + self.width' \
              '\n\t\ttext: "QUIT"' \
              '\n\n\tiButton:' \
              '\n\t\tid: BCalc' \
              '\n\t\tname: "BCalc"' \
              '\n\t\tsize: BQuit.size' \
              '\n\t\ttop: Layout.top - 6 - BQuit.height' \
              '\n\t\tright: BQuit.right' \
              '\n\t\ttext: "Calculate &\\n   Render"\n'

if __name__ == '__main__':
    print N_border, S_border, E_border, W_border
