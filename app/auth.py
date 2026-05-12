from functools import wraps
from flask import session, redirect, url_for

# Usuários fixos — mova para .env em produção
USUARIOS = {
    "admin": "senha123",
    "agente1": "mombaca2026",
}


def login_requerido(f):
    """Decorator que protege rotas que exigem autenticação."""
    @wraps(f)
    def decorador(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorador