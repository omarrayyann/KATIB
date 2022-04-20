import User
import Data

current_user = User.User("non")
current_status = "logged_out"
signed_in = False


def log_in(username,password):
    # Verifying
    if username==Data.sign_in_detals[0] and password==Data.sign_in_detals[1]:
        #Success
        return True
    else:
        return False
