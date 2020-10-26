__author__ = 'shivendra'
from flask import Flask, make_response, request
import io
import csv
import pandas as pd
import shutil
from zipfile import ZipFile
import time

reportdate = time.strftime('%Y-%m-%d')


app = Flask(__name__)

def transform(text_file_contents):
    print(text_file_contents) 
    return text_file_contents.replace("DEV", "DOVE")


@app.route('/')
def form():
    return """
        <html>
            <body>
                <h1>Process Deviations</h1>

                <form action="/transform" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" />
                    <input type="submit" />
                </form>
            </body>
        </html>
    """

@app.route('/transform', methods=["POST"])
def transform_view():
    f = request.files['data_file']
    outfile = reportdate + '_' + f.filename
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    upload_report = csv.reader(stream)
    #print("file contents: ", file_contents)
    #print(type(file_contents))
    #print(upload_report)
    for row in upload_report:
        print(row)

    stream.seek(0)
    result = transform(stream.read())
    

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=" + outfile
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
