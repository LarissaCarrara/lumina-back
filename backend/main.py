from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
import bcrypt
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

app = FastAPI()

# Modelo de dados para o login
class LoginData(BaseModel):
    email: str
    password: str

data_url = os.getenv("DATABASE_URL")

# Função para conectar ao banco e buscar o usuário
async def get_user(email: str):
    conn = await asyncpg.connect(data_url)
    user = await conn.fetchrow('SELECT * FROM users WHERE email = $1', email)
    await conn.close()
    return user

# Função para verificar a senha (usando bcrypt)
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Função para gerar o token JWT
def create_access_token(email: str):
    # Definindo o tempo de expiração do token (1 hora)
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": email, "exp": expiration}
    secret_key = "seu_secret_key_aqui"  # Use um segredo forte e seguro
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

@app.post("/login")
async def fazer_login(data: LoginData):
    user = await get_user(data.email)
    
    if user:
        # Verificando se a senha fornecida corresponde ao hash armazenado no banco
        if verify_password(data.password, user['password']):
            # Gerando o token de acesso
            token = create_access_token(data.email)
            return {"access_token": token}
        else:
            raise HTTPException(status_code=400, detail="Credenciais inválidas")
    else:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
