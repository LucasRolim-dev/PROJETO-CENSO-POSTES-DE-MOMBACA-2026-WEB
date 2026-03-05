import csv
import os
import boto3
from flask import Flask, render_template_string, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuração do Cliente S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

bairros = ["Centro", "Tejubana", "Recreio", "Vila Iracema", "Maria Sabino de Morais",
           "Vila Salete", "Antonio Felinto", "Boa Esperanca", "Alto do Clube",
           "Avenida Beira-Rio", "Ipiranga", "Sao Domingos", "Tejubana Centro",
           "Betânia", "Recreação", "Sao Jose", "Loteamento Jardins Florença",
           "Rocha Andrade", "Divino Salvador", "Antonio Soares",
           "Francisco Castelo de Castro", "Felecidade", "Riviera"]
bairros.sort()

ruas = ["R.Antônio Fernandes Martins Júnior", "Vila Iracema Oito", "Vila Iracema Nove",
        "Vila Iracema Dez", "R. Mãe Teresinha", "R. Vital Batista de Souza"]
ruas.sort()

@app.route('/')
def index():
    opcoes_bairros = "".join([f'<option value="{b}">{b}</option>' for b in bairros])
    opcoes_ruas = "".join([f'<option value="{r}">{r}</option>' for r in ruas])

    html = f'''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Censo Poste | Mombaça 2026</title>
        <style>
          :root {{
              --primary: #007bff;
              --bg: #121212;
              --card: #1e1e1e;
              --input: #252525;
              --text: #ffffff;
              --text-dim: #aaa;
          }}
          body {{ 
              font-family: 'Inter', sans-serif; 
              background-color: var(--bg); 
              color: var(--text); 
              display: flex;
              justify-content: center; 
              align-items: center; 
              min-height: 100vh; 
              margin: 0; 
          }}
          .container {{ 
              background: var(--card); 
              padding: 30px; 
              border-radius: 20px;
              box-shadow: 0 20px 50px rgba(0,0,0,0.5); 
              width: 90%; 
              max-width: 405px; 
              border: 1px solid #333; 
          }}
          h1 {{ text-align: center; font-size: 23px; margin-bottom: 27px; color: var(--primary); letter-spacing: -1px; }}
          .field-group {{ margin-bottom: 18px; }}
          label {{ display: block; margin-bottom: 8px; font-size: 14px; font-weight: 600; color: var(--text-dim); }}
          
          input[type="text"], select {{ 
              width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #333; background-color: var(--input); 
              color: white; box-sizing: border-box; font-size: 15px; outline: none;
          }}
              /* Container das listas com bordas arredondadas */
          .search-select-box {{ border: 2px solid #333; border-radius: 15px; overflow: hidden; background: var(--input);transition: 0.4s;}}
          .search-select-box {{ border: 1px solid #333; border-radius: 8px; overflow: hidden; background: var(--input); }}
          .search-select-box input {{ border: none; border-bottom: 1px solid #333; border-radius: 0; background: transparent; }}
          .search-select-box select {{ border: none; border-radius: 0; background: transparent; height: 150px; cursor: pointer; }}

          /* EFEITO VIBRANTE (ANIMAÇÃO) */
          @keyframes glow-vibration {{
              0% {{ box-shadow: 0 0 5px var(--primary); border-color: var(--primary); }}
              50% {{ box-shadow: 0 0 20px var(--primary); border-color: #00c3ff; }}
              100% {{ box-shadow: 0 0 5px var(--primary); border-color: var(--primary); }}
          }}

          .vibrar {{
              animation: glow-vibration 1.5s infinite ease-in-out;
              border-color: var(--primary) !important;
          }}

          button {{ 
              width: 100%; padding: 15px; border-radius: 8px; border: none; background: var(--primary);
              color: white; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s ease;
              margin-top: 10px; 
          }}
          button:hover {{ background: #0056b3; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,123,255,0.3); }}
      
          option {{ padding: 12px; border-bottom: 1px solid #2a2a2a; }}
          option:checked {{ background-color: var(--primary) !important; color: white; }}
        </style>
    </head>
    <body>
    <div class="container">  
      <h1>CENSO | POSTES DE MOMBAÇA 2026</h1>
      <form action="/salvar" method="post">
          <div class="field-group">
             <label>ID do Poste</label>
             <input type="text" name="id_poste" placeholder="Ex: P-117" required>
        </div>

        <div class="field-group">
            <label>Selecionar Bairro</label>
            <div class="search-select-box">
                <input type="text" id="busca_bairro" placeholder="Pesquisar Bairro" 
                       onkeyup="filtrarLista('busca_bairro', 'select_bairro')">
                <select name="bairro" id="select_bairro" size="5" required 
                        onchange="preencherBusca('select_bairro', 'busca_bairro')">
                     {opcoes_bairros}  
                </select>
            </div>
        </div> 

        <div class="field-group">
           <label>Selecionar Rua/Avenida</label>
           <div class="search-select-box">
                <input type="text" id="busca_rua" placeholder="Pesquisar Rua/Av" 
                       onkeyup="filtrarLista('busca_rua', 'select_rua')">
                <select name="rua" id="select_rua" size="5" required 
                        onchange="preencherBusca('select_rua', 'busca_rua')">
                     {opcoes_ruas}
                </select>
            </div>
        </div> 

        <button type="submit">💾 Salvar na Nuvem</button>
      </form>
    </div>

    <script>
        // Filtra a lista enquanto digita
        function filtrarLista(idInput, idSelect) {{
            var input = document.getElementById(idInput);
            var filter = input.value.toUpperCase();
            var select = document.getElementById(idSelect);
            var options = select.getElementsByTagName('option');

            for (var i = 0; i < options.length; i++) {{
                var txtValue = options[i].textContent || options[i].innerText;
                options[i].style.display = txtValue.toUpperCase().indexOf(filter) > -1 ? "" : "none";
            }}
        }}

        // Novo: Copia o item selecionado para a barra de busca
        function preencherBusca(idSelect, idInput) {{
            var select = document.getElementById(idSelect);
            var input = document.getElementById(idInput);
            input.value = select.value;

            // Preenche o campo de busca
            input.value = select.value;
            
            // Adiciona a classe de vibração/brilho
            box.classList.add('vibrar');
        }}
    </script> 
    </body>
    </html>
    '''     

    return render_template_string(html)

def fazer_backup_s3(nome_arquivo):
    try:
        s3_client.upload_file(nome_arquivo, os.getenv('AWS_BUCKET_NAME'), nome_arquivo)
        print("✅ Backup no S3 concluído!")
    except Exception as e:
        print(f"❌ Erro no backup: {e}")

@app.route('/salvar', methods=['POST'])
def salvar():
    nome_arquivo = "censo_postes_mombaca_2026.csv"
    id_poste = request.form.get('id_poste')
    bairro_selecionado = request.form.get('bairro')
    rua_selecionada = request.form.get('rua')

    arquivo_existe = os.path.exists(nome_arquivo)

    with open(nome_arquivo, "a", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f, delimiter=';')
        if not arquivo_existe:
            escritor.writerow(["ID do Poste", "Bairro", "Rua"])
        escritor.writerow([id_poste, bairro_selecionado, rua_selecionada]) 

    fazer_backup_s3(nome_arquivo)
    return "<h1>✅ Salvo com Sucesso!</h1><a href='/'>Voltar</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)