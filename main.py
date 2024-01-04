import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

# Der hier verwendete Code war zuvor eine HTML Seite mit JavaScript Code und wurde zu Python übersetzt und weiter angepasst.

st.set_page_config(page_title="Profilberechnung Einfeldträger", page_icon=None, layout='wide')

# erstellen eines Links
def create_link(url,text):
    return '<a href="{}" target="_blank">{}</a>'.format(url, text)
# Schnee- und Windlast
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
    option_height = {
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
    }
    option_zone = {
        "1",
        "1a",
        "2",
        "2a",
        "3"
    }
    st.session_state.snow_and_wind.clear()
    st.session_state.selected_option_snow_height = st.selectbox("Geländehöhe von NN", list(option_height))
    st.session_state.selected_option_snow_zone = st.selectbox("Zonenauswahl", list(option_zone))
    st.session_state.snow_load = st.session_state.data_storage_snow[st.session_state.selected_option_snow_height][st.session_state.selected_option_snow_zone]*0.8
    st.session_state.snow_load = round(st.session_state.snow_load, 2)
    new_snow=[st.session_state.snow_load, st.session_state.wind_load]
    st.session_state.snow_and_wind.append(new_snow)
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
    option_place = {
        "1 Binnenland",
        "2 Binnenland",
        "2 Küste und Inseln der Ostsee",
        "3 Binnenland",
        "3 Küste und Inseln der Ostsee",
        "4 Binnenland",
        "4 Küste der Nord- und Ostsee und Inseln der Ostsee",
        "4 Inseln der Nordsee"
    }
    option_building_height = {
        "< 10m",
        "10 m <h< 18m",
        "18 m < h < 25 m"
    }
    st.session_state.snow_and_wind.clear()
    st.session_state.selected_option_place = st.selectbox("Windzone und Standort", list(option_place))
    st.session_state.selected_option_building_height = st.selectbox("Gebäudehöhe", list(option_building_height))
    st.session_state.wind_load = st.session_state.data_storage_wind[st.session_state.selected_option_place][st.session_state.selected_option_building_height]*0.7
    st.session_state.wind_load = round(st.session_state.wind_load, 2)
    new_wind=[st.session_state.snow_load, st.session_state.wind_load]
    st.session_state.snow_and_wind.append(new_wind)
    if np.isnan (st.session_state.snow_and_wind[0][1]):
        st.error("Bitte gib eine gültige Gebäudehöhe ein.")
        return
if "distributed_load_array" not in st.session_state:
    st.session_state.distributed_load_array = []
if "counter_distributed_load" not in st.session_state:
    st.session_state.counter_distributed_load = 0
# Auswahlmöglichkeiten für den Dachaufbau
if "selected_option" not in st.session_state:
    st.session_state.selected_option = 0
if "selected_option_value" not in st.session_state:
    st.session_state.selected_option_value=0
# Bild Laden
if "image_length_grid" not in st.session_state:
    image_length_grid = Image.open('dachaufbau/Spannweite_Lasteinzugsbreite.jpg')
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
    extensive_dachbegrünung = st.session_state.snow_and_wind[0][0] + st.session_state.snow_and_wind[0][1] + st.session_state.layer_load_roof['extensive Dachbegrünung 10cm'] + st.session_state.layer_load_roof['zweilagige Dachabdichtung'] + st.session_state.layer_load_roof['Dämmstoff 20cm'] + st.session_state.layer_load_roof['Dampfsperre'] + st.session_state.layer_load_roof['Trapezblech']
    intensive_dachbegrünung = st.session_state.snow_and_wind[0][0] + st.session_state.snow_and_wind[0][1] + st.session_state.layer_load_roof['intensive Dachbegrünung 20cm'] + st.session_state.layer_load_roof['zweilagige Dachabdichtung'] + st.session_state.layer_load_roof['Dämmstoff 20cm'] + st.session_state.layer_load_roof['Dampfsperre'] + st.session_state.layer_load_roof['Trapezblech']
    leichter_dachaufbau = st.session_state.snow_and_wind[0][0] + st.session_state.snow_and_wind[0][1] + st.session_state.layer_load_roof['zweilagige Dachabdichtung'] + st.session_state.layer_load_roof['Dämmstoff 20cm'] + st.session_state.layer_load_roof['Dampfsperre'] + st.session_state.layer_load_roof['Trapezblech']
    schwerer_dachaufbau = st.session_state.snow_and_wind[0][0] + st.session_state.snow_and_wind[0][1] + st.session_state.layer_load_roof['Kies 5cm'] + st.session_state.layer_load_roof['zweilagige Dachabdichtung'] + st.session_state.layer_load_roof['Dämmstoff 20cm'] + st.session_state.layer_load_roof['Dampfsperre'] + st.session_state.layer_load_roof['BSH 4cm']
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
        'extensive Dachbegrünung':'dachaufbau/Pikto_Dachaufbau_extensiv.jpg',
        'intensive Dachbegrünung':'dachaufbau/Pikto_Dachaufbau_intensiv.jpg',
        'leichter Dachaufbau':'dachaufbau/Pikto_Dachaufbau_leicht.jpg',
        'schwerer Dachaufbau':'dachaufbau/Pikto_Dachaufbau_schwer.jpg',
        'kein Dachaufbau':'dachaufbau/Pikto_kein_Dachaufbau.jpg'
    }
    # st.selectbox für die Auswahl des Dachaufbaus
    st.session_state.selected_option = st.selectbox("Dachaufbau", list(option_values.keys()), help="Der Dachaufbau wird erst beim Klicken auf den Berechnungs Knopf in das statische System hinzugefügt. Die angegebene Last beinhaltet Schnee- und Windlast")
    st.session_state.selected_option_value = option_values[st.session_state.selected_option]
    # Passendes Bild Laden
    image_dachaufbau_auswahl = image_dachaufbau_list[st.session_state.selected_option]
    st.session_state.image_dachaufbau = Image.open(image_dachaufbau_auswahl)
    # Zeigen Sie den ausgewählten Wert neben der Option an
    st.write(f"{st.session_state.selected_option} : {st.session_state.selected_option_value} kN/m²")
