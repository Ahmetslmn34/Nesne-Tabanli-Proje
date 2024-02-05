import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

class Button:
    def __init__(self, position, width, height, value):
        self.position = position
        self.width = width
        self.height = height
        self.value = value
        self.is_clicked = False

    def draw(self, img, color=(225, 225, 225)):
        if self.is_clicked:
            color = (0, 255, 0)  
        cv2.rectangle(img, self.position, (self.position[0] + self.width, self.position[1] + self.height),
                      color, cv2.FILLED)
        cv2.rectangle(img, (self.position[0] - 2, self.position[1] - 2),
                      (self.position[0] + self.width + 2, self.position[1] + self.height + 2),
                      (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.position[0] + 40, self.position[1] + 60), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)

    def check_click(self, x, y):
        if self.position[0] < x < self.position[0] + self.width and \
                self.position[1] < y < self.position[1] + self.height:
            return True
        return False

button_values = [['7', '8', '9', '*'],
                ['4', '5', '6', '='],
                ['1', '2', '3', '+'],
                ['0', '/', '.', '-']]

button_list = []
for x in range(4):
    for y in range(4):
        x_position = x * 100 + 700
        y_position = y * 100 + 150
        button_list.append(Button((x_position, y_position), 100, 100, button_values[y][x]))
equation = ''
delay_counter = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    cv2.imshow('Image', img)
    cv2.rectangle(img, (700, 50), (700 + 400, 70 + 100), (255, 255, 255), cv2.FILLED)  
    cv2.rectangle(img, (700, 50), (700 + 400, 70 + 100), (50, 50, 50), 3)
    for button in button_list:
        button.draw(img, (255, 255, 255))
    hand = None  
    if hands:
        hand = hands[0]
        if hand['lmList'][8][0] == 0 and hand['lmList'][12][0] == 0:
            for button in button_list:
                x, y = hand['lmList'][8][1], hand['lmList'][8][2]  
                if button.check_click(x, y):
                    current_value = button_values[int(button_list.index(button) % 4)][int(button_list.index(button) / 4)]
                    if current_value == '=':
                        try:
                            equation = str(eval(equation))
                        except:
                            equation = 'Error'
                    else:
                        equation += current_value
                    button.is_clicked = not button.is_clicked 
    for button in button_list:
        if hand and button.check_click(hand['lmList'][8][1], hand['lmList'][8][2]):
            if button.value.isdigit():  
                button.is_clicked = not button.is_clicked
    if delay_counter != 0:
        delay_counter += 1
        if delay_counter > 10:
            delay_counter = 0
    cv2.putText(img, equation, (710, 120), cv2.FONT_HERSHEY_PLAIN, 3, (12, 45, 31), 3) 
    cv2.imshow('Image', img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        equation = ''
    if key == 27:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
