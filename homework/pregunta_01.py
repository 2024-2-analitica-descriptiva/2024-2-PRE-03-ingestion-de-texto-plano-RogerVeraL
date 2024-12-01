"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re, pandas as pd

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requerimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    def formato(header):
        """Formatea los títulos a minúsculas y reemplaza espacios por guiones bajos."""
        return header.lower().replace(" ", "_")

    # Leer el archivo y obtener las líneas
    with open("files/input/clusters_report.txt", "r") as file:
        lineas = file.readlines()

    # Procesar encabezados
    title1 = re.sub(r"\s{2,}", "-", lineas[0]).strip().split("-")
    title2 = re.sub(r"\s{2,}", "-", lineas[1]).strip().split("-")
    title1.pop() 
    title2.pop(0) 
    
    encabezados = [
        title1[0],  # cluster
        f"{title1[1]} {title2[0]}",  
        f"{title1[2]} {title2[1]}",
        title1[3], 
    ]
    encabezados = [formato(h) for h in encabezados]


    # Leer el archivo como DataFrame con pandas
    df = pd.read_fwf(
        "files/input/clusters_report.txt",
        widths=[9, 16, 16, 80], 
        header=None,
        names=encabezados,
        skip_blank_lines=False,
        converters={encabezados[2]: lambda x: x.rstrip(" %").replace(",", ".")},
    ).iloc[4:] 


    # Procesar columna de palabras clave
    col4 = df[encabezados[3]]
    df = df[df[encabezados[0]].notna()].drop(columns=[encabezados[3]])
    df = df.astype({
        encabezados[0]: int,
        encabezados[1]: int,
        encabezados[2]: float,
    })


    # Concatenar las palabras clave por cluster
    palabras_clave = []
    temp_text = ""
    for linea in col4:        
        if isinstance(linea, str): 
            if linea.endswith("."): 
                linea = linea[:-1]
            linea = re.sub(r'\s+', ' ', linea).strip()
            temp_text += linea + " "
        elif temp_text: 
            palabras_clave.append(", ".join(re.split(r'\s*,\s*', temp_text.strip())))
            temp_text = ""
    if temp_text:
        palabras_clave.append(", ".join(re.split(r'\s*,\s*', temp_text.strip())))

    df[encabezados[3]] = palabras_clave

    return df
