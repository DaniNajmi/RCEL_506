import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib as mpl

# --- CONFIG AND STYLE ---
st.set_page_config(layout="wide")

TITLE = "The 10 Most-Watched Nonsports Entertainment Programs,\nRanked by Year"
COLORS = {
    "parade": "#4b2500",     # dark brown
    "awards": "#e9a7a7",     # soft pink
    "60m":    "#ddc7ae",     # beige
    "ncis":   "#7f9baa",     # muted blue
    "other":  "#e6e6e6",     # light gray
}

mpl.rcParams["font.family"] = "DejaVu Serif"
mpl.rcParams["figure.dpi"] = 150

# --- DATA ---
grid = [
    # rank 1 (top row)
    ["awards","awards","awards","awards","awards","other","awards","other","parade","parade","parade"],
    # rank 2
    ["other","other","other","other","other","awards","other","awards","other","awards","awards"],
    # rank 3
    ["awards","other","other","other","other","parade","parade","parade","other","other","other"],
    # rank 4
    ["parade","awards","awards","parade","parade","60m","other","other","other","60m","other"],
    # rank 5
    ["ncis","other","other","awards","awards","other","other","other","60m","60m","other"],
    # rank 6
    ["other","other","parade","60m","other","other","other","other","60m","60m","other"],
    # rank 7
    ["ncis","parade","other","other","other","other","other","60m","60m","60m","60m"],
    # rank 8
    ["ncis","other","ncis","other","other","other","awards","other","60m","60m","60m"],
    # rank 9
    ["ncis","ncis","ncis","60m","other","other","other","other","60m","60m","other"],
    # rank 10 (bottom row)
    ["ncis","other","other","ncis","other","other","other","other","awards","60m","60m"],
]

# year labeling at top to match
years = ["","2014", "", "’16", "", "’18", "", "’20", "", "’22", ""]  # 11 columns

# parameters

n_rows = 10
n_cols = 11

cell = 1.0          # base unit
gap = 0.2          # spacing between squares
rounding = 0.10     # corner roundness

# layout offsets
left_margin = 0.5
top_margin = 2.5
bottom_margin = 1

fig_w = left_margin + n_cols*(cell+gap) + 0.8
fig_h = top_margin + n_rows*(cell+gap) + bottom_margin

fig, ax = plt.subplots(figsize=(fig_w, fig_h))
ax.set_xlim(0, fig_w)
ax.set_ylim(0, fig_h)
ax.axis("off")

# title
ax.text(0, fig_h-0.2, TITLE, ha="left", va="top", fontsize=20, fontweight="bold")

# Legend
legend_y = fig_h-1.3
ax.text(0, legend_y, "Broadcasts:", ha="left", va="center", fontsize=10, fontweight="bold")

legend_items = [("Macy’s Parade","parade"), ("Academy Awards","awards"), ("“60 Minutes”","60m"), ("“NCIS”","ncis"), ("Other","other")]
lx = 2.6

# --- STREAMLIT INTERACTIVITY ---
st.sidebar.header("Filter View")
target_name = st.sidebar.selectbox(
    "Select Broadcast Type:",
    ["All", "Macy’s Parade", "Academy Awards", "“60 Minutes”", "“NCIS”", "Other"]
)

# Map selected name back to data keys
name_to_key = {"All": "All", "Macy’s Parade": "parade", "Academy Awards": "awards", "“60 Minutes”": "60m", "“NCIS”": "ncis", "Other": "other"}
selected_broadcast_type = name_to_key[target_name]

# --- PLOTTING FUNCTION ---
def plot_interactive_grid(selected_type):
    n_rows = 10
    n_cols = len(years)
    cell = 0.8
    gap = 0.15
    rounding = 0.1
    left_margin, top_margin, bottom_margin = 0.5, 2.5, 1

    fig_w = left_margin + n_cols*(cell+gap) + 0.8
    fig_h = top_margin + n_rows*(cell+gap) + bottom_margin

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    # Title
    ax.text(0, fig_h-0.2, TITLE, ha="left", va="top", fontsize=20, fontweight="bold")

    # Grid logic
    grid_top_y = fig_h - top_margin
    for r in range(n_rows):
        for c in range(n_cols):
            x0 = left_margin + c*(cell+gap)
            y0 = grid_top_y - (r+1)*(cell+gap) + gap
            
            key = grid[r][c] if r < len(grid) else "other"
            
            # Highlighting logic
            if selected_type == "All" or key == selected_type:
                facecolor = COLORS[key]
            else:
                facecolor = "#f2f2f2" # Faded

            ax.add_patch(FancyBboxPatch((x0, y0), cell, cell,
                                       boxstyle=f"round,pad=0,rounding_size={rounding}",
                                       linewidth=0, facecolor=facecolor))
    return fig

# Display the result
st.pyplot(plot_interactive_grid(selected_broadcast_type))
