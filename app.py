import json
import os
import pypdftk
from flask import (
    Flask,
    make_response,
    send_file,
    request,
    abort,
    Response,
    jsonify
)
from functools import wraps


"""
Alters the `PATH` and `LD_LIBRARY_PATH` environment variables to let the system know where 
to find the binary and the GCJ dependency.
"""
if os.environ.get("AWS_EXECUTION_ENV") is not None:
    os.environ['PATH'] = os.environ.get('PATH') + ':' + os.environ.get('LAMBDA_TASK_ROOT') + '/bin'
    os.environ['LD_LIBRARY_PATH'] = os.environ.get('LAMBDA_TASK_ROOT') + '/bin'

# Configuration
app = Flask(__name__)

DEBUG = False
HOST = '0.0.0.0'
PORT = 5000
PDF_FOLDER = "pdf"

def get_supported_pdf_templates(path=PDF_FOLDER):
    supported_pdf = []
    for _, _, files in os.walk(PDF_FOLDER):  
        for filename in files:
            if filename[-4:] == ".pdf":
                supported_pdf.append(filename[:-4])
    return supported_pdf

SUPPORTED_PDF_FILES = get_supported_pdf_templates()


def check_supported_pdfnames(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.view_args['pdfname'] not in SUPPORTED_PDF_FILES:
            abort(500, "Not supported PDF name")
        return f(*args, **kwargs)
    return wrapper

@app.route('/pdf/<pdfname>', methods=['POST'])
@check_supported_pdfnames
def generate_filled_pdf(pdfname):
    """
    Generates filled PDF file.
    
    POST: /pdf/<pdfname>
    :body - data to be insered in PDF file (JSON).
    """
    r_json = request.get_json()
    if r_json is None:
        return abort(500, "Error in JSON body.")

    pdfFilePath = pypdftk.fill_form("{folder}/{file}.pdf".format(folder=PDF_FOLDER, file=pdfname), r_json)

    return send_file(pdfFilePath, attachment_filename='out.pdf')

@app.route('/pdf/<pdfname>')
@check_supported_pdfnames
def get_dump_data_fields(pdfname):
    """
    Get dumped fields for specified pdfname. Can be formatted.

    GET: /pdf/<pdfname>?format={pairs,keys}
    :pairs - list of pairs (key: value) for dumped data fields
    :keys - only dumped field names
    """
    data = pypdftk.dump_data_fields("{folder}/{file}.pdf".format(folder=PDF_FOLDER, file=pdfname))
    
    formated = request.args.get('format')
    if "pairs" == formated:
        data = format_fields_by_pairs(data)
    elif "keys" == formated:
        data = format_fields_by_keys(data)

    return jsonify(data)

@app.route('/pdf/')
def get_supported_pdfs():
    return jsonify(SUPPORTED_PDF_FILES)


def format_fields_by_pairs(dump_data_fields=[]):
    return [{field['FieldName']: field['FieldValue']} for field in dump_data_fields]

def format_fields_by_keys(dump_data_fields=[]):
    return [field['FieldName'] for field in dump_data_fields]

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)