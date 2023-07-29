IMAGES=["lscr.io/linuxserver/firefox:latest"]
CONTAINER_TIME_SECONDS=180

import os
from uuid import uuid4
from datetime import timedelta

from flask import Flask, render_template, request

app = Flask(__name__)

REDIS_SERVER = os.environ['REDIS_SERVER']

from rq import Queue
from redis import Redis
q = Queue(connection=Redis(REDIS_SERVER))

def setup_container(image_name):
    container_id = str(uuid4())+"-browser"
    #send start task
    q.enqueue('worker.create_container',args=(image_name,container_id))
    #send stop task in 180 seconds
    q.enqueue_in(timedelta(seconds=CONTAINER_TIME_SECONDS),'worker.kill_container',args=(container_id,))
    return container_id

# list options, captcha, user sends captcha and image name
@app.route('/', methods=['GET', 'POST'])
def index():
     if request.method == 'GET':
         return render_template("index.html", images=IMAGES)
     if request.method == 'POST':
         if request.form['image']:
             image_name = request.form['image'].strip()
             if image_name in IMAGES:
                 container_id = setup_container(image_name)
                 return render_template("container.html", container_id=container_id.split('-browser')[0])

if __name__ == '__main__':
    app.run(debug=False)
