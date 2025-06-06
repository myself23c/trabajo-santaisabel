#!/usr/bin/env python3
# update_db.py
import sqlite3, argparse, pandas as pd
from db_utils_ingest import (slug_name, norm_ddmmyyyy, clean_json, row_sha1,
                          STATIC_PATIENT, DETAILS_PATIENT, CONSULT_CORE)

def ensure_column(cur, table, col):
    cur.execute("SELECT 1 FROM pragma_table_info(?) WHERE name=?;", (table, col))
    if not cur.fetchone():
        cur.execute(f'ALTER TABLE {table} ADD COLUMN "{col}" TEXT;')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("-d", "--db", default="clinic.sqlite3")
    args = ap.parse_args()

    df = pd.read_csv(args.csv, encoding="utf-8")
    df.columns = [c.strip().lower() for c in df.columns]

    conn = sqlite3.connect(args.db)
    cur  = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    for col in df.columns:
        # cualquier columna nueva en CSV -> agregar a consultations (si no existe)
        if col not in STATIC_PATIENT|DETAILS_PATIENT|CONSULT_CORE:
            ensure_column(cur, "consultations", col)

    for _, row in df.iterrows():
        nombre = slug_name(row.get("nombres"), row.get("apellido_paterno"),
                           row.get("apellido_materno"))
        cur.execute("SELECT patient_id FROM patients WHERE nombre=?;", (nombre,))
        res = cur.fetchone()
        if res:
            pid = res[0]
        else:
            data_pt = {k: row.get(k) for k in STATIC_PATIENT}
            data_pt["fecha_de_nacimiento"] = norm_ddmmyyyy(
                data_pt.get("fecha_de_nacimiento"))
            data_pt["nombre"] = nombre
            cols = ", ".join(data_pt.keys())
            ph   = ", ".join("?"*len(data_pt))
            cur.execute(f"INSERT INTO patients ({cols}) VALUES ({ph});",
                        tuple(data_pt.values()))
            pid = cur.lastrowid

        # upsert de patient_details
        details = {k: row.get(k) for k in DETAILS_PATIENT}
        meta_dt = {k: v for k, v in row.items()
                   if k not in STATIC_PATIENT|DETAILS_PATIENT|CONSULT_CORE}
        details["meta"] = clean_json(meta_dt)
        cols = ", ".join(details.keys())
        ph   = ", ".join("?"*len(details))
        cur.execute(f"""
            INSERT INTO patient_details (patient_id,{cols})
            VALUES (?,{ph})
            ON CONFLICT (patient_id) DO UPDATE SET
            {", ".join(f"{c}=excluded.{c}" for c in details.keys())};
        """, (pid, *details.values()))

        # consulta
        cons = {k: row.get(k) for k in CONSULT_CORE}
        cons["fecha_consulta"] = norm_ddmmyyyy(cons.get("fecha_consulta"))
        cons["row_hash"] = row_sha1(row)
        extra_cols = [c for c in row.index
                      if c not in STATIC_PATIENT|DETAILS_PATIENT|CONSULT_CORE]
        for c in extra_cols:
            cons[c] = row[c]

        cols = ", ".join(cons.keys())
        ph   = ", ".join("?"*len(cons))
        try:
            cur.execute(f"""
                INSERT INTO consultations (patient_id,{cols})
                VALUES (?,{ph});
            """, (pid, *cons.values()))
        except sqlite3.IntegrityError:
            pass   # duplicado exacto

    conn.commit(); conn.close()
    print("✓ CSV procesado sin duplicar consultas")

if __name__ == "__main__":
    main()
