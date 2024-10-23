import pdfplumber
import csv

# date, account, amount, notes
accounts = {"High School Revenue" : ["richmond communi-payroll", "payroll"],
            "Sys Admin Revenue" : "earlham college-payroll",
            "Tutor Revenue" : ["lobby deposit d", "natco credit union"],
            "Other Revenue" : ["deposit venmo", "tax ref", "payments^", "natco cu"],
            "Car Expense" : ["knuckle busters", "autozone"],
            "McDonald's Expense" : ["mcdonald's"],
            "Restaurant Expense" : ["dairy queen", "doordash", "chipotle", "thai thara", "parlor doughnuts", "gulzars", " kfc ", "wendy's", "burger king", "domino's"],
            "Snack Expense" : ["milkhouse", "roscoe's", "metz", "fifth st. coffee", "the milk house"],
            "Guitar Expense" : ["sweetwater", "stringjoy"],
            "Lego Expense" : ["bricklink", "bricklink.co", "brick", "paypal"],
            "Game Expense" : ["playstation", "microsoft", "steam", "apple"],
            "Subscription Expense" : ["cricket wireless", "westside storage", "spotify", "amazon prime", "songsterr", "disney"],
            "Gas Expense" : ["speedway", "marathon", "bp", "holiday", "citgo", "trego travel center"],
            "Grocery Expense" : ["wal-mart", "dollar general", "johnsons", "menards", "mnrd-richmond"],
            "Entertainment Expense" : ["online amc", "dance alloy"],
            "School Expense" : ["college transcript", "tms*earlham", "tms*eac"],
            "Heatlh Expense" : ["whitewater valley dental"],
            "Other Expense" : ["venmo visa direct", "mktp", "ebay o", "metapay", "great clips", "goodwill", "venmo*", "hellomerch.com", "amazon.com*", "kohls"]}

def retrieve_pages(file):
    pages = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            page_text = text
            pages.append(page_text)
    return pages


def page_one(pages):
    split = pages[0].split("\n")

    start_index = 0
    for item in split:
        if "CHECKING ACCOUNT" in item or "KASASA CASH BACK W SAVER" in item:
            start_index = split.index(item)
    del split[0:start_index + 1]

    transactions = []

    for item in split:
        if "Home Banking Transfer Deposit" in item:
            continue
        elif "Home Banking Transfer Withdraw" in item:
            continue
        elif "ATM TRANSFER DEPOSIT" in item:
            continue
        elif "eBay Inc" in item  or "ACCTVERIFY" in item:
            continue
        elif "LOBBY DEPOSIT D" in item:
            transactions.append(item)
            transactions.append("NATCO CREDIT UNION")
        else:
            transactions.append(item)

    transaction_pairs = []

    for index in range(0, len(transactions), 2):
        if index + 1 < len(transactions):
            transaction_pairs.append([transactions[index], transactions[index + 1]])
        else:
            transaction_pairs.append([transactions[index]])

    final_trans_list = []
    for lst in transaction_pairs:
        temp_lst = []
        lst[0] = (lst[0].split(" "))
        date = lst[0][0]
        month, day = date.split("/")
        new_date = f"{int(month)}/{int(day)}"
        amount = lst[0][-2].replace("-", "")
        temp_lst.append(new_date)
        temp_lst.append(amount)
        temp_lst.append(lst[1].lower())
        final_trans_list.append(temp_lst)

    return final_trans_list

def middle_pages(pages):
    combined = []
    for index in range(1, len(pages) - 1):
        page = pages[index]
        split = page.split("\n")

        start_index = 0
        for item in split:
            if "---- ----" in item:
                start_index = split.index(item)
                break
        del split[0:start_index + 1]

        transactions = []

        for item in split:
            if "Home Banking Transfer Deposit" in item:
                continue
            elif "Home Banking Transfer Withdraw" in item:
                continue
            elif "ATM TRANSFER DEPOSIT" in item:
                continue
            else:
                transactions.append(item)

        transaction_pairs = []

    for index in range(0, len(transactions), 2):
        if index + 1 < len(transactions):
            transaction_pairs.append([transactions[index], transactions[index + 1]])
        else:
            transaction_pairs.append([transactions[index]])

    final_trans_list = []
    for lst in transaction_pairs:
        temp_lst = []
        lst[0] = (lst[0].split(" "))
        date = lst[0][0]
        month, day = date.split("/")
        new_date = f"{int(month)}/{int(day)}"
        amount = lst[0][-2].replace("-", "")
        temp_lst.append(new_date)
        temp_lst.append(amount)
        temp_lst.append(lst[1].lower())
        final_trans_list.append(temp_lst)
    combined.extend(final_trans_list)

    return combined
    
