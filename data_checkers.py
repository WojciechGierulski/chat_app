forbidden_names = ["Hitler"]


def name_checker(name, names_list=None):
    if names_list is None:
        names_list = []
    if name not in forbidden_names and ("|" not in name):
        if 20 >= len(name) >= 3:
            if name not in names_list:
                return "ok"
            else:
                return "That name is already taken"
        else:
            return "Name must be between 3 and 20 characters"
    else:
        return "That name is forbidden"


def password_checker(password):
    if (20 >= len(password) >= 1 or password == '') and " " not in password:
        return "ok"
    else:
        return "Password must be between 3 and 20 non-blank characters"


def capacity_checker(capacity):
    try:
        x = int(capacity)
        if x >= 2 and x <= 30:
            return "ok"
        else:
            return "Capacity must be an integer between 2 and 30"
    except ValueError:
        return "Capacity must be an integer between 2 and 30"
