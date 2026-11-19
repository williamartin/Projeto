import streamlit as st
from datetime import datetime
from google import genai
from google.genai import types
import urllib.parse
from fpdf import FPDF
import csv
import os

import sqlite3

def get_conn():
    conn = sqlite3.connect("academia.db")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            objetivo TEXT,
            condicao_clinica TEXT,
            observacoes_medicas TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS treinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT,
            divisao TEXT,
            foco_divisao TEXT,
            grupo_muscular TEXT,
            ordem INTEGER,
            exercicio TEXT,
            series INTEGER,
            repeticoes INTEGER,
            cadencia TEXT,
            descanso INTEGER,
            tecnica TEXT,
            instrucoes TEXT,
            adaptacao_clinica TEXT,
            video_url TEXT
        )
    """)
    conn.commit()
    return conn
def mostrar_area_aluno():
    st.subheader("📱 Área do Aluno")
    conn = get_conn()
    alunos = [row["nome"] for row in conn.execute("SELECT nome FROM alunos ORDER BY nome").fetchall()]

    if not alunos:
        st.info("Nenhum aluno cadastrado ainda.")
    else:
        aluno_sel = st.selectbox("Selecione seu nome:", alunos, key="sel_aluno_area")
        treinos = conn.execute(
            "SELECT divisao, foco_divisao, grupo_muscular, ordem, exercicio, series, repeticoes, cadencia, descanso, tecnica, instrucoes, adaptacao_clinica, video_url FROM treinos WHERE aluno = ? ORDER BY divisao, ordem",
            (aluno_sel,)
        ).fetchall()

        if not treinos:
            st.warning("Você ainda não possui treinos prescritos.")
        else:
            divisoes = list(dict.fromkeys([t["divisao"] for t in treinos]))
            div_sel = st.selectbox("Escolha o treino do dia:", divisoes, key="sel_div_aluno")
            treino_dia = [t for t in treinos if t["divisao"] == div_sel]

            st.markdown(f"### {div_sel} — Foco: {treino_dia['foco_divisao']}")
            for t in treino_dia:
                with st.expander(f"{t['ordem']}. {t['exercicio']} ({t['series']}x{t['repeticoes']})", expanded=True):
                    st.write(f"**Grupo:** {t['grupo_muscular']} | **Cadência:** {t['cadencia']} | **Descanso:** {t['descanso']}s | **Técnica:** {t['tecnica']}")
                    if t["instrucoes"]:
                        st.write(f"**Execução:** {t['instrucoes']}")
                    if t["adaptacao_clinica"]:
                        st.warning(f"**Adaptação Clínica:** {t['adaptacao_clinica']}")
                    if t["video_url"]:
                        st.video(t["video_url"])
    conn.close()


# Configuração da página
st.set_page_config(page_title="William - Professor de Tênis & Personal", page_icon="🎾", layout="wide")

# Barra lateral para configuração da Chave de API e Navegação
with st.sidebar:
    st.header("⚙️ Configurações")
    try:
        default_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        default_key = ""
    api_key = st.text_input("Gemini API Key", value=default_key, type="password")
    st.info("Insira sua chave do google AI Studio para ativar a IA.")
    
    st.markdown("---")
    st.header("📌 Módulos do Sistema")
    modulo = st.radio("Módulos do Sistema:",["🎾 Treino de Tênis", "💪 Personal Training", "💰 Controle Financeiro"]
)

# Título principal dinâmico
st.markdown(
    """
    <div style="background-color:#1E293B; padding:18px; border-radius:10px; margin-bottom:15px;">
        <h2 style="color:#FFFFFF; margin:0;">🏆 William — Treinamento Personalizado</h2>
        <p style="color:#CBD5E1; margin:5px 0 0 0;">Consultoria Esportiva • Tênis e Preparação Física</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Pegando data e hora atual no fuso do Brasil
data_atual = datetime.now().strftime("%d/%m/%Y")
hora_atual = datetime.now().strftime("%H:%M")
if api_key:
    client = genai.Client(api_key=api_key) 

