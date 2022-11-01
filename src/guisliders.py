import cProfile
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
            width = self.ent_width,
            font = self.ent_font,
            bg = self.ent_bg,
            highlightthickness=self.ent_htick,
            borderwidth=self.ent_bordw)
        self.entry_T.rowconfigure(row, weight=1, minsize=6)
        self.entry_T.columnconfigure(0, weight=1, minsize=6)
        self.entry_T.grid(row = row, column = 1, padx = 20, pady = 10, sticky = "nsew")
        # default value
        self.entry_T.insert(0, 0.25)

        # Interest Rate
        row = row + 1
        self.label_r = tk.Label(master=self.framel,
                                text = 'Interest Rate (%)',
                                relief = self.lab_relief,
                                bg = self.lab_bg,
                                height = self.lab_height,
                                font = self.lab_font)
        self.label_r.rowconfigure(row, weight=1, minsize=15)
        self.label_r.columnconfigure(0, weight= 1, minsize=15)
        self.label_r.grid(row = row, column = 0, padx = 25, pady = 10, sticky="w")
        #
        self.entry_r = tk.Entry(master=self.framel,
                                width = self.ent_width,
                                font = self.ent_font,
                                bg = self.ent_bg,
                                highlightthickness=self.ent_htick,
                                borderwidth = self.ent_bordw)
        self.entry_r.rowconfigure(row, weight=1, minsize=6)
        self.entry_r.columnconfigure(0, weight = 1, minsize = 6)
        self.entry_r.grid(row = row, column=1, padx = 20, pady = 10, sticky="nsew")
        # default value
        self.entry_r.insert(0, 2)

        # volatility
        row = row + 1
        self.label_v = tk.Label(master=self.framel,
                                text = 'Volatility (%)',
                                relief = self.lab_relief,
                                bg = self.lab_bg,
                                height = self.lab_height,
                                font = self.lab_font)
        self.label_v.rowconfigure(row, weight=1, minsize=15)
        self.label_v.columnconfigure(0, weight= 1, minsize=15)
        self.label_v.grid(row = row, column = 0, padx = 25, pady = 10, sticky="w")
        #
        self.entry_r = tk.Entry(master=self.framel,
                                width = self.ent_width,
                                font = self.ent_font,
                                bg = self.ent_bg,
                                highlightthickness=self.ent_htick,
                                borderwidth = self.ent_bordw)
        self.entry_v.rowconfigure(row, weight=1, minsize=6)
        self.entry_v.columnconfigure(0, weight = 1, minsize = 6)
        self.entry_v.grid(row = row, column=1, padx = 20, pady = 10, sticky="nsew")
        # default value
        self.entry_v.insert(0, 30)

        # divvie yield
        row = row + 1
        self.label_q = tk.Label(master=self.framel,
                                text = 'Dividend Yield',
                                relief = self.lab_relief,
                                bg = self.lab_bg,
                                height = self.lab_height,
                                font = self.lab_font)
        self.label_q.rowconfigure(row, weight=1, minsize=15)
        self.label_q.columnconfigure(0, weight= 1, minsize=15)
        self.label_q.grid(row = row, column = 0, padx = 25, pady = 10, sticky="w")
        #
        self.entry_q = tk.Entry(master=self.framel,
                                width = self.ent_width,
                                font = self.ent_font,
                                bg = self.ent_bg,
                                highlightthickness=self.ent_htick,
                                borderwidth = self.ent_bordw)
        self.entry_q.rowconfigure(row, weight=1, minsize=25)
        self.entry_q.columnconfigure(0, weight = 1, minsize = 25)
        self.entry_q.grid(row = row, column=1, padx = 20, pady = 10, sticky="nsew")
        # default value
        self.entry_q.insert(0, 0)

        # Button calculate option
        row = row + 1
        self.button = tk.Button(master=self.framel,
                                text = "Calculate",
                                highlightthickness=0,
                                borderwidth=0,
                                font = self.lab_font,
                                command = self.computeoption,
                                )




