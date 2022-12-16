from Function_Set import *
from Setting import *
from Raw_Data_Process import *

fig = go.Figure();
fig = make_subplots(rows=4, cols=1,shared_xaxes=True,
                vertical_spacing=0.01, 
                row_heights=[0.5,0.1,0.2,0.2]);
fig.add_trace(go.Candlestick(
                x= raw_data_eth.index,
                open=raw_data_eth["Open"],
                high=raw_data_eth['High'],
                low=raw_data_eth['Low'],
                close=raw_data_eth['Close'],
                increasing_line_color= 'red', decreasing_line_color= 'green'))
fig.add_trace(go.Scatter(x = raw_data_eth.index, y=raw_data_eth["Nor_Slope"],mode='lines',
                    name='ETH'),
                    row=2,col=1)

fig.update_layout(
    title='ETH Price from 2021-01-01 to 2021-12-31',
    # remove rangeslider
    xaxis_rangeslider_visible=False,
    yaxis_title='ETH',
    # shapes = [dict(
    #     x0= from_time_str, x1= to_time_str, y0=0, y1=1, xref='x', yref='paper',
    #     line_width=2)],
    )
fig.show()
