def FATAL(msg):
    print("\033[1;31m[-]", msg, "\033[0m")
    return


def OK(msg):
    print("\033[1;32m[+]", msg, "\033[0m")
    return


def WARN(msg):
    print("\033[1;33m[!]", msg, "\033[0m")
    return


def DEBUG(msg):
    print(msg)
    return
