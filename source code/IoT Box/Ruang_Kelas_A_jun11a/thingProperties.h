// Code generated by Arduino IoT Cloud, DO NOT EDIT.

#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>

const char DEVICE_LOGIN_NAME[]  = "3f8d00e0-e31f-4470-958c-e7593f300aed";

const char SSID[]               = SECRET_SSID;    // Network SSID (name)
const char PASS[]               = SECRET_OPTIONAL_PASS;    // Network password (use for WPA, or use as key for WEP)
const char DEVICE_KEY[]  = SECRET_DEVICE_KEY;    // Secret device password

void onDev1Change();
void onDev2Change();
void onDev3Change();
void onDev4Change();

CloudLight dev1;
CloudLight dev2;
CloudLight dev3;
CloudLight dev4;

void initProperties(){

  ArduinoCloud.setBoardId(DEVICE_LOGIN_NAME);
  ArduinoCloud.setSecretDeviceKey(DEVICE_KEY);
  ArduinoCloud.addProperty(dev1, READWRITE, ON_CHANGE, onDev1Change);
  ArduinoCloud.addProperty(dev2, READWRITE, ON_CHANGE, onDev2Change);
  ArduinoCloud.addProperty(dev3, READWRITE, ON_CHANGE, onDev3Change);
  ArduinoCloud.addProperty(dev4, READWRITE, ON_CHANGE, onDev4Change);

}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);
