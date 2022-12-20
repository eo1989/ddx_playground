import pytest as pyt
from ../src/guisliders.py import PlotGUI


@pyt.fixture(scope="function")
def plot_fn():
    def _plot_fn():
     return _plot_fn

