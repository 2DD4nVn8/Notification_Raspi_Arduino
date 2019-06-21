int tune1[] =   //famima1
{
    NOTE_F, NOTE_D, NOTE_A, NOTE_D, NOTE_E, NOTE_A2,
    NOTE_E, NOTE_F, NOTE_E, NOTE_A, NOTE_D
}; 

float duration1[]=
{1,1,1,1,1,3,
 1,1,1,1,4};



void sound_famima(){
  length = sizeof(tune1)/sizeof(tune1[0]);
  for(int x=0;x<length;x++){
    tone(tonePin,tune1[x]);
        delay(300*duration1[(x%100)]);    // to distinguish the notes, set a minimum time between them.

        noTone(tonePin); // stop the tone playing:
    }  
}
