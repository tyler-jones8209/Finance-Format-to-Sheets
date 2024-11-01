import pdfplumber
import csv

# date, account, amount, notes
accounts = {"Work Revenue" : ["richmond communi-payroll", "payroll", "earlham college-payroll"],
            "Other Revenue" : ["deposit venmo", "tax ref", "payments^", "natco cu", "venmo*"],
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
            "Other Expense" : ["venmo visa direct", "mktp", "ebay o", "metapay", "great clips", "goodwill", "hellomerch.com", "amazon.com*", "kohls"]}

def retrieve_pages(file):
    file_path = f"Finances/{file}" # fixing file path after moving to subdirectory 
    pages = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return pages


def page_one(pages):
    split = pages[0].split("\n")

    start_index = 0
    for item in split:
        if "CHECKING ACCOUNT" in item or "KASASA CASH BACK W SAVER" in item:
            start_index = split.index(item)
    del split[0:start_index + 1]


    # replace if/else statements with list
    skip_terms = ["Home Banking Transfer Deposit", "Home Banking Transfer Withdraw", "ATM TRANSFER DEPOSIT", "eBay Inc", "ACCTVERIFY"]

    transactions = []

    for item in split:
        if any(term in item for term in skip_terms):
            continue
        elif "LOBBY DEPOSIT D" in item:
            transactions.extend([item, "NATCO CREDIT UNION DEPOSIT"])
        else:
            transactions.append(item)

    transaction_pairs = []

    for index in range(0, len(transactions), 2):
        if index + 1 < len(transactions):
            transaction_pairs.append([transactions[index], transactions[index + 1]])
        else:
            transaction_pairs.append([transactions[index]])

    # removed temp_list
    final_trans_list = []
    for lst in transaction_pairs:
        lst[0] = (lst[0].split(" "))
        date = lst[0][0]
        month, day = date.split("/")
        new_date = f"{int(month)}/{int(day)}"
        amount = lst[0][-2].replace("-", "")
        final_trans_list.append([new_date, lst[1].lower(), amount])

    return final_trans_list

def middle_pages(pages):
    combined = []
    for index in range(1, len(pages) - 1):  # Start at page 1, end at len(pages) - 1
        page = pages[index]
        split = page.split("\n")

        start_index = next((i for i, item in enumerate(split) if "---- ----" in item), None)
        if start_index is not None:
            split = split[start_index + 1:]  # Adjust based on found start index


        skip_terms = ["Home Banking Transfer Deposit", "Home Banking Transfer Withdraw", "ATM TRANSFER DEPOSIT", "eBay Inc", "ACCTVERIFY"]

        transactions = []

        for item in split:
            # Check for skip terms
            if any(term in item for term in skip_terms):
                continue
            elif "LOBBY DEPOSIT D" in item:
                transactions.append(item)
                transactions.append("NATCO CREDIT UNION DEPOSIT")  # Handle special case
            else:
                transactions.append(item)

        transaction_pairs = []

        for index in range(0, len(transactions), 2):
            if index + 1 < len(transactions):
                transaction_pairs.append([transactions[index], transactions[index + 1]])
            else:
                transaction_pairs.append([transactions[index]])

        for lst in transaction_pairs:
            lst[0] = (lst[0].split(" "))
            date = lst[0][0]
            month, day = date.split("/")
            new_date = f"{int(month)}/{int(day)}"
            amount = lst[0][-2].replace("-", "")
            combined.append([new_date, lst[1].lower(), amount])

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

    skip_terms = ["Home Banking Transfer Deposit", "Home Banking Transfer Withdraw", "ATM TRANSFER DEPOSIT"]
    transactions = []

    for item in split:
        if any(term in item for term in skip_terms):
            continue
        elif "LOBBY DEPOSIT D" in item:
            transactions.extend([item, "NATCO CREDIT UNION DEPOSIT"])
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
        lst[0] = (lst[0].split(" "))
        date = lst[0][0]
        month, day = date.split("/")
        new_date = f"{int(month)}/{int(day)}"
        amount = lst[0][-2].replace("-", "")
        final_trans_list.append([new_date, lst[1].lower(), amount])
    
    return final_trans_list

def write_to_csv(transactions, filename='Finances/transactions.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(transactions)

if __name__ == "__main__":

    files = ["Jan2024.pdf", "Feb2024.pdf", "Mar2024.pdf", "Apr2024.pdf", "May2024.pdf", "Jun2024.pdf", "Jul2024.pdf", "Aug2024.pdf", "Sep2024.pdf", "Oct2024.pdf"]

    transactions = []

    for file in files:
        pages = retrieve_pages(file)
        transactions.extend(page_one(pages))
        transactions.extend(middle_pages(pages))
        transactions.extend(page_end(pages))


    # some transactions are a combination of gas and snacks. Since i only buy gas in $20 or $30 amounts, i subtract that from the amount and use the rest of the amount as a snack transacttion.
    for i, item in enumerate(transactions):
        text = item[1]  # account is now in item[1] after reordering
        amount = float(item[2])  # amount is now in item[2] after reordering
        matched = False  

        if len(item) < 4:
            item.append("")
        if "Snack Expense" in text:
            continue
        for account, keywords in accounts.items():
            if isinstance(keywords, str):
                keywords = [keywords]
            if any(all(word in text.lower() for word in keyword.split()) for keyword in keywords):
                if account == "Gas Expense":
                    if amount < 20:
                        item[1] = "Snack Expense"
                        item[3] = text
                    elif 20 <= amount < 30:
                        item[1] = "Gas Expense"
                        item[3] = text
                        snack_amount = amount - 20
                        if snack_amount > 0:
                            snack_item = [item[0], "Snack Expense", f"{snack_amount:.2f}", text]
                            transactions.insert(i + 1, snack_item)
                    elif amount >= 30:
                        item[1] = "Gas Expense"
                        item[3] = text
                        snack_amount = amount - 30
                        if snack_amount > 0:
                            snack_item = [item[0], "Snack Expense", f"{snack_amount:.2f}", text]
                            transactions.insert(i + 1, snack_item)      
                    matched = True
                    break
                else:
                    item[1] = account
                    item[3] = text
                    matched = True
                    break 
        if not matched: 
            item[1] = ""
            item[3] = text
    
    write_to_csv(transactions)

    print("Succesfully Wrote Information to CSV File.")
