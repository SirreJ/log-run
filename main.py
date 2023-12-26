import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Der hier verwendete Code war zuvor eine HTML Seite mit JavaScript Code und wurde zu Python übersetzt und weiter angepasst.

st.set_page_config(page_title="Profilberechnung Einfeldträger", page_icon=None, layout='wide')


#Die Werte werden zwar dargestellt, aber haben noch keine möglichkeit in meiner Berechnung berücksichtigt zu werden!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#Auswahlmöglichkeiten für den Dachaufbau

if "forces_array" not in st.session_state:
    st.session_state.distributed_load_array = []

if "forces_array" not in st.session_state:
    st.session_state.counter_distributed_load = 0
st.session_state.selected_option = 0
st.session_state.selected_option_value=0
def dachAufbau():
    # Dictionary mit den Werten für jede Dachaufbauoption
    option_values = {
        "keine Dachaufbau": 0.0,
        "extensive Dachbegrünung": 2.26,
        "intensive Dachbegrünung": 3.51,
        "leichter Dachaufbau": 1.26,
        "schwerer Dachaufbau": 2.0
    }
    # st.selectbox für die Auswahl des Dachaufbaus
    st.session_state.selected_option = st.selectbox("Dachaufbau", list(option_values.keys()))
    st.session_state.selected_option_value = option_values[st.session_state.selected_option]
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
    st.text(distributed_load)
    st.text(st.session_state.distributed_load_array)

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
    st.text(point_load)
    st.text(position)
    st.text(st.session_state.forces_array)
    st.text(st.session_state.counter_forces)

#Auswahlmöglichkeiten für die genaue Lasteingabe
def lastAuswahl():
    counter = 0  # Initialisieren Sie den Zähler
    
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
            position_input = st.text_input("Position (m)", key=f"position_{counter}")
            point_load = float(point_load_input) if point_load_input else 0
            position = float(position_input) if position_input else 0
            if st.button(f"Einfügen {counter}"):
                point_load_properties(length, position, point_load, st.session_state.counter_forces)
        # st.checkbox für die Entscheidung, ob weitere Eingaben gemacht werden sollen
        checkbox_label = "weitere Lasteingabe ({})".format(counter)

        # Eindeutiger Schlüssel für die Checkbox
        if not st.checkbox(checkbox_label, key=f"checkbox_{counter}"):
            break
        
        # Erhöhen Sie den Zähler für den nächsten Satz von Widgets
        counter += 1

