import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import folium
import csv
import sys
import webbrowser
import re
from folium import plugins

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Devices Mapper")
        self.setGeometry(500, 200, 200, 150)
        self.setLayout(qtw.QVBoxLayout())

        #Generates PyQt5 Label
        my_label = qtw.QLabel("Show multiple devices on one map")
        my_label.setFont(qtg.QFont('Helvetica', 18))
        my_label.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(my_label)

        #Generates PyQt5 Label
        my_label1 = qtw.QLabel("Enter device list like '1002, 1003, ...'")
        my_label1.setFont(qtg.QFont('Helvetica', 12))
        my_label1.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(my_label1)

        #Generates PyQt5 Box
        inputBox = qtw.QLineEdit()
        inputBox.setObjectName("device")
        #Placeholder text to speed up testing
        #inputBox.setText("1001, 1002, 1004, 1006, 1008, 1010")
        self.layout().addWidget(inputBox)

        #Generates PyQt5 Button
        button = qtw.QPushButton("Map Listed Devices", clicked = lambda: button_pressed())
        self.layout().addWidget(button)
        self.show()

        #Generates PyQt5 Label
        my_label2 = qtw.QLabel("or")
        my_label2.setFont(qtg.QFont('Helvetica', 12))
        my_label2.setAlignment(qtc.Qt.AlignCenter)
        self.layout().addWidget(my_label2)
        
        #Generates Second PyQt5 Button
        button1 = qtw.QPushButton("Map Whole Spreadsheet File", clicked = lambda: button1_pressed())
        self.layout().addWidget(button1)
        self.show()
        
        def set_marker(color, layer, row):
            csv_file = csv.reader(open('sample_device_list.csv', "r"), delimiter=",")
            row
            folium.Marker([row[1], row[2]],
                                        tooltip=row[3],
                                        icon=plugins.BeautifyIcon(icon='arrow-down',
                                                                  icon_shape="marker",
                                                                  iconSize=[40,40],
                                                                  number=row[0],
                                                                  inner_icon_style='font-family:Verdana, sans-serif; text-align: left; font-size:14px',
                                                                  border_color=(color),
                                                                  background_color=(color))
                                                                  #background_color='#76cba1')
                                        ).add_to(layer)
        
        def button_pressed():
            m = folium.Map(location=[38.433993,-122.717628],tiles=None, control_scale=True, zoom_start=11)
            folium.TileLayer(tiles='openstreetmap', name='Normal').add_to(m)
            folium.TileLayer('Stamen Terrain', name='Terrain map').add_to(m)
            folium.TileLayer('Stamen Toner', name='Printer friendly').add_to(m)
            layer_fuses = folium.FeatureGroup(name='Fuses')
            layer_reclosers = folium.FeatureGroup(name='Reclosers')
            layer_regulators = folium.FeatureGroup(name='Regulators')
            layer_capacitors = folium.FeatureGroup(name='Capacitors')
            layer_fuses.add_to(m)
            layer_reclosers.add_to(m)
            layer_regulators.add_to(m)
            layer_capacitors.add_to(m)
            folium.LayerControl().add_to(m)
            device_string = inputBox.text()
            device_list = device_string.split(", ")

            for single_plot in device_list:
                csv_file = csv.reader(open('sample_device_list.csv', "r"), delimiter=",")
                for row in csv_file:
                    if single_plot == row[0] and row[3] == 'Capacitor':
                                set_marker('#76cba1', layer_capacitors, row)
                    elif single_plot == row[0] and row[3] == 'Recloser':
                                set_marker('orange', layer_reclosers, row)
                    elif single_plot == row[0] and row[3] == 'Fuse':
                                set_marker('#6db6ff', layer_fuses, row)
                    elif single_plot == row[0] and row[3] == 'Regulator':
                                set_marker('#9999dd', layer_regulators, row)
                    if single_plot == 'all' and row[3] == 'Capacitor':
                                set_marker('#76cba1', layer_capacitors, row)
                    elif single_plot == 'all' and row[3] == 'Recloser':
                                set_marker('orange', layer_reclosers, row)
                    elif single_plot == 'all' and row[3] == 'Fuse':
                                set_marker('#6db6ff', layer_fuses, row)
                    elif single_plot == 'all' and row[3] == 'Regulator':
                                set_marker('#9999dd', layer_regulators, row)
            m
            m.save('devicelistmap.html')
            webbrowser.open_new_tab('devicelistmap.html')

        def button1_pressed():
            m = folium.Map(location=[38.433993,-122.717628],tiles=None, control_scale=True, zoom_start=11)
            folium.TileLayer(tiles='openstreetmap', name='Normal').add_to(m)
            folium.TileLayer('Stamen Terrain', name='Terrain map').add_to(m)
            folium.TileLayer('Stamen Toner', name='Printer friendly').add_to(m)
            
            layer_fuses = folium.FeatureGroup(name='Fuses')
            layer_reclosers = folium.FeatureGroup(name='Reclosers')
            layer_regulators = folium.FeatureGroup(name='Regulators')
            layer_capacitors = folium.FeatureGroup(name='Capacitors')
            layer_other = folium.FeatureGroup(name='Other')
            filedialog = qtw.QFileDialog.getOpenFileName(self, "Select a file...", "", "Spreadsheet (*.csv *.xml *.kml)")
            csv_file = csv.reader(open(filedialog[0], "r"), delimiter=",")
            
            for row in csv_file:
                if row[3] == 'Capacitor':
                                layer_capacitors.add_to(m)
                                set_marker('#76cba1', layer_capacitors, row)
                elif row[3] == 'Recloser':
                                set_marker('orange', layer_reclosers, row)
                elif row[3] == 'Fuse':
                                layer_fuses.add_to(m)
                                set_marker('#6db6ff', layer_fuses, row)
                elif row[3] == 'Regulator':
                                set_marker('#9999dd', layer_regulators, row)
            
                elif row[0].isdigit():
                                set_marker('#9999dd', m, row)
            
            folium.LayerControl().add_to(m)            
            m
            m.save('devicelistmap.html')
            webbrowser.open_new_tab('devicelistmap.html')

app = qtw.QApplication([])
mw = MainWindow()
app.exec_()
