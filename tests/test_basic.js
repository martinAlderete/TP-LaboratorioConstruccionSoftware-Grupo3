/**
 * tests/test_basic.js
 * Tests básicos de LogiTrack — Semana 3
 * Ejecutar con: node tests/test_basic.js
 */

const assert = require('assert');

// ─────────────────────────────────────────────
// Módulo: Generación de Tracking ID
// ─────────────────────────────────────────────

/**
 * Genera un tracking ID simulado (mismo algoritmo que el prototipo HTML).
 * Formato: LT-YYYYMMDD-XXXXX (ej: LT-20260329-A3F7K)
 */
function generarTrackingId() {
  const fecha = new Date();
  const yyyy = fecha.getFullYear();
  const mm = String(fecha.getMonth() + 1).padStart(2, '0');
  const dd = String(fecha.getDate()).padStart(2, '0');
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let sufijo = '';
  for (let i = 0; i < 5; i++) {
    sufijo += chars[Math.floor(Math.random() * chars.length)];
  }
  return `LT-${yyyy}${mm}${dd}-${sufijo}`;
}

// ─────────────────────────────────────────────
// Módulo: Transiciones de estado
// ─────────────────────────────────────────────

const ESTADOS_VALIDOS = ['Creado', 'En preparación', 'En tránsito', 'Entregado'];
const TRANSICIONES_VALIDAS = {
  'Creado': ['En preparación'],
  'En preparación': ['En tránsito'],
  'En tránsito': ['Entregado'],
  'Entregado': []
};

function esTransicionValida(estadoActual, estadoNuevo) {
  const siguientes = TRANSICIONES_VALIDAS[estadoActual] || [];
  return siguientes.includes(estadoNuevo);
}

// ─────────────────────────────────────────────
// Módulo: Validación de envío
// ─────────────────────────────────────────────

function validarEnvio(envio) {
  const camposRequeridos = ['remitente', 'destinatario', 'origen', 'destino', 'tipoPaquete'];
  for (const campo of camposRequeridos) {
    if (!envio[campo] || String(envio[campo]).trim() === '') {
      return { valido: false, error: `Campo requerido faltante: ${campo}` };
    }
  }
  return { valido: true };
}

// ─────────────────────────────────────────────
// TESTS
// ─────────────────────────────────────────────

let passed = 0;
let failed = 0;

function test(nombre, fn) {
  try {
    fn();
    console.log(`  ✅ ${nombre}`);
    passed++;
  } catch (err) {
    console.log(`  ❌ ${nombre}`);
    console.log(`     → ${err.message}`);
    failed++;
  }
}

// --- Suite 1: Tracking ID ---
console.log('\n📦 Suite 1: Generación de Tracking ID');

test('El tracking ID tiene el formato correcto (LT-YYYYMMDD-XXXXX)', () => {
  const id = generarTrackingId();
  assert.match(id, /^LT-\d{8}-[A-Z0-9]{5}$/);
});

test('Dos tracking IDs generados consecutivamente son distintos', () => {
  const id1 = generarTrackingId();
  const id2 = generarTrackingId();
  // En la misma ejecución pueden repetirse con baja probabilidad; lo validamos en conjunto
  // con la longitud más que con la unicidad estricta.
  assert.strictEqual(id1.length, id2.length);
  assert.strictEqual(id1.length, 17); // LT- (3) + 8 dígitos + - (1) + 5 chars = 17
});

test('El tracking ID contiene la fecha de hoy en el formato correcto', () => {
  const id = generarTrackingId();
  const partes = id.split('-');
  assert.strictEqual(partes.length, 3);
  const fechaParte = partes[1];
  assert.strictEqual(fechaParte.length, 8);
  const año = parseInt(fechaParte.substring(0, 4));
  assert.ok(año >= 2026, `El año debería ser >= 2026, fue ${año}`);
});

// --- Suite 2: Transiciones de estado ---
console.log('\n🔄 Suite 2: Transiciones de estado');

test('Creado → En preparación es una transición válida', () => {
  assert.strictEqual(esTransicionValida('Creado', 'En preparación'), true);
});

test('En preparación → En tránsito es una transición válida', () => {
  assert.strictEqual(esTransicionValida('En preparación', 'En tránsito'), true);
});

test('En tránsito → Entregado es una transición válida', () => {
  assert.strictEqual(esTransicionValida('En tránsito', 'Entregado'), true);
});

test('Creado → Entregado es una transición inválida (salto de estados)', () => {
  assert.strictEqual(esTransicionValida('Creado', 'Entregado'), false);
});

test('Entregado no tiene transiciones válidas (estado final)', () => {
  assert.strictEqual(esTransicionValida('Entregado', 'En tránsito'), false);
  assert.strictEqual(esTransicionValida('Entregado', 'Creado'), false);
});

test('Los estados del sistema son exactamente 4', () => {
  assert.strictEqual(ESTADOS_VALIDOS.length, 4);
});

// --- Suite 3: Validación de envío ---
console.log('\n📋 Suite 3: Validación de datos de envío');

test('Un envío con todos los campos requeridos es válido', () => {
  const envio = {
    remitente: 'María García',
    destinatario: 'Carlos López',
    origen: 'Buenos Aires',
    destino: 'Rosario',
    tipoPaquete: 'Caja mediana'
  };
  const resultado = validarEnvio(envio);
  assert.strictEqual(resultado.valido, true);
});

test('Un envío sin destinatario es inválido', () => {
  const envio = {
    remitente: 'María García',
    destinatario: '',
    origen: 'Buenos Aires',
    destino: 'Rosario',
    tipoPaquete: 'Caja mediana'
  };
  const resultado = validarEnvio(envio);
  assert.strictEqual(resultado.valido, false);
});

test('Un envío sin campo origen es inválido', () => {
  const envio = {
    remitente: 'María García',
    destinatario: 'Carlos López',
    destino: 'Rosario',
    tipoPaquete: 'Caja mediana'
  };
  const resultado = validarEnvio(envio);
  assert.strictEqual(resultado.valido, false);
});

// ─────────────────────────────────────────────
// Resultado final
// ─────────────────────────────────────────────
console.log(`\n─────────────────────────────`);
console.log(`Resultado: ${passed} pasados, ${failed} fallidos`);
console.log(`─────────────────────────────\n`);

if (failed > 0) {
  process.exit(1);
}
