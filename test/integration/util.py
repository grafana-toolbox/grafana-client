import socket


def port_is_up(host, port) -> bool:
    """
    test if a host is up

    https://github.com/lovelysystems/lovely.testlayers/blob/master/src/lovely/testlayers/util.py
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        ex = s.connect_ex((host, port))
        return ex == 0
