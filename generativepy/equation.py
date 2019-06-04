# Author:  Martin McBride
# Created: 2019-05-12
# Copyright (C) 2019, Martin McBride
# License: MIT

import subprocess
import cairo


def getEquationImage(equation, tempfolder='/tmp/', dpi=300, tempname='__equation__'):
    with open(tempfolder + tempname + '.tex', 'w') as fp:

        fp.write(r'\documentclass[]{standalone}' + '\n')
        fp.write(r'\usepackage{amsmath}' + '\n')
        fp.write(r'\usepackage{varwidth}' + '\n')
        fp.write(r'\begin{document}' + '\n')
        fp.write(r'\begin{varwidth}{\linewidth}' + '\n')
        fp.write(r'\[ {' + equation + r'} \]' + '\n')
        fp.write(r'\end{varwidth}' + '\n')
        fp.write(r'\end{document}' + '\n')
    subprocess.run(['latex', '-output-directory', tempfolder, tempfolder + tempname + '.tex'])
    subprocess.run(['dvipng', '-D', str(dpi), '-bg', 'Transparent', '-o', tempfolder + tempname + '.png', tempfolder + tempname + '.dvi'])
    image = cairo.ImageSurface.create_from_png(tempfolder + tempname + '.png')
    return image
