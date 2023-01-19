import streamlit as st
#st.set_page_config(page_title="UniSwapV3 Impermanent Loss", layout="wide")
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import numpy as np

st.title("Uniswap V3 Impermanent Loss")
st.subheader("Input")

P = st.number_input('ETH Price')
col1, col2 = st.columns(2)
P_min = col1.number_input('Min Price')
P_max = col2.number_input('Max Price')

y = st.number_input('USDC in Pool', value=100.00)
L=(np.sqrt(P_min)/min(P, P_max)+1/np.sqrt(min(P, P_max)))/(1-P_min/min(P,P_max))*y                                                                               
x=max(0,(np.sqrt(P_min)/P - 1/np.sqrt(P_max))*L+y/P)
st.write("ETH in Pool:")
st.text(x)

lower_bound = P_min/10000
upper_bound = 2.1*P_max
step = upper_bound/10000
prices = np.arange(P_min/1000,2*P_max+1,step)

loss = []
for price in prices:
    x_future = max(0,L*(min(1/np.sqrt(P_min),1/np.sqrt(price))-1/np.sqrt(P_max)))
    y_future = max(0,L*(min(np.sqrt(P_max),np.sqrt(price))-np.sqrt(P_min)))
    loss.append(-y_future - x_future * price + y+x*price)

df=pd.DataFrame()
df["Price"] = prices
df["Impermanent Loss"] = loss

fig = px.line(df, x="Price", y="Impermanent Loss", title='Impermanent Loss Chart (Token1 denominated)')
fig.update_xaxes(title_text='Price')
fig.update_yaxes(title_text='Impermanent Loss')
st.plotly_chart(fig,use_container_width=True)

st.subheader("PnL Calculation")

lower_bound = P_min/10000
upper_bound = 2.1*P_max
step = upper_bound/10000
prices = np.arange(P_min/1000,2*P_max+1,step)

pnl = []
for price in prices:
    x_future = max(0,L*(min(1/np.sqrt(P_min),1/np.sqrt(price))-1/np.sqrt(P_max)))
    y_future = max(0,L*(min(np.sqrt(P_max),np.sqrt(price))-np.sqrt(P_min)))
    pnl.append(y_future + x_future * price - y)
    
df = pd.DataFrame()
df["Price"] = prices
df["PNL"] = pnl

fig = px.line(df, x="Price", y="PNL", title='Impermanent loss without hedging')
fig.update_xaxes(title_text='Price')
fig.update_yaxes(title_text='PNL')
fig.show()


