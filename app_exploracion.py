# Importación de librerías
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf 
import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff



# Función para añadir espacios para la app de streamlit
def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")
    

def app():

    ##################### PRIMER APARTADO: ELECCIÓN DE EMPRESA O STOCK Y FECHAS DE ANÁLISIS
    # Título
    st.markdown("<center><font face='WildWest' size='6' >EXPLORACIÓN DE COTIZACIONES BURSÁTILES</font><br /></center>", unsafe_allow_html=True)
    space(3)

    # Columnas para fechas y elección de stock
    c1, c2, c3, c4 = st.columns([0.5, 0.5, 0.5, 1])

    # Elección de fechas (inicio y final) para explorar los valores 
    with c1:
        stock = st.selectbox("Stock a predecir:", ['AMZN', 'MSFT', 'AAPL', 'GOOG', '^IBEX'])
    
    with c2:
        inicio = st.date_input("Fecha de inicio (formato año/mes/día):",
                            datetime.date(2019, 1, 1))
    with c3:
        final = st.date_input("Fecha final (formato año/mes/día):",
                           datetime.date.today())
    with c4:
        variables_grafico =  st.selectbox("Variables a introducir en el gráfico:", ['Sólo precios de cierre', 'Gráfico de Candlesticks', 'Precios de cierre y medias móviles simples (a 50 y 200 días)',  
                                                                                    'Precios de cierre y medias móviles exponenciales (a 50 y 200 días)', 
                                                                                    'Precio máximo alcanzado en el día'])

    space(3)

    ##################### SEGUNDO APARTADO: CARGA DE DATOS Y REPRESENTACIÓN GRÁFICA
    # Carga de datos
    datos = yf.download(stock, inicio, final)
    datos = pd.DataFrame(datos) 
    datos['Date'] = datos.index # Creo un campo fecha con el índice
    datos['Date'] = datos['Date'].dt.strftime('%Y-%m-%d') # Cambio de formato
    datos['SMA50'] = datos['Close'].rolling(50).mean() # Media móvil simple a 50 días
    datos['SMA200'] = datos['Close'].rolling(200).mean() # Media móvil simple a 200 días
    datos['EMA50'] = datos['Close'].ewm(span=50, adjust=False).mean() # Media móvil exponencial a 50 días
    datos['EMA200'] = datos['Close'].ewm(span=200, adjust=False).mean() # Media móvil exponencial a 200 días
    space(2)


    lista_graphs_1 = ['Sólo precios de cierre', 'Precios de cierre y medias móviles simples (a 50 y 200 días)', 
                      'Precios de cierre y medias móviles exponenciales (a 50 y 200 días)', 
                      'Precio máximo alcanzado en el día']

    if variables_grafico in lista_graphs_1:
        # Para las columnas
        c1, c2 = st.columns([1, 1])

        with c1:
            # Para sólo precios de cierre
            if variables_grafico == 'Sólo precios de cierre':
                fig = px.line(datos, x = 'Date', y = ['Close'])
                fig.update_layout(
                    title={
                        'text': "Precios de cierre",
                        'y':1,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                    xaxis_title="Fecha",
                    yaxis_title="Precio",
                    font=dict(
                        family="Sans-serif",
                        size=14),
                    legend_title="",
                    plot_bgcolor='rgba(0,0,0,0)'
                    )

                st.plotly_chart(fig, use_container_width=True)
            
            # Para precios de cierre y SMA
            elif variables_grafico == 'Precios de cierre y medias móviles simples (a 50 y 200 días)':
                fig = px.line(datos, x = 'Date', y = ['Close', 'SMA50', 'SMA200'])
                fig.update_layout(
                    title={
                        'text': "Precios de cierre y medias móviles simples",
                        'y':1,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                    xaxis_title="Fecha",
                    yaxis_title="Precio",
                    font=dict(
                        family="Sans-serif",
                        size=14),
                    legend_title="",
                    plot_bgcolor='rgba(0,0,0,0)'
                    )

                st.plotly_chart(fig, use_container_width=True)
            
            # Para precios de cierre y EMA
            elif variables_grafico == 'Precios de cierre y medias móviles exponenciales (a 50 y 200 días)':
                fig = px.line(datos, x = 'Date', y = ['Close', 'EMA50', 'EMA200'])
                fig.update_layout(
                    title={
                        'text': "Precios de cierre y medias móviles exponenciales",
                        'y':1,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                    xaxis_title="Fecha",
                    yaxis_title="Precio",
                    font=dict(
                        family="Sans-serif",
                        size=14),
                    legend_title="",
                    plot_bgcolor='rgba(0,0,0,0)'
                    )

                st.plotly_chart(fig, use_container_width=True)
            
            # Para precios máximos
            elif variables_grafico == 'Precio máximo alcanzado en el día':
                fig = px.line(datos, x = 'Date', y = ['High'])
                fig.update_layout(
                    title={
                        'text': "Precios máximos alcanzados",
                        'y':1,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                    xaxis_title="Fecha",
                    yaxis_title="Precio",
                    font=dict(
                        family="Sans-serif",
                        size=14),
                    legend_title="",
                    plot_bgcolor='rgba(0,0,0,0)'
                    )

                st.plotly_chart(fig, use_container_width=True)

        with c2:
            #st.markdown("<h2 style='text-align: center; color: white; font-size:0.7cm;'> Histórico de volumen </h2>", unsafe_allow_html=True)
            fig = px.line(datos, x = 'Date', y = 'Volume')
            fig.update_layout(
                title={
                    'text': "Histórico de volumen",
                    'y':1,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                xaxis_title="Fecha",
                yaxis_title="Volumen",
                font=dict(
                    family="Sans-serif",
                    size=14),
                plot_bgcolor='rgba(0,0,0,0)',
                )
                
            st.plotly_chart(fig, use_container_width=True)


    candlestick_graph = ['Gráfico de Candlesticks']
    if variables_grafico in candlestick_graph:

        # Para las columnas
        c1, c2, c3 = st.columns([0.2, 2, 0.2])

        with c1:
            st.write("")

        with c2:
            fig = go.Figure(data = [go.Candlestick(x = datos['Date'],
                        open = datos['Open'],
                        high = datos['High'],
                        low = datos['Low'],
                        close = datos['Close'])])
            fig.update_layout(
                title={
                    'text': "Candlesticks",
                    'y':1,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                xaxis_title="Fecha",
                yaxis_title="Stock",
                font=dict(
                    family="Sans-serif",
                    size=14),
                plot_bgcolor='rgba(0,0,0,0)',
                )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with c3:
            st.write("")