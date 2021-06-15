import matplotlib.pyplot as plt
import utils
import db.plotdbfunctions as dbfunc

def create_figure():
    plt.figure()

def set_common_plot_info(author, dataset_name:str, x_label:str, y_label:str):
    potential_title=dbfunc.get_plot_title(author.id, dataset_name)
    plt.title(potential_title)
    plt.axis(utils.sanitize_axis_info(author, dataset_name))
    plt.xlabel("x" if x_label == "" else x_label)
    plt.ylabel("y" if y_label == "" else y_label)

def save_and_close(file_name:str):
    plt.savefig(file_name, dpi='figure')
    plt.close()