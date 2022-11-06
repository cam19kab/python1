from flask import Flask, render_template,Flask
#import cv2
#import mediapipe as mp

#Realizar nuestra VideoCaptura

cap = cv2.VideoCapture(0)

def gen_frame():
    # empezamos
    while True:
        ret, frame= cap.read()
        if not ret:
            break
        else:
            suc, encode = cv2.imencode('.jpg',frame)
            frame = encode.tobytes()

        yield(b'--frame\r\n'
            b'content-Type: image/jpeg\r\n\r\n'+ frame + b'\r\n')


#Creamos la app
app = Flask(__name__)

#Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen_frame(), mimetype="multipart/x-mixed-replace; boundary=frame")


# Ejecutar
if __name__=="__main__":
    app.run(debug=True)