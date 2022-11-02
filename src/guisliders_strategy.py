
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.axis import Axis
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models.blackscholes_strategy import BSOptStrat

class PlotGUI():
    def __init__(self, root, colorpalette = 'light') -> None:
        self.root = root
        self.root.title('Option strategy payoff calculator')
        self.root.geometry('1425x825')
        self.definepalette(colorpalette)
        self.guifont = 'Helvetica Neue'
        self.lframe_relief = "flat"  # "raised"
        self.rframe_relief = "flat"
        self.text_relief = "flat"
        self.text_font = (self.guifont, 20, "bold")
        self.label_relief = "flat"
        self.label_width = None
        self.label_height = 1
        self.label_font = (self.guifont, 14, "normal")
        self.entry_htick = 1
        self.entry_border = 0
        self.entry_width = 9
        self.entry_font = ("Helvetica Neue", 14, "normal")

        self.left_relx = 0.02
        self.left_rely = 0.02
        self.left_relwidth = 0.55
        self.setp_frame_lr = 0.01
