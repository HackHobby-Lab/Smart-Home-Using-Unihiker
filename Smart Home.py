import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
import threading
from pinpong.board import *
from pinpong.extension.unihiker import *

#Board().begin()  # Initialize the UNIHIKER

MQTT_ADDRESS = '192.168.X.XX'
MQTT_USER = 'ali'              #this is username for MQTT connection. 
MQTT_PASSWORD = '786'          #this is password for MQTT connection. Choose stronger password.
MQTT_TOPIC_test = 'esp pub topic' #This topic will be used by Python to which it'll subscribe and receive data from esp
topic ='esp sub topic'   #This topic will be used by Python to Publish data to esp

on_image_path = "lightbulbOn.png" #Path to the image
off_image_path = "lightbulbOff.png"
on_image_path_fan = "fanOn.png"
off_image_path_fan = "fanOff.png"


#MQTT connection
def on_connect(client, userdata, flags, rc):

        print('Connected with result code ' + str(rc))
        client.subscribe(MQTT_TOPIC_test)


        
def on_message(client, userdata, msg):
        global new_data
        #print(msg.topic + ' '  + str(msg.payload))
        message = msg.payload
        new_data =  message.decode()
        lcd_update() #Update the lcd for Temperature Value
        #print(new_data)

class light_Button(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.init_pinpong()
        
        #Label for options : "Day" and "Night"
        self.light_label = QLabel(self)
        self.light_label.setGeometry(10, 10, 40, 20)
        self.light_label.setStyleSheet("color: Green; background-color: transparent; font-size: 14px; font-family: Arial;")
        
        #MainWindow
        self.setWindowTitle("Automation") #This title is useless for Unihker but You can keep it if you're in Window Os
        self.setGeometry(0, 0, 240, 320)
        self.setStyleSheet("background-color: black;")
        label = QLabel("Smart Home", self) 
        label.setGeometry(70, 25, 165, 15)
        label.setStyleSheet("color: yellow; background-color: transparent; font-size: 16px; font-family: Arial;")
        

        #creating Lcd widget for Temperature
        self.lcd = QLCDNumber(self)
        self.lcd.setGeometry(QRect(110,290,64,23))
        self.lcd.setStyleSheet("color: yellow; background-color: transparent;")
        self.lcd.setFrameShape(QFrame.NoFrame)
        self.lcd.setLineWidth(1)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.setLayoutDirection(Qt.LeftToRight)
        label_Temp = QLabel("Temperature:", self) #Label for "Temperature before LCD Widget"
        label_Temp.setGeometry(30, 290, 90, 20)
        label_Temp.setStyleSheet("color: yellow; background-color: transparent; font-size: 16px; font-family: Arial;")
        label_C = QLabel("°C", self) # Label for "C" after LCD
        label_C.setGeometry(170, 290, 90, 20)
        label_C.setStyleSheet("color: yellow; background-color: transparent; font-size: 16px; font-family: Arial;")

        #creating first Button
        self.toggle_state = False
        self.toggle_button1 = QPushButton(self)
        self.toggle_button1.setGeometry(70, 50, 100, 60)
        self.toggle_button1.setCheckable(True)
        self.toggle_button1.setStyleSheet("background-color: grey;")
        self.toggle_button1.setText("Bulb")

        # Load the images for ON and OFF states
        self.on_icon1 = QIcon(on_image_path)
        #self.on_icon1.pixmap(100, 100)
        self.off_icon1 = QIcon(off_image_path)
        self.toggle_button1.setIcon(self.off_icon1)
        self.toggle_button1.setIconSize(QSize(50,50)) #Icon size, which is being displayed inside button
        self.toggle_button1.clicked.connect(self.toggle_button1_clicked)
        #self.toggle_button1.setStyleSheet("background-color: transparent; border: none;")

        # Create the second button
        self.toggle_state2 = False
        self.toggle_button2 = QPushButton(self)
        self.toggle_button2.setGeometry(70, 120, 100, 60)
        self.toggle_button2.setCheckable(True)
        self.toggle_button2.setStyleSheet("background-color: grey;")
        self.toggle_button2.setText("Bulb")
        # Load the images for the second button
        self.on_icon2 = QIcon(on_image_path)   
        self.off_icon2 = QIcon(off_image_path) 
        self.toggle_button2.setIcon(self.off_icon2)
        self.toggle_button2.setIconSize(QSize(50,50))
        self.toggle_button2.clicked.connect(self.toggle_button2_clicked)
        #self.toggle_button2.setStyleSheet("background-color: transparent; ")


        # Create the third button
        self.toggle_state3 = False
        self.toggle_button3 = QPushButton(self)
        self.toggle_button3.setGeometry(70, 190, 100, 60)
        self.toggle_button3.setCheckable(True)
        self.toggle_button3.setStyleSheet("background-color: grey;")
        self.toggle_button3.setText("Fan")
        # Load the images for the third button
        self.on_icon3 = QIcon(on_image_path_fan)  
        self.off_icon3 = QIcon(off_image_path_fan)  
        self.toggle_button3.setIcon(self.off_icon3)
        self.toggle_button3.setIconSize(QSize(50,50))
        self.toggle_button3.clicked.connect(self.toggle_button3_clicked)
        #self.toggle_button3.setStyleSheet("background-color: transparent; ")
    

    def toggle_button1_clicked(self):
        
        self.toggle_state = not self.toggle_state
        if self.toggle_state:
            self.toggle_button1.setIcon(self.on_icon1)
            print("Button 1 pressed")
            mqtt_client.publish(topic, "B1N") #Sending message to Client Esp8266
            print('ON')
            
        else:
            self.toggle_button1.setIcon(self.off_icon1)
            mqtt_client.publish(topic, "B1F") #Sending message to Client Esp8266
            print('OFF')


    def toggle_button2_clicked(self):
        self.toggle_state2 = not self.toggle_state2
        if self.toggle_state2:
            self.toggle_button2.setIcon(self.on_icon2)
            mqtt_client.publish(topic, "B2N") #Sending message to Client Esp8266
            print("Button 2 pressed")
        else:
            self.toggle_button2.setIcon(self.off_icon2)
            mqtt_client.publish(topic, "B2F") #Sending message to Client Esp8266

    def toggle_button3_clicked(self):
        self.toggle_state3 = not self.toggle_state3
        if self.toggle_state3:
            self.toggle_button3.setIcon(self.on_icon3)
            mqtt_client.publish(topic, "B3N") #Sending message to Client Esp8266
            print("Button 3 pressed")
        else:
            self.toggle_button3.setIcon(self.off_icon3)
            mqtt_client.publish(topic, "B3F") #Sending message to Client Esp8266
    
    
    
    def lcd_update(self):
            self.lcd.setProperty("intValue", new_data) #Updating the Lcd value
    


    def init_pinpong(self):
        Board().begin()  
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_light_intensity)
        self.timer.start(100)  
        
    def read_light_intensity(self):
        global light_value
        light_value = light.read()  #reading light sensor
        #print("Ambient light intensity: %d" % light_value)  
        
        
        if light_value < 25:
             self.light_label.setText("Night")
             #mqtt_client.publish(topic, "B1N") #Sending message to Client Esp8266


        else:
            self.light_label.setText("Day")
            #mqtt_client.publish(topic, "B1F") #Sending message to Client Esp8266


            
             
              
            

if __name__ == "__main__":
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_ADDRESS, 1884) 
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = light_Button()
    window.show()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message =  on_message
    lcd_update = window.lcd_update
    # Create a thread for running the MQTT client loop
    #Threading prevents other programs from getting blocked
    mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
    mqtt_thread.daemon = True  # Set the thread as a daemon so it doesn't block the program from exiting
    mqtt_thread.start()

    sys.exit(app.exec_())
    
        