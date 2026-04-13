import csv
import os
import boto3
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'chave-super-secreta-troque-isso')

USUARIOS = {
    "admin": "momb1234",
    "lucas rolim": "momb123"
}

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

bairros = ["Centro", "Tejubana", "Recreio", "Vila Iracema", "Maria Sabino de Morais",
           "Vila Salete", "Antonio Felinto", "Boa Esperanca", "Alto do Clube",
           "Avenida Beira-Rio", "Ipiranga", "Sao Domingos", "Tejubana Centro",
           "Betania", "Recreacao", "Sao Jose", "Loteamento Jardins Florenca",
           "Rocha Andrade", "Divino Salvador", "Antonio Soares",
           "Francisco Castelo de Castro", "Felecidade", "Riviera"]
bairros.sort()

ruas = ["R.Antonio Fernandes Martins Junior", "Vila Iracema Oito", "Vila Iracema Nove",
        "Vila Iracema Dez", "R. Mae Teresinha", "R. Vital Batista de Souza"]
ruas.sort()

def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorador

BASE_STYLE = """
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
        --primary: #3b82f6;
        --primary-dark: #1d4ed8;
        --primary-glow: rgba(59,130,246,0.3);
        --bg: #0a0a0f;
        --surface: #12121a;
        --card: #1a1a26;
        --border: #2a2a3a;
        --input-bg: #0f0f18;
        --text: #f0f0ff;
        --text-dim: #8888aa;
        --danger: #ef4444;
        --radius: 14px;
        --radius-sm: 8px;
    }

    html { font-size: 16px; }

    body {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--bg);
        color: var(--text);
        min-height: 100vh;
        min-height: 100dvh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: clamp(16px, 4vw, 40px);
        background-image:
            radial-gradient(ellipse 80% 60% at 50% -10%, rgba(59,130,246,0.12) 0%, transparent 70%),
            linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--surface); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

    .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: clamp(16px, 3vw, 24px);
        box-shadow: 0 25px 60px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.03) inset;
        width: 100%;
        max-width: 460px;
        padding: clamp(24px, 5vw, 44px) clamp(20px, 5vw, 40px);
        animation: fadeUp 0.4s ease both;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .title {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: clamp(16px, 3vw, 20px);
        color: var(--primary);
        text-align: center;
        letter-spacing: -0.5px;
        line-height: 1.2;
        margin-bottom: 6px;
    }
    .subtitle {
        font-size: clamp(11px, 2vw, 13px);
        color: var(--text-dim);
        text-align: center;
        margin-bottom: clamp(20px, 4vw, 32px);
    }

    .field-group { margin-bottom: clamp(14px, 3vw, 20px); }

    label {
        display: block;
        margin-bottom: 7px;
        font-size: clamp(12px, 1.8vw, 13px);
        font-weight: 500;
        color: var(--text-dim);
        letter-spacing: 0.3px;
    }

    input[type="text"], input[type="password"], select {
        width: 100%;
        padding: clamp(10px, 2vw, 13px) clamp(12px, 2.5vw, 16px);
        border-radius: var(--radius-sm);
        border: 1px solid var(--border);
        background-color: var(--input-bg);
        color: var(--text);
        font-family: 'DM Sans', sans-serif;
        font-size: clamp(14px, 2vw, 15px);
        outline: none;
        transition: border-color 0.25s, box-shadow 0.25s;
        -webkit-appearance: none;
        appearance: none;
    }

    input:focus, select:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px var(--primary-glow);
    }

    .search-select-box {
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
        background: var(--input-bg);
        transition: border-color 0.25s, box-shadow 0.25s;
    }
    .search-select-box:focus-within {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px var(--primary-glow);
    }
    .search-select-box input {
        border: none;
        border-bottom: 1px solid var(--border);
        border-radius: 0;
        background: transparent;
        box-shadow: none !important;
    }
    .search-select-box select {
        border: none;
        border-radius: 0;
        background: transparent;
        height: clamp(120px, 20vw, 155px);
        cursor: pointer;
        box-shadow: none !important;
    }

    @keyframes glow-pulse {
        0%   { box-shadow: 0 0 0 2px var(--primary), 0 0 10px var(--primary-glow); }
        50%  { box-shadow: 0 0 0 3px var(--primary), 0 0 20px rgba(59,130,246,0.5); }
        100% { box-shadow: 0 0 0 2px var(--primary), 0 0 10px var(--primary-glow); }
    }
    .vibrar-input {
        border-color: var(--primary) !important;
        animation: glow-pulse 2s infinite ease-in-out;
    }

    .btn {
        width: 100%;
        padding: clamp(12px, 2.5vw, 15px);
        border-radius: var(--radius-sm);
        border: none;
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        font-family: 'Syne', sans-serif;
        font-size: clamp(14px, 2vw, 16px);
        font-weight: 700;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;
        margin-top: clamp(8px, 2vw, 12px);
        letter-spacing: 0.3px;
        box-shadow: 0 4px 20px rgba(59,130,246,0.3);
    }
    .btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(59,130,246,0.45); }
    .btn:active:not(:disabled) { transform: translateY(0); }
    .btn:disabled { opacity: 0.6; cursor: not-allowed; }

    .alert-erro {
        background: rgba(239,68,68,0.1);
        border: 1px solid rgba(239,68,68,0.4);
        color: #fca5a5;
        padding: 10px 14px;
        border-radius: var(--radius-sm);
        font-size: clamp(12px, 2vw, 13px);
        margin-bottom: 18px;
        text-align: center;
    }

    .rodape {
        text-align: center;
        margin-top: 18px;
        font-size: clamp(10px, 1.8vw, 12px);
        color: #444466;
    }

    .logo-icon {
        width: clamp(48px, 8vw, 64px);
        height: clamp(48px, 8vw, 64px);
        background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(29,78,216,0.1));
        border: 1px solid rgba(59,130,246,0.3);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: clamp(22px, 4vw, 30px);
        margin: 0 auto clamp(14px, 3vw, 20px);
        box-shadow: 0 0 30px rgba(59,130,246,0.15);
    }

    @media (min-width: 600px) { .card { max-width: 480px; } }
    @media (min-width: 900px) { .card { max-width: 500px; } }
    @media (max-width: 360px) { .card { padding: 20px 16px; } .btn { font-size: 13px; } }
    @media (max-height: 500px) and (orientation: landscape) {
        body { padding: 10px; justify-content: flex-start; }
        .logo-icon { display: none; }
    }
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        senha = request.form.get('senha', '').strip()
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            erro = "Usuario ou senha incorretos."

    alerta = f"<div class='alert-erro'>&#9888; {erro}</div>" if erro else ""

    html_login = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
        <meta name="theme-color" content="#0a0a0f">
        <title>Login | Censo Postes</title>
        <style>
        {BASE_STYLE}
        input[type="text"], input[type="password"] {{ padding-right: 44px; }}
        .input-wrapper {{ position: relative; }}
        .input-wrapper .icon {{
            position: absolute; right: 14px; top: 50%;
            transform: translateY(-50%); color: var(--text-dim);
            font-size: 16px; pointer-events: none;
        }}
        </style>
    </head>
    <body>
      <div class="card">
        <div class="logo-icon">&#128161;</div>
        <h1 class="title">CENSO DE POSTES</h1>
        <p class="subtitle">Mombaca 2026 &middot; Acesso Restrito</p>
        {alerta}
        <form method="POST" autocomplete="on">
          <div class="field-group">
            <label for="usuario">Usuario</label>
            <div class="input-wrapper">
              <input type="text" id="usuario" name="usuario" placeholder="Digite seu usuario"
                     autocomplete="username" required autofocus>
              <span class="icon">&#128100;</span>
            </div>
          </div>
          <div class="field-group">
            <label for="senha">Senha</label>
            <div class="input-wrapper">
              <input type="password" id="senha" name="senha" placeholder="Digite sua senha"
                     autocomplete="current-password" required>
              <span class="icon">&#128274;</span>
            </div>
          </div>
          <button type="submit" class="btn">Entrar &rarr;</button>
        </form>
        <p class="rodape">Prefeitura Municipal de Mombaca &middot; CE</p>
      </div>
    </body>
    </html>
    """
    return render_template_string(html_login)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_requerido
def index():
    opcoes_bairros = "".join([f'<option value="{b}">{b}</option>' for b in bairros])
    opcoes_ruas    = "".join([f'<option value="{r}">{r}</option>' for r in ruas])
    usuario_logado = session.get('usuario', '')

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
        <meta name="theme-color" content="#0a0a0f">
        <title>Censo Poste | Mombaca 2026</title>
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        <style>
        {BASE_STYLE}

        .topbar {{
            width: 100%; max-width: 460px;
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: clamp(8px, 2vw, 14px); padding: 0 4px;
        }}
        .topbar-user {{
            font-size: clamp(12px, 2vw, 13px); color: var(--text-dim);
            display: flex; align-items: center; gap: 6px;
        }}
        .topbar-user strong {{ color: var(--primary); font-family: 'Syne', sans-serif; }}
        .btn-logout {{
            font-size: clamp(11px, 1.8vw, 12px); color: var(--danger);
            text-decoration: none; font-weight: 600;
            border: 1px solid rgba(239,68,68,0.35);
            padding: clamp(4px,1vw,6px) clamp(10px,2vw,14px);
            border-radius: 20px; transition: background 0.2s, color 0.2s; white-space: nowrap;
        }}
        .btn-logout:hover {{ background: var(--danger); color: white; }}

        .divider {{ border: none; border-top: 1px solid var(--border); margin: clamp(14px,3vw,22px) 0; }}

        .progress-bar {{
            height: 3px; background: var(--border); border-radius: 2px;
            margin-bottom: clamp(18px,3vw,26px); overflow: hidden;
        }}
        .progress-fill {{
            height: 100%; width: 0%;
            background: linear-gradient(90deg, var(--primary), #60a5fa);
            border-radius: 2px; transition: width 0.4s ease;
        }}

        @media (min-width: 600px) {{ .topbar {{ max-width: 480px; }} }}
        @media (min-width: 900px) {{ .topbar {{ max-width: 500px; }} }}
        </style>
    </head>
    <body>

    <div class="topbar">
        <div class="topbar-user">
            <span>&#128100;</span> <strong>{usuario_logado}</strong>
        </div>
        <a href="/logout" class="btn-logout">Sair &#8617;</a>
    </div>

    <div class="card">
        <div class="logo-icon">&#128161;</div>
        <h1 class="title">CENSO DE POSTES</h1>
        <p class="subtitle">Mombaca 2026 &middot; Registro de campo</p>

        <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>

        <form id="formCenso">
            <div class="field-group">
                <label>ID do Poste</label>
                <input type="text" id="id_poste" name="id_poste"
                       placeholder="Ex: P-117" autocomplete="off" inputmode="text" required
                       oninput="ativarBrilhoID(); atualizarProgress()">
            </div>

            <hr class="divider">

            <div class="field-group">
                <label>Bairro</label>
                <div class="search-select-box">
                    <input type="text" id="busca_bairro" placeholder="&#128269; Pesquisar bairro..."
                           onkeyup="filtrarLista('busca_bairro','select_bairro')">
                    <select name="bairro" id="select_bairro" size="5" required
                            onchange="preencherBusca('select_bairro','busca_bairro'); atualizarProgress()">
                        {opcoes_bairros}
                    </select>
                </div>
            </div>

            <div class="field-group">
                <label>Rua / Avenida</label>
                <div class="search-select-box">
                    <input type="text" id="busca_rua" placeholder="&#128269; Pesquisar rua..."
                           onkeyup="filtrarLista('busca_rua','select_rua')">
                    <select name="rua" id="select_rua" size="5" required
                            onchange="preencherBusca('select_rua','busca_rua'); atualizarProgress()">
                        {opcoes_ruas}
                    </select>
                </div>
            </div>

            <button type="button" class="btn" id="btnSalvar" onclick="enviarDados()">
                &#128190; Salvar na Nuvem
            </button>
        </form>
    </div>

    <script>
        function ativarBrilhoID() {{
            const el = document.getElementById('id_poste');
            el.value.trim() !== "" ? el.classList.add('vibrar-input') : el.classList.remove('vibrar-input');
        }}

        function atualizarProgress() {{
            const vals = [
                document.getElementById('id_poste').value.trim(),
                document.getElementById('select_bairro').value,
                document.getElementById('select_rua').value
            ];
            document.getElementById('progressFill').style.width = (vals.filter(v => v).length / 3 * 100) + '%';
        }}

        function filtrarLista(idInput, idSelect) {{
            const filter  = document.getElementById(idInput).value.toUpperCase();
            const options = document.getElementById(idSelect).getElementsByTagName('option');
            for (let i = 0; i < options.length; i++) {{
                const txt = options[i].textContent || options[i].innerText;
                options[i].style.display = txt.toUpperCase().includes(filter) ? "" : "none";
            }}
        }}

        function preencherBusca(idSelect, idInput) {{
            const val = document.getElementById(idSelect).value;
            const inp = document.getElementById(idInput);
            inp.value = val;
            inp.classList.add('vibrar-input');
        }}

        function enviarDados() {{
            const id     = document.getElementById('id_poste').value.trim();
            const bairro = document.getElementById('select_bairro').value;
            const rua    = document.getElementById('select_rua').value;

            if (!id || !bairro || !rua) {{
                Swal.fire({{ title: 'Atencao!', text: 'Preencha todos os campos.', icon: 'warning',
                    background: '#1a1a26', color: '#f0f0ff', confirmButtonColor: '#3b82f6' }});
                return;
            }}

            const btn = document.getElementById('btnSalvar');
            btn.innerText = "Salvando...";
            btn.disabled = true;

            fetch('/salvar', {{ method: 'POST', body: new FormData(document.getElementById('formCenso')) }})
            .then(r => {{
                if (r.ok) {{
                    Swal.fire({{ title: 'Salvo!', text: 'Dados enviados para a nuvem.', icon: 'success',
                        background: '#1a1a26', color: '#f0f0ff', confirmButtonColor: '#3b82f6' }});
                    document.getElementById('formCenso').reset();
                    ['id_poste','busca_bairro','busca_rua'].forEach(id => document.getElementById(id).classList.remove('vibrar-input'));
                    document.getElementById('progressFill').style.width = '0%';
                }} else if (r.status === 401) {{
                    Swal.fire('Sessao expirada','Faca login novamente.','warning').then(() => window.location.href='/login');
                }} else {{
                    r.json().then(d => Swal.fire('Erro', d.erro || 'Falha ao salvar', 'error'));
                }}
            }})
            .catch(err => Swal.fire('Erro Tecnico', err.message, 'error'))
            .finally(() => {{ btn.innerText = "Salvar na Nuvem"; btn.disabled = false; }});
        }}
    </script>
    </body>
    </html>
    """
    return render_template_string(html)


def fazer_backup_s3(nome_arquivo):
    try:
        s3_client.upload_file(nome_arquivo, os.getenv('AWS_BUCKET_NAME'), nome_arquivo)
        print("Backup no S3 concluido!")
        return True
    except Exception as e:
        print(f"Erro no backup: {e}")
        return False

@app.route('/salvar', methods=['POST'])
@login_requerido
def salvar():
    nome_arquivo       = "censo_postes_mombaca_2026.csv"
    id_poste           = request.form.get('id_poste', '').strip()
    bairro_selecionado = request.form.get('bairro', '').strip()
    rua_selecionada    = request.form.get('rua', '').strip()

    if not id_poste or not bairro_selecionado or not rua_selecionada:
        return jsonify({"erro": "Todos os campos sao obrigatorios"}), 400

    arquivo_existe = os.path.exists(nome_arquivo)
    with open(nome_arquivo, "a", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f, delimiter=';')
        if not arquivo_existe:
            escritor.writerow(["ID do Poste", "Bairro", "Rua", "Registrado por"])
        escritor.writerow([id_poste, bairro_selecionado, rua_selecionada, session.get('usuario')])

    if not fazer_backup_s3(nome_arquivo):
        return jsonify({"erro": "Dados salvos localmente, mas falha no backup S3"}), 500

    return "Sucesso", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)