#aufnahme der Streckenlasten
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
#Aufnahme der Puntktlasten
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
#Auswahlmöglichkeiten für die genaue Lasteingabe
def last_auswahl():
    counter = 1
    while True:
        # st.radio für die Auswahl von "Streckenlast" oder "Punktlast"
        # Weisen Sie eindeutige Schlüssel mit dem Zähler zu
        load_type = st.radio("Lasteingabe", ["Streckenlast", "Punktlast"], key=f"load_type_{counter}")
                    
        if load_type == "Streckenlast":
            # st.text_input für die Streckenelast mit einem eindeutigen Schlüssel
            distributed_load_input = st.text_input("Streckenelast (kN/m)", key=f"distributed_load_{counter}")
            distributed_load = float(distributed_load_input) if distributed_load_input else 0
            if st.button(f"Einfügen {counter}"):
                distributed_load_information(distributed_load, st.session_state.counter_distributed_load)
        elif load_type == "Punktlast":
            # st.text_input für die Punktlast und Position mit eindeutigen Schlüsseln
            point_load_input = st.text_input("Punktlast (kN)", key=f"point_load_{counter}")
            position_input = st.text_input("Position (m)", key=f"position_{counter}", help="Die Position ist die Entfernung der Punktlast von Auflager A.")
            point_load = float(point_load_input) if point_load_input else 0
            position = float(position_input) if position_input else 0
            if st.button(f"Einfügen {counter}"):
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
if "safe_counter_distributed_load" not in st.session_state:
    st.session_state.safe_counter_distributed_load = None
# Berechnung des statischen Systems
def do_calculations_system():
    # Wert des ausgewählten Dachaufbaus
    if st.session_state.safe_counter_distributed_load is not None:
        st.session_state.distributed_load_array.pop(st.session_state.safe_counter_distributed_load)
        option_distributed_load = st.session_state.selected_option_value * grid
        option_distributed_load = round(option_distributed_load, 2)
        new_distributed_load = {"counter_distributed_load" : st.session_state.safe_counter_distributed_load, "distributed_load" : option_distributed_load}
        st.session_state.distributed_load_array.insert(st.session_state.safe_counter_distributed_load, new_distributed_load)
    else:
        option_distributed_load = st.session_state.selected_option_value * grid
        st.session_state.safe_counter_distributed_load = st.session_state.counter_distributed_load
        option_distributed_load = round(option_distributed_load, 2)
        new_distributed_load = {"counter_distributed_load" : st.session_state.counter_distributed_load, "distributed_load" : option_distributed_load}
        st.session_state.distributed_load_array.append(new_distributed_load)
        st.session_state.counter_distributed_load = st.session_state.safe_counter_distributed_load
        st.session_state.counter_distributed_load += 1
    #Bestimmung der Auflagerkräfte
    resulting_forces = 0
    support_force_a_vertical = 0
    support_force_b_vertical = 0
    for distributed in st.session_state.distributed_load_array:
        resulting_forces += distributed["distributed_load"] * length / 2
        support_force_a_vertical += distributed["distributed_load"] * length

    point_load_calculation = 0
    for point_load in st.session_state.forces_array:
        point_load_calculation += point_load["point_load"] * (point_load["position"] / length)
        support_force_a_vertical += point_load["point_load"]

    support_force_b_vertical = point_load_calculation + resulting_forces
    support_force_a_vertical -= support_force_b_vertical



    support_force_a_vertical = round(support_force_a_vertical, 2)
    support_force_b_vertical = round(support_force_b_vertical, 2)

    # Entfernen der zuvor gespeicherten Auflagerkräfte
    if st.session_state.support_forces != []:
        st.session_state.support_forces.pop()
        st.session_state.support_forces.pop()
    
    # Speichern der Auflagerkräfte zur späteren Verwendung
    st.session_state.support_forces.append({"side": "left", "support_force": support_force_a_vertical})
    st.session_state.support_forces.append({"side": "right", "support_force": support_force_b_vertical})
    st.session_state.maximum_moment_position_in_array = 0

    # Ermittlung des maximalen Moments
    # Überprüfen, ob das erste if und das zweite if zum gleichen Ergebnis führen, wenn nur ein Moment angegeben ist!
    # Berechnung wenn für Momente
    if len(st.session_state.distributed_load_array) != 0 and len(st.session_state.forces_array) == 0:
        st.session_state.position = 0
        number_of_content_d= 0
        st.session_state.maximum_moment = 0
        st.session_state.weight_calculation_option = 1

        st.session_state.max_v = float(st.session_state.support_forces[0]['support_force'])

        while number_of_content_d < len(st.session_state.distributed_load_array):
            st.session_state.maximum_moment += st.session_state.distributed_load_array[number_of_content_d]['distributed_load'] * (length**2) / 8
            number_of_content_d += 1
        st.session_state.position = length/2
    elif (len(st.session_state.distributed_load_array) == 0 or st.session_state.distributed_load_array[0]['distributed_load'] == 0) and len(st.session_state.forces_array) != 0: 
        st.session_state.position = 0
        st.session_state.maximum_moment = 0
        st.session_state.weight_calculation_option = 2
        for obj in st.session_state.forces_array:
            if obj['position'] > length / 2:
                # Bestimmung der Seite zu welchem Auflager die geringere Entfernung besteht
                side = "right"
                # Füge die neue Eigenschaft zum st.session_state.forces_array hinzu
                obj['side'] = side
                # Falls die Länge doch noch gebraucht wird, sollte dieser neue Wert in das Array mit einem neuen Namen aufgenommen werden
                obj['position'] = length - obj['position']
            elif obj['position'] <= length / 2:
                # Bestimmung der Seite zu welchem Auflager die geringere Entfernung besteht
                side = "left"
                # Füge die neue Eigenschaft zum st.session_state.forces_array hinzu
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
            if (
                st.session_state.forces_array[indexCounter]['side'] == st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]['side']
                and st.session_state.forces_array[indexCounter]['position'] < st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]['position']
            ):
                st.session_state.maximum_moment += -float(st.session_state.forces_array[indexCounter]['point_load']) * (
                    float(st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]['position']) - float(st.session_state.forces_array[indexCounter]['position'])
                )
                st.session_state.position = st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]['position']
                indexCounter += 1  # Hochzählen, damit jedes Objekt einzeln abgefragt wird.
            else:
                indexCounter += 1
    elif (len(st.session_state.distributed_load_array) != 1 or st.session_state.distributed_load_array[0]['distributed_load'] != 0) and len(st.session_state.forces_array) != 0:
        st.session_state.weight_calculation_option = 3
        st.session_state.maximum_moment = 0
        for obj in st.session_state.forces_array:
            # Bestimmung der Seite zu welchem Auflager die geringere Entfernung besteht
            if obj['position'] > length / 2:
                side = "right"
                # Füge die neue Eigenschaft zum forces_array hinzu
                obj['side'] = side
                # Die Entfernung zum Auflager B wird erstellt
                obj['position'] = length - obj['position']
            elif obj['position'] <= length / 2:
                side = "left"
                # Füge die neue Eigenschaft zum forces_array hinzu
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
                            if st.session_state[index_count_side]['side'] == 'left':
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
                        # Überprüfung, ob die folgenden Werte noch links sind
                        count_right = 0
                        for index_count_side in range(index_counter_position + 1, len(st.session_state.forces_array)):
                            if st.session_state[index_count_side]['side'] == 'right':
                                count_right += 1
                        index_counter_position += 1
                        # Prüfen, ob der Nullpunkt zwischen zwei Punktlasten liegt.
                        st.session_state.position = last_added_position
                        position_between_point_loads = 0
                        position_between_point_loads = st.session_state.position_max_momentum / float(position_added_distributed_load)
                        st.write(position_between_point_loads)
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
        st.session_state.position = round(st.session_state.position, 2)  # Rundet auf zwei Dezimalstellen
        st.session_state.side_and_position_max_momentum.append(st.session_state.position)
        support_number = None
        # Herausfinden, welches Auflager zur Schnittberechnung geeignet ist
        # Anpassen, wenn Einfeldträger zu Mehrfeldträger wird!!!!!!!!!!!!
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
                st.session_state.maximum_moment += -float(st.session_state.forces_array[index_counter]['point_load']) * (
                    float(st.session_state.side_and_position_max_momentum[1]) - float(st.session_state.forces_array[index_counter]['position'])
                )
                index_counter += 1  # Hochzählen, damit jedes Objekt einzeln abgefragt wird.
            else:
                index_counter += 1
        number_of_content_d = 0
        while number_of_content_d < len(st.session_state.distributed_load_array):
            st.session_state.maximum_moment = float(st.session_state.maximum_moment) - (
                float(st.session_state.distributed_load_array[number_of_content_d]['distributed_load'])
                * (float(st.session_state.side_and_position_max_momentum[1]) ** 2) / 2
            )
            number_of_content_d += 1
        if st.session_state.side_and_position_max_momentum[0] == 'right':
            st.session_state.position = length - st.session_state.position 
    st.session_state.maximum_moment = round(st.session_state.maximum_moment, 2)
    st.session_state.safe_maximum_moment = 0
    #Moment vor dem Einfluss des Sicherheitsbeiwerts sichern.
    if st.session_state.maximum_moment != st.session_state.safe_maximum_moment:
        st.session_state.safe_maximum_moment += float(st.session_state.maximum_moment)
    st.session_state.maximum_moment *= st.session_state.safety_factor
    st.session_state.maximum_moment = round(st.session_state.maximum_moment, 2)
