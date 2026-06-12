# 🤖🎓 Agente Mentor de Estudantes

**Um Agente Inteligente para Análise e Recomendação de Desempenho Acadêmico**

[![Microsoft Agents League](https://img.shields.io/badge/Concurso-Microsoft%20Agents%20League-blue)](https://aka.ms/agentsleague)
[![GitHub Copilot](https://img.shields.io/badge/Desenvolvido%20com-GitHub%20Copilot-green)](https://github.com/features/copilot)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

## 📋 Visão Geral

O **Agente Mentor de Estudantes** é uma aplicação web inteligente que:

1. **Coleta dados** do desempenho acadêmico do aluno
2. **Faz previsões** usando um modelo de Machine Learning treinado
3. **Executa raciocínio multi-etapa** via OpenAI GPT-4o
4. **Gera recomendações personalizadas** baseadas em análise de IA
5. **Apresenta insights visuais** para melhor compreensão

## 🎯 Problema Resolvido

Educadores enfrentam desafios em:
- ❌ Identificar alunos em risco de baixo desempenho
- ❌ Gerar recomendações personalizadas em escala
- ❌ Entender os fatores complexos que afetam o desempenho
- ❌ Providenciar feedback humanizado e encorajador

**Este agente resolve** estes problemas através de análise de dados inteligente e recomendações baseadas em IA.

## 🏗️ Arquitetura

```
┌──────────────────────────────────────────────────────────┐
│                    CAMADA DE INTERFACE                    │
│                    (Streamlit Web UI)                     │
└────────────────┬─────────────────────────────┬──────────┘
                 │                             │
                 ↓                             ↓
        ┌────────────────┐      ┌──────────────────────┐
        │ Entrada Dados  │      │  Configurações       │
        │  do Aluno      │      │  & Histórico         │
        └────────┬───────┘      └──────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────┐
│                  CAMADA DE PROCESSAMENTO                  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────┐      ┌──────────────────────┐  │
│  │  Modelo ML          │      │  Validação de Dados  │  │
│  │  (RandomForest)     │◄─────┤                      │  │
│  │                     │      │  - Range check       │  │
│  │  Retorna:           │      │  - Normalização      │  │
│  │  - Previsão (0/1)   │      │                      │  │
│  │  - Probabilidade    │      └──────────────────────┘  │
│  └──────────┬──────────┘                                │
│             │                                            │
│             ↓                                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │  OpenAI GPT-4o (RACIOCÍNIO MULTI-ETAPA)         │  │
│  │  ✓ Diagnóstico                                   │  │
│  │  ✓ Análise de Causa-Raiz                        │  │
│  │  ✓ 3 Recomendações Específicas                 │  │
│  │  ✓ Motivação Personalizada                     │  │
│  └──────────┬───────────────────────────────────────┘  │
│             │                                            │
└─────────────┼──────────────────────────────────────────┘
              │
              ↓
┌──────────────────────────────────────────────────────────┐
│               CAMADA DE APRESENTAÇÃO                      │
├──────────────────────────────────────────────────────────┤
│  ✓ Métricas em Cards        ✓ Gráfico Radar             │
│  ✓ Análise Completa         ✓ Download em Markdown      │
└──────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Clone o Repositório

```bash
git clone https://github.com/edinaldo10/student-mentor-agent.git
cd student-mentor-agent
```

### 2. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 3. Configure a Chave OpenAI

Crie um arquivo `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sua-chave-aqui"
```

### 4. Treine o Modelo

```bash
python train_model.py
```

### 5. Execute a Aplicação

```bash
streamlit run app.py
```

Acesse em: http://localhost:8501

## 💡 Uso

### Modo: Análise Individual

1. Insira os dados do aluno:
   - Horas de estudo por semana
   - Presença em aulas (%)
   - Atividades extras concluídas
   - Nota do teste inicial

2. Clique em "🔍 Analisar com IA"

3. Receba:
   - Previsão de desempenho
   - Gráfico de perfil (radar)
   - Análise multi-etapa do agente
   - 3 recomendações específicas

4. Exporte o relatório em Markdown

## 🧠 Como Funciona o Agente

### Passo 1: Coleta de Dados
O usuário insere indicadores de desempenho acadêmico.

### Passo 2: Previsão ML
Um modelo RandomForest prevê: Bom ou Baixo desempenho.

### Passo 3: Raciocínio Multi-Etapa (GPT-4o)
O agente executa:
1. **DIAGNÓSTICO**: Identifica pontos fortes/fracos
2. **CAUSA-RAIZ**: Explica por que o resultado ocorreu
3. **RECOMENDAÇÕES**: Lista 3 ações específicas e mensuráveis
4. **MOTIVAÇÃO**: Mensagem encorajadora personalizada

### Passo 4: Apresentação
Resultados visuais com gráficos interativos.

## 🛠️ Tecnologias Utilizadas

### Core
- **Python 3.8+** - Linguagem principal
- **Streamlit** - Framework web
- **Scikit-learn** - Machine Learning
- **OpenAI GPT-4o** - Inteligência Artificial

### Desenvolvimento Assistido por IA
- **GitHub Copilot** - Geração e sugestão de código
- **VSCode Extensions** - Autocompletar inteligente

### Visualização
- **Plotly** - Gráficos interativos
- **Pandas** - Manipulação de dados

## 📈 Melhorias Futuras

- [ ] Integração com plataformas de educação (Canvas, Blackboard)
- [ ] Análise comparativa de turmas inteiras
- [ ] Previsão de notas futuras (forecasting)
- [ ] Dashboard para educadores
- [ ] Exportação para PDF e Excel
- [ ] Suporte a múltiplos idiomas

## 📝 Estrutura de Pastas

```
student-mentor-agent/
├── app.py                              # Aplicação principal
├── train_model.py                      # Script de treinamento
├── requirements.txt                    # Dependências
├── README.md                           # Este arquivo
├── architecture.md                     # Documentação de arquitetura
├── .streamlit/
│   └── secrets.toml                   # Chave API (não commitar)
├── models/
│   ├── modelo_performance_estudante.pkl
│   └── colunas_modelo.pkl
└── data/
    └── sample_data.csv
```

## 🔒 Segurança

- ⚠️ **Nunca commite** `secrets.toml` com sua chave API
- Use variáveis de ambiente em produção
- Adicione ao `.gitignore`:
  ```
  .streamlit/secrets.toml
  .env
  *.pkl
  ```

## 📜 Licença

Desenvolvido para o **Microsoft Agents League** no AI Skills Fest.

## 👨‍💻 Autor

**Edinaldo** | GitHub: [@edinaldo10](https://github.com/edinaldo10)

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Abra uma issue ou pull request.

---

**Desenvolvido com ❤️ usando GitHub Copilot, OpenAI GPT-4o e Machine Learning**

*Concurso: Microsoft Agents League @ AI Skills Fest*