
import pickle
from CheckServer import Server

servers = pickle.load( open( "servers.pickle", "rb" ) )

print("Example to add server")

servername = input("enter server name")
port = int(input("Enter a port number as integer"))
connection = input("Enter a type plain/ssl")

new_server = Server(servername, port, connection)
servers.append(new_server)

pickle.dump(servers, open("servers.pickle", "wb" ))