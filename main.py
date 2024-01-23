import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
# Der hier verwendete Code war zuvor eine HTML Seite mit JavaScript Code und wurde zu Python übersetzt und weiter angepasst.
st.set_page_config(page_title="log-run", page_icon="logo/logo.png", layout='wide')
# creating a link
def create_link(url,text):
    return '<a href="{}" target="_blank">{}</a>'.format(url, text)
# check if a number is even
def is_even(number):
    return number % 2 == 0
# snow- and windload
if "wind_load" not in st.session_state:
    st.session_state.wind_load = 0
if "snow_load" not in st.session_state:
    st.session_state.snow_load = 0
if "snow_and_wind" not in st.session_state:
        st.session_state.snow_and_wind = [st.session_state.wind_load,st.session_state.snow_load]
if "snow_data" not in st.session_state:
    st.session_state.snow_data = pd.read_excel('tabellen/Tebelle_Schneelast.xlsx')
if "data_storage_snow" not in st.session_state:
    st.session_state.data_storage_snow = {}
    # Erstellung der Datenbank mit Werten für kanthölzer.
    for rows in st.session_state.snow_data.iterrows():
        key = f"{rows[1]['Höhe NN']}"
        values = {
            "1": rows[1]['1'],
            "1a": rows[1]['1a'],
            "2": rows[1]['2'],
            "2a": rows[1]['2a'],
            "3": rows[1]['3']
        }
        st.session_state.data_storage_snow[key] = values
def more_information_snow():
    option_height = [
        "=< 200 m",
        "300 m",
        "400 m",
        "500 m",
        "600 m",
        "700 m",
        "800 m",
        "900 m",
        "1000 m",
        "1100 m",
        "1200 m",
        "1300 m",
        "1400 m",
        "1500 m"
    ]
    option_zone = [
        "1",
        "1a",
        "2",
        "2a",
        "3"
    ]
    st.session_state.snow_and_wind.clear()
    st.session_state.selected_option_snow_height = st.selectbox("Geländehöhe von NN", list(option_height), index=0)
    st.session_state.selected_option_snow_zone = st.selectbox("Zonenauswahl", list(option_zone), index=2)
    st.session_state.snow_load = st.session_state.data_storage_snow[st.session_state.selected_option_snow_height][st.session_state.selected_option_snow_zone]*0.8
    st.session_state.snow_load = round(st.session_state.snow_load, 2)
    new_snow=[st.session_state.snow_load, st.session_state.wind_load]
    st.session_state.snow_and_wind.append(new_snow)
    st.write(f"Schneelast = {st.session_state.snow_load}kn/m²")
    if np.isnan (st.session_state.snow_and_wind[0][0]):
        st.error("Bitte gib eine gültige Zone ein.")
        return
if "wind_data" not in st.session_state:
    st.session_state.wind_data = pd.read_excel('tabellen/Tabelle_Windlast.xlsx')
if "data_storage_wind" not in st.session_state:
    st.session_state.data_storage_wind = {}
    # Erstellung der Datenbank mit Werten für kanthölzer.
    for rows in st.session_state.wind_data.iterrows():
        key = f"{rows[1]['Ort']}"
        values = {
            "< 10m": rows[1]['< 10m'],
            "10 m <h< 18m": rows[1]['10 m <h< 18m'],
            "18 m < h < 25 m": rows[1]['18 m < h < 25 m']
        }
        st.session_state.data_storage_wind[key] = values
def more_information_wind():
    option_place = [
        "1 Binnenland",
        "2 Binnenland",
        "2 Küste und Inseln der Ostsee",
        "3 Binnenland",
        "3 Küste und Inseln der Ostsee",
        "4 Binnenland",
        "4 Küste der Nord- und Ostsee und Inseln der Ostsee",
        "4 Inseln der Nordsee"
    ]
    option_building_height = [
        "< 10m",
        "10 m <h< 18m",
        "18 m < h < 25 m"
    ]
    st.session_state.snow_and_wind.clear()
    st.session_state.selected_option_place = st.selectbox("Windzone und Standort", list(option_place), index=1)
    st.session_state.selected_option_building_height = st.selectbox("Gebäudehöhe", list(option_building_height), index=0)
    st.session_state.wind_load = st.session_state.data_storage_wind[st.session_state.selected_option_place][st.session_state.selected_option_building_height]*0.7
    st.session_state.wind_load = round(st.session_state.wind_load, 2)
    new_wind=[st.session_state.snow_load, st.session_state.wind_load]
    st.session_state.snow_and_wind.append(new_wind)
    st.write(f"Windlast = {st.session_state.wind_load}kn/m²")
    if np.isnan (st.session_state.snow_and_wind[0][1]):
        st.error("Bitte gib eine gültige Gebäudehöhe ein.")
        return
if "distributed_load_array" not in st.session_state:
    st.session_state.distributed_load_array = []
if "counter_distributed_load" not in st.session_state:
    st.session_state.counter_distributed_load = 0
# choice of  roof structure
if "selected_option" not in st.session_state:
    st.session_state.selected_option = 0
if "selected_option_value" not in st.session_state:
    st.session_state.selected_option_value=0
# load image
if "image_length_grid" not in st.session_state:
    image_length_grid = Image.open('dachaufbau/Spannweite_Lasteinzugsbreite.png')
def image_length_grid_place(length, grid):       
    # interaktive Beschriftung des Bilds
    draw = ImageDraw.Draw(image_length_grid)
    # Erste Beschriftung
    text_position1 = (325, 150)
    text_content1 = (f'{str(length)}m')
    text_color1 = (0, 0, 0)
    # Zweite Beschriftung
    text_position2 = (60, 325)
    text_content2 = (f'{str(grid)}m')
    text_color2 = (0, 0, 0)
    # Beschriftungen auf das Bild zeichnen
    font = ImageFont.truetype("OpenSans-Light.ttf", 30)
    draw.text(text_position1, text_content1, font=font, fill=text_color1)
    draw.text(text_position2, text_content2, font=font, fill=text_color2)
    st.image(image_length_grid)
if "image_dachaufbau" not in st.session_state:
    st.session_state.image_dachaufbau = 0
def dach_aufbau():
    # Dictionary mit den Werten für jede Dachaufbauoption
    extensive_dachbegrünung = st.session_state.layer_load_roof['extensive Dachbegrünung 10cm'] + st.session_state.layer_load_roof['zweilagige Dachabdichtung'] + st.session_state.layer_load_roof['Dämmstoff 20cm'] + st.session_state.layer_load_roof['Dampfsperre'] + st.session_state.layer_load_roof['Trapezblech']
    intensive_dachbegrünung = st.session_state.layer_load_roof['intensive Dachbegrünung 20cm'] + st.session_state.layer_load_roof['zweilagige Dachabdichtung'] + st.session_state.layer_load_roof['Dämmstoff 20cm'] + st.session_state.layer_load_roof['Dampfsperre'] + st.session_state.layer_load_roof['Trapezblech']
    leichter_dachaufbau = st.session_state.layer_load_roof['zweilagige Dachabdichtung'] + st.session_state.layer_load_roof['Dämmstoff 20cm'] + st.session_state.layer_load_roof['Dampfsperre'] + st.session_state.layer_load_roof['Trapezblech']
    schwerer_dachaufbau = st.session_state.layer_load_roof['Kies 5cm'] + st.session_state.layer_load_roof['zweilagige Dachabdichtung'] + st.session_state.layer_load_roof['Dämmstoff 20cm'] + st.session_state.layer_load_roof['Dampfsperre'] + st.session_state.layer_load_roof['BSH 4cm']
    extensive_dachbegrünung = round(extensive_dachbegrünung, 2)
    intensive_dachbegrünung = round(intensive_dachbegrünung, 2)
    leichter_dachaufbau = round(leichter_dachaufbau, 2)
    schwerer_dachaufbau = round(schwerer_dachaufbau, 2)
    option_values = {
        "kein Dachaufbau": 0.0,
        "extensive Dachbegrünung": extensive_dachbegrünung,
        "intensive Dachbegrünung": intensive_dachbegrünung,
        "leichter Dachaufbau": leichter_dachaufbau,
        "schwerer Dachaufbau": schwerer_dachaufbau
    }
    # Bilder Liste
    image_dachaufbau_list = {
        'extensive Dachbegrünung':'dachaufbau/Pikto_Dachaufbau_extensiv.png',
        'intensive Dachbegrünung':'dachaufbau/Pikto_Dachaufbau_intensiv.png',
        'leichter Dachaufbau':'dachaufbau/Pikto_Dachaufbau_leicht.png',
        'schwerer Dachaufbau':'dachaufbau/Pikto_Dachaufbau_schwer.png',
        'kein Dachaufbau':'dachaufbau/Pikto_kein_Dachaufbau.png'
    }
    # st.selectbox für die Auswahl des Dachaufbaus
    st.session_state.selected_option = st.selectbox("Dachaufbau", list(option_values.keys()))
    st.session_state.selected_option_value = option_values[st.session_state.selected_option]
    # Passendes Bild Laden
    st.session_state.image_dachaufbau_auswahl = image_dachaufbau_list[st.session_state.selected_option]
    st.session_state.image_dachaufbau = Image.open(st.session_state.image_dachaufbau_auswahl)
    # Zeigen Sie den ausgewählten Wert neben der Option an
    st.write(f"{st.session_state.selected_option} = {st.session_state.selected_option_value} kN/m²")
    roof_q=st.session_state.selected_option_value*grid
    roof_q=round(roof_q,2)
    st.write(f"{st.session_state.selected_option} = {roof_q} kN/m")
    # Wert des ausgewählten Dachaufbaus
    option_distributed_load = st.session_state.selected_option_value * grid
    option_distributed_load = round(option_distributed_load, 2)
    new_distributed_load = {"counter_distributed_load" : st.session_state.counter_distributed_load, "distributed_load" : option_distributed_load}
    st.session_state.distributed_load_array.append(new_distributed_load)
    st.session_state.counter_distributed_load += 1
    if option_distributed_load ==0 :
        st.session_state.distributed_load_array.pop()
        st.session_state.counter_distributed_load -=1
# adding distributed load
def distributed_load_information(distributed_load, counter_distributed_load):
    counter_distributed_load=st.session_state.counter_distributed_load
    if not distributed_load:
        st.error("Bitte gib eine gültige Zahl ein.")
        return
    distributed_load = float(distributed_load)
    # Erstellen eines Dictionaries zum Speichern von Streckenlasten
    new_distributed_load = {"counter_distributed_load": counter_distributed_load, "distributed_load": distributed_load}
    st.session_state.distributed_load_array.append(new_distributed_load)
    # Anzahl an Streckenlasten erhöhen
    st.session_state.counter_distributed_load += 1
if "forces_array" not in st.session_state:
    st.session_state.forces_array = []
if "counter_forces" not in st.session_state:
    st.session_state.counter_forces = 0
# get pointload
def point_load_properties(length, position, point_load, counter_forces):
    # Die Eingabe soll nicht möglich sein, wenn die Position die Länge überschreitet
    if length < position:
        print("Bitte gib eine gültige Position ein.")
        return
    # Speichern der Punktastdaten
    counter_forces = st.session_state.counter_forces
    new_force = {"counter_forces": counter_forces, "point_load": point_load, "position": position}
    st.session_state.forces_array.append(new_force)
    st.session_state.counter_forces += 1
# choice for the exact load input
def load_choice():
    counter = 1
    while True:
        # st.radio to chose between pointload and distributed load
        load_type = st.radio("Lasteingabe", ["Streckenlast", "Punktlast"], key=f"load_type_{counter}")
        if load_type == "Streckenlast":
            with st.container():
                    # st.text_input for a distributed load with a unique key
                    distributed_load_input = st.text_input("Streckenelast (kN/m)", key=f"distributed_load_{counter}")
                    distributed_load = float(distributed_load_input) if distributed_load_input else 0
                    distributed_load_information(distributed_load, st.session_state.counter_distributed_load)
        elif load_type == "Punktlast":
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    point_load_input = st.text_input("Punktlast (kN)", key=f"point_load_{counter}")
                with col2:
                    position_input = st.slider("Position (m)", min_value = 0.0, max_value = length, value = 0.0, step = 0.1, help="Die Position ist die Entfernung der Punktlast von Auflager A.", key=f"position_{counter}")
                    point_load = float(point_load_input) if point_load_input else 0
                    position = float(position_input) if position_input else 0
                    point_load_properties(length, position, point_load, st.session_state.counter_forces)
        # Erhöhen Sie den Zähler für den nächsten Satz von Widgets
        counter += 1
        # st.checkbox für die Entscheidung, ob weitere Eingaben gemacht werden sollen
        checkbox_label = "weitere Lasteingabe ({})".format(counter)
        # Eindeutiger Schlüssel für die Checkbox
        if not st.checkbox(checkbox_label, key=f"checkbox_{counter}"):
            break
if "support_forces" not in st.session_state:
    st.session_state.support_forces = [{"side":"left", "support_force":0},{"side":"right", "support_force":0}]
if "maximum_moment" not in st.session_state:
    st.session_state.maximum_moment = 0
if "maximum_moment_position_in_array" not in st.session_state:
    st.session_state.maximum_moment_position_in_array = 0
if "weight_calculation_option" not in st.session_state:
    st.session_state.weight_calculation_option = 0
if "side_and_position_max_momentum" not in st.session_state:
    st.session_state.side_and_position_max_momentum = []
if "max_v" not in st.session_state:
    st.session_state.max_v = 0
if "safe_maximum_moment" not in st.session_state:
    st.session_state.safe_maximum_moment = 0
if "position" not in st.session_state:
    st.session_state.position = 0
if "safety_factor" not in st.session_state:
    st.session_state.safety_factor = 1.4
if "maximum_moment_kragarm" not in st.session_state:
    st.session_state.maximum_moment_kragarm = 0
if "safe_maximum_moment_kragarm" not in st.session_state:
    st.session_state.safe_maximum_moment_kragarm = 0
