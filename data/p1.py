import pandas as pd

def procesar_csv_simple(archivo_entrada, archivo_salida):
    """Versión simplificada del procesamiento"""
    
    # Cargar datos
    df = pd.read_csv(archivo_entrada)
    print(f"Filas iniciales: {len(df)}")
    
    # 1. Eliminar artist_lastfm vacío
    df = df[df['artist_lastfm'].notna() & (df['artist_lastfm'].astype(str).str.strip() != '')]
    
    # 2. Procesar países
    mask_country_lastfm_vacio = df['country_lastfm'].isna() | (df['country_lastfm'].astype(str).str.strip() == '')
    mask_country_mb_no_vacio = df['country_mb'].notna() & (df['country_mb'].astype(str).str.strip() != '')
    
    # Copiar country_mb a country_lastfm donde sea posible
    df.loc[mask_country_lastfm_vacio & mask_country_mb_no_vacio, 'country_lastfm'] = \
        df.loc[mask_country_lastfm_vacio & mask_country_mb_no_vacio, 'country_mb']
    
    # Eliminar donde ambos países están vacíos
    df = df[~(mask_country_lastfm_vacio & ~mask_country_mb_no_vacio)]
    
    # 3. Procesar tags (misma lógica)
    df = df[df['tags_lastfm'].notna() & (df['tags_lastfm'].astype(str).str.strip() != '')]
    df = df[df['listeners_lastfm'].notna() & (df['listeners_lastfm'].astype(str).str.strip() != '')]
    df = df[df['scrobbles_lastfm'].notna() & (df['scrobbles_lastfm'].astype(str).str.strip() != '')]
    
    # 4. Eliminar ambiguous_artist TRUE
    df = df[df['ambiguous_artist'].astype(str).str.upper() != 'TRUE']
    
    # Guardar resultado
    df.to_csv(archivo_salida, index=False)
    print(f"Filas finales: {len(df)}")
    print(f"Archivo guardado: {archivo_salida}")

# Uso
procesar_csv_simple("artists.csv", "artists_v1.csv")