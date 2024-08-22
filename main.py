import tkinter
import tkinter as tk  # Import the tkinter to create GUI application
from tkinter import ttk  # Import the ttk to create widgets and more modification
import json  # import json for create json file and work with json file
import tkinter.messagebox as messagebox  # import messagebox to create error msg
from datetime import datetime  # import date and time to validate date and time
from prettytable import PrettyTable  # import prettytable for view transaction and Display summery


class FinanceTrackerGUI:
    # construct methods
    def __init__(self, window):
        self.window = window  # method for window
        self.window.title("Personal Finance Tracker")  # create window title
        self.header()  # call method header
        self.transactions = self.load_transactions("data.json")  # Load transactions from a JSON file
        self.create_widgets()  # call method create_widgets
        self.display_transactions()  # call method display_transactions
        self.search_transactions()  # call method search_transactions
        self.create_style()  # call method create_style

    def create_style(self):  # create method
        self.style = ttk.Style(self.window)  # Initialize a style
        self.style.configure(
            "Custom.Treeview.Heading",
            font=("Arial", 8, "bold"),  # font for headings and configuration
        )

    def header(self):  # create method
        label_for_heading = tk.Label(  # Create a label for the heading
            self.window,
            text="Personal Finance Tracker",
            font=("Times New Roman", 20, "bold"),
            fg="yellow",
            bg="black"
        )
        label_for_heading.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    def create_widgets(self):  # create method

        treeview_frame = tk.Frame(self.window, bd=2, relief="solid", bg="white")  # create a border to the frame
        treeview_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=30, pady=30)
        frame_width = 400  # Set the frame width
        frame_height = 200  # Set the frame height
        treeview_frame.config(width=frame_width, height=frame_height)  # Configure the frame's size
        treeview_frame.pack_propagate(False)  # block automatic sizing

        # Create the Treeview widget with defined columns
        self.treeview_table = ttk.Treeview(treeview_frame, columns=('Category', 'Amount', 'Date'), show='headings',
                                           style="Custom.Treeview.Heading")
        # Define the headings for the Treeview
        self.treeview_table.heading('Category', text='Category', anchor="w")  # Left-align the text
        self.treeview_table.heading('Amount', text='Amount', anchor="w")  # Left-align the text
        self.treeview_table.heading('Date', text='Date', anchor="w")  # Left-align the text
        self.treeview_table.bind("<Button-1>", self.treeview_header_click)  # create a click event to headers
        my_style = ttk.Style(self.window)  # Create a new style for window
        my_style.theme_use('clam')
        my_style.configure('Treeview.Heading', background='silver')

        my_Scrollbar_bar = ttk.Scrollbar(self.treeview_table, orient=tk.VERTICAL,
                                         command=self.treeview_table.yview)  # Create a vertical scrollbar for the Treeview
        self.treeview_table.config(yscrollcommand=my_Scrollbar_bar.set)  # Command to update the Treeview
        my_Scrollbar_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def load_transactions(self, filename):  # create method
        try:  # use try for error handling
            with open(filename, 'r') as tk_file:  # open json file for read
                transactions = json.load(tk_file)  # load data from json file
                return transactions  # return to transaction
        except FileNotFoundError:  # if there is no json file this will execute
            print("!No file found with that name!")
            return {}
        except json.JSONDecodeError:  # if there is no data in json file this will execute
            print("!Unable to parse the JSON file!")
            return {}

    def display_transactions(self):  # create method
        self.treeview_table.delete(*self.treeview_table.get_children())  # Clear existing data in the Treeview

        for key, value in self.transactions.items():
            for item in value:
                self.treeview_table.insert('', 'end',
                                           values=(key, item['Amount'], item['Date']))  # insert data into treeview

    def search_transactions(self):  # create method
        text_box_label = tkinter.Label(self.window, text="Enter your Data", font=("Times New Roman", 10, "bold"),
                                       fg="#000080")  # create label for textbox
        text_box_label.pack(pady=0)

        text_box = tk.Text(self.window, height=1, width=14)  # create textbox
        text_box.pack(pady=5)

        def search_config():  # create method
            text_data = text_box.get("1.0", tk.END).strip().lower()  # take data in the text box
            found_matches = False  # check if any results are found
            self.treeview_table.delete(*self.treeview_table.get_children())  # Clear existing data in the Treeview
            if text_data in self.transactions:
                found_matches = True  # check if any results are found
                for trans_dict_category in self.transactions[text_data]:
                    self.treeview_table.insert('', 'end', values=(
                        text_data, trans_dict_category['Amount'],
                        trans_dict_category['Date']))  # insert data into treeview

            for key, values in self.transactions.items():
                for trans_dict_amount in values:
                    if text_data == str(trans_dict_amount['Amount']):  # check validity of the data
                        found_matches = True  # check if any results are found
                        self.treeview_table.insert('', 'end', values=(
                            key, trans_dict_amount['Amount'], trans_dict_amount['Date']))  # insert data into treeview

            for key, values in self.transactions.items():
                for trans_dict_date in values:
                    if text_data == trans_dict_date['Date']:  # check validity of the data
                        found_matches = True  # check if any results are found
                        self.treeview_table.insert('', 'end', values=(
                            key, trans_dict_date['Amount'], trans_dict_date['Date']))  # insert data into treeview

            if not found_matches: # If no results found show a messagebox as error
                self.display_transactions()
                messagebox.showerror("Error", "No transactions Found ")

        search_button = tk.Button(self.window, text="Search", height=1, width=6, bg="green", fg="white",
                                  font=("Arial", 8), command=search_config)   # create search button
        search_button.pack(pady=10)

    def treeview_header_click(self, event):  # create method
        self.treeview_table.delete(*self.treeview_table.get_children())  # Clear existing data in the Treeview
        select_id = self.treeview_table.identify_column(event.x)  # for identified  which column header was clicked
        if select_id == "#1":   # if user clicker first one (category)
            category_keys = list(self.transactions.keys())  # get keys as list
            category_keys.sort() # sort list to generate order
            for category_element in category_keys:
                for data_dict in self.transactions[category_element]:
                    self.treeview_table.insert('', 'end',  # insert data into treeview
                                               values=(category_element, data_dict['Amount'], data_dict['Date']))

        elif select_id == "#2":  # if user clicker second one (Amount)
            transactions = []   # get empty transaction list
            for key, values in self.transactions.items():
                for sub_value in values:
                    transaction = sub_value.copy()
                    transaction['Category'] = key
                    transactions.append(transaction)

            transactions_sorted = sorted(transactions, key=lambda x: x["Amount"])
            for data_amount in transactions_sorted:
                self.treeview_table.insert('', 'end',       # insert data into treeview
                                           values=(data_amount["Category"], data_amount['Amount'], data_amount['Date']))

        elif select_id == "#3":
            transactions = []
            for key, values in self.transactions.items():
                for sub_value in values:
                    transaction = sub_value.copy()  # Make a copy of the transaction data
                    transaction['Category'] = key  # Add the category to the copied data
                    transactions.append(transaction) # Add to the transactions list

            transactions_sorted = sorted(transactions, key=lambda x: x["Date"])  # Sort transactions by the "Amount" in ascending order
            for data_date in transactions_sorted:
                self.treeview_table.insert('', 'end',   # insert data into treeview
                                           values=(data_date["Category"], data_date['Amount'], data_date['Date']))


