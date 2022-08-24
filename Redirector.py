import socket
import configparser
import concurrent.futures
from logger.logger import Logger

class RedirectServerTCP(Logger):
    def __init__(self, szSourceHost, szSourcePort):
        self.logger = Logger("Redirector")
        self.szSourceHost = szSourceHost
        self.szSourcePort = szSourcePort

    def client(self, szDestProtocol, szDestHost, szDestPort, bData):
        if szDestProtocol.upper() == "TCP":
            try:
                szMsg = f"{szDestProtocol} | {szDestHost} | {szDestPort} | {bData.decode()}"
                self.logger.info(szMsg)
                oSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                oSocket.connect((szDestHost, int(szDestPort)))
                oSocket.send(bData)
                oSocket.close()
            except Exception as e:
                self.logger.critical(e)
        elif szDestProtocol.upper() == "UDP":
            try:
                szMsg = f"{szDestProtocol} | {szDestHost} | {szDestPort} | {bData.decode()}"
                self.logger.info(szMsg)
                oSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                oSocket.sendto(bData, (szDestHost, int(szDestPort)))
                oSocket.close()
            except Exception as e:
                self.logger.critical(e)
        else:
            self.logger.error("Destination section protocol value in your config is error !!!")
            self.logger.error("protocol value just : TCP / UDP !!!")
    
    def process(self, oConnection):
        while True:
            bData = oConnection.recv(2**35)
            if len(bData) == 0:
                oConnection.close()
                break
            oConnection.close()
            return bData
    
    def start(self, mRedirect):
        oSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        oSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        oSocket.bind((self.szSourceHost, self.szSourcePort))
        oSocket.listen(5)
        self.logger.info(f"Server start at TCP {self.szSourceHost}:{self.szSourcePort}")
        while True:
            oConnection, szAddress = oSocket.accept()
            
            # test ok
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.process, oConnection)
                bData = future.result()

            # while True:
            #     bData = oConnection.recv(1024)
            #     if len(bData) == 0:
            #         oConnection.close()
            #         break

            #     for item in mRedirect:
            #         self.client(mRedirect[item][0], mRedirect[item][1], mRedirect[item][2], bData)

            for item in mRedirect:
                self.client(mRedirect[item][0], mRedirect[item][1], mRedirect[item][2], bData)


# TODO: test not ok
class RedirectServerUDP(Logger):
    def __init__(self, szSourceHost, szSourcePort):
        self.logger = Logger("Redirector")
        self.szSourceHost = szSourceHost
        self.szSourcePort = szSourcePort

    def client(self, szDestProtocol, szDestHost, szDestPort, bData):
        if szDestProtocol.upper() == "TCP":
            try:
                szMsg = f"{szDestProtocol} | {szDestHost} | {szDestPort} | {bData.decode()}"
                self.logger.info(szMsg)
                oSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                oSocket.connect((szDestHost, int(szDestPort)))
                oSocket.send(bData)
                oSocket.close()
            except Exception as e:
                self.logger.critical(e)
        elif szDestProtocol.upper() == "UDP":
            try:
                szMsg = f"{szDestProtocol} | {szDestHost} | {szDestPort} | {bData.decode()}"
                self.logger.info(szMsg)
                oSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                oSocket.sendto(bData, (szDestHost, int(szDestPort)))
                oSocket.close()
            except Exception as e:
                self.logger.critical(e)
        else:
            self.logger.error("Destination section protocol value in your config is error !!!")
            self.logger.error("protocol value just : TCP / UDP !!!")
    
    def process(self, oSocket):
        while True:
            bData, szAddress = oSocket.recvfrom(2**35)
            if len(bData) == 0:
                oSocket.close()
                break
            oSocket.close()
            return bData
    
    def start(self, mRedirect):
        oSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # oSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        oSocket.bind((self.szSourceHost, self.szSourcePort))
        self.logger.info(f"Server start at UDP {self.szSourceHost}:{self.szSourcePort}")

        # test ok
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.process, oSocket)
            bData = future.result()

        for item in mRedirect:
            self.client(mRedirect[item][0], mRedirect[item][1], mRedirect[item][2], bData)


def getConfig(szConfigName):
    config = configparser.ConfigParser()
    config.read(szConfigName)

    mRedirectMap = {}

    for item in config.sections():
        lstDetail = []
        lstDetail.append(config[item]["PROTOCOL"])
        lstDetail.append(config[item]["HOST"])
        lstDetail.append(config[item]["PORT"])
        mRedirectMap[item] = lstDetail
    return mRedirectMap


def main():
    logger = Logger("Redirector")
    mRedirect = getConfig("Redirector.conf")
    mSource = mRedirect["LOCAL"]
    szSourceProtocol = mSource[0]
    szSourceHost = mSource[1]
    szSourcePort = int(mSource[2])
    del mRedirect["LOCAL"]
    
    if szSourceProtocol.upper() == "TCP":
        server = RedirectServerTCP(szSourceHost, szSourcePort)
        server.start(mRedirect)
    elif szSourceProtocol.upper() == "UDP":
        server = RedirectServerUDP(szSourceHost, szSourcePort)
        server.start(mRedirect)
    else:
        logger.error("LOCAL section protocol value in your config is error !!!")
        logger.error("protocol value just : TCP / UDP !!!")

if __name__ == '__main__':
    main()