from flask import Flask, request, json

app = Flask("Indiana-FingerTip")


@app.route('/', methods=['POST'])
def post_location():
    #json {MAC:mac, x:x, y:y, z:z} w responsie błąd obliczeń silnika: {engineError: odlegloscOdPunktuWgEngina, engineLocation:{x:x, y:y, z:z}}
    print(json.dumps(request.json))
    return "ok"

if __name__ == "__main__":
    app.run()