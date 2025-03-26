
import os
from flask import Flask, send_from_directory, request
from flask_cors import CORS
import whisper
import psycopg2

model = whisper.load_model('medium')
app = Flask(__name__)
CORS(app)

# HTML file
@app.get('/')
def index():
  return send_from_directory('static', 'index.html')

# Get static files such as css and javascript.
@app.get('/<path:filename>')
def static_files(filename):
  return send_from_directory('static', filename)

# Endpoint for send audio file.
@app.post('/transcription')
def audio():
  file_name = 'audio.ogg'
  data = request.files['audio']
  data.save(file_name)
  result = model.transcribe(file_name)
  os.remove(file_name)
  return result["text"]

# Data save to database or files.
@app.post('/store')
def store():
  data = request.get_json()

  if data['type'] == 'file':
    # save to file
    with open(data['filename'], 'w') as writer:
      writer.write(data['text'])

  else:
    # save to database
    # Attension connect info set to .env for product.
    connection = psycopg2.connect("host=localhost dbname=postgres user=postgres password=pass")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO transcription(text) VALUES (%s)", (data['text'],))
    connection.commit()
    cursor.close()
    connection.close()

  return { "result": "ok" }

# Entry Point
if __name__ == '__main__':
  print("Start web server")
  app.run()