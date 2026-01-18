import json

def getScore(offset, limit) :
    with open("leadersTable.json", "r", encoding="utf-8") as f:
        scoreList = json.load(f)
    print(scoreList[offset : offset + limit])
    
getScore(0, 10)