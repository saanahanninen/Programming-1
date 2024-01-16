"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Saana Hänninen

12.5 Project: Warehouse Inventory.
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

"""

LOW_STOCK_LIMIT = 30
SALE_PERCENTAGE = 0


class Product:
    """
    This class represent a product i.e. an item available for sale.
    """

    def __init__(self, code, name, category, price, stock):
        """
        A Product object is initialised with a code, name, category, price and
        stock level.
        :param code: int, the product code.
        :param name: str, the product name.
        :param category: str, the product category.
        :param price: float, the product price.
        :param stock: int, the product stock level.
        """
        self.__code = code
        self.__name = name
        self.__category = category
        self.__price = price
        self.__stock = stock
        # As __price can change if a discount is set, __original_price
        # parameter is to be initialised to store the original price.
        self.__original_price = price
        # Initialise sale percentage to be zero as the price is not discounted
        # in the beginning.
        self.__sale_percentage = SALE_PERCENTAGE

    def __str__(self):
        """
        YOU SHOULD NOT MODIFY THIS METHOD or it will mess up
        the automated tests.
        """

        lines = [
            f"Code:     {self.__code}",
            f"Name:     {self.__name}",
            f"Category: {self.__category}",
            f"Price:    {self.__price:.2f}€",
            f"Stock:    {self.__stock} units",
        ]

        longest_line = len(max(lines, key=len))

        for i in range(len(lines)):
            lines[i] = f"| {lines[i]:{longest_line}} |"

        solid_line = "+" + "-" * (longest_line + 2) + "+"
        lines.insert(0, solid_line)
        lines.append(solid_line)

        return "\n".join(lines)

    def __eq__(self, other):
        """
        YOU SHOULD NOT MODIFY THIS METHOD or it will mess up
        the automated tests since the read_database function will
        stop working correctly.
        """

        return self.__code == other.__code and \
               self.__name == other.__name and \
               self.__category == other.__category and \
               self.__price == other.__price

    def modify_stock_size(self, amount):
        """
        YOU SHOULD NOT MODIFY THIS METHOD since read_database
        relies on its behavior and might stop working as a result.

        Allows the <amount> of items in stock to be modified.
        This is a very simple method: it does not check the
        value of <amount> which could possibly lead to
        a negative amount of items in stock. Caveat emptor.

        :param amount: int, how much to change the amount in stock.
                       Both positive and negative values are accepted:
                       positive value increases the stock and vice versa.
        """

        self.__stock += amount

    def is_stock_empty(self):
        """
        Checks whether the product is not in stock.
        :return: bool, returns true if the stock is empty, otherwise false.
        """
        if self.__stock <= 0:
            return True
        else:
            return False

    def is_low_stock(self):
        """
        Checks whether the product's stock is under the low stock limit.
        :return: bool, returns true if the stock is below the limit, otherwise
        false.
        """
        if self.__stock <= LOW_STOCK_LIMIT:
            return True
        else:
            return False

    def check_combinability(self, other):
        """
        Checks whether the product can be combined with another product:
        their prices and categories must be the same, product codes different.
        If the products cannot be combined, an error message is printed.
        :param other: Product, the product to be combined with the first product.
        :return: bool, returns false if the products' prices and categories are
        different and the codes are the same, otherwise true.
        """
        if self.__category != other.__category:
            print(f"Error: combining items of different categories "
                  f"'{self.__category}' and '{other.__category}'.")
            return False
        elif self.__price != other.__price:
            print(f"Error: combining items with different prices "
                  f"{self.__price:.2f}€ and {other.__price:.2f}€.")
            return False
        elif self.__code == other.__code:
            print(f"Error: bad parameters '{self.__code} {other.__code}' "
                  f"for combine command.")
            return False
        else:
            return True

    def add_stock(self, other):
        """
        Adds the stock of the other product to the first product's stock.
        :param other: Product, the product whose stock will be added.
        """
        self.__stock += other.__stock

    def set_sale_price(self, percentage):
        """
        Sets the sale price for a product.
        :param percentage: str, the sale percentage to be set.
        """
        self.__sale_percentage = float(percentage) / 100
        self.__price = self.__original_price * (1-self.__sale_percentage)

    def in_category(self, category):
        """
        Checks whether the product is in a specific category.
        :param category: str, the product category.
        :return: bool, returns true if the product belongs to the category,
        otherwise false.
        """
        if self.__category == category:
            return True
        else:
            return False


def _read_lines_until(fd, last_line):
    """
    YOU SHOULD NOT MODIFY THIS FUNCTION since read_database
    relies on its behavior and might stop working as a result.

    Reads lines from <fd> until the <last_line> is found.
    Returns a list of all the lines before the <last_line>
    which is not included in the list. Return None if
    file ends bofore <last_line> is found.
    Skips empty lines and comments (i.e. characeter '#'
    and everything after it on a line).

    You don't need to understand this function works as it is
    only used as a helper function for the read_database function.

    :param fd: file, file descriptor the input is read from.
    :param last_line: str, reads lines until <last_line> is found.
    :return: list[str] | None
    """

    lines = []

    while True:
        line = fd.readline()

        if line == "":
            return None

        hashtag_position = line.find("#")
        if hashtag_position != -1:
            line = line[:hashtag_position]

        line = line.strip()

        if line == "":
            continue

        elif line == last_line:
            return lines

        else:
            lines.append(line)


def read_database(filename):
    """
    YOU SHOULD NOT MODIFY THIS FUNCTION as it is ready.

    This function reads an input file which must be in the format
    explained in the assignment. Returns a dict containing
    the product code as the key and the corresponding Product
    object as the payload. If an error happens, the return value will be None.

    You don't necessarily need to understand how this function
    works as long as you understand what the return value is.
    You can probably learn something new though, if you examine the
    implementation.

    :param filename: str, name of the file to be read.
    :return: dict[int, Product] | None
    """

    data = {}

    try:
        with open(filename, mode="r", encoding="utf-8") as fd:

            while True:
                lines = _read_lines_until(fd, "BEGIN PRODUCT")
                if lines is None:
                    return data

                lines = _read_lines_until(fd, "END PRODUCT")
                if lines is None:
                    print(f"Error: premature end of file while reading '{filename}'.")
                    return None

                # print(f"TEST: {lines=}")

                collected_product_info = {}

                for line in lines:
                    keyword, value = line.split(maxsplit=1)  # ValueError possible

                    # print(f"TEST: {keyword=} {value=}")

                    if keyword in ("CODE", "STOCK"):
                        value = int(value)  # ValueError possible

                    elif keyword in ("NAME", "CATEGORY"):
                        pass  # No conversion is required for string values.

                    elif keyword == "PRICE":
                        value = float(value)  # ValueError possible

                    else:
                        print(f"Error: an unknown data identifier '{keyword}'.")
                        return None

                    collected_product_info[keyword] = value

                if len(collected_product_info) < 5:
                    print(f"Error: a product block is missing one or more data lines.")
                    return None

                product_code = collected_product_info["CODE"]
                product_name = collected_product_info["NAME"]
                product_category = collected_product_info["CATEGORY"]
                product_price = collected_product_info["PRICE"]
                product_stock = collected_product_info["STOCK"]

                product = Product(code=product_code,
                                  name=product_name,
                                  category=product_category,
                                  price=product_price,
                                  stock=product_stock)

                # print(product)

                if product_code in data:
                    if product == data[product_code]:
                        data[product_code].modify_stock_size(product_stock)

                    else:
                        print(f"Error: product code '{product_code}' conflicting data.")
                        return None

                else:
                    data[product_code] = product

    except OSError:
        print(f"Error: opening the file '{filename}' failed.")
        return None

    except ValueError:
        print(f"Error: something wrong on line '{line}'.")
        return None


def example_function_for_example_purposes(warehouse, parameters):
    """
    This function is an example of how to deal with the extra
    text user entered on the command line after the actual
    command word.

    :param warehouse: dict[int, Product], dict of all known products.
    :param parameters: str, all the text that the user entered after the command word.
    """

    try:
        # Let's try splitting the <parameters> string into two parts.
        # Raises ValueError if there are more or less than exactly two
        # values (in this case there should be one int and one float) in
        # the <parameters> string.
        code, number = parameters.split()

        # First parameter was supposed to be a products code i.e. an integer
        # and the second should be a float. If either of these assumptions fail
        # ValueError will be raised.
        code = int(code)
        number = float(number)

    except ValueError:
        print(f"Error: bad parameters '{parameters}' for example command.")
        return

    # <code> should be an existing product code in the <warehouse>.
    if code not in warehouse:
        print(f"Error: unknown product code '{code}'.")
        return

    # All the errors were checked above, so everything should be
    # smooth sailing from this point onward. Of course, the other
    # commands might require more or less error/sanity checks, this
    # is just a simple example.

    print("Seems like everything is good.")
    print(f"Parameters are: {code=} and {number=}.")


def is_integer(parameter):
    """
    Checks whether the parameter given by the user is an integer.
    :param parameter: str, the parameter given by the user.
    :return: bool, returns true if the parameter is an integer, otherwise false.
    """
    try:
        parameters = int(parameter)
        return True
    except ValueError:
        return False


def is_existing(data, parameter):
    """
    Checks whether a product code (parameter) given by the user exists in the
    used data.
    :param data: dict, the dict being used.
    :param parameter: str, the parameter given by the user.
    :return: bool, returns true if the product exists, otherwise false.
    """
    try:
        # To retrieve the possible Product object, the parameter must be
        # converted into an integer to match the keys in the data dict.
        product_object = data[int(parameter)]
        return True
    except (ValueError, KeyError):
        return False


def main():
    filename = input("Enter database name: ")
    # filename = "products.txt"

    warehouse = read_database(filename)
    if warehouse is None:
        return

    while True:
        command_line = input("Enter command: ").strip()

        if command_line == "":
            return

        command, *parameters = command_line.split(maxsplit=1)

        command = command.lower()

        if len(parameters) == 0:
            parameters = ""
        else:
            parameters = parameters[0]

        # If you have trouble undestanding what the values
        # in the variables <command> and <parameters> are,
        # remove the '#' comment character from the next line.
        # print(f"TEST: {command=} {parameters=}")

        if "example".startswith(command) and parameters != "":
            """
            'Example' is not an actual command in the program. It is
            implemented only to allow you to get ideas how to handle
            the contents of the variable <parameters>.

            Example command expects user to enter two values after the
            command name: an integer and a float:

                Enter command: example 123456 1.23

            In this case the variable <parameters> would refer to
            the value "123456 1.23". In other words, everything that
            was entered after the actual command name as a single string.
            """

            example_function_for_example_purposes(warehouse, parameters)

        elif "print".startswith(command) and parameters == "":
            # Print all known products in the ascending order of
            # the product codes.
            for product in sorted(warehouse):
                # Products are objects of the Product class, stored in the
                # warehouse dict as payloads.
                print(warehouse[product])

        elif "print".startswith(command) and parameters != "":
            # Print a single product when the product code is given. If
            # the product code is not an integer, or it doesn't exist in the
            # warehouse, an error message is printed.
            if is_integer(parameters) and is_existing(warehouse, parameters):
                print(warehouse[int(parameters)])
            else:
                print(f"Error: product '{parameters}' can not be printed as it"
                      f" does not exist.")

        elif "delete".startswith(command) and parameters != "":
            # Remove a product from the inventory if the product code given by
            # the user is an integer, and it exists. The stock has to be empty.
            if is_integer(parameters) and is_existing(warehouse, parameters):
                product = warehouse[int(parameters)]
                if product.is_stock_empty():
                    del warehouse[int(parameters)]
                # If there's stock left, an error message is printed.
                else:
                    print(f"Error: product '{parameters}' can not be deleted as"
                          f" stock remains.")
            # An error message is printed also if the code is not an integer or
            # existing.
            else:
                print(f"Error: product '{parameters}' can not be deleted as it "
                      f"does not exist.")

        elif "change".startswith(command) and parameters != "":
            # Change the amount of a product in stock.
            try:
                product_code, change = parameters.split()
                # If the parameters are integers and the product exists, change
                # its stock amount.
                if is_integer(product_code) and is_integer(change):
                    if is_existing(warehouse, product_code):
                        product = warehouse[int(product_code)]
                        product.modify_stock_size(int(change))
                    # If the product does not exist, print an error message.
                    else:
                        print(f"Error: stock for '{product_code}' can not be "
                              f"changed as it does not exist.")
                # Raise ValueError if parameters are not integers.
                else:
                    raise ValueError
            # Print a different error message if the user doesn't give correct
            # parameters (one product code and one change amount, integers).
            except ValueError:
                print(f"Error: bad parameters '{parameters}' for change command.")

        elif "low".startswith(command) and parameters == "":
            # Print the products under the low stock limit in the ascending
            # order of the product codes.
            for product in sorted(warehouse):
                product_object = warehouse[product]
                if product_object.is_low_stock():
                    print(warehouse[product])

        elif "combine".startswith(command) and parameters != "":
            # Combine two products into one by adding the second product's
            # stock to the first one's and deleting the second product.

            # Split the parameters to get the first and second product code as
            # separate parameters.
            first_parameter, second_parameter = parameters.split()

            try:
                if is_integer(first_parameter) and is_integer(second_parameter):
                    if is_existing(warehouse, first_parameter) and \
                            is_existing(warehouse, second_parameter):
                        first_product = warehouse[int(first_parameter)]
                        second_product = warehouse[int(second_parameter)]
                        # If products can be combined (same price and category,
                        # different codes), combine the stocks and delete the
                        # second code. The check_combinability method also prints
                        # possible error messages caused by products having
                        # different prices and categories or the same codes.
                        if first_product.check_combinability(second_product):
                            first_product.add_stock(second_product)
                            del warehouse[int(second_parameter)]
                        else:
                            continue
                    # If the product does not exist, an error is raised.
                    else:
                        raise KeyError
                # If either parameter is not an integer, an error is raised.
                else:
                    raise ValueError
            except (KeyError, ValueError):
                print(f"Error: bad parameters '{parameters}' for combine command.")

        elif "sale".startswith(command) and parameters != "":
            # Set a sale price for all the products in a category.

            category, percentage = parameters.split()
            # Check that the percentage is a float, otherwise an error message
            # is printed.
            try:
                float(percentage)
            except ValueError:
                print(f"Error: bad parameters '{category} {percentage}' "
                      f"for sale command.")
                continue

            # Initialise a counter to store the number of products belonging to
            # the discounted category.
            counter = 0
            # Go through each product in the warehouse and set the sale price
            # for the product if it belongs to the category being discounted.
            for product in warehouse:
                product_object = warehouse[product]
                if product_object.in_category(category):
                    product_object.set_sale_price(percentage)
                    counter += 1
            print(f"Sale price set for {counter} items.")

        else:
            print(f"Error: bad command line '{command_line}'.")


if __name__ == "__main__":
    main()
