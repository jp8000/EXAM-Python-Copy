# python -m pytest
# python -m pytest -v = see all test results 
# cd into the "tests" folder before running the pytest

import os
from src.ATM_Machine import update_balance_file, print_account_summary, get_account_types_and_numbers, OpeningAccountData


def test_update_balance_file():
    # Create test data with some initial data
    test_file_path = 'test_balances.txt'
    with open(test_file_path, 'w') as f:
        f.write('001|||9264945|||Cheque|||250\n')
        f.write('002|||9676422|||Saving|||100\n')

    # Update the balance for 001 account id number
    update_balance_file(test_file_path, '9264945', "500")

    # Check that the file was updated correctly
    with open(test_file_path, 'r') as f:
        lines = f.readlines()
        assert lines[0] == '001|||9264945|||Cheque|||500\n'
        assert lines[1] == '002|||9676422|||Saving|||100\n'

    # Clean up the test file
    os.remove(test_file_path)




def test_print_account_summary(capfd):
    # Create test data for the test
    account_types_and_numbers = [("Cheque", "9264945"), ("Savings", "9676422")]
    accounts = [OpeningAccountData(1, "9264945", "Cheque", 1000), OpeningAccountData(2, "9676422", "Savings", 5000)]

    # Call function with test data
    print_account_summary(account_types_and_numbers, accounts)

    # Capture output
    captured = capfd.readouterr()   # This is a fixture from the pytest used to capture the output strean of print_account_summary
    output_lines = captured.out.strip().split('\n')  #strip() = used to remove white/empty space from the string to unsure the comparison to the output in not affected 
                                                     # split() = used to split the sting into lines, this is because the expected output is also displaying to split lines 

    # Check if output matches expected output
    assert len(output_lines) == 3     # == 3   = checks the numbers of lines captured is equal to 3 
    assert output_lines[0] == "Please find your account summary below:"
    assert output_lines[1] == "1. Account Type:Cheque   Account Number:9264945   Account Balance:1000"
    assert output_lines[2] == "2. Account Type:Savings   Account Number:9676422   Account Balance:5000"




def test_get_account_types_and_numbers():
    # creates a list of objects, each ojct contains AccountOwnerID, AccountNumber, AccountType, OpeningBalance
    accounts = [
        OpeningAccountData(1, "111111", "Cheque", 500),
        OpeningAccountData(2, "654321", "Savings", 1000),
        OpeningAccountData(3, "789012", "Cheque", 200),
        OpeningAccountData(1, "444444", "Savings", 1500),
    ]
    account_owner_id = 1.  # the value '1' is used as the input for the account ID number 
    expected_output = [("Cheque", "111111"), ("Savings", "444444")] # expected output for the values of accout_id_id = 1 
    assert get_account_types_and_numbers(accounts, account_owner_id) == expected_output # check that accounts, account_owner_id is equal to to the expected output 



