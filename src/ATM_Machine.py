class UserInfo:
    def __init__(self, first_name, surname, mobile, account_owner_id):   # __init__ to assign values to objects 
        # arguments
        self.first_name = first_name
        self.surname = surname
        self.mobile = mobile
        self.account_owner_id = account_owner_id
    
    @classmethod
    def from_file(cls, file_path): # arguments being passed as parameters to 'from_file' 
        with open(file_path, 'r+') as f:    #with = o open and manage files.     # open(file_path, 'r+') = automatically close the file after being used.  # opens the file specified by file_path in read and write mode 'r+'.   #f = This variable can be used to interact with the file later on in the program
            lines = f.readlines()[1:]  # eads all lines from the file object, removes the first line, and returns the remaining lines as a list of strings, also skips the header in the txt files
            users = [] # creates list
            for line in lines:   # for loop.     line = variable assigned to each line in lines        in = iterate over 'lines'
                fields = line.strip().split(',') # fields = variable assigned to the sub strings                       line.split(','): This is a method that splits the string into a list of substrings
                if len(fields) < 3:    #len(fields) < 3 = checks if the line of text being processed is less then 3 
                    fields.extend(["N/A"] * (4 - len(fields))) # add default values for missing fields
                first_name, surname, mobile, account_owner_id = fields # assigns the values in the fields list to the variables 
                user = cls(first_name, surname, mobile, account_owner_id) # new instance of the UserInfo class and assigns it to the variable user.   # cls = current class 
                users.append(user) # adds each newly created user instance to the users list. By the end of the from_file method, the users list contains all the UserInfo 
        return users # returns the users list containing all the UserInfo

class OpeningAccountData:
    def __init__(self, account_owner_id, account_number, account_type, opening_balance):
        self.account_owner_id = account_owner_id
        self.account_number = account_number
        self.account_type = account_type
        self.opening_balance = opening_balance
    
    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r+') as f:
            lines = f.readlines()[1:] 
            accounts = []
            for line in lines:
                fields = line.strip().split('|||')
                account_owner_id, account_number, account_type, opening_balance = fields
                account = cls(account_owner_id, account_number, account_type, opening_balance)
                accounts.append(account)
        return accounts


def get_account_types_and_numbers(accounts, account_owner_id):  # function is used the fetch the user's accounts 
    account_types_and_numbers = [] # creates list
    for account in accounts:
        if account.account_owner_id == account_owner_id:      # if the 'account.account_owner_id' matches the 'account_owner_id' 
            account_types_and_numbers.append((account.account_type, account.account_number)) # creates a list of tuples, each tuple contains the account type and account number 
    return account_types_and_numbers # retuns the account_types_and_numbers when the function is called 


# Retrieve the user information from the file
users = UserInfo.from_file("data/UserInfo.txt") #creates a list of UserInfo objects by calling the from_file class method of the UserInfo class.
accounts = OpeningAccountData.from_file("data/OpeningAccountsData.txt") #creates a list of OpeningAccountData objects by calling the from_file class method of the OpeningAccountData class.


def update_balance_file(file_path, account_number, new_balance):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    with open(file_path, 'w') as f:
        for line in lines:
            fields = line.strip().split('|||')
            if fields[1] == account_number:
                fields[3] = str(new_balance)
                line = '|||'.join(fields) + '\n'
            f.write(line)


#ACCOUNT SUMMARY
def print_account_summary(account_types_and_numbers, accounts):
    print("Please find your account summary below:")
    for i, (account_type, account_number) in enumerate(account_types_and_numbers):
        for acc in accounts:
            if acc.account_type == account_type and acc.account_number == account_number:
                print(f"{i+1}. Account Type:{account_type}   Account Number:{account_number}   Account Balance:{acc.opening_balance}")
                continue
                # print_account_summary(account_types_and_numbers, accounts)



