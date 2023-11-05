import os
from flask import Flask, request, render_template, jsonify, send_from_directory
from dotenv import load_dotenv

from inference import infer
from bravediscussionfetcher import fetchDiscussionPosts

load_dotenv()
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
mongodb_db_password = os.getenv('MONGO_DB_PASSWORD')
brave_api_key = os.getenv('BRAVE_API_KEY')

app = Flask(__name__, template_folder="templates")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/infer", methods=['POST'])
def infer_from_claude():
    data = request.json
    discussionData = fetchDiscussionPosts(data['message'])
    response = infer(data['message'], anthropic_api_key, mongodb_db_password)
    return jsonify(data=response, discussionData=discussionData)


# Comment this line before deploying
app.run(debug=True)