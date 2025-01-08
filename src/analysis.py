import pyshark
import socket
import csv





domainCache = {}
def getDomainFromIp(ip):
    if ip in domainCache:
        return domainCache[ip]
    
    try:
        hostByName = socket.gethostbyaddr(ip)
        domain = hostByName[0]
    except socket.herror:
        domain = ip

    domainCache[ip] = domain
    return domain





class HttpRequests:
    def __init__(self):
        self.http1 = 0
        self.http2 = 0
        self.http3 = 0 

def analyzeFile(filePath):
    
    def getOrSet(requests, domain):
        if requests.get(domain) == None:
            requests[domain] = HttpRequests()
        return requests[domain]

    httpRequestsForDomain = {}

    capture = pyshark.FileCapture(filePath, tshark_path="C:/utils/Wireshark/tshark.exe", display_filter="http or quic or tcp.port == 443")

    for packet in capture:
        domain = None

        try:
            if 'http' in packet:
                if hasattr(packet.http, "host"):
                    domain = packet.http.host
                elif hasattr(packet, "ip"):
                    domain = getDomainFromIp(packet.ip.dst)

                getOrSet(httpRequestsForDomain, domain).http += 1                

            elif 'quic' in packet:
                if hasattr(packet, "ip"):
                    domain = getDomainFromIp(packet.ip.dst)

                getOrSet(httpRequestsForDomain, domain).http3 += 1                

            elif 'tcp' in packet and packet.tcp.dstport == "443":
                if hasattr(packet, "ip"):
                    domain = getDomainFromIp(packet.ip.dst)

                getOrSet(httpRequestsForDomain, domain).http2 += 1

        except AttributeError as e:
            print("Ignored packet")

    capture.close()        

    return httpRequestsForDomain


def main():
    inputFile = "C:/source/http-traffic-inspector/data/input.pcapng"
    outputFile = "C:/source/http-traffic-inspector/data/results.csv"

    results = analyzeFile(inputFile)

    for result in results:
        print(result)





if __name__ == "__main__":
    main()