# calculation of the support forces
def calculate_support_forces():
    # support forces
    resulting_forces = 0
    support_force_a_vertical = 0
    support_force_b_vertical = 0
    resulting_forces_all=0
    resulting_forces_left=0
    resulting_forces_right=0
    point_load_calculation = 0
    point_load_right = 0
    point_load_left = 0
    if length == position_b:
        for distributed in st.session_state.distributed_load_array:
            resulting_forces += distributed["distributed_load"] * length / 2
            support_force_a_vertical += distributed["distributed_load"] * length
        for point_load in st.session_state.forces_array:
            point_load_calculation += point_load["point_load"] * (point_load["position"] / length)
            support_force_a_vertical += point_load["point_load"]
        support_force_b_vertical = point_load_calculation + resulting_forces
        support_force_a_vertical -= support_force_b_vertical
        
    else:
        for distributed in st.session_state.distributed_load_array:
            resulting_forces_all += distributed["distributed_load"] * (length**2) / 2
            resulting_forces_left += distributed["distributed_load"] * (position_b**2) / 2
            resulting_forces_right += distributed["distributed_load"] * ((length - position_b)**2) / 2
        for point_load in st.session_state.forces_array:
            point_load_calculation += point_load["point_load"] * point_load["position"]
            if point_load["position"]<= position_b:
                point_load_left += point_load["point_load"] * (position_b-point_load["position"])
            else:
                point_load_right += point_load["point_load"] * (point_load["position"]-position_b)
        support_force_b_vertical = (point_load_calculation + resulting_forces_all)/position_b
        support_force_a_vertical = (resulting_forces_left+point_load_left-resulting_forces_right-point_load_right)/position_b
    support_force_a_vertical = round(support_force_a_vertical, 2)
    support_force_b_vertical = round(support_force_b_vertical, 2)
    # deleting support forces
    if st.session_state.support_forces != []:
        st.session_state.support_forces.pop()
        st.session_state.support_forces.pop()
    # saving support forces
    st.session_state.support_forces.append({"side": "left", "support_force": support_force_a_vertical})
    st.session_state.support_forces.append({"side": "right", "support_force": support_force_b_vertical})
    st.session_state.maximum_moment_position_in_array = 0
# calculation of the static system
def do_calculations_system():
    calculate_support_forces()
    # calculation of the maximum moment
    # only distributed load
    if len(st.session_state.distributed_load_array) != 0 and len(st.session_state.forces_array) == 0 and length==position_b:
        st.session_state.position = 0
        number_of_content_d= 0
        st.session_state.maximum_moment = 0
        st.session_state.weight_calculation_option = 1
        st.session_state.max_v = float(st.session_state.support_forces[0]['support_force'])
        while number_of_content_d < len(st.session_state.distributed_load_array):
            st.session_state.maximum_moment += st.session_state.distributed_load_array[number_of_content_d]['distributed_load'] * (length**2) / 8
            number_of_content_d += 1
        st.session_state.position = length/2
    # only pointload
    elif (len(st.session_state.distributed_load_array) == 0 or st.session_state.distributed_load_array[0]['distributed_load'] == 0) and len(st.session_state.forces_array) != 0 and length==position_b: 
        st.session_state.position = 0
        st.session_state.maximum_moment = 0
        st.session_state.weight_calculation_option = 2
        # assign a side to pointloads
        for obj in st.session_state.forces_array:
            if obj['position'] > length / 2:
                side = "right"
                obj['side'] = side
                obj['position'] = float(length) - float(obj['position'])
                obj['position'] = round(obj['position'],2)
            elif obj['position'] <= length / 2:
                side = "left"
                obj['side'] = side
        maximumSingleMoment = 0
        # Schleife durch jedes Element in st.session_state.forces_array
        for forcAr in st.session_state.forces_array:
            # Berechne das Produkt der aktuellen Objektwerte
            current_product = float(forcAr['point_load']) * float(forcAr['position'])
            # Vergleiche mit dem bisherigen maximalen Produkt
            if current_product > maximumSingleMoment:
                # Wenn das aktuelle Produkt größer ist, aktualisiere die Werte
                st.session_state.maximum_moment_position_in_array = forcAr['counter_forces']
                maximumSingleMoment = current_product
        # Herausfinden, welches Auflager zur Schnittberechnung geeignet ist
        # Anpassen, wenn Einfeldträger zu Mehrfeldträger wird
        if st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]['side'] == "left":
            support_number = 0
        else:
            support_number = 1
        st.session_state.max_v = float(st.session_state.support_forces[support_number]['support_force'])
        # Berechnung des maximalen Moments im Bauteil
        # Auflager der Seite miteinbeziehen
        st.session_state.maximum_moment += float(st.session_state.support_forces[support_number]['support_force']) * float(st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]["position"])
        indexCounter = 0
        # Überprüfen, ob das maximale Moment auf der rechten oder linken Hälfte ist und anschließende Berechnung
        while indexCounter < len(st.session_state.forces_array):
            if (st.session_state.forces_array[indexCounter]['side'] == st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]['side'] and st.session_state.forces_array[indexCounter]['position'] < st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]['position']):
                st.session_state.maximum_moment += -float(st.session_state.forces_array[indexCounter]['point_load']) * (float(st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]['position']) - float(st.session_state.forces_array[indexCounter]['position']))
                indexCounter += 1  # increase counter so every object will be checked
                st.write("ich werde ausgeführt")
            else:
                indexCounter += 1
        # position of the maximum moment
        if len(st.session_state.forces_array) == 1:
            st.session_state.position = st.session_state.forces_array[0]['position']
        else:
            st.session_state.position = st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]["position"]
        # giving the right side Pointload the right position
        for forces_side in st.session_state.forces_array:
            if forces_side["side"] == "right":
                forces_side['position'] = length - forces_side['position']
        # giving the position of the maximum moment the right location
        if st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]['side'] == "right":
            st.session_state.position = length-st.session_state.position
    # point and distributed load
    elif (len(st.session_state.distributed_load_array) != 1 or st.session_state.distributed_load_array[0]['distributed_load'] != 0) and len(st.session_state.forces_array) != 0 and length==position_b:
        st.session_state.weight_calculation_option = 3
        st.session_state.maximum_moment = 0
        for obj in st.session_state.forces_array:
            # assign a side to pointloads
            if obj['position'] > length / 2:
                side = "right"
                obj['side'] = side
                obj['position'] = length - obj['position']
            elif obj['position'] <= length / 2:
                side = "left"
                obj['side'] = side
        left_side_moment_point_load = 0
        right_side_moment_point_load = 0
        counter_forces_array = 0
        # Überprüfung, auf welcher Seite das Moment liegt.
        while counter_forces_array < len(st.session_state.forces_array):
            if st.session_state.forces_array[counter_forces_array]['side'] == "left":
                left_side_moment_point_load += st.session_state.forces_array[counter_forces_array]['point_load'] * st.session_state.forces_array[counter_forces_array]['position']
                counter_forces_array += 1
            elif st.session_state.forces_array[counter_forces_array]['side'] == "right":
                right_side_moment_point_load += st.session_state.forces_array[counter_forces_array]['point_load'] * st.session_state.forces_array[counter_forces_array]['position']
                counter_forces_array += 1
        st.session_state.position_max_momentum = 0
        index_counter_position = 0
        # Sortieren der Werte nach ihrer Position
        st.session_state.forces_array.sort(key=lambda x: x['position'])
        position_added_distributed_load = 0
        # Werte gehen sonst zu unendlich, da durch 0 geteilt wird!!!
        counter_distributed_load_division = 0
        while counter_distributed_load_division < len(st.session_state.distributed_load_array):
            position_added_distributed_load += float(st.session_state.distributed_load_array[counter_distributed_load_division]['distributed_load'])
            counter_distributed_load_division += 1
        st.session_state.position = 0
        position_between_point_loads = None
        if left_side_moment_point_load > right_side_moment_point_load:
            st.session_state.side_and_position_max_momentum.append(side := "left")
            # Streckenlasten addieren, damit zur weiteren Verwendung in der Positionsbestimmung
            st.session_state.position_max_momentum += st.session_state.support_forces[0]['support_force']
            last_added_position = 0
            # Last zur Bestimmung der Position, wenn das maximale Moment bei dem Umschlagpunkt von positiv zu negativ an der Position einer Einzellast
            while (index_counter_position <= len(st.session_state.forces_array)) and st.session_state.position_max_momentum > 0:
                # Die Längenüberprüfung wird ausgeführt, damit das Moment auch nach der letzten Punktlast liegen kann.
                if (st.session_state.forces_array[index_counter_position]['side'] == "left") or len(st.session_state.forces_array) >= index_counter_position+1:
                        if len(st.session_state.forces_array) >= index_counter_position:
                            st.session_state.position_max_momentum -= st.session_state.forces_array[index_counter_position]['point_load']
                        st.session_state.position_max_momentum -= position_added_distributed_load * (float(st.session_state.forces_array[index_counter_position]['position']) - last_added_position)
                        last_added_position = st.session_state.forces_array[index_counter_position]['position']
                        # Überprüfung, ob die folgenden Werte noch links sind
                        count_left = 0
                        for index_count_side in range(index_counter_position + 1, len(st.session_state.forces_array)):
                            if st.session_state.forces_array[index_count_side]['side'] == 'left':
                                count_left += 1
                        index_counter_position += 1
                        # Prüfen, ob der Nullpunkt zwischen zwei Punktlasten liegt.
                        st.session_state.position = last_added_position
                        position_between_point_loads = 0
                        position_between_point_loads = st.session_state.position_max_momentum / float(position_added_distributed_load)
                        if st.session_state.position_max_momentum < 0:
                            st.session_state.position = last_added_position
                            break
                        elif index_counter_position == len(st.session_state.forces_array) or (position_between_point_loads < float(st.session_state.forces_array[index_counter_position]['position'] - last_added_position)and st.session_state.forces_array[index_counter_position]['side'] == "left") or (count_left == 0):
                            st.session_state.position = last_added_position + position_between_point_loads
                            break
                else:
                        index_counter_position += 1
        else:
            st.session_state.side_and_position_max_momentum.append(side := "right")
            # Streckenlasten addieren, damit zur weiteren Verwendung in der Positionsbestimmung
            st.session_state.position_max_momentum += st.session_state.support_forces[1]['support_force']
            last_added_position = 0
            # Last zur Bestimmung der Position, wenn das maximale Moment bei dem Umschlagpunkt von positiv zu negativ an der Position einer Einzellast
            while (index_counter_position <= len(st.session_state.forces_array)) and st.session_state.position_max_momentum > 0:
                # Die Längenüberprüfung wird ausgeführt, damit das Moment auch nach der letzten Punktlast liegen kann.
                if (st.session_state.forces_array[index_counter_position]['side'] == "right") or len(st.session_state.forces_array) >= index_counter_position+1:
                        if len(st.session_state.forces_array) >= index_counter_position:
                            st.session_state.position_max_momentum -= st.session_state.forces_array[index_counter_position]['point_load']
                        st.session_state.position_max_momentum -= position_added_distributed_load * (float(st.session_state.forces_array[index_counter_position]['position']) - last_added_position)
                        last_added_position = st.session_state.forces_array[index_counter_position]['position']
                        # check if the values are on the right side
                        count_right = 0
                        for index_count_side in range(index_counter_position + 1, len(st.session_state.forces_array)):
                            if st.session_state.forces_array[index_count_side]['side'] == 'right':
                                count_right += 1
                        index_counter_position += 1
                        # check if Q(x)=0 is between two pointloads
                        st.session_state.position = last_added_position
                        position_between_point_loads = 0
                        position_between_point_loads = st.session_state.position_max_momentum / float(position_added_distributed_load)
                        if st.session_state.position_max_momentum < 0:
                            st.session_state.position = last_added_position
                            break
                        elif index_counter_position == len(st.session_state.forces_array) or (position_between_point_loads < float(st.session_state.forces_array[index_counter_position]['position'] - last_added_position)and st.session_state.forces_array[index_counter_position]['side'] == "right") or (count_right == 0):
                            st.session_state.position = last_added_position + position_between_point_loads
                            break
                else:
                        index_counter_position += 1
        # Sortieren der Werte nach ihrem Index
        st.session_state.forces_array.sort(key=lambda x: x['counter_forces'])
        st.session_state.position = round(st.session_state.position, 2) 
        st.session_state.side_and_position_max_momentum.append(st.session_state.position)
        support_number = None
        # Herausfinden, welches Auflager zur Schnittberechnung geeignet ist
        if st.session_state.support_forces[0]['side'] == st.session_state.side_and_position_max_momentum[0]:
            support_number = 0
        elif st.session_state.support_forces[1]['side'] == st.session_state.side_and_position_max_momentum[0]:
            support_number = 1
        st.session_state.max_v = float(st.session_state.support_forces[support_number]['support_force'])
        # Berechnung des maximalen Moments im Bauteil
        # Auflager der Seite miteinbeziehen.
        st.session_state.maximum_moment += float(st.session_state.support_forces[support_number]['support_force']) * float(st.session_state.side_and_position_max_momentum[1])
            # Aufagerkraft multipliziert mit dem Abstand X für die Position des Maximalen Moments
        index_counter = 0
        # Überprüfen, ob das maximale Moment auf der rechten oder linken Hälfte ist und anschließende Berechnung
        while index_counter < len(st.session_state.forces_array):
            if st.session_state.forces_array[index_counter]['side'] == st.session_state.side_and_position_max_momentum[0] and st.session_state.forces_array[index_counter]['position'] < float(st.session_state.side_and_position_max_momentum[1]):
                st.session_state.maximum_moment += -float(st.session_state.forces_array[index_counter]['point_load']) * (float(st.session_state.side_and_position_max_momentum[1]) - float(st.session_state.forces_array[index_counter]['position']))
                index_counter += 1 
            else:
                index_counter += 1
        number_of_content_d = 0
        # adding the distributed load
        while number_of_content_d < len(st.session_state.distributed_load_array):
            st.session_state.maximum_moment = float(st.session_state.maximum_moment) - (
                float(st.session_state.distributed_load_array[number_of_content_d]['distributed_load']) * (float(st.session_state.side_and_position_max_momentum[1]) ** 2) / 2)
            number_of_content_d += 1
        for side in st.session_state.forces_array:
            if side["side"] == "right":
                side["position"]=length -side["position"]
        if st.session_state.side_and_position_max_momentum[0] == 'right':
            st.session_state.position = length - st.session_state.position 
    elif length!=position_b:
        if st.session_state.support_forces[1]['support_force']<0:
            if st.session_state.support_forces[0]['support_force']>-st.session_state.support_forces[1]['support_force']:
                st.session_state.max_v = float(st.session_state.support_forces[0]['support_force'])
            else:
                st.session_state.max_v = -float(st.session_state.support_forces[1]['support_force'])
        else:
            if st.session_state.support_forces[0]['support_force']>st.session_state.support_forces[1]['support_force']:
                st.session_state.max_v = float(st.session_state.support_forces[0]['support_force'])
            else:
                st.session_state.max_v = float(st.session_state.support_forces[1]['support_force'])
        st.session_state.weight_calculation_option = 4
        st.session_state.maximum_moment = 0
        distributed_load_force = 0
        if len(st.session_state.distributed_load_array) != 0:
            for dist in st.session_state.distributed_load_array:
                    distributed_load_force += dist["distributed_load"]
        position_max_momentum = st.session_state.support_forces[0]["support_force"]
        # checking the position of the maximum moment
        # point load between A and B
        if (len(st.session_state.forces_array) != 0) and (len(st.session_state.distributed_load_array) == 0):
            st.session_state.forces_array.sort(key=lambda x: x['position'])
            index_counter_position=0
            while position_max_momentum > 0:
                if st.session_state.forces_array[index_counter_position]["position"] > position_b:
                    position_max_momentum = position_b
                    break
                position_max_momentum = position_max_momentum - st.session_state.forces_array[index_counter_position]["point_load"]
                if position_max_momentum < 0:
                    position_max_momentum = st.session_state.forces_array[index_counter_position]["position"]
                    break
                index_counter_position += 1
            if st.session_state.support_forces[0]["support_force"]<0:
                position_max_momentum = position_b
            st.session_state.forces_array.sort(key=lambda x: x['counter_forces'])
            st.session_state.position = position_max_momentum
        # point load behind B
        elif (len(st.session_state.forces_array) != 0) and (len(st.session_state.distributed_load_array) == 0) and st.session_state.forces_array[0]["position"] > position_b:
            position_max_momentum = position_b
            st.session_state.position = position_max_momentum
        # point and distributed load
        elif (len(st.session_state.forces_array) != 0) and (len(st.session_state.distributed_load_array) != 0):
            st.session_state.forces_array.sort(key=lambda x: x['position'])
            index_counter_position=0
            while position_max_momentum > 0:
                if index_counter_position==0:
                    current_position = position_max_momentum/distributed_load_force
                    if current_position < st.session_state.forces_array[index_counter_position]["position"]:
                        position_max_momentum = current_position
                        break
                    position_max_momentum -= distributed_load_force * st.session_state.forces_array[index_counter_position]["position"]
                if st.session_state.forces_array[index_counter_position]["position"] < position_b:
                    position_max_momentum -= st.session_state.forces_array[index_counter_position]["point_load"]
                    last_added_position = st.session_state.forces_array[index_counter_position]["position"]
                    index_counter_position += 1
                else:
                    position_max_momentum = position_b
                    break
                if position_max_momentum < 0:
                    position_max_momentum = last_added_position
                    break                
                position_between_point_loads = 0
                position_between_point_loads = position_max_momentum / distributed_load_force
                if index_counter_position != len(st.session_state.forces_array):
                    position_max_momentum -= distributed_load_force * st.session_state.forces_array[index_counter_position]["position"]
                if index_counter_position == len(st.session_state.forces_array) or position_between_point_loads < float(st.session_state.forces_array[index_counter_position]['position'] - last_added_position):
                    position_max_momentum = st.session_state.forces_array[index_counter_position-1]['position'] + position_between_point_loads
                    break
            position_max_momentum=round(position_max_momentum,2)
            st.session_state.position = position_max_momentum
            st.session_state.forces_array.sort(key=lambda x: x['counter_forces'])
        # only distributed load
        elif (len(st.session_state.forces_array) == 0) and (len(st.session_state.distributed_load_array) != 0):
            position_max_momentum = position_max_momentum/distributed_load_force

            st.session_state.position = position_max_momentum
        # maximum moment Feld
        maximum_moment_field = (st.session_state.support_forces[0]["support_force"] * st.session_state.position)
        if len(st.session_state.forces_array) !=0:
            index_countr_side=0
            st.session_state.forces_array.sort(key=lambda x: x['position'])
            while index_countr_side != len(st.session_state.forces_array):
                if st.session_state.forces_array[index_countr_side]["position"]<st.session_state.position:
                    maximum_moment_field = maximum_moment_field - st.session_state.forces_array[index_countr_side]["point_load"]*(st.session_state.position - st.session_state.forces_array[index_countr_side]["position"])
                    index_countr_side+=1
                else:
                    break
            st.session_state.forces_array.sort(key=lambda x: x['counter_forces'])
        if len(st.session_state.distributed_load_array):
            maximum_moment_field = maximum_moment_field-(distributed_load_force*st.session_state.position**2)/2
        st.session_state.maximum_moment = maximum_moment_field
        # Kragarm
        maximum_moment_kragarm = (st.session_state.support_forces[0]["support_force"] * position_b)
        if len(st.session_state.forces_array) !=0:
            index_countr_side=0
            st.session_state.forces_array.sort(key=lambda x: x['position'])
            while index_countr_side != len(st.session_state.forces_array):
                if st.session_state.forces_array[index_countr_side]["position"]<position_b:
                    maximum_moment_kragarm = maximum_moment_kragarm - st.session_state.forces_array[index_countr_side]["point_load"]*(position_b-st.session_state.forces_array[index_countr_side]["position"])
                    index_countr_side+=1
                else:
                    break
            st.session_state.forces_array.sort(key=lambda x: x['counter_forces'])
        if len(st.session_state.distributed_load_array):
            maximum_moment_kragarm = maximum_moment_kragarm - (distributed_load_force*position_b**2)/2
        st.session_state.maximum_moment_kragarm = maximum_moment_kragarm
    st.session_state.position = round(st.session_state.position, 2)
    st.session_state.maximum_moment = round(st.session_state.maximum_moment, 2)
    st.session_state.maximum_moment_kragarm = round(st.session_state.maximum_moment_kragarm, 2)
    st.session_state.safe_maximum_moment = 0
    st.session_state.safe_maximum_moment_kragarm = 0
    #Moment vor dem Einfluss des Sicherheitsbeiwerts sichern.
    if st.session_state.maximum_moment_kragarm != st.session_state.safe_maximum_moment_kragarm:
        st.session_state.safe_maximum_moment_kragarm = st.session_state.maximum_moment_kragarm
    if st.session_state.maximum_moment != st.session_state.safe_maximum_moment:
        st.session_state.safe_maximum_moment = float(st.session_state.maximum_moment)
    st.session_state.maximum_moment *= st.session_state.safety_factor
    st.session_state.maximum_moment = round(st.session_state.maximum_moment, 2)
    st.session_state.maximum_moment_kragarm *= st.session_state.safety_factor
    st.session_state.maximum_moment_kragarm = round(st.session_state.maximum_moment_kragarm, 2)
