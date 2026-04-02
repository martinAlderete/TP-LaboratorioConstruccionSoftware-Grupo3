"""
backend/app/ml/predictor.py
Modelo de predicción de demoras con GaussianNB — LogiTrack
TP Laboratorio de Construcción de Software — UNGS 1C2026

Entrena una vez al iniciar el servidor. Si existen .pkl previos los reutiliza
(útil en desarrollo local). En Railway el filesystem es efímero, por lo que
siempre entrena al arrancar (500 registros → ~200ms, despreciable).
"""

import pathlib
import pandas as pd
import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
)

# ── Rutas ─────────────────────────────────────────────────────────────────────
BASE_DIR      = pathlib.Path(__file__).parent
CSV_PATH      = BASE_DIR / "envios_historicos.csv"
MODEL_PKL     = BASE_DIR / "modelo.pkl"
ENCODERS_PKL  = BASE_DIR / "encoders.pkl"

# ── Definición de columnas ────────────────────────────────────────────────────
CATEGORICAL_COLS = ["origen", "destino", "tipo_paquete"]
FEATURE_COLS     = ["origen", "destino", "distancia_km", "peso_kg", "tipo_paquete"]
TARGET_COL       = "demorado"

# ── Singleton en memoria ──────────────────────────────────────────────────────
_modelo: GaussianNB | None = None
_encoders: dict = {}


def _entrenar_y_guardar() -> tuple[GaussianNB, dict]:
    """
    Carga el CSV, preprocesa, entrena GaussianNB, imprime métricas y
    persiste modelo + encoders en archivos .pkl.
    """
    # 1. Cargar dataset y descartar columnas irrelevantes
    df = pd.read_csv(CSV_PATH)
    df = df.drop(columns=["id", "dia_semana"])

    # 2. Codificar variables categóricas con LabelEncoder
    encoders = {}
    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    X = df[FEATURE_COLS].values
    y = df[TARGET_COL].values

    # 3. Split 80/20 solo para calcular métricas (informe del TP)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    modelo_eval = GaussianNB()
    modelo_eval.fit(X_train, y_train)
    y_pred = modelo_eval.predict(X_test)

    print("\n=== Métricas del modelo GaussianNB (split 80/20) ===")
    print(f"  Accuracy  : {accuracy_score(y_test, y_pred):.2%}")
    print(f"  Precisión : {precision_score(y_test, y_pred, zero_division=0):.2%}")
    print(f"  Recall    : {recall_score(y_test, y_pred, zero_division=0):.2%}")
    print(f"  Matriz de confusión:\n{confusion_matrix(y_test, y_pred)}")
    print("====================================================\n")

    # 4. Entrenar modelo final con TODOS los datos
    modelo = GaussianNB()
    modelo.fit(X, y)

    # 5. Persistir para reutilizar (evita reentrenar en caliente en dev local)
    joblib.dump(modelo, MODEL_PKL)
    joblib.dump(encoders, ENCODERS_PKL)

    return modelo, encoders


def cargar_modelo() -> None:
    """
    Inicializa el modelo en memoria.
    Carga desde .pkl si ya existen; si no, entrena y los genera.
    Debe llamarse una vez en el startup de FastAPI.
    """
    global _modelo, _encoders

    if MODEL_PKL.exists() and ENCODERS_PKL.exists():
        _modelo   = joblib.load(MODEL_PKL)
        _encoders = joblib.load(ENCODERS_PKL)
        print("Modelo de predicción cargado desde .pkl")
    else:
        print("Entrenando modelo de predicción por primera vez...")
        _modelo, _encoders = _entrenar_y_guardar()
        print("Modelo listo.")


def predecir(
    origen: str,
    destino: str,
    distancia_km: float,
    peso_kg: float,
    tipo_paquete: str,
) -> dict:
    """
    Predice si un envío tendrá demora usando el modelo GaussianNB entrenado.

    Args:
        origen:       Provincia de origen  (ej. "Córdoba")
        destino:      Provincia de destino (ej. "Buenos Aires")
        distancia_km: Distancia en km entre origen y destino
        peso_kg:      Peso del paquete en kg
        tipo_paquete: Tipo de paquete (ej. "Caja pequeña", "Pallet")

    Returns:
        {"demorado": bool, "probabilidad": float}
        donde probabilidad es la probabilidad de clase 1 (demorado), 0–1.
    """
    if _modelo is None:
        cargar_modelo()

    def _encode(col: str, val: str) -> int:
        """Codifica un valor categórico; si es desconocido devuelve 0 (fallback)."""
        try:
            return int(_encoders[col].transform([val])[0])
        except ValueError:
            return 0

    X = [[
        _encode("origen",       origen),
        _encode("destino",      destino),
        float(distancia_km),
        float(peso_kg),
        _encode("tipo_paquete", tipo_paquete),
    ]]

    pred = _modelo.predict(X)[0]
    prob = _modelo.predict_proba(X)[0][1]   # P(clase=1) → probabilidad de demora

    return {
        "demorado":     bool(pred),
        "probabilidad": round(float(prob), 4),
    }
