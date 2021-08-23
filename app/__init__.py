from flask import Flask, request, jsonify, safe_join, send_from_directory
from image import create_files, files_list, create_zip_file
from werkzeug.exceptions import NotFound
import os

app = Flask(__name__)

FILES_DIRECTORY = './files'
MAX_CONTENT_LENGTH = 1000000

if not os.path.exists(FILES_DIRECTORY):
    os.makedirs(FILES_DIRECTORY)

# Rota POST com o endpoint /upload que terá a função de enviar um arquivo 
# por formulário com o campo formulário nomeado "file", com o valor sendo o arquivo a ser enviado;
@app.post('/upload')
def upload_form():

    content_length = request.content_length 

    if content_length > MAX_CONTENT_LENGTH:
        return {"message": "The data value transmitted exceeds the capacity limit."}, 413

    files_list = list(request.files)
    files = request.files
    files_types =  ('image/png', 'image/jpg', 'image/gif')

    if len(files_list) == 0:
        return {"message": "Send at least 1 file."}, 406

    for f in files_list:
        received_file = files[f]
        received_file_type = received_file.mimetype
        filename = received_file.filename

        if filename in os.listdir(FILES_DIRECTORY):
            return {"message": f"{filename} file already exist"}, 409


        if received_file_type not in files_types:
            return {"message": f"{received_file_type} format file unsupported"}, 415
        
    uploaded_files = create_files(files, FILES_DIRECTORY)
    
    return jsonify(uploaded_files), 201


# Rota GET com o endpoint /files que irá listar todos os arquivos e 
@app.get('/files')
def list_files():
    files = files_list(FILES_DIRECTORY)

    return jsonify(files), 200


# um endpoint /files/<tipo> que lista os arquivos de um determinado tipo;
@app.get('/files/<string:tipo>')
def list_files_by_type(tipo: str):

    files = files_list(FILES_DIRECTORY)

    filtred_files = [file for file in files if file.endswith(tipo)]

    return jsonify(filtred_files), 200


# Rota GET com o endpoint /download/<file_name> responsável 
# por fazer o download do arquivo solicitado em file_name;

@app.get('/download/<string:file_name>')
def download_file(file_name: str):

    filename = safe_join(file_name)

    try: 
        return send_from_directory(directory='../files', path=filename, as_attachment=True), 200
    except NotFound:
        return {"message": "file not found"}, 404
    

# Rota GET com o endpoint /download-zip com query_params (file_type, compression_rate) 
# para especificar o tipo de arquivo para baixar todos compactados e também a taxa de compressão.
@app.get('/download-zip')
def download_dir_as_zip():

    files = files_list(FILES_DIRECTORY)

    if len(files) == 0:
        return {"message": "the directory is empty"}, 404

    file_type = request.args.get('file_type')

    try:
        compression_rate = int(request.args.get('compression_rate'))
    except TypeError:
        compression_rate = 9

    zip_file = create_zip_file('/tmp','./files',file_type,compression_rate)
    
    download = send_from_directory(directory='/tmp', path=zip_file['filename'], as_attachment=True)
    
    return download, 200