import cv2
import numpy as np

# SETTINGS
TOTAL_QUESTIONS = 100
OPTIONS_PER_QUESTION = 4

# Example Answer Key (all A)
ANSWER_KEY = {i:0 for i in range(TOTAL_QUESTIONS)}

# LOAD IMAGE
image = cv2.imread("hello.jpeg")

if image is None:
    print("❌ Image not found. Check file name.")
    exit()

print("✅ Image loaded")

# GRAYSCALE
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# BLUR
blur = cv2.GaussianBlur(gray,(5,5),0)

# THRESHOLD
thresh = cv2.threshold(blur,0,255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# FIND CONTOURS
contours,_ = cv2.findContours(thresh,
                              cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)

bubble_contours = []

# FILTER BUBBLES
for c in contours:

    x,y,w,h = cv2.boundingRect(c)

    aspect = w/float(h)

    if w>20 and h>20 and 0.8<aspect<1.2:
        bubble_contours.append(c)

print("Detected bubbles:",len(bubble_contours))

# SORT TOP TO BOTTOM
bubble_contours = sorted(bubble_contours,
                         key=lambda c:cv2.boundingRect(c)[1])

score = 0

for q in range(0,len(bubble_contours),4):

    question = bubble_contours[q:q+4]

    if len(question)<4:
        continue

    question = sorted(question,
                      key=lambda c:cv2.boundingRect(c)[0])

    bubbled = None
    max_pixels = 0

    for j,c in enumerate(question):

        mask = np.zeros(thresh.shape,dtype="uint8")

        cv2.drawContours(mask,[c],-1,255,-1)

        masked = cv2.bitwise_and(thresh,thresh,mask=mask)

        total = cv2.countNonZero(masked)

        if total>max_pixels:
            max_pixels = total
            bubbled = j

    correct = ANSWER_KEY[q//4]

    if bubbled == correct:

        score += 1

        x,y,w,h = cv2.boundingRect(question[correct])

        cv2.circle(image,(x+w//2,y+h//2),10,(0,255,0),2)

# SHOW SCORE
cv2.putText(image,
            f"Score: {score}/{TOTAL_QUESTIONS}",
            (30,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,0,0),
            2)

cv2.imwrite("result.jpg",image)

print("✅ Result saved as result.jpg")

cv2.imshow("Result",image)
cv2.waitKey(0)
cv2.destroyAllWindows()