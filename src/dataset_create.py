import os
import pandas as pd
import numpy as np
import random

# --------------------------------------------------

col_sens = [
    # --- Sistema Elétrico ---
    'sensor_volt_gerador_1', 'sensor_volt_gerador_2',
    'sensor_corrente_gerador_1', 'sensor_corrente_gerador_2',
    'sensor_temp_bateria', 'sensor_volt_bateria',
    'sensor_freq_sistema_eletrico',

    # --- Sistema Hidráulico ---
    'sensor_pressao_hidr_A', 'sensor_pressao_hidr_B',
    'sensor_temp_hidr_A', 'sensor_temp_hidr_B',
    'sensor_nivel_fluido_hidr_A', 'sensor_nivel_fluido_hidr_B',

    # --- Sistema de Combustível ---
    'sensor_fluxo_combustivel_m1', 'sensor_fluxo_combustivel_m2',
    'sensor_pressao_combustivel_m1', 'sensor_pressao_combustivel_m2',
    'sensor_temp_combustivel', 'sensor_nivel_tanque_esq', 'sensor_nivel_tanque_dir',

    # --- Motores ---
    'sensor_N1_motor_1', 'sensor_N2_motor_1', 'sensor_N1_motor_2', 'sensor_N2_motor_2',
    'sensor_EGT_motor_1', 'sensor_EGT_motor_2',
    'sensor_temp_oleo_motor_1', 'sensor_temp_oleo_motor_2',
    'sensor_pressao_oleo_motor_1', 'sensor_pressao_oleo_motor_2',
    'sensor_vib_motor_1', 'sensor_vib_motor_2',
    'sensor_pressao_sangria_ar_m1', 'sensor_pressao_sangria_ar_m2',
    'sensor_temp_sangria_ar_m1', 'sensor_temp_sangria_ar_m2',

    # --- Sistema Ambiental e Cabine ---
    'sensor_temp_cabine', 'sensor_pressao_cabine', 'sensor_altitude_cabine',
    'sensor_umidade_cabine', 'sensor_temp_ar_condicionado',
    'sensor_fluxo_ar_cabine',

    # --- Aviônicos e Sistema de Dados ---
    'sensor_temp_rack_avionico', 'sensor_data_bus_load',
    'sensor_integridade_dados', 'sensor_tensao_avionica',

    # --- Estrutural e Trem de Pouso ---
    'sensor_strain_asa', 'sensor_strain_fuselagem_popa', 'sensor_strain_fuselagem_nariz',
    'sensor_vib_trem_pouso_baia', 'sensor_vib_trem_pouso_principal',
    'sensor_posicao_trem_pouso', 'sensor_posicao_flap', 'sensor_posicao_leme',
    'sensor_posicao_ailerons', 'sensor_posicao_elevador',

    # --- Parâmetros de Voo ---
    'sensor_velocidade_ar', 'sensor_altitude', 'sensor_taxa_subida',
    'sensor_pitch', 'sensor_roll', 'sensor_yaw', 'sensor_g_load',
    'sensor_angulo_ataque', 'sensor_temp_externa',

    # --- Sistema de Navegação ---
    'sensor_gps_latitude', 'sensor_gps_longitude', 'sensor_gps_altitude',
    'sensor_velocidade_gps', 'sensor_heading_magnetico', 'sensor_heading_gyro'
]
col_clas = ['nivel1', 'nivel2', 'nivel3']

