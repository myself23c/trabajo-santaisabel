# utils_ingest.py
import re, json, hashlib
from datetime import datetime
from unidecode import unidecode
import pandas as pd

# ─── Normalización de texto -------------------------------------------------
def slug_name(nombres, ap_pat, ap_mat) -> str:
    txt = " ".join(filter(None, [str(nombres), str(ap_pat), str(ap_mat)]))
    txt = re.sub(r"\s{2,}", " ", txt.strip())
    return unidecode(txt).upper()

def norm_ddmmyyyy(d: str | None) -> str:
    if not d or pd.isna(d):
        return ""
    d = str(d).split()[0]
    try:
        return datetime.strptime(d, "%d/%m/%Y").date().isoformat()
    except Exception:
        return ""

def clean_json(d: dict) -> str:
    return json.dumps({k: ("" if (v != v) else v) for k, v in d.items()},
                      ensure_ascii=False)

# ─── Column families --------------------------------------------------------
STATIC_PATIENT = {
    "nombres", "apellido_paterno", "apellido_materno",
    "sexo", "lugar_de_nacimiento", "fecha_de_nacimiento", "curp"
}

DETAILS_PATIENT = {"numero_de_expediente", "telefono", "alergia"}

CONSULT_CORE = {
    "fecha_consulta", "hora", "peso", "talla", "tension_arterial", "fc", "fr",
    "temperatura", "dxtx", "imc", "cc", "plan", "subjetivo", "neurologico",
    "cabeza", "torax", "abdomen", "extremidades", "analisis", "diagnostico",
    "tratamiento", "medicamentos", "pronostico", "primera_vez_ano",
    "relacion_temporal", "dm2", "has", "ira", "asma", "conjuntivitis", "otitis",
    "deteccion_salud_mental", "folio_receta", "promocion_de_la_salud",
    "linea_vida", "esquema_vacunacion", "referido", "deteccion_adicciones",
    "deteccion_violencia_mujer", "prueba_edi", "resultado_edi",
    "resultado_battelle", "eda_tratamiento", "ira_tratamiento",
    "aplicacion_cedula_cancer_ano", "intervenciones_gerontologicas",
    "chisme", "febril", "embarazada", "nutricion", "eda"
}

# ─── Hash de fila para deduplicación ----------------------------------------
def row_sha1(row: pd.Series) -> str:
    s = "|".join(str(v) for v in row.tolist())
    return hashlib.sha1(s.encode()).hexdigest()
