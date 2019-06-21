 #define NOTE_A 440  //ド
#define NOTE_B 493　　//レ
#define NOTE_C 554  //ミ
#define NOTE_D 587  // ファ
#define NOTE_E 659  //ソ
#define NOTE_F 739  //ラ
#define NOTE_G 830  //シ
#define NOTE_A2 880  //ド
#define NOTE_B2 988  //レ

#define WHOLE 1
#define HALF 0.5
#define QUARTER 0.25
#define EIGHTH 0.125
#define SIXTEENTH 0.625



int length;   
int tonePin=2;                // buzzer pin
int ledPin=12;                // led pin
int BtnPin1=5;
int BtnPin2=6;
int BtnPin3=7;

void setup(){
  Serial.begin(9600);
  pinMode(tonePin,OUTPUT);   //  initialize the digital pin as an output
}

void loop(){
  sound_famima();  
}
