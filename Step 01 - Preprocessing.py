import pandas as pd
import csv


def CreateCSV(filePath, fieldnames):
    with open(filePath, mode="w", encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

def UpdateCSV(csvPath, write):
    with open(csvPath, mode="a", encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(write)

directory = r"/home/eloisa.oliveira/Downloads/TestRS/Preprocessed/"
csvSource = r"/home/eloisa.oliveira/Downloads/TestRS/Data/allData.csv"
df = pd.read_csv(csvSource)

csvName = "preprocessedData.csv"
csvNameInvalid = "preprocessedData_SeparatingInvalid.csv"
csvNameRole = "preprocessedData_SeparatingRoles.csv"

printFormatLine = 60


print(f"Dataset: {len(df)}")

### Remove empty columns
print("\nColumns only with 0 values:")

print("-"*printFormatLine)

for key in df.keys():
    if (df[key] == 0).all():
        print(f"Drop: {key}")
        df = df.drop(key,axis = 1)   
        
print("-"*printFormatLine)

print(f"\nWithout empty columns: {len(df.keys())}")
###

### Remove matches of type ARAM
matchesToRemove_ARAM = "ARAM"
columnToRemoveInfo = "gameMode"

df = df[df[columnToRemoveInfo] != matchesToRemove_ARAM]

print(f"\nWithout matches ARAM: {len(df)}")
###

### Remove matches that lasted less than 600 seconds
matchesToRemove_TIME = 600
columnToRemoveInfo = "gameDuration"

df = df[df[columnToRemoveInfo] > matchesToRemove_TIME]

print(f"\nWithout matches 600s or less: {len(df)}")
###

### Remove duplicated data 
summonerName = "summonerName"
matchId = "matchId"

df = df.drop_duplicates(subset = [summonerName,matchId])

print(f"\nWithout duplicates: {len(df)}")
###

### Remove matches of type COOP vs BOT
print("\nMatches COOP vs BOT:")

print("-"*printFormatLine)

matchesCount = df[matchId].value_counts()
matchesBot = []

for match, count in matchesCount.items():
    if count > 10 or count < 10:
        print(f"MatchId: {match}, Count: {count}")
        matchesBot.append(match)
        
countData = df[matchId].value_counts()
countMatches = pd.DataFrame({matchId: countData.index,"Count": countData.values})

matchesBotToRemove = countMatches[countMatches["Count"] < 10][matchId]

df = df[~df[matchId].isin(matchesBotToRemove)]

print("-"*printFormatLine)

print(f"\nWithout bot matches: {len(df)}\n")
###

dfFieldnames = []

for key in df.keys():
    dfFieldnames.append(key)

CreateCSV(directory + csvName, dfFieldnames)
CreateCSV(directory + csvNameRole, dfFieldnames)
CreateCSV(directory + csvNameInvalid, dfFieldnames)

individualPosition = "individualPosition"

for i in range(len(df)):
    row = df.iloc[i]  
    
    # All data preprocessed
    UpdateCSV(directory + csvName, row.tolist())
    
    # Separates data in two files 
    # Invalid when the values from individualPosition column are not specified 
    # Roles when the values from individualPosition column are specified 
    if row[individualPosition] == "Invalid":
        UpdateCSV(directory + csvNameInvalid, row.tolist())
    else:
        UpdateCSV(directory + csvNameRole, row.tolist())

print("-"*printFormatLine) 
print(df[individualPosition].value_counts())
print("-"*printFormatLine)
                