def page_end(pages):
    split = pages[-1].split("\n")

    start_index = 0
    for item in split:
        if "---- ----" in item:
            start_index = split.index(item)
            break
    del split[0:start_index + 1]

    end_index = 0
    for item in split:
        if "NEW BALANCE" in item:
            end_index = split.index(item)
            break
    del split[end_index::]

    transactions = []

    for item in split:
        if "Home Banking Transfer Deposit" in item:
            continue
        elif "Home Banking Transfer Withdraw" in item:
            continue
        elif "ATM TRANSFER DEPOSIT" in item:
            continue
        elif "LOBBY DEPOSIT D" in item:
            transactions.append(item)
            transactions.append("NATCO CREDIT UNION")
        else:
            transactions.append(item)

    transaction_pairs = []

    for index in range(0, len(transactions), 2):
        if index + 1 < len(transactions):
            transaction_pairs.append([transactions[index], transactions[index + 1]])
        else:
            transaction_pairs.append([transactions[index]])

    final_trans_list = []
    for lst in transaction_pairs:
        temp_lst = []
        lst[0] = (lst[0].split(" "))
        date = lst[0][0]
        month, day = date.split("/")
        new_date = f"{int(month)}/{int(day)}"
        amount = lst[0][-2].replace("-", "")
        temp_lst.append(new_date)
        temp_lst.append(amount)
        temp_lst.append(lst[1].lower())
        final_trans_list.append(temp_lst)
    

    return final_trans_list

def write_to_csv(transactions, filename='transactions.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Amount', 'Account', 'Text'])  # Write the header
        writer.writerows(transactions)  # Write the transactions


if __name__ == "__main__":

    files = ["Jan2024.pdf", "Feb2024.pdf", "Mar2024.pdf", "Apr2024.pdf", "May2024.pdf", "Jun2024.pdf", "Jul2024.pdf", "Aug2024.pdf", "Sep2024.pdf"]

    transactions = []

    for file in files:
        pages = retrieve_pages(file)
        one = page_one(pages)
        middle = middle_pages(pages)
        end = page_end(pages)
        transactions.extend(one)
        transactions.extend(middle)
        transactions.extend(end)

    counter = 0
    for i, item in enumerate(transactions):
        text = item[2]
        amount = float(item[1])
        matched = False  
        # Ensure there's a placeholder for item[3]
        if len(item) < 4:
            item.append("")
        if "Snack Expense" in text:
            continue
        for account, keywords in accounts.items():
            if isinstance(keywords, str):
                keywords = [keywords]
            # check if keyword appears in text
            if any(all(word in text.lower() for word in keyword.split()) for keyword in keywords):
                if account == "Gas Expense":
                    if amount < 20:
                        item[2] = "Snack Expense"
                        item[3] = text
                    elif 20 <= amount < 30:
                        item[2] = "Gas Expense"
                        item[3] = text
                        snack_amount = amount - 20
                        if snack_amount > 0:
                            snack_item = [item[0], f"{snack_amount:.2f}", "Snack Expense", text]
                            transactions.insert(i + 1, snack_item)
                    elif amount >= 30:
                        item[2] = "Gas Expense"
                        item[3] = text

                        snack_amount = amount - 30
                        if snack_amount > 0:
                            snack_item = [item[0], f"{snack_amount:.2f}", "Snack Expense", text]
                            transactions.insert(i + 1, snack_item)      
                    matched = True
                    break
                else:
                    item[2] = account
                    item[3] = text
                    matched = True
                    counter += 1
                    break 
        if not matched: 
            item[2] = "[]"
            item[3] = text
            counter += 1
    write_to_csv(transactions)
    for item in transactions:
        print(item)
