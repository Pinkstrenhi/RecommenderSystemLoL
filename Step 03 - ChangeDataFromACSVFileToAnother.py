import pandas as pd 

csvName = "finalData.csv"

directory = r"path = where you want to save your recommended data (add / at the end of the path)"
# Exemple: 
# directory = r"/home/eloisa.oliveira/Área de Trabalho/Data/"

sourceToChange = r"path = .csv file where you saved the preprocessed data"
# Exemple:
# sourceTrain = r"/home/eloisa.oliveira/Área de Trabalho/Preprocessing/preprocessedData.csv"
sourceChanger = r"path = .csv file where you saved the data with inidividualPosition classified"
# Exemple:
# sourceTest = r"/home/eloisa.oliveira/Área de Trabalho/Classification/classifiedDataWithlogisticRegression.csv"

dataToChange = pd.read_csv(sourceToChange)
dataChanger = pd.read_csv(sourceChanger)

matchId = "matchId"
individualPosition = "individualPosition"
summonerName = "summonerName"

for index,row in dataToChange.iterrows():
    rowMatchId = row[matchId]
    rowSummonerName = row[summonerName]
    
    # Finds the data with the same matchId and summonerName
    rowFilter = (dataChanger[matchId] == rowMatchId) & (dataChanger[summonerName] == rowSummonerName)
    
    if not rowFilter.empty:
        rowIndividualPosition = dataChanger.loc[rowFilter,individualPosition].values
        if len(rowIndividualPosition) > 0:
            dataToChange.at[index,individualPosition] = rowIndividualPosition[0]
        

dataToChange.to_csv(directory + csvName,index = False)

        

