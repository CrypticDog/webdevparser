__author__ = 'pvtcompyle'
from flask import Flask, make_response, request, send_file
import io
import csv
import pandas as pd
import numpy as np
import shutil
from zipfile import ZipFile
import time
from io import BytesIO

reportdate = time.strftime('%Y-%m-%d')


app = Flask(__name__)

def transform(text_file_contents):
    print(text_file_contents) 
    return text_file_contents.replace("d2020", "DEV2020")

def getEmplList(df):
    employees = df['EmployeesInvolved'].unique()
    employeelist = []

    for e in employees:
        empline = e.splitlines()
        for l in empline:
            if len(l)>0:
                employeelist.append(l.upper())
    employeelist.sort()
    employeelist = np.array(employeelist)
    employeelist = np.unique(employeelist)
    return(employeelist)

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

    # Check for upload file
    if not f:
        return "No file"
    if '.csv' in f.filename:
        outfile = reportdate + '_' + f.filename[:-4] + '.xlsx'
    else:
        return "Selected file is not a csv, please check your file and try again"    

    # Convert uploaded file from stream to dataframe
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    
    # Prep stream for writing to dataframe
    stream.seek(0)
    
    # Write stream to dataframe
    df = pd.read_csv(stream)

    # Populate array with list of unique employee names from input file
    employeelist = getEmplList(df)

    # Setup excel file for input    
    outputStream = BytesIO()
    writer = pd.ExcelWriter(outputStream, engine='xlsxwriter')
    
    # Create summary array
    EmployeeSummary = []
    for e in employeelist:
        employeeresult = df[df['EmployeesInvolved'].str.contains(e, case=False)]
        dev_count = len(employeeresult)
        EmployeeSummary.append([e, dev_count])
    
    # Convert summary array to dataframe
    SummaryResult = pd.DataFrame(EmployeeSummary)
    
    # Write summary to summary tab in excel file
    dropList = ["Employee", "Dev Count"]
    SummaryResult.to_excel(writer, sheet_name='Summary', index=False)

    # Write employee specific tabs and data to excel file
    dropList = ["Center", "DaysOpen", "Status", "DateClosed", "RootCause", "AssociatedDeviationCAPANumber"]
    for e in employeelist:
        listResult = df[df['EmployeesInvolved'].str.contains(e,case= False)]
        listResult = listResult.drop(dropList, axis=1)
        listResult.to_excel(writer, sheet_name=e, index=False)
    
    # Close excel file and prepare to send file back to user
    writer.close()
    outputStream.seek(0)

    # Return processed file to user
    return send_file(outputStream, attachment_filename=outfile, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
