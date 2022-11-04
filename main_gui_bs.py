"""
Interactive BSM prices and greeks plot using matplotlib sliders on a tkinter GUI
"""

import tkinter as tk
from src.guisliders import PlotGUI


def main_gui():
    root = tk.Tk()
	Gui = PlotGUI(root)
	Gui.root.mainloop()


if __name__ == "__main__":
    main_gui()