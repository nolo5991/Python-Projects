import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Function to define the parabola
def parabola(x, a):
    return -a * (x - 1) * (x - 5)

# Read the Excel file
file_path = "/home/noman/Documents/ratings.xlsx"
data = pd.read_excel(file_path)

def analyze_and_plot(data, aspect, title_suffix, color, linestyle):
    # Filter data for the given aspect
    aspect_data = data[data['rating_type'] == aspect]

    # Calculate Mean Opinion Score (MOS) and Standard Deviation for each stimuli ID
    summary = aspect_data.groupby('stimuli_ID')['rating'].agg(['mean', 'std']).reset_index()
    summary.rename(columns={'mean': 'MOS', 'std': 'StdDev'}, inplace=True)

    # Scatter data: MOS and StdDev
    x_scatter = summary['MOS']
    y_scatter = summary['StdDev']

    # Fit the parabola to the scatter data
    params, _ = curve_fit(parabola, x_scatter, y_scatter)
    a_estimate = params[0]  # Estimated value of a

    # Generate smooth parabola curve for plotting
    x_smooth = np.linspace(1, 5, 200)
    y_smooth = parabola(x_smooth, a_estimate)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.scatter(x_scatter, y_scatter, color=color, alpha=0.7, label=f'Stimuli Data Points ({aspect})')
    plt.plot(x_smooth, y_smooth, color='green', linewidth=2, linestyle=linestyle,
             label=f'Parabola: $y = -a(x-1)(x-5)$ (a={a_estimate:.2f})')

    # Add labels, title, and grid
    plt.title(f"SOS Analysis for Video {title_suffix} Ratings", fontsize=14)
    plt.xlabel("Mean Opinion Score (MOS)", fontsize=12)
    plt.ylabel("Standard Deviation (STD)", fontsize=12)
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.legend()
    plt.grid(False)
    plt.figtext(0.5, 0.01, f"Estimated a = {a_estimate:.4f}", ha="center", fontsize=10, color='black')

    # Set x-axis limit from 1 to 5
    plt.xlim(1, 5)

    # Show the plot
    plt.show()
# Analyze and plot for Appeal
analyze_and_plot(data, 'range_Appeal', "Appeal", "blue", "--")

# Analyze and plot for Quality
analyze_and_plot(data, 'range_Quality', "Quality", "red", "--")
