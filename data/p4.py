import pandas as pd
import re
from typing import List, Optional

class ExtractorColaboradores:
    def __init__(self):
        self.patrones_principales = [
            # Patrones con paréntesis
            (r'\(feat\.?\s*(.*?)\)', 'feat'),
            (r'\(ft\.?\s*(.*?)\)', 'ft'),
            (r'\(featuring\s*(.*?)\)', 'featuring'),
            (r'\(with\s*(.*?)\)', 'with'),
            # Patrones con corchetes
            (r'\[feat\.?\s*(.*?)\]', 'feat'),
            (r'\[ft\.?\s*(.*?)\]', 'ft'),
            (r'\[featuring\s*(.*?)\]', 'featuring'),
            (r'\[with\s*(.*?)\]', 'with'),
            # Patrones sin delimitadores
            (r'feat\.?\s*(.*?)(?:\s*\-|\s*\(|$)', 'feat'),
            (r'ft\.?\s*(.*?)(?:\s*\-|\s*\(|$)', 'ft'),
            (r'featuring\s*(.*?)(?:\s*\-|\s*\(|$)', 'featuring'),
            (r'with\s*(.*?)(?:\s*\-|\s*\(|$)', 'with')
        ]
        
        self.palabras_excluir = {
            'remix', 'mix', 'version', 'edit', 'radio', 'acoustic', 'live',
            'original', 'instrumental', 'demo', 'bonus', 'track', 'single'
        }
    
    def limpiar_artista(self, artista: str) -> str:
        """Limpia y formatea el nombre del artista"""
        artista = artista.strip()
        # Remover caracteres especiales al inicio/final
        artista = re.sub(r'^[^\w\s]+|[^\w\s]+$', '', artista)
        # Capitalizar nombre (maneja nombres compuestos)
        artista = ' '.join(
            word.capitalize() if word.lower() not in {'de', 'del', 'la', 'los', 'el', 'y'} 
            else word.lower() 
            for word in artista.split()
        )
        return artista
    
    def separar_colaboradores(self, texto_colaboradores: str) -> List[str]:
        """Separa múltiples colaboradores en una lista"""
        separadores = r'\s*&\s*|\s*,\s*|\s+and\s+|\s*\/\s*'
        colaboradores = re.split(separadores, texto_colaboradores)
        return [self.limpiar_artista(colab) for colab in colaboradores if colab.strip()]
    
    def extraer_colaboradores(self, track_name: str) -> Optional[str]:
        """Extrae colaboradores del nombre de la canción"""
        if pd.isna(track_name):
            return None
        
        track_name_str = str(track_name)
        colaboradores_encontrados = []
        
        # Buscar con patrones principales
        for patron, tipo in self.patrones_principales:
            matches = re.findall(patron, track_name_str, re.IGNORECASE)
            for match in matches:
                if match:
                    colaboradores = self.separar_colaboradores(match)
                    for colab in colaboradores:
                        if (colab and len(colab) > 1 and 
                            colab.lower() not in self.palabras_excluir and
                            colab not in colaboradores_encontrados):
                            colaboradores_encontrados.append(colab)
        
        # Búsqueda secundaria en paréntesis generales
        if not colaboradores_encontrados:
            patron_general = r'\((.*?)\)'
            matches_general = re.findall(patron_general, track_name_str)
            for match in matches_general:
                if (len(match) > 3 and 
                    not any(palabra in match.lower() for palabra in self.palabras_excluir)):
                    palabras = match.split()
                    # Heurística: si tiene 1-4 palabras y al menos una es >2 caracteres
                    if 1 <= len(palabras) <= 4 and any(len(palabra) > 2 for palabra in palabras):
                        artista_limpio = self.limpiar_artista(match)
                        if (artista_limpio and artista_limpio.lower() not in self.palabras_excluir):
                            colaboradores_encontrados.append(artista_limpio)
        
        return ', '.join(colaboradores_encontrados) if colaboradores_encontrados else None

def analizar_resultados(df: pd.DataFrame):
    """Analiza y muestra estadísticas de los resultados"""
    total = len(df)
    con_colaboradores = df['collaborating_artists'].notna().sum()
    
    print(f"\n=== ANÁLISIS DE RESULTADOS ===")
    print(f"Total de canciones: {total}")
    print(f"Canciones con colaboradores: {con_colaboradores}")
    print(f"Porcentaje: {con_colaboradores/total*100:.2f}%")
    
    # Top colaboradores más frecuentes
    if con_colaboradores > 0:
        todos_colaboradores = []
        for colaboradores in df['collaborating_artists'].dropna():
            todos_colaboradores.extend([colab.strip() for colab in colaboradores.split(',')])
        
        from collections import Counter
        top_colaboradores = Counter(todos_colaboradores).most_common(10)
        
        print(f"\nTop 10 colaboradores más frecuentes:")
        for artista, count in top_colaboradores:
            print(f"  {artista}: {count} apariciones")

# Uso principal
if __name__ == "__main__":
    extractor = ExtractorColaboradores()
    
    # Procesar archivo
    archivo_entrada = "songs_v1.csv"
    archivo_salida = "songs_v2.csv"
    
    try:
        df = pd.read_csv(archivo_entrada)
        df['collaborating_artists'] = df['track_name'].apply(extractor.extraer_colaboradores)
        
        # Mostrar ejemplos
        print("=== EJEMPLOS DETECTADOS ===")
        ejemplos = df[df['collaborating_artists'].notna()].head(8)
        for idx, row in ejemplos.iterrows():
            print(f"Canción: {row['track_name'][:60]}...")
            print(f"Colaboradores: {row['collaborating_artists']}")
            print("-" * 80)
        
        # Análisis
        analizar_resultados(df)
        
        # Guardar
        df.to_csv(archivo_salida, index=False)
        print(f"\nArchivo guardado como: {archivo_salida}")
        
    except Exception as e:
        print(f"Error: {e}")