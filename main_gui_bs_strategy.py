"""
Interactive option strategy payoff calculator w/ gui
options priced w/ BSM
"""

import tkinter as tk
from src.guisliders_strategy import PlotGUI

def main_gui():
	root = tk.Tk()
	colorpalette = "light"
	# colorpalette = "dark"
	Gui = PlotGUI(root, colorpalette)

	Gui.root.mainloop()


if __name__ == "__main__":
    main_gui()