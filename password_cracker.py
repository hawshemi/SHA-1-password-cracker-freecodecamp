import hashlib


def crack_sha1_hash(hash, use_salts=False):
    salts = []
    if use_salts:
        # Get all known salts from file if use salts is true
        with open("known-salts.txt") as salt_file:
            salts = salt_file.read()
            salts = salts.split("\n")

    with open("top-10000-passwords.txt", mode="r") as password_file:
        # get all passwords to check
        passwords = password_file.readlines()
        passwords = tuple(p.strip() for p in passwords)
        for password in passwords:
            if not use_salts:
                # password check without salts
                p_crack = hashlib.sha1()
                p_crack.update(password.encode("utf-8"))
                cracked_password_hash = p_crack.hexdigest()
                if cracked_password_hash == hash:
                    return password
            else:
                # password check with salts
                for salt in salts:
                    append_pass = salt + password
                    prepend_pass = password + salt
                    check_append = False
                    for _ in range(2):
                        if check_append:
                            check_append = False
                        else:
                            check_append = True
                        current_pass = append_pass if check_append else prepend_pass
                        p_crack = hashlib.sha1()
                        p_crack.update(current_pass.encode("utf-8"))
                        cracked_password_hash = p_crack.hexdigest()
                        if cracked_password_hash == hash:
                            return password

    return "PASSWORD NOT IN DATABASE"
