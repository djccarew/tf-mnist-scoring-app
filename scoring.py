# Copyright 2017 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This Flask app retrieves a TensorFlow MNIST model from Object Storage and uses it 
# to predict the values of new images of digits submitted by the user
#
# HTML and Javascript are used to capture the images of digits input by the user
#
import os
from flask import Flask, jsonify, request, Response, render_template
import numpy as np
from swift import fileio
import requests  
import json  
import pandas as pd
import tensorflow as tf
import cf_deployment_tracker

model_ready = False
model_files_available= False
credentials_available = False

### Replace the value with your own  Object Storage container name
container_name ="you Object storage container name"

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'Object-Storage' in vcap:
        creds = vcap['Object-Storage'][0]['credentials']
        user_id = creds['userId']
        password = creds['password']
        auth_url = creds['auth_url'] + '/v3/'
        project_id = creds['projectId']
        region = creds['region']
        credentials_available = True
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['Object-Storage'][0]['credentials']
        user_id = creds['userId']
        password = creds['password']
        auth_url = creds['auth_url']
        project_id = creds['projectId']
        region = creds['region']
        credentials_available = True
        
if  credentials_available:        
   swift_credentials = {
     'auth_url': auth_url,
     'project_id': project_id,
     'region': region,
     'user_id': user_id,
     'password': password,
   }

# Get saved TensorFlow model from Bluemix Object Storage
# Don't get the files if they are already here
# The app will still run if the TensorFlow model  files can't be retrieved
# or found locally but the scoring service will always return a 503 return code
# 
if  not os.path.isfile('model/MNIST-model.meta') or  not os.path.isfile('model/MNIST-model.index') or not os.path.isfile('model/MNIST-model.data-00000-of-00001'):
   if credentials_available: 
      try:
         fileio.get_binary_file(swift_credentials, container_name, "MNIST-model.data-00000-of-00001", "model/MNIST-model.data-00000-of-00001" )
         fileio.get_binary_file(swift_credentials, container_name, "MNIST-model.meta", "model/MNIST-model.meta" )
         fileio.get_binary_file(swift_credentials, container_name, "MNIST-model.index", "model/MNIST-model.index") 
         model_files_available = True
      except fileio.TokenException as e:
         print ("TokenException:", e)
      except fileio.SwiftGETException as e2:
         print ("SwiftGETException:", e2)
      except fileio.SwiftPUTException as e3:
         print ("SwiftPUTException:", e3)
else:
    model_files_available = True
    
if model_files_available:
    
   # Restore model from retrieved files
   sess = tf.InteractiveSession()

   model_name = "MNIST-model"

   new_saver = tf.train.import_meta_graph("model/" + model_name + ".meta")
   new_saver.restore(sess, "model/" + model_name)

   # Get vars saved via tf.add_collection
   x = tf.get_collection("x")[0]
   y_conv = tf.get_collection("y_conv")[0]
   keep_prob = tf.get_collection("keep_prob")[0]
   model_ready = True



def request_error(message, code):
    """"
    Utility function for generating a custom error response for a given given request
    Parameters -
       message - The custom message 
       code - The HTTP return code
    """
    
    response = jsonify({'errmsg': message})
    response.status_code = code
    return response

## HTML page 
@app.route('/')
def main_page():
    return render_template('index.html')

## Scoring service
@app.route('/api/score', methods=['POST'])
def scoring_service():
    if model_ready:
       image_raw = request.json
       # Create  a numpy array from the input  image's pixel values and normalize 
       # the values to the  0 to 1.0 range
       img = (np.array(image_raw, dtype=np.uint8)/255.0).reshape(1, 784)
       # Get prediction
       logit = sess.run(y_conv,feed_dict={ x: img, keep_prob: 1.0})
       digit = max(sess.run(tf.argmax(logit,1)))
       # Calculate confidence
       probability =  max(tf.nn.softmax(logit,name="softmax_tensor").eval().flatten().tolist())
     
       prediction= {
           "digit": digit,
           "probability": probability
       }
       return jsonify(results=prediction)
    else:
        return request_error("Scoring service not initialized", 503)


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
