#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// most of the code is based on code from www.inovafitness.com and 
// www.dfrobot.com

// set the LCD address to 0x2? for a 16 chars and 2 line display
// use a i2c scanner to detect the real address!
LiquidCrystal_I2C lcd(0x20, 20, 4); 

long previousMillis = 0;
const int analogInPin = A0;
int latch = 8;
int srclk = 9;
int ser = 10;

unsigned char displayTemp[8];
unsigned int Pm25 = 0;
unsigned int Pm10 = 0;

void ProcessSerialData()
{
  uint8_t mData = 0;
  uint8_t i = 0;
  uint8_t mPkt[10] = {0};
  uint8_t mCheck = 0;
  while (Serial.available() > 0)
  {
    // from www.inovafitness.com
    // packet format: AA C0 PM25_Low PM25_High PM10_Low PM10_High 0 0 CRC AB
    mData = Serial.read();     delay(2);//wait until packet is received
    //Serial.println(mData);
    //Serial.println("*");
    if (mData == 0xAA) //head1 ok
    {
      mPkt[0] =  mData;
      mData = Serial.read();
      if (mData == 0xc0) //head2 ok
      {
        mPkt[1] =  mData;
        mCheck = 0;
        for (i = 0; i < 6; i++) //data recv and crc calc
        {
          mPkt[i + 2] = Serial.read();
          delay(2);
          mCheck += mPkt[i + 2];
        }
        mPkt[8] = Serial.read();
        delay(1);
        mPkt[9] = Serial.read();
        if (mCheck == mPkt[8]) //crc ok
        {
          Serial.flush();
          //Serial.write(mPkt,10);

          Pm25 = (uint16_t)mPkt[2] | (uint16_t)(mPkt[3] << 8);
          Pm10 = (uint16_t)mPkt[4] | (uint16_t)(mPkt[5] << 8);
          if (Pm25 > 9999)
            Pm25 = 9999;
          if (Pm10 > 9999)
            Pm10 = 9999;
          //            Serial.println(Pm25);
          //          Serial.println(Pm10);
          //get one good packet
          return;
        }
      }
    }
  }
}

void setup() {
  lcd.init();                      // initialize the lcd
  // Print a message to the LCD.
  lcd.backlight();
  Serial.begin(9600, SERIAL_8N1);
  //Serial.begin(9600);
  Pm25 = 0;
  Pm10 = 0;
}

void loop() {
  ProcessSerialData();

  lcd.setCursor(0, 0);
  lcd.print("PM 2.5 -> ");
  lcd.print(float(Pm25) / 10.0);
  lcd.setCursor(0, 1);
  lcd.print("PM 10 -> ");
  lcd.print(float(Pm10) / 10.0);

//  Serial.print("Pm2.5 ");
//  Serial.print(float(Pm25) / 10.0);
//  Serial.println();//  Display();
//  Serial.print("Pm10 ");
//  Serial.print(float(Pm10) / 10.0);
//  Serial.println();
  delay(500);
}
