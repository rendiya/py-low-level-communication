/* Read TextFile Data: Written by ScottC on 24 April 2013
 Arduino IDE version: 1.0.4
 http://arduinobasics.blogspot.com.au/2013/04/serial-communication-tutorial-part-3.html
*/
// Protocol defines
#define ENQ 0x05
#define SYN 0x16
#define ACK 0x06
#define NAK 0x15
#define CAN 0x18

#define SOH 0x01
#define ETB 0x17
#define STX 0x02
#define ETX 0x03
#define EOT 0x04

bool synced;
byte readByte;
/* Global Variables */
 

void setup() {
  Serial.begin(9600);
  synced = false;
}

void loop() {
  if (synced==false){
    Serial.write(ENQ);
    if (Serial.available()){
      readByte = Serial.read();
      if (readByte == ACK){
        Sync();
      }
    }
    delay(200);
  }
  if (Serial.available()){
    readByte = Serial.read();
    if (readByte == ENQ){
      Serial.write(ACK);
      Sync();
      }
      else if(readByte==EOT){
        EndSync();
      }
      else if(readByte==NAK){
        EndSync();
        Serial.write(EOT);
      }
      else{
        Serial.write(NAK);
      }
    }
}

void Sync(){
  Serial.write("hello");
  synced = true;
}

void EndSync(){
  synced = false;
}
