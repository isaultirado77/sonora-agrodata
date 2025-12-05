# **Análisis de Agricultura y Disponibilidad Hídrica en Sonora (1999–2021)**

### *Reporte Técnico*

Este documento presenta el análisis exploratorio realizado sobre dos conjuntos de datos oficiales del Gobierno del Estado de Sonora:

1. **Agricultura Sonora (1999–2022)**
2. **Recursos Hídricos de Sonora (1941–2024)**

El objetivo es integrar, limpiar y analizar ambos datasets para entender la evolución agrícola del estado y su relación con la disponibilidad de agua en presas.

---

# 1. **Datos utilizados**

## 1.1 Agricultura Sonora (1999–2022)

Fuente oficial: Gobierno del Estado de Sonora — Datos Abiertos
URL: [https://datos.sonora.gob.mx/dataset/Agricultura%20Sonora](https://datos.sonora.gob.mx/dataset/Agricultura%20Sonora)
Formato original: 24 archivos Excel (uno por año)

Los datos contienen registros de:

* Superficie sembrada, cosechada y siniestrada
* Producción total y rendimiento
* Precio medio rural y valor económico
* Identificación de municipio, DDR, ciclo agrícola, cultivo y variedad

Problemas detectados:

* Variaciones en nombres de columnas
* Strings inconsistentes (tildes, mayúsculas, duplicaciones)
* Prefijos innecesarios como `"ddr "`
* Claves tratadas como texto por inconsistencias numéricas

### Transformación aplicada

```python
dfs = list(pd.read_excel(path, sheet_name='Hoja1') for path in data_paths)
agricultura = pd.concat(dfs)
agricultura = normalize_str(agricultura)
agricultura = agricultura.rename(columns=AGR_COLUMNS_MAP)
agricultura['distrito_ddr'] = agricultura['distrito_ddr'].str.replace('ddr ', '')
```

Principales pasos:

1. **Lectura y concatenación** de todos los años
2. **Normalización de strings** (minúsculas, sin acentos, sin caracteres especiales)
3. **Renombrado estandarizado** usando un mapa de columnas
4. **Corrección en distrito_ddr**
5. Exportación a `agricultura_processed.csv`

### Estructura final

 (ver [diccionario](../references/diccionario-agricultura.md) completo)

Columnas relevantes:

* `ano` — año del registro
* `sup_sembrada_ha` — hectáreas sembradas
* `sup_cosechada_ha` — hectáreas cosechadas
* `produccion_ton` — toneladas producidas
* `valor_produccion_miles_pesos` — valor económico

---

## 1.2 Recursos Hídricos de Sonora (1941–2024)

Fuente oficial: Gobierno del Estado de Sonora
URL: [https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos](https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos)
Archivos originales: por década (excepto 1960–1969)

Contenido:

* Clave de presa
* Fecha
* Nivel de almacenamiento (hm³)

Problemas detectados:

* Década faltante (1960–1969)
* Errores de codificación (`hmÂ3`)
* Fechas en formatos mixtos
* Falta de encabezado en los archivos

### Transformación aplicada

```python
dfs = list(pd.read_excel(path, sheet_name='Hoja1') for path in data_paths)
hidricos = pd.concat(dfs)
hidricos.columns = ['clave', 'fecha', 'almacenamiento_hm3']
hidricos['clave'] = hidricos.clave.str.lower()
```

Pasos:

1. Unión de todos los archivos
2. Asignación manual de nombres a columnas
3. Normalización de claves
4. Exportación a `hidricos_processed.csv`

### Estructura final

Columnas:

* `clave`
* `fecha`
* `almacenamiento_hm3`

---

# 2. **Análisis Exploratorio**

## 2.1 Evolución agrícola (1999–2021)

![Superficie Sembrada vs Cosechada 1999-2021](../plots/superficie_sembrada_cosechada.png)

Principales hallazgos:

* La superficie sembrada muestra un comportamiento estable con picos en 2016 y caídas en 2004 y 2020.
* La superficie cosechada sigue el mismo patrón, lo que indica bajas tasas de siniestro.
* Los descensos más fuertes coinciden con años de baja disponibilidad hídrica.

---

## 2.2 Cultivos más importantes

![Comparación de Superficie, Producción y Valor por Cultivo (Top 10)](../plots/top_cultivos.png)

Hallazgos clave:

* **Trigo:** mayor superficie y producción.
* **Uva, espárrago y papa:** generan mayor valor económico.
* **Alfalfa:** relevante en superficie y valor.
* Sistema dual: cultivos extensivos ↔ cultivos intensivos de alta rentabilidad.

---

## 2.3 Cultivos en crecimiento o declive

![Evolución de la superficie sembrada por cultivo](../plots/superficie_sembrada_cultivo.png)

![Cambio porcentual 1999–2021 en superficie sembrada (Top 10)](../plots/cambio_sup_sembrada.png)

Cambios porcentuales:

* Caídas fuertes: algodón (-93%), cártamo (-85%), uva (-27%)
* Crecimiento: espárrago (+191%), papa (+176%), alfalfa (+52%)
* Moderados: trigo (+16%), maíz (+9%)

El sistema agrícola se desplaza hacia cultivos de alto valor económico.

---

# 3. **Disponibilidad de agua y relación con la agricultura**

![Disponibilidad de agua vs Superficie sembrada](../plots/disponibilidad_agua_sup_sembrada.png)

Hallazgos:

* Periodos secos: 2002–2004 y 2019–2021.
* Estos años coinciden con reducciones en superficies sembradas.
* Periodos de mayor almacenamiento (2008–2010 y 2014–2016) acompañan expansiones agrícolas.
* La agricultura responde directamente a los ciclos hídricos, aunque no se establece causalidad.

---

# 4. **Limitaciones**

* Catálogos oficiales incompletos
* No se validó información geográfica o hidroagrícola
* El análisis es correlacional, no causal
* Precios y valor económico dependen de factores externos no incluidos en los datos

---

# 5. **Archivos finales en este repositorio**

```
/data/raw/agricultura/*.xlsx
/data/raw/hidricos/*.xlsx
/data/processed/agricultura_processed.csv
/data/processed/hidricos_processed.csv
/notebooks/eda.ipynb
/figures/*.png
README.md (este documento)
```

---

# 6. **Resumen técnico**

Este análisis integró más de 20 años de datos agrícolas y más de 80 años de datos hidrológicos para explorar la relación entre superficie sembrada, cultivos principales y disponibilidad de agua. La evidencia sugiere que la agricultura sonorense mantiene estabilidad general, pero sus oscilaciones dependen en gran medida de los ciclos hídricos del estado. El uso combinado de datos agrícolas y de presas permite desarrollar futuras líneas de investigación en manejo del agua, predicción de superficies o impactos climáticos.
