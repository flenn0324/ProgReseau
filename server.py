import socket
import threading

#Les variables connections et total_connections sont utilisées pour stocker les informations
# sur les connexions client. La variable connections est une liste qui contient des instances
# de la classe Client pour chaque client connecté, tandis que total_connections est un compteur
# qui enregistre le nombre total de clients connectés.
connections = []
total_connections = 0

#La classe Client est définie pour représenter chaque client connecté.
# Une nouvelle instance de cette classe est créée pour chaque nouveau client qui se connecte au serveur.
# Cette classe hérite de threading.Thread pour pouvoir être exécutée en tant que thread séparé.
#Chaque instance de la classe Client a les attributs suivants :
#socket : un objet socket associé au client, qui est utilisé pour envoyer et recevoir des données avec ce client.
#address : l'adresse IP et le numéro de port associés au client.
#id : un identifiant unique assigné à chaque client pour les différencier les uns des autres.
#name : le nom choisi par le client pour se présenter au serveur et aux autres clients.
#signal : un signal booléen qui indique si la connexion avec ce client est toujours active.

#La classe Client étend la classe threading.Thread pour pouvoir être exécutée en tant que thread séparé.
# Le constructeur de la classe prend en paramètres un objet socket,
# l'adresse IP et le numéro de port associés au client, un identifiant unique,
# un nom choisi par le client et un signal booléen indiquant si la connexion est active.
# Ces paramètres sont utilisés pour initialiser les attributs de l'instance.
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

    #La méthode _str_() est appelée lorsque l'on tente d'imprimer l'instance de la classe en tant que
    # chaîne de caractères. Elle retourne l'identifiant et l'adresse associés au client sous la forme
    # d'une chaîne de caractères.

    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    #La méthode run() est exécutée lorsque le thread associé à l'instance de la classe est lancé.
    # Elle utilise une boucle while pour continuer à attendre les données entrantes du client tant que
    # la connexion est active. Si une erreur se produit lors de
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)


def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1

def main():
    #Get host and port
    host = input("Host: ")
    port = int(input("Port: "))


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)


    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    
main()
