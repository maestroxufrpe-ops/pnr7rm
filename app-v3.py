import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import hashlib

# Configuração da página
st.set_page_config(
    page_title="SISPNR - Gestão & Portal do Militar | Exército Brasileiro",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização — SISPNR | Identidade institucional premium
st.markdown("""
<style>
:root {
    --eb-green: #173b2a;
    --eb-green-2: #23543d;
    --eb-green-3: #2f6b4d;
    --gold: #b99a5b;
    --gold-soft: #eadfca;
    --ink: #17211b;
    --muted: #6b756e;
    --surface: #ffffff;
    --surface-2: #f5f7f5;
    --line: #e2e7e3;
    --danger: #a83a3a;
    --warning: #a87819;
    --success: #2d6a4f;
}

/* Base */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 90% 0%, rgba(185,154,91,.08), transparent 26rem),
        linear-gradient(180deg, #f7f9f7 0%, #f2f5f2 100%);
}
[data-testid="stHeader"] { background: transparent; }
.block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

/* Tipografia */
html, body, [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", sans-serif;
    color: var(--ink);
}
h1, h2, h3, h4 { letter-spacing: -.02em; }

/* Cabeçalho institucional */
.eb-header {
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    padding: 24px 28px;
    margin-bottom: 24px;
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 18px;
    background:
        radial-gradient(circle at 95% 20%, rgba(185,154,91,.18), transparent 18rem),
        linear-gradient(135deg, #122d21 0%, #1c4932 55%, #173b2a 100%);
    color: #fff;
    box-shadow: 0 12px 35px rgba(23,59,42,.16);
}
.eb-header:after {
    content: "";
    position: absolute;
    left: 0; right: 0; bottom: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: .85;
}
.eb-kicker {
    margin: 0 0 5px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .16em;
    color: #d8c8a5;
}
.eb-title {
    margin: 0;
    font-size: clamp(20px, 2vw, 29px);
    line-height: 1.12;
    font-weight: 800;
}
.eb-subtitle {
    margin: 7px 0 0;
    color: #cbd9d0;
    font-size: 13px;
}
.eb-standard {
    white-space: nowrap;
    border: 1px solid rgba(234,223,202,.28);
    background: rgba(255,255,255,.07);
    color: #f3ead8;
    padding: 9px 13px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .03em;
    backdrop-filter: blur(8px);
}

/* Cabeçalhos */
.main-header, .sub-header {
    color: var(--eb-green);
    font-weight: 800;
}
.main-header {
    font-size: 25px;
    line-height: 1.2;
    padding: 0 0 11px;
    margin: 6px 0 20px;
    border-bottom: 1px solid var(--line);
    position: relative;
}
.main-header:after {
    content: "";
    position: absolute;
    bottom: -1px; left: 0;
    width: 76px; height: 3px;
    background: var(--gold);
    border-radius: 4px;
}
.sub-header {
    font-size: 19px;
    margin: 8px 0 16px;
}

/* Cartões */
.kpi-card {
    position: relative;
    min-height: 104px;
    padding: 18px 18px 16px;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(255,255,255,.92);
    box-shadow: 0 5px 18px rgba(23,59,42,.055);
    overflow: hidden;
}
.kpi-card:before {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, var(--gold), var(--eb-green-3));
}
.kpi-label {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .10em;
    color: var(--muted);
    text-transform: uppercase;
}
.kpi-value {
    margin-top: 7px;
    font-size: 29px;
    line-height: 1;
    font-weight: 850;
    color: var(--eb-green);
}

/* Portal público */
.portal-box {
    border: 1px solid #dce6df;
    border-left: 4px solid var(--eb-green-3);
    padding: 20px 22px;
    border-radius: 14px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #ffffff, #f3f7f4);
    box-shadow: 0 7px 22px rgba(23,59,42,.05);
}
.portal-box h4 { margin: 0 0 7px !important; color: var(--eb-green); }
.portal-box p { margin: 0; color: #5f6b63 !important; line-height: 1.55; }

/* Badges */
.status-badge-green, .status-badge-amber, .status-badge-red {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 11px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    border: 1px solid transparent;
}
.status-badge-green { background:#e7f3ec; color:#21603e; border-color:#cce4d5; }
.status-badge-amber { background:#fbf2dd; color:#88610e; border-color:#eeddb4; }
.status-badge-red { background:#f8e9e9; color:#913232; border-color:#eccaca; }

/* Abas */
button[data-baseweb="tab"] {
    font-weight: 750;
    color: #657168;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--eb-green);
}
div[data-baseweb="tab-highlight"] {
    background-color: var(--gold) !important;
    height: 3px !important;
}

/* Botões */
.stButton > button, .stFormSubmitButton > button {
    min-height: 42px;
    border-radius: 10px;
    border: 1px solid #d6ded8;
    font-weight: 750;
    letter-spacing: .01em;
    transition: all .16s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: translateY(-1px);
    border-color: var(--eb-green-3);
    box-shadow: 0 7px 18px rgba(23,59,42,.12);
}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1d4a33, #2f6b4d);
    border: 0;
    color: white;
}

/* Inputs */
div[data-baseweb="input"], div[data-baseweb="select"], textarea {
    border-radius: 10px !important;
}
input:focus, textarea:focus {
    border-color: var(--eb-green-3) !important;
    box-shadow: 0 0 0 1px var(--eb-green-3) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102b20 0%, #173b2a 100%);
    border-right: 1px solid rgba(255,255,255,.07);
}
section[data-testid="stSidebar"] * { color: #e7eee9; }
section[data-testid="stSidebar"] .stRadio label p { font-size: 13px; }
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.13); }
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,.08);
    color: #fff;
    border-color: rgba(255,255,255,.14);
}

/* Tabelas / alertas */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
}
div[data-testid="stAlert"] { border-radius: 11px; }

/* Login */
.login-shell {
    max-width: 470px;
    margin: 35px auto 0;
    padding: 30px;
    background: rgba(255,255,255,.96);
    border: 1px solid var(--line);
    border-radius: 18px;
    box-shadow: 0 18px 50px rgba(23,59,42,.10);
}
.login-mark {
    width: 54px; height: 54px;
    margin: 0 auto 14px;
    display: grid; place-items: center;
    border-radius: 15px;
    background: #eaf1ec;
    font-size: 26px;
}
.login-title { text-align:center; color:var(--eb-green); margin:0; font-weight:850; }
.login-copy { text-align:center; color:var(--muted); font-size:13px; margin:7px 0 22px; }

/* Responsividade */
@media (max-width: 800px) {
    .eb-header { align-items: flex-start; flex-direction: column; padding: 20px; }
    .eb-standard { white-space: normal; }
    .main-header { font-size: 21px; }
}
</style>
""", unsafe_allow_html=True)

DB_PATH = "pnr_eb.db"

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Inicialização do Banco de Dados com tabela de administradores
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS usuarios_adm (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        nome_completo TEXT NOT NULL,
        perfil TEXT NOT NULL,
        ultimo_login DATETIME
    );

    CREATE TABLE IF NOT EXISTS militares (
        id_militar INTEGER PRIMARY KEY AUTOINCREMENT,
        cpf TEXT UNIQUE NOT NULL,
        identidade TEXT NOT NULL,
        prec_cp TEXT,
        nome_completo TEXT NOT NULL,
        posto_graduacao TEXT NOT NULL,
        circulo_hierarquico TEXT NOT NULL,
        om_vinculacao TEXT NOT NULL,
        telefone_om TEXT,
        telefone_pessoal TEXT NOT NULL,
        email TEXT,
        nome_conjuge TEXT,
        cpf_conjuge TEXT,
        identidade_conjuge TEXT,
        possui_veiculo INTEGER DEFAULT 0,
        veiculo_descricao TEXT,
        possui_animal INTEGER DEFAULT 0,
        animal_descricao TEXT,
        banco TEXT,
        agencia TEXT,
        conta_corrente TEXT,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS dependentes (
        id_dependente INTEGER PRIMARY KEY AUTOINCREMENT,
        id_militar INTEGER NOT NULL,
        nome_completo TEXT NOT NULL,
        parentesco TEXT NOT NULL,
        cpf TEXT,
        possui_deficiencia_pcd INTEGER DEFAULT 0,
        comprovacao_rm_pcd TEXT,
        data_nascimento TEXT,
        FOREIGN KEY (id_militar) REFERENCES militares(id_militar) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS pnrs (
        id_pnr INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_pnr TEXT UNIQUE NOT NULL,
        endereco_completo TEXT NOT NULL,
        bairro TEXT NOT NULL,
        cidade TEXT NOT NULL,
        uf TEXT NOT NULL,
        cep TEXT,
        natureza TEXT NOT NULL CHECK (natureza IN ('Casa', 'Apartamento')),
        tipo TEXT NOT NULL,
        categoria TEXT NOT NULL CHECK (categoria IN ('Uso Geral', 'Funcional')),
        administracao_areas_comuns TEXT NOT NULL,
        regime_coletivo INTEGER DEFAULT 0,
        status_imovel TEXT NOT NULL DEFAULT 'Pronto/Vago' 
            CHECK (status_imovel IN ('Pronto/Vago', 'Ocupado', 'Em Manutenção/Reforma', 'A Título Precário', 'Indisponível')),
        observacoes TEXT
    );

    CREATE TABLE IF NOT EXISTS requerimentos_fila (
        id_requerimento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_militar INTEGER NOT NULL,
        nup_eb TEXT NOT NULL,
        data_hora_protocolo DATETIME NOT NULL,
        circulo_pretendido TEXT NOT NULL,
        prioridade_pcd INTEGER DEFAULT 0,
        status_fila TEXT NOT NULL DEFAULT 'Aguardando'
            CHECK (status_fila IN ('Aguardando', 'Contemplado', 'Desistente', 'Inativado/Movimentado', 'Atendido Precariamente')),
        data_desistencia DATETIME,
        motivo_desistencia TEXT,
        observacoes TEXT,
        FOREIGN KEY (id_militar) REFERENCES militares(id_militar)
    );

    CREATE TABLE IF NOT EXISTS ocupacoes_permissoes (
        id_ocupacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pnr INTEGER NOT NULL,
        id_militar INTEGER NOT NULL,
        id_requerimento INTEGER,
        tipo_ocupacao TEXT NOT NULL DEFAULT 'Regular' 
            CHECK (tipo_ocupacao IN ('Regular', 'Funcional', 'A Título Precário', 'Coletiva')),
        data_inicio_vigencia TEXT NOT NULL,
        data_entrega_chaves TEXT,
        diex_implantacao TEXT,
        nota_boletim_ocupacao TEXT,
        status_ocupacao TEXT NOT NULL DEFAULT 'Ativa' CHECK (status_ocupacao IN ('Ativa', 'Encerrada', 'Irregular')),
        data_encerramento TEXT,
        motivo_encerramento TEXT,
        FOREIGN KEY (id_pnr) REFERENCES pnrs(id_pnr),
        FOREIGN KEY (id_militar) REFERENCES militares(id_militar),
        FOREIGN KEY (id_requerimento) REFERENCES requerimentos_fila(id_requerimento)
    );

    CREATE TABLE IF NOT EXISTS vistorias_desocupacoes (
        id_vistoria INTEGER PRIMARY KEY AUTOINCREMENT,
        id_ocupacao INTEGER NOT NULL,
        finalidade TEXT NOT NULL CHECK (finalidade IN ('Ocupação', 'Desocupação')),
        data_vistoria TEXT NOT NULL,
        nome_vistoriador TEXT NOT NULL,
        posto_vistoriador TEXT NOT NULL,
        nome_fiscal_adm TEXT NOT NULL,
        leitura_hidrometro TEXT,
        contrato_energia TEXT,
        fato_gerador_desocupacao TEXT,
        nota_boletim_desocupacao TEXT,
        om_destino_militar TEXT,
        possui_avarias INTEGER DEFAULT 0,
        valor_reparos_avarias REAL DEFAULT 0.0,
        concordou_valor_reparos INTEGER DEFAULT 1,
        ocupacao_menos_2_anos INTEGER DEFAULT 0,
        valor_ressarcimento_pintura REAL DEFAULT 0.0,
        quidagem_debitos_concessionarias INTEGER DEFAULT 0,
        observacoes_vistoria TEXT,
        FOREIGN KEY (id_ocupacao) REFERENCES ocupacoes_permissoes(id_ocupacao)
    );
    """)
    
    cursor.execute("SELECT COUNT(*) FROM usuarios_adm")
    if cursor.fetchone()[0] == 0:
        pass_admin = hash_password("pnr2026")
        pass_gestor = hash_password("gestor2026")
        cursor.execute("INSERT INTO usuarios_adm (login, senha_hash, nome_completo, perfil) VALUES ('admin', ?, 'Administrador Geral da Prefeitura Militar', 'Administrador Geral')", (pass_admin,))
        cursor.execute("INSERT INTO usuarios_adm (login, senha_hash, nome_completo, perfil) VALUES ('gestor.pnr', ?, 'Gestor de Seção de PNR', 'Gestor de PNR')", (pass_gestor,))
    
    conn.commit()
    conn.close()

init_db()

# Gerenciamento de Sessão de Usuário Adm
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_login' not in st.session_state:
    st.session_state['user_login'] = ""
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ""
if 'user_profile' not in st.session_state:
    st.session_state['user_profile'] = ""

# Header Institucional
st.markdown("""
<div class="eb-header">
    <div>
        <div class="eb-kicker">MINISTÉRIO DA DEFESA • EXÉRCITO BRASILEIRO</div>
        <div class="eb-title">SISPNR — Sistema Integrado de Gestão e Consulta de PNR</div>
        <div class="eb-subtitle">Gestão de imóveis residenciais • Pretendentes • Ocupações • Vistorias</div>
    </div>
    <div class="eb-standard">EB10-IG-04.006 • Portaria nº 2.593/2025</div>
</div>
""", unsafe_allow_html=True)

# Menu Lateral (Modos de Acesso)
st.sidebar.title("📌 Modo de Acesso")
modo_acesso = st.sidebar.radio(
    "Selecione o Portal:",
    ["🔍 Portal do Militar Pretendente (Acesso Público)", "🔐 Área Administrativa (Gestão)"]
)

st.sidebar.markdown("---")

# ==============================================================================
# PORTAL PÚBLICO DE CONSULTA DO MILITAR PRETENDENTE
# ==============================================================================
if modo_acesso == "🔍 Portal do Militar Pretendente (Acesso Público)":
    st.markdown('<div class="main-header">🔍 Portal do Militar Pretendente — Consulta de Fila e Precedência</div>', unsafe_allow_html=True)
    st.caption("Conforme a Portaria nº 2.593/2025 (EB10-IG-04.006, Art. 2º, I, 'a'), é dever da administração dar ampla publicidade à relação de pretendentes à ocupação de PNR.")

    tab_individual, tab_transparencia = st.tabs(["👤 Consulta Individual do Requerimento", "📜 Relação Pública de Pretendentes (Transparência)"])

    with tab_individual:
        st.markdown("""
        <div class="portal-box">
            <h4 style="margin-top:0; color:#1b4332;">Informe seus dados para verificar sua posição na fila de precedência:</h4>
            <p style="font-size:14px; color:#495057;">Sua posição é calculada em tempo real, considerando rigorosamente a data e hora do protocolo do requerimento e as prioridades de cotas PcD (Art. 13).</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([2, 1])
        with c1:
            cpf_busca = st.text_input("Digite seu CPF (somente números):", placeholder="Ex: 12345678901", max_chars=11)
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            btn_buscar = st.button("🔎 Consultar Minha Posição", use_container_width=True)

        if btn_buscar or cpf_busca:
            if not cpf_busca.strip():
                st.warning("Por favor, informe o CPF para realizar a consulta.")
            else:
                conn = get_connection()
                cpf_limpo = cpf_busca.replace(".", "").replace("-", "").strip()
                
                # Busca do militar pelo CPF
                df_mil = pd.read_sql("SELECT * FROM militares WHERE cpf = ?", conn, params=(cpf_limpo,))

                if df_mil.empty:
                    st.error("⚠️ Nenhum cadastro de militar localizado com o CPF informado. Verifique os dígitos ou entre em contato com a Seção de PNR da sua Guarnição.")
                else:
                    mil = df_mil.iloc[0]
                    st.success(f"Militar Localizado: **{mil['posto_graduacao']} {mil['nome_completo']}** ({mil['om_vinculacao']})")

                    # Busca de requerimentos
                    df_reqs = pd.read_sql("""
                        SELECT r.*, 
                               (SELECT COUNT(*) FROM requerimentos_fila r2 
                                WHERE r2.circulo_pretendido = r.circulo_pretendido 
                                  AND r2.status_fila = 'Aguardando' 
                                  AND (r2.prioridade_pcd > r.prioridade_pcd 
                                       OR (r2.prioridade_pcd = r.prioridade_pcd AND r2.data_hora_protocolo < r.data_hora_protocolo))
                               ) + 1 as Posicao_Calculada,
                               (SELECT COUNT(*) FROM requerimentos_fila r3 
                                WHERE r3.circulo_pretendido = r.circulo_pretendido 
                                  AND r3.status_fila = 'Aguardando'
                               ) as Total_Circulo
                        FROM requerimentos_fila r
                        WHERE r.id_militar = ?
                        ORDER BY r.id_requerimento DESC
                    """, conn, params=(mil['id_militar'],))

                    if df_reqs.empty:
                        st.info("ℹ️ Não constam requerimentos de inscrição em PNR registrados para este militar.")
                    else:
                        for idx, req in df_reqs.iterrows():
                            st.markdown(f"### 📄 Requerimento NUP: `{req['nup_eb']}`")
                            col_a, col_b, col_c, col_d = st.columns(4)

                            status = req['status_fila']
                            if status == 'Aguardando':
                                status_html = '<span class="status-badge-amber">Aguardando na Fila</span>'
                            elif status == 'Contemplado':
                                status_html = '<span class="status-badge-green">Contemplado / PNR Atribuído</span>'
                            elif status == 'Desistente':
                                status_html = '<span class="status-badge-red">Desistência Registrada</span>'
                            else:
                                status_html = f'<span class="status-badge-amber">{status}</span>'

                            with col_a:
                                st.markdown(f"**Status Atual:**<br>{status_html}", unsafe_allow_html=True)
                            with col_b:
                                if status == 'Aguardando':
                                    st.markdown(f"**Posição Atual na Fila:**<br><span style='font-size:24px; font-weight:bold; color:#2d6a4f;'>{req['Posicao_Calculada']}º lugar</span> (de {req['Total_Circulo']})", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"**Posição na Fila:**<br>---", unsafe_allow_html=True)
                            with col_c:
                                st.markdown(f"**Círculo Pretendido:**<br>{req['circulo_pretendido']}", unsafe_allow_html=True)
                            with col_d:
                                st.markdown(f"**Data do Protocolo:**<br>{req['data_hora_protocolo']}", unsafe_allow_html=True)

                            # Detalhes adicionais
                            st.markdown("<br>", unsafe_allow_html=True)
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                pcd_txt = "Sim (Prioridade por Cota PcD - Art. 13, §8º)" if req['prioridade_pcd'] == 1 else "Não"
                                st.write(f"• **Prioridade PcD Comprovada:** {pcd_txt}")
                                st.write(f"• **Observações do Processo:** {req['observacoes'] or 'Sem observações'}")
                            with col_info2:
                                if status == 'Desistente':
                                    st.error(f"**Data da Desistência:** {req['data_desistencia']} | **Motivo:** {req['motivo_desistencia']}")
                                elif status == 'Contemplado':
                                    df_oc = pd.read_sql("""
                                        SELECT p.codigo_pnr, p.endereco_completo, o.data_inicio_vigencia, o.diex_implantacao
                                        FROM ocupacoes_permissoes o
                                        JOIN pnrs p ON o.id_pnr = p.id_pnr
                                        WHERE o.id_militar = ? AND o.status_ocupacao = 'Ativa'
                                    """, conn, params=(mil['id_militar'],))
                                    if not df_oc.empty:
                                        oc_data = df_oc.iloc[0]
                                        st.success(f"🏠 **PNR Atribuído:** {oc_data['codigo_pnr']} - {oc_data['endereco_completo']} | **Início:** {oc_data['data_inicio_vigencia']}")

                            st.markdown("---")

                conn.close()

    with tab_transparencia:
        st.markdown('<div class="sub-header">📜 Relação Pública Oficial de Pretendentes por Círculo</div>', unsafe_allow_html=True)
        st.caption("Lista pública anonimizada de precedência por ordem de protocolo e prioridades regulamentares (EB10-IG-04.006).")

        conn = get_connection()
        circulo_pub = st.selectbox("Selecione o Círculo Hierárquico para Consulta Pública:", ["Capitão/Tenente", "Subtenente/Sargento", "Oficial Superior", "Oficial-General", "Cabo/Soldado"])

        df_pub = pd.read_sql("""
            SELECT 
                ROW_NUMBER() OVER (
                    ORDER BY r.prioridade_pcd DESC, r.data_hora_protocolo ASC
                ) as Posicao,
                m.posto_graduacao as Posto_Graduacao,
                SUBSTR(m.nome_completo, 1, 1) || '*** ' || SUBSTR(m.nome_completo, INSTR(m.nome_completo, ' ') + 1, 1) || '***' as Nome_Anonimizado,
                m.om_vinculacao as OM,
                r.nup_eb as NUP_Protocolo,
                r.data_hora_protocolo as Data_Hora_Protocolo,
                CASE WHEN r.prioridade_pcd = 1 THEN 'Sim (Prioritário)' ELSE 'Não' END as Prioridade_PcD
            FROM requerimentos_fila r
            JOIN militares m ON r.id_militar = m.id_militar
            WHERE r.status_fila = 'Aguardando' AND r.circulo_pretendido = ?
            ORDER BY r.prioridade_pcd DESC, r.data_hora_protocolo ASC
        """, conn, params=(circulo_pub,))

        if not df_pub.empty:
            st.dataframe(df_pub, use_container_width=True, hide_index=True)
        else:
            st.info("Não há militares aguardando na fila deste círculo no momento.")

        conn.close()

# ==============================================================================
# ÁREA ADMINISTRATIVA (GESTAO - REQUER LOGIN)
# ==============================================================================
else:
    st.markdown('<div class="main-header">🔐 Área Administrativa — Seção de PNR & Prefeitura Militar</div>', unsafe_allow_html=True)

    # Verifica Autenticação
    if not st.session_state['authenticated']:
        st.markdown("""
        <div class="login-shell">
            <div class="login-mark">🔐</div>
            <h3 class="login-title">Acesso Restrito</h3>
            <p class="login-copy">Autenticação requerida para operadores da Seção de PNR.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_login"):
            login_user = st.text_input("Usuário de Acesso:", placeholder="Ex: admin")
            login_pass = st.text_input("Senha de Acesso:", type="password")
            btn_login = st.form_submit_button("🔑 Entrar no Sistema", use_container_width=True)

            if btn_login:
                conn = get_connection()
                cursor = conn.cursor()
                pass_hash = hash_password(login_pass)

                cursor.execute("SELECT id_usuario, nome_completo, perfil FROM usuarios_adm WHERE login = ? AND senha_hash = ?", (login_user, pass_hash))
                user_row = cursor.fetchone()

                if user_row:
                    st.session_state['authenticated'] = True
                    st.session_state['user_login'] = login_user
                    st.session_state['user_name'] = user_row[1]
                    st.session_state['user_profile'] = user_row[2]

                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("UPDATE usuarios_adm SET ultimo_login = ? WHERE id_usuario = ?", (now_str, user_row[0]))
                    conn.commit()
                    conn.close()

                    st.success(f"Acesso concedido! Bem-vindo, {user_row[1]}.")
                    st.rerun()
                else:
                    conn.close()
                    st.error("⚠️ Usuário ou senha inválidos. Tente novamente.")

        st.info("💡 **Credenciais de Demonstração:**\n- **Administrador:** `admin` / `pnr2026`\n- **Gestor de PNR:** `gestor.pnr` / `gestor2026`")

    else:
        # Usuário Autenticado - Painel Completo
        st.sidebar.success(f"👤 **Conectado:** {st.session_state['user_name']} | **Perfil:** {st.session_state['user_profile']}")
        if st.sidebar.button("🚪 Encerrar Sessão (Logout)"):
            st.session_state['authenticated'] = False
            st.session_state['user_login'] = ""
            st.session_state['user_name'] = ""
            st.session_state['user_profile'] = ""
            st.rerun()

        st.sidebar.markdown("---")
        modulo = st.sidebar.radio(
            "Módulos Administrativos:",
            [
                "📊 Dashboard Executivo",
                "📋 Fila de Pretendentes (Precedência)",
                "❌ Gestão de Desistências & Prazos",
                "🏠 Cadastro & Situação de PNRs",
                "🔑 Ocupações & Permissões de Uso",
                "🔍 Vistorias & Acerto de Contas",
                "⚙️ Gestão de Usuários Adm"
            ]
        )

        conn = get_connection()

        # 1. DASHBOARD EXECUTIVO
        if modulo == "📊 Dashboard Executivo":
            st.markdown('<div class="sub-header">📊 Indicadores Gerenciais de PNR</div>', unsafe_allow_html=True)
            
            tot_pnrs = pd.read_sql("SELECT COUNT(*) as QTD FROM pnrs", conn).iloc[0]['QTD']
            tot_ocupados = pd.read_sql("SELECT COUNT(*) as QTD FROM pnrs WHERE status_imovel = 'Ocupado'", conn).iloc[0]['QTD']
            tot_vagos = pd.read_sql("SELECT COUNT(*) as QTD FROM pnrs WHERE status_imovel = 'Pronto/Vago'", conn).iloc[0]['QTD']
            tot_fila = pd.read_sql("SELECT COUNT(*) as QTD FROM requerimentos_fila WHERE status_fila = 'Aguardando'", conn).iloc[0]['QTD']
            tot_pcd = pd.read_sql("SELECT COUNT(*) as QTD FROM requerimentos_fila WHERE status_fila = 'Aguardando' AND prioridade_pcd = 1", conn).iloc[0]['QTD']
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total PNRs</div><div class="kpi-value">{tot_pnrs}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">Ocupados</div><div class="kpi-value" style="color:#d90429;">{tot_ocupados}</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">Vagos</div><div class="kpi-value" style="color:#2b9348;">{tot_vagos}</div></div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">Na Fila</div><div class="kpi-value">{tot_fila}</div></div>', unsafe_allow_html=True)
            with col5:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">Prioridade PcD</div><div class="kpi-value" style="color:#0077b6;">{tot_pcd}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            df_pnrs_sum = pd.read_sql("SELECT tipo as Circulo, status_imovel as Situacao, COUNT(*) as Total FROM pnrs GROUP BY tipo, status_imovel", conn)
            st.dataframe(df_pnrs_sum, use_container_width=True, hide_index=True)

        # 2. FILA DE PRETENDENTES
        elif modulo == "📋 Fila de Pretendentes (Precedência)":
            st.markdown('<div class="sub-header">📋 Gestão da Relação de Pretendentes</div>', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["📌 Visualizar e Gerenciar Fila", "➕ Novo Requerimento"])
            
            with tab1:
                df_fila = pd.read_sql("""
                    SELECT 
                        r.id_requerimento,
                        ROW_NUMBER() OVER (PARTITION BY r.circulo_pretendido ORDER BY r.prioridade_pcd DESC, r.data_hora_protocolo ASC) as Posicao,
                        r.circulo_pretendido as Circulo,
                        CASE WHEN r.prioridade_pcd = 1 THEN 'Sim (Prioritário)' ELSE 'Não' END as Prioridade_PcD,
                        m.posto_graduacao || ' ' || m.nome_completo as Militar,
                        m.cpf as CPF,
                        m.om_vinculacao as OM,
                        r.nup_eb as NUP_Protocolo,
                        r.data_hora_protocolo as Data_Hora_Protocolo,
                        r.status_fila as Status
                    FROM requerimentos_fila r
                    JOIN militares m ON r.id_militar = m.id_militar
                    WHERE r.status_fila = 'Aguardando'
                    ORDER BY r.circulo_pretendido, r.prioridade_pcd DESC, r.data_hora_protocolo ASC
                """, conn)
                st.dataframe(df_fila, use_container_width=True, hide_index=True)

            with tab2:
                df_militares = pd.read_sql("SELECT id_militar, posto_graduacao || ' ' || nome_completo || ' (CPF: ' || cpf || ')' as rotulo FROM militares ORDER BY nome_completo", conn)
                if not df_militares.empty:
                    with st.form("form_req_adm"):
                        mil_sel = st.selectbox("Selecione o Militar:", df_militares['rotulo'].tolist())
                        mil_id = df_militares[df_militares['rotulo'] == mil_sel].iloc[0]['id_militar']
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            nup = st.text_input("NUP / Protocolo EB:", value="64535.019999/2026-10")
                            circ = st.selectbox("Círculo Pretendido:", ["Capitão/Tenente", "Subtenente/Sargento", "Oficial Superior", "Oficial-General", "Cabo/Soldado"])
                        with c2:
                            dt_p = st.date_input("Data Protocolo:", value=date.today())
                            hr_p = st.time_input("Hora Protocolo:", value=datetime.now().time())
                        pcd = st.checkbox("Possui Dependente PcD para Cota de Prioridade (Art. 13, §8º)")
                        obs = st.text_area("Observações:")
                        
                        if st.form_submit_button("✅ Protocolar na Fila"):
                            dt_str = f"{dt_p.strftime('%Y-%m-%d')} {hr_p.strftime('%H:%M:%S')}"
                            cursor = conn.cursor()
                            cursor.execute("INSERT INTO requerimentos_fila (id_militar, nup_eb, data_hora_protocolo, circulo_pretendido, prioridade_pcd, status_fila, observacoes) VALUES (?, ?, ?, ?, ?, 'Aguardando', ?)",
                                           (mil_id, nup, dt_str, circ, 1 if pcd else 0, obs))
                            conn.commit()
                            st.success("Requerimento cadastrado!")
                            st.rerun()

        # 3. DESISTENCIAS & PRAZOS
        elif modulo == "❌ Gestão de Desistências & Prazos":
            st.markdown('<div class="sub-header">❌ Controle de Desistências e Multas de Ocupação</div>', unsafe_allow_html=True)
            df_des = pd.read_sql("""
                SELECT r.id_requerimento, m.posto_graduacao || ' ' || m.nome_completo as Militar,
                       r.circulo_pretendido as Circulo, r.nup_eb as NUP,
                       r.data_desistencia as Data_Desistencia, r.motivo_desistencia as Motivo
                FROM requerimentos_fila r
                JOIN militares m ON r.id_militar = m.id_militar
                WHERE r.status_fila = 'Desistente'
            """, conn)
            st.dataframe(df_des, use_container_width=True, hide_index=True)

        # 4. GESTÃO DE PNRS
        elif modulo == "🏠 Cadastro & Situação de PNRs":
            st.markdown('<div class="sub-header">🏠 Cadastro de Imóveis</div>', unsafe_allow_html=True)
            df_p = pd.read_sql("SELECT * FROM pnrs", conn)
            st.dataframe(df_p, use_container_width=True, hide_index=True)

        # 5. OCUPAÇÃO
        elif modulo == "🔑 Ocupações & Permissões de Uso":
            st.markdown('<div class="sub-header">🔑 Permissões de Uso Vigentes</div>', unsafe_allow_html=True)
            df_o = pd.read_sql("""
                SELECT p.codigo_pnr as PNR, m.posto_graduacao || ' ' || m.nome_completo as Permissionario,
                       o.data_inicio_vigencia as Inicio, o.diex_implantacao as DIEx
                FROM ocupacoes_permissoes o
                JOIN pnrs p ON o.id_pnr = p.id_pnr
                JOIN militares m ON o.id_militar = m.id_militar
                WHERE o.status_ocupacao = 'Ativa'
            """, conn)
            st.dataframe(df_o, use_container_width=True, hide_index=True)

        # 6. VISTORIAS
        elif modulo == "🔍 Vistorias & Acerto de Contas":
            st.markdown('<div class="sub-header">🔍 Laudos de Vistoria de Ocupação / Desocupação</div>', unsafe_allow_html=True)
            df_v = pd.read_sql("""
                SELECT v.id_vistoria, v.finalidade, v.data_vistoria, p.codigo_pnr as PNR,
                       v.fato_gerador_desocupacao as Fato_Gerador, v.valor_reparos_avarias as Avarias_RS
                FROM vistorias_desocupacoes v
                JOIN ocupacoes_permissoes o ON v.id_ocupacao = o.id_ocupacao
                JOIN pnrs p ON o.id_pnr = p.id_pnr
            """, conn)
            st.dataframe(df_v, use_container_width=True, hide_index=True)

        # 7. GESTÃO DE USUÁRIOS
        elif modulo == "⚙️ Gestão de Usuários Adm":
            st.markdown('<div class="sub-header">⚙️ Gestão de Operadores do Sistema</div>', unsafe_allow_html=True)
            df_u = pd.read_sql("SELECT id_usuario, login, nome_completo, perfil, ultimo_login FROM usuarios_adm", conn)
            st.dataframe(df_u, use_container_width=True, hide_index=True)

            with st.expander("➕ Cadastrar Novo Administrador/Operador"):
                with st.form("form_new_adm"):
                    n_login = st.text_input("Login de Acesso:")
                    n_nome = st.text_input("Nome Completo / Posto:")
                    n_senha = st.text_input("Senha:", type="password")
                    n_perfil = st.selectbox("Perfil:", ["Gestor de PNR", "Administrador Geral", "Auditor/Fiscal"])
                    if st.form_submit_button("💾 Salvar Usuário"):
                        if n_login and n_senha:
                            cursor = conn.cursor()
                            cursor.execute("INSERT INTO usuarios_adm (login, senha_hash, nome_completo, perfil) VALUES (?, ?, ?, ?)",
                                           (n_login, hash_password(n_senha), n_nome, n_perfil))
                            conn.commit()
                            st.success("Administrador criado!")
                            st.rerun()

        st.markdown("""
        <div style="margin-top:34px;padding-top:14px;border-top:1px solid #e2e7e3;color:#7a847d;font-size:11px;text-align:center;">
            SISPNR • Gestão Administrativa de PNR • Ambiente institucional
        </div>
        """, unsafe_allow_html=True)

        conn.close()
