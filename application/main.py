from sklearn.svm import SVC 
from sklearn.metrics import classification_report
import pandas as pd 
import numpy as np 
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from pathlib import Path 

caminho = Path(Path.home(), "Documentos/healthcare_ML/")
dataset = pd.read_csv(f"{caminho}/dataset_healthcare/healthcare_dataset.csv")
dataset['Gender'] = (dataset["Gender"] == "Female").astype(int)

label_sangue = {"O-": 0.00, "O+": 1.00, "B-": 2.00, "AB+": 3.00, "A+":4.00, "AB-": 5.00, "A-": 6.00, "B+": 7.00}
label_medical = {'Diabetes': 0,  'Asthma': 1,  'Obesity': 2, 'Arthritis': 3, 'Hypertension':4, 'Cancer': 5}
label_insurance = {'Medicare': 0, 'UnitedHealthcare': 1, 'Aetna': 2, 'Cigna': 3, 'Blue Cross': 4}
label_medication = {'Aspirin': 0, 'Lipitor': 1, 'Penicillin': 2, 'Paracetamol': 3, 'Ibuprofen': 4}
label_results = {'Inconclusive': 0,  'Normal': 1, 'Abnormal': 2}
label_admission = {'Elective': 0, 'Emergency': 1, 'Urgent': 2}

dataset["Name"], _ = pd.factorize(dataset["Name"])
dataset["Doctor"], _ = pd.factorize(dataset["Doctor"])
dataset["Hospital"], _ = pd.factorize(dataset["Hospital"])
dataset["Admission Type"] = dataset["Admission Type"].replace(label_admission)
dataset["Discharge Date"] = pd.to_numeric(dataset["Discharge Date"].str.replace("-", ""))
dataset["Date of Admission"] = pd.to_numeric(dataset["Date of Admission"].str.replace("-", ""))
dataset["Test Results"] = dataset["Test Results"].replace(label_results)
dataset["Medication"] = dataset["Medication"].replace(label_medication)
dataset["Insurance Provider"] = dataset["Insurance Provider"].replace(label_insurance)
dataset["Medical Condition"] = dataset["Medical Condition"].replace(label_medical)
dataset["Blood Type"] = dataset["Blood Type"].replace(label_sangue)

def padronizacao(data, over=False):
    X = data[data.columns[:-1]].values
    y = data[data.columns[-1]].values
    escala = StandardScaler()
    X = escala.fit_transform(X)

    if over:
        ros = RandomOverSampler()
        X, y = ros.fit_resample(X, y)
    
    data = np.hstack((X, np.reshape(y, (-1, 1))))

    return data, X, y 

train, X_train, y_train = padronizacao(dataset, over=True)
test, X_test, y_test = padronizacao(dataset, over=False)

svm_model = SVC(C=100)
svm_model.fit(X_train, y_train)
y_pred = svm_model.predict(X_test)

print(classification_report(y_test, y_pred))