if "layer_load_roof" not in st.session_state:
    st.session_state.layer_load_roof={
        "Kies 5cm": 1,
        "extensive Dachbegrünung 10cm": 1,
        "intensive Dachbegrünung 20cm": 2.3,
        "zweilagige Dachabdichtung": 0.15,
        "Dampfsperre": 0.07,
        "BSH 4cm": 0.12,
        "Dämmstoff 20cm": 0.8,
        "Trapezblech": 0.125
    }
# beginning of the user interface
with st.container():
    col1, col2 = st.columns([1,3])
    with col1:
        st.image("logo/logo_mit_text.png",width=300)
    with col2:
        st.write("Dieses Programm wird zur analytischen Berechnung des statischen Systems eines Einfeldträgers genutzt. Im Anschluss kann die Dimensionierung eines Einfeldträgers anhand von Tabellenwerten vorgenommen werden. Darauf folgt ein Anzeigebereich, in der die unterschiedliche Profile miteinander verglichen werden können. Schließlich können die Ergebnisse als PDF ausgegeben und heruntergeladen werden.")
        st.write("Zur Dimensionierung genutzte Tabellen stammen aus dem Buch Tabellen zur Tragwerklehre 12. Auflage des Verlags Rudolf Müller von den Autoren Univ.-Prof. em. Dr.-Ing. Franz Krauss, Univ.-Prof. em. Dr.-Ing. Wilfried Führer und Prof. Dr.-Ing.Thomas Jürges. Die Schnee- und Windlasten sind standartmäßig für ein Gebäude in Aachen mit einer Gebäudehöhe von unter 10m eingestellt. Holzprofile werden mit den Werten für C24 Nadelholz nach DIN EN 338 berechnet. Stahlprofile werden mit den Werten für St 37 (S235) Baustahl berechnet.")
