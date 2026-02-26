import socket


def port_is_up(host, port) -> bool:
    """
    test if a host is up

    https://github.com/lovelysystems/lovely.testlayers/blob/master/src/lovely/testlayers/util.py
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ex = s.connect_ex((host, port))
    if ex == 0:
        s.close()
        return True
    return False
