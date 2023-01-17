import socket
import threading
import sys

#La fonction receive est définie pour attendre les données entrantes du serveur.
# Cette fonction prend en paramètres un objet socket et un signal booléen signal.
# La fonction utilise une boucle while pour continuer à attendre les données entrantes tant que signal est True.
# Si des données sont reçues, elles sont imprimées dans la console. Si une erreur est levée,
# cela signifie que la connexion avec le serveur a été interrompue, et la boucle s'arrête.
def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break

#Le code suivant demande à l'utilisateur de fournir l'hôte et le numéro de port
# du serveur avec lequel établir la connexion. Ces informations sont saisies en tant que chaîne
# de caractères et le numéro de port est converti en entier.
host = input("Host: ")
port = int(input("Port: "))

#Ensuite, une tentative de connexion au serveur est effectuée en utilisant l'objet socket créé précédemment.
# Si la connexion échoue, un message d'erreur est affiché et le programme s'arrête.
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)

#Si la connexion réussie, un nouveau thread est créé pour exécuter la fonction receive en arrière-plan.
# Cela permet à l'utilisateur de continuer à envoyer des données au serveur tout en étant informé
# des données entrantes du serveur en temps réel
receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()


while True:
    message = input()
    sock.sendall(str.encode(message))
