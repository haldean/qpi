from flask import Flask
from flask import render_template

app = Flask('qpi')

@app.route('/')
def main():
  return render_template('main.html')

def run_server():
  app.run(debug=True)

if __name__ == '__main__':
  run_server()
