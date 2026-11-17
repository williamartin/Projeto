import streamlit as st
from datetime import datetime
from google import genai
from google.genai import types
import urllib.parse
from fpdf import FPDF

# Configuração da página
st.set_page_config(page_title="ProCoach AI - Tênis & Personal", page_icon="🎾", layout="wide")

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
st.title(f"ProCoach AI — Módulo: {modulo}")
st.markdown("Gerador inteligente de periodização, horários e prescrição de treinos.")

# Pegando data e hora atual no fuso do Brasil
data_atual = datetime.now().strftime("%d/%m/%Y")
hora_atual = datetime.now().strftime("%H:%M")

# ==========================================
# MÓDULO 1: TREINO DE TÊNIS
# ==========================================
if modulo == "🎾 Treino de Tênis":
    st.markdown("### Planejamento de Sessão em Quadra")
    
    with st.form("form_tenis"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome_aluno_t = st.text_input("Nome do Aluno/Atleta", placeholder="Ex: Carlos Alberto")
            nivel_t = st.select_slider("Nível Técnico", options=["Iniciante", "Intermediário", "Avançado", "Competitivo"], key="niv_t")
            tipo_quadra = st.selectbox("Tipo de Quadra", ["Saibro (Clay)", "Dura (Hard Court)", "Grama (Grass)", "Beach Tennis / Indoor"])
            
        with col2:
            duracao_t = st.number_input("Duração da Aula (minutos)", min_value=30, max_value=180, value=60, step=15, key="dur_t")
            foco_t = st.text_input("Foco Principal do Treino", placeholder="Ex: Correção de forehand, consistência no fundo, saque e voleio")
            
        obs_t = st.text_area("Observações ou Dificuldades Recorrentes", placeholder="Ex: O aluno está abrindo muito o cotovelo no backhand...", key="obs_t")
        
        submit_t = st.form_submit_button("Gerar Treino de Tênis Completo")

    if submit_t:
        if not api_key:
            st.error("Insira sua API Key na barra lateral.")
        elif not nome_aluno_t or not foco_t:
            st.warning("Preencha o Nome e o Foco Principal.")
        else:
            with st.spinner("Construindo sessão de treinamento e buscando referências visuais..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    sys_prompt_tenis = f"""
                    Você é um Treinador de Tênis profissional de alto rendimento.
                    Sua tarefa é criar um plano de aula prático, dinâmico e estruturado.
                    
                    INFORMAÇÕES DE REGISTRO:
                    - Data de emissão: {data_atual}
                    - Horário de emissão: {hora_atual}
                    
                    REGRA OBRIGATÓRIA PARA VÍDEOS:
                    Para cada drill ou exercício principal indicado, adicione obrigatoriamente um link de pesquisa do YouTube formatado em Markdown (exemplo: [🎥 Ver execução no YouTube](https://www.youtube.com/results?search_query=como+fazer+drill+de+tenis)). O link deve ser uma busca direcionada no YouTube para o exercício específico.
                    
                    O plano deve conter:
                    1. Cabeçalho formatado com Data e Hora.
                    2. Aquecimento e Ativação.
                    3. Drills Técnicos / Sitacionais (com o link de vídeo em cada um).
                    4. Situação de Jogo / Pontuação.
                    5. Volta à Calma.
                    """
                    
                    user_prompt_tenis = f"""
                    Crie um treino de tênis para:
                    - Aluno: {nome_aluno_t}
                    - Nível: {nivel_t}
                    - Superfície: {tipo_quadra}
                    - Duração: {duracao_t} minutos
                    - Foco: {foco_t}
                    - Observações: {obs_t if obs_t else 'Nenhuma'}
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.5-flash-lite',
                        contents=user_prompt_tenis,
                        config=types.GenerateContentConfig(system_instruction=sys_prompt_tenis, temperature=0.4)
                    )
                    
                    st.success("Treino de Tênis gerado com sucesso!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    st.download_button("📥 Baixar Treino (.txt)", response.text, file_name=f"tenis_{nome_aluno_t.lower().replace(' ', '_')}_{data_atual.replace('/', '-')}.txt")
                except Exception as e:
                    st.error(f"Erro: {e}")

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
            local_p = st.selectbox("Local de Treino", ["Academia Completa", "Treino em Casa / Condomínio", "Estúdio / Box"])
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

        lesoes_p = st.text_area("Lesões, Restrições ou Dores Articulares", placeholder="Ex: Condromalácia patelar, protusão discal lombar...")

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
                    - Restrições/Lesões: {lesoes_p if lesoes_p else 'Nenhuma restrição relatada'}
                    - Organização: {tipo_divisao_p}
                    - Superiores: {', '.join(musculos_sup_p)}
                    - Inferiores: {', '.join(musculos_inf_p)}

                    Estrutura obrigatória da resposta:
                    1. **Resumo da Estratégia & Progressão ({mesociclo_p})**: Explique brevemente como aplicar a progressão de carga (ex: progressão dupla) nas semanas e inclua orientação de semana de Deload.
                    2. **Aquecimento & Mobilidade (5-8 min)**: Prescreva 3 exercícios específicos de preparação articular e séries de aquecimento antes da carga principal.
                    3. **Divisão dos Treinos**: Separe claramente os treinos (ex: Treino A - Superiores, Treino B - Inferiores). Para CADA exercício informe:
                       - Nome do Exercício e Músculo Alvo
                       - Séries x Repetições | Descanso | Intensidade (RPE ou Repetições na Reserva - RIR)
                       - Dica rápida de biomecânica e segurança
                       - Link clicável exato: [🎥 Ver Execução](https://youtube.com) (substitua NOME+DO+EXERCICIO usando sinais de +).
                    4. **Protocolo de Cardio**: Detalhe tempo e intensidade conforme solicitado ({cardio_p}).
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
                        pdf.set_font("Helvetica", "B", 16)
                        pdf.cell(0, 10, f"ProCoach AI - Planejamento de Treino", ln=True, align="C")
                        pdf.set_font("Helvetica", "I", 11)
                        pdf.cell(0, 8, f"Aluno(a): {aluno} | Objetivo: {objetivo_p} | Ciclo: {mesociclo_p}", ln=True, align="C")
                        pdf.ln(6)
                        pdf.set_font("Helvetica", size=10)
                        # Remove caracteres fora do padrão latin-1 (como emojis) para evitar erro no PDF
                        texto_limpo = texto.replace("**", "").replace("###", "").replace("##", "")
                        texto_latin1 = texto_limpo.encode("latin-1", "ignore").decode("latin-1")
                        pdf.multi_cell(0, 6, texto_latin1)
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