# Zeichnung des statischen Systems
def drawing_system():
    # Systemlinie
    startpoint_a = 0
    endpoint_b = 10
    middle_of_canvas_y = 5
    x_values_systemline = np.array([startpoint_a, endpoint_b])
    y_values_systemline = np.array([middle_of_canvas_y, middle_of_canvas_y])
    # Matplotlib-Funktion zum Zeichnen der Linie
    fig, ax = plt.subplots()
    ax.plot(x_values_systemline, y_values_systemline, marker=',', linestyle='-', color='black')
    ax.set_title('statisches System')
    plt.text(startpoint_a+((endpoint_b-startpoint_a)/2), middle_of_canvas_y-0.5, f'{length}m', fontsize=12, color='black', ha='center', va='center')
    #Auflager
    #Festlager
    x_values_fixed_support = np.array([startpoint_a, startpoint_a+0.5, startpoint_a-0.5, startpoint_a])
    y_values_fixed_support = np.array([middle_of_canvas_y, middle_of_canvas_y-1, middle_of_canvas_y-1, middle_of_canvas_y])
    ax.plot(x_values_fixed_support, y_values_fixed_support, marker=',', linestyle='-', color='black')
    plt.text(startpoint_a-1, middle_of_canvas_y-0.5, 'A', fontsize=12, color='black', ha='center', va='center')
    counter_slashes_fixed = 0
    while (counter_slashes_fixed<5):
         x_values_fixed_support_slash = np.array([startpoint_a-0.6+0.2*counter_slashes_fixed, startpoint_a-0.4+0.2*counter_slashes_fixed])
         y_values_fixed_support_slash = np.array([middle_of_canvas_y-1.3, middle_of_canvas_y-1])
         ax.plot(x_values_fixed_support_slash, y_values_fixed_support_slash, marker=',', linestyle='-', color='black')
         counter_slashes_fixed += 1
    #Lostlager
    x_values_not_fixed_support = np.array([endpoint_b, endpoint_b+0.5, endpoint_b-0.5, endpoint_b])
    y_values_not_fixed_support = np.array([middle_of_canvas_y, middle_of_canvas_y-1, middle_of_canvas_y-1, middle_of_canvas_y])
    ax.plot(x_values_not_fixed_support, y_values_not_fixed_support, marker=',', linestyle='-', color='black')
    plt.text(endpoint_b+1, middle_of_canvas_y-0.5, 'B', fontsize=12, color='black', ha='center', va='center')
    x_value_litle_line = np.array([endpoint_b-0.7, endpoint_b+0.7])
    y_value_litle_line = np.array([middle_of_canvas_y-1.2, middle_of_canvas_y-1.2])
    ax.plot(x_value_litle_line, y_value_litle_line, marker=',', linestyle='-', color='black')
    counter_slashes_fixed = 0
    while (counter_slashes_fixed<5):
         x_values_not_fixed_support_slash = np.array([endpoint_b-0.6+0.2*counter_slashes_fixed, endpoint_b-0.4+0.2*counter_slashes_fixed])
         y_values_not_fixed_support_slash = np.array([middle_of_canvas_y-1.5, middle_of_canvas_y-1.2])
         ax.plot(x_values_not_fixed_support_slash, y_values_not_fixed_support_slash, marker=',', linestyle='-', color='black')
         counter_slashes_fixed += 1
    #Streckenlast
    for arrow_field in st.session_state.distributed_load_array:
        if arrow_field["distributed_load"] != 0:
            length_between_supports = endpoint_b-startpoint_a
            x_value_distributed = np.array([startpoint_a, endpoint_b, endpoint_b, startpoint_a])
            y_value_distributed = np.array([middle_of_canvas_y+0.1+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.1+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.4+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.4+0.6*arrow_field["counter_distributed_load"]])
            ax.plot(x_value_distributed, y_value_distributed, marker=',', linestyle='-', color='black')
            length_between_supports = length_between_supports/7
            counter_arrows_dist = 0
            while counter_arrows_dist<8:
                force_location_x = startpoint_a + length_between_supports*counter_arrows_dist
                x_value_tip = np.array([force_location_x-0.1,force_location_x,force_location_x+0.1])
                y_value_tip = np.array([middle_of_canvas_y+0.2+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.1+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.2+0.6*arrow_field["counter_distributed_load"]])
                ax.plot(x_value_tip, y_value_tip, marker=',', linestyle='-', color='black')
                x_value_stick = np.array([force_location_x, force_location_x])
                y_value_stick = np.array([middle_of_canvas_y+0.1+0.6*arrow_field["counter_distributed_load"], middle_of_canvas_y+0.4+0.6*arrow_field["counter_distributed_load"]])
                ax.plot(x_value_stick, y_value_stick , marker=',', linestyle='-', color='black')
                counter_arrows_dist +=1
            plt.text(endpoint_b+1, middle_of_canvas_y+0.3+0.6*arrow_field["counter_distributed_load"], f'q{arrow_field["counter_distributed_load"]+1} = {arrow_field["distributed_load"]}kN/m', fontsize=12, color='black', ha='left', va='center')       
    #Punktlast
    if len(st.session_state.distributed_load_array) == 0 or st.session_state.distributed_load_array[0]["distributed_load"] ==0:
        for arrow in st.session_state.forces_array:
            force_location_x = startpoint_a + ((endpoint_b-startpoint_a)/length)*arrow["position"]
            x_value_tip = np.array([force_location_x-0.3,force_location_x,force_location_x+0.3])
            y_value_tip = np.array([middle_of_canvas_y+0.4, middle_of_canvas_y+0.1, middle_of_canvas_y+0.4])
            ax.plot(x_value_tip, y_value_tip, marker=',', linestyle='-', color='black')
            x_value_stick = np.array([force_location_x, force_location_x])
            y_value_stick = np.array([middle_of_canvas_y+0.1, middle_of_canvas_y+4])
            ax.plot(x_value_stick, y_value_stick , marker=',', linestyle='-', color='black')
            plt.text(force_location_x, middle_of_canvas_y+4.5, f'F{arrow["counter_forces"]+1} = {arrow["point_load"]}kN', fontsize=12, color='black', ha='center', va='center')
    else:
        for arrow in st.session_state.forces_array:
            force_location_x = startpoint_a + ((endpoint_b-startpoint_a)/length)*arrow["position"]
            x_value_tip = np.array([force_location_x-0.3,force_location_x,force_location_x+0.3])
            y_value_tip = np.array([middle_of_canvas_y+0.4+0.6*len(st.session_state.distributed_load_array), middle_of_canvas_y+0.1+0.6*len(st.session_state.distributed_load_array), middle_of_canvas_y+0.4+0.6*len(st.session_state.distributed_load_array)])
            ax.plot(x_value_tip, y_value_tip, marker=',', linestyle='-', color='black')
            x_value_stick = np.array([force_location_x, force_location_x])
            y_value_stick = np.array([middle_of_canvas_y+0.1+0.6*len(st.session_state.distributed_load_array), middle_of_canvas_y+4])
            ax.plot(x_value_stick, y_value_stick , marker=',', linestyle='-', color='black')
            plt.text(force_location_x, middle_of_canvas_y+4.5, f'F{arrow["counter_forces"]+1} = {arrow["point_load"]}kN', fontsize=12, color='black', ha='center', va='center')

    plt.xlim(-2,12)
    plt.ylim(-2,12)
    plt.axis('off')
    st.pyplot(fig)
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
# Beginn der Benutzeroberfläche
st.header("Vordimensionierung Einfeldträger")
st.write("Text zur Erläuterung der Nutzung des Programms und Informationen zu ausgeführten Berechnungen und gegebenenfalls Annahmen zur Berechnung der Profile. Holzprofile werden mit den Werten für C24 Nadelholz nach DIN EN 338 berechnet. Stahlprofile werden mit den Werten für St 37 (S235) Baustahl berechnet.")
# Statisches System
with st.container(border=True):
    col1, col3 = st.columns(2)
    with col1:
        # Eingaben für das statische System
        st.header("Eingabe für das statische System")
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                length_input = st.text_input ("Spannweite (m)", 5, help="Die Spannweite bestimmt die Länge des Trägers.")
                length = float(length_input)
                grid_input = st.text_input("Lasteinzugsbreite (m)", 3, help="Die Lasteinzugsbreite wird benötigt um die Last des Dachaufbaus auf den Träger zu bestimmen.")
                grid = float(grid_input)
            with col2:
                image_length_grid_place(length, grid)
        with st.expander("Wind- und Schneelast"):
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    img_url_snow="https://www.die.de/dokumentation/holzbau-dach/technik/images/schneelastzonen.jpg"
                    st.image(img_url_snow, caption="Schneelastzonen")
                    text = "Hier gelangst du zur Quelle des Bilds."
                    link_html =create_link(img_url_snow,text)
                    st.markdown(link_html, unsafe_allow_html=True)
                    more_information_snow()
                with col2:
                    img_url_wind="https://www.obo.de/fileadmin/default/OBO/Produkte/Transienten-_und_Blitzschutz-Systeme/Planungshilfen/VdS_Richtlinie__Blitzschutzklassen-Einteilung/Ermitteln_der_Windlast/deutschland-karte-windzonen.png"
                    st.image(img_url_wind, caption="Windlastzonen")
                    text = "Hier gelangst du zur Quelle des Bilds."
                    link_html =create_link(img_url_wind,text)
                    st.markdown(link_html, unsafe_allow_html=True)
                    more_information_wind()
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                dach_aufbau()
                with st.expander("Daten Dachaufbau"):
                    # Genauer Dachaufbau
                    if "more_information_roof" not in st.session_state:
                        st.session_state.more_information_roof = {
                            "kein Dachaufbau": 
                            """ 
                            
                            """,
                            "extensive Dachbegrünung": 
                            f""" 
                            Schneelast = {st.session_state.snow_and_wind[0][0]}kN/m²
                            Windlast = {st.session_state.snow_and_wind[0][1]}kN/m²
                            extensive Dachbegrünung 10cm = {st.session_state.layer_load_roof['extensive Dachbegrünung 10cm']}kN/m²
                            zweilagige Dachabdichtung = {st.session_state.layer_load_roof['zweilagige Dachabdichtung']}kN/m²
                            Dämmstoff 20cm = {st.session_state.layer_load_roof['Dämmstoff 20cm']}kN/m²
                            Dampfsperre = {st.session_state.layer_load_roof['Dampfsperre']}kN/m²
                            Trapezblech = {st.session_state.layer_load_roof['Trapezblech']}kN/m²        
                            """,
                            "intensive Dachbegrünung": 
                            f""" 
                            Schneelast = {st.session_state.snow_and_wind[0][0]}kN/m²
                            Windlast = {st.session_state.snow_and_wind[0][1]}kN/m²
                            intensive Dachbegrünung 20cm = {st.session_state.layer_load_roof['intensive Dachbegrünung 20cm']}kN/m²
                            zweilagige Dachabdichtung = {st.session_state.layer_load_roof['zweilagige Dachabdichtung']}kN/m²
                            Dämmstoff 20cm = {st.session_state.layer_load_roof['Dämmstoff 20cm']}kN/m²
                            Dampfsperre = {st.session_state.layer_load_roof['Dampfsperre']}kN/m²
                            Trapezblech = {st.session_state.layer_load_roof['Trapezblech']}kN/m²
                            """,
                            "leichter Dachaufbau": 
                            f""" 
                            Schneelast = {st.session_state.snow_and_wind[0][0]}kN/m²
                            Windlast = {st.session_state.snow_and_wind[0][1]}kN/m²
                            zweilagige Dachabdichtung = {st.session_state.layer_load_roof['zweilagige Dachabdichtung']}kN/m²
                            Dämmstoff 20cm = {st.session_state.layer_load_roof['Dämmstoff 20cm']}kN/m²
                            Dampfsperre = {st.session_state.layer_load_roof['Dampfsperre']}kN/m²
                            Trapezblech = {st.session_state.layer_load_roof['Trapezblech']}kN/m²
                            """,
                            "schwerer Dachaufbau": 
                            f""" 
                            Schneelast = {st.session_state.snow_and_wind[0][0]}kN/m²
                            Windlast = {st.session_state.snow_and_wind[0][1]}kN/m²
                            Kies 5cm = {st.session_state.layer_load_roof['Kies 5cm']}kN/m²
                            zweilagige Dachabdichtung = {st.session_state.layer_load_roof['zweilagige Dachabdichtung']}kN/m²
                            Dämmstoff 20cm = {st.session_state.layer_load_roof['Dämmstoff 20cm']}kN/m²
                            Dampfsperre = {st.session_state.layer_load_roof['Dampfsperre']}kN/m²
                            BSH 4cm = {st.session_state.layer_load_roof['BSH 4cm']}kN/m²
                            """,
                        }
                    st.text(st.session_state.more_information_roof[st.session_state.selected_option])
            with col2:
                st.image(st.session_state.image_dachaufbau)
        if st.checkbox("Genaue Lasteingabe"):
            last_auswahl()
        if st.button("Berechnen"):
            do_calculations_system()
    with col3:
        # Darstellungsbereich
        st.header("Darstellungsbereich")
        #Darstellung
        drawing_system()
        # Ergebnissausgabe
        st.subheader("Auflagerreaktionen A und B")
        #st.text(auflagerreaktion)
        st.write(f"A = {st.session_state.support_forces[0]['support_force']} kN und B = {st.session_state.support_forces[1]['support_force']} kN")
        st.subheader("Maximales Moment")
        #Moment ausgeben
        st.write(f"Das maximale Feldmoment beträgt {st.session_state.safe_maximum_moment} kNm und liegt bei {st.session_state.position}m.")
