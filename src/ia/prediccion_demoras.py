"""
src/ia/prediccion_demoras.py
Modelo de predicción de demoras — LogiTrack
Semana 3 — Ejecución independiente

Uso:
    python src/ia/prediccion_demoras.py

Requisitos:
    pip install scikit-learn pandas numpy
"""

import sys
import random
import math

# ─────────────────────────────────────────────────────────────────
# Generación de dataset simulado
# ─────────────────────────────────────────────────────────────────

random.seed(42)

PROVINCIAS = [
    "Buenos Aires", "Córdoba", "Santa Fe", "Mendoza",
    "Tucumán", "Salta", "Entre Ríos", "Misiones", "Neuquén", "Río Negro"
]

TIPOS_PAQUETE = ["Documento", "Caja pequeña", "Caja mediana", "Caja grande", "Pallet"]
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# Distancias aproximadas desde Buenos Aires (km)
DISTANCIAS = {
    "Buenos Aires": 0, "Córdoba": 700, "Santa Fe": 470, "Mendoza": 1040,
    "Tucumán": 1310, "Salta": 1580, "Entre Ríos": 370,
    "Misiones": 1230, "Neuquén": 1190, "Río Negro": 1050
}


def calcular_distancia(origen, destino):
    """Calcula distancia aproximada entre dos provincias (simulada)."""
    d_origen = DISTANCIAS.get(origen, 500)
    d_destino = DISTANCIAS.get(destino, 500)
    return abs(d_origen - d_destino) + random.randint(50, 200)


def generar_dataset(n=500):
    """Genera dataset simulado de envíos históricos con etiqueta de demora."""
    datos = []
    for _ in range(n):
        origen = random.choice(PROVINCIAS)
        destino = random.choice(PROVINCIAS)
        distancia = calcular_distancia(origen, destino)
        peso = round(random.uniform(0.1, 50.0), 2)            # kg
        tipo_idx = random.randint(0, len(TIPOS_PAQUETE) - 1)
        dia_idx = random.randint(0, 6)

        # Lógica simplificada para generar la etiqueta (demorado = 1)
        prob_demora = 0.0
        prob_demora += 0.38 * (distancia / 1600)               # distancia (38%)
        prob_demora += 0.27 * (peso / 50)                       # peso (27%)
        prob_demora += 0.21 * (tipo_idx / 4)                    # tipo (21%)
        prob_demora += 0.14 * (1 if dia_idx >= 5 else 0)        # fin de semana (14%)
        prob_demora += random.uniform(-0.1, 0.1)                # ruido

        demorado = 1 if prob_demora > 0.45 else 0

        datos.append({
            "distancia_km": distancia,
            "peso_kg": peso,
            "tipo_paquete": tipo_idx,
            "dia_semana": dia_idx,
            "demorado": demorado
        })
    return datos


# ─────────────────────────────────────────────────────────────────
# Modelo de predicción (regresión logística simplificada / mock)
# ─────────────────────────────────────────────────────────────────

class ModeloPrediccionDemoras:
    """
    Modelo simulado de predicción de demoras en envíos.
    Implementa una regresión logística simplificada sin dependencias externas,
    usando los pesos derivados del análisis de variables influyentes documentado.
    """

    # Pesos por variable (según análisis documentado en el informe)
    PESOS = {
        "distancia_km": 0.38,
        "peso_kg": 0.27,
        "tipo_paquete": 0.21,
        "dia_semana": 0.14,
    }

    # Rangos máximos para normalización
    MAXIMOS = {
        "distancia_km": 1600,
        "peso_kg": 50,
        "tipo_paquete": 4,
        "dia_semana": 6,
    }

    UMBRAL = 0.45

    def __init__(self):
        self.entrenado = False
        self.accuracy = 0.0
        self.precision = 0.0
        self.recall = 0.0
        self.f1 = 0.0
        self.n_entrenamiento = 0

    def _sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def _score(self, muestra):
        z = 0.0
        for var, peso in self.PESOS.items():
            valor = muestra.get(var, 0)
            normalizado = valor / self.MAXIMOS[var]
            z += peso * normalizado
        return self._sigmoid((z - 0.5) * 6)  # centrar y escalar

    def entrenar(self, dataset):
        """Simula el entrenamiento evaluando el modelo sobre el dataset."""
        self.n_entrenamiento = len(dataset)

        tp = fp = tn = fn = 0
        for muestra in dataset:
            pred = 1 if self._score(muestra) >= self.UMBRAL else 0
            real = muestra["demorado"]
            if pred == 1 and real == 1: tp += 1
            elif pred == 1 and real == 0: fp += 1
            elif pred == 0 and real == 0: tn += 1
            else: fn += 1

        total = tp + fp + tn + fn
        self.accuracy = (tp + tn) / total if total > 0 else 0
        self.precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        self.recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        self.f1 = (2 * self.precision * self.recall / (self.precision + self.recall)
                   if (self.precision + self.recall) > 0 else 0)
        self.entrenado = True

    def predecir(self, distancia_km, peso_kg, tipo_paquete, dia_semana):
        """
        Predice si un envío tendrá demora.

        Parámetros:
            distancia_km (float): Distancia en kilómetros.
            peso_kg (float): Peso del paquete en kg.
            tipo_paquete (int): Índice del tipo (0=Documento, 4=Pallet).
            dia_semana (int): Día de la semana (0=Lunes, 6=Domingo).

        Retorna:
            dict: {prediccion, probabilidad, confianza}
        """
        muestra = {
            "distancia_km": distancia_km,
            "peso_kg": peso_kg,
            "tipo_paquete": tipo_paquete,
            "dia_semana": dia_semana,
        }
        prob = self._score(muestra)
        pred = "DEMORADO" if prob >= self.UMBRAL else "EN TIEMPO"
        confianza = prob if prob >= self.UMBRAL else (1 - prob)

        return {
            "prediccion": pred,
            "probabilidad_demora": round(prob, 4),
            "confianza": round(confianza, 4),
        }

    def resumen(self):
        if not self.entrenado:
            return "Modelo no entrenado."
        return (
            f"  Registros de entrenamiento : {self.n_entrenamiento}\n"
            f"  Accuracy                   : {self.accuracy:.2%}\n"
            f"  Precisión                  : {self.precision:.2%}\n"
            f"  Recall                     : {self.recall:.2%}\n"
            f"  F1-Score                   : {self.f1:.2%}\n"
        )


