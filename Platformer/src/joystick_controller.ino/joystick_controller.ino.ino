#define joystickXPin A0
#define buttonJumpPin 2
#define buttonShiftPin 3

int leftThreshold = 400;  // 왼쪽으로 간주할 임계값
int rightThreshold = 600; // 오른쪽으로 간주할 임계값

void setup() {
    Serial.begin(9600); // 시리얼 통신 시작
    pinMode(joystickXPin, INPUT);
    pinMode(buttonJumpPin, INPUT_PULLUP); // 점프 버튼
    pinMode(buttonShiftPin, INPUT_PULLUP); // 달리기 버튼
}

void loop() {
    int xValue = analogRead(joystickXPin); // 조이스틱 X축 값 읽기
    bool buttonJump = !digitalRead(buttonJumpPin); // 점프 버튼 상태
    bool buttonShift = !digitalRead(buttonShiftPin); // 쉬프트 버튼 상태

    String direction;
    if (xValue < leftThreshold) {
        direction = "Left";
    } else if (xValue > rightThreshold) {
        direction = "Right";
    } else {
        direction = "Center";
    }

    // 시리얼 모니터에 값과 방향 출력
    Serial.print("Joystick X: ");
    Serial.print(xValue);
    Serial.print(" (");
    Serial.print(direction);
    Serial.print(") | Jump Button: ");
    Serial.print(buttonJump);
    Serial.print(" | Shift Button: ");
    Serial.println(buttonShift);

    delay(500); // 0.5초마다 출력
}