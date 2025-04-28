from flask import Flask, request, send_from_directory, render_template, redirect, url_for, abort
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import shutil

# Configurações
ROOT_FOLDER = '/data/data/com.termux/files/home/storage/shared/NAS'
UPLOAD_LIMIT_MB = 512

# Flask App
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = UPLOAD_LIMIT_MB * 1024 * 1024

# Helpers de Segurança
def secure_path(path):
    """Garante que o caminho final esteja dentro da pasta raiz."""
    safe_path = os.path.realpath(os.path.join(ROOT_FOLDER, path))
    if not safe_path.startswith(os.path.realpath(ROOT_FOLDER)):
        abort(403)
    return safe_path

def ensure_extension(filename):
    """Garante que o arquivo tenha extensão."""
    if '.' not in os.path.basename(filename):
        return filename + ".bin"
    return filename

# Rotas
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', defaults={'req_path': ''}, methods=['GET', 'POST'])
@app.route('/<path:req_path>', methods=['GET', 'POST'])
def index(req_path):
    target_folder = secure_path(req_path)

    if request.method == 'POST':
        try:
            if 'file' in request.files:
                for f in request.files.getlist('file'):
                    raw_name = f.filename or f.name
                    rel_path = raw_name if '/' in raw_name else secure_filename(raw_name)
                    rel_path = ensure_extension(rel_path)
                    save_path = secure_path(os.path.join(req_path, rel_path))

                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    f.save(save_path)
            elif 'new_folder' in request.form:
                new_folder = secure_filename(request.form['new_folder'])
                folder_path = secure_path(os.path.join(req_path, new_folder))
                os.makedirs(folder_path, exist_ok=True)
            return redirect(request.path)
        except Exception as e:
            abort(500, description=str(e))

    sort_key = request.args.get('sort', 'name')
    reverse = request.args.get('desc', '0') == '1'

    items = []
    try:
        for entry in os.scandir(target_folder):
            stat = entry.stat()
            items.append({
                'name': entry.name,
                'is_dir': entry.is_dir(),
                'size': stat.st_size if not entry.is_dir() else 0,
                'mtime': datetime.fromtimestamp(stat.st_mtime)
            })
    except FileNotFoundError:
        items = []

    def sort_items_key(item):
        if sort_key == 'size':
            return item['size']
        elif sort_key == 'date':
            return item['mtime']
        return item['name'].lower()

    items.sort(key=sort_items_key, reverse=reverse)

    rel_path = req_path.strip('/')
    folders = [{
        'name': it['name'],
        'path': '/'.join(filter(None, [rel_path, it['name']]))
    } for it in items if it['is_dir']]

    return render_template(
        'index.html',
        current_path=rel_path,
        items=items,
        folders=folders,
        sort_key=sort_key,
        reverse=reverse
    )

@app.route('/files/<path:file_path>')
def download(file_path):
    full_path = secure_path(file_path)
    if not os.path.isfile(full_path):
        abort(404)
    return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path), as_attachment=True)

@app.route('/delete/<path:file_path>', methods=['POST'])
def delete(file_path):
    full_path = secure_path(file_path)
    try:
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            if not os.listdir(full_path):
                os.rmdir(full_path)
            else:
                shutil.rmtree(full_path)
    except Exception as e:
        abort(500, description=str(e))
    return redirect(request.referrer or '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
