import pandas as pd

# Método más simple para eliminar duplicados
def eliminar_duplicados_simple(archivo_entrada, archivo_salida):
    """
    Elimina duplicados de manera simple manteniendo la primera ocurrencia
    """
    # Leer archivo
    df = pd.read_csv(archivo_entrada)
    
    print(f"Canciones originales: {len(df)}")
    
    # Eliminar duplicados (mismo título y artista)
    df_sin_duplicados = df.drop_duplicates(subset=['track_name', 'track_artist'])
    
    print(f"Canciones después de eliminar duplicados: {len(df_sin_duplicados)}")
    print(f"Duplicados eliminados: {len(df) - len(df_sin_duplicados)}")
    
    # Guardar resultado
    df_sin_duplicados.to_csv(archivo_salida, index=False)
    print(f"Archivo guardado: {archivo_salida}")
    
    return df_sin_duplicados

# Uso rápido
if __name__ == "__main__":
    eliminar_duplicados_simple(
        "songs_v2.csv", 
        "songs_v3.csv"
    )