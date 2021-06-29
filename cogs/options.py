from discord_slash.cog_ext import manage_commands

_dataset_name_option= manage_commands.create_option(
    name="dataset_name",
    description="Name of your dataset",
    option_type=3,
    required=True
)

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