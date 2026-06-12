# 🏗️ Arquitetura do Agente Mentor de Estudantes

## Visão Geral

```
┌──────────────────────────────────────────────────────────────┐
│                    CAMADA DE INTERFACE                        │
│                    (Streamlit Web UI)                         │
└────────────────┬─────────────────────────────┬──────────────┘
                 │                             │
                 ↓                             ↓
        ┌────────────────┐      ┌──────────────────────┐
        │ Entrada Dados  │      │  Configurações       │
        │  do Aluno      │      │  & Histórico         │
        └────────┬───────┘      └──────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│                  CAMADA DE PROCESSAMENTO                      │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────┐      ┌──────────────────────┐      │
│  │  Modelo ML          │      │  Validação de Dados  │      │
│  │  (RandomForest)     │◄─────┤                      │      │
│  │                     │      │  - Range check       │      │
│  │  Retorna:           │      │  - Normalização      │      │
│  │  - Previsão (0/1)   │      │                      │      │
│  │  - Probabilidade    │      └──────────────────────┘      │
│  └──────────┬──────────┘                                    │
│             │                                                │
│             ↓                                                │
│  ┌──────────────────────────────────────────────────┐      │
│  │  Cálculo de Métricas                             │      │
│  │  - Índice de Engajamento                         │      │
│  │  - Nível de Risco                                │      │
│  │  - Potencial de Melhoria                         │      │
│  └──────────┬───────────────────────────────────────┘      │
│             │                                                │
│             ↓                                                │
│  ┌──────────────────────────────────────────────────┐      │
│  │  OpenAI GPT-4o (RACIOCÍNIO MULTI-ETAPA)         │      │
│  │                                                  │      │
│  │  Passo 1: DIAGNÓSTICO                           │      │
│  │  └─ Análise de pontos fortes/fracos             │      │
│  │                                                  │      │
│  │  Passo 2: CAUSA-RAIZ                            │      │
│  │  └─ Explicar por que resultado ocorreu          │      │
│  │                                                  │      │
│  │  Passo 3: RECOMENDAÇÕES (3 específicas)         │      │
│  │  └─ Ações acionáveis e mensuráveis              │      │
│  │                                                  │      │
│  │  Passo 4: MOTIVAÇÃO                             │      │
│  │  └─ Mensagem encorajadora personalizada         │      │
│  └──────────┬───────────────────────────────────────┘      │
│             │                                                │
└─────────────┼──────────────────────────────────────────────┘
              │
              ↓
┌──────────────────────────────────────────────────────────────┐
│               CAMADA DE APRESENTAÇÃO                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐     ┌──────────────────┐              │
│  │  Métricas        │     │  Gráfico Radar   │              │
│  │  (Cards)         │     │  (Perfil do Aluno)              │
│  └──────────────────┘     └──────────────────┘              │
│                                                               │
│  ┌────────────────────────────────────────────┐             │
│  │  Análise Completa do Agente                │             │
│  │  (Com Expander para Detalhes)              │             │
│  └────────────────────────────────────────────┘             │
│                                                               │
│  ┌────────────────────────────────────────────┐             │
│  │  Botão de Download (Relatório Markdown)    │             │
│  └────────────────────────────────────────────┘             │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Fluxo de Dados

### 1. **Entrada**
```
Usuário insere:
├── Horas de estudo/semana (0-40)
├── Presença em aulas (0-100%)
├── Atividades extras (0-20)
├── Nota inicial (0-100)
└── Nome do aluno (opcional)
```

### 2. **Validação**
```
DataFrame é criado com:
- Verificação de types
- Range validation
- Normalização de features
```

### 3. **Previsão ML**
```
Modelo RandomForest processa:
- 100 árvores de decisão
- 4 features
- Retorna: classe (0 ou 1) + probabilidade
```

### 4. **Raciocínio IA (GPT-4o)**
```
Prompt enviado com:
- Dados do aluno (formatados)
- Previsão do modelo
- Instruções de raciocínio 4-etapas
- Tom: profissional, empático, motivador

Retorna: análise completa em texto
```

### 5. **Apresentação**
```
Streamlit renderiza:
- Cards com métricas principais
- Gráfico radar interativo (Plotly)
- Análise completa em expander
- Opção de download
- Armazenamento em histórico (session_state)
```

## Componentes

### Backend
| Componente | Função |
|-----------|--------|
| `app.py` | Aplicação principal, orquestração |
| `train_model.py` | Treinamento e save do modelo |
| Modelo ML | Previsão numérica |
| OpenAI API | Raciocínio e geração de texto |

### Frontend
| Componente | Função |
|-----------|--------|
| Streamlit | Renderização de UI |
| Plotly | Gráficos interativos |
| Session State | Histórico em memória |

## Segurança e Boas Práticas

### API Keys
```python
# ✅ Recomendado: usar secrets
api_key = st.secrets.get("OPENAI_API_KEY")

