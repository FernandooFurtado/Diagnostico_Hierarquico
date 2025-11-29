import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from inference import normal_data, diagnosticar_falha, carregar_modelos

MODEL_DIR = Path('./models/')
DATA_FILE = Path('./data/raw/dataset_aircraft_failures.csv') 


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