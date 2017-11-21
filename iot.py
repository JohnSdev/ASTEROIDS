
#IOT Labb
import random
import pygame
import time
import sys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
#IOT Labb


class iot():
# String containing Hostname, Device Id & Device Key in the format
    def __init__(self):
     
        self.CONNECTION_STRING = "ENTER OWN KEY"
    # choose HTTP, AMQP or MQTT as transport protocol
        self.PROTOCOL = IoTHubTransportProvider.MQTT
        self.MESSAGE_TIMEOUT = 10000
        self.AVG_WIND_SPEED = 19
        self.SEND_CALLBACKS = 0
        self.MSG_TXT = "{\"IOTLabb1\": \"Asteroids\",\"Highscore\": %.2f}"   
        print ( "Simulating a device using the Azure IoT Hub Device SDK for Python" )
        print ( "    Protocol %s" % self.PROTOCOL )
        print ( "    Connection string=%s" % self.CONNECTION_STRING )

    def send_confirmation_callback(self, message, result, user_context):
        global SEND_CALLBACKS
        print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
        map_properties = message.properties()
        print ( "    message_id: %s" % message.message_id )
        print ( "    correlation_id: %s" % message.correlation_id )
        key_value_pair = map_properties.get_internals()
        print ( "    Properties: %s" % key_value_pair )
        self.SEND_CALLBACKS += 1
        print ( "    Total calls confirmed: %d" % self.SEND_CALLBACKS )

    def iothub_client_init(self):
        # prepare iothub client
        client = IoTHubClient(self.CONNECTION_STRING, self.PROTOCOL)
        # set the time until a message times out
        client.set_option("messageTimeout", self.MESSAGE_TIMEOUT)
        client.set_option("logtrace", 0)
        return client

    def iothub_client_telemetry_sample_run(self, score):
        try:
            client = self.iothub_client_init()
            print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
            message_counter = 0

            #while True:
            msg_txt_formatted = self.MSG_TXT % (score)
            # messages can be encoded as string or bytearray
            if (message_counter & 1) == 1:
                message = IoTHubMessage(bytearray(msg_txt_formatted, 'utf8'))
            else:
                message = IoTHubMessage(msg_txt_formatted)
            # optional: assign ids
            message.message_id = "message_%d" % message_counter
            message.correlation_id = "correlation_%d" % message_counter
            # optional: assign properties
            prop_map = message.properties()
            prop_text = "PropMsg_%d" % message_counter
            prop_map.add("Property", prop_text)

            client.send_event_async(message, self.send_confirmation_callback, message_counter)
            print ( "IoTHubClient.send_event_async accepted message [%d] for transmission to IoT Hub." % message_counter )
            

            status = client.get_send_status()
            print ( "Send status: %s" % status )
            pygame.time.wait(500)
            #time.sleep(0.5)
            
            status = client.get_send_status()
            print ( "Send status: %s" % status )
            

            message_counter += 1

        except IoTHubError as iothub_error:
            print ( "Unexpected error %s from IoTHub" % iothub_error )
            
        #except KeyboardInterrupt:
        #    print ( "IoTHubClient sample stopped" )

