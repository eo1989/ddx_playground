import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt

plt.style.use("seaborn-dark")

from models.blackscholes import BSOpt


class PlotGUI:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Black Scholes playground")
        self.root.geometry("1350x850")
        self.mainbg = "#E0DFDF"
        self.root.configure(bg=self.mainbg)

        # Left Frame
        self.framel = tk.Frame(
            master=self.root, relief="flat", bg=self.mainbg, borderwidth=1
        )
        self.framel.place(relx=0.02, rely=0.02, relwidth=0.23, relheight=0.95)

        # label setup
        self.lab_relief = "flat"
        self.lab_bg = self.mainbg
        self.lab_height = 1
        self.lab_font = ("Helvetica Neue", 14, "normal")

        # Entry setup
        self.ent_htick = (2,)
        self.ent_bordw = 0
        self.ent_width = 13
        self.ent_font = ("Helvetica Neue", 14, "normal")
        self.ent_bg = "whitesmoke"

        # call or put
        row = 0
        self.label_CP = tk.Label(
            master=self.framel,
            text="Call or Put (C/P)",
            relief=self.lab_relief,
            bg=self.lab_bg,
            height=self.lab_height,
            font=self.lab_font,
        )
        self.label_CP.rowconfigure(row, weight=1, minsize=15)
        self.label_CP.columnconfigure(0, weight=1, minsize=15)
        self.label_CP.grid(row=row, column=0, padx=25, pady=(45, 10), sticky="w")
        self.entry_CP = tk.Entry(
            master=self.framel,
            width=self.ent_width,
            font=self.ent_font,
            bg=self.ent_bg,
            highlightthickness=self.ent_htick,
            borderwidth=self.ent_bordw,
        )
        self.entry_CP.rowconfigure(row, weight=1, minsize=15)
        self.entry_CP.columnconfigure(0, weight=1, minsize=15)
        self.entry_CP.grid(row=row, column=1, padx=20, pady=(45, 10), sticky="nsew")
        # default value
        self.entry_CP.insert(0, "C")

        # Strike price
        row = row + 1
        self.label_K = tk.Label(
            master=self.framel,
            text="Strike Price",
            relief=self.lab_relief,
            bg=self.lab_bg,
            height=self.lab_height,
            font=self.lab_font,
        )
        self.label_K.rowconfigure(row, weight=1, minsize=15)
        self.label_K.columnconfigure(0, weight=1, minsize=15)
        self.label_K.grid(row=row, column=0, padx=25, pady=10, sticky="w")
        #
        self.entry_K = tk.Entry(
            master=self.framel,
            width=self.ent_width,
            font=self.ent_font,
            bg=self.ent_bg,
            highlightthickness=self.ent_htick,
            borderwidth=self.ent_bordw,
        )
        self.label_K.rowconfigure(row, weight=1, minsize=6)
        self.label_K.columnconfigure(0, weight=1, minsize=6)
        self.label_K.grid(row=row, column=1, padx=20, pady=10, sticky="nsew")
        # default value
        self.entry_K.insert(0, 100)

        # Maturity
        row = row + 1
        self.label_T = tk.Label(
            master=self.framel,
            text="Maturity (Years)",
            relief=self.lab_relief,
            bg=self.lab_bg,
            height=self.lab_height,
            font=self.lab_font,
        )
        self.label_T.rowconfigure(row, weight=1, minsize=15)
        self.label_T.columnconfigure(0, weight=1, minsize=15)
        self.label_T.grid(row=row, column=0, padx=25, pady=10, sticky="w")
        #
        self.entry_T = tk.Entry(
            master=self.framel,
        )
