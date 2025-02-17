from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/getcode', methods=['GET'])
def get_code():
    return jsonify({"code": "45678"})


@app.route('/plus/<a>/<b>', methods=['GET'])
def plus(a, b):
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return jsonify(error="Invalid input"), 400    
    result = round(a + b, 2) 
    if result.is_integer():
        result = int(result)

    return jsonify(result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # i just want to trigger pulling scm lol
