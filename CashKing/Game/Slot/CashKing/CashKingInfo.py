'''
SymbolIDMap = {
    0: "",
    2: "Bonus",
    3: "Multi (Max)",
    4: "Multi (2nd)",
    5: "Multi (3rd)",
    6: "Multi (4th)",
    7: "Multi (5th)",
    10: "0",
    20: "00",
    30: "000",
    101: "1",
    105: "5",
    11: "1",
    12: "2",
    15: "5",
    21: "10",
    25: "50",
    31: "100",
}
'''

def reelWeightDataTransform(reelData):
    result = []
    for i in range(0, len(reelData), 2):
        export_reel_data = reelData[i]
        if type(reelData[i]) in [tuple, list]:
            export_reel_data = ",".join([str(x) for x in reelData[i]])
        result.append({"Result": export_reel_data, "Weight":reelData[i+1]})
    return result


GameInfo = [
{
    "game_id": "CashKing",
    "game_name": "CashKing",
    "chance_version": "Macross_v5(1)_20241219",
    "ProbId": "1",
    "base_game_rate": 9800,
    "main_reels": {
        "100": {
            "0":[2,4,99,6,6,3,7,1,3,3,5,2,3,3,4,1,6,4,7,5,3,3,2,99,3,7,2,6,6,1,1,3,7,99,2,5,5,7,3,6,1,1,7,2,6,3,1,1,5,7,7,1,3,3,1,1,2,3,3,7,4,1,4,6,6,6,4,1,4,3,3,1,1,3,1,99,6,7,4,5,4,1,1,1,2,2,6,7,5,2,5,3,6,99,4,1,5,3,3,3,1,7,6,5,1,4,3,2,4,4,4,7,4,5,5,3,4,99,5,6,7,7,3,6,7,6,1,1,4,4,4,5,2,5,6,99,7,5,1,1,1,2,7,4,2,3,6,1,3,4],
            "1":[2,2,5,3,2,2,2,5,5,5,6,7,5,4,2,2,3,7,1,4,7,6,3,3,4,4,4,6,7,5,5,99,2,4,4,1,1,1,4,4,7,6,6,6,1,1,1,3,5,4,4,3,3,3,2,3,6,7,7,1,1,2,7,7,4,3,3,5,2,7,2,3,3,3,2,4,6,2,4,6,5,5,1,7,7,2,3,7,6,2,2,1,1,1,5,1,2,99,2,2,5,5,2,2,2,4,4,7,5,2,7,5,7,7,1,1,7,7,4,3,7,6,5,4,1,6,2,7,4,1,1,2,7,1,6,2,2,6,2,4,6,99,4,2,2,2,5,1,2,7],
            "2":[1,1,1,7,7,4,6,3,6,6,3,5,99,2,2,7,5,3,2,1,7,6,3,1,2,6,5,3,7,99,1,1,1,5,7,3,6,3,2,4,1,1,99,3,7,3,3,7,3,3,1,2,5,3,3,2,1,1,1,2,2,1,4,1,4,5,3,3,2,2,2,3,3,7,5,5,4,1,5,4,99,4,3,6,6,6,2,4,7,2,99,2,5,2,3,3,1,1,4,6,2,2,2,5,1,1,1,4,2,3,7,5,3,5,3,3,2,5,4,3,3,3,6,5,7,6,4,2,5,99,3,3,1,1,3,7,1,6,5,3,3,3,7,5,7,4,7,5,99,3],
            "3":[2,4,2,7,5,6,3,3,2,2,99,2,2,3,4,6,4,1,7,3,3,4,7,6,1,1,1,6,3,6,99,2,2,6,3,4,2,3,7,1,4,1,5,5,7,1,1,5,5,2,99,3,2,7,1,5,1,4,7,2,6,1,7,3,3,3,4,1,2,1,4,99,5,1,3,1,1,4,4,4,6,5,4,2,2,2,3,3,4,3,1,3,7,6,2,1,99,3,7,2,6,7,6,2,2,6,6,99,7,7,4,4,4,6,6,2,3,3,4,1,1,5,4,7,7,7,4,7,99,3,2,7,3,7,1,6,2,99,2,1,3,4,2,2,5,5,5,7,7,7],
            "4":[99,4,6,2,4,6,5,5,5,2,4,99,2,7,1,2,3,5,4,4,1,1,3,5,1,1,2,2,1,1,6,1,7,5,99,4,1,3,6,6,6,4,5,4,2,2,7,4,4,5,5,3,6,99,2,2,2,5,4,2,5,5,2,2,7,6,7,3,3,2,1,3,6,6,1,99,5,4,3,4,3,3,2,2,3,5,4,7,6,1,2,3,5,6,6,1,1,5,99,4,3,7,4,7,5,2,2,2,1,4,7,2,6,1,4,5,2,1,1,4,7,1,5,1,4,4,5,1,1,6,99,4,6,4,4,1,2,3,5,6,99,2,5,2,5,3,7,7,5,6],
            "5":[4,5,2,99,7,3,3,3,6,2,4,4,4,7,7,3,1,6,3,2,2,5,4,6,6,1,5,5,5,1,1,3,3,6,2,5,1,3,3,1,4,7,6,2,3,3,99,1,3,1,1,1,5,7,3,2,99,5,4,7,6,2,3,4,5,2,5,7,7,7,6,2,7,7,2,4,6,2,1,3,2,3,6,6,1,2,1,7,4,7,5,1,7,3,99,2,7,4,3,6,3,2,3,5,7,7,7,2,6,6,2,1,2,3,3,3,7,7,5,1,2,6,2,3,1,4,7,5,3,3,7,1,1,99,3,4,3,2,5,2,2,6,3,3,7,7,7,5,4,2],
            "6":[5,2,3,3,99,3,3,3,6,3,6,3,6,5,7,2,2,1,4,4,6,1,1,7,4,6,1,3,1,6,5,1,1,7,2,99,7,1,3,4,6,4,4,3,6,1,2,1,1,2,5,99,5,5,5,4,7,4,1,4,3,5,5,1,5,3,3,7,3,5,5,1,1,2,7,3,3,5,99,1,2,2,2,4,7,3,1,5,5,99,3,4,7,2,7,7,3,2,2,1,1,5,2,1,5,7,3,7,3,7,99,5,7,4,4,5,5,6,1,1,1,3,3,2,2,2,7,3,4,5,5,3,6,3,7,99,6,4,3,2,2,5,6,1,7,6,1,7,7,7]
             },
        "500": 2,
        "1000": 3,
    },
    "fever_reels": {
        "0": {}},
    "extra_odds": {
        "Ratio": 1,
        "base_trigger_scatter":[0.5,0.2,0.1,0.05,0.01,0,0,0],
        "Bonus": {
            "100": {
                "Odds": [5,5,5,10,10,10,25,50,100,200,300,500],
                "Weight": [300,300,300,380,380,380,220,50,8,4,3,2]
            },
            "500": {
                "Odds": [5,5,5,10,10,10,25,50,100,200,500,1000],
                "Weight": [300,300,300,380,380,380,220,50,8,4,3,2]
            },
            "1000": {
                "Odds": [5,5,5,10,10,10,25,50,100,500,1000,2000],
                "Weight": [700,700,700,800,800,800,500,100,30,8,5,3]
            },
            "5000": {
                "Odds": [5,5,5,10,10,10,25,50,100,500,1000,3000],
                "Weight": [700,700,700,800,800,800,500,120,50,8,5,2]
            },
            "10000": {
                "Odds": [5,5,5,10,10,10,25,50,100,500,1000,5000],
                "Weight": [700,700,700,800,800,800,500,120,50,8,5,2]
            },
        },
        "FakeReelWeight": {
            "100":{
                "0": reelWeightDataTransform([
                    11, 2,
                    15, 2,
                    21, 1,
                    25, 0,
                ]),
                "1": reelWeightDataTransform([
                    10, 2,
                    20, 1,
                    11, 2,
                    15, 2,
                    21, 1,
                    25, 0,
                ]),
                "2": reelWeightDataTransform([
                    10, 2,
                    20, 0,
                    11, 2,
                    15, 1,
                ]),
                "3": reelWeightDataTransform([
                    3, 0,
                    4, 0,
                    5, 1,
                    6, 2,
                    7, 5,
                    2, 3,
                ])
            },
        }
    },
},
]

if __name__ == "__main__":
    import json
    print(json.dumps(GameInfo, indent=4))