def open_gui(): # Function to create and open the GUI
    window = tk.Tk()
    app = FinanceTrackerGUI(window)
    window.geometry("600x500") # assign size
    window.mainloop()


if __name__ == "__main__":
    open_gui()

transactions = {}  # get empty dictionary for transaction


def load_transactions():  # lord transaction because this lord transaction have to use many places
    try:  # use try for error handling
        with open('data.json', 'r') as Load_trans:  # open json file for read
            data_dict = json.load(Load_trans)  # load data from json file
            transactions.update(data_dict)  # add current dictionaries to main dictionary
    except FileNotFoundError:
        print("!There is no file such that!")  # if there is no json file this will execute
    except json.JSONDecodeError:
        print("Note!No current data in json file")  # if there is no data in json file this will execute


def save_transaction():
    with open('data.json', 'w') as save_trans:  # open json file for write
        json.dump(transactions, save_trans)  # write data to json file


def read_bulk_transactions_from_file():
    try:  # use try for error handling
        with open('bulk_data.txt', 'r') as collect_data:  # open text file for read
            lines = collect_data.readlines()  # read data at ones and add into the list
            new_data = [line.strip('\n,') for line in
                        lines]  # remove "\n," in the lines list create new list called new_data
        cleaned_new_data = list(filter(None,
                                       new_data))  # when read data and get into list some time it coming with an empty list this use for remove that
        for to_dict in cleaned_new_data:
            clean_data = to_dict.split(
                ",")  # Split the string `to_dict` into a list of substrings using `,` as the delimiter and assign it to the variable `clean_data`
            transactions[clean_data[0]] = []  # create key value and make a empty list for store dictionary
            float_amount = float(clean_data[1])  # convert string amount into float
            transactions[clean_data[0]].append(
                {"Amount": float_amount, "Date": clean_data[2]})  # adding item to dictionary
        load_transactions()
        save_transaction()
    except FileNotFoundError:  # if there is no text file this will execute
        print("There is no file such that")


