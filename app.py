from flask import Flask, request, send_file
import os
import cv2
import numpy as np

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]
    filepath = "input.jpg"
    file.save(filepath)

    # ===== YOUR CODE STARTS (UNCHANGED) =====
    image = cv2.imread(filepath)

    TOTAL_QUESTIONS = 100
    ANSWER_KEY = {i:0 for i in range(TOTAL_QUESTIONS)}

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.threshold(blur,0,255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    contours,_ = cv2.findContours(thresh,
                                  cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)

    bubble_contours = []

    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        aspect = w/float(h)
        if w>20 and h>20 and 0.8<aspect<1.2:
            bubble_contours.append(c)

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

    cv2.putText(image,
                f"Score: {score}/{TOTAL_QUESTIONS}",
                (30,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,0,0),
                2)

    output_path = "result.jpg"
    cv2.imwrite(output_path,image)
    # ===== YOUR CODE ENDS =====

    return send_file(output_path, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(debug=True)