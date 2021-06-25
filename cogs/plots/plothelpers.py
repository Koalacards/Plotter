import matplotlib.pyplot as plt
import utils
import asyncutils
import db.plotdbfunctions as dbfunc
import numpy as np

def create_figure():
    plt.figure()

async def set_common_plot_info(ctx, dataset_name:str, x_label:str, y_label:str):
    author = ctx.author
    potential_title=dbfunc.get_plot_title(author.id, dataset_name)
    plt.title(potential_title)
    plt.axis(utils.sanitize_axis_info(author, dataset_name))
    plt.xlabel("x" if x_label == "" else x_label)
    plt.ylabel("y" if y_label == "" else y_label)

    #X ticks
    x_ticks_info = await asyncutils.sanitize_ticks_info(ctx, dataset_name, True)
    if x_ticks_info != False and x_ticks_info is not None:
        x_ticks = np.array(x_ticks_info[0])
        x_labels=None
        try:
            x_labels = np.array(x_ticks_info[1])
        except:
            pass
        plt.xticks(x_ticks, x_labels)

    #Y ticks
    y_ticks_info = await asyncutils.sanitize_ticks_info(ctx, dataset_name, False)
    if y_ticks_info != False and y_ticks_info is not None:
        y_ticks = np.array(y_ticks_info[0])
        y_labels=None
        try:
            y_labels = np.array(y_ticks_info[1])
        except:
            pass
        plt.yticks(y_ticks, y_labels)
            


def save_and_close(file_name:str):
    plt.savefig(file_name, dpi='figure')
    plt.close()