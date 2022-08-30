from generativepy.color import Color
from generativepy.formulas import rasterise_formula

rasterise_formula("create-png-1", r"e^{i \pi}+1 = 0", Color("red"), dpi=800)
rasterise_formula("create-png-2", r"\frac{\cancel{a}b}{\cancel{a}c} = 0", Color("green"), packages=["cancel"])
rasterise_formula("create-png-3", r"x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}", Color("black"))