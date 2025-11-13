import pandas as pd
import joblib
import warnings
from pathlib import Path
from sklearn.model_selection import train_test_split
import numpy as np

warnings.filterwarnings('ignore', category=FutureWarning)

MODEL_DIR = Path('../models/')
DATA_FILE = Path('../data/raw/dataset_aircraft_failures.csv') 

def normal_data(n_amo):
    data = {
        'sensor_volt_gerador_1': np.random.normal(115.0, 0.5, n_amo),
        'sensor_volt_gerador_2': np.random.normal(115.0, 0.5, n_amo),
        'sensor_corrente_gerador_1': np.random.normal(300.0, 10.0, n_amo),
        'sensor_corrente_gerador_2': np.random.normal(295.0, 10.0, n_amo),
        'sensor_temp_bateria': np.random.normal(25.0, 2.0, n_amo),
        'sensor_volt_bateria': np.random.normal(28.0, 0.2, n_amo),
        'sensor_freq_sistema_eletrico': np.random.normal(400.0, 2.0, n_amo),
        'sensor_pressao_hidr_A': np.random.normal(3000.0, 15.0, n_amo),
        'sensor_pressao_hidr_B': np.random.normal(3000.0, 15.0, n_amo),
        'sensor_temp_hidr_A': np.random.normal(45.0, 2.0, n_amo),
        'sensor_temp_hidr_B': np.random.normal(45.0, 2.0, n_amo),
        'sensor_nivel_fluido_hidr_A': np.random.normal(95.0, 3.0, n_amo),
        'sensor_nivel_fluido_hidr_B': np.random.normal(95.0, 3.0, n_amo),
        'sensor_fluxo_combustivel_m1': np.random.normal(1200.0, 20.0, n_amo),
        'sensor_fluxo_combustivel_m2': np.random.normal(1180.0, 20.0, n_amo),
        'sensor_pressao_combustivel_m1': np.random.normal(35.0, 1.0, n_amo),
        'sensor_pressao_combustivel_m2': np.random.normal(35.0, 1.0, n_amo),
        'sensor_temp_combustivel': np.random.normal(20.0, 1.0, n_amo),
        'sensor_nivel_tanque_esq': np.random.normal(70.0, 5.0, n_amo),
        'sensor_nivel_tanque_dir': np.random.normal(70.0, 5.0, n_amo),
        'sensor_N1_motor_1': np.random.normal(85.0, 0.5, n_amo),
        'sensor_N2_motor_1': np.random.normal(90.0, 0.5, n_amo),
        'sensor_N1_motor_2': np.random.normal(84.5, 0.5, n_amo),
        'sensor_N2_motor_2': np.random.normal(89.5, 0.5, n_amo),
        'sensor_EGT_motor_1': np.random.normal(800.0, 10.0, n_amo),
        'sensor_EGT_motor_2': np.random.normal(805.0, 10.0, n_amo),
        'sensor_temp_oleo_motor_1': np.random.normal(85.0, 2.0, n_amo),
        'sensor_temp_oleo_motor_2': np.random.normal(86.0, 2.0, n_amo),
        'sensor_pressao_oleo_motor_1': np.random.normal(50.0, 1.5, n_amo),
        'sensor_pressao_oleo_motor_2': np.random.normal(50.5, 1.5, n_amo),
        'sensor_vib_motor_1': np.random.normal(0.2, 0.05, n_amo),
        'sensor_vib_motor_2': np.random.normal(0.2, 0.05, n_amo),
        'sensor_pressao_sangria_ar_m1': np.random.normal(40.0, 1.5, n_amo),
        'sensor_pressao_sangria_ar_m2': np.random.normal(40.0, 1.5, n_amo),
        'sensor_temp_sangria_ar_m1': np.random.normal(200.0, 5.0, n_amo),
        'sensor_temp_sangria_ar_m2': np.random.normal(200.0, 5.0, n_amo),
        'sensor_temp_cabine': np.random.normal(22.0, 1.0, n_amo),
        'sensor_pressao_cabine': np.random.normal(10.5, 0.1, n_amo), 
        'sensor_altitude_cabine': np.random.normal(8000.0, 100.0, n_amo),
        'sensor_umidade_cabine': np.random.normal(45.0, 5.0, n_amo),
        'sensor_temp_ar_condicionado': np.random.normal(20.0, 1.0, n_amo),
        'sensor_fluxo_ar_cabine': np.random.normal(50.0, 2.0, n_amo),
        'sensor_temp_rack_avionico': np.random.normal(30.0, 1.5, n_amo),
        'sensor_data_bus_load': np.random.normal(40.0, 5.0, n_amo),
        'sensor_integridade_dados': np.random.normal(99.9, 0.05, n_amo),
        'sensor_tensao_avionica': np.random.normal(28.0, 0.2, n_amo),
        'sensor_strain_asa': np.random.normal(150.0, 15.0, n_amo),
        'sensor_strain_fuselagem_popa': np.random.normal(140.0, 15.0, n_amo),
        'sensor_strain_fuselagem_nariz': np.random.normal(130.0, 15.0, n_amo),
        'sensor_vib_trem_pouso_baia': np.random.normal(0.1, 0.02, n_amo),
        'sensor_vib_trem_pouso_principal': np.random.normal(0.15, 0.03, n_amo),
        'sensor_posicao_trem_pouso': np.random.normal(0.0, 0.01, n_amo), 
        'sensor_posicao_flap': np.random.normal(0.0, 0.01, n_amo), 
        'sensor_posicao_leme': np.random.normal(0.0, 0.01, n_amo),
        'sensor_posicao_ailerons': np.random.normal(0.0, 0.01, n_amo),
        'sensor_posicao_elevador': np.random.normal(0.0, 0.01, n_amo),
        'sensor_velocidade_ar': np.random.normal(450.0, 15.0, n_amo),
        'sensor_altitude': np.random.normal(35000.0, 500.0, n_amo),
        'sensor_taxa_subida': np.random.normal(0.0, 10.0, n_amo), 
        'sensor_pitch': np.random.normal(2.5, 0.5, n_amo),
        'sensor_roll': np.random.normal(0.0, 1.0, n_amo),
        'sensor_yaw': np.random.normal(0.0, 0.5, n_amo),
        'sensor_g_load': np.random.normal(1.0, 0.05, n_amo),
        'sensor_angulo_ataque': np.random.normal(5.0, 0.5, n_amo),
        'sensor_temp_externa': np.random.normal(-45.0, 3.0, n_amo),
        'sensor_gps_latitude': np.random.normal(-23.5, 0.01, n_amo),
        'sensor_gps_longitude': np.random.normal(-46.6, 0.01, n_amo),
        'sensor_gps_altitude': np.random.normal(35000.0, 500.0, n_amo),
        'sensor_velocidade_gps': np.random.normal(450.0, 10.0, n_amo),
        'sensor_heading_magnetico': np.random.normal(90.0, 2.0, n_amo),
        'sensor_heading_gyro': np.random.normal(90.0, 2.0, n_amo)
    }

    col_sens = list(data.keys())
    
    df = pd.DataFrame(data, columns=col_sens)
    
    df = df.fillna(0) 

    df['nivel1'] = 'NORMAL'
    df['nivel2'] = 'NORMAL'
    df['nivel3'] = 'NORMAL'

    return df

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

