from flask import Flask, render_template, request, jsonify
import json
from main_engine import ExternalModuleEngine
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
core_engine = ExternalModuleEngine()


@app.route('/external_module_engine', methods=['GET','POST'])
def process_external_module_request():
    if request.method == 'GET':
        command = decode_get_request()
    elif request.method == 'POST':
        command = decode_post_request()
    else:
        command = {}

    try:
        result = core_engine.process_command(command)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status':0, 'info':'process {} error, exception is :{}'.format(json.dumps(command), str(e))})


def index():
    return render_template('test.html')


def decode_get_request():
    result = {}
    for arg in request.args:
        result[arg.lower()] = request.args[arg]

    return result


def decode_post_request():
    result = {}
    for arg in request.form:
        result[arg.lower()] = request.form[arg]

    if result == {}:
        try:
            for arg in request.json:
                result[arg.lower()] = request.json[arg]
        except:
            pass
    return result


if __name__ == '__main__':
    app.run(debug=True)