# static system
with st.container(border=True):
    col1, col3 = st.columns(2)
    with col1:
        # input for the static system
        st.header("Eingabe statische System")
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                length_input = st.slider("Spannweite (m)", min_value = 0.1, max_value = 30.0, value = 5.0, step = 0.1, help="Die Spannweite bestimmt die Länge des Trägers.")
                length = float(length_input)
                position_b_input = st.slider("Auflagerposition (m)", min_value = 0.1, max_value = length, value = length, step = 0.1, help="Die Anpassung dieser Länge wird zum erzeugen eines Kragarms verwendet.")
                position_b = float(position_b_input)
                grid_input = st.slider("Lasteinzugsbreite (m)", min_value = 0.1, max_value = 15.0, value = 3.0, step = 0.1, help="Die Lasteinzugsbreite wird benötigt um die Last des Dachaufbaus auf den Träger zu bestimmen.")
                grid = float(grid_input)
            with col2:
                image_length_grid_place(length, grid)
        with st.expander("Wind- und Schneelast"):
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    img_url_snow="https://www.die.de/dokumentation/holzbau-dach/technik/schnee.html"
                    img_snow="zonen_karten/schnee_last_zonen.png"
                    st.image(img_snow, caption="Schneelastzonen")
                    text = "Hier gelangst du zur Quelle des Bilds."
                    link_html = create_link(img_url_snow,text)
                    st.markdown(link_html, unsafe_allow_html=True)
                    more_information_snow()
                with col2:
                    img_url_wind="https://www.obo.de/produkte/schutzinstallation/produkthighlights/planungshilfen-vds-richtlinie-blitzschutzklassen-einteilung/ermitteln-der-windlast/"
                    img_wind="zonen_karten/deutschland_karte_windzonen.png"
                    st.image(img_wind, caption="Windlastzonen")
                    text = "Hier gelangst du zur Quelle des Bilds."
                    link_html = create_link(img_url_wind,text)
                    st.markdown(link_html, unsafe_allow_html=True)
                    more_information_wind()
            with st.container():
                st.session_state.counter_distributed_load = 0
                st.session_state.distributed_load_array.clear()
                checkbox_label = "Hinzufügen der Wind- und Schneelast"
                snow_wind_check=st.checkbox(checkbox_label, key="wind_snow")
                if snow_wind_check:
                    option_distributed_load = (st.session_state.snow_and_wind[0][0] + st.session_state.snow_and_wind[0][1]) * grid
                    option_distributed_load = round(option_distributed_load, 2)
                    new_distributed_load = {"counter_distributed_load" : st.session_state.counter_distributed_load, "distributed_load" : option_distributed_load}
                    st.session_state.distributed_load_array.append(new_distributed_load)
                    st.session_state.counter_distributed_load += 1
                    snow_wind = f"""
                                Schneelast = {st.session_state.snow_and_wind[0][0]}kN/m²
                                Windlast = {st.session_state.snow_and_wind[0][1]}kN/m²"""
        with st.expander("Dachaufbau"):
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    dach_aufbau()
                with col2:
                    st.image(st.session_state.image_dachaufbau)
        with st.expander("Schichten Dachaufbau"):
            # exact roof structure
            if "more_information_roof" not in st.session_state:
                                st.session_state.more_information_roof = {
                                    "kein Dachaufbau": 
                                    """ 
                                    
                                    """,
                                    "extensive Dachbegrünung": 
                                    f""" 
                                    1 extensive Dachbegrünung 10cm = {st.session_state.layer_load_roof['extensive Dachbegrünung 10cm']}kN/m²
                                    2 zweilagige Dachabdichtung = {st.session_state.layer_load_roof['zweilagige Dachabdichtung']}kN/m²
                                    3 Dämmstoff 20cm = {st.session_state.layer_load_roof['Dämmstoff 20cm']}kN/m²
                                    4 Dampfsperre = {st.session_state.layer_load_roof['Dampfsperre']}kN/m²
                                    5 Trapezblech = {st.session_state.layer_load_roof['Trapezblech']}kN/m²        
                                    """,
                                    "intensive Dachbegrünung": 
                                    f""" 
                                    1 intensive Dachbegrünung 20cm = {st.session_state.layer_load_roof['intensive Dachbegrünung 20cm']}kN/m²
                                    2 zweilagige Dachabdichtung = {st.session_state.layer_load_roof['zweilagige Dachabdichtung']}kN/m²
                                    3 Dämmstoff 20cm = {st.session_state.layer_load_roof['Dämmstoff 20cm']}kN/m²
                                    4 Dampfsperre = {st.session_state.layer_load_roof['Dampfsperre']}kN/m²
                                    5 Trapezblech = {st.session_state.layer_load_roof['Trapezblech']}kN/m²
                                    """,
                                    "leichter Dachaufbau": 
                                    f""" 
                                    1 zweilagige Dachabdichtung = {st.session_state.layer_load_roof['zweilagige Dachabdichtung']}kN/m²
                                    2 Dämmstoff 20cm = {st.session_state.layer_load_roof['Dämmstoff 20cm']}kN/m²
                                    3 Dampfsperre = {st.session_state.layer_load_roof['Dampfsperre']}kN/m²
                                    4 Trapezblech = {st.session_state.layer_load_roof['Trapezblech']}kN/m²
                                    """,
                                    "schwerer Dachaufbau": 
                                    f""" 
                                    1 Kies 5cm = {st.session_state.layer_load_roof['Kies 5cm']}kN/m²
                                    2 zweilagige Dachabdichtung = {st.session_state.layer_load_roof['zweilagige Dachabdichtung']}kN/m²
                                    3 Dämmstoff 20cm = {st.session_state.layer_load_roof['Dämmstoff 20cm']}kN/m²
                                    4 Dampfsperre = {st.session_state.layer_load_roof['Dampfsperre']}kN/m²
                                    5 BSH 4cm = {st.session_state.layer_load_roof['BSH 4cm']}kN/m²
                                    """,
                                }
            st.text(st.session_state.more_information_roof[st.session_state.selected_option])
        with st.expander("technische Aufbaulasten"):
            # additional_roof_structures
            counter = 1
            counter_aufbaulasten=f"{counter}a"
            if "additional_roof_structures" not in st.session_state:
                st.session_state.additional_roof_structures=[]
            st.session_state.additional_roof_structures.clear()
            def build_load(counter_aufbaulasten,counter):
                    while True:
                        # Dictionary mit den Werten für Zusätzliche Aufbaulasten
                        option_values = {
                            "Photovoltaik": 0.102,
                            "Solarthermie":0.167,
                        }
                        # st.selectbox für die Auswahl des Dachaufbaus
                        st.session_state.selected_option_extra = st.selectbox("Aufbaulasten", list(option_values.keys()), key=counter_aufbaulasten)
                        st.session_state.selected_option_extra_value = option_values[st.session_state.selected_option_extra]
                        # Zeigen Sie den ausgewählten Wert neben der Option an
                        st.write(f"{st.session_state.selected_option_extra} = {st.session_state.selected_option_extra_value} kN/m²")
                        # Wert des ausgewählten Dachaufbaus
                        st.session_state.additional_roof_structures.append(f"{st.session_state.selected_option_extra} = {st.session_state.selected_option_extra_value} kN/m²")
                        option_distributed_load = st.session_state.selected_option_extra_value * grid
                        option_distributed_load = round(option_distributed_load, 2)
                        new_distributed_load = {"counter_distributed_load" : st.session_state.counter_distributed_load, "distributed_load" : option_distributed_load}
                        st.session_state.distributed_load_array.append(new_distributed_load)
                        st.session_state.counter_distributed_load += 1
                        counter+=1
                        counter_aufbaulasten=f"{counter}a"
                        # unique key for the checkbox
                        if not st.checkbox("weitere Aufbaulasten", key=f"checkbox_{counter_aufbaulasten}"):
                            break
            if  st.checkbox("hinzufügen von Aufbaulasten"):
                build_load(counter_aufbaulasten,counter)
        with st.expander("individuelle Lasten"):
            st.session_state.forces_array.clear()
            st.session_state.counter_forces=0
            load_choice()
        st.session_state.side_and_position_max_momentum.clear()
        do_calculations_system()
    with col3:
        # results of the static system
        st.header("Ergebnisse statisches System")
        # drawing the static system
        def drawing_system():
            # systemline
            startpoint_a = 0
            endpoint_b = length
            middle_of_canvas_y = 5
            x_values_systemline = np.array([startpoint_a, endpoint_b])
            y_values_systemline = np.array([middle_of_canvas_y, middle_of_canvas_y])
            fig, ax = plt.subplots()
            ax.plot(x_values_systemline, y_values_systemline, marker=',', linestyle='-', color='black')
            ax.set_title('statisches System')
            # distances
            x_values_systemline = np.array([startpoint_a, startpoint_a, startpoint_a, position_b, position_b, position_b])
            y_values_systemline = np.array([middle_of_canvas_y-2.7,middle_of_canvas_y-3.3, middle_of_canvas_y-3, middle_of_canvas_y-3, middle_of_canvas_y-2.7,middle_of_canvas_y-3.3])
            ax.plot(x_values_systemline, y_values_systemline, marker=',', linestyle='-', color='black')
            plt.text(startpoint_a+((position_b-startpoint_a)/2), middle_of_canvas_y-3-0.5, f'{position_b}m', fontsize=8, color='black', ha='center', va='center')
            if length!=position_b:
                x_values_systemline = np.array([position_b, endpoint_b, endpoint_b, endpoint_b])
                y_values_systemline = np.array([middle_of_canvas_y-3, middle_of_canvas_y-3, middle_of_canvas_y-2.7,middle_of_canvas_y-3.3])
                ax.plot(x_values_systemline, y_values_systemline, marker=',', linestyle='-', color='black')
                text2=length-position_b
                text2=round(text2,2)
                st.write(text2)
                plt.text(startpoint_a+position_b+((length-position_b)/2), middle_of_canvas_y-3-0.5, f'{text2}m', fontsize=8, color='black', ha='center', va='center')
            # supports
            # fixed support
            x_values_fixed_support = np.array([startpoint_a, startpoint_a+0.5, startpoint_a-0.5, startpoint_a])
            y_values_fixed_support = np.array([middle_of_canvas_y, middle_of_canvas_y-1, middle_of_canvas_y-1, middle_of_canvas_y])
            ax.plot(x_values_fixed_support, y_values_fixed_support, marker=',', linestyle='-', color='black')
            plt.text(startpoint_a-1, middle_of_canvas_y-0.5, 'A', fontsize=8, color='black', ha='center', va='center')
            counter_slashes_fixed = 0
            while (counter_slashes_fixed<5):
                x_values_fixed_support_slash = np.array([startpoint_a-0.6+0.2*counter_slashes_fixed, startpoint_a-0.4+0.2*counter_slashes_fixed])
                y_values_fixed_support_slash = np.array([middle_of_canvas_y-1.3, middle_of_canvas_y-1])
                ax.plot(x_values_fixed_support_slash, y_values_fixed_support_slash, marker=',', linestyle='-', color='black')
                counter_slashes_fixed += 1
            # not fixed support
            position_b_drawing = position_b
            x_values_not_fixed_support = np.array([position_b_drawing, position_b_drawing+0.5, position_b_drawing-0.5, position_b_drawing])
            y_values_not_fixed_support = np.array([middle_of_canvas_y, middle_of_canvas_y-1, middle_of_canvas_y-1, middle_of_canvas_y])
            ax.plot(x_values_not_fixed_support, y_values_not_fixed_support, marker=',', linestyle='-', color='black')
            plt.text(position_b_drawing+1, middle_of_canvas_y-0.5, 'B', fontsize=8, color='black', ha='center', va='center')
            x_value_litle_line = np.array([position_b_drawing-0.7, position_b_drawing+0.7])
            y_value_litle_line = np.array([middle_of_canvas_y-1.2, middle_of_canvas_y-1.2])
            ax.plot(x_value_litle_line, y_value_litle_line, marker=',', linestyle='-', color='black')
            counter_slashes_fixed = 0
            while (counter_slashes_fixed<5):
                x_values_not_fixed_support_slash = np.array([position_b_drawing-0.6+0.2*counter_slashes_fixed, position_b_drawing-0.4+0.2*counter_slashes_fixed])
                y_values_not_fixed_support_slash = np.array([middle_of_canvas_y-1.5, middle_of_canvas_y-1.2])
                ax.plot(x_values_not_fixed_support_slash, y_values_not_fixed_support_slash, marker=',', linestyle='-', color='black')
                counter_slashes_fixed += 1
            # distributed load
            for arrow_field in st.session_state.distributed_load_array:
                if arrow_field["distributed_load"] != 0:
                    length_between_supports = endpoint_b-startpoint_a
                    x_value_distributed = np.array([startpoint_a, endpoint_b, endpoint_b, startpoint_a])
                    y_value_distributed = np.array([middle_of_canvas_y+0.4+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.4+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.7+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.7+0.6*arrow_field["counter_distributed_load"]])
                    ax.plot(x_value_distributed, y_value_distributed, marker=',', linestyle='-', color='black')
                    length_between_supports = length_between_supports/7
                    counter_arrows_dist = 0
                    while counter_arrows_dist<8:
                        force_location_x = startpoint_a + length_between_supports*counter_arrows_dist
                        x_value_tip = np.array([force_location_x-0.1,force_location_x,force_location_x+0.1])
                        y_value_tip = np.array([middle_of_canvas_y+0.5+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.4+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.5+0.6*arrow_field["counter_distributed_load"]])
                        ax.plot(x_value_tip, y_value_tip, marker=',', linestyle='-', color='black')
                        x_value_stick = np.array([force_location_x, force_location_x])
                        y_value_stick = np.array([middle_of_canvas_y+0.5+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.7+0.6*arrow_field["counter_distributed_load"]])
                        ax.plot(x_value_stick, y_value_stick , marker=',', linestyle='-', color='black')
                        counter_arrows_dist +=1
                    plt.text(endpoint_b+1, middle_of_canvas_y+0.6+0.6*arrow_field["counter_distributed_load"], f'q{arrow_field["counter_distributed_load"]+1} = {arrow_field["distributed_load"]}kN/m', fontsize=8, color='black', ha='left', va='center')       
            # pointload
            st.session_state.forces_array.sort(key=lambda x: x['position'])
            counter_image_arrow = 0
            for arrow in st.session_state.forces_array:
                    force_location_x = startpoint_a + ((endpoint_b-startpoint_a)/length)*arrow["position"]
                    x_value_tip = np.array([force_location_x-0.3,force_location_x,force_location_x+0.3])
                    y_value_tip = np.array([middle_of_canvas_y+0.8+0.6*len(st.session_state.distributed_load_array), middle_of_canvas_y+0.4+0.6*len(st.session_state.distributed_load_array), middle_of_canvas_y+0.8+0.6*len(st.session_state.distributed_load_array)])
                    ax.plot(x_value_tip, y_value_tip, marker=',', linestyle='-', color='black')
                    x_value_stick = np.array([force_location_x, force_location_x])
                    y_value_stick = np.array([middle_of_canvas_y+0.4+0.6*len(st.session_state.distributed_load_array), middle_of_canvas_y+4])
                    ax.plot(x_value_stick, y_value_stick , marker=',', linestyle='-', color='black')
                    if counter_image_arrow % 2 == 1:
                        plt.text(force_location_x, middle_of_canvas_y+5.1, f'F{arrow["counter_forces"]+1} = {arrow["point_load"]}kN', fontsize=12, color='black', ha='center', va='center')
                    else:
                        plt.text(force_location_x, middle_of_canvas_y+4.5, f'F{arrow["counter_forces"]+1} = {arrow["point_load"]}kN', fontsize=12, color='black', ha='center', va='center')
                    counter_image_arrow+=1
            st.session_state.forces_array.sort(key=lambda x: x['counter_forces'])
            plt.xlim(-2,length+2)
            plt.ylim(-2,12)
            plt.axis('off')
            st.pyplot(fig,use_container_width=True)
            plt.savefig("image_system.png", dpi=150, format='png')
        drawing_system()
        if len(st.session_state.distributed_load_array)!=0 or len(st.session_state.forces_array)!=0:
            with st.container():
                # display of the inner forces
                st.session_state.forces_array.sort(key=lambda x: x['position'])
                if position_b==length:
                    def add_condition_transverse_force(calculation, x_value):
                        counter_list=1
                        equation_list = []
                        equation_list.append(calculation)
                        condition_equation_list = []
                        condition_equation_list.append(x_value<st.session_state.forces_array[0]["position"])
                        # adding the pointLoads to the right spots
                        for forces_equation in st.session_state.forces_array:
                            # creating the new equations for the specific range of x
                            new_equation = calculation + forces_equation["point_load"]
                            calculation = new_equation
                            equation_list.append(new_equation)
                            # creating the specific range of x
                            if counter_list is not len(st.session_state.forces_array):
                                new_condition = (forces_equation["position"] <= x_value) & (x_value < st.session_state.forces_array[counter_list]["position"])
                                counter_list+=1
                            else:
                                new_condition = (forces_equation["position"] <= x_value)
                            condition_equation_list.append(new_condition)
                        # giving each range the right equation
                        result_equation = [np.where(condition_equation_list, equation_list, 0) for condition_equation_list, equation_list in zip(condition_equation_list, equation_list)]
                        final_equation_transverse = np.sum(result_equation, axis=0)
                        return final_equation_transverse
                    def add_condition_moment_curve(calculation, x_value):
                        counter_list=1
                        calculation += -(st.session_state.support_forces[0]['support_force']*(x_value))
                        equation_list = []
                        equation_list.append(calculation)
                        condition_equation_list = []
                        condition_equation_list.append(x_value <= st.session_state.forces_array[0]["position"])
                        # adding the pointLoads to the right spots
                        for forces_equation_m in st.session_state.forces_array:
                            # creating the new equations for the specific range of x
                            new_calculation = calculation + (forces_equation_m["point_load"]*(x_value-forces_equation_m["position"]))
                            calculation = new_calculation
                            equation_list.append(new_calculation)
                            # creating the specific range of x
                            if counter_list is not len(st.session_state.forces_array):
                                new_condition = (forces_equation_m["position"] <= x_value) & (x_value < st.session_state.forces_array[counter_list]["position"])
                                counter_list+=1
                            else:
                                new_condition = (forces_equation_m["position"] < x_value)
                            condition_equation_list.append(new_condition)
                        # giving each range the right equation
                        result_equation = [np.where(condition_equation_list, equation_list, 0) for condition_equation_list, equation_list in zip(condition_equation_list, equation_list)]
                        final_equation_transverse = np.sum(result_equation, axis=0)
                        return final_equation_transverse
                    def non_linear_function_transverse(x):
                                equation=-st.session_state.support_forces[0]['support_force']
                                if len(st.session_state.distributed_load_array) !=0:
                                    for dist_load in st.session_state.distributed_load_array:
                                        equation += (dist_load["distributed_load"]*x)
                                    final_equation_transverse = equation
                                if len(st.session_state.forces_array) != 0:
                                    final_equation_transverse = add_condition_transverse_force(equation, x)
                                return final_equation_transverse
                    def non_linear_function_moment(x):
                                final_equation=0
                                if len(st.session_state.distributed_load_array) !=0:
                                    for dist_load in st.session_state.distributed_load_array:
                                        final_equation -= (dist_load["distributed_load"]*(x)*(length-x))/2
                                    if len(st.session_state.forces_array) != 0: 
                                        final_equation = 0
                                        for dist_load in st.session_state.distributed_load_array:
                                            final_equation += (dist_load["distributed_load"]*(x)**2)/2
                                        final_equation = add_condition_moment_curve(final_equation, x)
                                if len(st.session_state.forces_array) != 0 and len(st.session_state.distributed_load_array) ==0: 
                                        final_equation = add_condition_moment_curve(final_equation, x)
                                return final_equation
                else:
                    def add_condition_transverse_force(calculation, x_value):
                        counter_list=1
                        equation_list = []
                        equation_list.append(calculation)
                        condition_equation_list = []
                        if st.session_state.forces_array[0]["position"]<position_b:
                            condition_equation_list.append(x_value<st.session_state.forces_array[0]["position"])
                        elif st.session_state.forces_array[0]["position"]>position_b: 
                            condition_equation_list.append(x_value<position_b)
                            new_equation = calculation - st.session_state.support_forces[1]['support_force']
                            calculation = new_equation
                        # adding the pointLoads to the right spots
                        for forces_equation in st.session_state.forces_array:
                            # creating the new equations for the specific range of x
                            new_equation = calculation + forces_equation["point_load"]
                            calculation = new_equation
                            # creating the specific range of x
                            if counter_list is not len(st.session_state.forces_array) and forces_equation["position"] < position_b:
                                equation_list.append(new_equation)
                                if st.session_state.forces_array[counter_list]["position"] > position_b:
                                    new_condition = (forces_equation["position"] <= x_value) & (x_value < position_b)
                                    condition_equation_list.append(new_condition)
                                    new_equation = calculation - st.session_state.support_forces[1]['support_force']
                                    calculation = new_equation
                                    new_condition = (position_b <= x_value) & (x_value < st.session_state.forces_array[counter_list]["position"])
                                    condition_equation_list.append(new_condition)
                                    equation_list.append(new_equation)
                                else:
                                    new_condition = (forces_equation["position"] <= x_value) & (x_value < st.session_state.forces_array[counter_list]["position"])
                                    condition_equation_list.append(new_condition)
                                counter_list+=1
                            elif counter_list is len(st.session_state.forces_array) and forces_equation["position"] < position_b:
                                equation_list.append(new_equation)
                                new_condition = (forces_equation["position"] <= x_value) & (x_value < position_b)
                                condition_equation_list.append(new_condition)
                                new_condition = position_b <= x_value
                                new_equation = calculation - st.session_state.support_forces[1]['support_force']
                                calculation = new_equation
                                equation_list.append(calculation)
                                condition_equation_list.append(new_condition)
                                counter_list+=1
                            elif counter_list is not len(st.session_state.forces_array) and forces_equation["position"] > position_b:
                                if counter_list is 1:
                                    new_equation = calculation - forces_equation["point_load"]
                                    calculation = new_equation
                                    equation_list.append(calculation)
                                    new_condition = (position_b <= x_value) & (x_value < forces_equation["position"])
                                    new_equation = calculation + forces_equation["point_load"]
                                    calculation = new_equation
                                    condition_equation_list.append(new_condition)
                                    equation_list.append(new_equation)
                                    new_condition = (forces_equation["position"] <= x_value) & (x_value < st.session_state.forces_array[counter_list]["position"])
                                    condition_equation_list.append(new_condition)
                                    counter_list+=1
                                else:
                                    equation_list.append(new_equation)
                                    new_condition = (forces_equation["position"] <= x_value) & (x_value < st.session_state.forces_array[counter_list]["position"])
                                    condition_equation_list.append(new_condition)
                                    counter_list+=1
                            elif counter_list is len(st.session_state.forces_array) and forces_equation["position"] > position_b:
                                if len(st.session_state.forces_array) is 1 and forces_equation["position"] > position_b:
                                    new_equation = calculation - forces_equation["point_load"]
                                    calculation = new_equation
                                    equation_list.append(calculation)
                                    new_condition = (position_b <= x_value) & (x_value < forces_equation["position"])
                                    condition_equation_list.append(new_condition)
                                    new_equation = calculation + forces_equation["point_load"]
                                    calculation = new_equation
                                    equation_list.append(calculation)
                                    new_condition = (forces_equation["position"] <= x_value)
                                    condition_equation_list.append(new_condition)
                                    counter_list+=1
                                else:
                                    calculation = new_equation
                                    equation_list.append(calculation)
                                    condition_equation_list.append(forces_equation["position"] <= x_value)
                                    counter_list+=1
                        # giving each range the right equation
                        result_equation = [np.where(condition_equation_list, equation_list, 0) for condition_equation_list, equation_list in zip(condition_equation_list, equation_list)]
                        final_equation_transverse = np.sum(result_equation, axis=0)
                        return final_equation_transverse
                    def add_condition_moment_curve(calculation, x_value):
                        counter_list=1
                        equation_list = []
                        equation_list.append(calculation)
                        condition_equation_list = []
                        if st.session_state.forces_array[0]["position"]<position_b:
                            condition_equation_list.append(x_value<st.session_state.forces_array[0]["position"])
                        elif st.session_state.forces_array[0]["position"]>position_b: 
                            condition_equation_list.append(x_value<position_b)
                            new_equation = calculation - st.session_state.support_forces[1]['support_force']*(x_value-position_b)
                            calculation = new_equation
                        # adding the pointLoads to the right spots
                        for forces_equation_m in st.session_state.forces_array:
                            # creating the new equations for the specific range of x
                            new_equation = calculation + forces_equation_m["point_load"]*(x_value-forces_equation_m["position"])
                            calculation = new_equation
                            # creating the specific range of x
                            if counter_list is not len(st.session_state.forces_array) and forces_equation_m["position"] < position_b:
                                if st.session_state.forces_array[counter_list]["position"] > position_b:
                                    equation_list.append(new_equation)
                                    new_condition = (forces_equation_m["position"] <= x_value) & (x_value < position_b)
                                    condition_equation_list.append(new_condition)
                                    new_equation = calculation - (st.session_state.support_forces[1]['support_force']*(x_value-position_b))
                                    calculation = new_equation
                                    new_condition = (position_b <= x_value) & (x_value < st.session_state.forces_array[counter_list]["position"])
                                    condition_equation_list.append(new_condition)
                                    equation_list.append(new_equation)
                                else:
                                    equation_list.append(new_equation)
                                    new_condition = (forces_equation_m["position"] <= x_value) & (x_value < st.session_state.forces_array[counter_list]["position"])
                                    condition_equation_list.append(new_condition)
                                counter_list+=1
                            elif counter_list is len(st.session_state.forces_array) and forces_equation_m["position"] < position_b:
                                equation_list.append(new_equation)
                                new_condition = (forces_equation_m["position"] <= x_value) & (x_value < position_b)
                                condition_equation_list.append(new_condition)
                                new_condition = position_b <= x_value
                                new_equation = calculation - (st.session_state.support_forces[1]['support_force']*(x_value-position_b))
                                calculation = new_equation
                                equation_list.append(calculation)
                                condition_equation_list.append(new_condition)
                                counter_list+=1
                            elif counter_list is not len(st.session_state.forces_array) and forces_equation_m["position"] > position_b:
                                if counter_list is 1:
                                    new_equation = calculation - forces_equation_m["point_load"]*(x_value-forces_equation_m["position"])
                                    calculation = new_equation
                                    equation_list.append(calculation)
                                    new_condition = (position_b <= x_value) & (x_value < forces_equation_m["position"])
                                    new_equation = calculation + forces_equation_m["point_load"]*(x_value-forces_equation_m["position"])
                                    calculation = new_equation
                                    condition_equation_list.append(new_condition)
                                    equation_list.append(new_equation)
                                    new_condition = (forces_equation_m["position"] <= x_value) & (x_value < st.session_state.forces_array[counter_list]["position"])
                                    condition_equation_list.append(new_condition)
                                    counter_list+=1
                                else:
                                    equation_list.append(new_equation)
                                    new_condition = (forces_equation_m["position"] <= x_value) & (x_value < st.session_state.forces_array[counter_list]["position"])
                                    condition_equation_list.append(new_condition)
                                    counter_list+=1
                            elif counter_list is len(st.session_state.forces_array) and forces_equation_m["position"] > position_b:
                                if len(st.session_state.forces_array) is 1 and forces_equation_m["position"] > position_b:
                                    new_equation = calculation - forces_equation_m["point_load"]*(x_value-forces_equation_m["position"])
                                    calculation = new_equation
                                    equation_list.append(calculation)
                                    new_condition = (position_b <= x_value) & (x_value < forces_equation_m["position"])
                                    condition_equation_list.append(new_condition)  
                                    new_equation = calculation + forces_equation_m["point_load"]*(x_value-forces_equation_m["position"])
                                    calculation = new_equation
                                    equation_list.append(calculation)
                                    condition_equation_list.append(forces_equation_m["position"] < x_value)
                                    counter_list+=1
                                else:
                                    calculation = new_equation
                                    equation_list.append(calculation)
                                    condition_equation_list.append(forces_equation_m["position"] < x_value)
                                    counter_list+=1
                        # giving each range the right equation
                        result_equation = [np.where(condition_equation_list, equation_list, 0) for condition_equation_list, equation_list in zip(condition_equation_list, equation_list)]
                        final_equation_transverse = np.sum(result_equation, axis=0)
                        return final_equation_transverse
                    def non_linear_function_transverse(x):
                                equation=-st.session_state.support_forces[0]['support_force']
                                if len(st.session_state.distributed_load_array) !=0:
                                    for dist_load in st.session_state.distributed_load_array:
                                        equation += (dist_load["distributed_load"]*x)
                                    final_equation_transverse = equation
                                if len(st.session_state.forces_array) != 0:
                                    final_equation_transverse = add_condition_transverse_force(equation, x)
                                #equations if there is no pointload
                                elif len(st.session_state.forces_array) == 0 and len(st.session_state.distributed_load_array) !=0:
                                    calculation = equation
                                    equation_list = []
                                    equation_list.append(calculation)
                                    condition_equation_list = []
                                    condition_equation_list.append(x<position_b)
                                    calculation = calculation - st.session_state.support_forces[1]['support_force']
                                    equation_list.append(calculation)
                                    condition_equation_list.append(position_b<=x)
                                    # giving each range the right equation
                                    result_equation = [np.where(condition_equation_list, equation_list, 0) for condition_equation_list, equation_list in zip(condition_equation_list, equation_list)]
                                    final_equation_transverse = np.sum(result_equation, axis=0)
                                return final_equation_transverse
                    def non_linear_function_moment(x):
                                final_equation=0
                                final_equation = -(st.session_state.support_forces[0]['support_force']*x)
                                if len(st.session_state.distributed_load_array) !=0:
                                    for dist_load in st.session_state.distributed_load_array:
                                        final_equation += (dist_load["distributed_load"]*(x)**2)/2
                                if len(st.session_state.forces_array) != 0: 
                                        final_equation = add_condition_moment_curve(final_equation, x)
                                elif len(st.session_state.forces_array) == 0 and len(st.session_state.distributed_load_array) !=0:
                                    calculation = final_equation
                                    equation_list = []
                                    equation_list.append(calculation)
                                    condition_equation_list = []
                                    condition_equation_list.append(x<position_b)
                                    new_equation = calculation - (st.session_state.support_forces[1]['support_force']*(x-position_b))
                                    calculation = new_equation
                                    equation_list.append(calculation)
                                    condition_equation_list.append(position_b<=x)
                                    # giving each range the right equation
                                    result_equation = [np.where(condition_equation_list, equation_list, 0) for condition_equation_list, equation_list in zip(condition_equation_list, equation_list)]
                                    final_equation = np.sum(result_equation, axis=0)
                                return final_equation
                col4, col5=st.columns(2)
                with col4:
                    def draw_transverse_force_curve():
                        # image matplotlib
                        # systemline
                        startpoint_a = 0
                        endpoint_b = length
                        middle_of_canvas_y = 0
                        x_values_systemline = np.array([startpoint_a, endpoint_b])
                        y_values_systemline = np.array([middle_of_canvas_y, middle_of_canvas_y])
                        # Matplotlib-Funktion zum Zeichnen der Linie
                        fig, ax = plt.subplots()
                        ax.plot(x_values_systemline, y_values_systemline, marker=',', linestyle='-', color='black')
                        # x-values
                        step_size=0.01
                        array_steps=np.arange(0,length+step_size,step_size)
                        x_data = np.array(array_steps)
                        # x-values small steps
                        x_smooth = np.linspace(x_data.min(), x_data.max(), 100)
                        # y-values
                        y_smooth = -(non_linear_function_transverse(x_smooth))
                        # create plot
                        ax.plot(x_smooth, y_smooth, label='Glatte nicht-lineare Kurve', color='cornflowerblue')
                        # closing the curve
                        length_y=(len(y_smooth))
                        x_values_closing_left = np.array([startpoint_a, startpoint_a])
                        y_values_closing_left = np.array([middle_of_canvas_y, y_smooth[0]])
                        ax.plot(x_values_closing_left, y_values_closing_left, marker=',', linestyle='-', color='cornflowerblue')
                        x_values_closing_right = np.array([endpoint_b, endpoint_b])
                        y_values_closing_right = np.array([middle_of_canvas_y, y_smooth[length_y-1]])
                        ax.plot(x_values_closing_right, y_values_closing_right, marker=',', linestyle='-', color='cornflowerblue')
                        ax.set_title('Querkraftverlauf')
                        # adjusting the visible range
                        if length==position_b:
                            if st.session_state.support_forces[0]['support_force']>st.session_state.support_forces[1]['support_force']:
                                yrange = st.session_state.support_forces[0]['support_force']*1.2
                            else:
                                yrange = st.session_state.support_forces[1]['support_force']*1.2
                        else:
                            if st.session_state.support_forces[0]['support_force']>st.session_state.support_forces[1]['support_force']:
                                yrange = st.session_state.support_forces[0]['support_force']*1.2
                            else:
                                yrange = st.session_state.support_forces[1]['support_force']*1.2
                        plt.xlim()
                        plt.ylim(yrange,-yrange)
                        plt.savefig("image_transverse.png", dpi=150, format='png')
                        # image plotly
                        fig = go.Figure()
                        fig.update_xaxes(range=[x_values_systemline.min(), x_values_systemline.max()])
                        fig.update_yaxes(range=[yrange, -yrange])
                        cornflower_blue="RGB(104, 150, 236)"
                        fig.add_trace(go.Scatter(x=x_values_systemline, y=y_values_systemline, mode='lines', name='Systemlinnie', line=dict(color="black"), showlegend=False))
                        fig.add_trace(go.Scatter(x=x_values_closing_left, y=y_values_closing_left, mode='lines', name='closing left', line=dict(color=cornflower_blue), showlegend=False))
                        fig.add_trace(go.Scatter(x=x_values_closing_right, y=y_values_closing_right, mode='lines', name='closing right', line=dict(color=cornflower_blue), showlegend=False))
                        fig.add_trace(go.Scatter(x=x_smooth, y=y_smooth, mode='lines', name='Querkraftverlauf', line=dict(color=cornflower_blue), showlegend=False))
                        fig.update_layout(title='Querkraftverlauf',
                                        xaxis_title='Position (m)',
                                        yaxis_title='Querkraft (kN)',
                                        plot_bgcolor='white')
                        st.plotly_chart(fig, use_container_width=True)
                    draw_transverse_force_curve()
                with col5:
                    def draw_moment_curve():
                        # systemline
                        startpoint_a = 0
                        endpoint_b = length
                        middle_of_canvas_y = 0
                        x_values_systemline = np.array([startpoint_a, endpoint_b])
                        y_values_systemline = np.array([middle_of_canvas_y, middle_of_canvas_y])
                        # Matplotlib-Funktion zum Zeichnen der Linie
                        fig, ax = plt.subplots()
                        ax.plot(x_values_systemline, y_values_systemline, marker=',', linestyle='-', color='black')                 
                        # Punkte der X-Werte
                        step_size=0.01
                        array_steps=np.arange(0,length+step_size,step_size)
                        x_data = np.array(array_steps)
                        # Feinere Abtastung der x-Werte
                        x_smooth = np.linspace(x_data.min(), x_data.max(), 100)
                        # Nicht-lineare y-Werte berechnen
                        y_smooth = -(non_linear_function_moment(x_smooth))
                        # create plot
                        ax.plot(x_smooth, y_smooth, label='Glatte nicht-lineare Kurve', color='cornflowerblue')
                        ax.set_title('Momentenverlauf')
                        # adjusting the visible range
                        if position_b==length:
                            yrange = st.session_state.safe_maximum_moment*1.5
                        if position_b!=length:
                            if st.session_state.safe_maximum_moment>(st.session_state.safe_maximum_moment_kragarm*-1):
                                yrange = st.session_state.safe_maximum_moment*1.5
                            else:
                                yrange=st.session_state.safe_maximum_moment_kragarm*-1.5
                        plt.xlim()
                        plt.ylim(yrange, -yrange)
                        plt.axis('on')
                        plt.savefig("image_moment.png", dpi=150, format='png')
                        # image plotly
                        fig = go.Figure()
                        fig.update_xaxes(range=[x_values_systemline.min(), x_values_systemline.max()])
                        fig.update_yaxes(range=[yrange, -yrange])
                        cornflower_blue="RGB(104, 150, 236)"
                        fig.add_trace(go.Scatter(x=x_values_systemline, y=y_values_systemline, mode='lines', name='Systemlinie', line=dict(color="black"), showlegend=False))
                        fig.add_trace(go.Scatter(x=x_smooth, y=y_smooth, mode='lines', name='Momentenverlauf', line=dict(color=cornflower_blue), showlegend=False))
                        fig.update_layout(title='Momentenverlauf',
                                        xaxis_title='Position (m)',
                                        yaxis_title='Moment (kNm)',
                                        plot_bgcolor='white')
                        st.plotly_chart(fig, use_container_width=True)                                    
                    draw_moment_curve()
        st.session_state.forces_array.sort(key=lambda x: x['counter_forces'])
        # results
        st.subheader("Auflagerreaktionen A und B")
        st.write(f"A = {st.session_state.support_forces[0]['support_force']} kN und B = {st.session_state.support_forces[1]['support_force']} kN")
        st.subheader("Maximales Moment")
        if length == position_b:
            st.write(f"Das maximale Feldmoment beträgt {st.session_state.safe_maximum_moment} kNm und liegt bei {st.session_state.position}m.")
        else:
            st.write(f"Das maximale Feldmoment beträgt {st.session_state.safe_maximum_moment} kNm und liegt bei {st.session_state.position}m.")
            st.write(f"Das Stützmoment beträgt {st.session_state.safe_maximum_moment_kragarm} kNm und liegt bei {position_b}m.")
