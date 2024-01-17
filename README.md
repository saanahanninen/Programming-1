These are some of the projects I did during the Programming 1 course during my BSc Computer Science studies.


&#x270F;&#xFE0F; guiproject (final course project):

The program works as a to-do list that shows to-dos (stored in a .txt file)
in alphabetical and priority order. The program allows the user to add and delete to-dos.
The aim was to create an advanced GUI (using components not covered in the course materials).

&#127922; mölkky:

Mölkky is a traditional Finnish game where players aim to score exactly 50 points.
If a player ends up having more than 50 points, their score will be decreased to 25 points.

This program acts as a scorekeeper where two players, Matti and Teppo, can keep track of
their scores after each throw.

This exercise included a code template. I implemented the Player class, a warning message
that will be printed if the total score of the player is 40-49 points, a supporting feedback
that will be printed if the entered score is larger than the average of all the points entered
for that player, and the hit percentage printout.

&#128230; warehouse:

When the program starts, it asks the user the name of the file containing the product
information. A user interface is then shown to the user in which they can enter
the following commands:

print - Prints all known products in ascending order by product code.

print {code} - Prints the information of the product specified by the code.

change {code} {amount} - Changes the inventory amount of the product indicated by the code
by the amount. The amount can be a positive or negative integer: positive values increase
the inventory, negative values decrease it.

delete {code} - Deletes the product identified by the code from the warehouse inventory.
However, only a product whose quantity in the inventory is 0 or less can be deleted.

low - Prints all products in ascending order by product code whose inventory quantity has
fallen below a preset limit (30).

combine {code1} {code2} - It sometimes happens that the central warehouse makes a mistake
and a single item is assigned two different product codes. In these situations it is useful
to be able to combine these two products into one. However, not just any two products can be combined.
The following conditions must be met: their prices must be the same and their product categories must be the same.
If combining is possible, the stock quantity of the product code2 is added to the stock quantity of code1.

sale {category} {sale_percentage} - Sets all the products in the category on sale for sale_percentage (float).

For this project, I was given a code template where I implemented the commands and Product class methods
that allow all the commands to be implemented.
