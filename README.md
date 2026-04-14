# 🧬 ADN Analyzer - Mutant Detector

API desarrollada en FastAPI para detectar si un humano es mutante a partir de su secuencia de ADN, basada en la prueba técnica de Mercado Libre.

---

## 🚀 Descripción

Magneto necesita reclutar mutantes para su ejército.
Esta API analiza secuencias de ADN y determina si pertenecen a un mutante.

Un ADN es considerado mutante si contiene **más de una secuencia de 4 letras iguales consecutivas** en:

* Horizontal
* Vertical
* Diagonal

---

## 🧠 Ejemplo

```json
{
  "dna": [
    "ATGCGA",
    "CAGTGC",
    "TTATGT",
    "AGAAGG",
    "CCCCTA",
    "TCACTG"
  ]
}
```

➡️ Resultado: `mutante`

---

## 🧱 Tecnologías utilizadas

* Python 3.11+
* FastAPI
* SQLModel
* PostgreSQL
* Redis (cache y rate limiting)
* Pytest (testing)
* SlowAPI (rate limit)

---

## 📦 Estructura del proyecto

```
app/
├── core/          # Configuración (cache, rate limit, settings)
├── db/            # Conexión a base de datos
├── models/        # Modelos SQLModel
├── schemas/       # Validación de datos (Pydantic)
├── services/      # Lógica de negocio (isMutant)
├── repositories/  # Acceso a datos
├── routers/       # Endpoints (FastAPI)
├── tests/         # Pruebas unitarias e integración
├── main.py        # Entry point
```

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/adn-analyzer.git
cd adn-analyzer
```

---

### 2. Crear entorno virtual

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🐘 Configuración de base de datos

### PostgreSQL

Crear base de datos:

```sql
CREATE DATABASE dna_analyzer;
CREATE DATABASE dna_analyzer_test;
```

---

## 🔐 Variables de entorno

Crear archivo `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dna_analyzer
REDIS_URL=redis://localhost:6379
```

---

## 🧪 Variables para testing

Crear `.env.test`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dna_analyzer_test
REDIS_URL=redis://localhost:6379
```

---

## ▶️ Ejecución de la API

```bash
uvicorn main:app --reload
```

---

## 🌐 Endpoints

### 🔍 Detectar mutante

```http
POST /mutant/
```

#### Request:

```json
{
  "dna": ["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]
}
```

#### Respuestas:

* ✅ 200 → Mutante
* ❌ 403 → Humano

---

### 📊 Estadísticas

```http
GET /stats/
```

#### Respuesta:

```json
{
  "count_mutant_dna": 40,
  "count_humans_dna": 100,
  "ratio": 0.4
}
```

---

## ⚡ Optimizaciones implementadas

* Cache con Redis (reduce carga en DB)
* Rate limiting (protección contra tráfico alto)
* Arquitectura por capas (separación de responsabilidades)
* Uso de transacciones en testing
* Reutilización de resultados (evita cálculos duplicados)

---

## 🧪 Testing

### Ejecutar tests

```bash
pytest -v
```

---

### Coverage

```bash
pytest --cov=app
```

---

### Tipos de pruebas

* Unitarias → lógica `isMutant`
* Integración → endpoints
* Cache → comportamiento de almacenamiento
* Base de datos → persistencia y consultas

---

## 🧠 Algoritmo

El algoritmo:

* Recorre la matriz NxN
* Busca secuencias de 4 letras iguales en:

  * Horizontal
  * Vertical
  * Diagonal (ambas direcciones)
* Detiene la ejecución al encontrar más de una coincidencia

Complejidad aproximada:

```
O(N²)
```

---

## ⚠️ Consideraciones

* Solo se permite un registro por ADN
* Validación de entrada estricta (NxN, caracteres válidos)
* Manejo de concurrencia mediante DB + cache

---

## 🚀 Escalabilidad

Preparado para:

* Alto tráfico (cache + rate limit)
* Escalado horizontal
* Despliegue en cloud (Docker-ready)

---

## 📌 Mejoras futuras

* Dockerización completa
* CI/CD (GitHub Actions)
* Métricas (Prometheus)
* Logs estructurados
* Test de carga (k6)

---

## 👨‍💻 Autor

Mateo Ursuga Zapata

---

## 📜 Licencia

MIT
