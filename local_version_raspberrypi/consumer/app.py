import datetime
from flask import Flask, Response, render_template, request, redirect, url_for, session, abort, flash
from kafka import KafkaConsumer
import os 


#NOTE - when running this, run with gunicorn kafka_consumer:app -b 127.0.0.1:8001 - or whatever 
#address and port is assigned in your NGINX file 

# Fire up the Kafka Consumer
topic = "distributed-video1"

consumer = KafkaConsumer(
    topic, 
    bootstrap_servers=['localhost:9092'])


# Set the consumer in a Flask App
app = Flask(__name__)
app.secret_key = 'sdfsdfds32423rwsdgsdg_UI*#^$*&^shjfgs'




@app.route('/', methods=['GET'])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('camera.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == '46566656':
        session['logged_in'] = True
    else:
        flash('wrong! hahaha')
    return home()


@app.route('/dogcam', methods=['GET'])
def dogcam():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('camera.html')



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()



###THIS PART BELOW IS FOR THE ACTUAL CV STREAM/ INGESTION 

@app.route('/video', methods=['GET'])
def video():
    return Response(
        get_video_stream(), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

def get_video_stream():
    for msg in consumer:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + msg.value + b'\r\n\r\n')




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)