def normal_data(n_amo):
    data = {
        # --- Sistema Elétrico ---
        'sensor_volt_gerador_1': np.random.normal(115.0, 0.5, n_amo),
        'sensor_volt_gerador_2': np.random.normal(115.0, 0.5, n_amo),
        'sensor_corrente_gerador_1': np.random.normal(300.0, 10.0, n_amo),
        'sensor_corrente_gerador_2': np.random.normal(295.0, 10.0, n_amo),
        'sensor_temp_bateria': np.random.normal(25.0, 2.0, n_amo),
        'sensor_volt_bateria': np.random.normal(28.0, 0.2, n_amo),
        'sensor_freq_sistema_eletrico': np.random.normal(400.0, 2.0, n_amo),

        # --- Sistema Hidráulico ---
        'sensor_pressao_hidr_A': np.random.normal(3000.0, 15.0, n_amo),
        'sensor_pressao_hidr_B': np.random.normal(3000.0, 15.0, n_amo),
        'sensor_temp_hidr_A': np.random.normal(45.0, 2.0, n_amo),
        'sensor_temp_hidr_B': np.random.normal(45.0, 2.0, n_amo),
        'sensor_nivel_fluido_hidr_A': np.random.normal(95.0, 3.0, n_amo),
        'sensor_nivel_fluido_hidr_B': np.random.normal(95.0, 3.0, n_amo),

        # --- Sistema de Combustível ---
        'sensor_fluxo_combustivel_m1': np.random.normal(1200.0, 20.0, n_amo),
        'sensor_fluxo_combustivel_m2': np.random.normal(1180.0, 20.0, n_amo),
        'sensor_pressao_combustivel_m1': np.random.normal(35.0, 1.0, n_amo),
        'sensor_pressao_combustivel_m2': np.random.normal(35.0, 1.0, n_amo),
        'sensor_temp_combustivel': np.random.normal(20.0, 1.0, n_amo),
        'sensor_nivel_tanque_esq': np.random.normal(70.0, 5.0, n_amo),
        'sensor_nivel_tanque_dir': np.random.normal(70.0, 5.0, n_amo),

        # --- Motores ---
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

        # --- Sistema Ambiental e Cabine ---
        'sensor_temp_cabine': np.random.normal(22.0, 1.0, n_amo),
        'sensor_pressao_cabine': np.random.normal(10.5, 0.1, n_amo),
        'sensor_altitude_cabine': np.random.normal(8000.0, 100.0, n_amo),
        'sensor_umidade_cabine': np.random.normal(45.0, 5.0, n_amo),
        'sensor_temp_ar_condicionado': np.random.normal(20.0, 1.0, n_amo),
        'sensor_fluxo_ar_cabine': np.random.normal(50.0, 2.0, n_amo),

        # --- Aviônicos e Sistema de Dados ---
        'sensor_temp_rack_avionico': np.random.normal(30.0, 1.5, n_amo),
        'sensor_data_bus_load': np.random.normal(40.0, 5.0, n_amo),
        'sensor_integridade_dados': np.random.normal(99.9, 0.05, n_amo),
        'sensor_tensao_avionica': np.random.normal(28.0, 0.2, n_amo),

        # --- Estrutural e Trem de Pouso ---
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

        # --- Parâmetros de Voo ---
        'sensor_velocidade_ar': np.random.normal(450.0, 15.0, n_amo),
        'sensor_altitude': np.random.normal(35000.0, 500.0, n_amo),
        'sensor_taxa_subida': np.random.normal(1500.0, 50.0, n_amo),
        'sensor_pitch': np.random.normal(2.5, 0.5, n_amo),
        'sensor_roll': np.random.normal(0.0, 1.0, n_amo),
        'sensor_yaw': np.random.normal(0.0, 0.5, n_amo),
        'sensor_g_load': np.random.normal(1.0, 0.05, n_amo),
        'sensor_angulo_ataque': np.random.normal(5.0, 0.5, n_amo),
        'sensor_temp_externa': np.random.normal(-45.0, 3.0, n_amo),

        # --- Sistema de Navegação ---
        'sensor_gps_latitude': np.random.normal(-23.5, 0.01, n_amo),
        'sensor_gps_longitude': np.random.normal(-46.6, 0.01, n_amo),
        'sensor_gps_altitude': np.random.normal(35000.0, 500.0, n_amo),
        'sensor_velocidade_gps': np.random.normal(450.0, 10.0, n_amo),
        'sensor_heading_magnetico': np.random.normal(90.0, 2.0, n_amo),
        'sensor_heading_gyro': np.random.normal(90.0, 2.0, n_amo)
    }

    df = pd.DataFrame(data, columns = col_sens)

    df['nivel1'] = 'NORMAL'
    df['nivel2'] = 'NORMAL'
    df['nivel3'] = 'NORMAL'

    df = df.fillna(0)
    return df

# --------------------------------------------------

# Falha no gerador
def source_failure(n_amo):
    df = normal_data(n_amo)

    df['sensor_volt_gerador_1'] = np.random.normal(5.0, 0.5, n_amo) 
    df['sensor_corrente_gerador_1'] = np.random.normal(0.0, 0.5, n_amo) 
    df['sensor_volt_bateria'] = np.random.normal(27.5, 0.2, n_amo) 
    df['sensor_temp_bateria'] = np.random.normal(35.0, 2.0, n_amo) 

    df['nivel1'] = 'SISTEMAS'
    df['nivel2'] = 'ELÉTRICO'
    df['nivel3'] = 'FALHA NO GERADOR 1'

    return df

# Falha na bomba hidráulica
def pump_failure(n_amo):
    df = normal_data(n_amo)

    df['sensor_pressao_hidr_A'] = np.random.normal(50.0, 10.0, n_amo)
    df['sensor_temp_hidr_A']    = np.random.normal(20.0, 2.0, n_amo) 
    df['sensor_nivel_fluido_hidr_A'] = np.random.normal(94.0, 3.0, n_amo) 

    df[col_clas[0]] = 'SISTEMAS'
    df[col_clas[1]] = 'HIDRÁULICO'
    df[col_clas[2]] = 'FALHA BOMBA A'

    return df

