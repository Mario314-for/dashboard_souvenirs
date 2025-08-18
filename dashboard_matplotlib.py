# -*- coding: utf-8 -*-
# Dashboard de Souvenirs - Matplotlib
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('datos_souvenirs.csv', parse_dates=['fecha'])

# 1) Serie de tiempo de ingresos por categoría
ts = df.groupby(['fecha', 'categoria'])['ingreso'].sum().reset_index()
pivot_ts = ts.pivot(index='fecha', columns='categoria', values='ingreso').fillna(0)
plt.figure()
pivot_ts.plot(ax=plt.gca())
plt.title('Ingresos mensuales por categoría')
plt.xlabel('Mes')
plt.ylabel('Ingresos ($)')
plt.tight_layout()
plt.savefig('assets/serie_ingresos_categoria.png', dpi=140)
plt.close()

# 2) Barras apiladas de salidas por área
salidas_m_area = df.groupby(['fecha','area_destino'])['salidas'].sum().reset_index()
pivot_stack = salidas_m_area.pivot(index='fecha', columns='area_destino', values='salidas').fillna(0)
plt.figure()
pivot_stack.plot(kind='bar', stacked=True, ax=plt.gca())
plt.title('Salidas mensuales por área de destino')
plt.xlabel('Mes')
plt.ylabel('Unidades')
plt.tight_layout()
plt.savefig('assets/barras_apiladas_salidas_area.png', dpi=140)
plt.close()

# 3) Heatmap de correlación
corr = pivot_ts.corr()
plt.figure()
plt.imshow(corr, aspect='auto')
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha='right')
plt.yticks(range(len(corr.index)), corr.index)
plt.title('Matriz de correlación de ingresos por categoría')
plt.colorbar()
plt.tight_layout()
plt.savefig('assets/heatmap_correlacion.png', dpi=140)
plt.close()

# 4) Pareto de ingresos por producto
prod_ingresos = df.groupby('producto')['ingreso'].sum().sort_values(ascending=False)
plt.figure()
ax = plt.gca()
prod_ingresos.plot(kind='bar', ax=ax)
ax.set_title('Pareto de ingresos por producto')
ax.set_xlabel('Producto')
ax.set_ylabel('Ingresos ($)')
ax2 = ax.twinx()
cum = prod_ingresos.cumsum()/prod_ingresos.sum()*100
ax2.plot(range(len(cum)), cum.values, marker='o')
ax2.set_ylabel('Acumulado (%)')
ax2.set_ylim(0, 110)
plt.tight_layout()
plt.savefig('assets/pareto_productos.png', dpi=140)
plt.close()

print('Gráficas generadas en carpeta assets/')