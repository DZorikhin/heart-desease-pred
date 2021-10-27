import requests

host = 'https://heart-disease-pred-z.herokuapp.com/'
url = f'{host}/predict'

parameters = {
    "age": 45,
    "cigsPerDay": 20,
    "totChol": 250,
    "sysBP": 250,
    "BMI": 25,
    "heartRate": 65,
    "glucose": 100,
    "male": 1,
    "currentSmoker": 1,
    "BPMeds": 1,
    "prevalentStroke": 0,
    "prevalentHyp": 1,
    "diabetes": 0
}

response = requests.post(url, json=parameters).json()
print(response)

if response['risk'] == True:
    print('The person with provided health parameters has 10-year risk of future coronary heart disease')
else:
    print('The person with provided health parameters has NO 10-year risk of future coronary heart disease')