from flask import (
    Blueprint, jsonify, redirect,
    render_template, request, session, url_for,
)

from .auth import USUARIOS, login_requerido
from .storage import backup_s3, salvar_csv
from .data import bairros, ruas

main = Blueprint("main", __name__)


# ── Login ──────────────────────────────────────────────────
@main.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha   = request.form.get("senha", "").strip()
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            session["usuario"] = usuario
            return redirect(url_for("main.index"))
        erro = "Usuário ou senha incorretos."
    return render_template("login.html", erro=erro)


# ── Logout ─────────────────────────────────────────────────
@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


# ── Formulário principal ───────────────────────────────────
@main.route("/")
@login_requerido
def index():
    return render_template(
        "index.html",
        bairros=bairros,
        ruas=ruas,
        usuario=session.get("usuario"),
    )


# ── Salvar registro ────────────────────────────────────────
@main.route("/salvar", methods=["POST"])
@login_requerido
def salvar():
    id_poste = request.form.get("id_poste", "").strip()
    bairro   = request.form.get("bairro",   "").strip()
    rua      = request.form.get("rua",      "").strip()

    if not all([id_poste, bairro, rua]):
        return jsonify({"erro": "Todos os campos são obrigatórios."}), 400

    salvar_csv(id_poste, bairro, rua, session.get("usuario", ""))

    if not backup_s3():
        return jsonify({"erro": "Dados salvos localmente, mas falha no backup S3."}), 500

    return "Sucesso", 200