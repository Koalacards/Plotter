# Plotter
Upcoming discord bot that will bring matplotlib functionalities to discord

To create the bot yourself:
- Go to the discord developer portal (https://discord.com/developers/applications) and create an application, then a bot
- Clone the repo and add two files: confidential.py in the base directory, and plotdata.db in the "db" folder
- Copy the bot's client token, and in confidential.py paste in `RUN_ID="<YOUR TOKEN>"`. For example, if your token was 12345, confidential.py should say `RUN_ID="12345"`
- Install the following python libraries:
    - discord
    - matplotlib
    - numpy

- Run entry.py, and everything should work!

Happy plotting! 