# -----------------------------------------
#               definitions
# -----------------------------------------

    def get_CP(self):
        CP = str(self.entry_CP.get())
        if CP not in ["C", "P"]:
            messagebox.showerror("Option type error", "Enter either 'C' or 'P' in the Call/Put field")
        else:
            return CP

    def get_K(self):
        try:
            K = float(self.entry_K.get())
            if K < 1:
                messagebox.showerror("Strike value error", "Enter at least a strike price equal to 1")
            else:
                return K
        except:
            messagebox.showerror("Strike value error", "Enter a valid strike price")

    def get_T(self):
        '''
        Get the Maturity entry
        '''
        try:
            T = float(self.entry_T.get())
            if T < 0:
                # Returns error if a negative maturity is entered
                messagebox.showerror("Maturity value error", "Enter a maturity at least equal to 0 (expiration)")
            elif T > 5:
                # Returns a maximum maturity of 5 years
                messagebox.showerror("Maturity value error", "Enter a maturity at least equal to 5 (years)")
            else:
                return T
        except:
            messagebox.showerror("Maturity value error", "Enter a valid maturity value (between 0 and 5 years)")


    def get_r(self):
        '''
        Get the Interest Rate entry
        '''
        try:
            r = float(self.entry_r.get())
            if r < 0.01:
                # Returns a mininum of 0.01% (1 basis point)
                messagebox.showerror("Interest Rate value error", "Enter at least an interest rate equal to 0.01(%)")
            elif r > 10:
                # Returns a maximum interest rate of 10% (1000 basis point)
                messagebox.showerror("Interest Rate value error", "Enter at least an interest rate equal to 10(%)")
            else:
                return r / 100
        except:
            messagebox.showerror("Interest Rate value error", "Enter a valid interest rate value (between 0.01% and 10%)")


    def get_v(self):
        '''
        Get the Volatility entry
        '''
        try:
            v = float(self.entry_v.get())
            if v < 1:
                # Returns a mininum volatility of 1%
                messagebox.showerror("Volatility value error", "Enter at least a volatility equal 1(%)")
            elif v > 100:
                # Return a maximum volatility of 100%
                messagebox.showerror("Volatility value error", "Enter at least a volatility equal 100(%)")
            else:
                return v / 100
        except:
            messagebox.showerror("Volatility value error", "Enter a valid volatility value (between 1% and 100%)")


    def get_q(self):
        '''
        Get the Dividend Yield entry
        '''
        try:
            q = float(self.entry_q.get())
            if q < 0:
                # If a negative dividend yield is entered, then return 0
                messagebox.showerror("Dividend Yield value error", "Enter at least a dividend yield equal 0(%)")
            else:
                return q
        except:
            messagebox.showerror("Dividend Yield value error", "Enter a valid dividend yield value")


    @staticmethod
    def get_Smin(K) -> None:
        """
        Automatic generation of a minimum underlying price (for plot)
        calculated as 60% below the input strike price
        """
        return round(K*(1 - 0.6), 0)


    @staticmethod
    def get_Smax(K) -> None:
        return round(K*(1 + 0.6), 0)

    @staticmethod
    def get_Sset(Smin, Smax) -> np.ndarray:  # double check this return type!!
        return np.linspace(Smin, Smax, 150)

    def define_slider(self, sliderax, labl = "Slider", vmin = 0, vmax = 1, vstp = 0.1, vini = 0.5):
        return Slider(ax = sliderax,
                      label = labl,
                      valmin = vmin,
                      valmax = vmax,
                      valstep = vstp,
                      valinit = vini,
                      color = 'gray',
                      initcolor = 'gray')

    def computeoption(self):
        self.CP = self.get_CP()
        self.K = self.get_K()
        self.T = self.get_T()
        self.r = self.get_r()
        self.v = self.get_v()
        self.q = self.get_q()
        self.Smin = self.get_Smin(self.K)
        self.Smax = self.get_Smax(self.K)
        self.Sset = self.get_Sset(self.Smin, self.Smax)

        # calc the option
        self.option = [BSOpt(self.CP, s, self.K, self.T, self.r, self.v, q = self.q) for s in self.Sset]

        # update description
        self.updatedescription()

        # plot the option price and greeks
        self.plotoption()


    def updatedescription(self):
        # message 1: update call or put price according to data entry
        auxoption = "Call" if self.CP == "C" else "Put"
        self.message1 = '''The BSM ''' + auxoption + ''' price is given by:'''
        self.text_box1.configure(text = self.message1)

        # image 1: update formula for the option
        if auxoption == "Call""":
            pass
        else:
