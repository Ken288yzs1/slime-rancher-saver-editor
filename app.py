"""史莱姆牧场1 存档修改器 - 后端 (Flask + 内存存储 + 自动清理)
注意: 内存字典存储, 必须单worker运行(见Dockerfile)"""
import io, os, time, uuid, threading
from flask import Flask, request, jsonify, send_file, send_from_directory
import core

app = Flask(__name__, static_folder="static", static_url_path="")

SAVES = {}
LOCK = threading.Lock()
EXPIRE_SEC = 1800
MAX_SIZE = 5 * 1024 * 1024

def cleanup():
    now=time.time()
    with LOCK:
        for k in [k for k,v in SAVES.items() if now-v["ts"]>EXPIRE_SEC]:
            del SAVES[k]

def get_data(fid):
    cleanup()
    with LOCK:
        if fid not in SAVES: return None
        SAVES[fid]["ts"]=time.time()
        return SAVES[fid]["data"]

@app.route("/")
def index():
    return send_from_directory("static","index.html")

@app.route("/api/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"ok":False,"msg":"未收到文件"}),400
    f=request.files["file"]; raw=f.read()
    if not raw: return jsonify({"ok":False,"msg":"文件为空"}),400
    if len(raw)>MAX_SIZE: return jsonify({"ok":False,"msg":"文件过大(>5MB)"}),400
    data=bytearray(raw)
    if len(core.scan_srad(data))==0:
        return jsonify({"ok":False,"msg":"未检测到SRAD, 可能不是有效存档"}),400
    fid=uuid.uuid4().hex
    with LOCK:
        SAVES[fid]={"data":data,"name":f.filename or "gamesave-sav","ts":time.time()}
    return jsonify({"ok":True,"fileId":fid,"overview":core.get_overview(data)})

@app.route("/api/items/<fid>")
def api_items(fid):
    d=get_data(fid)
    if d is None: return jsonify({"ok":False,"msg":"存档不存在或已过期"}),404
    return jsonify({"ok":True,"items":core.list_items(d)})

@app.route("/api/slimes/<fid>")
def api_slimes(fid):
    d=get_data(fid)
    if d is None: return jsonify({"ok":False,"msg":"存档不存在或已过期"}),404
    return jsonify({"ok":True,"slimes":core.list_slimes(d)})

@app.route("/api/market/<fid>")
def api_market(fid):
    d=get_data(fid)
    if d is None: return jsonify({"ok":False,"msg":"存档不存在或已过期"}),404
    base,rows=core.list_market(d)
    return jsonify({"ok":True,"market":rows,"addr":(f"0x{base:X}" if base is not None else None)})

@app.route("/api/convertible")
def api_convertible():
    return jsonify({"ok":True,"list":core.convertible_list()})

@app.route("/api/edit/item", methods=["POST"])
def edit_item():
    j=request.get_json(force=True); d=get_data(j.get("fileId"))
    if d is None: return jsonify({"ok":False,"msg":"存档不存在或已过期"}),404
    res=core.edit_item_count(d,int(j["addr"]),int(j["count"]))
    res["items"]=core.list_items(d)
    return jsonify(res)

@app.route("/api/edit/slime", methods=["POST"])
def edit_slime():
    j=request.get_json(force=True); d=get_data(j.get("fileId"))
    if d is None: return jsonify({"ok":False,"msg":"存档不存在或已过期"}),404
    res=core.edit_slime_type(d,int(j["from"]),int(j["to"]))
    res["slimes"]=core.list_slimes(d)
    return jsonify(res)

@app.route("/api/edit/market", methods=["POST"])
def edit_market():
    j=request.get_json(force=True); d=get_data(j.get("fileId"))
    if d is None: return jsonify({"ok":False,"msg":"存档不存在或已过期"}),404
    res=core.edit_market_clear(d)
    base,rows=core.list_market(d); res["market"]=rows
    return jsonify(res)

@app.route("/api/download/<fid>")
def download(fid):
    d=get_data(fid)
    if d is None: return jsonify({"ok":False,"msg":"存档不存在或已过期"}),404
    with LOCK: name=SAVES[fid]["name"]
    return send_file(io.BytesIO(bytes(d)),as_attachment=True,
                     download_name=name,mimetype="application/octet-stream")

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",7860)))
