import os
import subprocess

from flask import Flask, request

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ.get('FLASK_SECRET', '+%+3Q23!zbc+!Dd@')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


@app.route('/', methods=["POST"])
def start_delirium():
    json = request.get_json() or {}
    text = json.get('text', "L'exemple par défaut est")
    model = json.get('model', 'flaubert-base-cased')
    length = json.get('length', 20)
    temperature = json.get('temperature', 0.1)
    repetition_penalty = json.get('repetition_penalty', 2)

    SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
    command = f'''python {SCRIPT_DIR}/run_generation.py \
    --model_type="{model}" \
    --length={length} \
    --model_name_or_path="{model}" \
    --temperature={temperature} \
    --repetition_penalty={repetition_penalty} \
    --prompt "{text}"'''
    result = subprocess.check_output(command, shell=True)
    return result, 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, use_reloader=True)
