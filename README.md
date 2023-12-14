# AlcoBot-Telegram
This is a telegram bot created using the TeleBot module in Python. The bot provides information about the chemical structure of alcoholic compounds at the user's request.

Here are the main functions and features of your bot:

The beginning of the conversation:

When sending the /start command, the bot greets the user and suggests writing the name of the alcohol.
Menu:

The user can open the menu with the command /menu, which provides four buttons:
"Add": Adds a new item to the alcohol database.
"Delete": Deletes an item from the database.
"Update": Starts the process of updating the element (name or structure).
"Get a list of alcohols": Displays a list of all alcohols in the database.
Getting information:

The user can send the name of the alcohol, and the bot will provide the chemical structure of this alcohol.
If there is a corresponding picture of the structure in the database, the bot will send it to the user.
Updating an element:

When selecting the "Update" option from the menu, the bot offers to choose what needs to be updated: the name or the structure.
After the selection, the bot waits for the input of new data from the user.
The database:

The bot uses an SQLite database (alcohol_database.db), where the names and structures of alcohols are stored.
Interaction with images:

If there is an image of the chemical structure of alcohol in the database, the bot sends it to the user in response.
Error handling:

The bot provides feedback and informs the user in case of errors.