def add_transactions():
    load_transactions()
    global money_amount, transactions_date
    while True:  # while loop for iterate category if it is not a string value
        category = input("enter category of your transaction:").lower()
        if category.isalpha():  # using isalpha check whether category is not numeric value
            transactions[category] = []  # create key value and make a empty list for store dictionary
            break
        else:
            print("!you can only enter string type value!")
            continue  # continue if it is not a string value

    while True:  # while loop for iterate money_amount if it is not a integer Value
        try:  # use try except for make sure Amount is integer Value
            money_amount = float(
                input("enter amount of money:"))  # using float because its enable to input cent values(eg-348.45)
            break
        except ValueError:  # if user enter string type this will execute
            print("!you can only enter integer values!")
            continue

    while True:  # while loop for iterate transaction_date if it is not in correct format
        try:
            transactions_date = input("enter date of your transaction:(yyyy-mm-dd):")
            date_format = datetime.strptime(transactions_date,
                                            '%Y-%m-%d')  # set transaction_date(string) into date format
            year = date_format.year  # Set aside the date to check
            if year == 2024:  # check given transaction is relevant to 2024
                break
            else:
                print("year you entered unmatched|You must enter 2024 transaction")
                continue  # continue when its not relevant to 2024
        except:
            print("!invalid Date!|Format(yyyy-mm-dd)")
            continue  # continue when it is not in correct format
    while True:  # while loop for iterate next_round
        next_round = input("Do you want to add another item|yes/No|:").lower()
        if next_round == "yes":
            transactions[category].append(
                {"Amount": money_amount, "Date": transactions_date})  # adding dictionary to list
            add_transactions()  # call add transaction function if user want to add another item
        elif next_round == "no":
            load_transactions()
            transactions[category].append(
                {"Amount": money_amount, "Date": transactions_date})  # adding dictionary to list
            save_transaction()
            print("Your transaction/s added successfully ")
            break
        else:
            print("you can only enter yes or no")
            continue  # continue when next_round input is not yes or no
        break


def view_transaction():
    print("your all the transaction below")
    transactions.clear()  # use clear transaction because when view transaction repeat current data get doubled
    load_transactions()  # read the current data in json file
    for key, value in transactions.items():
        count_number = 1
        print(key.capitalize())  # use capitalize to create title
        table = PrettyTable(["Number", "Amount", "Date"])  # create table and assign field name
        for sub_data in value:
            table.add_row([count_number, sub_data["Amount"], sub_data["Date"]])  # adding data to the table
            count_number += 1
        print(table, "\n")


def update_transaction():
    view_transaction()  # view current transaction to user
    print("-------------------------------------------")
    update_transaction_Category = input(
        "what transaction category do want to update(enter transaction category):").lower()
    found_categories = []  # Collect all matching categories
    for key, value in transactions.items():
        lower_key = key.lower()  # check user input and key of the dictionary are matched
        if lower_key == update_transaction_Category:
            found_categories.append(key)
    if not found_categories:  # if user input and key of the dictionary unmatch this part execute
        print("!Please enter a correct category!")
        update_transaction()
    else:
        while True:  # while loop for iterate update_transaction_number if it is not a integer Value
            try:
                update_transaction_number = int(input("Enter transaction number do you want to update:"))
                if 0 < update_transaction_number <= len(
                        transactions[update_transaction_Category]):  # check user transaction number is valid one or not
                    print(f"1)Category-{update_transaction_Category}"
                          f"\n2)Amount-{transactions[update_transaction_Category][update_transaction_number - 1]['Amount']}\n3)Date-"
                          f"{transactions[update_transaction_Category][update_transaction_number - 1]['Date']}")
                    while True:  # while loop for iterate  select_update_transaction  if it is not a integer Value
                        try:
                            select_update_transaction = int(input("Enter Number you want to update(1 | 2 | 3):"))
                            if select_update_transaction == 1:  # if user input 1 update category of transaction
                                new_category = input("Enter your New category:")
                                transactions[new_category] = transactions.pop(
                                    update_transaction_Category)  # update new category
                                save_transaction()
                                print("Transaction successfully update ")
                                break
                            elif select_update_transaction == 2:  # if user input 2 update amount of the transaction
                                while True:  # while loop for iterate New_amount if it is not a float Value or integer value
                                    try:
                                        New_amount = float(input("Enter new Amount:"))
                                        transactions[update_transaction_Category][update_transaction_number - 1][
                                            'Amount'] = New_amount  # update new amount
                                        save_transaction()
                                        print("Transaction successfully update ")
                                        break
                                    except ValueError:
                                        print("!you can enter only integer Value!")
                                        continue
                                break
                            elif select_update_transaction == 3:  # if user input 3 update amount of the transaction
                                try:
                                    while True:  # while loop for iterate new date if it is not relevant to given format
                                        new_Date = input("enter new Date(yyyy-mm-dd):")
                                        date_format = datetime.strptime(new_Date,
                                                                        '%Y-%m-%d')  # set transaction_date(string) into date format
                                        year = date_format.year  # Set aside the date to check
                                        if year == 2024:  # execute if it is only 2024 transaction
                                            transactions[update_transaction_Category][update_transaction_number - 1][
                                                'Date'] = new_Date
                                            save_transaction()
                                            print("Transaction successfully update ")
                                            break
                                        else:
                                            print("year you entered unmatched|You must enter 2024 transaction")
                                            continue  # continue when it's not relevant to 2024
                                except:  # if new_date not in given format this will execute
                                    print("!invalid Date!|Format(yyyy-mm-dd)!")
                                    continue
                                break
                            else:  # execute when select transaction number other than 1,2,or 3
                                print("!You can only enter 1|2|3!")
                                continue
                        except ValueError:  # execute when it is not and integer value
                            print("!youcan only enter integer values!")
                            continue

                    break

                else:  # execute when transaction number invalid
                    print("!Enter valid Transaction!")
                    continue
            except ValueError:  # execute when transaction number string type
                print("!Enter valid Transaction!")
                continue
    while True:
        choice = input("Do you want to update another transaction? (yes/no): ").lower()
        if choice == "yes":
            update_transaction()
            break
        elif choice == "no":
            break
        else:
            print("!Please enter either 'yes' or 'no'!")
            continue