# Laden von Daten, @st.cache damit sie nur geladen werden, wenn man sie braucht.
if "wood_data" not in st.session_state:
    st.session_state.wood_data = pd.read_excel('tabellen/Tabelle_Kantholz.xlsx')
if "data_storage_wood" not in st.session_state:
    st.session_state.data_storage_wood = {}
    # Erstellung der Datenbank mit Werten für kanthölzer.
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
if "ipe_data" not in st.session_state:
    st.session_state.ipe_data = pd.read_excel('tabellen/Tabelle_IPE.xlsx')
if "data_storage_ipe" not in st.session_state:
    st.session_state.data_storage_ipe = {}
    # Erstellung der Datenbank mit Werten für kanthölzer.
    for rows in st.session_state.ipe_data.iterrows():
        key = f"{rows[1]['b']}/{rows[1]['h']}"
        values = {
            "b": rows[1]['b'],
            "h": rows[1]['h'],
            "availableArea": rows[1]['A'],
            "weightPerMeterInKG": rows[1]['G'],
            "availableITrägheitsmoment": int(rows[1]['I']),
            "available_w": rows[1]['W']
        }
        st.session_state.data_storage_ipe[key] = values
if "tension_rd" not in st.session_state: 
    st.session_state.tension_rd = {
        "IPE": 21.8,
        "Kantholz": 1.5
    }
