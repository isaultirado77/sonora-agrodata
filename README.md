<p align="center">
  <img src="figures/portada.jpg" alt="Portada del proyecto" width="100%" style="max-height: 320px; object-fit: cover;">
</p>

# 🌾 **Sonora AgroData**

**Análisis de agricultura y recursos hídricos en Sonora (1999–2021)**

Este proyecto integra, procesa y analiza datos oficiales de **agricultura** y **recursos hídricos** del estado de Sonora, con el objetivo de comprender su evolución, los cultivos más relevantes y la relación entre la actividad agrícola y los ciclos de disponibilidad de agua.

Incluye un **pipeline ETL completo**, una base de datos **DuckDB**, un **EDA reproducible**, y dos reportes:

* un **informe técnico**,
* y un **artículo narrativo tipo Medium**.

---

## 📁 **Estructura del proyecto**

```
sonora-agrodata/
├── etl/                # Extract, Transform, Load
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── scripts/            # Configuración y utilidades
│   ├── config.py
│   └── utils.py
├── data/
│   ├── raw/            # Datos descargados
│   ├── interim/
│   └── processed/      # CSV + GeoJSON + DuckDB
├── nb/                 # Notebooks del EDA
├── plots/              # Gráficos generados
├── report/             # Reportes técnico y Medium
├── figures/            # Portada del proyecto
├── main.py             # Orquestador del pipeline completo
├── Makefile
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

---

## 🗂️ **Datos utilizados**

### **1. Agricultura Sonora (1999–2021)**

Fuente: Gobierno del Estado de Sonora
[https://datos.sonora.gob.mx/dataset/Agricultura%20Sonora](https://datos.sonora.gob.mx/dataset/Agricultura%20Sonora)

* Superficie sembrada
* Superficie cosechada
* Volumen de producción
* Valor económico
* Cultivos, variedades, DDR, municipio

**Diccionario:** [`references/diccionario-agricultura.md`](references/diccionario-agricultura.md)

---

### **2. Recursos Hídricos Sonora (1944–2024)**

Fuente: Gobierno del Estado de Sonora
[https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos](https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos)

* Registros mensuales por presa
* Almacenamiento en $\text{hm}^3$

**Diccionario:** [`references/diccionario-recursos-hídricos.md`](references/diccionario-recursos-hídricos.md)

---

### **3. Geometrías municipales (INEGI)**

Fuente: INEGI — Marco Geoestadístico
[https://www.inegi.org.mx](https://www.inegi.org.mx)

* Límites municipales del estado de Sonora

---

## ⚙️ **1. Configuración del entorno (recomendado: ejecución local con uv)**

Este proyecto usa **Python 3.13** y el gestor de dependencias **uv**.

### **1. Verifica tu versión de Python**

```bash
python --version
```

Debe ser **3.12 o superior**.

---

### **2. Instala uv**

```bash
pip install uv
```

---

### **3. Instala dependencias**

```bash
uv sync --frozen
```

Esto crea un entorno virtual y sincroniza exactamente las dependencias del proyecto.

---

## 🚀 **2. Ejecución del pipeline ETL (local)**

Puedes usar el **Makefile**.
O bien ejecutar cada módulo con `uv run`.

Al ejecutar el pipeline, se generan tres productos principales:

#### **📥 Datos crudos (`data/raw/`)**

Descargados desde las fuentes oficiales: agricultura, recursos hídricos y geometría municipal.

#### **🔧 Datos procesados (`data/processed/`)**

Archivos limpios y estandarizados utilizados para análisis:

* `agricultura_processed.csv`
* `hidricos_processed.csv`
* `presas_processed.csv`
* `mpios_processed.geojson`

#### **🗄 Base de datos DuckDB (`data/processed/sonora.duckdb`)**

El pipeline carga automáticamente todos los datos procesados en DuckDB, creando tablas listas para consulta y análisis.

---

### **Pipeline completo**

```bash
make etl
```

Internamente ejecuta:

```bash
make extract
make transform
make load
```

---

### **Ejecutar todo manualmente**

```bash
uv run python -m etl.extract
uv run python -m etl.transform
uv run python -m etl.load
```

---

### **Orquestación vía main.py**

```bash
uv run python main.py
```

---

# 🐋 **3. Ejecución con Docker (opcional)**

## **1. Construir la imagen**

```bash
docker compose build
```

## **2. Ejecutar los servicios**

### **Pipeline ETL**

```bash
docker compose up etl
```

### **Jupyter Lab**

```bash
docker compose up jupyter
```

Accede en tu navegador a:

```
http://localhost:8888
```

## **3. Ver logs**

```bash
docker compose logs -f
```

---

## 📊 **4. Reproducir el EDA**

Los análisis se encuentran en los notebooks:

* `nb/01_1-eda-agricultura.ipynb`
* `nb/01_2-eda-hidricos.ipynb`
* `nb/02-eda.ipynb` *(EDA global utilizado para los reportes)*

Puedes abrirlos localmente:

```bash
make run_jupyter
```

o, en Docker:

```bash
docker compose up jupyter
```

---

## 🌐 **5. Resultados principales**

El análisis muestra una fuerte conexión entre la **superficie sembrada** y la **disponibilidad de agua** en presas, especialmente en los ciclos de sequía 2002–2004 y 2019–2021.

Gráfico destacado: `plots/disponibilidad_agua_sup_sembrada.png`

![Disponibilidad de agua vs Superficie sembrada](/plots/disponibilidad_agua_sup_sembrada.png)

Este gráfico cruza almacenamiento total en presas y superficie sembrada, mostrando que las caídas agrícolas coinciden con mínimos hídricos pronunciados.

---

## 📄 **6. Reportes**

### 📘 **Reporte técnico**

[`report/reporte-tecnico.md`](report/reporte-tecnico.md)

### ✍️ **Artículo estilo Medium**

[`report/reporte.md`](report/reporte.md)
(versión final publicada en Medium)

---

## 🖼️ **Crédito de imagen**

La imagen utilizada en la portada del proyecto:

> **“Wheat fields at CIMMYT's CENEB (Ciudad Obregón) experiment station”**
> por *International Maize and Wheat Improvement Center (CIMMYT)*,
> bajo licencia **CC BY-NC 2.0**.

[https://creativecommons.org/licenses/by-nc/2.0/](https://creativecommons.org/licenses/by-nc/2.0/)

---

## 📚 **Licencia**

Este proyecto está publicado bajo la licencia **MIT**.
