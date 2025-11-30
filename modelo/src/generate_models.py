import joblib
import warnings
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import plotly.graph_objects as go
import plotly.express as px

warnings.filterwarnings('ignore', category=FutureWarning)

DATA_FILE = Path('./data/raw/dataset_aircraft_failures.csv')
MODEL_DIR = Path('./models/')

MODEL_DIR.mkdir(exist_ok=True)
(MODEL_DIR / 'nivel1').mkdir(exist_ok=True)
(MODEL_DIR / 'nivel2').mkdir(exist_ok=True)
(MODEL_DIR / 'nivel3').mkdir(exist_ok=True)

print(f"Carregando dataset de {DATA_FILE}...")
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"ERRO: Arquivo {DATA_FILE} não encontrado.")
    print("Por favor, rode o script 'dataset_create.py' primeiro.")
    exit()

print(f"Dataset carregado com {len(df)} amostras.")

X = df.filter(like='sensor_') 
y = df[['nivel1', 'nivel2', 'nivel3']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42, stratify = y['nivel1'])

print(f"Amostras de Treino: {len(X_train)} | Amostras de Teste: {len(X_test)}")

# Create and save model
def crs_model(df_treino_x, df_treino_y_alvo, nome_modelo, subpasta_nivel):

    caminho_salvar = MODEL_DIR / subpasta_nivel / f"{nome_modelo}.pkl"
    
    print("-" * 30)
    print(f"Iniciando treino: {nome_modelo}")
    print(f"Total de amostras de treino: {len(df_treino_x)}")
    
    if len(df_treino_x) == 0:
        print(f"AVISO: Sem dados de treino para {nome_modelo}. Pulando.")
        return

    modelo = RandomForestClassifier(n_estimators = 2, class_weight = 'balanced', random_state = 0, max_depth = 10, n_jobs = -1)
    
    modelo.fit(df_treino_x, df_treino_y_alvo)
    
    joblib.dump(modelo, caminho_salvar)
    print(f"Modelo salvo com sucesso em: {caminho_salvar}")
    print("-" * 30)

crs_model(
    df_treino_x = X_train,
    df_treino_y_alvo = y_train['nivel1'],
    nome_modelo = 'modelo_raiz',
    subpasta_nivel = 'nivel1'
)

filtro_sistemas = (y_train['nivel1'] == 'SISTEMAS')
crs_model(
    df_treino_x=X_train[filtro_sistemas],
    df_treino_y_alvo=y_train[filtro_sistemas]['nivel2'],
    nome_modelo='modelo_sistemas',
    subpasta_nivel='nivel2'
)

filtro_estrutural = (y_train['nivel1'] == 'ESTRUTURAL')
crs_model(
    df_treino_x=X_train[filtro_estrutural],
    df_treino_y_alvo=y_train[filtro_estrutural]['nivel2'],
    nome_modelo='modelo_estrutural',
    subpasta_nivel='nivel2'
)

filtro_eletrico = (y_train['nivel2'] == 'ELÉTRICO')
crs_model(
    df_treino_x = X_train[filtro_eletrico],
    df_treino_y_alvo = y_train[filtro_eletrico]['nivel3'],
    nome_modelo = 'modelo_eletrico',
    subpasta_nivel = 'nivel3'
)

filtro_hidraulico = (y_train['nivel2'] == 'HIDRÁULICO')
crs_model(
    df_treino_x = X_train[filtro_hidraulico],
    df_treino_y_alvo = y_train[filtro_hidraulico]['nivel3'],
    nome_modelo = 'modelo_hidraulico',
    subpasta_nivel = 'nivel3'
)

filtro_motor = (y_train['nivel2'] == 'MOTOR')
crs_model(
    df_treino_x = X_train[filtro_motor],
    df_treino_y_alvo = y_train[filtro_motor]['nivel3'],
    nome_modelo = 'modelo_motor',
    subpasta_nivel = 'nivel3'
)

filtro_combustivel = (y_train['nivel2'] == 'COMBUSTÍVEL')
crs_model(
    df_treino_x = X_train[filtro_combustivel],
    df_treino_y_alvo = y_train[filtro_combustivel]['nivel3'],
    nome_modelo = 'modelo_combustivel',
    subpasta_nivel = 'nivel3'
)

