import os
import time

# Configurações globais do sistema (ERRO: Credenciais expostas no código)
DATABASE_USER = "admin"
DATABASE_PASSWORD = "SenhaSuperSecreta123"
API_TOKEN = "ghp_token_exemplo_123456"
API_URL = "https://api.securebank.com.br/v1/credit-check"

def conectar_banco_dados():
    print("[DEBUG] Inicializando pool de conexões com o banco...")
    time.sleep(0.5)
    # ERRO: Vazando credenciais em string de log/debug
    print(f"[DEBUG] Tentando autenticar usuário '{DATABASE_USER}' com a senha '{DATABASE_PASSWORD}'...")
    print("[SUCCESS] Conexão com o banco de dados estabelecida com sucesso.")
    return True

def consultar_score_credito(cpf_cliente):
    print(f"[INFO] Solicitando análise de risco para o CPF: {cpf_cliente}")
    time.sleep(0.8)
    
    # Simulação de um cabeçalho HTTP de autenticação
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # ERRO: Imprimindo o objeto de requisição inteiro para "auditoria", vazando o token
    print(f"[TRACE] Enviando requisição para {API_URL} com headers: {headers}")
    
    # Mock de resposta da API
    return {"status": "aprovado", "score": 850, "limite_sugerido": 5000.00}

def processar_analise_diaria():
    print("--- INICIANDO ROTINA DE ANÁLISE DE CRÉDITO ---")
    
    if conectar_banco_dados():
        # Simula a busca de um cliente no banco e a checagem na API
        cpf_teste = "123.456.789-00"
        resultado = consultar_score_credito(cpf_teste)
        
        print(f"\n[RESULTADO] Cliente {cpf_teste}: Status {resultado['status'].upper()}")
        print(f"[RESULTADO] Limite pré-aprovado: R$ {resultado['limite_sugerido']}")
    
    print("--- ROTINA FINALIZADA ---")

if __name__ == "__main__":
    processar_analise_diaria()