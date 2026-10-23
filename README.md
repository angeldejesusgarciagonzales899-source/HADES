# Sistema de análisis de inventario

Proyecto académico para Programación Computacional III – Segundo Cómputo angel de jesus garcia gonzalez, david alejandro cruz albarenga.

## Descripción
Aplicación de escritorio en Python con PyQt5, Pandas y Matplotlib. Lee `datos.csv`, permite filtrar por sucursal, muestra una tabla del inventario, gráficos y un resumen estadístico.

## Sucursales
- San Salvador
- Santa Ana
- San Miguel
- La Libertad
- Sonsonate

## Requisitos
- Python 3.11 recomendado
- Ver `requirements.txt`

## Instalación en Windows
Abre PowerShell dentro de esta carpeta y ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python inventario_app.py
```

Si PowerShell bloquea la activación del entorno, puedes ejecutar directamente:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe inventario_app.py
```

## Análisis con Pandas
La aplicación usa `shape`, `dtypes`, `isnull().sum()` y `describe()` para inspeccionar los datos. Los gráficos se crean con Matplotlib.

## Archivos
- `inventario_app.py`: aplicación gráfica.
- `datos.csv`: inventario simulado de 100 registros.
- `informe_consultoria.pdf`: informe de resultados.
- `requirements.txt`: dependencias.
- `.gitignore`: archivos temporales excluidos.

## Integrantes
1. [angel de jesus garcia gonzalez]
2. [david alejandro cruz albarenga]

## Nota sobre los datos
Los registros son simulados con fines académicos y no representan ventas o inventarios reales de una empresa.
