from flask import Flask
import os
import time

#PORT = os.environ.get('PORT')
#name = os.environ.get('NAME')
#if name == None or len(name) == 0:
#  name = "world"

#if PORT == None or len(PORT) == 0:
#  PORT = 5000
PORT = 80
MESSAGE = "\nFrontend Server - Port:" + str(PORT)
print("Message: '" + MESSAGE + "'")

app = Flask(__name__)


@app.route("/")
def root():
  print("Handling web request. Returning message.")
  result = MESSAGE + "\nMy Flask Application"
  result = result.encode("utf-8")
  return result


if __name__ == "__main__":
  print('Preparing to sleep for 5 minutes')
  #time.sleep(305)
  app.run(debug=True, host="0.0.0.0", port=PORT)