# initialisierung von Werten, die während einer sitzung gespeichert werden sollen.
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
def do_calculations_system():
    # Wert des ausgewählten Dachaufbaus
    st.write(st.session_state.safe_counter_distributed_load)
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
    st.write(st.session_state.safe_counter_distributed_load)
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
        st.session_state.weigh_calculation_option = 1

        st.session_state.max_v = float(st.session_state.support_forces[0]['support_force'])

        while number_of_content_d < len(st.session_state.distributed_load_array):
            st.session_state.maximum_moment += st.session_state.distributed_load_array[number_of_content_d]['distributed_load'] * (length**2) / 8
            number_of_content_d += 1
        st.session_state.position = length/2
        st.write("es werden nur streckenlasten berechnet")
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
        st.write("es werden nur punktlasten berechnet")
    elif (len(st.session_state.distributed_load_array) != 1 or st.session_state.distributed_load_array[0]['distributed_load'] != 0) and len(st.session_state.forces_array) != 0:
        st.session_state.weight_calculation_option = 3
        st.session_state.maximum_moment = 0
        for obj in st.session_state.forces_array:
            if obj['position'] > length / 2:
                # Bestimmung der Seite zu welchem Auflager die geringere Entfernung besteht
                side = "right"
                # Füge die neue Eigenschaft zum forces_array hinzu
                obj['side'] = side
                # Falls die Länge doch noch gebraucht wird, sollte dieser neue Wert in das Array mit einem neuen Namen aufgenommen werden
                obj['position'] = length - obj['position']
            elif obj['position'] <= length / 2:
                # Bestimmung der Seite zu welchem Auflager die geringere Entfernung besteht
                side = "left"
                # Füge die neue Eigenschaft zum forces_array hinzu
                obj['side'] = side
        left_side_moment_point_load = 0
        right_side_moment_point_load = 0
        counter_forces_array = 0
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
            while index_counter_position < len(st.session_state.forces_array) and (st.session_state.position_max_momentum > 0 or position_found == True):
                if st.session_state.forces_array[index_counter_position]['side'] == "left":
                    st.session_state.position_max_momentum -= st.session_state.forces_array[index_counter_position]['point_load']
                    st.session_state.position_max_momentum -= position_added_distributed_load * (
                        float(st.session_state.forces_array[index_counter_position]['position']) - last_added_position
                    )
                    last_added_position = st.session_state.forces_array[index_counter_position]['position']
                    # Überprüfung, ob die folgenden Werte noch links sind
                    count_left = 0
                    for index_count_side in range(index_counter_position + 1, len(st.session_state.forces_array)):
                        if st.session_state[index_count_side]['side'] == 'left':
                            count_left += 1
                    index_counter_position += 1
                    # Prüfen, ob der Nullpunkt zwischen zwei Punktlasten liegt.
                    position_between_point_loads = 0
                    position_between_point_loads = st.session_state.position_max_momentum / float(position_added_distributed_load)
                    if index_counter_position >= len(st.session_state.forces_array):
                        st.session_state.position = last_added_position
                    else:
                        if (
                            position_between_point_loads < float(st.session_state.forces_array[index_counter_position]['position'] - last_added_position)
                            and st.session_state.forces_array[index_counter_position]['side'] == "left"
                        ) or (count_left == 0):
                            st.session_state.position = last_added_position + position_between_point_loads
                            position_found = True
                else:
                    index_counter_position += 1
        else:
            st.session_state.side_and_position_max_momentum.append(side := "right")
            # Streckenlasten addieren, damit zur weiteren Verwendung in der Positionsbestimmung
            st.session_state.position_max_momentum += st.session_state.support_forces[1]['support_force']
            last_added_position = 0
            # Last zur Bestimmung der Position, wenn das maximale Moment bei dem Umschlagpunkt von positiv zu negativ an der Position einer Einzellast
            while index_counter_position < len(st.session_state.forces_array) and (st.session_state.position_max_momentum > 0 or position_found == True):
                if st.session_state.forces_array[index_counter_position]['side'] == "right":
                    st.session_state.position_max_momentum -= st.session_state.forces_array[index_counter_position]['point_load']
                    st.session_state.position_max_momentum -= position_added_distributed_load * (
                        float(st.session_state.forces_array[index_counter_position]['position']) - last_added_position
                    )
                    last_added_position = st.session_state.forces_array[index_counter_position]['position']
                    # Überprüfung, ob die folgenden Werte noch links sind
                    count_left = 0
                    for index_count_side in range(index_counter_position + 1, len(st.session_state.forces_array)):
                        if st.session_state[index_count_side]['side'] == 'right':
                            count_left += 1
                    index_counter_position += 1
                    # Prüfen, ob der Nullpunkt zwischen zwei Punktlasten liegt.
                    position_between_point_loads = 0
                    position_between_point_loads = st.session_state.position_max_momentum / float(position_added_distributed_load)
                    if index_counter_position >= len(st.session_state.forces_array):
                        st.session_state.position = last_added_position
                    else:
                        if (
                            position_between_point_loads < float(st.session_state.forces_array[index_counter_position]['position'] - last_added_position)
                            and st.session_state.forces_array[index_counter_position]['side'] == "right"
                        ) or (count_left == 0):
                            st.session_state.position = last_added_position + position_between_point_loads
                            position_found = True
                else:
                    index_counter_position += 1
        # Sortieren der Werte nach ihrem Index
        st.session_state.forces_array.sort(key=lambda x: x['counter_forces'])
        st.session_state.position = format(st.session_state.position, '.2f')  # Rundet auf zwei Dezimalstellen
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
        st.write("es werden punktlasten und streckenlasten berechnet")
    else:
        st.write("es werden keine Lasten zur berechnung genutzt")
        st.write(st.session_state.distributed_load_array)
        st.write(st.session_state.forces_array)
    st.session_state.maximum_moment = round(st.session_state.maximum_moment, 2)
    st.session_state.safe_maximum_moment = 0
    #Moment vor dem Einfluss des Sicherheitsbeiwerts sichern.
    if st.session_state.maximum_moment != st.session_state.safe_maximum_moment:
        st.session_state.safe_maximum_moment += float(st.session_state.maximum_moment)
    st.session_state.maximum_moment *= st.session_state.safety_factor
    st.session_state.maximum_moment = round(st.session_state.maximum_moment, 2)