# ❌ Não fazer: hardcoded
api_key = "sk-..."
```

### Cache de Recursos
```python
@st.cache_resource
def init_openai_client():
    return OpenAI(api_key=...)
    # Inicializado apenas uma vez por sessão
```

### Tratamento de Erros
```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    st.error(f"❌ Erro: {str(e)}")
```

## Performance

- **Tempo de previsão ML**: ~50ms
- **Tempo de resposta GPT-4o**: ~2-3s
- **Renderização Streamlit**: ~200ms
- **Total**: ~3-4 segundos por análise

## Escalabilidade

### Melhorias Futuras
1. **Database**: PostgreSQL para armazenar histórico
2. **Cache**: Redis para respostas frequentes
3. **Async**: Processamento paralelo com asyncio
4. **Batch**: Analisar múltiplos alunos em lote
5. **API**: REST API para integração com LMS

## Tecnologias e Alternativas

| Componente | Usado | Alternativas |
|-----------|-------|--------------|
| Frontend | Streamlit | Gradio, Dash, FastAPI+React |
| ML | Scikit-learn | TensorFlow, PyTorch, XGBoost |
| LLM | OpenAI GPT-4o | Anthropic Claude, Hugging Face |
| Visualização | Plotly | Matplotlib, Altair |

## Stack Tecnológico Detalhado

### Desenvolvimento Assistido por IA
- **GitHub Copilot** - Autocompletar e geração de código
- **VSCode Copilot Chat** - Assistência em tempo real
- **OpenAI API** - Raciocínio multi-etapa

### Machine Learning
- **Scikit-learn** - Modelo de previsão (RandomForest)
- **Pandas** - Processamento de dados
- **NumPy** - Operações numéricas

### Interface & Visualização
- **Streamlit** - Framework web interativo
- **Plotly** - Gráficos e dashboards
- **HTML/CSS** - Customização de estilo

### DevOps & Deployment
- **GitHub** - Controle de versão
- **Python 3.8+** - Runtime

## Fluxo de Desenvolvimento

```
1. Usuário acessa a aplicação Streamlit
   ↓
2. Insere dados do aluno (sliders, inputs)
   ↓
3. Clica em "Analisar com IA"
   ↓
4. Sistema valida dados de entrada
   ↓
5. Modelo ML faz previsão
   ↓
6. Calcula métricas adicionais
   ↓
7. GPT-4o executa raciocínio 4-etapas
   ↓
8. Streamlit renderiza resultados
   ↓
9. Usuário visualiza análise completa
   ↓
10. Pode exportar relatório em Markdown
```

## Estrutura de Dados

### Input
```python
{
    "horas_estudo": float,      # 0-40
    "presenca_aula": float,     # 0-100
    "atividades_extras": float, # 0-20
    "nota_teste_entrada": float # 0-100
}
```

### Output (Previsão)
```python
{
    "previsao": int,            # 0 ou 1
    "probabilidade": float,     # 0-1
    "confianca": float,         # 0-100%
}
```

### Output (Análise)
```python
{
    "timestamp": str,
    "nome": str,
    "previsao": str,
    "confianca": float,
    "metricas": {
        "indice_engajamento": float,
        "nivel_risco": str,
        "cor_risco": str,
        "potencial_melhoria": float
    },
    "recomendacao": str,
    "dados": dict
}
```

## Casos de Uso

### 1. Professor analisa aluno individual
```
Professor insere dados de um aluno → recebe análise personalizada e recomendações
```

### 2. Identificar alunos em risco
```
Analisar grupo de alunos → filtrar por nível de risco alto → atuar preventivamente
```

### 3. Acompanhamento temporal
```
Analisar mesmo aluno em diferentes períodos → comparar progresso → ajustar estratégias
```

### 4. Validação de modelo
```
Usar dados históricos → comparar previsões com desempenho real → calibrar modelo
```

## Limitações Conhecidas

- ⚠️ Modelo treinado com dados sintéticos
- ⚠️ Requer chave OpenAI válida
- ⚠️ Análise em tempo real (sem cache de resposta)
- ⚠️ Histórico armazenado apenas em memória (perdido ao recarregar)
- ⚠️ Sem autenticação de usuário

## Roadmap

- [ ] Integração com plataformas LMS
- [ ] Dashboard para educadores
- [ ] Análise de turma inteira
- [ ] Previsão de notas futuras
- [ ] Exportação para PDF
- [ ] Suporte a múltiplos idiomas
- [ ] Autenticação e permissões
- [ ] Banco de dados persistente

---

**Última atualização:** 2026 | Agente Mentor v1.0