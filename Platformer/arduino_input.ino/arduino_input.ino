const int JOY_X = A3;    // X축 핀
const int BUTTON1 = 2;   // 버튼1 핀
const int BUTTON2 = 3;   // 버튼2 핀

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON1, INPUT_PULLUP);
  pinMode(BUTTON2, INPUT_PULLUP);
}

void loop() {
  int xValue = analogRead(JOY_X);
  int button1State = !digitalRead(BUTTON1);  // 버튼 눌림 = 1
  int button2State = !digitalRead(BUTTON2);
  
  String data = String(xValue) + "," + 
                String(button1State) + "," + 
                String(button2State);
                
  Serial.println(data);
  delay(50);  // 통신 안정성을 위한 딜레이
}