def Display_summury():
    load_transactions()  # load the current transaction from the json file
    Total_Expense = 0  # get variable for total income and total expense
    table1 = PrettyTable()  # create table for total Expense
    table1.field_names = ["Category", "Amount"]  # assign field name
    for key, values in transactions.items():
        Total_Expense_item = sum(expense["Amount"] for expense in values)  # get total amount of the transaction
        Total_Expense += Total_Expense_item
        table1.add_row([key, Total_Expense_item])  # add data to the table
    print(
        f"  Your Total Expense\n{table1}\n   Total            {Total_Expense}")


def Delete_transaction():
    view_transaction()
    delete_transaction_category = input("What transaction do you want to delete: ")
    delete_transaction_category_lower = delete_transaction_category.lower()  # convert delete_transaction_category in to lower

    found_categories = []  # Collect all matching categories

    for key, value in transactions.items():  # find delete_transaction_category is match with transaction dictionary
        lower_key = key.lower()
        if lower_key == delete_transaction_category_lower:
            found_categories.append(key)

    if not found_categories:  # if it is not match this will execute
        print("!Please enter a correct category!")
        Delete_transaction()
    else:
        for category in found_categories:
            while True:  # while loop for iterate  delete_transaction_number  if it is not a integer Value
                try:
                    delete_transaction_number = int(input("Enter transaction number: "))
                    if 0 < delete_transaction_number <= len(
                            transactions[category]):  # check user transaction number is valid one or not
                        del transactions[category][delete_transaction_number - 1]  # delete transaction
                        print("Transaction Delete successfully")
                        if not transactions[category]:  # delete empty list in dictionary
                            del transactions[category]
                        save_transaction()
                        break
                    else:
                        print("!Invalid number. Please check your transaction number!")
                        continue
                except ValueError:  # execute when delete_transaction number is not an integer value
                    print("!Please enter an integer value!")
                    continue
            break
    while True:
        choice = input("Do you want to delete another transaction? (yes/no): ").lower()
        if choice == "yes":
            Delete_transaction()
            break
        elif choice == "no":
            break
        else:
            print("!Please enter either 'yes' or 'no'!")
            continue


def menu():
    while True:  # use while True for iterate main menu
        try:
            print("|WELCOME TO YOUR FINANCE Tracker|")
            print("-------------------------------")
            print("1)Add Transaction")
            print("2)View Transactions")
            print("3)Update Transaction")
            print("4)Delete Transaction")
            print("5)Display Summary")
            print("6)Open GUI")
            print("7)Exit")
            choice = int(input("Enter your choice(Enter Number): "))
            read_bulk_transactions_from_file()  # call  read_bulk_transactions_from_file()
            if choice == 1:
                add_transactions()  # call add_transactions()
                continue
            elif choice == 2:
                view_transaction()  # call view_transaction()
                continue
            elif choice == 3:
                update_transaction()  # call update_transaction()
                continue
            elif choice == 4:
                Delete_transaction()  # call Delete_transaction()
                continue
            elif choice == 5:
                Display_summury()  # call Display_summury()
                continue
            elif choice == 6:
                open_gui()
            elif choice == 7:
                break  # exit from while loop

            else:
                print("!Invalid choice!")
                continue  # continue if it is not in 1-6
        except ValueError:
            print("!you can only enter integer values!")
            continue  # continue  if it is not an integer


menu()  # call main menu
