import sys
from pathlib import Path
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QMessageBox, QTabWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

ARCHIVO_CSV = Path(__file__).resolve().parent / "datos.csv"

class VentanaInventario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de análisis de inventario")
        self.resize(1100, 720)
        try:
            self.datos = pd.read_csv(ARCHIVO_CSV)
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudo leer datos.csv:\n{error}")
            raise

        central = QWidget()
        self.setCentralWidget(central)
        principal = QVBoxLayout(central)

        titulo = QLabel("INVENTARIO DE SUCURSALES")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; padding: 8px;")
        principal.addWidget(titulo)

        controles = QHBoxLayout()
        controles.addWidget(QLabel("Filtrar por sucursal:"))
        self.combo_sucursal = QComboBox()
        self.combo_sucursal.addItem("Todas")
        self.combo_sucursal.addItems(sorted(self.datos["Sucursal"].dropna().unique()))
        self.combo_sucursal.currentTextChanged.connect(self.actualizar_vista)
        controles.addWidget(self.combo_sucursal)
        self.btn_resumen = QPushButton("Mostrar resumen Pandas")
        self.btn_resumen.clicked.connect(self.mostrar_resumen)
        controles.addWidget(self.btn_resumen)
        principal.addLayout(controles)

        self.etiqueta_resumen = QLabel()
        self.etiqueta_resumen.setStyleSheet("font-size: 13px; padding: 5px;")
        principal.addWidget(self.etiqueta_resumen)

        self.tabs = QTabWidget()
        principal.addWidget(self.tabs)

        tab_datos = QWidget()
        layout_datos = QVBoxLayout(tab_datos)
        self.tabla = QTableWidget()
        layout_datos.addWidget(self.tabla)
        self.tabs.addTab(tab_datos, "Datos del inventario")

        tab_graficos = QWidget()
        layout_graficos = QVBoxLayout(tab_graficos)
        self.figura = Figure(figsize=(8, 5))
        self.canvas = FigureCanvas(self.figura)
        layout_graficos.addWidget(self.canvas)
        self.tabs.addTab(tab_graficos, "Gráficos")

        self.actualizar_vista()

    def datos_filtrados(self):
        sucursal = self.combo_sucursal.currentText()
        if sucursal == "Todas":
            return self.datos.copy()
        return self.datos[self.datos["Sucursal"] == sucursal].copy()

    def actualizar_vista(self):
        datos = self.datos_filtrados()
        self.tabla.setRowCount(len(datos))
        self.tabla.setColumnCount(len(datos.columns))
        self.tabla.setHorizontalHeaderLabels(list(datos.columns))
        for fila, (_, registro) in enumerate(datos.iterrows()):
            for columna, valor in enumerate(registro):
                self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))
        self.tabla.resizeColumnsToContents()

        unidades = int(datos["Cantidad"].sum())
        valor_stock = (datos["Cantidad"] * datos["Precio"]).sum()
        self.etiqueta_resumen.setText(
            f"Registros: {len(datos)}    |    Unidades disponibles: {unidades:,}    "
            f"|    Valor estimado del stock: ${valor_stock:,.2f}"
        )
        self.actualizar_graficos()

    def actualizar_graficos(self):
        datos = self.datos_filtrados()
        self.figura.clear()
        ax1 = self.figura.add_subplot(121)
        ax2 = self.figura.add_subplot(122)
        por_categoria = datos.groupby("Categoria")["Cantidad"].sum().sort_values()
        if len(por_categoria):
            por_categoria.plot(kind="barh", ax=ax1)
        ax1.set_title("Unidades por categoría")
        ax1.set_xlabel("Unidades")

        por_sucursal = self.datos.groupby("Sucursal")["Cantidad"].sum().sort_values()
        por_sucursal.plot(kind="bar", ax=ax2)
        ax2.set_title("Stock por sucursal (total)")
        ax2.set_ylabel("Unidades")
        ax2.tick_params(axis="x", rotation=35)
        self.figura.tight_layout()
        self.canvas.draw()

    def mostrar_resumen(self):
        datos = self.datos_filtrados()
        mensaje = (
            f"Información general\n"
            f"Filas y columnas: {datos.shape}\n"
            f"Tipos de datos:\n{datos.dtypes.to_string()}\n\n"
            f"Valores faltantes por columna:\n{datos.isnull().sum().to_string()}\n\n"
            f"Estadísticas numéricas:\n{datos.describe().round(2).to_string()}"
        )
        QMessageBox.information(self, "Resumen de Pandas", mensaje)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaInventario()
    ventana.show()
    sys.exit(app.exec_())
