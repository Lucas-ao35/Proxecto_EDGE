import pandas as pd

# Versión más simple y directa
def eliminar_duplicados_simple():
    """Elimina duplicados conservando el artista con más scrobbles"""
    
    # Cargar archivo
    df = pd.read_csv("artists_v2.csv")
    
    print(f"Antes: {len(df)} filas, {df['artist_lastfm'].nunique()} artistas únicos")
    
    # Ordenar por scrobbles (mayor primero) y eliminar duplicados
    df_ordenado = df.sort_values('scrobbles_lastfm', ascending=False)
    df_sin_duplicados = df_ordenado.drop_duplicates(subset=['artist_lastfm'], keep='first')
    
    print(f"Después: {len(df_sin_duplicados)} filas, {df_sin_duplicados['artist_lastfm'].nunique()} artistas únicos")
    
    # Guardar
    df_sin_duplicados.to_csv("artists_v3.csv", index=False)
    print("✅ Archivo guardado: artists_v3.csv")

# Ejecutar
eliminar_duplicados_simple()