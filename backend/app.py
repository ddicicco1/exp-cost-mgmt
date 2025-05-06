from flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef hello():\n    return 'Hello, ECM!'\n\nif __name__ == '__main__':\n    app.run(debug=True, host='0.0.0.0')\n
