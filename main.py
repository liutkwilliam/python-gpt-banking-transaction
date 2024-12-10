from format_files import format_files_to_list, group_cat

red = '\033[91m'
green = '\033[32m'
end_colour = '\033[0m'
blue_underline = '\033[1;4;34m'

def heading_generator(title_text: str, color: str):
    hyphen = "-"
    title = color + hyphen * (5 + len(title_text) + 5) + "\n" + \
            hyphen * 4 + " " + title_text + " " + hyphen * 4 + "\n" + \
            hyphen * (5 + len(title_text) + 5) + end_colour
    return print(title)

# valide login

def login_sys(account_ls: list):

    heading_generator("Banking System", green)

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
                name = account_ls[line_check][1]
                login_status = True
                break
            else: 
                line_check += 1
        if login_status != True:
            print(f"{red}Error: Incorrect User ID or password.{end_colour}")
            login_attempt -= 1
            if login_attempt == 0:
                print(f"{red}Error: You have reached the maximum attempt allowed. Goodbye!{end_colour}")
                quit()
            else: 
                print(f"{red}You have {login_attempt} login attempts remaining{end_colour}")

    return (login_status, user_id, name)

# Display Menu

def banking_sys(login_status: bool, user_id: str, name: str, trans_ls: list):
    sorted_ls = extract_record(trans_ls, user_id)

    # heading_generator(f"Welcome {name}! User ID: {user_id}")

    print(f"--- {green}Welcome {name}! User ID: {user_id} ---{end_colour}")

    menu_start = f'''\n{blue_underline}Select one of the options below:{end_colour}
    0. Display Current Balance
    1. Make a payment
    2. Display all transaction
    3. Display Income and Expenses Summary
    4. Logout
    '''

    # open opening balance file
    open_bal = format_files_to_list("opening_balances.csv")

    # calculate summary first
    summary_calc = group_summary(sorted_ls)

    while login_status == True:
        print(menu_start)
        try:
            select_no = int(input("Enter your option: "))
        except ValueError:
            print("The value must type an integer")
            continue
        if select_no == 0:
            for find_id in open_bal:
                if find_id[0] == user_id:
                    value_bal = float(find_id[1])
                    break
            for each_cat in summary_calc:
                if each_cat[0] == "Deposit":
                    value_bal += float(each_cat[1])
                else:
                    value_bal -= float(each_cat[1])
            print(f"Your current balance is ${value_bal}")

        if select_no == 2:
            print(f"The following is the transactions by {user_id}.")
            print("| Transaction Date | Type | Category | Amount | Description |")
            for row in sorted_ls:
                print("| " + row[1] + " | " + row[2] + " | " + row[3] + " | " + row[4] + " | " + row[5] + " | ")
            print()
        if select_no == 3:
            print(f"{blue_underline}Summary by Transaction Type:{end_colour}")
            for each_cat in summary_calc:
                print(f"{each_cat[0]}: {each_cat[1]}")
        if select_no == 4:
            print(f"{green}You have successfully logout. GoodBye!{end_colour}")
            quit()

def extract_record(trans_ls: list, user_id: str):
    extract_records = []
    find_row = 1
    while find_row < len(trans_ls[1:]):
        if trans_ls[find_row][0] == user_id:
            extract_records.append(trans_ls[find_row])
        find_row += 1
    # sort list desc
    sorted_ls = sorted(extract_records, key=lambda x: x[1], reverse=True)
    return sorted_ls

  
# transaction summaries by transaction type / category

def group_summary(trans_ls: list):
    if not trans_ls:
        print("No transactions to summarize.")
        return

    summary = []

    for trans in trans_ls:
        try:
            type_name = trans[2]
            price = float(trans[4])  # Ensure price can be converted to float
        except (IndexError, ValueError):
            print(f"Invalid transaction entry: {trans}")
            continue  # Skip invalid rows

        for total in summary:
            if total[0] == type_name:
                total[1] += price  # Accumulate price
                total[1] = round(total[1], 2)  # Keep totals consistent
                break
        else:
            summary.append([type_name, round(price, 2)])  # New type, add to summary

    for total in summary:
        total[1] = f"{total[1]:.2f}"

    return summary

def main():
    account_cred = format_files_to_list("account_credentials.csv")
    bank_trans = format_files_to_list("banking_transactions.csv")

    login_status, user_id, name = login_sys(account_cred)
    banking_sys(login_status, user_id, name, bank_trans)  

if __name__ == "__main__":
    main()