filtro_pneumatico = (y_train['nivel2'] == 'PNEUMÁTICO')
crs_model(
    df_treino_x = X_train[filtro_pneumatico],
    df_treino_y_alvo = y_train[filtro_pneumatico]['nivel3'],
    nome_modelo = 'modelo_pneumatico',
    subpasta_nivel = 'nivel3'
)

filtro_cabine = (y_train['nivel2'] == 'CABINE')
crs_model(
    df_treino_x = X_train[filtro_cabine],
    df_treino_y_alvo = y_train[filtro_cabine]['nivel3'],
    nome_modelo = 'modelo_cabine',
    subpasta_nivel = 'nivel3'
)

filtro_avionica = (y_train['nivel2'] == 'AVIÔNICA')
crs_model(
    df_treino_x = X_train[filtro_avionica],
    df_treino_y_alvo = y_train[filtro_avionica]['nivel3'],
    nome_modelo = 'modelo_avionica',
    subpasta_nivel = 'nivel3'
)

filtro_trem_de_pouso = (y_train['nivel2'] == 'TREM DE POUSO')
crs_model(
    df_treino_x = X_train[filtro_trem_de_pouso],
    df_treino_y_alvo = y_train[filtro_trem_de_pouso]['nivel3'],
    nome_modelo = 'modelo_trem_de_pouso',
    subpasta_nivel = 'nivel3'
)

filtro_controles = (y_train['nivel2'] == 'CONTROLES DE VOO')
crs_model(
    df_treino_x = X_train[filtro_controles],
    df_treino_y_alvo = y_train[filtro_controles]['nivel3'],
    nome_modelo = 'modelo_controles_de_voo',
    subpasta_nivel = 'nivel3'
)

filtro_fuselagem = (y_train['nivel2'] == 'FUSELAGEM')
crs_model(
    df_treino_x = X_train[filtro_fuselagem],
    df_treino_y_alvo = y_train[filtro_fuselagem]['nivel3'],
    nome_modelo = 'modelo_fuselagem',
    subpasta_nivel = 'nivel3'
)

filtro_asa = (y_train['nivel2'] == 'ASA')
crs_model(
    df_treino_x = X_train[filtro_asa],
    df_treino_y_alvo = y_train[filtro_asa]['nivel3'],
    nome_modelo = 'modelo_asa',
    subpasta_nivel = 'nivel3'
)

print("\n" + "=" * 50)
print("VERIFICAÇÃO FINAL: Testando o Modelo Raiz nos dados de Teste")

modelo_raiz_carregado = joblib.load(MODEL_DIR / 'nivel1' / 'modelo_raiz.pkl')
predicoes_n1 = modelo_raiz_carregado.predict(X_test)

y_real_n1 = y_test['nivel1']

print(f"Acurácia do Modelo Raiz (Nível 1): {accuracy_score(y_real_n1, predicoes_n1) * 100.0:.2f}%")
print("\nRelatório de Classificação (Nível 1):")
print(classification_report(y_real_n1, predicoes_n1))
print("=" * 50)

df_comp = pd.DataFrame({"Real": y_real_n1, "Predito": predicoes_n1})
real_counts = df_comp["Real"].value_counts().sort_index()
pred_counts = df_comp["Predito"].value_counts().sort_index()

fig = go.Figure()
fig.add_trace(go.Bar(x=real_counts.index, y=real_counts.values, name="Real"))
fig.add_trace(go.Bar(x=pred_counts.index, y=pred_counts.values, name="Predito"))
fig.update_layout(title="Comparativo – Real vs Predito (Nível 1)",
                  xaxis_title="Classe", yaxis_title="Quantidade", barmode="group")
fig.show()

tabela = pd.crosstab(df_comp["Real"], df_comp["Predito"])
fig = px.imshow(tabela, text_auto=True, color_continuous_scale="Blues",
                title="Heatmap – Real vs Predito")
fig.update_xaxes(title="Predito")
fig.update_yaxes(title="Real")
fig.show()

df_comp["Acertou"] = df_comp["Real"] == df_comp["Predito"]
fig = px.scatter(df_comp, x=df_comp.index, y="Real", color="Acertou",
                 color_discrete_map={True: "green", False: "red"},
                 hover_data=["Real", "Predito"],
                 title="Comparação – Acertos (verde) e Erros (vermelho)")
fig.update_layout(xaxis_title="Índice da Amostra", yaxis_title="Classe Real")
fig.show()