while True:
    # Ask the user to input their ID number
    user_id_number = input("Please enter your ID number: ")

    # Check if the user's ID number matches the account owner ID
    matched = False
    for user in users:
        if user_id_number == user.account_owner_id:
            print(f"Welcome {user.first_name} {user.surname}! Please select an option: 1, 2, 3, or q.")
            matched = True
            

    if not matched:
        print("Your ID number is incorrect, please try again!")
        continue
    # if the user's ID number does not match send user to start

    # Menu options
    banking_options = {
        '1': 'Deposit',
        '2': 'Withdraw',
        '3': 'Balance',
        'q': 'Quit'
    }

    
    # assigning the menu item a key and value
    print("Please select an option: ")
    for key, value in banking_options.items():
        print(f"{key}: {value}")

    # storing the user choice inside user choice
    user_choice = input("Select from the menu: ")

    # valid input check for the menu 
    if user_choice not in banking_options:
        print("Wrong input - Please make sure to enter a valid input.")
        continue



    # Process the user's choice to select an option
    if user_choice == "1": #DEPOSIT
        account_types_and_numbers = get_account_types_and_numbers(accounts, user_id_number)
        print("Which account do you wish to deposit into: ")
        for i, (account_type, account_number) in enumerate(account_types_and_numbers):
            print(f"{i+1}. {account_type}: {account_number}")

        # Get the user's choice of bank account
        account_choice = int(input("Select an account: "))
        if account_choice >= 1 and account_choice <= len(account_types_and_numbers):
    
            # Get the deposit amount from the user
            try:
                deposit_amount = float(input("Enter the amount you wish to deposit: "))
                print("You entered a valid deposit amount of:", deposit_amount)
            # Error check - If the users input is unable to be converted to an integer it means the input was invalid  
            except ValueError:
                print("Invalid deposit amount. Please enter a valid number.")
                continue

            # Find the selected account and update its balance
            for i, (account_type, account_number) in enumerate(account_types_and_numbers):
                if i+1 == account_choice:
                    for account in accounts:
                        if account.account_number == account_number:
                            account.opening_balance = str(float(account.opening_balance) + deposit_amount)

                            # prints the account plus the new opening balance
                            print(f"Deposit successful! The new balance for account {account_number} is {account.opening_balance}")
                            # Update the balance in the account object
                            account.opening_balance = str(float(account.opening_balance))

                            # Update the .txt file with the new balance
                            update_balance_file('data/OpeningAccountsData.txt', account.account_number, account.opening_balance)
                            # Prints selected account infomation 
                            print_account_summary(account_types_and_numbers, accounts)
        else:
            # The account choice is not valid - return user to start
            print("Wrong Input - Invalid account number selected.")
            continue


    elif user_choice == "2": # WITHDRAW
        account_types_and_numbers = get_account_types_and_numbers(accounts, user_id_number)
        print("Which account do you wish to withdraw from: ")
        for i, (account_type, account_number) in enumerate(account_types_and_numbers):
            print(f"{i+1}. {account_type}: {account_number}")

        # Get the user's choice of bank account
        account_choice = int(input("Select an account: "))
        if account_choice >= 1 and account_choice <= len(account_types_and_numbers):
           
            # Get the Withdraw amount from the user
            try:
                withdraw_amount = float(input(f"Enter the amount you wish to withdraw: "))
                print("You entered a valid deposit amount of:", withdraw_amount )
            # Error check - If the users input is unable to be converted to an integer it means the input was invalid  
            except ValueError:
                    print("Invalid deposit amount. Please enter a valid number.")
                    continue

            # Find the selected account and update its balance
            for i, (account_type, account_number) in enumerate(account_types_and_numbers):
                if i+1 == account_choice:
                    for account in accounts:
                        if account.account_number == account_number:
                            # checks if the user withdraw amount is greater then the current opening balance 
                            if withdraw_amount > float(account.opening_balance):
                                print(f"Error - Amount entered {withdraw_amount} which is greater than amount in account")

                            else:
                                # Takes the opening balance subtracts the users Withdraw amount 
                                account.opening_balance = str(float(account.opening_balance) - withdraw_amount)
                                print(f"The new balance for account {account_number} is {account.opening_balance}")
                                # Updates the balance in the account object
                                account.opening_balance = str(float(account.opening_balance))

                                # Update the .txt file with the new balance
                                update_balance_file('data/OpeningAccountsData.txt', account.account_number, account.opening_balance)
                                # Prints selected account infomation 
                                print_account_summary(account_types_and_numbers, accounts)
        else:
            # The account choice is not valid - return user to start
            print("Wrong Input - Invalid account number selected.")
            continue
                         
                            



    elif user_choice  == "3":# BALANCE
        account_types_and_numbers = get_account_types_and_numbers(accounts, user_id_number)
        print("Which account do you wish to check the balance of: ")
        for i, (account_type, account_number) in enumerate(account_types_and_numbers):
            print(f"{i+1}. {account_type}: {account_number}")

        # Get the user's choice of bank account
        account_choice = int(input("Select an account: "))
        if account_choice >= 1 and account_choice <= len(account_types_and_numbers):


            # Find the selected account and update its balance
            for i, (account_type, account_number) in enumerate(account_types_and_numbers):
                if i+1 == account_choice:
                    for account in accounts:
                        if account.account_number == account_number:
                            # Prints the account type and account plus the opening balance
                            print(f"The opening balanmce of account ({account_type} - {account_number}) = {account.opening_balance}")
                            # Prints selected account infomation 
                            print_account_summary(account_types_and_numbers, accounts)
        else:
                # The account choice is not valid - return user to start
                print("Wrong Input - Invalid account number selected.")
                continue
                     

  
    
    elif user_choice == "q":
        #reads OpeningAccountData.txt and stores the data inide accounts
        accounts = OpeningAccountData.from_file("data/OpeningAccountsData.txt")
        # A for loop which iterates each 'account' inside 'accounts' and prints the results 
        # The last print statement is empty to provide a space between each account for better readability
        for account in accounts:
            print("Account name: ", account.account_owner_id)
            print("Account type: ", account.account_type)
            print("Account number: ", account.account_number)
            print("Balance:", account.opening_balance)
            print()
        break # Quits the program if q was selected




    

    
# User will now loop back to the start of the program as it's a while loop      