if "needed_w" not in st.session_state: 
    st.session_state.needed_w = 0
if "number_k0" not in st.session_state:
    st.session_state.number_k0 = {
        "IPE": 15,
        "Kantholz": 312
    }
if "number_k0" not in st.session_state:
    st.session_state.schub_rd = {
        "IPE": 12.6,
        "Kantholz": 0.12
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
def check_profil_wood(counter_variant, cross_section_wood_input, material_choice):
    # Entfernen der zuvor gespeicherten Ergebnisse
    if len(st.session_state.results_variant) > 0 and len(st.session_state.results_variant) > counter_variant:
        del st.session_state.results_variant[counter_variant-1]
    weight = 0
    weight = float(st.session_state.data_storage_wood[cross_section_wood_input]["weightPerMeterInKG"])
    safe_weight = 0
    safe_weight += weight
    # kg in kN umwandeln
    weight = weight * length / 100
    st.session_state.safe_maximum_moment_check = st.session_state.safe_maximum_moment
    st.session_state.maximum_moment_check = st.session_state.maximum_moment
    if st.session_state.weight_calculation_option == 1:
        st.session_state.maximum_moment_check += weight
        st.session_state.safe_maximum_moment_check += weight
    elif st.session_state.weight_calculation_option == 2:
        st.session_state.maximum_moment_check += weight * (st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]["position"] ** 2) / 2
        st.session_state.safe_maximum_moment_check += weight * (st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]["position"] ** 2) / 2
    elif st.session_state.weight_calculation_option == 3:
        st.session_state.maximum_moment_check += weight * (st.session_state.side_and_position_max_momentum[1] ** 2) / 2
        st.session_state.safe_maximum_moment_check += weight * (st.session_state.side_and_position_max_momentum[1] ** 2) / 2
    # Bei den Momentenbestimmungen auch die Position bestimmen
    st.session_state.maximum_moment_check = round(st.session_state.maximum_moment_check, 2)
    st.session_state.safe_maximum_moment_check = round(st.session_state.safe_maximum_moment_check, 2)
    st.session_state.needed_w = (st.session_state.maximum_moment_check * 100) / st.session_state.tension_rd[material_choice]
    results_variant_title = f'''Variante {counter_variant}'''
    # Zugriff auf Datenbank und Suche nach passendem W.
    st.session_state.needed_i_traegheitsmoment=0
    st.session_state.needed_area=0
    st.session_state.needed_w = round(st.session_state.needed_w, 2)
    if st.session_state.needed_w > st.session_state.data_storage_wood[cross_section_wood_input]["available_w"]:
        results_variant = f'''
        Das gewählte Profil passt nicht.
        erf W > vorh W
        {st.session_state.needed_w}cm³ > {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}cm³
        '''
    else:
        if (length * 100) / st.session_state.data_storage_wood[cross_section_wood_input]["h"] > 15:
            # Gebrauchstauglichkeitsnachweis
            st.session_state.needed_i_traegheitsmoment = st.session_state.number_k0[material_choice] * (st.session_state.safe_maximum_moment_check/100) * (length * 100)
            st.session_state.needed_i_traegheitsmoment = round(st.session_state.needed_i_traegheitsmoment, 2)
            if st.session_state.needed_i_traegheitsmoment <= st.session_state.data_storage_wood[cross_section_wood_input]["availableITrägheitsmoment"]:
                results_variant = f'''
                Der Tragfähigkeitsnachweis und der Gebrauchstauglichkeitsnachweis bestehen die Prüfung.
                erf W < vorh W
                {st.session_state.needed_w}cm³ < {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}cm³
                erf I < vorh I
                {st.session_state.needed_i_traegheitsmoment}cm⁴ < {st.session_state.data_storage_wood[cross_section_wood_input]['availableITrägheitsmoment']}cm⁴
                '''
            else:
                results_variant = f'''
                Das Profil der Variante {counter_variant} besteht die Prüfung nicht.
                Neuen Querschnitt wählen aufgrund des Gebrauchstauglichkeitsnachweises.
                erf W < vorh W
                {st.session_state.needed_w}cm³ < {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}cm³
                erf I > vorh I
                {st.session_state.needed_i_traegheitsmoment}cm⁴ > {st.session_state.data_storage_wood[cross_section_wood_input]['availableITrägheitsmoment']}cm⁴
                '''         
        elif (length * 100) / st.session_state.data_storage_wood[cross_section_wood_input]["h"] < 11:
            # Schubnachweis mit Sicherheitsbeiwert von 1.4
            st.session_state.needed_area = ((3 * st.session_state.max_v)* 1.4) / (2 * st.session_state.schub_rd[material_choice])
            if st.session_state.needed_area <= st.session_state.data_storage_wood[cross_section_wood_input]["availableArea"]:
                results_variant = f'''
                Der Tragfähigkeitsnachweis und der Schubnachweis bestehen die Prüfung.
                erf W < vorh W
                {st.session_state.needed_w}cm³ < {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}cm³
                erf A < vorh A
                {st.session_state.needed_area}cm² < {st.session_state.data_storage_wood[cross_section_wood_input]['availableArea']}cm²
                '''
            else:
                results_variant = f'''
                Das Profil der Variante {counter_variant} besteht die Prüfung nicht.
                Neuen Querschnitt wählen aufgrund des Schubnachweises. 
                erf W < vorh W
                {st.session_state.needed_w}cm³ < {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}cm³
                erf A > vorh A
                {st.session_state.needed_area}cm² > {st.session_state.data_storage_wood[cross_section_wood_input]['availableArea']}cm²
                '''
        else:
            results_variant = f'''
            Das Profil der Variante {counter_variant} besteht die Prüfung.
            Es ist kein Nachweis der Gebrauchstauglichkeit oder der Spannung notwendig.
            erf W < vorh W
            {st.session_state.needed_w}cm³ < {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}cm³
            '''
    # Speichern der Ergebnisse
    result_variant_array = {"title": results_variant_title, "text": results_variant, "profil": material_choice,"max_moment": st.session_state.maximum_moment_check, "weight": safe_weight, "height": st.session_state.data_storage_wood[cross_section_wood_input]["h"], "width":st.session_state.data_storage_wood[cross_section_wood_input]["b"], "erf_a": st.session_state.needed_area, "erf_w": st.session_state.needed_w, "erf_i": st.session_state.needed_i_traegheitsmoment, "image": st.session_state.image_profil_safe}
    # Ersetzen der Ergebnisse
    st.session_state.results_variant.insert(counter_variant-1, result_variant_array)