if "wood_data" not in st.session_state:
    st.session_state.wood_data = pd.read_excel('tabellen/Tabelle_Kantholz.xlsx')
if "data_storage_wood" not in st.session_state:
    st.session_state.data_storage_wood = {}
    # create datastorage for kanthölzer
    for rows in st.session_state.wood_data.iterrows():
        key = f"{int(rows[1]['b'])}/{int(rows[1]['h'])}"
        values = {
            "b": rows[1]['b'],
            "h": rows[1]['h'],
            "availableArea": rows[1]['A'],
            "weightPerMeterInKG": rows[1]['G'],
            "availableITrägheitsmoment": int(rows[1]['I']),
            "available_w": rows[1]['W']
        }
        st.session_state.data_storage_wood[key] = values
        # sorting the values by the area
        st.session_state.data_storage_wood = dict(sorted(st.session_state.data_storage_wood.items(), key=lambda item: item[1]['availableArea']))
if "bsh_data" not in st.session_state:
    st.session_state.bsh_data = pd.read_excel('tabellen/Tabelle_bsh.xlsx')
if "data_storage_bsh" not in st.session_state:
    st.session_state.data_storage_bsh = {}
    # create datastorage for bsh
    for rows in st.session_state.bsh_data.iterrows():
        key = f"{int(rows[1]['h'])}"
        values = {
            "h": rows[1]['h'],
            "availableArea": rows[1]['A'],
            "availableITrägheitsmoment": int(rows[1]['I']),
            "available_w": rows[1]['W']
        }
        st.session_state.data_storage_bsh[key] = values
