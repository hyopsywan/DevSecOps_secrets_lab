import os
import time

# Configurações globais do sistema (CORRIGIDO: Lendo de variáveis de ambiente em runtime)
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
API_TOKEN = os.getenv("API_TOKEN")
API_URL = "https://api.securebank.com.br/v1/credit-check"

def conectar_banco_dados():
    print("[DEBUG] Inicializando pool de conexões com o banco...")
    time.sleep(0.5)
    
    # CORRIGIDO: Omitindo a senha real nos logs de auditoria
    if DATABASE_PASSWORD:
        senha_mascarada = "***"
    else:
        senha_mascarada = "NÃO CONFIGURADA"
        
    print(f"[DEBUG] Tentando autenticar usuário '{DATABASE_USER}' com a senha '{senha_mascarada}'...")
    print("[SUCCESS] Conexão com o banco de dados estabelecida com sucesso.")
    return True

def consultar_score_credito(cpf_cliente):
    print(f"[INFO] Solicitando análise de risco para o CPF: {cpf_cliente}")
    time.sleep(0.8)
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # CORRIGIDO: Mascarando o token sensível antes de exibir para trace/auditoria
    headers_seguros = headers.copy()
    if API_TOKEN:
        headers_seguros["Authorization"] = "Bearer ***"
        
    print(f"[TRACE] Enviando requisição para {API_URL} com headers: {headers_seguros}")
    return {"status": "aprovado", "score": 850, "limite_sugerido": 5000.00}

def processar_analise_diaria():
    print("--- INICIANDO ROTINA DE ANÁLISE DE CRÉDITO ---")
    
    # Validação de segurança prévia
    if not all([DATABASE_USER, DATABASE_PASSWORD, API_TOKEN]):
        print("\n❌ ERRO DE CONFIGURAÇÃO: Secrets essenciais não injetados no ambiente!")
        print("--- ROTINA ABORTADA POR SEGURANÇA ---\n")
        return

    if conectar_banco_dados():
        cpf_teste = "123.456.789-00"
        resultado = consultar_score_credito(cpf_teste)
        
        print(f"\n[RESULTADO] Cliente {cpf_teste}: Status {resultado['status'].upper()}")
        print(f"[RESULTADO] Limite pré-aprovado: R$ {resultado['limite_sugerido']}")
    
    print("--- ROTINA FINALIZADA ---")

if __name__ == "__main__":
    processar_analise_diaria()