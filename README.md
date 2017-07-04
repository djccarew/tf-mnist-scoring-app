# TensorFlow MNIST Scoring Overview

<p>The TensorFlow MNIST Scoring application is a Python application that captures a handwritten digit and then predicts it's value using a model developed for the MNIST dataset and then saved for reuse.</p>

<p>The model was built using a Convolutional Neural Network using the approach outlined in this tutorial. The model acheived 99.26% accuracy on the 10,000 digits in the MNIST test dataset.</p> 


<p>To run the app just enter a digit in the canvas, and click the *Read digit* button. The app will respond with it's prediction and a confidence level. If the level is belo**Note:** the model was *only* trained on handwritten digits so it's performance on non-digits or with random doodling may be unpredictable.</p>

<p>Click on the button below to automatically deploy this app to Bluemix</>
[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy)



## Deploying the app to Bluemix manually

1. If you do not already have a Bluemix account, [sign up here][bluemix_signup_url]

2. Download and install the [Cloud Foundry CLI][cloud_foundry_url]

3. Clone the app to your local environment from your terminal using the following command

  ```
  git clone https://github.com/IBM-Bluemix/box-watson.git
  ```

4. cd into this newly created directory

5. Edit the `manifest.yml` file and change the `<host>` value to something unique.

  ```
 applications:
  - name: tf-mnist-scoring
    host: tf-mnist-scoring
    path: .
    memory: 128M
    instances: 1
    disk_quota: 1024M
    buildpack: python_buildpack    
  ```
  The host you use will determine your application url (e.g. `<application-host>.mybluemix.net`)

6. Connect to Bluemix using the CF CLI and follow the prompts to log in.

  ```
  $ cf api https://api.ng.bluemix.net
  $ cf login
  ```

7. Push your app to Bluemix. 

  ```
  $ cf push
  ```

And voila! You now have your very own instance of the TensorFlow MNIST driver running on Bluemix.

## Running the app locally

1. You will need *Python 2.7 or greater* and *pip* installed 


2. Clone the app to your local environment from your terminal using the following command

  ```
  git clone https://github.com/djccarew/tf-mnist-scoring-app.git
  ```

3. cd into this newly created directory

4. Install the required  packages using the following command

  ```
  pip install -r requirements.txt
  ```

5. Start your app locally with the following command.

  ```
  python scoring.py
  ```

 To access the app, go to [localhost:5000](http://localhost:5000) in your browser. 
 
 ## Using your own model 
 
 1. If you haven't already signed up for the IBM Data Science Experience [sign up here][dse_signup-url]
 
 2. Once logged in to the IBM Data Science Experience, create a new notebook using the **FROM URL** option and this URL
 
 3. Run the code in the notebook to build a new model and to save that model in the Object Storage instance associated  with your Data Science Experience project
 
 4. Clone this app to your local environment from your terminal using the following command

  ```
  git clone https://github.com/djccarew/tf-mnist-scoring-app.git
  
  ```
 5. cd into this newly created directory
 
 6. In the Data Science Experience select **Data Services->Object Storage** 
 
 7. Double click on the tile for your Object Storage instance and click on the container that was automatically created for your project
 
 8. Download the 3 files *MNIST-model.meta, MNIST-model.index, MNIST-model.data-00000-00001* and   overwrite the ones in the *model* subfolder in the local copy of the app
 
 9. Push your app to Bluemix. 

  ```
  $ cf push
  ```
  
  or start  your app locally
  
  ```
  $ python scoring.py
  ```
  
10. When you run the app again you will be using  the model that you built in the Data Science Experience

## (Optional) Binding your app to your Object Storage instance
<p>Rather than downloading the model files manually you can bind your app to your Object Storage instance  so the app  can copy the model files directly from  Object Storage  </p>

 1. In the Data Science Experience select **Data Services->Object Storage** 
 
 2. Double click on the tile for your Object Storage instance and note the name of the  the container that was automatically created for your project
 ![alt text](https://ibm.box.com/shared/static/znt35nvkcatb0f0mp8hckupu08g1jdry.png)
 
 3. Clone this app to your local environment from your terminal using the following command

  ```
  git clone https://github.com/djccarew/tf-mnist-scoring-app.git
  
  ```
 4. cd into this newly created directory
 
 5. Edit the source file *scoring.py* and set the *container_name* variable on line 34 to the container name from step 2
 
   ```
    container_name='your_container_name'
   ```
 6. Save the file.
 
 7. Delete the file *model/MNIST-model.meta*
 
 8. In a new browser tab go to the Bluemix [dashboard][bm_dash_url]
 
 9. Note the name of your Object Storage instance (it will be something like *Object Storage-05*)
 
 10. From your local command line enter the follwing command to bind the serviec to your app (put quotes around your service name if it contains  spaces)
 
    ```
    $ cf bind-service tf-minist-scoring "your Object Storage instance name"
    ```
    
 12. Push the app to Bluemix
 
    ```
    $ cf push
    ```
 13. When your app is run again the model file will be downloaded from Object Storage
 

## License
This app is licensed under the Apache 2.0 license. It utilizes the [jqScribble](https://github.com/jimdoescode/jqScribble) jQuery plug-in to capture user input. 
 
[bluemix_signup_url]: http://ibm.biz/box-api-signup
[dse_signup_url]: http://datascience.ibm.com
[cloud_foundry_url]: https://github.com/cloudfoundry/cli