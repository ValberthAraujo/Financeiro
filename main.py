from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("./assets/UI/interface.kv")

class MyFirstWidget(BoxLayout):

    txt_inpt = ObjectProperty(None)


class MyApp(App):
    def build(self):
        return MyFirstWidget()

if __name__ == '__main__':
    MyApp().run()
