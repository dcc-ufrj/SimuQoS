
# -*- coding: utf-8 -*-
import cairo, math, random

import cairoplot

data = [13, 30, 11, 25, 2]
x_labels = [ "jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008" ]
cairoplot.dot_line_plot( 'dot_line_3_series_legend.svg', data, 400, 300, x_labels = x_labels, 
                             axis = True, grid = True, x_title = "Tempo", y_title = "Nº de Peers", series_colors = [(1,0,0)])
