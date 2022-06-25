import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import Flask, send_file, current_app, send_from_directory
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'uploads/')
UPLOAD_FOLDER = "uploads"
EXTENSION_HEADER = {
    'txt': 'text/plain',
    'pdf': 'application/pdf',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
}


class researchGatewayService:
    name = 'research_gateway'
    user_rpc = RpcProxy('user_service')
    storage_rpc = RpcProxy('storage_service')
    session_rpc = RpcProxy('session_service')

    @http('POST', '/login')
    def login_account(self, request):
        req = request.json
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            login = self.user_rpc.login(req['email'], req['password'])

            if int(login['status_code']) == 200:
                email = {
                    'id_user': int(login['id_user']),
                    'email': req['email']
                }
                session_id = self.session_rpc.set_session_data(email)
                response = Response(json.dumps(login['response'], indent=4))
                response.set_cookie('sessionID', session_id)

                return response
            else:
                return int(login['status_code']), (json.dumps(login['response'], indent=4))
        else:
            return 400, json.dumps({"status": "error", "message": "Log Out First!"}, indent=4)

    @http('POST', '/register')
    def register_account(self, request):
        req = request.json
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            register = self.user_rpc.register(
                req['nrp'], req['nama'], req['email'], req['password'])
            return int(register['status_code']), (json.dumps(register['response'], indent=4))
        else:
            return 400, json.dumps({"status": "error", "message": "Log Out First!"}, indent=4)

    @http('GET', '/logout')
    def logout_account(self, request):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            logout = self.session_rpc.delete_session('sessionID')
            response = Response(json.dumps(logout))
            response.delete_cookie('sessionID')

            return response

    @http('POST', '/upload')
    def upload(self, request):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            session = self.session_rpc.get_session_data(cookies)

            app = Flask(__name__)
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']
            title = request.form['title']
            abstract = request.form['abstract']

            file_type = (file.filename).split('.')[-1]
            filename = (''.join(e for e in file.filename if e.isalnum())).replace(
                file_type, '')
            file_name = str(
                hash(str(session['id_user']))) + '_' + filename + '.' + file_type

            upload_files = self.storage_rpc.upload_files(
                file_name, title, abstract, session['id_user'])

            filename = secure_filename(file_name)
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))

            return 200,  json.dumps({"status": "success", "message": "Paper uploaded successfully!"}, indent=4)

    @http('GET', '/download/<int:file_id>')
    def download(self, request, file_id):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            session = self.session_rpc.get_session_data(cookies)
            download = self.storage_rpc.download_file(
                file_id, session['id_user'])

            if download['status_code'] == 200:
                filename = download['filename']

                response = Response(
                    open(UPLOADS_PATH + '/' + filename, 'rb').read())
                file_type = filename.split('.')[-1]

                response.headers['Content-Type'] = EXTENSION_HEADER[file_type]
                response.headers['Content-Disposition'] = 'attachment; filename={}'.format(
                    filename)

                return response
            else:
                return int(download['status_code']), (json.dumps(download['response'], indent=4))

    @http('GET', '/file')
    def view_file(self, request):
        cookies = request.cookies.get('sessionID')

        if cookies is None:
            return 400,  json.dumps({"status": "error", "message": "Log In First!"}, indent=4)
        else:
            session = self.session_rpc.get_session_data(cookies)
            file = self.storage_rpc.view_file(session['id_user'])
            return int(file['status_code']), (json.dumps(file['response'], indent=4))
