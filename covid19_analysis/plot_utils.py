import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import Circle
from matplotlib import cm
import numpy as np

def lstrip(list_in, cond=None, min_value=0):
    list_out = []
    for v in list_in:
        keep = cond(v, min_value) if cond is not None else v
        if keep or list_out:
            list_out.append(v)
    return list_out


def cond(value, min_value=0):
    if value > min_value:
        return True
    return False


def interpol_helper(y, mask_val):
    return y==mask_val, lambda z: z.nonzero()[0]


def interpol(y, mask_val):
    zeros, x = interpol_helper(y, mask_val)
    if np.any(zeros):
        y[zeros] = np.interp(x(zeros), x(~zeros), y[~zeros])
    return zeros, x, y



def plot_1d(ax, data, meas, start_value, scale=None, transform=None, log_y=False, **kwargs):
    x_label = kwargs.get("x_label", "x_label")
    y_label = kwargs.get("y_label", "y_label")
    title = kwargs.get("title", "")
    linestyles = ("-", "-.", ":")
    # 1d plots
    max_len = 0
    interpolated = False
    for i, (key, val_dict) in enumerate(data.items()):
        list_strip = np.array(lstrip(val_dict[meas], cond, start_value))
        if scale:
            list_strip = list_strip * scale[key]
        zeros, _, list_strip = interpol(list_strip, 0)
        print(list_strip)
        if transform and len(list_strip):
            list_strip = transform(list_strip)
        max_len = max(len(list_strip), max_len)
        if np.any(zeros):
            interpolated = True
            interpol_x = []
            interpol_y = []
            for j, (z, mark_val) in enumerate(zip(zeros, list_strip)):
                if z:
                    interpol_x.append(j)
                    interpol_y.append(mark_val)
            ax.plot(interpol_x, interpol_y, linestyle="-", color="black", marker="v")
        ax.plot(list_strip, label=key, linestyle=linestyles[i%len(linestyles)])
            
    handles, labels = ax.get_legend_handles_labels()
    if interpolated:
        handles.append(Line2D([0], [0], color="black", linestyle="", marker="v"))
        labels.append("interpolated")
    ax.legend(handles, labels, loc="lower right", prop={"size": 25})
    if log_y:
        ax.set_yscale("log")

    ax.set_xticks(range(max_len))
    ax.set_xticklabels(range(max_len), rotation=0)

    ax.set_xlabel(x_label, fontsize=25)
    ax.set_ylabel(y_label, fontsize=25)
    ax.set_title(title, fontsize=35)


def plot_2d(ax, data, x, y, scale_x=None, scale_y=None, transform_x=None, transform_y=None, **kwargs):
    x_label = kwargs.get("x_label", "x_label")
    y_label = kwargs.get("y_label", "y_label")
    title = kwargs.get("title", "")
    linestyles = ("-", "-.", ":")
    for i, (key, val_dict) in enumerate(data.items()):
        list_strip_x = np.array(val_dict[x])
        list_strip_y = np.array(val_dict[y])
        if scale_x:
            list_strip_x = list_strip_x * scale_x[key]
        _, _, list_strip_x = interpol(list_strip_x, 0)
        if transform_x:
            list_strip_x = transform_x(list_strip_x)
        if scale_y:
            list_strip_y = list_strip_y * scale_y[key]
        _, _, list_strip_y = interpol(list_strip_y, 0)
        if transform_y:
            list_strip_y = transform_y(list_strip_y)
        ax.plot(list_strip_x, list_strip_y, label=key, linestyle=linestyles[i%len(linestyles)])
        
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc="lower right", prop={"size": 25})

    ax.set_xlabel(x_label, fontsize=25)
    ax.set_ylabel(y_label, fontsize=25)

    ax.set_title(title, fontsize=35)



def plot_3d_bubbles(ax, tuple_dict, **kwargs):
        x_label = kwargs.get("x_label", "x_label")
        y_label = kwargs.get("y_label", "y_label")
        z_label = kwargs.get("z_label", "z_label")
        title = kwargs.get("title", "")

        radii = np.array([values[2] for values in tuple_dict.values()])
        max_radius = 5.
        scale = max_radius / max(radii)
        radii = radii * scale
        colors = radii / max(radii)

        color_map = cm.get_cmap("jet")

        for (key, values), radius, color in zip(tuple_dict.items(), radii, colors):
            print("blah")
            ax.add_patch(Circle((values[0], values[1]), radius, color=color_map(color), alpha=0.5))
            ax.text(values[0], values[1], key, fontsize=25)

        ax.set_xlabel(x_label, fontsize=25)
        ax.set_ylabel(y_label, fontsize=25)

        ax.axis("equal")