st.header("Vordimensionierung Einfeldträger")
st.write("Text zur Erläuterung der Nutzung des Programms und Informationen zu ausgeführten Berechnungen und gegebenenfalls Annahmen zur Berechnung der Profile. Holzprofile werden mit den Werten für C24 Nadelholz nach DIN EN 338 berechnet. Stahlprofile werden mit den Werten für St 37 (S235) Baustahl berechnet. ")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # Eingaben für das statische System
        st.subheader("Eingabe für das statische System")
        length_input = st.text_input ("Spannweite", 5)
        length = float(length_input)

        grid_input = st.text_input("Lasteinzugsbreite", 3)
        grid = float(grid_input)
       
        dachAufbau()

        if st.checkbox("Genaue Lasteingabe"):
            lastAuswahl()

        if st.button("Berechnen"):
            do_calculations_system()
    with col2:
        # Darstellungsbereich
        st.header("Darstellungsbereich")
        #Darstellung

        # Ergebnissausgabe
        st.subheader("Auflagerreaktionen A und B")
        #st.text(auflagerreaktion)
        st.write(f"A = {st.session_state.support_forces[0]['support_force']} kN und B = {st.session_state.support_forces[1]['support_force']} kN")

        st.subheader("Maximales Moment")
        #Moment ausgeben
        st.write(f"Das maximale Feldmoment beträgt {st.session_state.safe_maximum_moment} kNm und liegt bei {st.session_state.position}m.")
        
# Kleine Datenbank mit Werten (klein)
# Eigengewicht hinzufügen
st.session_state.data_storage_wood = {
    "8/16": {"available_w": 341, "availableITrägheitsmoment": 2730, "h": 16, "availableArea": 128, "weightPerMeterInKG": 7.68},
    "10/20": {"available_w": 667, "availableITrägheitsmoment": 6670, "h": 20, "availableArea": 200, "weightPerMeterInKG": 12},
    "12/24": {"available_w": 1150, "availableITrägheitsmoment": 13820, "h": 24, "availableArea": 288, "weightPerMeterInKG": 17.3},
    "13/18": {"available_w": 702, "availableITrägheitsmoment": 6320, "h": 18, "availableArea": 234, "weightPerMeterInKG": 14},
    "14/28": {"available_w": 1830, "availableITrägheitsmoment": 25610, "h": 28, "availableArea": 392, "weightPerMeterInKG": 23.4},
    "16/24": {"available_w": 1536, "availableITrägheitsmoment": 18430, "h": 24, "availableArea": 384, "weightPerMeterInKG": 23},
    "18/26": {"available_w": 972, "availableITrägheitsmoment": 8750, "h": 26, "availableArea": 468, "weightPerMeterInKG": 28}
}

if "tension_rd_wood" not in st.session_state: 
    st.session_state.tension_rd_wood = 1.5
if "needed_w" not in st.session_state: 
    st.session_state.needed_w = 0
if "number_k0" not in st.session_state:
    st.session_state.number_k0 = 312
if "number_k0" not in st.session_state:
    st.session_state.maximum_moment_check = 0