if "image_profil_list" not in st.session_state:
    st.session_state.image_profil_list = {
        'Kantholz':'material_profil/Pikto_Kantholz.jpg',
        'IPE':'material_profil/Pikto_IPE.jpg'
    }
if "image_profil_safe" not in st.session_state:
    st.session_state.image_profil_safe = 0
def check_profil_ipe(counter_variant, cross_section_ipe_input, material_choice):
     # Entfernen der zuvor gespeicherten Ergebnisse
    if len(st.session_state.results_variant) > 0 and len(st.session_state.results_variant) > counter_variant:
        del st.session_state.results_variant[counter_variant-1]
    weight = 0
    weight = float(st.session_state.data_storage_ipe[cross_section_ipe_input]["weightPerMeterInKG"])
    safe_weight = 0
    safe_weight += weight
    # kg in kN umwandeln
    weight = weight * length / 100
    st.session_state.safe_maximum_moment_check = st.session_state.safe_maximum_moment
    st.session_state.maximum_moment_check = st.session_state.maximum_moment
    if st.session_state.weight_calculation_option == 1:
        st.session_state.maximum_moment_check += weight
        st.session_state.safe_maximum_moment_check += weight
    elif st.session_state.weight_calculation_option == 2:
        st.session_state.maximum_moment_check += weight * (st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]["position"] ** 2) / 2
        st.session_state.safe_maximum_moment_check += weight * (st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]["position"] ** 2) / 2
    elif st.session_state.weight_calculation_option == 3:
        st.session_state.maximum_moment_check += weight * (st.session_state.side_and_position_max_momentum[1] ** 2) / 2
        st.session_state.safe_maximum_moment_check += weight * (st.session_state.side_and_position_max_momentum[1] ** 2) / 2
    # Bei den Momentenbestimmungen auch die Position bestimmen
    st.session_state.maximum_moment_check = round(st.session_state.maximum_moment_check, 2)
    st.session_state.safe_maximum_moment_check = round(st.session_state.safe_maximum_moment_check, 2)
    st.session_state.needed_w = (st.session_state.maximum_moment_check * 100) / st.session_state.tension_rd[material_choice]
    results_variant_title = f'''Variante {counter_variant}'''
    # Zugriff auf Datenbank und Suche nach passendem W.
    st.session_state.needed_i_traegheitsmoment=0
    st.session_state.needed_area=0
    st.session_state.needed_w = round(st.session_state.needed_w, 2)
    if st.session_state.needed_w > st.session_state.data_storage_ipe[cross_section_ipe_input]["available_w"]:
        results_variant = f'''
        Das gewählte Profil passt nicht.
        erf W > vorh W
        {st.session_state.needed_w}cm³ > {st.session_state.data_storage_ipe[cross_section_ipe_input]['available_w']}cm³
        '''
    else:
        if (length * 100) / st.session_state.data_storage_ipe[cross_section_ipe_input]["h"] > 22:
            # Gebrauchstauglichkeitsnachweis
            st.session_state.needed_i_traegheitsmoment = st.session_state.number_k0[material_choice] * (st.session_state.safe_maximum_moment_check/100) * (length * 100)
            st.session_state.needed_i_traegheitsmoment = round(st.session_state.needed_i_traegheitsmoment, 2)
            if st.session_state.needed_i_traegheitsmoment <= st.session_state.data_storage_ipe[cross_section_ipe_input]["availableITrägheitsmoment"]:
                results_variant = f'''
                Der Tragfähigkeitsnachweis und der Gebrauchstauglichkeitsnachweis bestehen die Prüfung.
                erf W < vorh W
                {st.session_state.needed_w}cm³ < {st.session_state.data_storage_ipe[cross_section_ipe_input]['available_w']}cm³
                erf I < vorh I
                {st.session_state.needed_i_traegheitsmoment}cm⁴ < {st.session_state.data_storage_ipe[cross_section_ipe_input]['availableITrägheitsmoment']}cm⁴
                '''
            else:
                results_variant = f'''
                Das Profil der Variante {counter_variant} besteht die Prüfung nicht.
                Neuen Querschnitt wählen aufgrund des Gebrauchstauglichkeitsnachweises.
                erf W < vorh W
                {st.session_state.needed_w}cm³ < {st.session_state.data_storage_ipe[cross_section_ipe_input]['available_w']}cm³
                erf I > vorh I
                {st.session_state.needed_i_traegheitsmoment}cm⁴ > {st.session_state.data_storage_ipe[cross_section_ipe_input]['availableITrägheitsmoment']}cm⁴
                '''         
        elif (length * 100) / st.session_state.data_storage_ipe[cross_section_ipe_input]["h"] < 6:
            # Schubnachweis mit Sicherheitsbeiwert von 1.4
            st.session_state.needed_area = (st.session_state.max_v * 1.4) / st.session_state.schub_rd[material_choice]
            if st.session_state.needed_area <= st.session_state.data_storage_ipe[cross_section_ipe_input]["availableArea"]:
                results_variant = f'''
                Der Tragfähigkeitsnachweis und der Schubnachweis bestehen die Prüfung.
                erf W < vorh W
                {st.session_state.needed_w}cm³ < {st.session_state.data_storage_ipe[cross_section_ipe_input]['available_w']}cm³
                erf A < vorh A
                {st.session_state.needed_area}cm² < {st.session_state.data_storage_ipe[cross_section_ipe_input]['availableArea']}cm²
                '''
            else:
                results_variant = f'''
                Das Profil der Variante {counter_variant} besteht die Prüfung nicht.
                Neuen Querschnitt wählen aufgrund des Schubnachweises. 
                erf W < vorh W
                {st.session_state.needed_w}cm³ < {st.session_state.data_storage_ipe[cross_section_ipe_input]['available_w']}cm³
                erf A > vorh A
                {st.session_state.needed_area}cm² > {st.session_state.data_storage_ipe[cross_section_ipe_input]['availableArea']}cm²
                '''
        else:
            results_variant = f'''
            Das Profil der Variante {counter_variant} besteht die Prüfung.
            Es ist kein Nachweis der Gebrauchstauglichkeit oder der Spannung notwendig.
            erf W < vorh W
            {st.session_state.needed_w}cm³ < {st.session_state.data_storage_ipe[cross_section_ipe_input]['available_w']}cm³
            '''
    # Speichern der Ergebnisse
    result_variant_array = {"title": results_variant_title, "text": results_variant, "profil": material_choice,"max_moment": st.session_state.maximum_moment_check, "weight": safe_weight, "height": st.session_state.data_storage_ipe[cross_section_ipe_input]["h"], "width":st.session_state.data_storage_ipe[cross_section_ipe_input]["b"], "erf_a": st.session_state.needed_area, "erf_w": st.session_state.needed_w, "erf_i": st.session_state.needed_i_traegheitsmoment, "image": st.session_state.image_profil_safe}
    # Ersetzen der Ergebnisse
    st.session_state.results_variant.insert(counter_variant-1, result_variant_array)
