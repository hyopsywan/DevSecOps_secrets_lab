# Laboratório DevSecOps: Gestão de Secrets em Pipelines de CI/CD
> **Empresa Fictícia:** SecureBank Analytics S.A.  
> **Foco da Atividade:** Identificação de riscos de vazamento de credenciais e aplicação de técnicas de Hardening em esteiras de deploy.

---

## 1. Contexto do Projeto e Situação-Problema
Durante uma revisão de segurança na infraestrutura da *SecureBank Analytics S.A.*, a equipe de Cyber Security identificou vulnerabilidades críticas no fluxo de desenvolvimento de uma aplicação de análise de crédito. 

Por falta de práticas de segurança em desenvolvimento (AppSec), credenciais de banco de dados e tokens de APIs externas estavam sendo tratados de forma inadequada. O objetivo deste laboratório foi simular esse cenário inseguro (vulnerável), realizar a análise de riscos e aplicar as devidas correções utilizando boas práticas de DevSecOps de forma incremental no histórico do Git.

---

## 2. Estrutura do Projeto
O laboratório foi estruturado da seguinte forma:

```text
devsecops-secrets-lab/
├── app/
│   └── main.py              # Código da aplicação (Rotina de Análise de Crédito)
├── .github/
│   └── workflows/
│       └── pipeline.yml     # Workflow de CI/CD (GitHub Actions)
├── Dockerfile               # Configuração do container da aplicação
├── .gitignore               # Bloqueio de arquivos sensíveis no Git
├── .dockerignore            # Bloqueio de arquivos sensíveis no build do Docker
├── .env.example             # Modelo público de variáveis (sem valores reais)
└── README.md                # Documentação técnica do projeto
```
### 3. 🛠️ Análise Didática: Como Cada Alteração Salvou o SecureBank

Em engenharia de segurança, aplicamos o conceito de **Defesa em Profundidade** (*Defense in Depth*). Isso significa que a segurança não depende de uma única barreira, mas de várias camadas independentes. Veja abaixo o impacto prático de cada vulnerabilidade e como a respectiva correção blindou o projeto:

#### Camada 1: O Código-Fonte (`app/main.py`)
**Conceito Guardião:** *Prevenção de Hardcoded Credentials (Credenciais Fixas)*

*   **O Cenário Inseguro:** As credenciais ficavam escritas direto no texto do script. Qualquer um com acesso de leitura ao arquivo roubava o acesso ao banco de dados. Além disso, logs de auditoria (`[DEBUG]` e `[TRACE]`) expunham as senhas na tela durante a execução.
*   **Como a correção trouxe segurança:** O código tornou-se **independente de dados sensíveis**. Ele agora usa `os.getenv()`, o que significa que o script apenas avisa ao sistema operacional: *"Eu preciso de uma senha, mas não sei qual é. Injete-a na minha memória quando me executar"*. Criamos também um mascaramento de log que valida se o segredo existe, mas exibe apenas `***`.

```python
# ❌ ANTES (Vulnerável: Credencial exposta no DNA do arquivo)
DATABASE_PASSWORD = "SenhaSuperSecreta123"

# ✅ DEPOIS (Seguro: Leitura em memória e proteção de saída)
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
print("Senha do banco: [PROTEGIDO] (***)")
```
#### Camada 2: O Versionamento (`.gitignore`)
**Conceito Guardião:** *Isolamento de Escopo e Ambiente Local*

*   **O Cenário Inseguro:** Sem o filtro, arquivos locais como o `.env` (usados para testes no computador do desenvolvedor) eram enviados acidentalmente para a nuvem através do `git push`. Se o repositório fosse interceptado ou ficasse público, as senhas vazariam instantaneamente.
*   **Como a correção trouxe segurança:** O arquivo `.gitignore` atua como uma "venda" nos olhos do Git. Ao listar o `.env` e extensões como `*.key` ou `*.pem`, o Git passa a ignorar completamente a existência desses arquivos locais. Mesmo que você digite `git add .`, eles nunca sairão da sua máquina física.

```text
# Regras aplicadas para criar o ponto cego seguro no Git:
.env
*.key
credentials.json
```
#### Camada 3: A Imagem e o Container (`Dockerfile` e `.dockerignore`)
**Conceito Guardião:** *Imutabilidade de Imagem Limpa (Zero-Secret Build)*

*   **O Cenário Inseguro:** A instrução `COPY .env /app/.env` compactava as senhas locais e as embutia de forma estática dentro das camadas da imagem Docker. Um atacante com acesso à imagem final conseguiria ler a senha facilmente inspecionando o histórico do container (`docker history`).
*   **Como a correção trouxe segurança:** Removemos a cópia do `.env` e criamos o `.dockerignore`. Agora, a imagem gerada para o SecureBank é 100% genérica e limpa (pode ser usada em testes, homologação ou produção sem alterações). Os segredos são injetados apenas em tempo de execução (*runtime*) diretamente na memória volátil do container usando a flag `-e`.

```dockerfile
# ❌ ANTES (Imagem gerada com a senha embutida nas camadas)
COPY .env /app/.env

# ✅ DEPOIS (A imagem nasce sem dados sensíveis e consome apenas em execução)
COPY app/ /app/

# Execução segura em runtime:
# docker run -e DATABASE_PASSWORD="..." devsecops-secrets-lab
```
#### Camada 4: A Esteira de CI/CD (`pipeline.yml`)
**Conceito Guardião:** *Centralização Criptográfica e Ocultação de Logs (Scrubbing)*

*   **O Cenário Inseguro:** Comandos textuais como `echo "DATABASE_PASSWORD=..."` deixavam as chaves expostas no arquivo YAML e, pior, gravavam as senhas permanentemente no histórico público de logs da aba *Actions*.
*   **Como a correção trouxe segurança:** Migramos as credenciais para o **GitHub Secrets**, que armazena os dados com criptografia de ponta a ponta (nem o próprio criador consegue visualizar o valor após salvá-lo). No arquivo do pipeline, usamos a sintaxe nativa `${{ secrets.DATABASE_PASSWORD }}`. O GitHub Actions injeta o valor direto na memória da máquina virtual de testes e possui um sistema automatizado de *Scrubbing*: se o código tentar imprimir a senha na tela por acidente, o robô do GitHub intercepta a saída e substitui o texto por `***` nos logs de execução.

```yaml
# ❌ ANTES (Texto claro exposto na automação)
run: echo "DATABASE_PASSWORD=SenhaSuperSecreta123"

# ✅ DEPOIS (Injeção criptografada em memória volátil)
env:
  DATABASE_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}
```

### 4. Linha do Tempo dos Commits Aplicados

A remediação do projeto foi documentada de forma incremental e profissional através das seguintes alterações controladas:

*   **`fix(security): remover secrets chumbados no codigo e mascarar logs`**  
    Refatoração do script Python para adoção de variáveis de ambiente em runtime e implementação de filtros de exibição.
    
*   **`fix(security): adicionar .env e credenciais locais ao .gitignore`**  
    Remoção do arquivo `.env` do cache de rastreamento do Git e aplicação das regras de exclusão para arquivos de configuração locais.
    
*   **`fix(security): isolar contexto do docker e remover copy do .env no dockerfile`**  
    Criação do filtro `.dockerignore` e higienização do processo de build para geração de imagens de containers limpas.
    
*   **`fix(security): migrar variaveis de ambiente para github secrets no workflow`**  
    Adoção da sintaxe declarativa criptografada nativa do GitHub Actions e eliminação de comandos textuais que expunham dados sensíveis nos logs do console.
