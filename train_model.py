import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

# ============================================================================
# GERAR DADOS DE TREINAMENTO
# ============================================================================

print("🔄 Gerando dados de treinamento...")

np.random.seed(42)
n_samples = 200

# Simular dados de alunos
horas_estudo = np.random.uniform(5, 35, n_samples)
presenca_aula = np.random.uniform(40, 100, n_samples)
atividades_extras = np.random.uniform(0, 20, n_samples)
nota_teste_entrada = np.random.uniform(20, 90, n_samples)

# Target: bom desempenho (1) ou baixo (0)
# Lógica: combinação de fatores
y = []
for h, p, a, n in zip(horas_estudo, presenca_aula, atividades_extras, nota_teste_entrada):
    score = (h/35 * 0.3) + (p/100 * 0.3) + (a/20 * 0.2) + (n/90 * 0.2)
    y.append(1 if score > 0.55 else 0)

y = np.array(y)

# Criar DataFrame
df = pd.DataFrame({
    'horas_estudo': horas_estudo,
    'presenca_aula': presenca_aula,
    'atividades_extras': atividades_extras,
    'nota_teste_entrada': nota_teste_entrada
})

print(f"✅ Dados gerados: {n_samples} amostras")
print(f"   - Bom desempenho: {sum(y)} amostras")
print(f"   - Baixo desempenho: {len(y) - sum(y)} amostras")

# ============================================================================
# TREINAR MODELO
# ============================================================================

print("\n🧠 Treinando modelo...")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    df, y, test_size=0.2, random_state=42
)

# Treinar
modelo = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

modelo.fit(X_train, y_train)

# Avaliar
train_score = modelo.score(X_train, y_train)
test_score = modelo.score(X_test, y_test)

print(f"✅ Modelo treinado!")
print(f"   - Acurácia treino: {train_score:.2%}")
print(f"   - Acurácia teste: {test_score:.2%}")

# ============================================================================
# SALVAR MODELO E FEATURES
# ============================================================================

print("\n💾 Salvando modelo...")

os.makedirs('models', exist_ok=True)

joblib.dump(modelo, 'models/modelo_performance_estudante.pkl')
joblib.dump(df.columns.tolist(), 'models/colunas_modelo.pkl')

print("✅ Arquivos salvos:")
print("   - models/modelo_performance_estudante.pkl")
print("   - models/colunas_modelo.pkl")

# ============================================================================
# SALVAR DADOS DE EXEMPLO
# ============================================================================

print("\n📊 Salvando dados de exemplo...")

os.makedirs('data', exist_ok=True)
df.to_csv('data/sample_data.csv', index=False)

print("✅ Dados de exemplo salvos em: data/sample_data.csv")

print("\n" + "="*50)
print("🎉 Modelo treinado com sucesso!")
print("="*50)