def calculate_risk(amount):

    if amount <= 50:
        return 10

    elif amount <= 200:
        return 50

    else:
        return 90