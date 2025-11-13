import pandas as pd
import joblib
import warnings
from pathlib import Path
from sklearn.model_selection import train_test_split

warnings.filterwarnings('ignore', category=FutureWarning)

MODEL_DIR = Path('../models/')
DATA_FILE = Path('../data/raw/dataset_aircraft_failures.csv') 

def carregar_modelos():
    print("Carregando arsenal de modelos...")
    modelos = {}
    
    modelos['raiz'] = joblib.load(MODEL_DIR / 'nivel1' / 'modelo_raiz.pkl')
    
    modelos['sistemas'] = joblib.load(MODEL_DIR / 'nivel2' / 'modelo_sistemas.pkl')
    modelos['estrutural'] = joblib.load(MODEL_DIR / 'nivel2' / 'modelo_estrutural.pkl')
    
    modelos['eletrico'] = joblib.load(MODEL_DIR / 'nivel3' / 'modelo_eletrico.pkl')
    modelos['hidraulico'] = joblib.load(MODEL_DIR / 'nivel3' / 'modelo_hidraulico.pkl')
    modelos['motor'] = joblib.load(MODEL_DIR / 'nivel3' / 'modelo_motor.pkl')
    modelos['combustivel'] = joblib.load(MODEL_DIR / 'nivel3' / 'modelo_combustivel.pkl')
    modelos['pneumatico'] = joblib.load(MODEL_DIR / 'nivel3' / 'modelo_pneumatico.pkl')
    modelos['cabine'] = joblib.load(MODEL_DIR / 'nivel3' / 'modelo_cabine.pkl')
    modelos['avionica'] = joblib.load(MODEL_DIR / 'nivel3' / 'modelo_avionica.pkl')
    modelos['trem_de_pouso'] = joblib.load(MODEL_DIR / 'nivel3' / 'modelo_trem_de_pouso.pkl')
    modelos['controles_de_voo'] = joblib.load(MODEL_DIR / 'nivel3' / 'modelo_controles_de_voo.pkl')
    modelos['fuselagem'] = joblib.load(MODEL_DIR / 'nivel3' / 'modelo_fuselagem.pkl')
    modelos['asa'] = joblib.load(MODEL_DIR / 'nivel3' / 'modelo_asa.pkl')
    
    print("Todos os 13 modelos carregados com sucesso.")
    return modelos

def diagnosticar_falha(amostra_sensores, modelos):
    
    amostra_df = amostra_sensores.to_frame().T
    
    pred_n1 = modelos['raiz'].predict(amostra_df)[0]
    
    if pred_n1 == 'NORMAL':
        return ['NORMAL', 'NORMAL', 'NORMAL']

    pred_n2 = None
    if pred_n1 == 'SISTEMAS':
        pred_n2 = modelos['sistemas'].predict(amostra_df)[0]
    elif pred_n1 == 'ESTRUTURAL':
        pred_n2 = modelos['estrutural'].predict(amostra_df)[0]
    else:
        return [pred_n1, 'ERRO_N2', 'ERRO_N2']

    pred_n3 = None
    
    mapeamento_modelos_n3 = {
        'ELÉTRICO': 'eletrico',
        'HIDRÁULICO': 'hidraulico',
        'MOTOR': 'motor',
        'COMBUSTÍVEL': 'combustivel',
        'PNEUMÁTICO': 'pneumatico',
        'CABINE': 'cabine',
        'AVIÔNICA': 'avionica',
        'TREM DE POUSO': 'trem_de_pouso',
        'CONTROLES DE VOO': 'controles_de_voo',
        'FUSELAGEM': 'fuselagem',
        'ASA': 'asa'
    }
    
    nome_modelo_n3 = mapeamento_modelos_n3.get(pred_n2)
    
    if nome_modelo_n3:
        pred_n3 = modelos[nome_modelo_n3].predict(amostra_df)[0]
    else:
        return [pred_n1, pred_n2, 'ERRO_N3']

    return [pred_n1, pred_n2, pred_n3]

if __name__ == "__main__":
    
    modelos_carregados = carregar_modelos()
    
    print(f"Recarregando dados de teste de {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    
    X = df.filter(like='sensor_') 
    y = df[['nivel1', 'nivel2', 'nivel3']]
    
    _, X_test, _, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42, 
        stratify=y['nivel1']
    )
    
    indices_falha_teste = y_test[y_test['nivel1'] != 'NORMAL'].index
    
    amostras_para_teste = indices_falha_teste.to_series().sample(5)
    
    print("\n" + "=" * 50)
    print("INICIANDO DIAGNÓSTICO EM 5 FALHAS ALEATÓRIAS...")
    print("=" * 50)
    
    for i, indice in enumerate(amostras_para_teste):
        amostra = X_test.loc[indice]
        real = y_test.loc[indice].values
        
        predito = diagnosticar_falha(amostra, modelos_carregados)
        
        print(f"\n--- TESTE #{i+1} (Índice da Amostra: {indice}) ---")
        print(f"  DIAGNÓSTICO REAL:    {real[0]} > {real[1]} > {real[2]}")
        print(f"  DIAGNÓSTICO DA IA:   {predito[0]} > {predito[1]} > {predito[2]}")
        
        if list(real) == list(predito):
            print("  STATUS: ACERTO! (Perfeito)")
        else:
            print("  STATUS: ERROU! (Verificar lógica ou treino)")
        print("-" * 50)