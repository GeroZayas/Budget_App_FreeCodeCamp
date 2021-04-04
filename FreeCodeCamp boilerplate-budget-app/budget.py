class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = []
        self.funds = 0

    def deposit(self, amount, description=''):
        deposit = {"amount": amount, "description": description}
        self.ledger.append(deposit)
        self.funds += amount

    def withdraw(self, amount, description=''):
        if self.funds >= amount:
            self.funds -= amount
            withdraw = {"amount": (amount * -1), "description": description}
            self.ledger.append(withdraw)
            return True
        else:
            return False

    def get_balance(self):
        return self.funds

    def transfer(self, amount, destination):
        if self.funds >= amount:
            # I had to format the destinoation like this >> .strip('*').replace('*', '').replace('\nTotal: 0',
            # '') << because, for some reason, it didn't just worked with strip() and all the right side after the
            # name was ->  *******\nTotal:0 <- I don't know why, but I guess it takes it from the __str__() at the
            # end of the class.
            format_destination = str(destination).strip('*').replace('*', '').replace('\nTotal: 0', '')
            description = f"Transfer to {format_destination}"
            self.withdraw(amount, description)
            deposit_description = f"Transfer from {self.category.strip('*')}"
            destination.deposit(amount, deposit_description)
            self.check_funds(amount)
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self.funds:
            return False
        else:
            return True

    # What we use to Print objects of a class in Python -> def __str__(self):
    def __str__(self):
        title = self.category
        # this below is to know how many * to print around the title -> ****Food****
        title_length = len(self.category)
        asterisks = '*' * int((30 - title_length) / 2)
        title_line = asterisks + title + asterisks
        category_total = f"Total: {self.funds}"
        # printing the object
        # Here a for loop is used to get hold of every description and amount in the legder
        # NOTE how to make it print the numbers with 2 decimal places -> "{:.2f}".format
        # NOTE how the amount is right aligned (rjust) with a limit of 7 char // description is left aligned and it
        # has a limit of 23 char -> [:23]
        content = ''
        for i in self.ledger:
            amount = str("{:.2f}".format(float(i['amount']))).rjust(7)
            description = i['description'].ljust(23)[:23]
            content += f"{description}{amount}\n"
        object_printed = f"{title_line}\n{content}{category_total}"
        return object_printed


def create_spend_chart(categories=[]):
    cat_names = []
    withdraws = []
    withdraw_percentage = []
    for category in categories:
        cat_names.append(category.category)
        # Store withdrawn amount as 0 for each category
        withdrawn_amount = 0
        # if the movemente is negative, (withdraw), I use - in  front of it to make it positive and add it
        for movement in category.ledger:
            if movement["amount"] < 0:
                withdrawn_amount -= movement["amount"]
        # Put each withdraw in the list of withdraws
        withdraws.append(withdrawn_amount)
    for num in range(len(withdraws)):
        withdraw_percentage.append(withdraws[num] / sum(withdraws) * 100)

    # elements of bar chart
    title = "Percentage spent by category"
    y_axis = '|'
    bar = ' o '
    x_axis = '---'
    x_axis_space = '    '
    # ---------------- BAR CHART Construction----------------
    new_line = '\n'
    longest_cat_name = max(cat_names, key=len)
    blank_space = ' '
    bar_char = ''
    cat_items = len(cat_names)

    for n in range(100, -1, -10):
        bar_char += str(n).rjust(3) + y_axis
        for num in withdraw_percentage:
            if num >= n:
                bar_char += bar
            else:
                bar_char += blank_space * 3

        bar_char += ' ' + new_line

    # ---------------- X axis ----------------
    x_axis = x_axis_space + x_axis * cat_items + '-'

    # ---------------- Vertical names below bar chart ----------------
    vertical_names = ''
    counter_letter = 0
    letters_in_name = 0

    while letters_in_name <= len(longest_cat_name):
        vertical_names += '    '
        for n in range(len(cat_names)):
            try:
                for letter in cat_names[n][counter_letter]:
                    vertical_names += ' ' + letter + ' '
            except IndexError:
                vertical_names += ' ' + ' ' + ' '

        vertical_names += ' ' + new_line

        counter_letter += 1
        letters_in_name += 1

    bar_char = title + new_line + bar_char + x_axis + new_line + vertical_names.rstrip() + '  '

    return bar_char
