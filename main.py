from flask import Flask, redirect, render_template, request
from pysondb import db


app = Flask(__name__)

scores = db.getDb("scores.json")

# {
#     "name": "John",
#     "pr": 19,
#     "pr-date": "24-11-2024"
#     "runs": [
#               {"score":19, "date":"24-11-2024"},
#               {"score":10, "date":"21-11-2024"}
#           ]
# }

def prs():
    data = scores.getAll()

    prs = []
    for i in data:
        prs.append({"name": i["name"], "pr": i["pr"], "date": i["pr-date"]})

    prs.sort(key=lambda x: x["pr"], reverse=True)
    return prs
    


@app.route('/')
def home():

    prs_data = prs()
    print(prs_data)

    return render_template('main.html', prs=prs_data)


@app.route('/api/names')
def names():
    data = scores.getAll()

    names = []
    for i in data:
        names.append(i["name"])

    return names

# Add a new score (Post request)
@app.route('/api/score', methods=['POST'])
def add_score():
    data = request.get_json()
    name = data["name"]
    score = data["score"]
    date = data["date"]

    data = scores.getByQuery({"name": name})

    if data:
        data[0]["runs"].append({"score": int(score), "date": date})
        if int(score) > data[0]["pr"]:
            data[0]["pr"] = int(score)
            data[0]["pr-date"] = date

        scores.updateByQuery({"name": name}, data[0])
        return redirect('/')


    scores.add({"name": name, "pr": int(score), "pr-date": date, "runs": [{"score": int(score), "date": date}]})

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
