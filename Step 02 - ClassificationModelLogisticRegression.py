import os
import csv
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report,f1_score

def CreateCSV(filePath,fieldnames):
    with open(filePath, mode="w",encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
def UpdateCSV(csvPath,write):
    with open(csvPath, mode="a",encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(write)

def ClassificationModel(name,classificationModel,trainX,trainY,testX,testY):
    model = classificationModel
    model.fit(trainX,trainY)
    predictionY = model.predict(testX)
    
    accuracy = accuracy_score(testY,predictionY)
    print(f"\n\n{name} Accuracy: {accuracy}")
    
    f1 = f1_score(testY,predictionY,average = "macro")
    print(f"\n{name} F1 Score: {f1}")
    
    print(f"Classification:\n{classification_report(testY,predictionY)}")
    return model


csvName = "classifiedDataWithlogisticRegression.csv"

directory = r"path = where you want to save your classified data (add / at the end of the path)"
# Exemple: 
# directory = r"/home/eloisa.oliveira/Área de Trabalho/Classification/"

sourceTrain = r"path = .csv file where you saved the data with inidividualPosition specified"
# Exemple:
# sourceTrain = r"/home/eloisa.oliveira/Área de Trabalho/Preprocessing/preprocessedData_SeparatingRoles.csv"
sourceTest = r"path = .csv file where you saved the data with inidividualPosition not specified"
# Exemple:
# sourceTest = r"/home/eloisa.oliveira/Área de Trabalho/Preprocessing/preprocessedData_SeparatingInvalid.csv"

dataTrain = pd.read_csv(sourceTrain)

championName = "championName"
win = "win"
matchId = "matchId"
individualPosition = "individualPosition"

# All columns with string values 
# To remove for classification
columnsStr = ["puuid","accountId","matchId","gameCreation","gameDuration","gameStartTimestamp",
              "gameEndTimestamp","gameEndTimestampToDate","gameMode","gameType","platformId",
              "championName","gameEndedInEarlySurrender","gameEndedInSurrender","lane",
              "role","summonerName","teamPosition","win"]


### Train model phase
trainX = dataTrain.drop([individualPosition] + columnsStr,axis = 1)
trainY = dataTrain[individualPosition]

scaler = StandardScaler()

trainX = scaler.fit_transform(trainX)

trainX,testX,trainY,testY = train_test_split(trainX,trainY,test_size = 0.2,random_state = 42)

logisticRegression = ClassificationModel("Logistic Regression",LogisticRegression(),trainX,trainY,testX,testY)
###

### Test model phase
dataTest = pd.read_csv(sourceTest)

testX = dataTest.drop([individualPosition] + columnsStr, axis = 1)
testY = logisticRegression.predict(testX)

dataTest[individualPosition] = testY
### 

printFormatLine = 60
print("-" * printFormatLine)
print("Predicting individualPosition:\n")
print(len(dataTest[individualPosition]))
print("\n")
print(dataTest[individualPosition])

dataTest.to_csv(os.path.join(directory,csvName),index = False)

