import serial, time

arduino = serial.Serial('/dev/cu.usbmodem14601', 9600, timeout=.1)
time.sleep(5) #give the connection a second to settle
arduino.write(b'Hello from Python!')

while True:
	data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
	if data:
		print(data.decode("utf-8"))

"""
void setup() {
  Serial.begin(9600);
}

void loop() {
  // Serial.println("Hello world from Ardunio!"); // write a string
  while(Serial.available())
  {
    String input = Serial.readString();
    Serial.println(input);
  }
  delay(1000);
}
"""
