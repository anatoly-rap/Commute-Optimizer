import sys
from PyQt5.QtWidgets import  QSpacerItem, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QSize
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

def calculate_metrics(data):
    min_speed = data['SpeedMPH'].min()
    max_speed = data['SpeedMPH'].max()
    avg_speed = data['SpeedMPH'].mean()
    return min_speed, max_speed, avg_speed

def gen_speed_time_graph(data, min_speed, max_speed, avg_speed):
    fig = px.line(data, x='Time', y='MPH', title=f'Speed Over Time (Min: {min_speed} MPH, Max: {max_speed} MPH, Avg: {avg_speed} MPH)')
    fig.update_layout(xaxis_title='Time', yaxis_title='Speed (MPH)')
    return fig

def combine_plots_to_html(map_fig, speed_fig):
    map_html = map_fig.to_html(full_html=False, include_plotlyjs='cdn')
    speed_html = speed_fig.to_html(full_html=False, include_plotlyjs=False)
    combined_html = f"<html><head></head><body><div style='display:flex;justify-content:space-between;'>{map_html}{speed_html}</div></body></html>"
    return combined_html

def setup_header_label():
    header_label = QLabel("Commute Optimizer")
    header_label.setAlignment(Qt.AlignCenter)
    size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    header_label.setSizePolicy(size_policy)
    return header_label

def setup_map_view(data):
    map_view = QWebEngineView()
    map_view.setFixedSize(QSize(600, 650))
    map_view.setHtml(gen_plot(data).to_html(include_plotlyjs='cdn'))
    return map_view

def setup_speed_view(data):
    min_speed, max_speed, avg_speed = calculate_metrics(data)
    speed_fig = gen_speed_time_graph(data, min_speed, max_speed, avg_speed)
    speed_view = QWebEngineView()
    speed_view.setFixedSize(QSize(600, 650))
    speed_view.setHtml(speed_fig.to_html(include_plotlyjs='cdn'))
    return speed_view

def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_widget = QWidget()
    grid_layout = QGridLayout(main_widget)
    grid_layout.addWidget(
        setup_header_label(), 0, 0, 1, 2)
    grid_layout.addWidget(
        setup_map_view(
            load_trip()), 1, 0)
    grid_layout.addWidget(
        setup_speed_view(load_trip()), 1, 1) 
    grid_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 0, 1, 2)
    main_widget.setLayout(grid_layout)
    main_window.setCentralWidget(main_widget)
    main_window.setFixedSize(QSize(1200, 650))
    main_window.show()
    sys.exit(app.exec_())
if __name__=="__main__":
    main()
