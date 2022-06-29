import streamlit as st
from streamlit_option_menu import option_menu
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
from smartapi import SmartConnect
from spacy import displacy
from bs4 import BeautifulSoup
import matplotlib
import spacy
import streamlit as st
import os

from spacy import displacy
from bs4 import BeautifulSoup
import matplotlib
from PIL import Image


hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
            #MainMenu {visibility: hidden;}

st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#with st.sidebar:
  #horizontal menu
selected2 = option_menu(None, ["Home","Auto-Trade", "Prediction", "Compare", "Alert"], 
    icons=['house',"robot", "graph-up-arrow", 'sliders',"bell-fill"], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected2


#HOME


if selected2 == "Home":

  #opening the image

  image = Image.open('page.png')



  #displaying the image on streamlit app
  col1, col2, col3 = st.columns([0.2, 5, 0.2])
  col2.image(image, use_column_width=True)

  st.title('Live Chart')



#Auto-Trade

if selected2 == "Auto-Trade":

  #opening the image

  image = Image.open('Auto trade.png')



  #displaying the image on streamlit app
  col1, col2, col3 = st.columns([0.2, 5, 0.2])
  col2.image(image, use_column_width=True)



  obj = SmartConnect(api_key = 'B94qZLC7')
  data = obj.generateSession('P714176', 'P@ssw0rd@123')

  def place_order(orderparams):
      try:
          orderID = obj.placeOrder(orderparams)
          placeholder1.success(f"The Order ID for Symbol {orderparams['tradingsymbol']} is: {orderID}")
      except Exception as e:
          placeholder1.error(f"Order placement for Symbol {orderparams['tradingsymbol']} failed: {e}")

  def generate_trade_list(uploaded_file):

      try:
          df = pd.read_csv(uploaded_file)
      except Exception as e:
          df = pd.read_excel(uploaded_file)
      trade_list = [] #empty list

    #looping over each row in the dataframe and storing
    #the value in each column to generate orderparams dict
    #we use str to convert to strings
      for index, rows in df.iterrows():
          new_dict = {"variety": str(rows['variety']), 
                      "tradingsymbol" : str(rows['tradingsymbol']),
                      "symboltoken" : str(rows['symboltoken']),
                      "transactiontype": str(rows['transactiontype']), 
                      "exchange": str(rows['exchange']),
                      "ordertype": str(rows['ordertype']), 
                      "producttype": str(rows['producttype']),
                      "duration": str(rows['duration']), 
                      "price": str(rows['price']), 
                      "quantity": str(rows['quantity']),
                      "triggerprice": str(rows['triggerprice'])}

          trade_list.append(new_dict)

      return trade_list

  if __name__ == '__main__':

      st.title("Trade Hassle-free")

      with st.form(key = 'angel_broking_execution'):

          uploaded_file = st.file_uploader("Upload your trades file", type = ['xlsx', 'csv'])
          submitbutton = st.form_submit_button("Submit")

          if submitbutton:
              trade_list = generate_trade_list(uploaded_file)
              placeholder1 = st.empty()
              for trade in trade_list:
                  place_order(trade)



#Prediction

if selected2 == "Prediction":

  START = "2015-01-01"
  TODAY = date.today().strftime("%Y-%m-%d")
  st.title('Stock Forecast App')
  stocks = ('GOOGL', 'AAPL', 'MSFT', 'TSLA', 'AMZN', 'FB', 'NFLX', 'BTC-USD')
  selected_stock = st.selectbox('Select dataset for prediction', stocks)
  n_years = st.slider('Years of prediction:', 1, 4)
  period = n_years * 365

  @st.cache
  def load_data(ticker):
      data = yf.download(ticker, START, TODAY)
      data.reset_index(inplace=True)

      return data

  

  data_load_state = st.text('Loading data...')
  data = load_data(selected_stock)
  data_load_state.text('Loading data... done!')

  st.subheader('Raw data')
  st.write(data.tail())

#Plot raw data

  def plot_raw_data():
	  fig = go.Figure()
	  fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	  fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	  fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	  st.plotly_chart(fig)
	
  plot_raw_data()

# Predict forecast with Prophet.
  df_train = data[['Date','Close']]
  df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

  m = Prophet()
  m.fit(df_train)
  future = m.make_future_dataframe(periods=period)
  forecast = m.predict(future)

# Show and plot forecast
  st.subheader('Forecast data')
  st.write(forecast.tail())
    
  st.write(f'Forecast plot for {n_years} years')
  fig1 = plot_plotly(m, forecast)
  st.plotly_chart(fig1)

  st.write("Forecast components")
  fig2 = m.plot_components(forecast)
  st.write(fig2)



 #Compare

if selected2 == "Compare":
  st.title('Compare-O-Meter')

  tickers = ('TSLA', 'AAPL', 'MSFT', 'BTC-USD', 'ETH-USD','NFLX')

  dropdown = st.multiselect('Pick your assets', tickers)

  start = st.date_input('Start', value = pd.to_datetime('2021-01-01'))
  end = st.date_input('End', value = pd.to_datetime('today'))

  def relativeret(df):
    rel = df.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret


  if len(dropdown) > 0:
    df = relativeret(yf.download(dropdown,start,end)['Adj Close'])
    st.line_chart(df)

if selected2 == "Alert":

    #opening the image

  image = Image.open('Alert.png')



  #displaying the image on streamlit app
  col1, col2, col3 = st.columns([0.2, 5, 0.2])
  col2.image(image, use_column_width=True)



  import streamlit as st 
  st.title("Get Evey Price Actions!")
  st.write("[Join our Telegram Channel to get live upadtes Of Market Movements!](https://t.me/sppalert)")
  