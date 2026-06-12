import streamlit as st
import joblib
import pandas as pd
import numpy as np
from openai import OpenAI
import plotly.graph_objects as go
from datetime import datetime
import json

# ============================================================================
# 1. CONFIGURAÇÃO DO AGENTE
# ============================================================================

# Configuração da página Streamlit
st.set_page_config(
    page_title="Agente Mentor de Estudantes",
    page_icon="🤖🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 3em;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 10px;
    }
    .subheader-custom {
        font-size: 1.3em;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session_state
if "historico" not in st.session_state:
    st.session_state.historico = []

# Tentar carregar modelos
try:
    modelo = joblib.load('models/modelo_performance_estudante.pkl')
    colunas = joblib.load('models/colunas_modelo.pkl')
    modelo_carregado = True
except FileNotFoundError:
    modelo_carregado = False
    st.warning("⚠️ Modelos não encontrados. Execute `train_model.py` primeiro.")

# Inicializar cliente OpenAI
@st.cache_resource
def init_openai_client():
    api_key = st.secrets.get("OPENAI_API_KEY", "SUA_CHAVE_AQUI")
    return OpenAI(api_key=api_key)

client = init_openai_client()

# ============================================================================
# 2. FUNÇÕES DO AGENTE
# ============================================================================

def raciocinar_plano_de_acao(dados, previsao, nome_aluno="Aluno"):
    """
    Agente de Raciocínio: Usa GPT-4o para interpretar dados
    e criar um plano de ação humanizado em múltiplas etapas.
    """
    status = "Bom desempenho 📈" if previsao == 1 else "Baixo desempenho ⚠️"
    
    # Extrair valores dos dados
    dados_dict = dados.iloc[0].to_dict()
    dados_formatados = {
        "Horas de Estudo": f"{dados_dict.get('horas_estudo', 0):.1f}h/semana",
        "Presença em Aulas": f"{dados_dict.get('presenca_aula', 0):.0f}%",
        "Atividades Extras": f"{dados_dict.get('atividades_extras', 0):.0f}",
        "Nota Inicial": f"{dados_dict.get('nota_teste_entrada', 0):.1f}/100"
    }
    
    prompt = f"""
    Você é um MENTOR PEDAGÓGICO especializado em análise de desempenho estudantil.
    
    DADOS DO ALUNO: {nome_aluno}
    {json.dumps(dados_formatados, ensure_ascii=False, indent=2)}
    
    PREVISÃO DO MODELO: {status}
    
    TAREFA (raciocínio em múltiplas etapas):
    
    Passo 1: DIAGNÓSTICO
    Analise os dados acima e identifique os pontos fortes e fracos deste aluno.
    
    Passo 2: CAUSA-RAIZ
    Explique por que o aluno obteve esta previsão de desempenho.
    
    Passo 3: RECOMENDAÇÕES ESPECÍFICAS
    Liste exatamente 3 recomendações acionáveis para melhorar ou manter o desempenho.
    Cada recomendação deve ser específica, prática e mensurável.
    
    Passo 4: MOTIVAÇÃO
    Termine com uma mensagem encorajadora e personalizada.
    
    Use um tom profissional, empático e motivador.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um agente de raciocínio educacional especializado em criar planos de ação personalizados para alunos."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erro ao processar com IA: {str(e)}"

def calcular_metricas(dados, previsao):
    """Calcula métricas adicionais para o aluno."""
    dados_dict = dados.iloc[0].to_dict()
    
    horas_estudo = dados_dict.get('horas_estudo', 0)
    presenca_aula = dados_dict.get('presenca_aula', 0)
    atividades_extras = dados_dict.get('atividades_extras', 0)
    nota_inicial = dados_dict.get('nota_teste_entrada', 0)
    
    # Calcular índice de engajamento (0-100)
    indice_engajamento = (presenca_aula * 0.4 + (horas_estudo / 40 * 100) * 0.3 + (atividades_extras / 20 * 100) * 0.3)
    indice_engajamento = min(100, max(0, indice_engajamento))
    
    # Nível de risco
    if previsao == 1:
        nivel_risco = "Baixo" if indice_engajamento > 70 else "Médio"
        cor_risco = "🟢"
    else:
        nivel_risco = "Alto" if indice_engajamento < 50 else "Médio"
        cor_risco = "🔴" if nivel_risco == "Alto" else "🟡"
    
    return {
        "indice_engajamento": indice_engajamento,
        "nivel_risco": nivel_risco,
        "cor_risco": cor_risco,
        "potencial_melhoria": 100 - nota_inicial
    }

def gerar_grafico_radar(dados, metricas):
    """Gera gráfico radar com métricas do aluno."""
    dados_dict = dados.iloc[0].to_dict()
    
    categorias = [
        "Presença",
        "Dedicação",
        "Atividades",
        "Base Inicial"
    ]
    
    valores = [
        dados_dict.get('presenca_aula', 0),
        min(100, (dados_dict.get('horas_estudo', 0) / 40 * 100)),
        min(100, (dados_dict.get('atividades_extras', 0) / 20 * 100)),
        dados_dict.get('nota_teste_entrada', 0)
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        name='Perfil do Aluno',
        marker=dict(color='rgba(31, 119, 180, 0.8)')
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=400,
        title="Perfil de Desempenho do Aluno"
    )
    
    return fig

# ============================================================================
# 3. INTERFACE STREAMLIT
# ============================================================================

st.markdown("<div class='main-header'>🤖🎓 Agente Mentor de Estudantes</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader-custom'>Análise Inteligente de Desempenho Acadêmico com IA</div>", unsafe_allow_html=True)

# Sidebar - Configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    modo = st.radio(
        "Escolha o modo de análise:",
        ["Análise Individual", "Comparação de Turma", "Histórico"]
    )
    
    st.divider()
    
    st.subheader("Informações da API")
    if st.secrets.get("OPENAI_API_KEY") == "SUA_CHAVE_AQUI":
        st.warning("Configure sua chave OpenAI em `.streamlit/secrets.toml`")
    else:
        st.success("✅ Chave OpenAI configurada")
    
    st.divider()
    
    st.subheader("Sobre")
    st.info("""
    **Agente Mentor v1.0**
    
    Desenvolvido com:
    - 🤖 GitHub Copilot (código assistido)
    - 🧠 OpenAI GPT-4o (raciocínio)
    - 🔢 Scikit-learn (ML)
    - 🎨 Streamlit (interface)
    """)

# ============================================================================
# 4. MODO: ANÁLISE INDIVIDUAL
# ============================================================================

if modo == "Análise Individual":
    st.subheader("📊 Insira os Dados do Aluno")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📚 Dados de Estudo")
        horas_estudo = st.slider(
            "Horas de estudo por semana",
            min_value=0,
            max_value=40,
            value=15,
            step=1,
            help="Quantas horas por semana o aluno estuda?"
        )
        
        presenca_aula = st.slider(
            "Presença em aulas (%)",
            min_value=0,
            max_value=100,
            value=85,
            step=5,
            help="Percentual de presença nas aulas"
        )
    
    with col2:
        st.markdown("### 🎯 Desempenho")
        atividades_extras = st.slider(
            "Atividades extras concluídas",
            min_value=0,
            max_value=20,
            value=8,
            step=1,
            help="Número de atividades complementares"
        )
        
        nota_teste_entrada = st.slider(
            "Nota do teste inicial (0-100)",
            min_value=0,
            max_value=100,
            value=60,
            step=5,
            help="Avaliação inicial do aluno"
        )
    
    # Nome do aluno (opcional)
    nome_aluno = st.text_input(
        "Nome do aluno (opcional)",
        value="Aluno(a)",
        placeholder="Digite o nome para personalização"
    )
    
    st.divider()
    
    # Botão de análise
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        analisar = st.button(
            "🔍 Analisar com IA",
            use_container_width=True,
            type="primary"
        )
    
    with col_btn2:
        st.button(
            "🔄 Limpar",
            use_container_width=True,
            on_click=lambda: st.rerun()
        )
    
    with col_btn3:
        exportar = st.button(
            "📥 Exportar",
            use_container_width=True
        )
    
    # ====== PROCESSAMENTO E ANÁLISE ======
    
    if analisar:
        if not modelo_carregado:
            st.error("❌ Modelos não carregados. Execute train_model.py primeiro.")
        else:
            # Preparar dados
            dados_input = pd.DataFrame(
                [[horas_estudo, presenca_aula, atividades_extras, nota_teste_entrada]],
                columns=colunas
            )
            
            # Fazer previsão
            with st.spinner("🔄 Fazendo previsão com modelo ML..."):
                previsao = modelo.predict(dados_input)[0]
                probabilidade = modelo.predict_proba(dados_input)[0]
            
            # Calcular métricas
            metricas = calcular_metricas(dados_input, previsao)
            
            # Raciocínio do agente
            with st.spinner("🤖 Agente analisando dados e gerando recomendações..."):
                recomendacao = raciocinar_plano_de_acao(dados_input, previsao, nome_aluno)
            
            # Guardar no histórico
            analise_atual = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nome": nome_aluno,
                "previsao": "Bom Desempenho" if previsao == 1 else "Baixo Desempenho",
                "confianca": max(probabilidade) * 100,
                "metricas": metricas,
                "recomendacao": recomendacao,
                "dados": {
                    "horas_estudo": horas_estudo,
                    "presenca_aula": presenca_aula,
                    "atividades_extras": atividades_extras,
                    "nota_teste_entrada": nota_teste_entrada
                }
            }
            st.session_state.historico.append(analise_atual)
            
            # ====== EXIBIÇÃO DOS RESULTADOS ======
            
            st.success("✅ Análise concluída!")
            st.divider()
            
            # Resultado principal
            st.subheader("📈 Resultado da Previsão")
            
            col_res1, col_res2, col_res3, col_res4 = st.columns(4)
            
            with col_res1:
                st.metric(
                    "Status",
                    "✅ Bom" if previsao == 1 else "⚠️ Baixo",
                    f"Confiança: {max(probabilidade)*100:.1f}%"
                )
            
            with col_res2:
                st.metric(
                    "Engajamento",
                    f"{metricas['indice_engajamento']:.0f}%",
                    "Nível de envolvimento"
                )
            
            with col_res3:
                st.metric(
                    "Nível de Risco",
                    f"{metricas['cor_risco']} {metricas['nivel_risco']}",
                    "Avaliação de risco"
                )
            
            with col_res4:
                st.metric(
                    "Potencial de Melhoria",
                    f"{metricas['potencial_melhoria']:.0f} pontos",
                    "até 100"
                )
            
            st.divider()
            
            # Gráfico radar
            st.subheader("📊 Perfil de Desempenho")
            fig_radar = gerar_grafico_radar(dados_input, metricas)
            st.plotly_chart(fig_radar, use_container_width=True)
            
            st.divider()
            
            # Recomendações do agente
            st.subheader("🎯 Análise e Recomendações do Agente")
            
            with st.expander("Clique para ver a análise completa", expanded=True):
                st.markdown(recomendacao)
            
            st.divider()
            
            # Exportar análise
            if exportar:
                relatorio = f"""
# RELATÓRIO DE ANÁLISE - Agente Mentor

**Data:** {analise_atual['timestamp']}
**Aluno:** {nome_aluno}

## Resultado da Previsão
- **Status:** {analise_atual['previsao']}
- **Confiança:** {analise_atual['confianca']:.1f}%
- **Nível de Risco:** {metricas['nivel_risco']}
- **Índice de Engajamento:** {metricas['indice_engajamento']:.1f}%

## Dados Coletados
- Horas de estudo/semana: {horas_estudo}h
- Presença em aulas: {presenca_aula}%
- Atividades extras: {atividades_extras}
- Nota inicial: {nota_teste_entrada}/100

## Análise e Recomendações do Agente
{recomendacao}

---
*Relatório gerado automaticamente pelo Agente Mentor v1.0*
*Desenvolvido com GitHub Copilot, OpenAI GPT-4o e Machine Learning*
                """
                
                st.download_button(
                    label="📥 Baixar Relatório (Markdown)",
                    data=relatorio,
                    file_name=f"relatorio_{nome_aluno}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )

# ============================================================================
# 5. MODO: HISTÓRICO
# ============================================================================

elif modo == "Histórico":
    st.subheader("📋 Histórico de Análises")
    
    if not st.session_state.historico:
        st.info("Nenhuma análise realizada ainda. Vá para 'Análise Individual' para começar.")
    else:
        for idx, analise in enumerate(st.session_state.historico, 1):
            with st.expander(f"Análise {idx}: {analise['nome']} - {analise['timestamp']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Status", "✅ Bom" if "Bom" in analise['previsao'] else "⚠️ Baixo")
                
                with col2:
                    st.metric("Confiança", f"{analise['confianca']:.1f}%")
                
                with col3:
                    st.metric("Engajamento", f"{analise['metricas']['indice_engajamento']:.0f}%")
                
                st.markdown("### Dados da Análise")
                dados_df = pd.DataFrame([analise['dados']])
                st.dataframe(dados_df)
                
                st.markdown("### Recomendações")
                st.markdown(analise['recomendacao'])

# ============================================================================
# 6. MODO: COMPARAÇÃO DE TURMA (placeholder)
# ============================================================================

elif modo == "Comparação de Turma":
    st.subheader("👥 Comparação de Turma")
    st.info("Feature em desenvolvimento. Será possível comparar múltiplos alunos em breve.")

# ============================================================================
# 7. FOOTER
# ============================================================================

st.divider()
st.markdown("""
---
**Agente Mentor de Estudantes v1.0** | Desenvolvido com ❤️ usando:
- 🤖 [GitHub Copilot](https://github.com/features/copilot) - Desenvolvimento Assistido por IA
- 🧠 [OpenAI GPT-4o](https://openai.com/gpt-4o) - Raciocínio Multi-etapa
- 🔢 [Scikit-learn](https://scikit-learn.org/) - Machine Learning
- 🎨 [Streamlit](https://streamlit.io/) - Interface Web

**Concurso:** Microsoft Agents League @ AI Skills Fest
""")