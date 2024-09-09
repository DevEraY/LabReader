import pandas as pd
from difflib import SequenceMatcher
import tabula
import json
from kivy.app import App
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screenmanager import MDScreenManager
from lab_reader_screens import all_screens
from kivy.lang.builder import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList,OneLineListItem
from kivymd.uix.button import MDRaisedButton
from kivymd.theming import ThemableBehavior
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from disclaimer_text import disclaimer


class TahlilValue:
    def __init__(self, name,sonuc, birim):
        self.name = name
        if isinstance(sonuc, float):
                    
            sonuc_numeric = sonuc  # No need for conversion if it's already a float
        else:
            if all(char.isdigit() or char == '.' or char == "," for char in sonuc):
                sonuc_final = sonuc.replace(",", ".")
                sonuc_numeric = float(sonuc_final)
                        
            else:
                
                sonuc_numeric = 0
        self.sonuc = sonuc_numeric
        self.birim = birim
        self.similarity_points = []

    def add_similarity_point(self, param_instance, similarity):
        self.similarity_points.append((param_instance, similarity))

    def rank_similarity_points(self):
        self.similarity_points.sort(key=lambda x: x[1], reverse=True)

class ParameterValue:
    def __init__(self, name, unit, gender, LL, UL, LM, HM):
        self.name = name
        self.unit = unit
        self.gender = gender
        self.lower_limit = LL
        self.upper_limit = UL
        self.low_message = LM
        self.high_message = HM



        self.similarity_points = []

    def add_similarity_point(self, tahlil_instance, similarity):
        self.similarity_points.append((tahlil_instance, similarity))

    def rank_similarity_points(self):
        self.similarity_points.sort(key=lambda x: x[1], reverse=True)

class DisclaimerScreen(Screen):
    
    def on_enter(self):
        app = App.get_running_app()
        filename = "kullanici_bilgilendirme_okudu_onayladi.json"
        with open(filename, 'r') as file:
            data = json.load(file)

        self.dialog_shown = data ['kullanici_bilgilendirme_onay']    
        if not self.dialog_shown:
            self.show_disclaimer_popup()
        else:
            app.change_screen("main")    

    def show_disclaimer_popup(self):
        
        popup_content = BoxLayout(orientation="vertical", spacing=10)
        
        # Add disclaimer text
        disclaimer_text = disclaimer
        disclaimer_label = Label(
            text=disclaimer_text,
            size_hint_y=None,
            size_hint_x=None,
            valign="top",
            
            text_size=(Window.width * 0.8 - 40, None)
        )
        disclaimer_label.bind(texture_size=disclaimer_label.setter('size'))

        content_scrollview = ScrollView(size_hint=(None, None), size=(Window.width * 0.8 , Window.height * 0.4),
                                        bar_width=15, do_scroll_x=False, do_scroll_y=True)

        content_scrollview.add_widget(disclaimer_label)
        
        popup_content.add_widget(content_scrollview)
        
        # Add Accept button
        accept_button = Button(text="Okudum, anladım, kabul ediyorum.", size_hint=(None, None), size=(300, 50), font_size=16)
        accept_button.bind(on_release=self.accept_disclaimer)
        popup_content.add_widget(accept_button)

        self.popup = Popup(
            title="Sorumluluk reddi beyanı",
            content=popup_content,
            size_hint=(None, None),
            size=(Window.width * 0.8 , Window.height * 0.6),
            auto_dismiss=False,
            separator_height=0
        )
        self.popup.open()

    def accept_disclaimer(self,instance):
        app = App.get_running_app()
        # Change kullanici_bilgilendirme_onay to True
        # Update the JSON file with the new value
        with open('kullanici_bilgilendirme_okudu_onayladi.json', 'w') as json_file:
            json.dump({'kullanici_bilgilendirme_onay': True}, json_file)    
        self.popup.dismiss()
        app.change_screen("main")
    
    
    