def check_profil():
    weight = 0
    weight = float(st.session_state.data_storage_wood[cross_section_wood_input]["weightPerMeterInKG"])
    # kg in kN umwandeln
    weight = weight * length / 100
    st.session_state.maximum_moment_check = st.session_state.maximum_moment
    if st.session_state.weight_calculation_option == 1:
        st.session_state.maximum_moment_check += weight
    elif st.session_state.weight_calculation_option == 2:
        st.session_state.maximum_moment_check += weight * (st.session_state.forces_array[st.session_state.maximum_moment_position_in_array]["position"] ** 2) / 2
    elif st.session_state.weight_calculation_option == 3:
        st.session_state.maximum_moment_check += weight * (st.session_state.side_and_position_max_momentum[1] ** 2) / 2
    # Bei den Momentenbestimmungen auch die Position bestimmen
    st.session_state.needed_w = (st.session_state.maximum_moment_check * 100) / st.session_state.tension_rd_wood
    #anpassen an die Zahl der Variante, wenn es möglich ist
    if st.session_state.needed_w != 0:
        col2.header("Ergebnisübersicht Variante 1")
    # Zugriff auf Datenbank und Suche nach passendem W.
    if st.session_state.needed_w > st.session_state.data_storage_wood[cross_section_wood_input]["available_w"]:
        col2.write("Das gewählte Profil passt nicht.")
        col2.write("erf W > vorh W")
        col2.write(f"{st.session_state.needed_w} > {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}")
        # Neue Querschnitt wählen, wenn nötig.
        # Weitere Rechnungen einfügen oder Vergleich für Gebrauchstauglichkeit oder Schubspannungsnachweis + Überprüfung, ob es einen besseren Querschnitt gibt!!!
    else:
        # Die 1 in den Texten anpassen, wenn mehrere Varianten möglich sind!!!
        if (length * 100) / st.session_state.data_storage_wood[cross_section_wood_input]["h"] > 15:
            # Gebrauchstauglichkeitsnachweis
            needed_i_traegheitsmoment = st.session_state.number_k0 * (st.session_state.safe_maximum_moment/100) * (length * 100)
            if needed_i_traegheitsmoment <= st.session_state.data_storage_wood[cross_section_wood_input]["availableITrägheitsmoment"]:
                col2.write("Der Tragfähigkeitsnachweis und der Gebrauchstauglichkeitsnachweis bestehen die Prüfung.")
                col2.write("erf W < vorh W")
                col2.write(f"{st.session_state.needed_w} < {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}")
                col2.write("erf I < vorh I")
                col2.write(f"{needed_i_traegheitsmoment} < {st.session_state.data_storage_wood[cross_section_wood_input]['availableITrägheitsmoment']}")
            else:
                col2.write("Das Profil der Variante 1 besteht die Prüfung nicht.")
                col2.write("Neuen Querschnitt wählen aufgrund des Gebrauchstauglichkeitsnachweises.") 
                col2.write("erf W < vorh W")
                col2.write(f"{st.session_state.needed_w} < {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}") 
                col2.write("erf I > vorh I")
                col2.write(f"{needed_i_traegheitsmoment} > {st.session_state.data_storage_wood[cross_section_wood_input]['availableITrägheitsmoment']}")         
        elif (length * 100) / st.session_state.data_storage_wood[cross_section_wood_input]["h"] < 11:
            # Schubnachweis
            print(st.session_state.max_v)
            needed_area = (3 * st.session_state.max_v) / (2 * st.session_state.schub_rd)
            if needed_area <= st.session_state.data_storage_wood[cross_section_wood_input]["availableArea"]:
                col2.write("Der Tragfähigkeitsnachweis und der Schubnachweis bestehen die Prüfung.")
                col2.write("erf W < vorh W")
                col2.write(f"{st.session_state.needed_w} < {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}") 
                col2.write("erf A < vorh A")
                col2.write(f"{needed_area} < {st.session_state.data_storage_wood[cross_section_wood_input]['availableArea']}")
            else:
                col2.write("Das Profil der Variante 1 besteht die Prüfung nicht.")
                col2.write("Neuen Querschnitt wählen aufgrund des Schubnachweises.") 
                col2.write("erf W < vorh W")
                col2.write(f"{st.session_state.needed_w} < {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}") 
                col2.write("erf A > vorh A")
                col2.write(f"{needed_area} > {st.session_state.data_storage_wood[cross_section_wood_input]['availableArea']}")
        else:
            col2.write("Das Profil der Variante 1 besteht die Prüfung.")
            col2.write("Es ist kein Nachweis der Gebrauchstauglichkeit oder der Spannung notwendig.")
            col2.write("erf W < vorh W")
            col2.write(f"{st.session_state.needed_w} < {st.session_state.data_storage_wood[cross_section_wood_input]['available_w']}") 
def next_variant():
    counter = 0  # Initialisieren Sie den Zähler
    # Materialauswahl
    material_choice = st.selectbox("Material", ["Kantholz", "IPE"])
    st.text("Profil")
    if material_choice == "Kantholz":
        cross_section_wood_input = st.text_input("Querschnitt (b/h)", value="8/16")
        if st.button("Prüfen"):
            check_profil()
    elif material_choice == "IPE":
        cross_section_ipe_input = st.text_input("Querschnitt", placeholder="Platzhalter")
        if st.button("Prüfen"):
            check_profil()
    if st.checkbox("weitere Variante"):
        next_variant()
    counter += 1

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Profilauswahl:")
        st.text("Variante 1")
        st.text("Mögliche Querschnitte Aktuell: 8/16, 10/20, 12/24, 13/18, 14/28, 16/24, 18/26")
        # Materialauswahl
        material_choice = st.selectbox("Material", ["Kantholz", "IPE"])
        st.text("Profil")
        if material_choice == "Kantholz":
            cross_section_wood_input = st.text_input("Querschnitt (b/h)", value="8/16")
            if st.button("Prüfen"):
                check_profil()
        elif material_choice == "IPE":
            cross_section_ipe_input = st.text_input("Querschnitt", placeholder="Platzhalter")
            if st.button("Prüfen"):
                check_profil()
        if st.checkbox("weitere Variante"):
            next_variant()

    with col2:
        if st.session_state.needed_w == 0:
            st.header("Ergebnisübersicht")

with st.container():
    # Weitere Informationen
    st.header("Weitere Informationen")