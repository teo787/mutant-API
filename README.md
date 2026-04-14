- Horizontal
- Vertical
- Diagonal

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

➡️ Resultado: mutante

🧱 Tecnologías utilizadas
Python 3.11+
FastAPI
SQLModel
PostgreSQL
Redis (cache y rate limiting)
Pytest (testing)
SlowAPI (rate limit)
📦 Estructura del proyecto
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
⚙️ Instalación
1. Clonar el repositorio
git clone https://github.com/tu-usuario/adn-analyzer.git
cd adn-analyzer
2. Crear entorno virtual
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
3. Instalar dependencias
pip install -r requirements.txt
🐘 Configuración de base de datos
PostgreSQL

Crear base de datos:

CREATE DATABASE dna_analyzer;
CREATE DATABASE dna_analyzer_test;
🔐 Variables de entorno

Crear archivo .env:

DATABASE_URL=postgresql://user:password@localhost:5432/dna_analyzer
REDIS_URL=redis://localhost:6379
🧪 Variables para testing

Crear .env.test:

DATABASE_URL=postgresql://user:password@localhost:5432/dna_analyzer_test
REDIS_URL=redis://localhost:6379
▶️ Ejecución de la API
uvicorn main:app --reload
🌐 Endpoints
🔍 Detectar mutante
POST /mutant/
Request:
{
  "dna": ["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]
}
Respuestas:
✅ 200 → Mutante
❌ 403 → Humano
📊 Estadísticas
GET /stats/
Respuesta:
{
  "count_mutant_dna": 40,
  "count_humans_dna": 100,
  "ratio": 0.4
}
⚡ Optimizaciones implementadas
✅ Cache con Redis (reduce carga en DB)
✅ Rate limiting (protección contra tráfico alto)
✅ Indexación en base de datos
✅ Separación por capas (arquitectura limpia)
✅ Uso de transacciones en testing
🧪 Testing
Ejecutar tests
pytest -v
Coverage
pytest --cov=app
Tipos de pruebas
Unitarias → lógica isMutant
Integración → endpoints
Cache → comportamiento de almacenamiento
Base de datos → persistencia y consultas
🧠 Algoritmo

El algoritmo:

Recorre la matriz NxN
Busca secuencias de 4 iguales en:
Horizontal
Vertical
Diagonal (ambas direcciones)
Detiene la ejecución al encontrar más de una coincidencia

Complejidad aproximada:

O(N²)

Optimizado para evitar recorridos redundantes.

⚠️ Consideraciones
Solo se permite un registro por ADN
Validación de entrada estricta (NxN, caracteres válidos)
Manejo de concurrencia mediante DB + cache
🚀 Escalabilidad

Preparado para:

Alto tráfico (cache + rate limit)
Escalado horizontal
Despliegue en cloud (Docker-ready)
📌 Mejoras futuras
Dockerización completa
CI/CD (GitHub Actions)
Métricas (Prometheus)
Logs estructurados
Test de carga (k6)
👨‍💻 Autor

Mateo Ursuga Zapata