PRAGMA foreign_keys = ON;

-------------------------  PACIENTES  -------------------------
CREATE TABLE IF NOT EXISTS patients (
    patient_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre              TEXT NOT NULL UNIQUE,
    nombres             TEXT,
    apellido_paterno    TEXT,
    apellido_materno    TEXT,
    sexo                TEXT,
    lugar_de_nacimiento TEXT,
    fecha_de_nacimiento    TEXT,             -- yyyy-mm-dd
    curp                TEXT UNIQUE,
    meta                JSON
);

-------------------  INFO SEMIESTÁTICA DEL PACIENTE -----------
CREATE TABLE IF NOT EXISTS patient_details (
    patient_id            INTEGER PRIMARY KEY,
    numero_de_expediente  TEXT,
    telefono              TEXT,
    alergia               TEXT,
    meta                  JSON,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-----------------------  CONSULTAS  ---------------------------
CREATE TABLE IF NOT EXISTS consultations (
    consulta_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id       INTEGER NOT NULL,
    row_hash         TEXT UNIQUE,         -- evita duplicados absolutos
    fecha_consulta   TEXT,                -- yyyy-mm-dd
    hora             TEXT,                -- HH:MM
    peso             TEXT,
    talla            TEXT,
    tension_arterial TEXT,
    fc               TEXT,
    fr               TEXT,
    temperatura      TEXT,
    dxtx             TEXT,
    imc              TEXT,
    cc               TEXT,
    plan             TEXT,
    subjetivo        TEXT,
    neurologico      TEXT,
    cabeza           TEXT,
    torax            TEXT,
    abdomen          TEXT,
    extremidades     TEXT,
    analisis         TEXT,
    diagnostico      TEXT,
    tratamiento      TEXT,
    medicamentos     TEXT,
    pronostico       TEXT,
    primera_vez_ano  TEXT,
    relacion_temporal TEXT,
    dm2              TEXT,
    has              TEXT,
    ira              TEXT,
    asma             TEXT,
    conjuntivitis    TEXT,
    otitis           TEXT,
    deteccion_salud_mental TEXT,
    folio_receta     TEXT,
    promocion_de_la_salud TEXT,
    linea_vida       TEXT,
    esquema_vacunacion TEXT,
    referido         TEXT,
    deteccion_adicciones TEXT,
    deteccion_violencia_mujer TEXT,
    prueba_edi       TEXT,
    resultado_edi    TEXT,
    resultado_battelle TEXT,
    eda_tratamiento  TEXT,
    ira_tratamiento  TEXT,
    aplicacion_cedula_cancer_ano TEXT,
    "INTERVENCIONES_GERONTOLOGICAS" TEXT,
    CHISME           TEXT,
    febril           TEXT,
    embarazada       TEXT,
    nutricion        TEXT,
    eda              TEXT,
    data             JSON,               -- futuras columnas
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE INDEX IF NOT EXISTS idx_cons_pid_fecha
        ON consultations (patient_id, fecha_consulta);
