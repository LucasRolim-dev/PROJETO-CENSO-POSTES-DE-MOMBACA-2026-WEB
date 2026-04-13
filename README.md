# 📊 Web-Censo — Postes de Mombaça 2026

> Sistema de catalogação georreferenciada de postes públicos do município de Mombaça/CE, desenvolvido como projeto prático da **Unidade 5 — Provimento de Serviços Computacionais** do programa **Capacita-iRede** (Nuvem e DevOps).

---

## 🗂️ Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Como Executar](#-como-executar)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Endpoints da API](#-endpoints-da-api)
- [Autor](#-autor)

---

## 📌 Sobre o Projeto

O **Web-Censo** é uma aplicação web containerizada que permite o registro e a consulta de postes públicos de Mombaça/CE. Os agentes de campo acessam o sistema via navegador, preenchem os dados do poste (ID, bairro, rua) e as informações são salvas em banco de dados PostgreSQL com backup automático na nuvem AWS S3.

**Funcionalidades:**
- Login com controle de acesso por sessão
- Cadastro de postes com seleção de bairro e rua
- Backup automático no Amazon S3
- Interface responsiva (mobile, tablet e desktop)

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|---|---|---|
| Python / Flask | 3.11+ | Backend e servidor web |
| PostgreSQL | 16 | Banco de dados relacional |
| Docker | 24+ | Containerização |
| Docker Compose | 3.8 | Orquestração dos containers |
| Amazon S3 | — | Backup dos dados na nuvem |
| SweetAlert2 | 11 | Alertas no frontend |

---

## ✅ Pré-requisitos

Antes de executar, certifique-se de ter instalado:

- [Docker](https://docs.docker.com/get-docker/) `>= 24`
- [Docker Compose](https://docs.docker.com/compose/install/) `>= 2.0`
- Conta AWS com bucket S3 configurado

---

## 🚀 Como Executar

**1. Clone o repositório**
```bash
git clone https://github.com/LucasRolim-dev/PROJETO-CENSO-POSTES-DE-MOMBACA-2026-WEB
cd PROJETO-CENSO-POSTES-DE-MOMBACA-2026-WEB
```

**2. Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

**3. Suba os containers**
```bash
docker-compose up -d
```

**4. Acesse no navegador**
```
http://localhost:3000
```

**Para encerrar:**
```bash
docker-compose down
```

**Para ver os logs:**
```bash
docker-compose logs -f web-censo
```

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
# Aplicação
SECRET_KEY=sua-chave-secreta-aqui

# Banco de dados
DB_HOST=db-censo
DB_USER=censo_user
DB_PASSWORD=sua-senha-aqui
DB_NAME=censo_db

# AWS S3
AWS_ACCESS_KEY_ID=sua-access-key
AWS_SECRET_ACCESS_KEY=sua-secret-key
AWS_REGION=us-east-1
AWS_BUCKET_NAME=nome-do-seu-bucket
```

> ⚠️ **Nunca suba o arquivo `.env` para o repositório.** Ele já está incluído no `.gitignore`.

---

## 📁 Estrutura do Projeto

```
web-censo-mombaca/
├── app.py                  # Aplicação Flask principal
├── Dockerfile              # Imagem da aplicação
├── docker-compose.yml      # Orquestração dos serviços
├── requirements.txt        # Dependências Python
├── .env.example            # Modelo de variáveis de ambiente
├── .env                    # Variáveis reais (não versionar!)
├── .dockerignore           # Arquivos ignorados no build
└── README.md               # Este arquivo
```

---

## 🔌 Endpoints da API

| Método | Rota | Descrição | Autenticação |
|---|---|---|---|
| `GET` | `/` | Formulário de cadastro | ✅ Requerida |
| `GET` | `/login` | Tela de login | ❌ Pública |
| `POST` | `/login` | Autenticar usuário | ❌ Pública |
| `GET` | `/logout` | Encerrar sessão | ✅ Requerida |
| `POST` | `/salvar` | Salvar dados do poste | ✅ Requerida |

---

## 👤 Autor

Desenvolvido por **[Lucas Rolim Cavalcante]** · [LinkedIn](https://www.linkedin.com/in/lucas-rolim-117-dev/) como 
projeto prático do programa **Capacita-iRede**.

Município de Mombaça · Ceará · 2026