if "ipe_data" not in st.session_state:
    st.session_state.ipe_data = pd.read_excel('tabellen/Tabelle_IPE.xlsx')
if "data_storage_ipe" not in st.session_state:
    st.session_state.data_storage_ipe = {}
    # create datastorage for kanthölzer.
    for rows in st.session_state.ipe_data.iterrows():
        key = f"IPE {int(rows[1]['h']*10)}"
        values = {
            "b": rows[1]['b'],
            "h": rows[1]['h'],
            "availableArea": rows[1]['A'],
            "weightPerMeterInKG": rows[1]['G'],
            "availableITrägheitsmoment": int(rows[1]['I']),
            "available_w": rows[1]['W'],
            "available_area_steg":rows[1]['Asteg']
        }
        st.session_state.data_storage_ipe[key] = values
if "ipb_data" not in st.session_state:
    st.session_state.ipb_data = pd.read_excel('tabellen/Tabelle_IPB_HE_B.xlsx')
if "data_storage_ipb" not in st.session_state:
    st.session_state.data_storage_ipb = {}
    # create datastorage for kanthölzer.
    for rows in st.session_state.ipe_data.iterrows():
        key = f"IPB {int(rows[1]['h']*10)}"
        values = {
            "b": rows[1]['b'],
            "h": rows[1]['h'],
            "availableArea": rows[1]['A'],
            "weightPerMeterInKG": rows[1]['G'],
            "availableITrägheitsmoment": int(rows[1]['I']),
            "available_w": rows[1]['W'],
            "available_area_steg":rows[1]['Asteg']
        }
        st.session_state.data_storage_ipb[key] = values
if "tension_rd" not in st.session_state: 
    st.session_state.tension_rd = {
        "IPE": 21.8,
        "IPB": 21.8,
        "Kantholz": 1.5,
        "Brettschichtholz": 1.5
    }
if "needed_w" not in st.session_state: 
    st.session_state.needed_w = 0
if "number_k0" not in st.session_state:
    st.session_state.number_k0 = {
        "IPE": 15,
        "IPB": 15,
        "Kantholz": 312,
        "Brettschichtholz": 312
    }
if "schub_rd" not in st.session_state:
    st.session_state.schub_rd = {
        "IPE": 12.6,
        "IPB": 12.6,
        "Kantholz": 0.12,
        "Brettschichtholz": 0.12
    }
if "e_modul" not in st.session_state:
    st.session_state.e_modul = {
        "IPE": 21000,
        "IPB": 21000,
        "Kantholz": 1100,
        "Brettschichtholz": 1100
    }
if "maximum_moment_check" not in st.session_state:
    st.session_state.maximum_moment_check = 0
if "results_variant" not in st.session_state:
    st.session_state.results_variant = []
if "safe_maximum_moment_check" not in st.session_state:
    st.session_state.safe_maximum_moment_check = 0
if "needed_i_traegheitsmoment" not in st.session_state:
    st.session_state.needed_i_traegheitsmoment=0
if "needed_area" not in st.session_state:
    st.session_state.needed_area=0
if "counter_if_all_true" not in st.session_state:
    st.session_state.counter_if_all_true = 0
# checking the profil
def check_wood(counter_variant, cross_section_wood_input, material_choice, width):
    st.session_state.counter_if_all_true=0
    weight = 0
    if material_choice=="Brettschichtholz":
        weight = 5*(float(width)/100)*(float(st.session_state.data_storage_bsh[cross_section_wood_input]["h"])/100)
    else:
        weight = float(st.session_state.data_storage_wood[cross_section_wood_input]["weightPerMeterInKG"])
    safe_weight = 0
    safe_weight += weight*length
    safe_weight = round(safe_weight,2)
    # convert kg in kN
    weight = weight / 100
    if length== position_b:
        st.session_state.safe_maximum_moment_check = st.session_state.safe_maximum_moment
        st.session_state.maximum_moment_check = st.session_state.maximum_moment
    elif length!= position_b:
        if -st.session_state.maximum_moment_kragarm<st.session_state.maximum_moment:
            st.session_state.safe_maximum_moment_check = st.session_state.safe_maximum_moment
            st.session_state.maximum_moment_check = st.session_state.maximum_moment
        else:
            st.session_state.safe_maximum_moment_check = -st.session_state.safe_maximum_moment_kragarm
            st.session_state.maximum_moment_check = -st.session_state.maximum_moment_kragarm
    # for each constelation of loads a different weightcalculation
    if st.session_state.weight_calculation_option == 1:
        st.session_state.maximum_moment_check += (weight*length**2)/8
        st.session_state.safe_maximum_moment_check += (weight*length**2)/8
    elif st.session_state.weight_calculation_option == 2:
        st.session_state.maximum_moment_check += weight * (st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]["position"] **2)/ 2
        st.session_state.safe_maximum_moment_check += weight * (st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]["position"] **2)/ 2
    elif st.session_state.weight_calculation_option == 3:
        st.session_state.maximum_moment_check += weight * (st.session_state.side_and_position_max_momentum[1])**2 / 2
        st.session_state.safe_maximum_moment_check += weight * (st.session_state.side_and_position_max_momentum[1])**2 / 2
    if st.session_state.maximum_moment_kragarm<st.session_state.maximum_moment and st.session_state.weight_calculation_option == 4:
        st.session_state.maximum_moment_check += weight * (st.session_state.position)**2 / 2
        st.session_state.safe_maximum_moment_check += weight * (st.session_state.position)**2 / 2
    elif st.session_state.maximum_moment_kragarm>st.session_state.maximum_moment and st.session_state.weight_calculation_option == 4:   
        st.session_state.maximum_moment_check += weight * (position_b)**2 / 2
        st.session_state.safe_maximum_moment_check += weight * (position_b)**2 / 2
    # Bei den Momentenbestimmungen auch die Position bestimmen
    st.session_state.maximum_moment_check = round(st.session_state.maximum_moment_check, 2)
    st.session_state.safe_maximum_moment_check = round(st.session_state.safe_maximum_moment_check, 2)
    st.session_state.needed_w = (st.session_state.maximum_moment_check * 100) / st.session_state.tension_rd[material_choice]
    if is_even(counter_variant)==0:
        results_variant_title = f'''Variante {counter_variant}'''
    else:
        results_variant_title = f'''alternative zu Variante {counter_variant-1}'''
    # Zugriff auf Datenbank und Suche nach passendem W.
    st.session_state.needed_i_traegheitsmoment=0
    st.session_state.needed_area=0
    st.session_state.needed_w = round(st.session_state.needed_w, 2)
    neededw=st.session_state.needed_w
    if material_choice=="Brettschichtholz":
        availablew=st.session_state.data_storage_bsh[cross_section_wood_input]["available_w"]*float(width)
    else:
        availablew=st.session_state.data_storage_wood[cross_section_wood_input]["available_w"]
    # degree of utilization
    degree_of_utilization_w = round(st.session_state.needed_w / availablew *100, 2)
    if st.session_state.needed_w > availablew:
        results_variant = f'''
        Neuen Querschnitt wählen aufgrund des Tragfähigkeitsnachweises ✖ 
        erf W > vorh W
        {st.session_state.needed_w}cm³ > {availablew}cm³
        η = {degree_of_utilization_w}%
        '''
        result_w=f"${neededw}cm^3 > {availablew}cm^3$"
    else:
        results_variant = f'''
        Tragfähigkeitsprüfung erfüllt ✔
        erf W < vorh W
        {st.session_state.needed_w}cm³ < {availablew}cm³
        η = {degree_of_utilization_w}%
        '''
        st.session_state.counter_if_all_true += 1
        result_w=f"${neededw}cm^3 < {availablew}cm^3$"
    # Gebrauchstauglichkeitsnachweis
    st.session_state.needed_i_traegheitsmoment = st.session_state.number_k0[material_choice] * (st.session_state.safe_maximum_moment_check/100) * (length * 100)
    st.session_state.needed_i_traegheitsmoment = round(st.session_state.needed_i_traegheitsmoment, 2)
    neededi=st.session_state.needed_i_traegheitsmoment
    if material_choice=="Brettschichtholz":
        availablei=st.session_state.data_storage_bsh[cross_section_wood_input]["availableITrägheitsmoment"]*float(width)
    else:
        availablei=st.session_state.data_storage_wood[cross_section_wood_input]['availableITrägheitsmoment']
    # degree of utilization
    degree_of_utilization_i = round(st.session_state.needed_i_traegheitsmoment / availablei *100, 2)
    deflection = (5*(st.session_state.safe_maximum_moment_check*100)*((length*100)**2))/(48*st.session_state.e_modul[material_choice]*availablei)
    available_deflection = (length*100.0)/300.0
    deflection = round(deflection,2)
    available_deflection = round(available_deflection,2)
    if st.session_state.needed_i_traegheitsmoment <= availablei:
        results_variant += f'''
        Durchbiegungsnachweis erfüllt ✔
        erf I < vorh I
        {st.session_state.needed_i_traegheitsmoment}cm^4 < {availablei}cm^4
        erf Durchbiegung < l/300
        {deflection}cm < {available_deflection}cm
        η = {degree_of_utilization_i}%
        '''
        st.session_state.counter_if_all_true += 1
        result_i=f"${neededi}cm^4 < {availablei}cm^4$"
    else:
        results_variant += f'''
        Neuen Querschnitt wählen aufgrund des Gebrauchstauglichkeitsnachweises ✖
        erf I > vorh I
        {st.session_state.needed_i_traegheitsmoment}cm^4 > {availablei}cm^4
        erf Durchbiegung > l/300
        {deflection}cm > {available_deflection}cm
        η = {degree_of_utilization_i}%
        '''
        result_i=f"${neededi}cm^4 > {availablei}cm^4$"     
    # proof of thrust with safety factor of 1.4
    st.session_state.needed_area = ((3 * st.session_state.max_v)* 1.4) / (2 * st.session_state.schub_rd[material_choice])
    st.session_state.needed_area = round(st.session_state.needed_area, 2)
    neededa=st.session_state.needed_area
    if material_choice=="Brettschichtholz":
        availablea=st.session_state.data_storage_bsh[cross_section_wood_input]["availableArea"]*float(width)
    else:
        availablea=st.session_state.data_storage_wood[cross_section_wood_input]['availableArea']
    # degree of utilization
    degree_of_utilization_a = round(st.session_state.needed_area / availablea *100, 2)
    if st.session_state.needed_area <= availablea:
        results_variant += f'''
        Schubnachweis erfüllt ✔
        erf A < vorh A
        {st.session_state.needed_area}cm² < {availablea}cm²
        η = {degree_of_utilization_a}%
        '''
        st.session_state.counter_if_all_true += 1
        result_a=f"${neededa}cm^2 < {availablea}cm^2$"
    else:
        results_variant += f'''
        Neuen Querschnitt wählen aufgrund des Schubnachweises ✖
        erf A > vorh A
        {st.session_state.needed_area}cm² > {availablea}cm²
        η = {degree_of_utilization_a}%
        '''
        result_a=f"${neededa}cm^2 > {availablea}cm^2$"  
    # saving the results  
    if material_choice is not "Brettschichtholz":
        width=st.session_state.data_storage_wood[cross_section_wood_input]["b"]
        height=st.session_state.data_storage_wood[cross_section_wood_input]["h"]
    else:
        height=st.session_state.data_storage_bsh[cross_section_wood_input]["h"]
    counter_result=st.session_state.counter_if_all_true
    w_compare_wood=r"$erf W \leq vorh W$"
    w_how_wood=r"$erf W = \frac{max M_{d}}{\sigma_{Rd}}$"
    i_compare_wood=r"$erf I \leq vorh I$"
    i_how_wood=r"$erf I = k_{0} \cdot max M \cdot l$"
    a_compare_wood=r"$erf A \leq vorh A$"
    a_how_wood=r"$erf A = \frac{3 \cdot maxV_{d}}{2 \cdot \tau_{Rd}}$"
    result_variant_array = {"title": results_variant_title, "properties": f"Ausgewähltes Profil: {material_choice} {cross_section_wood_input}", "text": results_variant, "profil": material_choice ,"profil_text": f"{material_choice} {cross_section_wood_input}","max_moment": st.session_state.maximum_moment_check, "weight": safe_weight, "height": height, "width":width, "erf_a": st.session_state.needed_area, "erf_w": st.session_state.needed_w, "erf_i": st.session_state.needed_i_traegheitsmoment, "image": st.session_state.image_profil_safe, "w_compare": w_compare_wood, "w_how":w_how_wood, "i_compare": i_compare_wood, "i_how":i_how_wood, "a_compare": a_compare_wood, "a_how":a_how_wood, "result_w":result_w, "result_i":result_i, "result_a":result_a, "check_result":counter_result}
    return result_variant_array
