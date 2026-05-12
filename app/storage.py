import csv
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError

CSV_FILE = os.path.join("data", "censo_postes_mombaca_2026.csv")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


def salvar_csv(id_poste: str, bairro: str, rua: str, usuario: str) -> None:
    """Salva um registro no arquivo CSV local."""
    os.makedirs("data", exist_ok=True)
    arquivo_existe = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        if not arquivo_existe:
            writer.writerow(["ID do Poste", "Bairro", "Rua", "Registrado por"])
        writer.writerow([id_poste, bairro, rua, usuario])


def backup_s3() -> bool:
    """Faz upload do CSV para o bucket S3. Retorna True se bem-sucedido."""
    bucket = os.getenv("AWS_BUCKET_NAME")
    if not bucket:
        print("⚠️  AWS_BUCKET_NAME não configurado.")
        return False
    try:
        s3_client.upload_file(CSV_FILE, bucket, os.path.basename(CSV_FILE))
        print("✅ Backup no S3 concluído.")
        return True
    except (BotoCoreError, ClientError) as e:
        print(f"❌ Erro no backup S3: {e}")
        return False