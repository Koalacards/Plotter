# Plotter Documentation

Welcome to Plotter, a bot for making data sets and graphs directly on Discord. The following documentation will list the commands you can use to access Plotter and it's functionalities.

## How to Read the Documentation

Here is an example command setup:

/**test** [param1] (param2)

Description of the test command

- **param1**: _type_ : the first parameter in test

- **param1**: _type_ : the second parameter in test

The command to enter is right after the forward slash (in this case, test), followed by parameters. Parameters in brackets [] are required for the command, and parameters in parenthesis () are optional.

The parameters are then listed, with the type required for the parameter (text, integer, floating point number, list of values) and a short description of what the parameter needs to be.


## Help Command

/**help** (subset)

This is the default help command, which lists out all of the commands for use in Discord.

- **subset**: _text_ (default: ""): The particular page of commands to see; one of the options: `dataset`, `features`, `generation`, `plots`, `utility`or no string which shows a landing page.

## Dataset Commands

/**createdataset** [name]

Creates a dataset under a certain name, which they will then reference when adding data.

- **name**: _text_ : The name of the dataset to create, can be any string.

/**removedataset** [name]

Removes a pre-existing dataset the user has under a certain name (if it exists)

- **name**: _text_ : The name of the dataset to create, can be any string.

/**addnumberrow** [dataset_name] [row_name] [numbers] (separator)

Adds a set of numbers to a dataset under a certain row name. If the row name does not exist, a row will be created with those numbers, and if the row name does exist the numbers will be added to the end of the row.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **row_name**: _text_: The name of the row of data, or a pre-existing row to add to
- **numbers**: _text_: The numbers to add as text, with the text being split by the separator given as an optional parameter
- **separator**: _text_ (default: " "): The separator for the numbers text, defaulted to a space

/**addrandomnumrow** [dataset_name] [row_name] [amount_of_random_numbers] [minimum_number] [maximum_number]

Adds a randomly generated set of numbers to a dataset under a certain row name. If the row name does not exist, a row will be created with the numbers, and if the row name does exist the numbers will be added to the end of the row.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **row_name**: _text_: The name of the row of data, or a pre-existing row to add to
- **amount_of_random_numbers**: _integer_ : The amount of random numbers that will be generated 
- **minimum_number**: _floating point number_: The minimum possible number to be generated (inclusive)
- **maximum_number**: _floating point number_: The maximum possible number to be generated (inclusive)

/**addstringrow** [dataset_name] [row_name] [strings] (separator)

Adds a set of strings to a dataset under a certain row name. If the row name does not exist, a row will be created with those strings, and if the row name does exist the strings will be added to the end of the row.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **row_name**: _text_: The name of the row of data, or a pre-existing row to add to
- **strings**: _text_: The strings to add as text, with the text being split by the separator given as an optional parameter
- **separator**: _text_ (default: " "): The separator for the strings text, defaulted to a space

/**addcolorrow** [dataset_name] [row_name] [strings] (separator)

Adds a set of colors (in hex code format) dataset under a certain row name. If the row name does not exist, a row will be created with those colors, and if the row name does exist the colors will be added to the end of the row.

- **dataset_name**: _text_: The name of the dataset, can be any string (command will not run if user does not have a dataset with the given name)
- **row_name**: _text_: The name of the row of data, or a pre-existing row to add to
- **colors**: _text_: The colors (in hex code format) to add as text, with the text being split by the separator given as an optional parameter
