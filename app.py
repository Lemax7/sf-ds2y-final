import json

from flask import Flask, request

from predictions import check_visitor, predict


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        params = request.args
        if not len(params):
            return 'No input data'
        else:
            visitorid = request.args.get("visitorid")
            if visitorid is None:
                return "incorrect query parameter. Correct is '/?visitorid=...'"
            if not visitorid.isnumeric():
                return 'Incorrect visitorid. Numeric only!'
            visitorid = int(visitorid)
            if visitorid is None:
                return "No visitorid input data"
            
            if not check_visitor(visitorid):
                return "Wrong visitorid!"
            
            
            recommendations = predict(visitorid)
            recommendations = [str(rec) for rec in recommendations]
            recommendations_str = ", ".join(recommendations)
            
            response = f"""
            visitorid is {visitorid}, recommended itemids: {(recommendations_str)}
            """
            return response
    else:
        return "<h1>No data in GET request</h1>"
    
@app.route('/recomm/', methods=['GET'])
def recomm():  
    if request.method == 'GET':
        params = request.args
        if not len(params):
            return []
        else:
            visitorid = request.args.get("visitorid")
            if visitorid is None or not visitorid.isnumeric():
                return []
            visitorid = int(visitorid)
            if visitorid is None:
                return []
            if not check_visitor(visitorid):
                return []
            recommendations = [int(rec) for rec in predict(visitorid)]
            recomm_json = {"recommendations": recommendations}
            return json.dumps(recomm_json)
    else:
        return []


if __name__ == "__main__":
    app.run('localhost', debug=False)
