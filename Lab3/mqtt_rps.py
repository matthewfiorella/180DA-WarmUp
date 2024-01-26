import paho.mqtt.client as mqtt
import numpy as np

game_state = {"me": None, "nick": None}

# If p1 wins returns 1, loss returns -1, tie returns 0
def determine_winner(p1, p2):
    if p1 == p2:
        return 0
    elif p1 == "r":
        if p2 == "p":
            return -1
        elif p2 == "s":
            return 1
    elif p1 == "p":
        if p2 == "s":
            return -1
        elif p2 == "r":
            return 1
    elif p1 == "s":
        if p2 == "r":
            return -1
        elif p2 == "p":
            return 1
        
# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/rps/nn")

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')
        
# The default message callback.
# (won’t be used if only publishing, but can still exist)
def on_message(client, userdata, message):
    opponent_choice = str(message.payload.decode())
    game_state["nick"] = opponent_choice
    
# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')
# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()
# 4. use subscribe() to subscribe to a topic and receive messages.
# 5. use publish() to publish messages to the broker.
# payload must be a string, bytearray, int, float or None.
user_rps = input("Choose Rock, Paper, or Scissors (r/p/s): ")
while user_rps != "r" and user_rps != "p" and user_rps != "s":
    user_rps = input("Please only input (r/p/s): ")

game_state["me"] = user_rps
client.publish("ece180d/rps/mf", user_rps, qos=1)
while True:
    if game_state["me"] and game_state["nick"]:
        print("your opponent played: " + game_state["nick"])
        winner = determine_winner(game_state["me"], game_state["nick"])
        if winner == 1:
            print("you won!")
        elif winner == 0:
            print("tie!")
        elif winner == -1:
            print("you lost!")
        game_state = {"me": None, "nick": None}
        user_rps = input("Choose Rock, Paper, or Scissors (r/p/s): ")
        while user_rps != "r" and user_rps != "p" and user_rps != "s":
            user_rps = input("Please only input (r/p/s): ")
        game_state["me"] = user_rps
        client.publish("ece180d/rps/mf", user_rps, qos=1)
# 6. use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()