# About

World Health Organization has estimated 12 million deaths occur worldwide, every year due to Heart diseases. Half the deaths in the United States and other developed countries are due to cardio vascular diseases. The early prognosis of cardiovascular diseases can aid in making decisions on lifestyle changes in high risk patients and in turn reduce the complications. This research intends to pinpoint the most relevant/risk factors of heart disease as well as predict the overall risk.

## Source
The dataset is publically available on the Kaggle website, and it is from an ongoing cardiovascular study on residents of the town of Framingham, Massachusetts. The classification goal is to predict whether the patient has 10-year risk of future coronary heart disease (CHD).The dataset provides the patients’ information. It includes over 4,000 records and 15 attributes.
[Kaggle link.](https://www.kaggle.com/dileep070/heart-disease-prediction-using-logistic-regression)

## Variables
Each attribute is a potential risk factor. There are both demographic, behavioral and medical risk factors.

Demographic:
* Sex: male or female (Nominal)
* Age: Age of the patient (Continuous)

Behavioral:
* Current Smoker: whether or not the patient is a current smoker (Nominal)
* Cigs Per Day: the number of cigarettes that the person smoked on average in one day (Continuous)

Medical(history):
* BP Meds: whether or not the patient was on blood pressure medication (Nominal)
* Prevalent Stroke: whether or not the patient had previously had a stroke (Nominal)
* Prevalent Hyp: whether or not the patient was hypertensive (Nominal)
* Diabetes: whether or not the patient had diabetes (Nominal)

Medical(current):
* Tot Chol: total cholesterol level (Continuous)
* Sys BP: systolic blood pressure (Continuous)
* Dia BP: diastolic blood pressure (Continuous)
* BMI: Body Mass Index (Continuous)
* Heart Rate: heart rate (Continuous)
* Glucose: glucose level (Continuous)

Predict variable (desired target):
* 10 year risk of coronary heart disease CHD (binary: “1”, means “Yes”, “0” means “No”)

## Solution
This is a binary classification problem. It has been decided to use following models for the development of ML solution:
1. [Logistic Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
2. [Decision Tree Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)
3. [Random Forest Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
4. [XGBoost](https://xgboost.readthedocs.io/en/latest/)
5. [LightGBM](https://lightgbm.readthedocs.io/en/latest/)
6. [k-Nearest Neighbors](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)

Evaluation metric [ROC-AUC](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html) has been chosen for the model selection process.

Please refer to `notebook.ipynb` where you may find the following:
 - data preparation, data cleaning
 - handling NaN values
 - EDA, outliers analysis
 - feature importance analysis, analysis of target variable
 - model selection process and parameters tuning

Selected model is Logistic Regression based on chosen metric.

**Please be aware that this project has been done on macOS.**

## Train the final model and Predict
In `train.py` file you may find data preprocessing, training the final model and saving it into a pickle file. `predict.py` file contains loading the model and serving it via a web service with Flask.

## Dependency and Environment management
It has been decided to use conda virtual environment for managing dependencies. The following command was used to create environment file with required packages:
`conda env export > environment_full.yml` inside working project directory. In order to install the dependencies and activate the environment please use following commands: `conda env create -f environment_full.yml` and `conda activate ds`. 

## Containerization
The majority of depencencies have been removed except required for production deployment:
  - python=3.9
  - flask
  - scikit-learn=0.24
  - gunicorn
  - numpy
  
Please refer to `environment.yml` file for details.

Installation of dependencies and activating a conda environment in a Dockerfile is not a straightforward process and significantly differs from using other virtual environment handling tools. I used [this](https://pythonspeed.com/articles/activate-conda-dockerfile/) article as a guidance when I create the `Dockerfile`. I would like to pay your attention to additional file `entrypoint.sh` which is used to disable so-called “bash strict mode” when activating conda environment. This is done because some Conda activation scripts break when this mode is enabled. Before proceeding with the building of container please make sure that the line `CMD ["./entrypoint.sh"]` in `Dockerfile` **is commented** and line `exec gunicorn --bind 0.0.0.0:<dollar_sign>PORT predict:app` in `entrypoint.sh` **is commented**.

Build the container: `sudo docker build -t heart-disease .`

Run the container: `docker run -it --rm -p 9696:9696 heart-disease`

Test prediction made by the model by running: `python predict-test.py`. Based on the health parameters provided in the `predict-test.py` file you should get the following result:
```
{'disease_probability': 0.22, 'risk': False}
The person with provided health parameters has NO 10-year risk of future coronary heart disease
```

## Deployment to the Cloud: Heroku
*It is assumed that you already have Heroku account*

Due to the nature of how Heroku creates applications and specific requirements to the Dockerfile command please make sure that you've done the following in the `Dockerfile`:
- comment line `EXPOSE 9696` - [EXPOSE is NOT supported by Heroku](https://devcenter.heroku.com/articles/container-registry-and-runtime#:~:text=EXPOSE%20%2D%20While%20EXPOSE%20can%20be,get%20the%20%24PORT%20environment%20variable.)
- comment line `ENTRYPOINT ["./entrypoint.sh"]`
- uncomment line `CMD ["./entrypoint.sh"]` - CMD is required to run on Heroku 

Please make sure that you've done the following in the `entrypoint.sh` as well:
- comment line `exec gunicorn --bind=0.0.0.0:9696 predict:app`
- uncomment line `exec gunicorn --bind 0.0.0.0:<dollar_sign>PORT predict:app` - PORT is set by Heroku

Make sure that you’re logged in to Heroku (`heroku login`) and then login to the Container Registry by running `heroku container:login`. Run the following commands:
- `heroku apps:create heart-disease-pred-z` - create app with name heart-disease-pred-z (choose any)
- `heroku git:remote -a heart-disease-pred-z` - (optional) in case the app not found
- `heroku container:push web` - build the image and push to Container Registry
- `heroku container:release web` - release the image to your app
- `heroku open` - (optional) open app in the browser

Public endpoint to test: `https://heart-disease-pred-z.herokuapp.com/predict`. Please run the command `python predict-test-cloud.py` to test the model prediction. Based on health data provided in that file you should get the following result:
```
{'disease_probability': 0.8, 'risk': True}
The person with provided health parameters has 10-year risk of future coronary heart disease
```

**Be aware that it might take some time (couple of minutes) for the app to respond because it might require to launch the app on Heroku platform.**

## Deployment to the Cloud: AWS Elastic Beanstalk (Attempt)
*It is assumed that you already have AWS account and assinged IAM user. `Dockerfile` and `entrypoint.sh` files are used as in Containerization section*

It is required to install `awsebcli` in the current active environment to deploy the model to the AWS cloud. It could be done with the following command: `conda install -c conda-forge awsebcli`. 

Create an application: `eb init -p docker -r eu-west-1 heart-disease-pred`.

Test EB locally: `eb local run --port 9696` and `python predict-test.py`.

Create an environment in the cloud: `eb create heart-disease-pred-env`. During execution of this command I experienced the issue of creating image from my Dockerfile which could be associated with the way how conda activates environment inside docker container and how this process interacts with Elastic Beanstalk internal processes. The decision I made is to make it as an deployment attempt and proceed with deployment on Heroku (explained above).

