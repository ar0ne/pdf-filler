import json
import pypdftk
from flask import (
    Flask, make_response,
    send_file, request, abort, 
    Response, jsonify)
from functools import wraps

app = Flask(__name__)
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
PDF_FOLDER = "pdf"

SUPPORTED_PDF_FILES = ['test']

def supported_pdfnames(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.view_args['pdfname'] not in SUPPORTED_PDF_FILES:
            abort(500, "Not supported PDF name")
        return f(*args, **kwargs)
    return wrapper

@app.route('/pdf/<pdfname>', methods=['POST'])
@supported_pdfnames
def generate_filled_pdf(pdfname):
    r_json = request.get_json()
    if r_json is None:
        return abort(500, "Inpute JSON is required")

    pdfFilePath = fill_out_form("%s/%s.pdf" % (PDF_FOLDER, pdfname), r_json)

    return send_file(pdfFilePath, attachment_filename='out.pdf')

@app.route('/pdf/<pdfname>')
@supported_pdfnames
def get_dump_data_fields(pdfname):
    """
    /pdf/<pdfname>?format={pairs,keys}
    :pairs - list of pairs (key: value) for dumped data fields
    :keys - only dumped field names
    """
    if pdfname not in SUPPORTED_PDF_FILES:
        return abort(500, "Not supported PDF name")
    
    data = pypdftk.dump_data_fields("%s/%s.pdf" % (PDF_FOLDER, pdfname))
    
    formated = request.args.get('format')
    print(formated)
    if "pairs" == formated:
        data = format_fields_by_pairs(data)
    elif "keys" == formated:
        data = format_fields_by_keys(data)
    
    return jsonify(data)

@app.route('/pdf/')
def get_supported_pdfs():
    return jsonify(SUPPORTED_PDF_FILES)

def fill_out_form(pdf_file_path, data):
    return pypdftk.fill_form(pdf_file_path, data)

def format_fields_by_pairs(dump_data_fields=[]):
    pairs = []
    for field in dump_data_fields:
        pairs.append({field['FieldName']: field['FieldValue']})
    return pairs

def format_fields_by_keys(dump_data_fields=[]):
    keys = []
    for field in dump_data_fields:
        keys.append(field['FieldName'])
    return keys

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)