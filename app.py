import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib as mpl

# --- STYLE & CONFIG ---
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

years = ["","2014", "", "’16", "", "’18", "", "’20", "", "’22", ""]
legend_items = [("Macy’s Parade","parade"), ("Academy Awards","awards"), ("“60 Minutes”","60m"), ("“NCIS”","ncis"), ("Other","other")]
note = "Note: Academy Awards programs also include red carpet broadcasts.   Source: Nielsen   By The New York\ntimes"

# --- SIDEBAR INTERFACE ---
st.sidebar.header("Navigation")
selected_broadcast_name = st.sidebar.selectbox(
    "Select the Broadcast Type Desired:",
    options=["All", "Macy’s Parade", "Academy Awards", "“60 Minutes”", "“NCIS”", "Other"]
)

# Mapping back to keys
name_to_key = {"All": "All", "Macy’s Parade": "parade", "Academy Awards": "awards", "“60 Minutes”": "60m", "“NCIS”": "ncis", "Other": "other"}
selected_broadcast_type = name_to_key[selected_broadcast_name]

# --- PLOTTING FUNCTION ---
def plot_interactive_grid(selected_type):
    n_rows = 10
    n_cols = len(years)
    cell = 0.8
    gap = 0.1
    rounding = 0.1
    
    # original layout offsets
    left_margin = 1
    top_margin = 2
    bottom_margin = 1.3

    fig_w = left_margin + n_cols*(cell+gap) + 0.8
    fig_h = top_margin + n_rows*(cell+gap) + bottom_margin

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    # 1. Title
    ax.text(0, fig_h-0.2, TITLE, ha="left", va="top", fontsize=20, fontweight="bold")

    # 2. Legend Subtitles
    legend_y = fig_h-1.3
    ax.text(0, legend_y, "Broadcasts:", ha="left", va="center", fontsize=13, fontweight="bold")
    lx = 2.6
    for name, key in legend_items:
        # colored square
        ax.add_patch(FancyBboxPatch((lx, legend_y-0.18), 0.35, 0.35,
                                   boxstyle=f"round,pad=0,rounding_size=0.05",
                                   linewidth=0, facecolor=COLORS[key]))
        # legend text
        l_color = ("#4b2500" if key == "parade" else ("#e9a7a7" if key=="awards" else ("#ddc7ae" if key=="60m" else ("#7f9baa" if key=="ncis" else "#e6e6e6"))))
        ax.text(lx+0.5, legend_y, name, ha="left", va="center", fontsize=12, color=l_color)
        lx += 2.45 if key!="parade" else 2.2

    grid_top_y = fig_h - top_margin
    
    # 3. Year labels (Top)
    for c, year in enumerate(years):
        x = left_margin + c*(cell+gap) + cell/2
        ax.text(x, grid_top_y + 0.40, year, ha="center", va="center", fontsize=12, color="#6b6b6b")

    # 4. Rank Labels (Left) and Tiles
    for r in range(n_rows):
        rank = r+1
        y_center = grid_top_y - r*(cell+gap) - cell/2
        ax.text(left_margin-0.2, y_center, str(rank), ha="right", va="center", fontsize=12, color="#6b6b6b")

        for c in range(n_cols):
            x0 = left_margin + c*(cell+gap)
            y0 = grid_top_y - (r+1)*(cell+gap) + gap
            key = grid[r][c]
            
            # Interactive Highlighting logic
            if selected_type == 'All' or key == selected_type:
                tile_facecolor = COLORS[key]
            else:
                tile_facecolor = "#f2f2f2" # Neutral faded gray

            ax.add_patch(FancyBboxPatch((x0, y0), cell, cell,
                                       boxstyle=f"round,pad=0,rounding_size={rounding}",
                                       linewidth=0, facecolor=tile_facecolor))

    # 5. Footnote (Bottom)
    ax.text(0, 0.6, note, ha="left", va="bottom", fontsize=14, color="#6b6b6b")

    return fig

st.pyplot(plot_interactive_grid(selected_broadcast_type))
