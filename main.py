from format_files import format_files_to_list, group_cat

# valide login

def login_sys(account_ls: list):

    print("Welcome to Banking System")

    login_status = False
    login_attempt = 3
    while login_status == False:
        user_id = input("Enter your User ID: ")
        password = input("Enter your Password: ")
        line_check = 0
        while line_check < len(account_ls):
            check_user_id = account_ls[line_check][0]
            check_password = account_ls[line_check][2]
            if user_id == check_user_id and password == check_password:
                username = account_ls[line_check][1]
                login_status = True
                break
            else: 
                line_check += 1
        if login_status != True:
            print("Incorrect User ID or password. Please try again.")
            login_attempt -= 1
            if login_attempt == 0:
                print("You have reached the maximum attempt allowed. Goodbye!")
                quit()
            else: 
                print(f"You have {login_attempt} login attempts remaining")

    return (login_status, user_id, username)

# Display Menu

def banking_sys(trans_ls: list, login_status: bool, curr_account: str, name: str):

    menu_start = '''Select one of the options below:
    1. Make a payment
    2. Display all transaction
    3. Display Income and Expenses Summary
    4. Logout
    '''

    print(f"Welcome {name}! User ID: {curr_account}")

    while login_status == True:
        sorted_ls = extract_record(trans_ls, curr_account)
        print(menu_start)
        try:
            select_no = int(input("Enter your option: "))
        except ValueError:
            print("The value must type an integer")
            continue
        if select_no == 2:
            print(f"The following is the transactions by {curr_account}.")
            print("| Transaction Date | Type | Category | Amount | Description |")
            for row in sorted_ls:
                print("| " + row[1] + " | " + row[2] + " | " + row[3] + " | " + row[4] + " | " + row[5] + " | ")
            print()
        if select_no == 3:
            group_summary(sorted_ls)
            continue
        if select_no == 4:
            print("You have successfully logout. GoodBye!")
            quit()

def extract_record(trans_ls: list, curr_account: str):
    extract_records = []
    find_row = 1
    while find_row < len(trans_ls[1:]):
        if trans_ls[find_row][0] == curr_account:
            extract_records.append(trans_ls[find_row])
        find_row += 1
    # sort list desc
    sorted_ls = sorted(extract_records, key=lambda x: x[1], reverse=True)
    return sorted_ls

  
# transaction summaries by transaction type / category

def group_summary(trans_ls: list):

    group_summary = []

    for trans in trans_ls:
        type_name = trans[2]
        price = float(trans[4])
        for total in group_summary:
            if total[0] == type_name:
                total[1] += price
                break
        else:
            group_summary.append([type_name, round(price, 2)])

    print("Summary by Transaction Type: ", group_summary, "\n")


def main():
    account_ls = format_files_to_list("account_credentials.csv")
    transaction_ls = format_files_to_list("banking_transactions.csv")
    open_balance = format_files_to_list("opening_balances.csv")


    login_status, user_id, username = login_sys(account_ls)
    banking_sys(transaction_ls, login_status, user_id, username)
    

if __name__ == "__main__":
    main()