# checking the profil and giving an alternativ solution
def check_profil_wood(counter_variant, cross_section_wood_input, material_choice, width):
    # result of the input
    st.session_state.results_variant.insert(counter_variant-1, check_wood(counter_variant, cross_section_wood_input, material_choice, width))
    # better result
    counter_variant += 1
    st.session_state.counter_if_all_true=0
    while st.session_state.counter_if_all_true < 3:
        if material_choice == "Kantholz":
            for try_profil in st.session_state.data_storage_wood:
                current_variant = 0
                current_variant = check_wood(counter_variant, try_profil, material_choice, width)
                if try_profil == "20/30" and st.session_state.counter_if_all_true != 3:
                    return st.write("Es gibt keine passende Variante als Kantholz!")
                if st.session_state.counter_if_all_true == 3:
                    break
        elif material_choice == "Brettschichtholz":
            for try_profil in st.session_state.data_storage_bsh:
                current_variant = 0
                current_variant = check_wood(counter_variant, try_profil, material_choice, width)
                if try_profil == "270"and st.session_state.counter_if_all_true != 3:
                    return st.write("Es gibt keine passende Variante als Brettschichtholz!")
                if st.session_state.counter_if_all_true == 3:
                    break
    st.session_state.results_variant.insert(counter_variant-1, current_variant)
if "image_profil_list" not in st.session_state:
    st.session_state.image_profil_list = {
        'Kantholz':'material_profil/Pikto_Kantholz.png',
        'Brettschichtholz':'material_profil/Pikto_bsh.png',
        'IPE':'material_profil/Pikto_IPE.png',
        'IPB':'material_profil/Pikto_IPE.png'
    }
if "image_profil_safe" not in st.session_state:
    st.session_state.image_profil_safe = 0
# checking the profil
def check_ipe(counter_variant, cross_section_input, material_choice, data_storage):
    st.session_state.counter_if_all_true=0
    weight = 0
    weight = float(data_storage[cross_section_input]["weightPerMeterInKG"])
    safe_weight = 0
    safe_weight += weight*length
    safe_weight = round(safe_weight,2)
    # convert kg in kN
    weight = weight / 100
    if length== position_b:
        st.session_state.safe_maximum_moment_check = st.session_state.safe_maximum_moment
        st.session_state.maximum_moment_check = st.session_state.maximum_moment
    elif length!= position_b:
        if -st.session_state.maximum_moment_kragarm<st.session_state.maximum_moment:
            st.session_state.safe_maximum_moment_check = st.session_state.safe_maximum_moment
            st.session_state.maximum_moment_check = st.session_state.maximum_moment
        else:
            st.session_state.safe_maximum_moment_check = -st.session_state.safe_maximum_moment_kragarm
            st.session_state.maximum_moment_check = -st.session_state.maximum_moment_kragarm
    # for each constelation of loads a different weightcalculation
    if st.session_state.weight_calculation_option == 1:
        st.session_state.maximum_moment_check += (weight*length**2)/8
        st.session_state.safe_maximum_moment_check += (weight*length**2)/8
    elif st.session_state.weight_calculation_option == 2:
        st.session_state.maximum_moment_check += weight * (st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]["position"] **2)/ 2
        st.session_state.safe_maximum_moment_check += weight * (st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]["position"] **2)/ 2
    elif st.session_state.weight_calculation_option == 3:
        st.session_state.maximum_moment_check += weight * (st.session_state.side_and_position_max_momentum[1])**2 / 2
        st.session_state.safe_maximum_moment_check += weight * (st.session_state.side_and_position_max_momentum[1])**2 / 2
    if st.session_state.maximum_moment_kragarm<st.session_state.maximum_moment and st.session_state.weight_calculation_option == 4:
        st.session_state.maximum_moment_check += weight * (st.session_state.position)**2 / 2
        st.session_state.safe_maximum_moment_check += weight * (st.session_state.position)**2 / 2
    elif st.session_state.maximum_moment_kragarm>st.session_state.maximum_moment and st.session_state.weight_calculation_option == 4:   
        st.session_state.maximum_moment_check += weight * (position_b)**2 / 2
        st.session_state.safe_maximum_moment_check += weight * (position_b)**2 / 2
    st.session_state.maximum_moment_check = round(st.session_state.maximum_moment_check, 2)
    st.session_state.safe_maximum_moment_check = round(st.session_state.safe_maximum_moment_check, 2)
    st.session_state.needed_w = (st.session_state.maximum_moment_check * 100) / st.session_state.tension_rd[material_choice]
    if is_even(counter_variant)==0:
        results_variant_title = f'''Variante {counter_variant}'''
    else:
        results_variant_title = f'''alternative zu Variante {counter_variant-1}'''
    # acces the data storage to get the right W
    st.session_state.needed_i_traegheitsmoment=0
    st.session_state.needed_area=0
    st.session_state.needed_w = round(st.session_state.needed_w, 2)
    neededw=st.session_state.needed_w
    availablew=data_storage[cross_section_input]["available_w"]
    # degree of utilization
    degree_of_utilization_w = round(st.session_state.needed_w / data_storage[cross_section_input]['available_w']*100, 2)
    if st.session_state.needed_w > data_storage[cross_section_input]["available_w"]:
        results_variant = f'''
        Neuen Querschnitt wählen aufgrund des Tragfähigkeitsnachweises ✖
        erf W > vorh W
        {st.session_state.needed_w}cm³ > {data_storage[cross_section_input]['available_w']}cm³
        η = {degree_of_utilization_w}%
        '''
        result_w=f"${neededw}cm^3 > {availablew}cm^3$"
    else:
        results_variant = f'''
        Tragfähigkeitsnachweis erfüllt ✔
        erf W < vorh W
        {st.session_state.needed_w}cm³ < {data_storage[cross_section_input]['available_w']}cm³
        η = {degree_of_utilization_w}%
        '''
        st.session_state.counter_if_all_true += 1
        result_w=f"${neededw}cm^3 < {availablew}cm^3$"
    # Gebrauchstauglichkeitsnachweis
    st.session_state.needed_i_traegheitsmoment = st.session_state.number_k0[material_choice] * (st.session_state.safe_maximum_moment_check/100) * (length * 100)
    st.session_state.needed_i_traegheitsmoment = round(st.session_state.needed_i_traegheitsmoment, 2)
    neededi=st.session_state.needed_i_traegheitsmoment
    availablei=data_storage[cross_section_input]["availableITrägheitsmoment"]
    # degree of utilization
    degree_of_utilization_i = round(st.session_state.needed_i_traegheitsmoment / data_storage[cross_section_input]['availableITrägheitsmoment'] *100, 2)
    deflection = (5*(st.session_state.safe_maximum_moment_check*100)*((length*100)**2))/(48*st.session_state.e_modul[material_choice]*data_storage[cross_section_input]['availableITrägheitsmoment'])
    available_deflection = (length*100)/300
    deflection = round(deflection,2)
    available_deflection = round(available_deflection,2)
    if st.session_state.needed_i_traegheitsmoment <= data_storage[cross_section_input]["availableITrägheitsmoment"]:
        results_variant += f'''
        Durchbiegungsnachweis erfüllt ✔
        erf I < vorh I
        {st.session_state.needed_i_traegheitsmoment}cm^4 < {data_storage[cross_section_input]['availableITrägheitsmoment']}cm^4
        erf Durchbiegung < l/300
        {deflection}cm < {available_deflection}cm
        η = {degree_of_utilization_i}%
        '''
        st.session_state.counter_if_all_true += 1
        result_i=f"${neededi}cm^4 < {availablei}cm^4$"
    else:
        results_variant += f'''
        Neuen Querschnitt wählen aufgrund des Gebrauchstauglichkeitsnachweises ✖
        erf I > vorh I
        {st.session_state.needed_i_traegheitsmoment}cm^4 > {data_storage[cross_section_input]['availableITrägheitsmoment']}cm^4
        erf Durchbiegung > l/300
        {deflection}cm > {available_deflection}cm
        η = {degree_of_utilization_i}%
        '''
        result_i=f"${neededi}cm^4 > {availablei}cm^4$"
    # Schubnachweis mit Sicherheitsbeiwert von 1.4
    st.session_state.needed_area = (st.session_state.max_v * 1.4) / st.session_state.schub_rd[material_choice]
    st.session_state.needed_area = round(st.session_state.needed_area, 2)
    neededa=st.session_state.needed_area
    availablea=data_storage[cross_section_input]["available_area_steg"]
    # degree of utilization
    degree_of_utilization_a = round(st.session_state.needed_area / data_storage[cross_section_input]['availableArea'] *100, 2)
    if st.session_state.needed_area <= data_storage[cross_section_input]["available_area_steg"]:
        results_variant += f'''
        Schubnachweis erfüllt ✔
        erf Asteg < vorh Asteg
        {st.session_state.needed_area}cm² < {data_storage[cross_section_input]['available_area_steg']}cm²
        η = {degree_of_utilization_a}%
        '''
        st.session_state.counter_if_all_true += 1
        result_a=f"${neededa}cm^2 < {availablea}cm^2$"
    else:
        results_variant += f'''
        Neuen Querschnitt wählen aufgrund des Schubnachweises ✖
        erf Asteg > vorh Asteg
        {st.session_state.needed_area}cm² > {data_storage[cross_section_input]['available_area_steg']}cm²
        η = {degree_of_utilization_a}%
        '''
        result_a=f"${neededa}cm^2 > {availablea}cm^2$"
    # saving the results
    counter_result=st.session_state.counter_if_all_true
    w_compare_wood=r"$erf W \leq vorh W$"
    w_how_wood=r"$erf W = \frac{max M_{d}}{\sigma_{Rd}}$"
    i_compare_wood=r"$erf I \leq vorh I$"
    i_how_wood=r"$erf I = k_{0} \cdot max M \cdot l$"
    a_compare_wood=r"$erf A_{Steg} \leq vorh A_{Steg}$"
    a_how_wood=r"$erf A_{Steg} = \frac{maxV_{d}}{\tau_{Rd}}$"
    result_variant_array = {"title": results_variant_title,"properties": f"Ausgewähltes Profil: {cross_section_input}", "text": results_variant, "profil": material_choice ,"profil_text":cross_section_input,"max_moment": st.session_state.maximum_moment_check, "weight": safe_weight, "height": data_storage[cross_section_input]["h"], "width":data_storage[cross_section_input]["b"], "erf_a": st.session_state.needed_area, "erf_w": st.session_state.needed_w, "erf_i": st.session_state.needed_i_traegheitsmoment, "image": st.session_state.image_profil_safe, "w_compare": w_compare_wood, "w_how":w_how_wood, "i_compare": i_compare_wood, "i_how":i_how_wood, "a_compare": a_compare_wood, "a_how":a_how_wood, "result_w":result_w, "result_i":result_i, "result_a":result_a, "check_result":counter_result}
    return result_variant_array
# checking the profil and giving an alternativ solution
def check_profil_ipe(counter_variant, cross_section_input, material_choice, data_storage):
    # result of the input
    st.session_state.results_variant.insert(counter_variant-1, check_ipe(counter_variant, cross_section_input, material_choice, data_storage))
    # better result
    counter_variant += 1
    st.session_state.counter_if_all_true=0
    while st.session_state.counter_if_all_true < 3:
        for try_profil in data_storage:
            current_variant = 0
            current_variant = check_ipe(counter_variant, try_profil, material_choice, data_storage)
            if try_profil == "IPE 600" and st.session_state.counter_if_all_true != 3:
                return st.write("Es gibt keine passende Variante als IPE!")
            if try_profil == "IPB 1000" and st.session_state.counter_if_all_true != 3:
                return st.write("Es gibt keine passende Variante als IPB!")
            if st.session_state.counter_if_all_true == 3:
                break
    st.session_state.results_variant.insert(counter_variant-1, current_variant)
