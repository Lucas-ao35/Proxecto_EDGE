import pandas as pd

def filtrar_artistas_comunes_simple():
    """Versión simplificada para filtrar por artistas comunes"""
    
    # Cargar los archivos
    df_artistas = pd.read_csv("artists_v1.csv")  # CSV con artist_lastfm
    df_canciones = pd.read_csv("spotify_songs.csv")  # CSV con track_artist
    
    # Obtener artistas únicos de cada dataset
    artistas_lastfm = set(df_artistas['artist_lastfm'].dropna().unique())
    artistas_tracks = set(df_canciones['track_artist'].dropna().unique())
    
    # Encontrar artistas comunes
    artistas_comunes = artistas_lastfm.intersection(artistas_tracks)
    
    print(f"Artistas comunes encontrados: {len(artistas_comunes)}")
    
    # Filtrar ambos datasets
    df_artistas_filtrado = df_artistas[df_artistas['artist_lastfm'].isin(artistas_comunes)]
    df_canciones_filtrado = df_canciones[df_canciones['track_artist'].isin(artistas_comunes)]
    
    # Guardar resultados
    df_artistas_filtrado.to_csv("artistas_filtrados.csv", index=False)
    df_canciones_filtrado.to_csv("canciones_filtradas.csv", index=False)
    
    print("✅ Archivos guardados:")
    print(f"   - artistas_filtrados.csv: {len(df_artistas_filtrado)} filas")
    print(f"   - canciones_filtradas.csv: {len(df_canciones_filtrado)} filas")

# Ejecutar
filtrar_artistas_comunes_simple()
