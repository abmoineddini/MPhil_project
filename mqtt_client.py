# enable TLS client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

import time
import paho.mqtt.client as paho
from paho import mqtt
import passwords


def Sub_Spatial_Rec_Data_Collection(TestName):
    myGlobalMessagePayload = ''
    # setting callbacks for different events to see if it works, print the message etc.
    def on_connect(client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    # setting callback for getting logs
    def on_log(client, userdata, level, buf):
        print("log : " + buf)

    # print which topic was subscribed to
    def on_subscribe(client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    # print message, useful for checking if it was successful
    def on_message(client, userdata, msg):
        print("msg : " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        global myGlobalMessagePayload
        myGlobalMessagePayload = str(msg.payload)
        return msg.payload

    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    

    # enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    UserName, password = passwords.mqttClient()
    client.username_pw_set(UserName, password)
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    client.subscribe(topic=TestName, qos=0)

    client.on_connect = on_connect
    client.on_log = on_log
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    client.connect("9526343732ac44a4954317841c2548d1.s2.eu.hivemq.cloud", 8883)

    client.loop_start()
    time.sleep(7)
    client.loop_stop()
    client.disconnect

    return myGlobalMessagePayload



def Pub_Spatial_Rec_Data_Collection(TestName, Progress):
    def on_connect(client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    # with this callback you can see if your publish was successful
    def on_publish(client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    def on_log(client, userdata, level, buf):
        print("log : " + buf)

    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.on_log = on_log

    # enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # client.tls_insecure_set(True)
    # set username and password
    UserName, password = passwords.mqttClient()
    client.username_pw_set(UserName, password)
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    client.connect("9526343732ac44a4954317841c2548d1.s2.eu.hivemq.cloud", 8883)

    client.on_publish = on_publish

    client.loop_start()
    client.publish(topic=TestName, payload= Progress, qos=0)
    time.sleep(3)
    client.loop_stop()

    client.disconnect






