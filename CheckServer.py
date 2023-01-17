import socket
import ssl
import time
from datetime import datetime
import pickle

from gmail import email_alert

#La classe Server a trois principales méthodes: _init_, check_connection et create_history.

class Server():

    #La méthode _init_ est le constructeur de la classe Server. Elle prend trois arguments: name,
    # port et connection. Ces derniers représentent le nom du serveur,
    # le port sur lequel le serveur écoute et le type de connexion (soit "plain" ou "ssl").
    def __init__(self, name, port, connection):
        self.name = name
        self.port = port
        self.connection = connection.lower()
        self.history = []
        self.alert = False

    #La méthode check_connection essaie de se connecter au serveur en utilisant le type de connexion
    # spécifié (soit un socket simple ou un socket enveloppé par SSL). Si la tentative de connexion réussit,
    # elle enregistre un message indiquant que le serveur est en fonctionnement.
    # Si la tentative de connexion échoue,
    # elle enregistre un message d'erreur et envoie un email d'alerte.
    def check_connection(self):
        msg = ""
        success = False
        now = datetime.now()

        try:
            if self.connection == "plain":
                socket.create_connection((self.name, self.port), timeout=10)
                msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                success = True
                self.alert = False
            elif self.connection == "ssl":
                ssl.wrap_socket(socket.create_connection((self.name, self.port), timeout=10))
                msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                success = True
                self.alert = False

        except socket.timeout:
            msg = f"server: {self.name} timeout. On port {self.port}"
        except (ConnectionRefusedError, ConnectionResetError) as e:
            msg = f"server: {self.name} {e}"
        except Exception as e:
            msg = f"service inconnu: {e}"

        
        if success == False and self.alert == False:
            # Send Alert
            self.alert = True
            print("alert alert")
            email_alert(self.name,f"{msg}\n{now}","derbaleamine@gmail.com")

        self.create_history(msg,success,now)

    #La méthode create_history enregistre le message et le statut de succès de la dernière
    #appel à check_connection dans une liste d'historique interne.
    #Si la liste d'historique devient plus longue que 100 éléments,
    #l'élément le plus ancien est supprimé de la liste.

    def create_history(self, msg, success, now):
        history_max = 100
        self.history.append((msg,success,now))

        while len(self.history) > history_max:
            self.history.pop(0)



    #Le bloc if _name_ == "_main_": en fin de code est exécuté lorsque le programme est exécuté.
    # Il essaie de charger une liste d'objets Server à partir d'un fichier appelé "servers.pickle".
    # Si cela échoue (par exemple, parce que le fichier n'existe pas), il crée une liste d'objets Server
    # en utilisant des valeurs par défaut. Ensuite, il entre dans une boucle infinie qui appelle répétitivement
    # la méthode check_connection pour chaque objet Server de la liste, et dort 5 secondes entre chaque itération.
    # Enfin, il enregistre la liste d'objets Server dans le fichier "servers.pickle".
if __name__ == "__main__":
    try:
        servers = pickle.load(open("servers.pickle", "rb"))
    except:
        servers = [ 
            Server("reddit.com", 80, "plain"),
            Server("localhost", 443 , "plain"), #service apache
            Server("facebook.com", 80, "plain")
        ]
    while True:
        for server in servers:
            server.check_connection()
            print(len(server.history))
            print(server.history[-1])
            time.sleep(5)

    pickle.dump(servers, open("servers.pickle", "wb"))