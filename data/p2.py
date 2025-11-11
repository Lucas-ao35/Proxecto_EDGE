import pandas as pd

# Configuración de columnas a eliminar para cada archivo
configuracion = {
    'artists_v1.csv': {
        'columnas_eliminar': ['country_mb', 'tags_mb', 'ambiguous_artist'],
        'salida': 'artists_v2.csv'
    },
    'spotify_songs.csv': {
        'columnas_eliminar': ['energy', 'key', 'loudness', 'mode', 'liveness', 'valence'],
        'salida': 'songs_v1.csv'
    }
}

def limpiar_csv(archivo_entrada, columnas_eliminar, archivo_salida):
    try:
        df = pd.read_csv(archivo_entrada)
        columnas_existentes = [col for col in columnas_eliminar if col in df.columns]
        
        if columnas_existentes:
            df_limpio = df.drop(columns=columnas_existentes)
            df_limpio.to_csv(archivo_salida, index=False)
            print(f"✓ {archivo_salida} creado - Columnas eliminadas: {columnas_existentes}")
        else:
            print(f"⚠ No se encontraron columnas para eliminar en {archivo_entrada}")
            
    except FileNotFoundError:
        print(f"✗ Error: No se encontró {archivo_entrada}")
    except Exception as e:
        print(f"✗ Error procesando {archivo_entrada}: {e}")

# Procesar todos los archivos
for archivo, config in configuracion.items():
    limpiar_csv(archivo, config['columnas_eliminar'], config['salida'])