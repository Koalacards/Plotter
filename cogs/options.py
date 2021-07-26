from discord_slash.cog_ext import manage_commands





##################
'''
Option completion per file:
datasetcommands.py: 12/12
helpcommand.py: 0/1
plotfeaturecommands.py: 3/6
savedplotgeneration.py: 0/2
utilitycommands.py: 0/2
scatterplot.py: 0/1
bargraph.py: 0/1
'''
##################

### Common options

_dataset_name_option= manage_commands.create_option(
    name="dataset_name",
    description="Name of your dataset",
    option_type=3,
    required=True
)

_row_name_option = manage_commands.create_option(
    name="row_name",
    description="Name of the row to add your values to",
    option_type=3,
    required=True
)

_separator_option= manage_commands.create_option(
    name="separator",
    description="String Separator [Default: ' '] (For example, '1, 2, 3' should have separator ', ')",
    option_type=3,
    required=True
)

dataset_name_only_options=[
    _dataset_name_option
]

#Datasetcommands command options

createdataset_options=[
    manage_commands.create_option(
        name="name",
        description="The name of the dataset to create",
        option_type=3,
        required=True
    )
]

removedataset_options=[
    manage_commands.create_option(
        name="name",
        description="The name of the dataset to remove",
        option_type=3,
        required=True
    )
]

addnumberrow_options=[
    _dataset_name_option,
    _row_name_option,
    manage_commands.create_option(
        name="numbers",
        description="Numbers to add to your row (must be separated by your separator, default is space separation)",
        option_type=3,
        required=True
    ),
    _separator_option
]

addstringrow_options=[
    _dataset_name_option,
    _row_name_option,
    manage_commands.create_option(
        name="strings",
        description="Strings to add to your row (must be separated by your separator, default is space separation)",
        option_type=3,
        required=True
    ),
    _separator_option
]

addrandomnumberrow_options=[
    _dataset_name_option,
    _row_name_option,
    manage_commands.create_option(
        name="amount_of_random_numbers",
        description="How many random numbers to add to your row [Must be an integer value]",
        option_type=4,
        required=True
    ),
    manage_commands.create_option(
        name="minimum_number",
        description="The minimum possible number for your range of random numbers",
        option_type=3,
        required=True
    ),
    manage_commands.create_option(
        name="maximum_number",
        description="The maximum possible number for your range of random numbers",
        option_type=3,
        required=True
    )
]

removerow_options=[
    _dataset_name_option,
    _row_name_option
]

addcolorrow_options=[
    _dataset_name_option,
    _row_name_option,
    manage_commands.create_option(
        name="colors",
        description="Colors [hexcode format: '#000FFF'] to add to your row",
        option_type=3,
        required=True
    ),
    _separator_option
]

addrandomcolorrow_options=[
    _dataset_name_option,
    _row_name_option,
    manage_commands.create_option(
        name="amount_of_random_colors",
        description="How many random colors to add to your row [Must be an integer value]",
        option_type=4,
        required=True
    )
]




#Plotfeaturecommands command options

legend_options=[
    _dataset_name_option,
    manage_commands.create_option(
        name="legend",
        description="Whether your want the legend on your graph on or off",
        option_type=3,
        required=True,
        choices=[
            "on",
            "off"
        ]
    )
]

setaxisoption_options=[
    _dataset_name_option,
    manage_commands.create_option(
        name="axis_option",
        description="Set your axis settings to one of the various options!",
        option_type=3,
        required=True,
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
    manage_commands.create_option(
        name="plot_title",
        description="The title of your plot",
        option_type=3,
        required=True
    )
]