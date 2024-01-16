"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Saana Hänninen
13.10 Project: Graphical User Interface.
The program works as a to-do list that shows to-dos (stored in a .txt file)
in alphabetical and priority order. The program allows the user to add and delete to-dos,
which will then lead to changes in the used .txt file. The aim was to create an advanced
GUI (using components not covered in the course materials).

Photos unsplash.com
"""

from tkinter import *


class TodoGUI:
    """
    Class TodoGUI: defines what actions can be done and how the .txt file is used.
    """

    def __init__(self):
        """
        Initialises the components of the GUI.
        """
        self.__mainw = Tk()
        self.__mainw.title(f"To-Do List")
        self.__main_title = Label(self.__mainw, text="To-Do List",
                                  font="Helvetica 36", justify="center")
        self.__main_title.grid(row=0, column=5, columnspan=6, padx=(30, 0), sticky=W)
        self.__close_button = Button(self.__mainw, text="Exit", command=self.__mainw.destroy)
        self.__close_button.grid(row=5, column=10, columnspan=2, padx=(0, 10), sticky=E)

        # Photo widgets
        self.__main_photo = PhotoImage(file="main.png")
        self.__added_photo = PhotoImage(file="added.png")
        self.__deleted_photo = PhotoImage(file="deleted.png")
        self.__dashboard_photo = PhotoImage(file="dashboard.png")

        self.__main_photo_label = Label(self.__mainw, image=self.__main_photo)
        self.__main_photo_label.grid(row=0, column=0, rowspan=6, columnspan=4,
                                     pady=10, padx=10)

        self.__dashboard_photo_label = Label(self.__mainw, image=self.__dashboard_photo)

        # File opening widgets
        self.__filename_label = Label(self.__mainw, text="Enter the name of your to-do file",
                                      justify="left")
        self.__filename_label.grid(row=1, column=5, columnspan=6, padx=(30, 0),
                                   sticky=W)

        self.__filename = Entry()
        self.__filename.grid(row=2, column=5, padx=(30, 0), sticky=N)

        self.__file_button = Button(self.__mainw, text="Continue", command=self.check_file)
        self.__file_button.grid(row=2, column=11, padx=(0, 10), sticky=N)

        self.__errormessage = Label(self.__mainw, justify="left")
        self.__errormessage.grid(row=3, column=5, columnspan=4, padx=(30, 10),
                                 sticky=N)

        # Instruction widgets
        self.start_instruction_label = \
            Label(self.__mainw, text="Works with\n- .txt files\n- max 10 different "
                                     "to-dos in format priority;to-do\n- priorities "
                                     "high/low\n- to-do length 3-40 characters",
                  justify="left", font="Helvetica 12 italic")
        self.start_instruction_label.grid(row=3, column=5, columnspan=4,
                                          padx=(30, 10), sticky=N)

        self.__instruction_label = Label(self.__mainw,
                                         text="Select an action from the menu on the left",
                                         justify="left")

        # Dashboard widgets
        self.__dashboard_title = Label(self.__mainw, text="Current To-Dos",
                             font="Helvetica 24")
        self.__dashboard_content = Label(self.__mainw)

        # Menu widgets
        self.__add_new_button = Button(self.__mainw, text="Add",
                                       command=self.add_input, borderwidth=2,
                                       relief=GROOVE, height=3, width=10,
                                       highlightbackground="#FFFFFF")

        self.__delete_button = Button(self.__mainw, text="Delete",
                                       command=self.delete_input, borderwidth=2,
                                       relief=GROOVE, height=3, width=10,
                                      highlightbackground="#FFFFFF")

        self.__open_button = Button(self.__mainw, text="Open...",
                                       command=self.open_file, borderwidth=2,
                                       relief=GROOVE, height=3, width=10,
                                    highlightbackground="#FFFFFF")
        self.__exit_button = Button(self.__mainw, text="Exit",
                                       command=self.__mainw.destroy, borderwidth=2,
                                    relief=GROOVE, height=3, width=10,
                                    highlightbackground="#FFFFFF")

        # To-do adding widgets
        self.__add_label = Label(self.__mainw, text="Write a new to-do\n"
                                                    "(3-40 characters)", justify="left")
        self.__add_todo = Entry()
        self.__added_label = Label(self.__mainw)

        self.__btn = StringVar(self.__mainw, "high")
        self.__priority_label = Label(self.__mainw,
                                      text="Select the priority level", justify="left")
        self.__high_radiobutton = Radiobutton(self.__mainw, text="High priority",
                                              variable=self.__btn, value="high")
        self.__low_radiobutton = Radiobutton(self.__mainw, text="Low priority",
                                             variable=self.__btn, value="low")

        self.__add_button = Button(self.__mainw, text="Add", command=self.add_todo)

        # Deleting widgets
        self.__delete_label = Label(self.__mainw, text="Give the number of "
                                                       "the to-do to be deleted")
        self.__delete_number = Entry()
        self.__deleted_label = Label(self.__mainw)
        self.__delete_btn = Button(self.__mainw, text="Delete", command=self.delete_todo)

        # Mainloop
        self.__mainw.mainloop()

    def check_file(self):
        """
        Checks whether the file can be opened for use. If so, the dashboard,
        menu and new instructions will be displayed.
        :return: str | None, returns the filename if the file will be used,
        otherwise None.
        """
        filename = self.__filename.get()

        try:
            file = open(filename, mode="r")
            # Use line_check to check whether the requirements for lines
            # (format, length...) are met, and continue in the try part if so.
            if self.line_check(file):
                self.insert_dashboard()
                self.insert_instructions()
                self.insert_menu()
                self.__errormessage.grid_forget()
                # The initial exit button won't be needed as the user can now
                # exit from the menu on the left.
                self.__close_button.grid_forget()
                self.start_instruction_label.grid_forget()
                self.__add_new_button.configure(state=NORMAL)
                self.__delete_button.configure(state=NORMAL)
                return filename
            else:
                raise Exception

        except (OSError, Exception):
            self.__errormessage.configure(text=f"Opening the file '{filename}' failed."
                                               f"\nPlease check the file requirements"
                                               f" below and try again.")
            self.__filename.delete(0, END)
            self.start_instruction_label.grid(row=4, column=5, columnspan=4,
                                              padx=(30, 10), sticky=N)
            return None

    def line_check(self, file):
        """
        Checks whether the file the user wants to open meets the line
        requirements: max 10 lines in format priority;to-do and to-do length
        3-40 characters. The same to-do can't exist twice.
        :param file: file, the file the user is trying to open.
        :return: bool, returns true if the file is ok to be used, otherwise false.
        """
        try:
            lines = file.readlines()
            if len(lines) == 0:
                return True
            line_number = 1
            lines_list = []
            for line in lines:
                if line_number > 10:
                    return False
                prio, todo = line.rstrip().rsplit(";")
                if prio != "high" and prio != "low":
                    return False
                if len(todo) < 3 or len(todo) > 40:
                    return False
                line_number += 1
                if line not in lines_list:
                    lines_list.append(line)
                else:
                    return False

        except ValueError:
            return False

        return True

    def insert_dashboard(self):
        """
        Inserts the dashboard widgets that will be displaying the file contents.
        """
        self.__dashboard_title.grid(row=7, column=2, columnspan=2)
        self.__dashboard_content.grid(row=8, column=2, columnspan=2, rowspan=8,
                                      sticky=N)
        self.__dashboard_photo_label.grid(row=7, column=5, columnspan=3, rowspan=14, pady=10, sticky=NW)

        # Use display_todos to display each to-do in the file.
        self.display_todos()

    def insert_instructions(self):
        """
        Inserts the instruction widget that tells the user to select an action
        from the menu.
        """
        # Clear the top section of the GUI to make space for the instructions.
        self.empty_top()
        self.__instruction_label.grid(row=1, column=5, columnspan=4,
                                      padx=(30, 10), sticky=N)

    def insert_menu(self):
        """
        Inserts the menu on the left of the GUI containing buttons for adding
        new to-dos, deleting to-dos, opening a new file and exiting.
        """
        self.__add_new_button.grid(row=8, column=0, columnspan=2, sticky=N)
        self.__delete_button.grid(row=9, column=0, columnspan=2, sticky=N)
        self.__open_button.grid(row=10, column=0, columnspan=2, sticky=N)
        self.__exit_button.grid(row=11, column=0, columnspan=2, sticky=N)

    def empty_top(self):
        """
        Clears the top of the GUI of various widgets to make space for displaying
        new content.
        """
        self.__instruction_label.grid_forget()
        self.start_instruction_label.grid_forget()
        self.__add_label.grid_forget()
        self.__add_todo.grid_forget()
        self.__high_radiobutton.grid_forget()
        self.__low_radiobutton.grid_forget()
        self.__add_button.grid_forget()
        self.__filename.grid_forget()
        self.__file_button.grid_forget()
        self.__filename_label.grid_forget()
        self.__errormessage.configure(text="")
        self.__errormessage.grid_forget()
        self.__added_label.grid_forget()
        self.__delete_label.grid_forget()
        self.__delete_number.grid_forget()
        self.__deleted_label.grid_forget()
        self.__delete_btn.grid_forget()
        self.__priority_label.grid_forget()

    def open_file(self):
        """
        Displays the widgets needed for opening a new file. Will be called when
        the "Open..." button is clicked. Here, adding and deleting to-dos to
        the previously open file is disabled.
        """
        # Clear the top section of the GUI to make space for the file opening
        # widgets.
        self.empty_top()

        self.__filename_label.grid(row=1, column=5, columnspan=6, padx=(30, 0), sticky=W)
        self.__filename.grid(row=2, column=5, padx=(30, 0), sticky=N)
        self.__file_button.grid(row=2, column=11, padx=(0, 10), sticky=N)
        self.__errormessage.grid(row=3, column=5, columnspan=4, padx=(30, 10), sticky=N)

        self.__add_new_button.configure(state=DISABLED)
        self.__delete_button.configure(state=DISABLED)

    def sort_todos(self):
        """
        Divides the to-dos to high and low priority to-dos and puts them in
        alphabetical order.
        :return: list, returns the lists of high and low priority to-dos.
        """
        filename = self.__filename.get()
        file = open(filename, mode="r")
        high_prios = []
        low_prios = []
        for line in file:
            # Use try-except to avoid any errors when splitting the lines.
            # If there is, for some reason, lines that don't have a
            # semicolon in the file, skip them.
            try:
                prio, todo = line.rstrip().split(";")
            except ValueError:
                continue
            if prio == "high":
                high_prios.append(todo)
            else:
                low_prios.append(todo)

        high_prios = sorted(high_prios)
        low_prios = sorted(low_prios)

        return high_prios, low_prios

    def display_todos(self):
        """
        Displays the to-dos in the dashboard. Each to-do will be given a number
        to highlight the total amount of to-dos and to help with deleting them
        later on.
        """
        # Call sort_todos to get the to-dos in two alphabetically ordered
        # priority lists.
        high_prios, low_prios = self.sort_todos()

        printable_high_prios = ""
        printable_low_prios = ""

        # Assign a number to each to-do, then add each to-do to the string
        # containing priorities that are ready to be shown.
        num = 1
        for todo in high_prios:
            high_prio = f"{num}. {todo}"
            printable_high_prios += f"\n{high_prio}"
            num += 1
        for todo in low_prios:
            low_prio = f"{num}. {todo}"
            printable_low_prios += f"\n{low_prio}"
            num += 1

        if len(printable_high_prios) == 0:
            printable_high_prios = f"You have no high priority to-dos"
        if len(printable_low_prios) == 0:
            printable_low_prios = f"You have no low priority to-dos"

        # Set the dashboard content to be the numbered to-dos.
        dashboard_content = f"High priorities:\n{printable_high_prios} \n \n" \
                            f"Low priorities:\n{printable_low_prios} \n \n"
        self.__dashboard_content.configure(text=dashboard_content, justify="left")

    def add_input(self):
        """
        Displays the widgets needed for adding a new to-do. Will be called when
        the "Add" button is clicked.
        """
        # Clear the top section of the GUI to make space for the to-do adding
        # widgets.
        self.empty_top()

        self.__add_label.grid(row=1, column=5, columnspan=6, padx=(30, 0), sticky=W)
        self.__add_todo.grid(row=2, column=5, padx=(30, 0), sticky=N)
        self.__priority_label.grid(row=2, column=5, columnspan=6, padx=(30, 0), sticky=SW)
        self.__high_radiobutton.grid(row=3, column=5, padx=(15, 0), sticky=W)
        self.__low_radiobutton.grid(row=3, column=5, sticky=E)
        self.__add_button.grid(row=2, column=11, padx=(0, 10), sticky=N)

    def delete_input(self):
        """
        Displays the widgets needed for deleting a to-do. Will be called when
        the "Delete" button is clicked.
        """
        # Clear the top section of the GUI to make space for the deleting widgets.
        self.empty_top()

        self.__delete_label.grid(row=1, column=5, columnspan=6, padx=(30, 0), sticky=W)
        self.__delete_number.grid(row=2, column=5, padx=(30, 0), sticky=N)
        self.__delete_btn.grid(row=2, column=10, padx=(0, 10), sticky=N)

    def add_todo(self):
        """
        Adds a new to-do entered by the user if there's space in the file (max 9
        to-dos at the moment of entering a new one), the to-do is 3-40
        characters, and it doesn't exist yet. The photo by the dashboard will
        also be changed to added_photo if the adding is successful.
        """
        # Get the filename and check the file before trying to add the new to-do.
        filename = self.check_file()

        line_counter = 0
        # Initialise a list to hold already existing to-dos.
        already_existing = []
        file = open(filename, mode="r")
        for line in file:
            # Use try-except to avoid any errors in reading the lines.
            try:
                line_counter += 1
                priority, to_do = line.rstrip().split(";")
                already_existing.append(to_do)
            except ValueError:
                continue

        if 0 <= line_counter <= 9:
            priority = self.__btn.get()
            todo = self.__add_todo.get()
            if 2 < len(todo) <= 40 and todo not in already_existing and todo.isspace() is False:
                file = open(filename, mode="a")
                if line_counter == 0:
                    print(f"{priority};{todo}", end="", file=file)
                else:
                    print(f"\n{priority};{todo}", end="", file=file)
                self.__added_label.configure(text="To-do added to the list")
                self.__dashboard_photo_label.configure(image=self.__added_photo)
            elif 40 < len(todo) or len(todo) < 3 or todo.isspace():
                self.__added_label.configure\
                    (text="Make sure your to-do is 3-40 characters")
            else:
                self.__added_label.configure\
                    (text="Please enter a to-do that does not exist yet")
        else:
            self.__added_label.configure(
                text="Your to-do list is already full\nPlease remove a to-do and try again")

        file.close()
        self.__add_todo.delete(0, END)
        self.__added_label.grid(row=2, column=5, columnspan=4, padx=(30, 10))
        self.__instruction_label.grid_forget()
        self.display_todos()

    def delete_todo(self):
        """
        Deletes a to-do that the user wishes to be deleted if it exists.
        The photo by the dashboard will also be changed to deleted_photo if the
        deletion is successful.
        """
        # Get the filename and check the file before trying to delete the to-do.
        filename = self.check_file()

        high_prios, low_prios = self.sort_todos()
        prios = high_prios + low_prios
        # Initialise to_be_saved string to hold all to-dos that won't be deleted.
        to_be_saved = ""

        try:
            number_to_be_deleted = int(self.__delete_number.get())
            to_be_deleted = prios[number_to_be_deleted-1]
            for line in open(filename, mode="r"):
                line_parts = line.rstrip().split(";")
                # Go through each to-do and add them to to_be_saved unless it's
                # the to-do the user wishes to delete.
                if line_parts[1] != to_be_deleted:
                    to_be_saved += f"{line_parts[0]};{line_parts[1]}\n"
            # Write the file with to_be_saved string.
            file = open(filename, mode="w")
            print(f"{to_be_saved}", end="", file=file)

            self.__deleted_label.configure(text=
                                            f"To-do number {number_to_be_deleted}"
                                            f" has been deleted.")
            self.__dashboard_photo_label.configure(image=self.__deleted_photo)
            self.__delete_btn.grid_forget()
            file.close()
        except (ValueError, IndexError):
            self.__deleted_label.configure(text=f"To-do could not be deleted."
                                                f" Make sure to enter an integer "
                                                f"that exists in the to-do list below.")

        self.__deleted_label.grid(row=2, column=5, columnspan=4, padx=(30, 10))
        self.__delete_number.delete(0, END)
        self.__instruction_label.grid_forget()
        self.display_todos()


def main():
    todogui = TodoGUI()


if __name__ == "__main__":
    main()