# ==========================================
# MÓDULO 1: TREINO DE TÊNIS
# ==========================================
if modulo == "🎾 Treino de Tênis":
    st.markdown("### 🎾 Planejamento Técnico, Tático e Físico de Tênis")

    with st.form("form_tenis"):
        st.markdown("#### 👤 Perfil do Aluno / Atleta")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            nome_aluno_t = st.text_input("Nome do Tenista", placeholder="Ex: Lucas Oliveira")
        with col2:
            idade_t = st.number_input("Idade", min_value=5, max_value=95, value=28)
        with col3:
            mao_t = st.selectbox("Mão Dominante", ["Destro", "Canhoto"])
        with col4:
            backhand_t = st.selectbox("Tipo de Backhand", ["Duas mãos", "Uma mão"])

        col5, col6, col7 = st.columns(3)
        with col5:
            nivel_t = st.selectbox(
                "Nível Técnico",
                ["Iniciante (Primeiros contatos)", "Intermediário (Troca bolas e joga games)", "Avançado (Controle de spin e tática)", "Competitivo / Torneios"]
            )
            piso_t = st.selectbox("Tipo de Quadra", ["Saibro (Terra Batida)", "Quadra Rápida (Dura / Lisonda)", "Grama / Sintética"])
        with col6:
            formato_t = st.selectbox("Formato da Aula", ["Individual (Particular)", "Dupla (2 alunos)", "Grupo / Clínica (3 a 4 alunos)", "Treino no Paredão / Sozinho"])
            duracao_t = st.number_input("Duração da Sessão (min)", min_value=30, max_value=180, value=60, step=15)
        with col7:
            objetivo_t = st.selectbox(
                "Objetivo Principal",
                ["Consistência e Regularidade", "Construção de Ponto e Tática", "Potência e Spin (Topspin/Slice)", "Preparação para Torneio / Jogo", "Condicionamento Físico Específico"]
            )
            materiais_t = st.multiselect(
                "Materiais Disponíveis",
                ["Cesto de Bolas", "Cones e Alvos", "Escada de Agilidade", "Elásticos / Mini-bands", "Bola Medicinal", "Nenhum (Apenas raquete e bolas)"],
                default=["Cesto de Bolas", "Cones e Alvos"]
            )

        st.markdown("---")
        st.markdown("#### 🎯 Fundamentos e Situações de Jogo")

        col_tec, col_tat = st.columns(2)
        with col_tec:
            fundamentos_t = st.multiselect(
                "Golpes / Fundamentos Foco:",
                ["Forehand (Base)", "Backhand (Base)", "Saque (1º e 2º serviço)", "Devolução de Saque", "Voleios (Forehand/Backhand)", "Smash", "Approach e Jogo de Rede", "Drop Shot / Lob"],
                default=["Forehand (Base)", "Backhand (Base)", "Saque (1º e 2º serviço)"]
            )

        with col_tat:
            fisico_t = st.multiselect(
                "Movimentação e Físico em Quadra:",
                ["Split-Step e Tempo de Reação", "Deslocamento Lateral e Recuperação", "Jogo de Pés Aberto/Fechado (Stances)", "Resistência Anaeróbia (Pontos longos)", "Prevenção de Lesões (Ombro/Cotovelo)"],
                default=["Split-Step e Tempo de Reação", "Deslocamento Lateral e Recuperação"]
            )

        obs_t = st.text_area("Observações Técnicas ou Limitações Físicas", placeholder="Ex: Dificuldade no lançamento da bola no saque, histórico de epicondilite...")

        submit_t = st.form_submit_button("Gerar Plano de Aula de Tênis", type="primary")

    if submit_t:
        if not api_key:
            st.error("Insira sua API Key na barra lateral.")
        elif not nome_aluno_t:
            st.warning("Preencha o Nome do Tenista.")
        else:
            with st.spinner("Estruturando drills, tática e preparação física em quadra..."):
                try:
                    client = genai.Client(api_key=api_key)

                    sys_prompt_tenis = """
                    Você é um Treinador de Tênis certificado (CBT / ITF) e preparador físico especializado em esportes de raquete.
                    Crie planos de aula dinâmicos, progressivos e com drills práticos para quadra.
                    """

                    user_prompt_tenis = f"""
                    Elabore um plano de aula completo de tênis para:
                    - Tenista: {nome_aluno_t} | Idade: {idade_t} anos | Mão: {mao_t} | Backhand: {backhand_t}
                    - Nível: {nivel_t} | Piso: {piso_t}
                    - Formato: {formato_t} | Duração total: {duracao_t} minutos
                    - Objetivo Principal: {objetivo_t}
                    - Materiais: {', '.join(materiais_t)}
                    - Fundamentos Foco: {', '.join(fundamentos_t)}
                    - Movimentação/Físico: {', '.join(fisico_t)}
                    - Observações/Lesões: {obs_t if obs_t else 'Nenhuma'}

                    Estrutura obrigatória da resposta (divida os minutos proporcionalmente aos {duracao_t} min totais):
                    1. **Aquecimento & Coordenação (10-15 min)**: Mobilidade articular específica (ombro, punho, quadril) + mini-tênis com foco em controle e split-step.
                    2. **Bloco Técnico - Drills de Cesto / Alimentação (20-25 min)**: Crie 2 a 3 drills práticos para os fundamentos escolhidos ({', '.join(fundamentos_t)}), explicando posicionamento na quadra, alvos e correção biomecânica.
                    3. **Bloco Tático - Situações Reais de Jogo (15-20 min)**: Crie 2 dinâmicas de pontos jogados adaptadas ao piso ({piso_t}) e ao objetivo ({objetivo_t}).
                    4. **Condicionamento Específico & Volta à Calma (5-10 min)**: Exercícios curtos de movimentação/prevenção e alongamento final.
                    5. **Referências Visuais**: Para os 2 principais fundamentos trabalhados, inclua links clicáveis exatamente neste formato:
                       [🎥 Ver Técnica no YouTube](https://youtube.com) (substitua FUNDAMENTO pelo nome do golpe separado por +).
                    """

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=user_prompt_tenis,
                        config=types.GenerateContentConfig(
                            system_instruction=sys_prompt_tenis
                        )
                    )

                    texto_tenis = response.text
                    st.success("Plano de Aula de Tênis gerado com sucesso!")
                    st.markdown("---")
                    st.markdown(texto_tenis)

                    def criar_pdf_tenis(texto, aluno):
                        pdf = FPDF()
                        pdf.add_page()
                        
                        pdf.set_fill_color(30, 41, 59)
                        pdf.set_text_color(255, 255, 255)
                        pdf.set_font("Helvetica", "B", 15)
                        pdf.cell(0, 12, "WILLIAM - PLANO DE TREINO DE TENIS", ln=True, align="C", fill=True)
                        
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font("Helvetica", "I", 10)
                        cabecalho_limpo = aluno.encode("latin-1", "ignore").decode("latin-1")
                        pdf.cell(0, 8, f"Atleta: {cabecalho_limpo} | Piso: {piso_t} | Foco: {objetivo_t}", ln=True, align="C")
                        pdf.ln(5)

                        return pdf.output(dest="S").encode("latin-1")

                    pdf_tenis_bytes = criar_pdf_tenis(texto_tenis, nome_aluno_t)

                    st.markdown("---")
                    st.markdown("#### 📤 Entrega e Compartilhamento")
                    col_t1, col_t2, col_t3 = st.columns(3)

                    with col_t1:
                        st.download_button(
                            label="📄 Baixar Plano em PDF",
                            data=pdf_tenis_bytes,
                            file_name=f"Tenis_{nome_aluno_t.replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )

                    with col_t2:
                        st.download_button(
                            label="📝 Baixar em Texto (.txt)",
                            data=texto_tenis,
                            file_name=f"Tenis_{nome_aluno_t.replace(' ', '_')}.txt"
                        )

                    with col_t3:
                        resumo_wpp_t = f"Olá {nome_aluno_t}! Segue o resumo do seu plano de aula de Tênis ({piso_t} - {objetivo_t}):\n\n" + texto_tenis[:1500] + "\n\n(Consulte o PDF completo para todos os drills e links de técnica!)"
                        link_wpp_t = f"https://wa.me{urllib.parse.quote(resumo_wpp_t)}"
                        st.link_button("📲 Enviar via WhatsApp", link_wpp_t)

                except Exception as e:
                    st.error(f"Erro ao gerar plano de tênis: {e}")

# ==========================================
# MÓDULO 2: PERSONAL TRAINING
# ==========================================
elif modulo == "💪 Personal Training":
    perfil_p = st.radio("Modo de Acesso:", ["🏋️ Personal", "📱 Aluno"], horizontal=True)
    st.markdown("---")
    if "Aluno" in perfil_p:
        mostrar_area_aluno()
    

    elif perfil_p == "🏋️ Personal":
        t_ia, t1, t2, t3 = st.tabs([
            "🤖 Gerar com IA",
            "1️⃣ Cadastrar Aluno",
            "2️⃣ Prescrever Treino (Manual)",
            "3️⃣ Fichas Ativas"
        ])

        # --- ABA 0: GERADOR COM IA ---
        with t_ia:
            st.subheader("🤖 Prescrição Inteligente com IA")
            with st.form("form_personal"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    nome_aluno_p = st.text_input("Nome do Aluno")
                with col2:
                    idade_p = st.number_input("Idade", min_value=10, max_value=100, value=30)
                with col3:
                    sexo_p = st.selectbox("Sexo", ["Masculino", "Feminino"])

                col4, col5, col6 = st.columns(3)
                with col4:
                    peso_p = st.number_input("Peso (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.5)
                with col5:
                    altura_p = st.number_input("Altura (cm)", min_value=120, max_value=230, value=170)
                with col6:
                    nivel_p = st.selectbox("Nível de Experiência", ["Iniciante", "Intermediário", "Avançado"])

                col7, col8 = st.columns(2)
                with col7:
                    objetivo_p = st.selectbox(
                        "Objetivo Principal",
                        ["Hipertrofia", "Emagrecimento", "Condicionamento Físico", "Força", "Reabilitação / Saúde"]
                    )
                with col8:
                    local_treino_p = st.selectbox(
                        "Local / Estrutura de Treino",
                        ["Academia Completa", "Condomínio / Academia Básica", "Em Casa (Peso do Corpo / Elásticos)"]
                    )

                dias_treino_p = st.slider("Dias de treino na semana", 1, 7, 4)
                tempo_sessao_p = st.slider("Tempo disponível por sessão (minutos)", 20, 120, 60, step=10)
                escopo_tipo = st.radio(
                    "Tipo de Prescrição",
                    ["Ficha de Treino Semanal", "Periodização Mensal Completa"],
                    horizontal=True
                )
                patologia_p = st.text_area(
                    "Patologias, lesões, dores articulares ou restrições médicas",
                    placeholder="Ex: Condromalácia patelar grau II, hérnia de disco L4-L5, hipertensão controlada..."
                )

                gerar_treino = st.form_submit_button("Gerar Prescrição de Treino", type="primary")

            if gerar_treino:
                if not api_key:
                    st.error("Insira sua API Key na barra lateral.")
                elif not nome_aluno_p:
                    st.warning("Por favor, informe o nome do aluno.")
                else:
                    with st.spinner("Gerando prescrição técnica de treinamento..."):
                        try:
                            sys_prompt_personal = """Você é um Personal Trainer sênior, especialista em fisiologia do exercício, biomecânica aplicada, cinesiologia e prescrição de treinamento individualizado.
Regras obrigatórias:
1. Estruture o treino de forma clara, técnica e profissional, separando por divisões (ex: Treino A, Treino B, Treino C) conforme a frequência semanal.
2. Para cada exercício, especifique obrigatoriamente: nome do exercício, grupos musculares trabalhados, número de séries, faixa de repetições, tempo de descanso entre séries, cadência sugerida e dicas biomecânicas de execução segura.
3. Nunca substitua o médico ou fisioterapeuta; caso haja patologias ou dores relatadas, priorize a integridade articular, evite movimentos contraindicados e justifique as adaptações."""

                            escopo_pedido = (
                                f"Monte uma ficha de treino semanal completa dividida em {dias_treino_p} sessões de até {tempo_sessao_p} minutos, "
                                f"para o ambiente '{local_treino_p}', focada em {objetivo_p} (nível {nivel_p})."
                                if escopo_tipo == "Ficha de Treino Semanal"
                                else f"Monte uma periodização completa de 4 semanas (microciclos 1 a 4) com {dias_treino_p} treinos semanais de até {tempo_sessao_p} minutos, "
                                f"para o ambiente '{local_treino_p}', focada em {objetivo_p} (nível {nivel_p}), detalhando a progressão de volume e intensidade."
                            )

                            tem_patologia = bool(patologia_p and patologia_p.strip())
                            bloco_clinico_prompt = (
                                f"ATENÇÃO CLÍNICA E BIOMECÂNICA: O aluno apresenta o seguinte quadro clínico/restrição: '{patologia_p}'. "
                                f"Adapte toda a seleção de exercícios para proteger as estruturas afetadas, liste explicitamente quais movimentos tradicionais foram evitados por contraindicação e inclua uma seção final de 'Cuidados e Recomendações Clínicas durante o Treino'."
                                if tem_patologia
                                else "O aluno não relatou patologias, dores ou restrições médicas. Aplique progressão padrão segura com aquecimento articular específico antes de cada sessão."
                            )

                            user_prompt_personal = f"""Crie uma prescrição profissional de treinamento para:
- Aluno: {nome_aluno_p} | Idade: {idade_p} anos | Sexo: {sexo_p}
- Antropometria: Peso {peso_p} kg | Altura {altura_p} cm
- Nível: {nivel_p} | Objetivo: {objetivo_p} | Local: {local_treino_p}

{escopo_pedido}

{bloco_clinico_prompt}"""

                            response = client.models.generate_content(
                                model="gemini-3.5-flash-lite",
                                contents=user_prompt_personal,
                                config=types.GenerateContentConfig(
                                    system_instruction=sys_prompt_personal
                                )
                            )
                            st.success(f"Prescrição gerada com sucesso para {nome_aluno_p}!")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Erro ao gerar prescrição: {e}")

        # --- ABA 1: CADASTRAR ALUNO ---
        with t1:
            with st.form("f_aluno", clear_on_submit=True):
                nome = st.text_input("Nome do Aluno*")
                objetivo = st.selectbox("Objetivo", ["Hipertrofia", "Emagrecimento", "Reabilitação / Saúde", "Força", "Condicionamento"])
                condicao = st.selectbox("Patologia / Restrição*", ["Nenhuma restrição", "Hipertensão Arterial", "Hérnia de Disco / Lombar", "Condromalácia / Joelho", "Lesão de Ombro", "Diabetes", "Outra"])
                obs_med = st.text_area("Detalhes do Laudo / Restrições")
                if st.form_submit_button("💾 Salvar Aluno", use_container_width=True):
                    if nome.strip():
                        conn = get_conn()
                        conn.execute(
                            "INSERT INTO alunos (nome, objetivo, condicao_clinica, observacoes_medicas) VALUES (?,?,?,?)",
                            (nome.strip(), objetivo, condicao, obs_med)
                        )
                        conn.commit()
                        conn.close()
                        st.success(f"Aluno {nome} salvo!")
                else:
                    st.error("Digite o nome.")

        conn = get_conn()
        alunos = conn.execute("SELECT * FROM alunos ORDER BY nome").fetchall()
        conn.close()
        for a in alunos:
            col_info, col_del = st.columns([6, 1])
            with col_info:
                st.info(
                    f"👤 **{a['nome']}** ({a['objetivo']}) | 🩺 "
                    f"**{a['condicao_clinica']}** — {a['observacoes_medicas']}"
                )
            with col_del:
                if st.button("🗑️", key=f"del_aluno_{a['id']}"):
                        conn = get_conn()
                        conn.execute("DELETE FROM alunos WHERE id = ?", (a['id'],))
                        conn.execute("DELETE FROM treinos WHERE aluno = ?", (a['nome'],))
                        conn.commit()
                        conn.close()
                        st.rerun()

        # --- ABA 2: PRESCREVER TREINO MANUAL ---
        with t2:
            conn = get_conn()
            alunos = conn.execute("SELECT * FROM alunos ORDER BY nome").fetchall()
            conn.close()

            if not alunos:
                st.warning("Cadastre um aluno na aba '1️⃣ Cadastrar Aluno' primeiro.")
            else:
                sel = st.selectbox("Aluno:", [a["nome"] for a in alunos])
                with st.form("f_treino_manual", clear_on_submit=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        div = st.selectbox("Divisão", ["Treino A", "Treino B", "Treino C", "Treino D", "Treino E", "Full Body"])
                        grp = st.selectbox("Grupo Muscular", ["Peito", "Costas", "Ombros", "Bíceps", "Tríceps", "Quadríceps", "Posterior de Coxa", "Glúteos", "Panturrilha", "Abdômen", "Cardio"])
                        ex_nome = st.selectbox("Nome do Exercício", ["Supino Reto", "Supino Inclinado", "Crucifixo", "Puxada Frontal", "Remada Curvada", "Remada Baixa", "Desenvolvimento", "Elevação Lateral", "Rosca Direta", "Tríceps Pulley", "Agachamento Livre", "Leg Press 45", "Cadeira Extensora", "Mesa Flexora", "Elevação Pélvica", "Panturrilha em Pé", "Abdominal Supra"])

            if "Aluno" in perfil_p:
                mostrar_area_aluno()
                

                    
elif modulo == "💰 Controle Financeiro":
    st.markdown("### 💰 Gestão Financeira & Fluxo de Caixa")

    ARQUIVO_FIN = "financeiro_william.csv"
    COLUNAS = ["Tipo", "Data", "Nome_Descricao", "Modalidade_Categoria", "Plano", "Valor", "Status", "Observacoes"]

    def carregar_dados():
        if not os.path.exists(ARQUIVO_FIN):
            return []
        with open(ARQUIVO_FIN, mode="r", encoding="utf-8") as f:
            leitor = csv.DictReader(f)
            dados = []
            for linha in leitor:
                linha["Valor"] = float(linha["Valor"])
                dados.append(linha)
            return dados

    def salvar_dados(lista_dados):
        with open(ARQUIVO_FIN, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=COLUNAS)
            escritor.writeheader()
            escritor.writerows(lista_dados)

    registros = carregar_dados()

    with st.expander("⚙️ Configurar Chave PIX para Cobranças"):
        chave_pix = st.text_input("Sua Chave PIX (CPF, E-mail, Celular ou Aleatória)", placeholder="Ex: william@email.com")

    # 1. KPIs - Indicadores Financeiros
    receitas_pagas = sum(r["Valor"] for r in registros if r["Tipo"] == "Receita" and r["Status"] == "Pago")
    receitas_pendentes = sum(r["Valor"] for r in registros if r["Tipo"] == "Receita" and r["Status"] in ["Pendente", "Atrasado"])
    despesas_totais = sum(r["Valor"] for r in registros if r["Tipo"] == "Despesa")
    lucro_liquido = receitas_pagas - despesas_totais
    alunos_unicos = set(r["Nome_Descricao"] for r in registros if r["Tipo"] == "Receita")
    ticket_medio = (receitas_pagas / len(alunos_unicos)) if len(alunos_unicos) > 0 else 0.0

    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    col_m1.metric("💵 Recebido (Caixa)", f"R$ {receitas_pagas:,.2f}")
    col_m2.metric("⏳ A Receber", f"R$ {receitas_pendentes:,.2f}")
    col_m3.metric("📉 Despesas", f"R$ {despesas_totais:,.2f}")
    col_m4.metric("📈 Lucro Líquido", f"R$ {lucro_liquido:,.2f}")
    col_m5.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.2f}")

    st.markdown("---")

    aba_lancar, aba_tabela, aba_cobrar = st.tabs([
        "➕ Novo Lançamento", "📊 Planilha Editável & Backup", "📲 Cobrança WhatsApp"
    ])

    with aba_lancar:
        tipo_lancamento = st.radio("Tipo de Movimentação:", ["Receita (Aluno)", "Despesa (Custo Operacional)"], horizontal=True)

        with st.form("form_financeiro", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                if tipo_lancamento == "Receita (Aluno)":
                    nome_desc = st.text_input("Nome do Aluno", placeholder="Ex: Carlos Mendes")
                    categoria = st.selectbox("Modalidade", ["Tênis", "Personal Training", "Consultoria Online", "Avaliação Física"])
                else:
                    nome_desc = st.text_input("Descrição da Despesa", placeholder="Ex: 3 Tubos de Bola / Aluguel Quadra")
                    categoria = st.selectbox("Categoria de Custo", ["Material Esportivo (Bolas/Cordas)", "Locação de Quadra/Espaço", "Transporte/Combustível", "Marketing/Sistemas", "Outros"])
            with c2:
                valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f")
                data_venc = st.date_input("Data (Vencimento ou Pagamento)")
            with c3:
                if tipo_lancamento == "Receita (Aluno)":
                    plano = st.selectbox("Plano / Formato", ["Mensal (1x sem)", "Mensal (2x sem)", "Mensal (3x+ sem)", "Pacote 8 Aulas", "Pacote 10 Aulas", "Aula Avulsa"])
                    status = st.selectbox("Status", ["Pago", "Pendente", "Atrasado"])
                else:
                    plano = "Custo Fixo/Variável"
                    status = st.selectbox("Status", ["Pago", "Pendente"])
                obs_fin = st.text_input("Observações", placeholder="Ex: Via PIX, vence dia 10...")

            btn_salvar_fin = st.form_submit_button("Salvar Lançamento", type="primary")

        if btn_salvar_fin:
            if not nome_desc or valor <= 0:
                st.warning("Preencha o nome/descrição e um valor maior que zero.")
            else:
                registros.append({
                    "Tipo": "Receita" if tipo_lancamento == "Receita (Aluno)" else "Despesa",
                    "Data": str(data_venc),
                    "Nome_Descricao": nome_desc,
                    "Modalidade_Categoria": categoria,
                    "Plano": plano,
                    "Valor": float(valor),
                    "Status": status,
                    "Observacoes": obs_fin
                })
                salvar_dados(registros)
                st.success("Lançamento registrado com sucesso!")
                st.rerun()

        with aba_tabela:
            if not registros:
             st.info("Nenhum lançamento cadastrado ainda.")
            else:
             st.markdown("#### 📋 Lista de Movimentações")
            for idx, item in enumerate(registros):
                cor_status = "✅" if item["Status"] == "Pago" else ("⚠️" if item["Status"] == "Atrasado" else "⏳")
                c_info, c_acao1, c_acao2 = st.columns([4, 1.5, 1])
                with c_info:
                    st.write(f"**{cor_status} {item['Nome_Descricao']}** ({item['Modalidade_Categoria']} - {item['Plano']}) | **{item['Data']}** | **R$ {item['Valor']:,.2f}** — *{item['Status']}*")
                with c_acao1:
                    if item["Status"] != "Pago":
                        if st.button("✅ Dar Baixa", key=f"pagar_{idx}"):
                            registros[idx]["Status"] = "Pago"
                            salvar_dados(registros)
                            st.rerun()
                with c_acao2:
                    if st.button("🗑️", key=f"del_{idx}", help="Excluir lançamento"):
                        registros.pop(idx)
                        salvar_dados(registros)
                        st.rerun()
                st.divider()

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if os.path.exists(ARQUIVO_FIN):
                with open(ARQUIVO_FIN, "rb") as f:
                    st.download_button(
                        "📥 Baixar Planilha Backup (.csv)",
                        data=f.read(),
                        file_name="Backup_Financeiro_William.csv",
                        mime="text/csv"
                    )
        with col_b2:
            arquivo_up = st.file_uploader("Restaurar Backup (.csv)", type=["csv"], label_visibility="collapsed")
            if arquivo_up is not None:
                with open(ARQUIVO_FIN, "wb") as f:
                    f.write(arquivo_up.getvalue())
                st.success("Backup restaurado com sucesso!")
                st.rerun()

            with aba_cobrar:
                pendentes = [r for r in registros if r["Tipo"] == "Receita" and r["Status"] in ["Pendente", "Atrasado"]]
        if not pendentes:
            st.success("Nenhum aluno com pagamento pendente ou atrasado no momento!")
        else:
            nomes_pendentes = list(dict.fromkeys(r["Nome_Descricao"] for r in pendentes))
            aluno_sel = st.selectbox("Selecione o aluno para enviar lembrete:", nomes_pendentes)
            dados_aluno = next(r for r in pendentes if r["Nome_Descricao"] == aluno_sel)

            pix_texto = f"\n🔑 Chave PIX: {chave_pix}" if chave_pix else ""
            msg_cobranca = (
                f"Olá {aluno_sel}, tudo bem? Passando para lembrar sobre a sua mensalidade/pacote de "
                f"{dados_aluno['Modalidade_Categoria']} ({dados_aluno['Plano']}) com vencimento em {dados_aluno['Data']}.\n"
                f"💰 Valor: R$ {dados_aluno['Valor']:,.2f}{pix_texto}\n\n"
                f"Qualquer dúvida estou à disposição. Bons treinos!"
            )

            st.text_area("Prévia da mensagem:", value=msg_cobranca, height=140)
            link_wpp_fin = f"https://wa.me{urllib.parse.quote(msg_cobranca)}"
            st.link_button(f"📲 Enviar Cobrança para {aluno_sel} via WhatsApp", link_wpp_fin, type="primary")

                

