from flask import Flask

app = Flask(__name__) # create instance of Flask

@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__': # if this is run directly without import in another 
    app.run(port=5000,debug=True)