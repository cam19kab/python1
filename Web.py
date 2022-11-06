from flask import Flask, render_template,Flask,Response
import cv2
import mediapipe as mp

# Drawing Funtion
# Create own drawing function

mpDibujo = mp.solutions.drawing_utils
ConfDibu =mpDibujo.DrawingSpec(thickness=1,circle_radius=1)

# Create a object where we are save all the face

mpMallaFacial = mp.solutions.face_mesh
MallaFacial = mpMallaFacial.FaceMesh(max_num_faces=1)

# VideoCapture
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
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
            resultados = MallaFacial.process(frameRGB)

            # If we detect some face
            if resultados.multi_face_landmarks:
                # iteration
                for rostros in resultados.multi_face_landmarks:
                    #drawing
                    mpDibujo.draw_landmarks(frame, rostros, mpMallaFacial.FACEMESH_TESSELATION, ConfDibu, ConfDibu)

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