# ─────────────────────────────────────────────────────────────────
# Variables influyentes
# ─────────────────────────────────────────────────────────────────

def mostrar_variables_influyentes():
    print("\n📊 Variables influyentes en la predicción de demoras:")
    variables = [
        ("Distancia origen–destino", 38),
        ("Peso del paquete",         27),
        ("Tipo de envío",            21),
        ("Día de la semana",         14),
    ]
    for nombre, importancia in variables:
        barra = "█" * (importancia // 2)
        print(f"  {nombre:<28} {importancia:>3}%  {barra}")


# ─────────────────────────────────────────────────────────────────
# Casos de prueba de predicción
# ─────────────────────────────────────────────────────────────────

CASOS_PRUEBA = [
    {
        "descripcion": "Documento liviano, corta distancia, día hábil",
        "distancia_km": 150, "peso_kg": 0.5, "tipo_paquete": 0, "dia_semana": 1,
        "esperado": "EN TIEMPO"
    },
    {
        "descripcion": "Pallet pesado, larga distancia, fin de semana",
        "distancia_km": 1400, "peso_kg": 45.0, "tipo_paquete": 4, "dia_semana": 6,
        "esperado": "DEMORADO"
    },
    {
        "descripcion": "Caja mediana, distancia moderada, miércoles",
        "distancia_km": 600, "peso_kg": 15.0, "tipo_paquete": 2, "dia_semana": 2,
        "esperado": "EN TIEMPO"
    },
    {
        "descripcion": "Caja grande, larga distancia, sábado",
        "distancia_km": 1100, "peso_kg": 30.0, "tipo_paquete": 3, "dia_semana": 5,
        "esperado": "DEMORADO"
    },
]


# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

def main():
    separador = "─" * 55

    print(f"\n{'='*55}")
    print("  LogiTrack — Modelo de Predicción de Demoras")
    print(f"  Semana 3 — Ejecución independiente")
    print(f"{'='*55}\n")

    # 1. Generar dataset
    print("⚙️  Generando dataset simulado (500 envíos históricos)...")
    dataset = generar_dataset(500)
    demorados = sum(1 for d in dataset if d["demorado"] == 1)
    print(f"   Total: {len(dataset)} registros | "
          f"Demorados: {demorados} | En tiempo: {len(dataset) - demorados}")

    # 2. Entrenar modelo
    print("\n🧠 Entrenando modelo...")
    modelo = ModeloPrediccionDemoras()
    modelo.entrenar(dataset)

    print("\n📈 Métricas del modelo:")
    print(modelo.resumen())

    # 3. Variables influyentes
    mostrar_variables_influyentes()

    # 4. Casos de prueba
    print(f"\n{separador}")
    print("🧪 Casos de prueba de predicción:")
    print(separador)

    todos_ok = True
    for i, caso in enumerate(CASOS_PRUEBA, 1):
        resultado = modelo.predecir(
            distancia_km=caso["distancia_km"],
            peso_kg=caso["peso_kg"],
            tipo_paquete=caso["tipo_paquete"],
            dia_semana=caso["dia_semana"],
        )
        ok = resultado["prediccion"] == caso["esperado"]
        if not ok:
            todos_ok = False
        icono = "✅" if ok else "❌"
        print(f"\n  Caso {i}: {caso['descripcion']}")
        print(f"    Predicción : {resultado['prediccion']} {icono}")
        print(f"    Confianza  : {resultado['confianza']:.1%}")
        print(f"    Esperado   : {caso['esperado']}")

    print(f"\n{separador}")
    if todos_ok:
        print("✅ Todos los casos de prueba pasaron correctamente.")
    else:
        print("⚠️  Algunos casos de prueba no coincidieron con lo esperado.")
    print(separador)

    print("\n✅ Ejecución del modelo completada.\n")
    return 0 if todos_ok else 1


if __name__ == "__main__":
    sys.exit(main())
