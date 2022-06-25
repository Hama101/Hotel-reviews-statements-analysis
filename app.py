from flask import *
from flask_cors import CORS
# from model import load_model 
import model as m
from analyser import analyse


model = m.load_model()
print("model loaded : ", model)
print("\n running the server")

def create_app(register_stuffs=True):
    app = Flask(__name__)
    CORS(app)  # This makes the CORS feature cover all routes in the app
    return app


app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyse-text' , methods=['POST','GET'])
def home():
    if request.method == 'POST':
        text = request.form['text'] or request.get_json()['text']
        #return fromatted json
        return jsonify(analyse(text, model))

    if request.method == 'GET':
        return {
            "error" : "Not allowed method!"
        }



if __name__ == '__main__':
    app.run(debug=True , threaded=True)