class MainScreen(Screen):
    gender = "Male"
    

    def on_gender_selected(self, selected_gender):
        print(selected_gender)
        if selected_gender == "Kadın":
            self.gender = "Female"

        elif selected_gender == "Erkek":
            self.gender = "Male"


        return


    def on_file_selected(self,  selection):
        if selection:
            self.file_path = selection[0]

    def process_pdf(self):
        if not self.file_path:
            self.output_label.text = "Please select a PDF file."
            return

        try:
            tables = tabula.read_pdf(self.file_path, pages="all", multiple_tables=True)
        except Exception as e:
            self.output_label.text = f"Error extracting tables: {e}"
            return

        combined_df = pd.concat(tables, ignore_index=True)

        # ... (Rest of your processing code)
        def jaccard_similarity(str1, str2):
            set1 = set(str1)
            set2 = set(str2)

            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            return intersection / union

        def similar_substring(a, b):
            string_1 = a.lower().replace(" ", "")
            string_2 = b.lower().replace(" ", "")
            similarity = SequenceMatcher(None, string_1, string_2).ratio()
            return similarity

        def composite_similarity(target, reference):
            jaccard = jaccard_similarity(target, reference)
            substring = similar_substring(target, reference)

            # Adjust weights based on importance
            weight_jaccard = 0.2
            weight_substring = 0.8

            composite_score = (weight_jaccard * jaccard) + (weight_substring * substring)

            return composite_score



        # Read "combined_tables" Excel file
        combined_tables = combined_df
        # Read "parametrelerr.csv" file
        parameters = pd.read_csv('parametrelerr.csv')

        # Create Tahlil and Parameter values based on the data

        tahlil_values = [TahlilValue(row['Tahlil'], row['Sonuç'], row['Sonuç\rBirimi']) for index, row in combined_tables.iterrows() if pd.notna(row['Tahlil'])]
        parameter_values = [ParameterValue(row['Parameter'], row['Unit'],row['Gender'],row['Lower_Limit'],row['Upper_Limit'],row['Low_Message'],row['High_Message'] ) for index, row in parameters.iterrows() if pd.notna(row['Parameter'])]

        # Add similarity points based on the calculated values
        for tahlil_instance in tahlil_values:
            for parameter_instance in parameter_values:
                similarity = composite_similarity(tahlil_instance.name, parameter_instance.name)
                if tahlil_instance.birim != parameter_instance.unit:
                    similarity = similarity - 0.5                    
                   
                if self.gender == parameter_instance.gender:
                    similarity = similarity + 0.08

                tahlil_instance.add_similarity_point(parameter_instance, similarity)
                parameter_instance.add_similarity_point(tahlil_instance, similarity)

        # Rank similarity points for each Tahlil and Parameter
        for tahlil in tahlil_values:
            tahlil.rank_similarity_points()

        for parameter in parameter_values:
            parameter.rank_similarity_points()

        # Create pairs based on the highest similarity points
        matched_pairs = {}

        def find_best_match_for_parameter(parameter_instance, tahlil_instances):
            best = parameter_instance.similarity_points[0]
            most_similar_name_parameter = best[0]
            return most_similar_name_parameter

        for parameter_instance in parameter_values:
            best_parameter = find_best_match_for_parameter(parameter_instance, tahlil_values)

            # Check if the best match is also the best match for the Tahlil instance
            for tahlil_instance in tahlil_values:
                best = tahlil_instance.similarity_points
                bestest = best[0][0]
                most_similar_name_tahlil = bestest.name
                if best_parameter.name == tahlil_instance.name and parameter_instance.name == most_similar_name_tahlil and \
                        best[0][1] > 0.5:
                    matched_pairs[parameter_instance] = tahlil_instance

        # Create a GridLayout to hold the Labels (allows both x and y scrolling)
        content_scrollview = ScrollView(size_hint=(None, None), size=(Window.width * 0.8 , Window.height * 0.6),
                                        bar_width=15, do_scroll_x=True, do_scroll_y=True)

        container_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        container_layout.bind(minimum_height=container_layout.setter('height'))




        # Print matched pairs
        output_text = "Matched Pairs:\n"
        for parameter, tahlil in matched_pairs.items():
            sonuc = combined_tables.loc[combined_tables['Tahlil'] == tahlil.name, 'Sonuç'].values[0]
            result = None

            


            

            def is_within_limits(sonuc_numeric, lower_limit, upper_limit):
                responding_message = ""
                low_mes = parameter.low_message
                high_mes = parameter.high_message

                if sonuc_numeric < lower_limit:
                    responding_message = f"{tahlil.name} değeriniz düşük çıkmıştır.  {low_mes}"
                    #f"{tahlil} değeriniz referans değerden düşük çıkmıştır. Normal aralık {lower_limit} - {upper_limit} arasındadır. Tavsiyemiz: {low_mes}"


                elif sonuc_numeric > upper_limit:
                    responding_message = f"{tahlil.name} değeriniz yüksek çıkmıştır.  {high_mes}"

                else:
                    print("sıkıntı yok")
                return responding_message
            if pd.notna(sonuc):
                result = is_within_limits(tahlil.sonuc, parameter.lower_limit, parameter.upper_limit)

            popup_width = Window.width * 0.8
            max_line_length_factor = 0.09  # Adjust the factor as needed
            max_line_length = int(popup_width * max_line_length_factor)

            if result and result != "nan":
                result_label = Label(text=result, font_size='15sp', markup=True, size_hint_y=None, height=dp(30),
                                     valign='top')  # Adjust height as needed
                result_label.bind(size=result_label.setter('text_size'))
                print(f"Length of the popup text: {popup_width}")
                print(f"Calculated max_line_length: {max_line_length}")
                print(f"Length of the result text: {len(result)}")

                # Check sentence length and add line breaks
                if len(result) > max_line_length:


                    result_lines = [result[i:i + max_line_length] for i in range(0, len(result), max_line_length)]
                    for line in result_lines:
                        line_label = Label(text=line, font_size='15sp', markup=True, size_hint_y=None, height=dp(30),
                                           valign='top', text_size=(Window.width * 0.8 - 40, None) )
                        line_label.bind(size=line_label.setter('text_size'))
                        container_layout.add_widget(line_label)
                else:
                    container_layout.add_widget(result_label)

                line_of_hashes = Label(text='#' * int(max_line_length * 0.8), font_size='15sp', markup=True, size_hint_y=None,
                                       height=dp(30), valign='top')
                line_of_hashes.bind(size=line_of_hashes.setter('text_size'))
                container_layout.add_widget(line_of_hashes)

        content_scrollview = ScrollView(size_hint=(None, None), size=(Window.width * 0.8 , Window.height * 0.5),
                                        bar_width=15, do_scroll_x=True, do_scroll_y=True)
        content_scrollview.add_widget(container_layout)

        # Create a Popup with the ScrollView as content
        popup = Popup(title='PDF Processing Result', content=content_scrollview,
                      size_hint=(None, None), size=(Window.width * 0.8, Window.height * 0.6))
        popup.open()


class AboutScreen(Screen):
    

    pass

class ContentNavigationDrawer(BoxLayout):
    pass

class DrawerList(MDList, ThemableBehavior):
    pass


class MyApp(MDApp):
    

    def change_screen(self, screen_name):
        self.root.current = screen_name
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.file_path = None

        # Main layout
        self.root = Builder.load_string(all_screens)
        self.root.current = 'disclaimer'
        print(self.root.current)
        #
        # # FileChooserListView for selecting a PDF file
        # file_chooser = FileChooserListView()
        # file_chooser.bind(selection=self.on_file_selected)
        # main_layout.add_widget(file_chooser)
        #
        # # Button to start processing
        # process_button = Button(text="Process PDF", on_press=self.process_pdf)
        # main_layout.add_widget(process_button)
        #
        # # Output label
        # self.output_label = Label(text="")
        # main_layout.add_widget(self.output_label)
        #
        return self.root







MyApp().run()