def next_variant():
    counter_variant = 1
    while True:
        # Materialauswahl
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"Variante {counter_variant}")
                material_choice = st.selectbox(f"Material {counter_variant}", ["Kantholz", "IPE"])
                st.text(f"Profil {counter_variant}")
                if material_choice == "Kantholz":    
                    image_profil_choice = st.session_state.image_profil_list[material_choice]
                    image_profil = Image.open(image_profil_choice)
                    st.session_state.image_profil_safe = image_profil
                    col2.image(image_profil)
                    cross_section_wood_input = st.text_input(f"Querschnitt {counter_variant} (b/h)", value="8/16")
                    if st.button(f"Prüfen {counter_variant}"):
                        check_profil_wood(counter_variant, cross_section_wood_input, material_choice)
                elif material_choice == "IPE":
                    cross_section_ipe_input = st.text_input(f"Querschnitt {counter_variant}", value="10.0/20.0", help="Das IPE Profil muss mit einer Nachkommastelle eingegeben werden.")
                    image_profil_choice = st.session_state.image_profil_list[material_choice]
                    image_profil = Image.open(image_profil_choice)
                    st.session_state.image_profil_safe = image_profil
                    col2.image(image_profil)
                    if st.button(f"Prüfen {counter_variant}"):
                        check_profil_ipe(counter_variant, cross_section_ipe_input, material_choice)
                # Zähler erhöhen
                counter_variant += 1
                # Checkbox für die nächste Variante
                checkbox_label = "weitere Variante ({})".format(counter_variant)
                if not st.checkbox(checkbox_label, key=f"checkbox_variant{counter_variant}"):
                    break
