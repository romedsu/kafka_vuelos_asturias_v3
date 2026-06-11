import pandas as pd
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

columnas = ['aerolineaIATA',
            'aerolineaID',
            'origenIATA',
            'origenID', 
            'destinoIATA', 
            'destinoID', 'codigoExtra', 
            'stops', 
            'equipo']

df= pd.read_csv('routes.dat',names=columnas, header=None, sep=',')

# filtro detino u origen --> OVD
df_ovd =df[ (df['origenIATA'] == 'OVD') | (df['destinoIATA']== 'OVD')].copy()


# # limpieza nulos o 0
# # Si la columna es de texto, usa un string vacío o 'N/A'
# df_ovd['codigoExtra'] = df_ovd['codigoExtra'].fillna('')

# # Si la columna es numérica (como 'stops'), usa 0
# df_ovd['stops'] = df_ovd['stops'].fillna(0)

df_ovd = df_ovd.drop(columns=['codigoExtra', 'stops', 'equipo'])

# añadir columna rutaID
# reseteo index de routes.dat original
df_ovd = df_ovd.reset_index(drop=True)
# emepezar en 1
df_ovd.index = df_ovd.index + 1
# nombre nueva columna
df_ovd.index.name = 'rutaID'

df_ovd.to_csv('/app/output/rutas_ovd.csv', index=True)

logging.info(f'Filtrado rutas ASTURIAS (OVD) : {len(df_ovd)} rutas')




