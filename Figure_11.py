import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter, LogLocator
import pandas as pd
import textwrap
import sys,os
dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(dir)

# path to file to save results to (*.csv)
#in_file = f"{parent_dir}\\results\\figure_14_table_3_data.csv"
in_file = f"{dir}\\results\\figure_14_table_3_data_for_figure.csv"
out_img = f"{dir}\\results\\figure_14.png"

# create formatter to label x axes
from matplotlib.ticker import FuncFormatter

def shift_first_tick(x, pos):
    if x == 1000:
        return "   1000"   # add leading spaces to push it right
    return f"{int(x)}"

# obtain the data
df = pd.read_csv(in_file)

# Create figure
fig = plt.figure(figsize=(5.833, 3))

# Define grid specifications and labels
row_n = 2
col_n = 4

row_lbl = ["original to\nsimplified","simplified\nto original"]
col_lbl = ["Lower Manhattan","Lake Shelbyville","Cannonball River","India-Bangladesh Border"]
data_lbl = ["manhattan","lake_shelbyville","cannonball","india_bangladesh"]

# Create GridSpec with extra column for row labels

#gs = gridspec.GridSpec(nrows=row_n, ncols=col_n + 1, width_ratios=[0.4] + [1] * col_n, wspace=0.5, hspace=0.3)
gs = gridspec.GridSpec(
    nrows=row_n,
    ncols=col_n + 1,
    width_ratios=[0.25] + [1] * col_n,
    wspace=0.15,
    hspace=0.05
)
ax_list = []
spine_color="0.35"
# Create subplots and add labels
for i in range(row_n):
    for j in range(col_n):
        ax = fig.add_subplot(gs[i, j+1])  # Skip first column for row labels
        ax_list.append(ax)
        # obtain data for this plot
        feat_data = df[df["feature"] == data_lbl[j]]
        if i == 0:
            feat_data = feat_data[feat_data["direction"] == "orig_to_simp"]
        else:
            feat_data = feat_data[feat_data["direction"] == "simp_to_orig"]
        
        true_val = float(feat_data.loc[feat_data['method'] == 'exact','d_avg'].values[0])
        true_time = float(feat_data.loc[feat_data['method'] == 'exact','elapsed_sec'].values[0])
        
        # axis properties
        ax.set_xscale('log')
        ax.tick_params(axis = 'y',labelsize = 7)
        ax.tick_params(
            axis = 'both',
            which = 'minor',
            bottom = False,
            left = False,
            top = False
        )
        ax.tick_params(
            axis='both',
            color=spine_color,
            labelcolor="black"
            )

        ax.set_ylim(-10,200)
        ax.axhline(y = 0,color = spine_color,linewidth = 0.8)
        ax.set_xticks([])
        ax.invert_xaxis()
        ax.spines['bottom'].set_visible(False)
        for spine in ax.spines.values():
            spine.set_color(spine_color)
            spine.set_zorder(0)

        # axis tick marks        
        ax_2 = ax.twiny()
        ax_2.set_xscale('log')
        ax_2.minorticks_off()

        ax_2.patch.set_visible(False)
        ax_2.set_zorder(-10)

        ax_2.set_xlim(ax.get_xlim())
        ax_2.spines['top'].set_position(('data',0))
        ax_2.spines['top'].set_visible(True)
        ax_2.spines['bottom'].set_visible(False)
        for spine in ax_2.spines.values():
            spine.set_color(spine_color)
            spine.set_zorder(0)

        #ax_2.xaxis.set_major_formatter(ScalarFormatter())
        ax_2.xaxis.set_major_formatter(FuncFormatter(shift_first_tick))
        ax_2.set_ylim(-10,200)
        ax_2.set_xticks([1,10,100,1000])
        
        ax_2.xaxis.set_ticks_position('top')        
        ax_2.xaxis.set_label_position('top')
        

        ax_2.tick_params(
            axis='x',
            which='major',
            labelsize=7,
            pad=-15,
            direction='in',
            bottom=False,
            top=True,
            color=spine_color,
            labelcolor='black'
        )

        # plot vertex to vertex data
        v_data = feat_data[(feat_data["method"] == "vrt_to_vrt") & (feat_data["elapsed_sec"] <= true_time)]
        x = v_data["spacing"].astype(float).tolist()
        y = v_data["d_avg"].astype(float).tolist()
        y = [100 * (val - true_val) / true_val for val in y]
        ax.plot(x,y,
                marker = 'o',
                ms=1.5,
                mec = 'black',
                mfc = 'black',
                linestyle = 'None',
                label = r'$\bar{d}_{v(A)→v(B)}$')

        v_data = feat_data[(feat_data["method"] == "vrt_to_vrt") & (feat_data["elapsed_sec"] > true_time)]
        x = v_data["spacing"].astype(float).tolist()
        y = v_data["d_avg"].astype(float).tolist()
        y = [100 * (val - true_val) / true_val for val in y]
        ax.plot(x,y,
                marker = 'o',
                ms = 3,
                mew = 0.8,
                mec = 'black',
                mfc = 'white',
                linestyle = 'None',
                zorder=3,
                clip_on = False    
        )
        

        # plot vertex to polyline data
        v_data = feat_data[(feat_data["method"] == "vrt_to_line") & (feat_data["elapsed_sec"] <= true_time)]
        x = v_data["spacing"].astype(float).tolist()
        y = v_data["d_avg"].astype(float).tolist()
        y = [100 * (val - true_val) / true_val for val in y]
        ax.plot(x,y, 
                marker = '>',
                ms = 1.5,
                mec = 'black',
                mfc = 'black',
                linestyle = 'None',
                label = r"$\bar{d}_{v(A)→B}$")

        v_data = feat_data[(feat_data["method"] == "vrt_to_line") & (feat_data["elapsed_sec"] > true_time)]
        x = v_data["spacing"].astype(float).tolist()
        y = v_data["d_avg"].astype(float).tolist()
        y = [100 * (val - true_val) / true_val for val in y]
        ax.plot(x,y, 
                marker = '>',
                ms = 2.5,
                mew = 0.8,
                mec = 'black',
                mfc = 'white',
                linestyle = 'None',
                zorder=3,
                clip_on = False    
            )

        # # plot polyline 2 polyline values
        # x = [true_time]
        # y = [0]
        # ax.plot(x,y,marker = '+',color = 'white',markersize = 14, linestyle = 'None',label = "A→B")
        # ax.plot(x,y,marker = '+',color = 'black',markersize = 8, linestyle = 'None',label = "A→B")

        # axis labels
        if j == 0:
            if i  == 0:
                # place "% error" inside the axis, above the top tick
                ax.text(
                    -0.08, 1.05,
                    "% error",
                    ha="right", va="bottom",
                    fontsize=7,
                    fontstyle="italic",
                    transform=ax.transAxes
                )
        else:
            ax.set_yticklabels([])
        
        # column labels
        if i == 0:
            lbl = textwrap.wrap(col_lbl[j],width = len(col_lbl[j]) - 3)
            lbl = "\n".join(lbl)
            ax.set_title(lbl, fontsize=7)
            ax_2.set_xticklabels([])
        else:
            #ax.set_xlabel("spacing (m)",fontsize = 8,fontstyle = "italic",labelpad = 10)
            pass
            
    # Add row label in the first column
    label_ax = fig.add_subplot(gs[i, 0])
    label_ax.axis('off')  # Hide axes
    label_ax.text(-1.5, 0.75, row_lbl[i], va='top', ha='left', fontsize=7)

# create a unified legend

# Collect handles and labels from all axes
handles, labels = [], []
for ax in ax_list:
    h, l = ax.get_legend_handles_labels()
    handles.extend(h)
    labels.extend(l)

# Remove duplicates (optional)
unique = dict(zip(labels, handles))

# Create a single legend
fig.legend(
    unique.values(), 
    unique.keys(), 
    loc='lower left', 
    bbox_to_anchor = (0,0.15),
    ncol=1, 
    fontsize=7, 
    handlelength = 0.8,
    handletextpad = 0.2,
    frameon = True
)

# Clean things up
# fig.subplots_adjust(bottom = 0.15,left = -0.00)
fig.subplots_adjust(
    left=0.08,
    right=0.98,
    top=0.91,
    bottom=0.18,
    wspace=0.15,
    hspace=0.05
)


# plt.show()  
print(f'out_img: {out_img}')
#fig.tight_layout()
fig.savefig(out_img,dpi = 1200)
plt.close(fig)
