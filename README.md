# 🎖️ SISPNR — Sistema Integrado de Gestão & Portal de Consulta de PNR

> **Aplicação Web para Administração e Transparência na Distribuição de Próprios Nacionais Residenciais (PNR) do Exército Brasileiro.**

---

## 📌 Visão Geral

O **SISPNR** foi desenvolvido para informatizar, simplificar e dar transparência à gestão de PNRs e à relação de pretendentes na Guarnição. O sistema é totalmente alinhado com as **Instruções Gerais para a Administração dos Próprios Nacionais Residenciais do Exército (EB10-IG-04.006 - 3ª Edição, 2025 / Portaria – C Ex Nº 2.593/2025)**.

---

## 🚀 Funcionalidades Principais

### 🌐 1. Portal Público do Militar Pretendente (Autoatendimento)
* **Consulta por CPF:** Permite ao militar verificar sua posição exata na relação de pretendentes sem necessidade de login.
* **Transparência e Precedência:** Cálculo da posição na fila por Círculo Hierárquico baseado rigorosamente na **data e hora exatas do protocolo** do requerimento e na cota prioritária para dependente PcD (Art. 13, IV e §8º).
* **Relação Pública Anonimizada:** Consulta pública da lista mantendo a conformidade com a LGPD.

### 🔐 2. Painel Administrativo de Gestão (Prefeitura Militar / Seção PNR)
* **Gestão da Fila de Espera:** Homologação de novos requerimentos, registro formal de desistências e atualização de prioridades.
* **Ocupações e Permissões de Uso:** Distribuição automatizada do PNR vago para o topo da fila, geração do Termo de Permissão de Uso (Anexo C) e controle de DIEx para desconto em contracheque (CPEx).
* **Vistorias e Desocupações:** Registro de laudos de vistoria de entrada e saída (Anexo F), leitura de medidores e apuração automática de avarias e cobrança do material de pintura para ocupações inferiores a 2 anos.
* **Calculadora de Prazos Legais e Multas:** Monitoramento de prazos de devolução (Art. 31) e apuração de multa por ocupação irregular de 10 vezes a taxa de uso (Art. 33, III).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **Framework Web:** [Streamlit](https://streamlit.io/)
* **Manipulação de Dados:** Pandas
* **Banco de Dados:** SQLite3 / PostgreSQL (SQL Relacional)
* **Segurança:** Autenticação SHA-256 para perfis administrativos

---

## 📁 Estrutura de Arquivos do Repositório

```text
pnr7rm/
├── app-v3.py             # Aplicação web principal (Portal + Painel Adm)
├── requirements.txt      # Dependências Python para execução/deploy
├── schema_pnr_eb.sql     # Script SQL de criação do banco de dados relacional
├── seed_pnr_eb.sql       # Script SQL de povoamento de dados de teste
└── README.md             # Documentação do projeto

💻 Como Executar Localmente
Pré-requisitos
Ter o Python 3.10+ instalado no computador.

# 1. Clonar o repositório
git clone https://github.com/SEU-USUARIO/pnr7rm.git
cd pnr7rm

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Executar o sistema web
streamlit run app-v3.py

O sistema abrirá automaticamente no navegador no endereço http://localhost:8501.
🔐 Credenciais de Acesso (Demonstração)

    Usuário: admin
    Senha: pnr2026

📜 Amparo Normativo
Este sistema observa rigorosamente a legislação militar pertinente:

    Portaria – C Ex Nº 2.593, de 2 de dezembro de 2025 (EB10-IG-04.006 - 3ª Edição).
    Lei Complementar nº 97/1999 e Decreto nº 5.751/2006.


---

### 📝 Como adicionar ao GitHub:
1. No seu repositório no GitHub, clique no arquivo `README.md` (ou em **Add file** ➔ **Create new file** e nomeie como `README.md`).
2. Clique no ícone de **lápis (Edit file)**.
3. Cole o texto acima e clique no botão verde **Commit changes**.