# Falha na bomba de combustivel
def pump_fuel(n_amo):
    df = normal_data(n_amo)
    
    df['sensor_pressao_combustivel_m1'] = np.random.normal(2.0, 0.5, n_amo) 
    df['sensor_fluxo_combustivel_m1']   = np.random.normal(300.0, 20.0, n_amo) 

    df['sensor_N1_motor_1'] = np.random.normal(60.0, 5.0, n_amo) 
    df['sensor_EGT_motor_1'] = np.random.normal(600.0, 10.0, n_amo) 

    df[col_clas[0]] = 'SISTEMAS'
    df[col_clas[1]] = 'COMBUSTÍVEL'
    df[col_clas[2]] = 'FALHA BOMBA M1'
    
    return df

# Dano na fuselagem por stress
def airframe_failure(n_amo):
    df = normal_data(n_amo)

    df['sensor_strain_fuselagem_popa'] = np.random.normal(850.0, 50.0, n_amo)
    df['sensor_g_load'] = np.random.normal(1.0, 0.5, n_amo) 

    df[col_clas[0]] = 'ESTRUTURAL'
    df[col_clas[1]] = 'FUSELAGEM'
    df[col_clas[2]] = 'DANO POR FADIGA'

    return df

# Problema de vibração no motor
def engine_vibration(n_amo):
    df = normal_data(n_amo)

    df['sensor_vib_motor_1'] = np.random.normal(2.5, 0.3, n_amo) 
    df['sensor_temp_oleo_motor_1'] = np.random.normal(95.0, 5.0, n_amo) 
    df['sensor_pressao_oleo_motor_1'] = np.random.normal(45.0, 2.0, n_amo) #

    df[col_clas[0]] = 'SISTEMAS'
    df[col_clas[1]] = 'MOTOR'
    df[col_clas[2]] = 'ALTA VIBRAÇÃO M1'

    return df

# Dano na asa
def wing_damage(n_amo):
    df = normal_data(n_amo)

    df['sensor_strain_asa'] = np.random.normal(900.0, 50.0, n_amo) 
    df['sensor_posicao_ailerons'] = np.random.normal(0.2, 0.05, n_amo) 

    df[col_clas[0]] = 'ESTRUTURAL'
    df[col_clas[1]] = 'ASA'
    df[col_clas[2]] = 'DANO ESTRUTURAL'

    return df

# Superaquecimento de EGT (Febre no motor)
def engine_egt_high(n_amo):
    df = normal_data(n_amo)
    
    df['sensor_EGT_motor_2'] = np.random.normal(1050.0, 20.0, n_amo) 
    df['sensor_temp_oleo_motor_2'] = np.random.normal(98.0, 2.0, n_amo)
    df['sensor_N2_motor_2'] = np.random.normal(92.0, 1.0, n_amo) 

    df[col_clas[0]] = 'SISTEMAS'
    df[col_clas[1]] = 'MOTOR'
    df[col_clas[2]] = 'EGT ALTA M2'

    return df

# Vazamento Hidráulico B (Lento)
def hydraulic_leak_B(n_amo):
    df = normal_data(n_amo)
    
    df['sensor_nivel_fluido_hidr_B'] = np.random.normal(40.0, 5.0, n_amo)
    df['sensor_pressao_hidr_B'] = np.random.normal(2500.0, 100.0, n_amo)
    df['sensor_temp_hidr_B'] = np.random.normal(60.0, 5.0, n_amo) 

    df[col_clas[0]] = 'SISTEMAS'
    df[col_clas[1]] = 'HIDRÁULICO'
    df[col_clas[2]] = 'VAZAMENTO SISTEMA B'

    return df

# Falha Pneumática (Vazamento de ar quente)
def pneumatic_leak(n_amo):
    df = normal_data(n_amo)
    
    df['sensor_pressao_sangria_ar_m1'] = np.random.normal(10.0, 2.0, n_amo) 
    df['sensor_temp_sangria_ar_m1'] = np.random.normal(150.0, 10.0, n_amo) 

    df['sensor_fluxo_ar_cabine'] = np.random.normal(30.0, 2.0, n_amo) 

    df[col_clas[0]] = 'SISTEMAS'
    df[col_clas[1]] = 'PNEUMÁTICO'
    df[col_clas[2]] = 'VAZAMENTO SANGRIA M1'

    return df

