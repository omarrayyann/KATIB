import Data

current_user = ''
signed_in = False


def log_in(username, password):
    # Verifying
    for i in range(len(Data.sign_in_detals)):
        if username == Data.sign_in_detals[i].username and password == Data.sign_in_detals[i].password:
            #Success
            global current_user, signed_in
            current_user = Data.sign_in_detals[i]
            signed_in = True
            return True
    return False

def log_out():
    global current_user, signed_in
    current_user = ''
    signed_in = False