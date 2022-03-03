# Plotter Documentation

Welcome to Plotter, a bot for making data sets and graphs directly on Discord. The following documentation will list the commands you can use to access Plotter and it's functionalities.

This documentation can be found on Plotter's official github, https://github.com/Koalacards/Plotter/blob/main/docs.md

Plotter can be invited to anyone's Discord server using the following URL: https://discord.com/api/oauth2/authorize?client_id=836212383847809075&permissions=2147535872&scope=bot%20applications.commands

## Table of Contents
 - [How to Read the Documentation](#how-to-read-the-documentation)
 - [Help Command](#help-command)
 - [Dataset Commands](#dataset-commands)
   - [createdataset](#createdataset)
   - [removedataset](#removedataset)
   - [addnumberrow](#addnumberrow)
   - [addrandomnumrow](#addrandomnumrow)
   - [addstringrow](#addstringrow)
   - [addcolorrow](#addcolorrow)
   - [addrandomcolorrow](#addrandomcolorrow)
   - [removerow](#removerow)
 - [Viewing Datasets Commands](#viewing-datasets-commands)
   - [viewdatasets](#viewdatasets)
   - [viewdata](#viewdata)
   - [viewdataintxt](#viewdataintxt)
   - [viewgraphdata](#viewgraphdata)
   - [viewgraphdataintxt](#viewgraphdataintxt)
 - [Plot Feature Commands](#plot-feature-commands)
   - [setplottitle](#setplottitle)
   - [setaxisboundaries](#setaxisboundaries)
   - [setaxisoption](#setaxisoption)
   - [setxticks](#setxticks)
   - [setyticks](#setyticks)
   - [legend](#legend)
 - [Plot Commands](#plot-commands)
   - [scatterplot](#scatterplot)
   - [bargraph](#bargraph)
 - [Plot Generation Commands](#plot-generation-commands)
   - [plotgenerate](#plotgenerate)
   - [plotcombine](#plotcombine)
 - [Utility Commands](#utility-commands)
   - [report](#report)
   - [suggest](#suggest)
   - [invite](#invite)
   - [support](#support)

## How to Read the Documentation

Here is an example command setup:

#### test
```/test [param1] (param2)```

Description of the test command

- **param1**: _type_ : the first parameter in test 
- **param2**: _type_ (default: ...): the second parameter in test

<img width="508" alt="image" src="https://user-images.githubusercontent.com/44925247/156574345-63c42d4e-d0f4-48b4-a6ec-e547dde6740d.png">


The command to enter is right after the forward slash (in this case, test), followed by parameters. Parameters in brackets [] are required for the command, and parameters in parenthesis () are optional.

The parameters are then listed, with the type required for the parameter (text, integer, floating point number, list of values) and a short description of what the parameter needs to be.


## Help Command

#### help
```/help (subset)```

This is the default help command, which lists out all of the commands for use in Discord.

- **subset**: _text_ (default: ""): The particular page of commands to see; one of the options: `dataset`, `features`, `generation`, `plots`, `utility`or no string which shows a landing page.

<img width="665" alt="image" src="https://user-images.githubusercontent.com/44925247/156578303-1b9369fa-8fc3-4ec8-9a45-64a0af153a5e.png">

## Dataset Commands

The following commands are used in order to create datasets and rows of data within the dataset, which will be used to create plots.

#### createdataset
```/createdataset [name]```

Creates a dataset under a certain name, which they will then reference when adding data.

- **name**: _text_ : The name of the dataset to create, can be any string.

![image](https://user-images.githubusercontent.com/44925247/156580891-8e9d3a8e-45cc-4a35-99a6-881e8246b1f8.png)

#### removedataset
```/removedataset [name]```

Removes a pre-existing dataset the user has under a certain name (if it exists)

- **name**: _text_ : The name of the dataset to create, can be any string.

![image](https://user-images.githubusercontent.com/44925247/156580991-51b56725-f948-4021-aba3-7e064d7e355d.png)


#### addnumberrow
```/addnumberrow [dataset_name] [row_name] [numbers] (separator)```

Adds a set of numbers to a dataset under a certain row name. If the row name does not exist, a row will be created with those numbers, and if the row name does exist the numbers will be added to the end of the row.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **row_name**: _text_: The name of the row of data, or a pre-existing row to add to
- **numbers**: _text_: The numbers to add as text, with the text being split by the separator given as an optional parameter
- **separator**: _text_ (default: " "): The separator for the numbers text, defaulted to a space

![image](https://user-images.githubusercontent.com/44925247/156581113-23a67d24-6728-49d5-9ff5-301ffb77fbb2.png)

#### addrandomnumrow
```/addrandomnumrow [dataset_name] [row_name] [amount_of_random_numbers] [minimum_number] [maximum_number]```

Adds a randomly generated set of numbers to a dataset under a certain row name. If the row name does not exist, a row will be created with the numbers, and if the row name does exist the numbers will be added to the end of the row.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **row_name**: _text_: The name of the row of data, or a pre-existing row to add to
- **amount_of_random_numbers**: _integer_ : The amount of random numbers that will be generated 
- **minimum_number**: _floating point number_: The minimum possible number to be generated (inclusive)
- **maximum_number**: _floating point number_: The maximum possible number to be generated (inclusive)

![image](https://user-images.githubusercontent.com/44925247/156583056-a267ea86-21bf-4aef-83e1-a66535c4aadd.png)

#### addstringrow
```/addstringrow [dataset_name] [row_name] [strings] (separator)```

Adds a set of strings to a dataset under a certain row name. If the row name does not exist, a row will be created with those strings, and if the row name does exist the strings will be added to the end of the row.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **row_name**: _text_: The name of the row of data, or a pre-existing row to add to
- **strings**: _text_: The strings to add as text, with the text being split by the separator given as an optional parameter
- **separator**: _text_ (default: " "): The separator for the strings text, defaulted to a space

![image](https://user-images.githubusercontent.com/44925247/156581746-3c226ca3-b18e-4ee4-85c6-ec96f8f3067e.png)

#### addcolorrow
```/addcolorrow [dataset_name] [row_name] [strings] (separator)```

Adds a set of colors (in hex code format) dataset under a certain row name. If the row name does not exist, a row will be created with those colors, and if the row name does exist the colors will be added to the end of the row.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **row_name**: _text_: The name of the row of data, or a pre-existing row to add to
- **colors**: _text_: The colors (in hex code format) to add as text, with the text being split by the separator given as an optional parameter
- **separator**: _text_ (default: " "): The separator for the colors text, defaulted to a space

![image](https://user-images.githubusercontent.com/44925247/156581838-321c82c8-d29e-46f3-bdc9-7f1da0513a53.png)

#### addrandomcolorrow
```/addrandomcolorrow [dataset_name] [row_name] [amount_of_random_colors]```

Adds a randomly generated set of colors (in hex-code format) to a dataset under a certain row name. If the row name does not exist, a row will be created with the numbers, and if the row name does exist the numbers will be added to the end of the row.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **row_name**: _text_: The name of the row of data, or a pre-existing row to add to
- **amount_of_random_colors**: _integer_ : The amount of random numbers that will be generated 

![image](https://user-images.githubusercontent.com/44925247/156583285-7e26def9-2201-4ee6-9068-6ecc76ed9198.png)

#### removerow
```/removerow [dataset_name] [row_name]```

Removes a row of data from the given dataset, if the row and/or dataset names exist. If not the bot will do nothing

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **row_name**: _text_: The name of the row of data, can be any string (command will not run if the user does not have a row in the dataset with the given name)

![image](https://user-images.githubusercontent.com/44925247/156582621-16056bd5-adea-4c01-b0ca-cb49dabf969c.png)


## Viewing Datasets Commands

The following commands are used to view the data within a dataset, or to view the datasets a user has.

#### viewdatasets
```/viewdatasets```

View all datasets owned by the user.

![image](https://user-images.githubusercontent.com/44925247/156583330-6a188899-f93a-41ec-81cf-55eab8ea05ab.png)

#### viewdata
```/viewdata [dataset_name]```

Views the rows of data and values within rows for a given dataset. 

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)

![image](https://user-images.githubusercontent.com/44925247/156583427-27e4849b-073f-4c31-8256-b5563084533a.png)


#### viewdataintxt
```/viewdataintxt [dataset_name]```

Provides the rows of data and values within rows for a given dataset in a .txt file (this is useful for larger datasets that may not be able to show up on Discord due to Discord's 2000 character message limit).

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)

![image](https://user-images.githubusercontent.com/44925247/156583714-29dbe4cf-617c-4da6-81eb-540baa32bee4.png)

#### viewgraphdata
```/viewgraphdata [dataset_name]```

Views the saved graphs and properties of the graphs for a dataset. For information on how to save a graph, refer to the `Plot Generation Commands`.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)

![image](https://user-images.githubusercontent.com/44925247/156587792-f9471d33-fef1-40ae-ad0a-874c87a380c1.png)

#### viewgraphdataintxt
```/viewgraphdataintxt [dataset_name]```
Provides the saved graphs and properties of the graphs for a given dataset in a .txt file (this is useful for larger datasets that may not be able to show up on Discord due to Discord's 2000 character message limit). For information on how to save a graph, refer to the `Plot Generation Commands`.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)

![image](https://user-images.githubusercontent.com/44925247/156587976-b8cc8752-37b9-4d7d-93b7-db75c64b68b1.png)

## Plot Feature Commands

The following commands are used to set universal features of plots in a dataset, such as the title, axis options, and whether or not to include a legend. These commands should be used before the creation of a plot, unless the user wants the default matplotlib settings.

#### setplottitle
```/setplottitle [dataset_name] [plot_title]```

Sets the title of any plot created in the dataset. If this command is not called, the default title of each plot is the name of the dataset.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **plot_title**: _text_: The title of the plot, can be any string

![image](https://user-images.githubusercontent.com/44925247/156583798-8a72d15a-7987-468f-9b28-30ea23c14145.png)

#### setaxisboundaries
```/setaxisboundaries [dataset_name] [minimum_x] [maximum_x] [minimum_y] [maximum_y]```

Sets the ranges for each of the x and y axes.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **minimum_x** _floating point number_: The minimum x value for the axis
- **maximum_x** _floating point number_: The maximum x value for the axis
- **minimum_y** _floating point number_: The minimum y value for the axis
- **maximum_y** _floating point number_: The maximum y value for the axis

![image](https://user-images.githubusercontent.com/44925247/156583897-1954284a-98f2-4b22-ac55-75973d1e3102.png)

#### setaxisoption
```/setaxisoption [dataset_name] [axis_option]```

Sets the axis option setting for each plot in the dataset. This is how axes can be scaled or slightly altered.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **axis_option**: _text_: The axis option: which must be one of the following: `on`, `off`, `equal`, `scaled`, `tight`, `auto`, `image`, or `square`

![image](https://user-images.githubusercontent.com/44925247/156583968-593bc8b4-33d0-4984-ae1d-f423dc633722.png)

#### setxticks
```/setxticks [dataset_name] [ticks_row] (labels_row) (remove_ticks)```

Sets the ticks for the x-axis of the graph, or the numbers that show ticked along the x axis. Optionally allows the user to add labels under the ticks, or to remove a pre-existing setting of ticks to go back to the matplotlib default.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **ticks_row**: _text_: The name of a row of numbers in the dataset that will become the x ticks for the dataset plots
- **labels_row**: _text_(default: ""): The name of a row of data (text or numbers) in the dataset that will be the x labels for the dataset plots. This row of data must be the same length as the row of ticks.
- **remove_ticks**: _text_(default: "off"): Whether or not to remove a pre-existing ticks setting. Must be one of the following: `on`, `off`. If set to `on`, the settings given in the command will not be applied; the only thing that will occur is a reset of previous settings

![image](https://user-images.githubusercontent.com/44925247/156584237-e1733a01-f32f-4217-bd81-0f533b4ddfc2.png)

#### setyticks
```/setyticks [dataset_name] [ticks_row] (labels_row) (remove_ticks)```

Sets the ticks for the y-axis of the graph, or the numbers that show ticked along the y axis. Optionally allows the user to add labels under the ticks, or to remove a pre-existing setting of ticks to go back to the matplotlib default.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **ticks_row**: _text_: The name of a row of numbers in the dataset that will become the y ticks for the dataset plots
- **labels_row**: _text_ (default: ""): The name of a row of data (text or numbers) in the dataset that will be the y labels for the dataset plots. This row of data must be the same length as the row of ticks.
- **remove_ticks**: _text_(default: "off"): Whether or not to remove a pre-existing ticks setting. Must be one of the following: `on`, `off`. If set to `on`, the settings given in the command will not be applied; the only thing that will occur is a reset of previous settings

![image](https://user-images.githubusercontent.com/44925247/156584382-b7651339-52ce-43d8-95b9-18402be9af97.png)

#### legend
```/legend [dataset_name] [legend]```

Turns the legend option either on or off for plots in the dataset. If the legend option is on, then a legend will be created in the plot with labels equal to  the `label` parameter in the plot commands. For more information, please refer to `Plot Commands`.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **legend**: _text_: Whether the legend should be on or off, text must be one of the following options: `on`, `off`

![image](https://user-images.githubusercontent.com/44925247/156584441-fb49d829-e867-4873-b51f-a2f81298cdfb.png)

## Plot Commands

The following commands create the different types of graphs using the data in datasets and plot features set using the Plot Feature Commands.

#### scatterplot
```/scatterplot [dataset_name] [x_row] [y_row] (x_label) (y_label) (size_row) (color_row_or_one_color) (transparency) (saveas)```

Creates a scatterplot with the following properties and dataset data.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **x_row**: _text_: The name of a row of numbers in the dataset corresponding to the x values in the scatterplot. Command will not run if the row does not exist or the row is not a row of numbers
- **y_row**: _text_: The name of a row of numbers in the dataset corresponding to the y values in the scatterplot. This row must contain the same number of values as the x row. Command will not run if the row does not exist or the row is not a row of numbers
- **x_label**: _text_(default: ""): The label for the x axis of the plot
- **y_label**: _text_(default: ""): The label for the y axis of the plot
- **size_row**: _text_(default: ""): The name of a row of numbers in the dataset corresponding to the size of each scatter in the scatterplot. This row must contain the same number of values as the x and y rows. Command will not run if the row does not exist or the row is not a row of numbers
- **color_row_or_one_color**(default: ""): _text_: EITHER the name of the row of colors in the dataset corresponding to the size of each scatter OR a single color hex code for all scatters in the plot. If the input is a row, the row must contain the same number of values as the x, y and size rows, and must also exist in the dataset and contain only colors
- **transparency**(default: 1): _floating point number_: A number between 0 and 1 determining how transparent the scatters are, from 0 being invisible to 1 being fully opaque
- **save_as**(default: ""): _text_: A name to save the graph as so that it can be generated easily. To generate graphs, view the `Plot Generation Commands`. The graph will then show up in the `viewgraphdata` and `viewgraphdataintxt` commands

![image](https://user-images.githubusercontent.com/44925247/156587568-d8effb0c-3204-40df-b6cc-d1f98f6079e5.png)

#### bargraph
```/bargraph [dataset_name] [x_row] [height_row] (x_label) (y_label) (width) (bottom_coords_row) (align) (color_row_or_one_color) (label) (saveas)```

Creates a bar graph with the following properties and dataset data.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **x_row**: _text_: The name of a row of numbers in the dataset corresponding to the x values in the bar graph. Command will not run if the row does not exist or the row is not a row of numbers.
- **height_row**: _text_: The name of a row of numbers in the dataset corresponding to the height values in the bar graph. This row must contain the same number of values as the x row. Command will not run if the row does not exist or the row is not a row of numbers
- **x_label**: _text_(default: ""): The label for the x axis of the plot
- **y_label**: _text_(default: ""): The label for the y axis of the plot
- **width**: _floating point number_(default: 0.8): The width of all of the bars
- **bottom_coords_row**: _text_(default: ""): The name of a row of numbers in the dataset corresponding to the initial heights of each bar in the bar graph. This row must contain the same number of values as the x row and heigh row. Command will not run if the row does not exist or the row is not a row of numbers
- **align**: _text_(default: "center"): The alignment of the bars, must be one of: `center`, `edge`
- **color_row_or_one_color**(default: ""): _text_: EITHER the name of the row of colors in the dataset corresponding to the size of each bar OR single color hex code for all sbars plot. If the input is a row, the row must contain the same number of values as the x and height rows, and must also exist in the dataset and contain only colors
- **save_as**(default: ""): _text_: A name to save the graph as so that it can be generated easily. To generate graphs, view the `Plot Generation Commands`. The graph will then show up in the `viewgraphdata` and `viewgraphdataintxt` commands

![image](https://user-images.githubusercontent.com/44925247/156587684-df21a562-e8c4-4b6d-b4ed-b421176a2f7a.png)

## Plot Generation Commands

These commands generate previous plots that were created using the `save_as` parameters in either graph creation or combination.

#### plotgenerate
```/plotgenerate [dataset_name] [saved_plot_name]```

Generates a plot using the given saved_plot_name, which should be the name of a previously saved plot in the dataset. The `viewgraphdata` command can be used to see which graph names have been saved.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **saved_plot_name**: _text_: The name of the previously saved plot to generate (command will not run if the name of the plot does not exist)

![image](https://user-images.githubusercontent.com/44925247/156588251-5279ab44-df15-4da9-805c-201663edc689.png)

#### plotcombine
```/plotcombine [dataset_name] [first_plot_name] [second_plot_name] (saveas)```

Combines the two given saved plots into one, where both data plots will show up together. **Note**: The x and y labels for the graph will be from the first plot, NOT the second!

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **first_plot_name**: _text_: The name of the first previously saved plot to combine, using this plot's label information for the combined plot (command will not run if the name of the plot does not exist)
- **second_plot_name**: _text_: The name of the second previously saved plot to generate (command will not run if the name of the plot does not exist)
- **save_as**(default: ""): _text_: A name to save the combined graph as so that it can be generated easily. The graph will then show up in the `viewgraphdata` and `viewgraphdataintxt` commands

![image](https://user-images.githubusercontent.com/44925247/156588324-3946486d-ead5-47a4-acc8-280d6714a156.png)

## Utility Commands

These commands have various functions that do not involve creating datasets or plots

#### report
```/report [report]```

Allows the user to report the bug directly for the developer(s) to see.

- **report**: _text_: The bug/problem to report

![image](https://user-images.githubusercontent.com/44925247/156588391-d086a704-d21d-4cbd-b687-36a933f15217.png)

#### suggest
```/suggest [suggestion]```

Allows the user to submit a feature suggestion directly for the developer(s) to see.

- **suggestion**: _text_: The suggestion offered by the user

![image](https://user-images.githubusercontent.com/44925247/156588441-44784193-6040-47c7-94be-3522bb71a730.png)

#### invite
```/invite```

Provides a URL for users to invite Plotter to their servers.

![image](https://user-images.githubusercontent.com/44925247/156588474-380bf7b1-cde1-43a1-a9c4-7b0e7e4c021b.png)

#### support
```/support```

Provides a link to the offical Plotter support server, where they will be able to get more in-depth assistance.

![image](https://user-images.githubusercontent.com/44925247/156588512-bc2320ac-f914-4a56-a122-44b6dc54f0a8.png)