# Despressurização da Cabine
def cabin_depressurization(n_amo):
    df = normal_data(n_amo)

    df['sensor_pressao_cabine'] = np.random.normal(2.0, 0.5, n_amo)
    df['sensor_altitude_cabine'] = np.random.normal(25000.0, 500.0, n_amo) 
    df['sensor_fluxo_ar_cabine'] = np.random.normal(10.0, 2.0, n_amo)

    df[col_clas[0]] = 'SISTEMAS'
    df[col_clas[1]] = 'CABINE'
    df[col_clas[2]] = 'DESPRESSURIZAÇÃO'
    return df

# Superaquecimento Aviônico
def avionics_overheat(n_amo):
    df = normal_data(n_amo)
    
    df['sensor_temp_rack_avionico'] = np.random.normal(90.0, 5.0, n_amo) 
    df['sensor_data_bus_load'] = np.random.normal(95.0, 2.0, n_amo) 
    df['sensor_integridade_dados'] = np.random.normal(80.0, 5.0, n_amo) 
    df['sensor_tensao_avionica'] = np.random.normal(27.0, 1.0, n_amo) 

    df[col_clas[0]] = 'SISTEMAS'
    df[col_clas[1]] = 'AVIÔNICA'
    df[col_clas[2]] = 'SUPERAQUECIMENTO'
    return df

# Falha de Extensão do Trem de Pouso
def landing_gear_stuck(n_amo):
    df = normal_data(n_amo)
    
    df['sensor_altitude'] = np.random.normal(5000.0, 100.0, n_amo)
    df['sensor_velocidade_ar'] = np.random.normal(200.0, 10.0, n_amo)
    df['sensor_posicao_trem_pouso'] = np.random.normal(0.5, 0.05, n_amo) 
    df['sensor_vib_trem_pouso_baia'] = np.random.normal(3.0, 0.5, n_amo) 
    df['sensor_pressao_hidr_A'] = np.random.normal(2800.0, 50.0, n_amo) 

    df[col_clas[0]] = 'SISTEMAS'
    df[col_clas[1]] = 'TREM DE POUSO'
    df[col_clas[2]] = 'FALHA EXTENSÃO'
    
    return df

# Flap Assimétrico
def flap_asymmetric(n_amo):
    df = normal_data(n_amo)
    
    df['sensor_altitude'] = np.random.normal(3000.0, 100.0, n_amo)
    df['sensor_velocidade_ar'] = np.random.normal(180.0, 10.0, n_amo)
    df['sensor_posicao_flap'] = np.random.normal(0.3, 0.02, n_amo)
    df['sensor_posicao_ailerons'] = np.random.normal(0.4, 0.05, n_amo) 
    df['sensor_roll'] = np.random.normal(5.0, 1.0, n_amo)

    df[col_clas[0]] = 'SISTEMAS'
    df[col_clas[1]] = 'CONTROLES DE VOO'
    df[col_clas[2]] = 'FLAP ASSIMÉTRICO'
    return df
# --------------------------------------------------
print('Criando datasset...')

df_normal = normal_data(200000) 

df_source_failure   = source_failure(10000)
df_pump_failure_A   = pump_failure(10000) 
df_pump_fuel        = pump_fuel(10000)
df_airframe_failure = airframe_failure(5000)
df_engine_vibration = engine_vibration(5000)
df_wing_damage      = wing_damage(5000)
df_eng_egt_high     = engine_egt_high(5000)
df_hyd_leak_B       = hydraulic_leak_B(10000)
df_pneum_leak       = pneumatic_leak(10000)
df_cabin_depress    = cabin_depressurization(2000) 
df_avionics_hot     = avionics_overheat(5000)
df_gear_stuck       = landing_gear_stuck(5000)
df_flap_asym        = flap_asymmetric(5000)


dataframe_list = [
    df_normal,
    df_source_failure, df_pump_failure_A, df_pump_fuel,
    df_airframe_failure, df_engine_vibration, df_wing_damage,
    df_eng_egt_high, df_hyd_leak_B, df_pneum_leak,
    df_cabin_depress, df_avionics_hot, df_gear_stuck, df_flap_asym
]

df_final = pd.concat(dataframe_list)
df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)

file_name = './data/raw/dataset_aircraft_failures.csv'

try:
    os.makedirs(os.path.dirname(file_name), exist_ok = True)
    df_final.to_csv(file_name, index=False)

    print(f"Dataset salvo com sucesso: {file_name}")

except OSError as e:
    print(f"Erro ao salvar o arquivo: {e}")

print(f"Total de amostras: {len(df_final)}")
print(f"Total de colunas: {len(df_final.columns)}")
print("\nVisão do novo dataset (últimas 5 colunas):\n")
print(df_final.iloc[:, -5:].head())