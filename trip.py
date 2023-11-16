import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.express as px
import pandas as pd

def load_trip():
    #any dataset you gathered, which must include lat,long, and speed. 
    file_path = './trip1.xlsx'
    data = pd.read_excel(file_path)
    return data

def gen_plot(data):
    lat = data['Lat']
    lon = data['Lng']
    velocity = data['SpeedMPH']
    fig = px.scatter_mapbox (
        data, 
        lat=lat,
        lon=lon, 
        color=velocity,
        color_continuous_scale=px.colors.sequential.Plasma,
        zoom=10,
        height=600,
        mapbox_style="open-street-map"
    )
    return fig

def fig_to_HTML(fig):
    plot_html = fig.to_html(include_plotlyjs='cdn')
    return plot_html

def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.resize(800, 600)
    web_engine_view = QWebEngineView(main_window)
    data = load_trip()
    fig = gen_plot(data)
    web_engine_view.setHtml(fig_to_HTML(fig))
    main_window.setCentralWidget(web_engine_view)
    main_window.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()