def testar_falha_manual(modelos):
    print("\n" + "=" * 50)
    print("INICIANDO DIAGNÓSTICO MANUAL")
    print("=" * 50)

    df_paciente = normal_data(1)
    
    amostra_custom = df_paciente.drop(columns=['nivel1', 'nivel2', 'nivel3']).iloc[0]

    print("Estado ANTES da falha (Normal):")
    print(f"  Pressão Hidr. A: {amostra_custom['sensor_pressao_hidr_A']:.1f} psi")
    print(f"  Temp. Hidr. A:   {amostra_custom['sensor_temp_hidr_A']:.1f} C")

    predito = diagnosticar_falha(amostra_custom, modelos)
    print("\n--- DIAGNÓSTICO DA IA ---")
    print(f"  {predito[0]} > {predito[1]} > {predito[2]}")
    
    amostra_custom['sensor_pressao_hidr_A'] = 50.0
    amostra_custom['sensor_temp_hidr_A'] = 20.0
    amostra_custom['sensor_nivel_fluido_hidr_A'] = 94.0 

    print("\nEstado DEPOIS da falha (Injetada):")
    print(f"  Pressão Hidr. A: {amostra_custom['sensor_pressao_hidr_A']:.1f} psi")
    print(f"  Temp. Hidr. A:   {amostra_custom['sensor_temp_hidr_A']:.1f} C")

    predito = diagnosticar_falha(amostra_custom, modelos)
    
    print("\n--- DIAGNÓSTICO DA IA ---")
    print(f"  {predito[0]} > {predito[1]} > {predito[2]}")

    if predito[2] == 'FALHA BOMBA A':
        print("  STATUS: SUCESSO! A IA validou uma falha injetada manualmente.")
    else:
        print("  STATUS: FALHA! A IA não identificou a falha injetada.")
    print("-" * 50)

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
        print(f"  DIAGNÓTICO DA IA:   {predito[0]} > {predito[1]} > {predito[2]}")
        
        if list(real) == list(predito):
            print("  STATUS: ACERTO! (Perfeito)")
        else:
            print("  STATUS: ERROU! (Verificar lógica ou treino)")
        print("-" * 50)

    testar_falha_manual(modelos_carregados)