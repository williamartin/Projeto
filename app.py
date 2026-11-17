import streamlit as st
from datetime import datetime
from google import genai
from google.genai import types
import urllib.parse
from fpdf import FPDF

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
    modulo = st.radio("Escolha a ferramenta:", ["🎾 Treino de Tênis", "💪 Personal Training"])

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
    st.markdown("### 🏋️ Planejamento de Musculação & Periodização Profissional")

    with st.form("form_personal"):
        # 1. Dados Biométricos e Anamnese
        st.markdown("#### 👤 Perfil e Anamnese do Aluno")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            nome_aluno_p = st.text_input("Nome do Aluno", placeholder="Ex: Mariana Souza")
        with col2:
            idade_p = st.number_input("Idade", min_value=12, max_value=100, value=30)
        with col3:
            peso_p = st.number_input("Peso (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.5)
        with col4:
            altura_p = st.number_input("Altura (cm)", min_value=100, max_value=230, value=170)

        col_anam1, col_anam2 = st.columns(2)
        with col_anam1:
            historico_p = st.selectbox(
                "Histórico Recente de Treino",
                ["Treinando continuamente há mais de 6 meses", "Iniciando agora (Sedentário)", "Retornando após pausa (Destreinado)", "Atleta / Alto Rendimento"]
            )
        with col_anam2:
            recuperacao_p = st.selectbox(
                "Qualidade do Sono e Estresse",
                ["Sono bom e estresse controlado", "Sono irregular / Estresse moderado", "Pouco sono / Estresse elevado (Ajustar volume)"]
            )

        # 2. Periodização, Rotina e Cardio
        st.markdown("---")
        st.markdown("#### 📅 Estrutura e Periodização (Mesociclo)")
        col5, col6, col7 = st.columns(3)
        with col5:
            objetivo_p = st.selectbox("Objetivo Principal", ["Hipertrofia", "Emagrecimento / Definição", "Força Máxima", "Resistência Muscular", "Saúde e Longevidade"])
            mesociclo_p = st.selectbox("Duração do Mesociclo", ["4 semanas", "6 semanas", "8 semanas", "12 semanas"])
        with col6:
            experiencia_p = st.selectbox("Nível Técnico", ["Iniciante", "Intermediário", "Avançado"])
            frequencia_p = st.selectbox("Frequência Semanal", ["2x na semana", "3x na semana", "4x na semana", "5x na semana", "6x na semana"])
        with col7:
            duracao_p = st.number_input("Tempo por Sessão (min)", min_value=30, max_value=180, value=60, step=10)
            cardio_p = st.selectbox("Protocolo de Cardio", ["Não incluir cardio", "LISS (Moderado contínuo pós-treino)", "HIIT (Alta intensidade pós-treino)", "Cardio em horário separado / dias off"])

        col_loc1, col_loc2 = st.columns(2)
        with col_loc1:
            local_p = st.selectbox("Local de Treino", ["Academia", "Treino em Casa / Condomínio", "Estúdio / Box"])
        with col_loc2:
            equipamentos_p = st.multiselect(
                "Equipamentos Disponíveis",
                ["Máquinas e Cabos", "Halteres", "Barra e Anilhas", "Elásticos", "Peso do Corpo", "Kettlebell"],
                default=["Máquinas e Cabos", "Halteres", "Barra e Anilhas"]
            )

        # 3. Divisão Muscular Estilo MuscleWiki
        st.markdown("---")
        st.markdown("#### 🎯 Divisão por Grupos Musculares (Superiores e Inferiores)")

        tipo_divisao_p = st.radio(
            "Modelo de Organização:",
            ["Superiores e Inferiores Separados (Upper / Lower)", "Divisão Tradicional (ABC / ABCD)", "Foco Específico nos Músculos Selecionados"],
            horizontal=True
        )

        col_sup, col_inf = st.columns(2)
        with col_sup:
            st.markdown("**💪 Membros Superiores e Core**")
            musculos_sup_p = st.multiselect(
                "Grupos Superiores:",
                ["Peitoral", "Costas (Dorsais)", "Ombros (Deltoides)", "Bíceps", "Tríceps", "Antebraço", "Abdômen / Core"],
                default=["Peitoral", "Costas (Dorsais)", "Ombros (Deltoides)", "Bíceps", "Tríceps"]
            )

        with col_inf:
            st.markdown("**🦵 Membros Inferiores**")
            musculos_inf_p = st.multiselect(
                "Grupos Inferiores:",
                ["Quadríceps", "Posterior de Coxa (Isquiotibiais)", "Glúteos", "Panturrilhas", "Adutores / Abdutores"],
                default=["Quadríceps", "Posterior de Coxa (Isquiotibiais)", "Glúteos", "Panturrilhas"]
            )

            st.markdown("---")
            st.markdown("#### 🩺 Avaliação Clínica, Patologias e Restrições")
        
        condicoes_p = st.multiselect(
            "Selecione condições de saúde ou lesões diagnosticadas:",
            [
                "Nenhuma condição especial",
                "Hérnia de Disco Lombar (L4-L5 / L5-S1)",
                "Hérnia de Disco Cervical",
                "Condromalácia Patelar / Dor no Joelho",
                "Lesão no Ombro (Tendinite / Bursite / Manguito)",
                "Hipertensão Arterial (Pressão Alta)",
                "Diabetes Tipo 1 ou 2",
                "Osteopenia / Osteoporose",
                "Desvios Posturais (Escoliose / Hiperlordose)",
                "Gestante ou Pós-Parto",
                "Fibromialgia / Fadiga Crônica"
            ],
            default=["Nenhuma condição especial"]
        )

        lesoes_p = st.text_area(
            "Detalhes clínicos, medicamentos ou liberação médica:",
            placeholder="Ex: Protusão em L5-S1 sem dor aguda no momento; toma losartana; liberado pelo ortopedista..."
        )


        submit_p = st.form_submit_button("Gerar Periodização Completa", type="primary")

    if submit_p:
        if not api_key:
            st.error("Insira sua API Key na barra lateral.")
        elif not nome_aluno_p:
            st.warning("Preencha o Nome do Aluno.")
        else:
            with st.spinner("Calculando volume, RPE e estruturando mesociclo..."):
                try:
                    client = genai.Client(api_key=api_key)

                    sys_prompt_personal = """
                    Você é um Personal Trainer e Fisiologista do Exercício de elite.
                    Crie periodizações seguras, baseadas em ciência, biomecânica e controle de carga (RPE/RIR).
                    """

                    user_prompt_personal = f"""
                    Elabore um planejamento completo de treino para:
                    - Aluno: {nome_aluno_p} | Idade: {idade_p} anos | Peso: {peso_p} kg | Altura: {altura_p} cm
                    - Histórico: {historico_p} | Recuperação/Sono: {recuperacao_p}
                    - Objetivo: {objetivo_p} | Nível Técnico: {experiencia_p}
                    - Duração do Mesociclo: {mesociclo_p} | Frequência: {frequencia_p} | Duração por sessão: {duracao_p} min
                    - Cardio: {cardio_p}
                    - Local: {local_p} | Equipamentos: {', '.join(equipamentos_p)}
                    - Condições de Saúde / Patologias: {', '.join(condicoes_p)}
                    - Detalhes Clínicos / Observações: {lesoes_p if lesoes_p else 'Nenhum detalhe adicional'}
                    - Organização: {tipo_divisao_p}
                    - Superiores: {', '.join(musculos_sup_p)}
                    - Inferiores: {', '.join(musculos_inf_p)}

                    REGRAS DE SEGURANÇA CLÍNICA (OBRIGATÓRIO):
                    - Se houver patologias listadas (como Hérnia de Disco, Condromalácia, Hipertensão, etc.), crie uma seção inicial chamada **⚠️ Adaptações Clínicas e Contraindicações** listando exatamente quais exercícios foram evitados (ex: evitar compressão axial/flexão lombar com carga na hérnia, evitar isometria prolongada/Valsalva na hipertensão) e quais exercícios corretivos/estabilizadores (ex: core stability, McGill Big 3) foram incluídos.

                    Estrutura obrigatória da resposta:
                    1. **⚠️ Adaptações Clínicas e Contraindicações** (caso haja condição selecionada).
                    2. **Resumo da Estratégia & Progressão ({mesociclo_p})**: Progressão dupla e semana de Deload.
                    3. **Aquecimento & Mobilidade (5-8 min)**: 3 exercícios específicos de preparação articular e estabilidade protetora.
                    4. **Divisão dos Treinos**: Separe claramente os treinos (ex: Treino A - Superiores, Treino B - Inferiores). Para CADA exercício informe:
                       - Nome do Exercício e Músculo Alvo
                       - Séries x Repetições | Descanso | Intensidade (RPE ou RIR)
                       - Dica rápida de biomecânica segura adaptada à condição do aluno
                       - Link clicável exato: [🎥 Ver Execução](https://youtube.com) (substitua NOME+DO+EXERCICIO usando sinais de +).
                    5. **Protocolo de Cardio**: Tempo e intensidade ({cardio_p}).
                    """

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=user_prompt_personal,
                        config=types.GenerateContentConfig(
                            system_instruction=sys_prompt_personal
                        )
                    )

                    texto_ficha = response.text
                    st.success("Periodização gerada com sucesso!")
                    st.markdown("---")
                    st.markdown(texto_ficha)

                    # Função para gerar PDF limpo
                    def criar_pdf(texto, aluno):
                        pdf = FPDF()
                        pdf.add_page()
                        
                        pdf.set_fill_color(30, 41, 59)
                        pdf.set_text_color(255, 255, 255)
                        pdf.set_font("Helvetica", "B", 15)
                        pdf.cell(0, 12, "WILLIAM - PERIODIZACAO DE TREINO", ln=True, align="C", fill=True)
                        
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font("Helvetica", "I", 10)
                        cabecalho_limpo = aluno.encode("latin-1", "ignore").decode("latin-1")
                        pdf.cell(0, 8, f"Aluno(a): {cabecalho_limpo} | Objetivo: {objetivo_p} | Ciclo: {mesociclo_p}", ln=True, align="C")
                        pdf.ln(5)

                        return pdf.output(dest="S").encode("latin-1")


                    pdf_bytes = criar_pdf(texto_ficha, nome_aluno_p)

                    # Botões de Entrega Profissional (PDF, TXT e WhatsApp)
                    st.markdown("---")
                    st.markdown("#### 📤 Entrega e Compartilhamento")
                    col_btn1, col_btn2, col_btn3 = st.columns(3)

                    with col_btn1:
                        st.download_button(
                            label="📄 Baixar Ficha em PDF",
                            data=pdf_bytes,
                            file_name=f"Ficha_{nome_aluno_p.replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )

                    with col_btn2:
                        st.download_button(
                            label="📝 Baixar em Texto (.txt)",
                            data=texto_ficha,
                            file_name=f"Ficha_{nome_aluno_p.replace(' ', '_')}.txt"
                        )

                    with col_btn3:
                        resumo_wpp = f"Olá {nome_aluno_p}! Segue o resumo do seu novo planejamento de treino ({objetivo_p} - {mesociclo_p}):\n\n" + texto_ficha[:1500] + "\n\n(Consulte o PDF completo para todos os detalhes e links de vídeo!)"
                        link_wpp = f"https://wa.me/?text={urllib.parse.quote(resumo_wpp)}"
                        st.link_button("📲 Enviar via WhatsApp", link_wpp)

                except Exception as e:
                    st.error(f"Erro ao gerar periodização: {e}")
