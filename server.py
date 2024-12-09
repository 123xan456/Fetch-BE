import pandas as pd
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
datafile = "points_sheet.csv"
df = pd.read_csv(datafile)

class Add(Resource):
    """
    Adds new point transaction
    """
    def post(self):
        try:
            global df
            data = request.get_json()
            data = {
                "payer": [data["payer"]],
                "points": [data["points"]],
                "timestamp": [data["timestamp"]]
            }
            data = pd.DataFrame(data)
            
            df = pd.concat([df, data], ignore_index=True)      
            df.to_csv(datafile, index = False)
            return 200            
        
        except Exception as e:
            return {'error': str(e)}, 400
    
class Spend(Resource):
    """
    Deducts points from user 
    """
    def post(self):
        try:
            global df
            data = request.get_json()
            df_sort = df.sort_values(by='timestamp')
            
            payers = {}
            spend_amount = data["points"]
            for record in df_sort.itertuples():
                #get amount to deduct
                payer_amount = int(record.points)
                amount = min(payer_amount, spend_amount)
                spend_amount -= amount
                
                payers[record.payer] = payers.get(record.payer, 0) - amount
                df_sort.at[record.Index, 'points'] -= amount 
                
                if spend_amount == 0: #done spending
                    res = [{"payer": key, "points": val} for key,val in payers.items()]
                    df = df_sort
                    df_sort.to_csv(datafile, index=False)
                    return res, 200
                
            #if reached here, not enough points 
            return {'error': "You don't have enough points!"}, 400
                        
        except Exception as e:
            return {'error': str(e)}, 400            

class Balance(Resource):
    """
    Returns payers and balance points
    """
    def get(self):   
        try:
            global df       
            res = {}
            for record in df.itertuples():
                res[record.payer] = res.get(record.payer, 0) + record.points
            return res, 200
    
        except Exception as e:
            return {'error': str(e)}, 400
    
class Clear(Resource):
    """
    Clears CSV of all point transactions
    """
    def get(self):
        try:
            global df 
            df = df.iloc[0:0]
            df.to_csv(datafile, index=False)
            
            return 200
        except Exception as e:
            return {'error': str(e)}, 400
    
# attach resource to URL path
api.add_resource(Add, '/add') 
api.add_resource(Spend, '/spend') 
api.add_resource(Balance, '/balance') 
api.add_resource(Clear, '/clear') 

if __name__ == '__main__': 
    app.run(host = "localhost", port = 8000) 
