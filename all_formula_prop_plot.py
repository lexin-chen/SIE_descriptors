# This script generates multiple plots for fitting all charges using all 16 formulas and all 9 properties.
import modules as mod
import matplotlib.pyplot as plt
import time
from contextlib import suppress
import os

start = time.perf_counter()
file_name = f"csv/ions.csv"
formula_list = ["Q1R1", "Q1R2", "Q2R1", "Q2R2", "Q3R1","Q3R2", "Q4R1", "Q4R2", "Q5R1", "Q5R2", "Q6R1","Q6R2", "Q7R1", "Q7R2", "Q8R1", "Q8R2"]
property_list = ["dG", "dH", "viscosity", "diffusion", "gfet", "dlcst", "sn2", "activity", "lysozyme"]

if __name__ == "__main__":
    for per, property in enumerate(property_list):
        for each, formula in enumerate(formula_list):
            formula_func = getattr(mod.formulas, formula)
            df = mod.read_data(file_name, property, formula, by_charge=False)
            fig, ax = plt.subplots()
            with suppress(TypeError):
                prop, fit_data, parameters, SE = mod.fit_parameters(formula, formula_func, property, df)
                ax = mod.custom_axis(formula, property, ax)
                ax = mod.plot_all_charges(prop, fit_data, ax, df)
            dir_name = f"graphs/{property}"
            figure_name = f"{formula}_{property}"
            my_path = os.path.abspath(dir_name)
            fig.savefig(os.path.join(my_path, figure_name), bbox_inches = "tight", dpi = 300, transparent = True)
            plt.close()
            print(f"Finished with {formula}: {property}..")
end = time.perf_counter()
print(f'Finished in {round(end-start,2)} seconds')      # All charges takes 7.4 min on a regular laptop.