from flask import Flask, request, jsonify, safe_join
from werkzeug.utils import secure_filename
from image import create_directory, create_files, files_list
import os

app = Flask(__name__)

FILES_DIRECTORY = './files'
MAX_CONTENT_LENGTH = 1000000
create_directory(FILES_DIRECTORY)

# Rota POST com o endpoint /upload que terá a função de enviar um arquivo 
# por formulário com o campo formulário nomeado "file", com o valor sendo o arquivo a ser enviado;
@app.post('/upload')
def upload_form():

    files_list = list(request.files)
    files = request.files
    files_types =  ('image/png', 'image/jpg', 'image/gif')

    if len(files_list) == 0:
        return {"message": "Envie pelo menos 1 arquivo."}, 406

    for f in files_list:
        received_file = files[f]
        received_file_type = received_file.mimetype
        

        if received_file_type not in files_types:
            return {"message": f"{received_file_type} format file unsupported"}, 415
        

    uploaded_files = create_files(files, FILES_DIRECTORY)

    filename = secure_filename(received_file.filename)
    file_path = safe_join(FILES_DIRECTORY, filename)

    if os.path.getsize(file_path) > MAX_CONTENT_LENGTH:
        os.remove(file_path)
        return {"message": "file size exceeded"}, 413

    return jsonify(uploaded_files)


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
def download_file(file_name):
    return ''


# Rota GET com o endpoint /download-zip com query_params (file_type, compression_rate) 
# para especificar o tipo de arquivo para baixar todos compactados e também a taxa de compressão.
@app.get('/download-zip')
def download_dir_as_zip():

    file_type = request.args.get('file_type')
    compression_rate = request.args.get('compression_rate')
    
    return ''