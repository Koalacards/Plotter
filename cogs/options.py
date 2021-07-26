from discord_slash.cog_ext import manage_commands





##################
'''
Option completion per file:
datasetcommands.py: 12/12
helpcommand.py: 0/1
plotfeaturecommands.py: 3/6
savedplotgeneration.py: 2/2
utilitycommands.py: 2/2
scatterplot.py: 0/1
bargraph.py: 0/1
'''
##################

#function to create options easily
def create_option(name:str, description:str, option_type:int=3, required:bool=True, choices=None):
    return manage_commands.create_option(
        name=name,
        description=description,
        option_type=option_type,
        required=required,
        choices=choices
    )


### Common options

_dataset_name_option= create_option(
    "dataset_name",
    "Name of your dataset"
)


_row_name_option = create_option(
    "row_name",
    "Name of the row to add your values to"
)

_separator_option= create_option(
    "separator",
    "String Separator [Default: ' '] (For example, '1, 2, 3' should have separator ', ')",
    required=False
)

_saveas_option = create_option(
    "saveas",
    "Name to save your graph as (overridable), graph will show up in '/viewgraphdata [dataset]'",
    required=False
)

dataset_name_only_options=[
    _dataset_name_option
]

#Datasetcommands command options

createdataset_options=[
    create_option(
        "name",
        "The name of the dataset to create"
    )
]

removedataset_options=[
    create_option(
        "name",
        "The name of the dataset to remove"
    )
]

addnumberrow_options=[
    _dataset_name_option,
    _row_name_option,
    create_option(
        "numbers",
        "Numbers to add to your row (must be separated by your separator, default is space separation)"
    ),
    _separator_option
]

addstringrow_options=[
    _dataset_name_option,
    _row_name_option,
    create_option(
        "strings",
        "Strings to add to your row (must be separated by your separator, default is space separation)"
    ),
    _separator_option
]

addrandomnumberrow_options=[
    _dataset_name_option,
    _row_name_option,
    create_option(
        "amount_of_random_numbers",
        "How many random numbers to add to your row [Must be an integer value]",
        option_type=4
    ),
    create_option(
        "minimum_number",
        "The minimum possible number for your range of random numbers"
    ),
    create_option(
        "maximum_number",
        "The maximum possible number for your range of random numbers"
    )
]

removerow_options=[
    _dataset_name_option,
    _row_name_option
]

addcolorrow_options=[
    _dataset_name_option,
    _row_name_option,
    create_option(
        "colors",
        "Colors [hexcode format: '#000FFF'] to add to your row"
    ),
    _separator_option
]

addrandomcolorrow_options=[
    _dataset_name_option,
    _row_name_option,
    create_option(
        "amount_of_random_colors",
        "How many random colors to add to your row [Must be an integer value]",
        option_type=4
    )
]


#Help command options




#Plotfeaturecommands command options

legend_options=[
    _dataset_name_option,
    create_option(
        "legend",
        "Whether your want the legend on your graph on or off",
        choices=[
            "on",
            "off"
        ]
    )
]

setaxisoption_options=[
    _dataset_name_option,
    create_option(
        "axis_option",
        "Set your axis settings to one of the various options!",
        choices=[
            "on",
            "off",
            "equal",
            "scaled",
            "tight",
            "auto",
            "image",
            "square"
        ]
    )
]

setplottitle_options = [
    _dataset_name_option,
    create_option(
        "plot_title",
        "The title of your plot"
    )
]

#Savedplotgeneration command options

plotgenerate_options= [
    _dataset_name_option,
    create_option(
        "saved_plot_name",
        "The name of a plot you have saved (use /viewgraphdata [dataset])"
    )
]

plotcombine_options = [
    _dataset_name_option,
    create_option(
        "first_plot_name",
        "The name of a saved plot to combine first (Axis/title details will be taken from this plot)"
    ),
    create_option(
        "second_plot_name",
        "The name of a saved plot to combine second"
    ),
    _saveas_option
]

#utilitycommands command options

report_options= [
    create_option(
        "report",
        "The bug report to be directly sent to Plotter staff!"
    )
]

suggest_options= [
    create_option(
        "suggestion",
        "The suggestion to be directly sent to Plotter staff!"
    )
]




#scatterplot command options

#bargraph command options
