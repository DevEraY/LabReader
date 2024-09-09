all_screens = '''

ScreenManager:
    MainScreen:
        name: 'main'

        
    AboutScreen:
        name: 'about'  


    DisclaimerScreen:
        name: 'disclaimer'        

<MainScreen>:
    MDScreen:


        BoxLayout:
            orientation: 'vertical'
            
            MDNavigationLayout:
                ScreenManager:
                    Screen:
                        BoxLayout:
                            orientation: 'vertical'
                            MDTopAppBar:
                                title: 'Doktor Tahlil'
                                left_action_items: [["menu", lambda x: nav_drawer.set_state('toggle')]]
                                elevation: 3
                            

                            FileChooserListView:
                                id: file_chooser
                                on_selection: root.on_file_selected(self.selection)

                            MDRectangleFlatButton:
                                text: 'Analiz et'
                                on_press: root.process_pdf()

                            MDBoxLayout:
                                orientation: 'horizontal'

                                MDCheckbox:
                                    id: men_checkbox
                                    group: 'gender'
                                    active: True
                                    on_active: root.on_gender_selected('Erkek' if men_checkbox.active else 'Kadın')

                                MDLabel:
                                    text: 'Erkek'

                                MDCheckbox:
                                    id: women_checkbox
                                    group: 'gender'
                                    on_active: root.on_gender_selected('Kadın' if women_checkbox.active else 'Erkek')

                                MDLabel:
                                    text: 'Kadın'  

                            Label:
                                id: output_label
                                text: ''  
                            
                MDNavigationDrawer:
                    id: nav_drawer
                    ContentNavigationDrawer:
                        orientation: 'vertical'
                        padding: "8dp"
                        spacing: "8dp"

                        Image:
                            id: avatar
                            size_hint: (0.5, 0.5)
                            source: "dr_lab_reading.jpeg"

                        MDLabel:
                            text: "Doktor Tahlil"
                            font_style: "Subtitle1"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            text: "PDF şeklindeki tahlillerinizi okur"
                            size_hint_y: None
                            font_style: "Caption"
                            height: self.texture_size[1]

                        ScrollView:
                            DrawerList:
                                id: md_list
                                MDList:
                                    OneLineIconListItem:
                                        text: "Lab Değerlendirme"
                                        on_release: app.change_screen("main")
                                        IconLeftWidget:
                                            icon: "account"

                                    OneLineIconListItem:
                                        text: "Hakkımızda "
                                        on_release: app.change_screen("about") 
                                        IconLeftWidget:
                                            icon: "information-outline"
                       


        
       
<AboutScreen>:
    MDScreen:

        
            

        BoxLayout:
            orientation: 'vertical'
            
            MDNavigationLayout:
                ScreenManager:
                    Screen:
                        BoxLayout:
                            orientation: 'vertical'
                            MDTopAppBar:
                                title: 'Doktor Tahlil'
                                left_action_items: [["menu", lambda x: nav_drawer.set_state('toggle')]]
                                elevation: 1
                            BoxLayout:
                                ScrollView:
                                    size_hint: (None, None)
                                    size: (Window.width * 0.8, Window.height * 0.8)
                                    Label:
                                        id: output_label
                                        text: 'Merhaba ben İstanbul Tıp Fakültesi (nam-ı diğer Çapa)  5. sınıf bir hekim adayıyım. Günümüzde çoğu birey sağlık bilgisini internetten araştırmaktadır. Bu bilgi kirliliğini bir nebze olsa önlemek, tahlillerde yazan garip kısaltmaların ve sonuçların ne anlamaa geldiğini genel bir şekilde tarif etmek amacıyla bu uygulamayı geliştirdim. Sorumluluk reddi beyanında da belirttiğim gibi uygulama herhangi bir tıbbi tavsiye içermemektedir. Tahlillerinizi mutlaka hekiminize danışmanız gerekmektedir. Şu anda uygulama hala geliştirilme aşamasındadır, şikayet ve önerileriniz önem arzetmektedir, iletişim için :'  
                                        multiline: True
                                        width: Window.width * 0.4
                                        height: Window.height * 0.6
                                        text_size: (self.width, None)
                                        size_hint_y: None
                                        halign: 'center'
                                        valign: 'center'
                                    
                MDNavigationDrawer:
                    id: nav_drawer
                    ContentNavigationDrawer:
                        orientation: 'vertical'
                        padding: "8dp"
                        spacing: "8dp"

                        Image:
                            id: avatar
                            size_hint: (0.5, 0.5)
                            source: "dr_lab_reading.jpeg"

                        MDLabel:
                            text: "Doktor Tahlil"
                            font_style: "Subtitle1"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            text: "PDF şeklindeki tahlillerinizi okur"
                            size_hint_y: None
                            font_style: "Caption"
                            height: self.texture_size[1]

                        ScrollView:
                            DrawerList:
                                id: md_list
                                MDList:
                                    OneLineIconListItem:
                                        text: "Lab Değerlendirme"
                                        on_release: app.change_screen("main")
                                        IconLeftWidget:
                                            icon: "account"

                                    OneLineIconListItem:
                                        text: "Hakkımızda "
                                        on_release: app.change_screen("about") 
                                        IconLeftWidget:
                                            icon: "information-outline"
        
       

<DisclaimerScreen>:
    


        

                                               

'''