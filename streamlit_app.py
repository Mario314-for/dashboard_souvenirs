# -*- coding: utf-8 -*-
# App Streamlit para explorar datos de souvenirs
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Dashboard Souvenirs', layout='wide')
st.title('Dashboard Souvenirs - Marketing')

df = pd.read_csv('datos_souvenirs.csv', parse_dates=['fecha'])

st.sidebar.header('Filtros')
categoria_sel = st.sidebar.multiselect('Categoría', sorted(df['categoria'].unique().tolist()))
area_sel = st.sidebar.multiselect('Área destino', sorted(df['area_destino'].unique().tolist()))
rango_fecha = st.sidebar.date_input('Rango de fechas', [df['fecha'].min(), df['fecha'].max()])

f = df.copy()
if categoria_sel:
    f = f[f['categoria'].isin(categoria_sel)]
if area_sel:
    f = f[f['area_destino'].isin(area_sel)]
if len(rango_fecha) == 2:
    f = f[(f['fecha'] >= pd.to_datetime(rango_fecha[0])) & (f['fecha'] <= pd.to_datetime(rango_fecha[1]))]

col1, col2 = st.columns(2)

with col1:
    st.subheader('Ingresos mensuales por categoría')
    ts = f.groupby(['fecha', 'categoria'])['ingreso'].sum().reset_index()
    if not ts.empty:
        pivot_ts = ts.pivot(index='fecha', columns='categoria', values='ingreso').fillna(0)
        fig = plt.figure()
        pivot_ts.plot(ax=plt.gca())
        plt.xlabel('Mes'); plt.ylabel('Ingresos ($)'); plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info('No hay datos con los filtros actuales')

with col2:
    st.subheader('Salidas mensuales por área')
    salidas = f.groupby(['fecha','area_destino'])['salidas'].sum().reset_index()
    if not salidas.empty:
        pivot_stack = salidas.pivot(index='fecha', columns='area_destino', values='salidas').fillna(0)
        fig = plt.figure()
        pivot_stack.plot(kind='bar', stacked=True, ax=plt.gca())
        plt.xlabel('Mes'); plt.ylabel('Unidades'); plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info('No hay datos con los filtros actuales')

st.subheader('Pareto de ingresos por producto')
prod_ingresos = f.groupby('producto')['ingreso'].sum().sort_values(ascending=False)
if not prod_ingresos.empty:
    fig = plt.figure()
    ax = plt.gca()
    prod_ingresos.plot(kind='bar', ax=ax)
    ax.set_xlabel('Producto'); ax.set_ylabel('Ingresos ($)')
    ax2 = ax.twinx()
    cum = prod_ingresos.cumsum()/prod_ingresos.sum()*100
    ax2.plot(range(len(cum)), cum.values, marker='o')
    ax2.set_ylabel('Acumulado (%)'); ax2.set_ylim(0, 110)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info('No hay datos con los filtros actuales')

st.caption('Matplotlib sin estilos personalizados, una gráfica por figura')