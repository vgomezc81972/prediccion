# Importación de librerías
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf 
import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly



# Función para añadir espacios para la app de streamlit
def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")
    

def app():

    ##################### PRIMER APARTADO: ELECCIÓN DE EMPRESA O STOCK Y FECHAS DE PREDICCIONES
    # Título
    st.markdown("<center><font face='WildWest' size='6' >PREDICCIÓN DE COTIZACIONES BURSÁTILES</font><br /></center>", unsafe_allow_html=True)
    space(3)

    # Columnas para fechas y elección de stock
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])

    # Elección de fechas (inicio y final) para explorar los valores 
    with c1:
        stock = st.selectbox("Stock a elegir:", ['AMZN', 'MSFT', 'AAPL', 'GOOG', '^IBEX'])
    
    with c2:
        inicio = st.date_input("Fecha de inicio de datos (formato año/mes/día):",
                            datetime.date(2019, 1, 1))
    with c3:
        final = st.date_input("Fecha final de datos (formato año/mes/día):",
                           datetime.date.today())
    with c4:
        dias_a_predecir = st.number_input("Días a predecir (entre 1 y 800): ", min_value = 1, max_value = 800)
        st.write("Días a predecir escogido: ", dias_a_predecir)

    space(1)

    ##################### SEGUNDO APARTADO: CARGA DE DATOS Y REPRESENTACIÓN GRÁFICA
    # Carga de datos
    datos = yf.download(stock, inicio, final)
    datos = pd.DataFrame(datos) 
    datos = datos.reset_index() 
    datos['Date'] = datos['Date'].dt.strftime('%Y-%m-%d') # Cambio de formato

    # Campos para Prophet
    datos = datos.loc[:, ['Date', 'Close']]
    datos = datos.rename(columns = {"Date":"ds","Close":"y"}) # Prophet necesita columna "ds" e "y"


    ##################### REALIZACIÓN DE PREDICCIONES (BOTÓN PARA LLEVARLO A CABO)
    
    # Columnas para botón
    c1, c2, c3 = st.columns([1, 1, 1])   

    c1.write("")
    with c2:
        boton_predicciones = st.button("Click para realizar las predicciones con Prophet 🗲")
    c3.write("")

    # Columnas para resumen
    if boton_predicciones: 
        c1, c2, c3, c4 = st.columns([1, 1, 1, 1])

        with c1:
            st.write("Stock elegido: ", stock)
        
        with c2:
            st.write("Fecha de inicio de datos elegido: ", inicio)
        
        with c3:
            st.write("Fecha final de datos elegido: ", final)
        
        with c4:
            st.write("Días elegidos para predecir: ", dias_a_predecir)

        c1, c2, c3 = st.columns([0.2, 2, 0.2])
            
        c1.write("")
        
        with c2:

            # Prophet 
            model = Prophet(daily_seasonality = True)
            model.fit(datos)

            # Predicción
            fut = model.make_future_dataframe(periods=dias_a_predecir) 
            forecast = model.predict(fut)

            # Gráfico
            fig = plot_plotly(model, forecast)
            fig.update_layout(
                xaxis_title="Fecha",
                yaxis_title="Stock",
                font=dict(
                    family="Sans-serif",
                    size=14),
                legend_title="",
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend = False,
                )      
            fig.update_traces(marker=dict(size=3, color = 'white'))

            st.plotly_chart(fig, use_container_width=True)
        
        c3.write("")




    