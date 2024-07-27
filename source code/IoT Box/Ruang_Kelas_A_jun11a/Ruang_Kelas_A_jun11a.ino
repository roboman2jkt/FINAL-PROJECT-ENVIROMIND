#include "arduino_secrets.h"
/* 
  Sketch generated by the Arduino IoT Cloud Thing "Untitled"
  https://create.arduino.cc/cloud/things/97f149f4-6a57-4732-b813-120fe213026f 

  Arduino IoT Cloud Variables description

  The following variables are automatically generated and updated when changes are made to the Thing

  CloudLight dev1;
  CloudLight dev2;
  CloudLight dev3;
  CloudLight dev4;

  Variables which are marked as READ/WRITE in the Cloud Thing will also have functions
  which are called when their values are changed from the Dashboard.
  These functions are generated with the Thing and added at the end of this sketch.
*/

#include "thingProperties.h"

#define device1 32
#define device2 33
#define device3 25
#define device4 26

#define button1 15
#define button2 17
#define button3 4
#define button4 2


boolean sta1, sta2, sta3, sta4;



void setup() {
  // Initialize serial and wait for port to open:
  Serial.begin(9600);

  pinMode(device1, OUTPUT);  //relay1
  pinMode(device2, OUTPUT);  //relay2
  pinMode(device3, OUTPUT);  //relay3
  pinMode(device4, OUTPUT); //relay4

  pinMode(button1, INPUT);  //button1
  pinMode(button2, INPUT);  //button2
  pinMode(button3, INPUT);  //button3
  pinMode(button4, INPUT); //button4
  
  // This delay gives the chance to wait for a Serial Monitor without blocking if none is found
  delay(1500); 

  // Defined in thingProperties.h
  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  
  /*
     The following function allows you to obtain more information
     related to the state of network and IoT Cloud connection and errors
     the higher number the more granular information you’ll get.
     The default is 0 (only errors).
     Maximum is 4
 */
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();
  // Your code here 

  if (WiFi.status() == WL_CONNECTED || WiFi.status() != WL_CONNECTED ){
    if(digitalRead(button1) == 1){
      delay(100);
      sta1 = !sta1;
      dev1 = sta1;
      delay(500);
    }

    if(digitalRead(button2) == 1){
      delay(100);
      sta2 = !sta2;
      dev2 = sta2;
      delay(500);
    }
    
    if(digitalRead(button3) == 1){
      delay(100);
      sta3 = !sta3;
      dev3 = sta3;
      delay(500);
    }
    
     if(digitalRead(button4) == 1){
      delay(100);
      sta4 = !sta4;
      dev4 = sta4;
      delay(500);
    }
    
   
  }
  
  if(sta1){
      digitalWrite(device1, HIGH);
    }else{
      digitalWrite(device1, LOW);
    }
  if(sta2){
    digitalWrite(device2, HIGH);
  }else{
    digitalWrite(device2, LOW);
    }
  if(sta3){
      digitalWrite(device3, HIGH);
  }else{
    digitalWrite(device3, LOW);
  }
  if(sta4){
    digitalWrite(device4, HIGH);
  }else{
    digitalWrite(device4, LOW);
    }
}


/*
  Since Dev1 is READ_WRITE variable, onDev1Change() is
  executed every time a new value is received from IoT Cloud.
*/
void onDev1Change()  {
  // Add your code here to act upon Dev1 change
  if(dev1 == 1){
    sta1 = 1; //pembalik
  }else{
    sta1 = 0;
  }

  if(sta1){
      digitalWrite(device1, HIGH);
    }else{
      digitalWrite(device1, LOW);
    }
}

/*
  Since Dev2 is READ_WRITE variable, onDev2Change() is
  executed every time a new value is received from IoT Cloud.
*/
void onDev2Change()  {
  // Add your code here to act upon Dev2 change
   if(dev2 == 1){
    sta2 = 1; //pembalik
  }else{
    sta2 = 0;
  }
    
    if(sta2){
      digitalWrite(device2, HIGH);
    
    }else{
      digitalWrite(device2, LOW);
    }
  
}

/*
  Since Dev3 is READ_WRITE variable, onDev3Change() is
  executed every time a new value is received from IoT Cloud.
*/
void onDev3Change()  {
  // Add your code here to act upon Dev3 change
  if(dev3 == 1){
    sta3 = 1; //pembalik
  }else{
    sta3 = 0;
  }
    
    if(sta3){
      digitalWrite(device3, HIGH);
    }else{
      digitalWrite(device3, LOW);
    }
  
}

/*
  Since Dev4 is READ_WRITE variable, onDev4Change() is
  executed every time a new value is received from IoT Cloud.
*/
void onDev4Change()  {
  // Add your code here to act upon Dev4 change
  if(dev4 == 1){
    sta4 = 1; //pembalik
  }else{
    sta4 = 0;
  }
    
    if(sta4){
      digitalWrite(device4, HIGH);
    }else{
      digitalWrite(device4, LOW);
    }
  }