# Überprüfung der Querschnitte
with st.container(border=True):
    col1, col3 = st.columns(2)
    with col1:
        st.header("Profilauswahl")
        with st.expander("Tabelle Kantholz"):
            st.write(st.session_state.wood_data)
        with st.expander("Tabelle IPE"):
            st.write(st.session_state.ipe_data)
        if st.checkbox("Variante 1"):
            next_variant()
    with col3:
        st.header("Ergebnisübersicht")
        # Ergebnisse der Überprüfung
        for item in st.session_state.results_variant:
            st.subheader(item["title"])
            st.text(item["text"])
def variant_comparison():
        if len(st.session_state.results_variant) != 0:
            # Dynamisch Spalten erstellen
            num_columns = len(st.session_state.results_variant)
            dynamic_columns = st.columns(num_columns)
            # Füllen der Spalten mit Daten
            for i, col in enumerate(dynamic_columns):
                col.subheader(f"Variante {i+1}")
                col.write(f"Profil: {st.session_state.results_variant[i]['profil']}")
                col.image(st.session_state.results_variant[i]['image'])
                col.write(f"Höhe: {st.session_state.results_variant[i]['height']}cm")
                col.write(f"Breite: {st.session_state.results_variant[i]['width']}cm")
                col.write(f"Eigengewicht: {st.session_state.results_variant[i]['weight']}kg")
                col.write(f"max Moment mit Eigengewicht: {st.session_state.results_variant[i]['max_moment']}kNm")
                col.write(f"erf A: {st.session_state.results_variant[i]['erf_a']}cm²")
                col.write(f"erf W: {st.session_state.results_variant[i]['erf_w']}cm³")
                col.write(f"erf I: {st.session_state.results_variant[i]['erf_i']}cm⁴")     
# Variantenvergleich
with st.expander("Weitere Informationen"):
    variant_comparison()