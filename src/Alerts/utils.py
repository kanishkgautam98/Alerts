import socket, dateparser

"""https://medium.com/better-programming/how-to-check-the-users-internet-connection-in-python-224e32d870c8"""
def checkInternetConnectivity(host = "8.8.8.8", port = 53, timeout = 3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as err:
        print(err)
        return False

def parseDateTime(date):
	return dateparser.parse(date)

