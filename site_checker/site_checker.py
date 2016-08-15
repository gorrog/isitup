import httplib

conn = httplib.HTTPSConnection("www.sarsefiling.co.za")
conn.request("GET", "/")
r1 = conn.getresponse()
print r1.status, r1.reason






# def check_server()