def next_variant():
    counter_variant = 1
    if st.session_state.maximum_moment != 0:
        while True:
            # materialchoice
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(f"Variante {counter_variant}")
                    material_choice = st.selectbox(f"Material {counter_variant}", ["Kantholz", "Brettschichtholz", "IPE", "IPB"])
                    st.text(f"Profil {counter_variant}")
                    if material_choice == "Kantholz":  
                        key_list = list(st.session_state.data_storage_wood.keys())
                        image_profil_choice = st.session_state.image_profil_list[material_choice]
                        image_profil = Image.open(image_profil_choice)
                        st.session_state.image_profil_safe = image_profil
                        col2.image(image_profil)
                        cross_section_wood_input = st.selectbox(f"Querschnitt {counter_variant} (b/h)", key_list)
                        width=1
                        check_profil_wood(counter_variant, cross_section_wood_input, material_choice, width)
                    elif material_choice == "IPE":
                        key_list = list(st.session_state.data_storage_ipe.keys())
                        cross_section_ipe_input = st.selectbox(f"Profil {counter_variant}", key_list)
                        image_profil_choice = st.session_state.image_profil_list[material_choice]
                        image_profil = Image.open(image_profil_choice)
                        st.session_state.image_profil_safe = image_profil
                        col2.image(image_profil)
                        check_profil_ipe(counter_variant, cross_section_ipe_input, material_choice, st.session_state.data_storage_ipe)
                    elif material_choice == "IPB":
                        key_list = list(st.session_state.data_storage_ipb.keys())
                        cross_section_ipe_input = st.selectbox(f"Profil {counter_variant}", key_list)
                        image_profil_choice = st.session_state.image_profil_list[material_choice]
                        image_profil = Image.open(image_profil_choice)
                        st.session_state.image_profil_safe = image_profil
                        col2.image(image_profil)
                        check_profil_ipe(counter_variant, cross_section_ipe_input, material_choice, st.session_state.data_storage_ipb)
                    elif material_choice == "Brettschichtholz":
                        key_list = list(st.session_state.data_storage_bsh.keys())
                        image_profil_choice = st.session_state.image_profil_list[material_choice]
                        image_profil = Image.open(image_profil_choice)
                        st.session_state.image_profil_safe = image_profil
                        col2.image(image_profil)
                        cross_section_wood_input = st.selectbox(f"Querschnitt {counter_variant} (h)", key_list)
                        width = st.text_input(label="Breite (cm)",key=counter_variant)
                        if not width:
                            st.error("Bitte gib eine Zahl ein.")
                            return
                        else:
                            if (float(width)*12) < float(cross_section_wood_input):
                                st.error("Die Breite ist zu schmal.")
                                return
                        check_profil_wood(counter_variant, cross_section_wood_input, material_choice, width)
                    # increase counter
                    counter_variant += 2
                    # checkbox for the next variant
                    checkbox_label = "weitere Variante ({})".format(counter_variant)
                    if not st.checkbox(checkbox_label, key=f"checkbox_variant{counter_variant}"):
                        break
# checking the crossection
with st.container(border=True):
    col1, col3 = st.columns(2)
    with col1:
        st.header("Profilauswahl")
        with st.expander("Tabelle Kantholz"):
            st.write(st.session_state.wood_data)
        with st.expander("Tabelle IPE"):
            st.write(st.session_state.ipe_data)
        with st.expander("Tabelle IPB"):
            st.write(st.session_state.ipb_data)
        with st.expander("Tabelle Brettschichtholz"):
            st.write(st.session_state.bsh_data)
        st.session_state.results_variant.clear()
        if st.checkbox("Variante 1"):
            next_variant()
    with col3:
        st.header("Ergebnisübersicht")
        # results of the checking
        for item in st.session_state.results_variant:
            st.subheader(item["title"])
            st.write(item["properties"])
            st.text(item["text"])
if "variant_comparison_list" not in st.session_state:
    st.session_state.variant_comparison_list=[]
if "latex_code_pictures" not in st.session_state:
    st.session_state.latex_code_pictures=[]
def latex_to_png(latex_code, counter_pictures):
    # create a picture of LaTeX-Code
    fg, ax = plt.subplots()
    ax.text(0.5, 0.5, latex_code, size=12, ha='center', va='center', transform=ax.transAxes)
    ax.axis('off')
    output_filename=f"latex_code{counter_pictures}.png"
    # save the picture as PNG
    plt.savefig(output_filename, dpi=50, bbox_inches='tight')
    plt.close()
    st.session_state.latex_code_pictures.append(output_filename)
st.session_state.latex_code_pictures.clear()
def variant_comparison():
        if len(st.session_state.results_variant) != 0:
            # Dynamisch Spalten erstellen
            num_columns = len(st.session_state.results_variant)
            dynamic_columns = st.columns(num_columns)
            # Füllen der Spalten mit Daten
            st.session_state.variant_comparison_list.clear()
            counter_pictures=0
            for i, col in enumerate(dynamic_columns):
                col.subheader(f"Variante {i+1}")
                if st.session_state.results_variant[i]['check_result']==3:
                    check_result="Alle Nachweise erfüllt"
                else:
                    check_result="Nachweise nicht erfüllt"
                col.write(check_result)
                col.image(st.session_state.results_variant[i]['image'])
                col.write(f"Profil = {st.session_state.results_variant[i]['profil_text']}")
                col.write(f"Höhe = {st.session_state.results_variant[i]['height']}cm")
                col.write(f"Breite = {st.session_state.results_variant[i]['width']}cm")
                col.write(f"Eigengewicht = {st.session_state.results_variant[i]['weight']}kg")
                col.write(f"max Moment mit Eigengewicht = {st.session_state.results_variant[i]['max_moment']}kNm")
                col.write("<strong>Tragfähigkeit:</strong>", unsafe_allow_html=True)
                col.markdown(st.session_state.results_variant[i]['w_compare'])
                col.markdown(st.session_state.results_variant[i]['w_how'])
                col.markdown(st.session_state.results_variant[i]['result_w'])
                col.write("<strong>Durchbiegungsnachweis:</strong>", unsafe_allow_html=True)
                col.markdown(st.session_state.results_variant[i]['i_compare'])
                col.markdown(st.session_state.results_variant[i]['i_how'])
                col.markdown(st.session_state.results_variant[i]['result_i']) 
                col.write("<strong>Schubnachweis:</strong>", unsafe_allow_html=True)
                col.markdown(st.session_state.results_variant[i]['a_compare'])
                col.markdown(st.session_state.results_variant[i]['a_how'])
                col.markdown(st.session_state.results_variant[i]['result_a'])
                # saving the LaTex-Code as png
                latex_to_png(st.session_state.results_variant[i]['w_compare'], counter_pictures)
                counter_pictures+=1
                latex_to_png(st.session_state.results_variant[i]['w_how'], counter_pictures)
                counter_pictures+=1
                latex_to_png(st.session_state.results_variant[i]['result_w'], counter_pictures)
                counter_pictures+=1
                latex_to_png(st.session_state.results_variant[i]['i_compare'], counter_pictures)
                counter_pictures+=1
                latex_to_png(st.session_state.results_variant[i]['i_how'], counter_pictures)
                counter_pictures+=1
                latex_to_png(st.session_state.results_variant[i]['result_i'], counter_pictures)
                counter_pictures+=1
                latex_to_png(st.session_state.results_variant[i]['a_compare'], counter_pictures)
                counter_pictures+=1
                latex_to_png(st.session_state.results_variant[i]['a_how'], counter_pictures)
                counter_pictures+=1
                latex_to_png(st.session_state.results_variant[i]['result_a'], counter_pictures)
                counter_pictures+=1
                add_variant_list=[
                f"""Variante {i+1}
                {check_result}
                Profil: {st.session_state.results_variant[i]['profil_text']}
                Höhe: {st.session_state.results_variant[i]['height']}cm
                Breite: {st.session_state.results_variant[i]['width']}cm
                Eigengewicht: {st.session_state.results_variant[i]['weight']}kg
                max Moment mit Eigengewicht: {st.session_state.results_variant[i]['max_moment']}kNm
                erf A: {st.session_state.results_variant[i]['erf_a']}cm²
                erf W: {st.session_state.results_variant[i]['erf_w']}cm³
                erf I: {st.session_state.results_variant[i]['erf_i']}cm^4""",
                st.session_state.image_profil_list[st.session_state.results_variant[i]['profil']]
                ]
                st.session_state.variant_comparison_list.append(add_variant_list)
# variant comparison
with st.expander("Vergleichsansicht"):
    variant_comparison()
# create the PDF
if length==position_b:
    titel="Dimensionierung Einfeldträger"
else:
    titel="Dimensionierung Einfeldträger mit Kragarm"
export_as_pdf = st.button("PDF erstellen")
def create_download_link(val, filename):
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">{titel}</a>'
# write the PDF
länge=f"Spannweite = {length}m"
breite=f"Lasteinzugsbreite = {grid}m"
dach=st.session_state.more_information_roof[st.session_state.selected_option]
gewichts_last=f"{st.session_state.selected_option} = {st.session_state.selected_option_value} kN/m²"
if export_as_pdf: 
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 5, titel, ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    pdf.cell(60, 5, länge)
    pdf.cell(60, 5, breite, ln=True)
    if snow_wind_check:
        pdf.ln(10)
        pdf.multi_cell(0, 5, snow_wind)
    if st.session_state.selected_option is not "kein Dachaufbau":
        pdf.ln(10)
        pdf.multi_cell(0, 5, dach)
        pdf.cell(60, 5, gewichts_last, ln=True)
        pdf.image(st.session_state.image_dachaufbau_auswahl, x=10,y=pdf.get_y() -40, w= 30)
    if len(st.session_state.additional_roof_structures) is not 0:
        pdf.ln(10)
        for additional in st.session_state.additional_roof_structures:
            pdf.cell(0, 5, additional,ln=True)
    if len(st.session_state.forces_array) !=0:
        pdf.multi_cell(0, 5, "Punktlasten:")
        for point in st.session_state.forces_array:
            pdf.cell(50, 5, f"F{point['counter_forces']+1} = {point['point_load']}kN", ln=True)
    pdf.ln(10)
    if len(st.session_state.distributed_load_array) !=0:
        pdf.multi_cell(0, 5, "Streckenlasten:")
        for dist in st.session_state.distributed_load_array:
            pdf.cell(50, 5, f"q{dist['counter_distributed_load']+1} = {dist['distributed_load']}kN/m", ln=True)
    pdf.ln(10)
    pdf.image("image_system.png", w= 150)
    # checking if there is enough space for the pictures
    max_y = pdf.h
    current_position_y = pdf.get_y()
    remaining_space = max_y - current_position_y
    if remaining_space < 80:
        pdf.add_page()
    second_counter=0
    current_position_y=pdf.get_y()
    same_position=current_position_y
    while second_counter<2:
        if second_counter is 0:
            pdf.set_xy(10, same_position)
            pdf.image("image_transverse.png", w=80)
        elif second_counter is 1:
            pdf.set_xy(100, same_position)
            pdf.image("image_moment.png", w=80)
        second_counter += 1
    pdf.ln(10)
    pdf.cell(60, 5, "Auflagerreaktionen A und B", ln=True)
    pdf.ln(10)
    pdf.cell(60, 5, f"A = {st.session_state.support_forces[0]['support_force']} kN und B = {st.session_state.support_forces[1]['support_force']} kN", ln=True)
    pdf.ln(10)
    pdf.cell(60, 5, "Maximales Moment", ln=True)
    pdf.ln(10)
    pdf.cell(60, 5, f"Das maximale Feldmoment beträgt {st.session_state.safe_maximum_moment} kNm und liegt bei {st.session_state.position}m.", ln=True)
    pdf.ln(10)
    if length!=position_b:
        pdf.cell(60, 5, f"Das Stützmoment beträgt {st.session_state.safe_maximum_moment_kragarm} kNm und liegt bei {position_b}m.", ln=True)
        pdf.ln(10)
    counter_pictures = 0
    if st.session_state.results_variant != 0:
        for item in st.session_state.results_variant:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(60, 5, item["title"], ln=True)
            pdf.set_font('Arial', '', 12)
            text_to_edit = item["text"]
            latin1_encoded = text_to_edit.encode('latin-1', 'replace').decode('latin-1')
            new_words_to_remove = "?"
            count = 0
            # change every second ?
            edited_text_1 = ""
            for char in latin1_encoded:
                if char == new_words_to_remove:
                    if count % 2 == 1:
                        edited_text_1 += 'Ausnutzungsgrad'
                    else:
                        edited_text_1 += ''
                    if count==5:
                        count = 0
                    else:
                        count += 1
                else:
                    edited_text_1 += char
            pdf.multi_cell(0, 5, edited_text_1)
            pdf.ln(10)
        for variants in st.session_state.variant_comparison_list:
            pdf.image(variants[1], w=20)
            pdf.multi_cell(0, 5, variants[0])
            pdf.ln(10)
            pdf.cell(60, 5, "Tragfähigkeit:", ln=True)
            max_y = pdf.h
            current_position_y = pdf.get_y()
            remaining_space = max_y - current_position_y
            if remaining_space < 60:
                pdf.add_page()
            second_counter=0
            current_position_y=pdf.get_y()
            same_position=current_position_y
            while second_counter<3:
                if second_counter is 0:
                    pdf.set_xy(10, current_position_y)
                elif second_counter is 1:
                    pdf.set_xy(70, same_position)
                elif second_counter is 2:
                    pdf.set_xy(130, same_position)
                pdf.image(st.session_state.latex_code_pictures[counter_pictures], w=50)
                counter_pictures += 1
                second_counter += 1
            pdf.ln(10)
            pdf.cell(60, 5, "Durchbiegungsnachweis:", ln=True)
            max_y = pdf.h
            current_position_y = pdf.get_y()
            remaining_space = max_y - current_position_y
            if remaining_space < 60:
                pdf.add_page()
            second_counter=0
            current_position_y=pdf.get_y()
            same_position=current_position_y
            while second_counter<3:
                if second_counter is 0:
                    pdf.set_xy(10, current_position_y)
                elif second_counter is 1:
                    pdf.set_xy(70, same_position)
                elif second_counter is 2:
                    pdf.set_xy(130, same_position)
                pdf.image(st.session_state.latex_code_pictures[counter_pictures], w=50)
                counter_pictures += 1
                second_counter += 1
            pdf.ln(10)
            pdf.cell(60, 5, "Schubnachweis:", ln=True)
            max_y = pdf.h
            current_position_y = pdf.get_y()
            remaining_space = max_y - current_position_y
            if remaining_space < 60:
                pdf.add_page()
            second_counter=0
            current_position_y=pdf.get_y()
            same_position=current_position_y
            while second_counter<3:
                if second_counter is 0:
                    pdf.set_xy(10, current_position_y)
                elif second_counter is 1:
                    pdf.set_xy(70, same_position)
                elif second_counter is 2:
                    pdf.set_xy(130, same_position)
                pdf.image(st.session_state.latex_code_pictures[counter_pictures], w=50)
                counter_pictures += 1
                second_counter += 1
            pdf.ln(10)

    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "Dimensionierung Einfeldträger")
    st.markdown(html, unsafe_allow_html=True)