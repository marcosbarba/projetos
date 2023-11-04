from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.button import MDRoundFlatButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout


class ShoppingListApp(MDApp):
    def build(self):
        self.items = []  # Lista de itens
        self.total_cost = 0.0  # Variável para rastrear o custo total

        self.theme_cls.theme_style = "Light"  # Definindo o tema como Light

        layout = RelativeLayout()

        # Adicione a imagem de fundo
        background = Image(source='app.jpg')
        layout.add_widget(background)

        # Crie um layout de conteúdo que ficará acima da imagem de fundo
        content_layout = MDBoxLayout(orientation='vertical')

        # Caixa de entrada para adicionar itens
        input_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, None), adaptive_height=True)
        self.item_input = MDTextField(hint_text='Nome do item', size_hint_x=0.6)
        self.item_cost_input = MDTextField(hint_text='Custo do item', size_hint_x=0.2)
        add_button = MDRaisedButton(text='Adicionar item', size_hint_x=0.2)
        add_button.bind(on_release=self.add_item)

        # Defina a cor do texto para preto
        add_button.theme_text_color = "Primary"
        self.item_input.theme_text_color = "Primary"
        self.item_cost_input.theme_text_color = "Primary"

        input_layout.add_widget(self.item_input)
        input_layout.add_widget(self.item_cost_input)
        input_layout.add_widget(add_button)

        # Lista de itens
        self.scroll_view = ScrollView()
        self.item_list = MDBoxLayout(orientation='vertical', spacing=dp(5))

        # Rótulo para exibir o custo total
        self.total_label = MDLabel(
            text='Custo total: $0.00',
            size_hint=(1, None),  # Define o tamanho em relação ao layout pai
            height=dp(64)  # Altura maior para empurrar o rótulo para baixo
        )

        # Defina a cor do texto para preto
        self.total_label.theme_text_color = "Primary"

        self.total_label.height = dp(44)

        clear_button = MDRaisedButton(text='Limpar Tudo')
        clear_button.bind(on_release=self.clear_items)

        content_layout.add_widget(input_layout)
        content_layout.add_widget(self.scroll_view)
        self.scroll_view.add_widget(self.item_list)
        content_layout.add_widget(self.total_label)
        content_layout.add_widget(clear_button)

        layout.add_widget(content_layout)

        return layout

    def add_item(self, instance):
        item_text = self.item_input.text.strip()
        item_cost_text = self.item_cost_input.text.strip()

        if item_text and item_cost_text:
            try:
                item_cost_text = item_cost_text.replace(',', '.')
                item_cost = float(item_cost_text)
                self.total_cost += item_cost

                item_label = TwoLineAvatarIconListItem(
                    text=f'{item_text}',
                    secondary_text=f'Custo: $ {item_cost:.2f}'
                )

                delete_button = MDRoundFlatButton(
                    text="X",
                    size_hint=(None, None),
                    size=(dp(32), dp(32))
                )
                delete_button.bind(on_release=lambda btn: self.delete_item(item_label, item_cost))
                item_label.add_widget(delete_button)

                self.items.append((item_text, item_cost))

                self.item_list.add_widget(item_label)
                self.total_label.text = f'Custo total: $ {self.total_cost:.2f}'

                self.item_input.text = ''
                self.item_cost_input.text = ''

                self.save_data()
            except ValueError:
                self.show_error_message("Custo do item não é um número válido.")

    def delete_item(self, item_label, item_cost):
        self.total_cost -= item_cost
        item_text = item_label.text
        self.items = [(text, cost) for text, cost in self.items if text != item_text]
        self.item_list.remove_widget(item_label)
        self.total_label.text = f'Custo total: $ {self.total_cost:.2f}'
        self.save_data()

    def clear_items(self, instance):
        self.total_cost = 0.0
        self.items = []
        self.item_list.clear_widgets()
        self.total_label.text = 'Custo total: $0.00'

        self.save_data()

    def show_error_message(self, message):
        error_label = MDLabel(text=message, theme_text_color="Secondary", halign="center")
        self.item_list.add_widget(error_label)

    def save_data(self):
        with open('shopping_list.txt', 'w') as file:
            for item_text, item_cost in self.items:
                file.write(f"{item_text} - {item_cost:.2f}\n")


if __name__ == '__main__':
    ShoppingListApp().run()


class ShoppingListApp(MDApp):
    def build(self):
        self.items = []  # Lista de itens
        self.total_cost = 0.0  # Variável para rastrear o custo total

        self.theme_cls.theme_style = "Light"  # Definindo o tema como Light

        layout = MDBoxLayout(orientation='vertical')

        # Caixa de entrada para adicionar itens
        input_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, None), adaptive_height=True)
        self.item_input = MDTextField(hint_text='Nome do item', size_hint_x=0.6)
        self.item_cost_input = MDTextField(hint_text='Custo do item', size_hint_x=0.2)
        add_button = MDRaisedButton(text='Adicionar item', size_hint_x=0.2)
        add_button.bind(on_release=self.add_item)

        input_layout.add_widget(self.item_input)
        input_layout.add_widget(self.item_cost_input)
        input_layout.add_widget(add_button)

        # Lista de itens
        self.scroll_view = ScrollView()
        self.item_list = MDBoxLayout(orientation='vertical', spacing=dp(5))

        # Rótulo para exibir o custo total
        self.total_label = MDLabel(text='Custo total: $0.00')
        self.total_label.height = dp(44)

        clear_button = MDRaisedButton(text='Limpar Tudo')
        clear_button.bind(on_release=self.clear_items)

        layout.add_widget(input_layout)
        layout.add_widget(self.scroll_view)
        self.scroll_view.add_widget(self.item_list)
        layout.add_widget(self.total_label)
        layout.add_widget(clear_button)

        return layout

    def add_item(self, instance):
        item_text = self.item_input.text.strip()
        item_cost_text = self.item_cost_input.text.strip()

        if item_text and item_cost_text:
            try:
                item_cost_text = item_cost_text.replace(',', '.')
                item_cost = float(item_cost_text)
                self.total_cost += item_cost

                item_label = TwoLineAvatarIconListItem(
                    text=f'{item_text}',
                    secondary_text=f'Custo: $ {item_cost:.2f}'
                )

                delete_button = MDRoundFlatButton(
                    text="X",
                    size_hint=(None, None),
                    size=(dp(32), dp(32))
                )
                delete_button.bind(on_release=lambda btn: self.delete_item(item_label, item_cost))
                item_label.add_widget(delete_button)

                self.items.append((item_text, item_cost))

                self.item_list.add_widget(item_label)
                self.total_label.text = f'Custo total: $ {self.total_cost:.2f}'

                self.item_input.text = ''
                self.item_cost_input.text = ''

                self.save_data()
            except ValueError:
                self.show_error_message("Custo do item não é um número válido.")

    def delete_item(self, item_label, item_cost):
        self.total_cost -= item_cost
        item_text = item_label.text
        self.items = [(text, cost) for text, cost in self.items if text != item_text]
        self.item_list.remove_widget(item_label)
        self.total_label.text = f'Custo total: $ {self.total_cost:.2f}'
        self.save_data()

    def clear_items(self, instance):
        self.total_cost = 0.0
        self.items = []
        self.item_list.clear_widgets()
        self.total_label.text = 'Custo total: $0.00'

        self.save_data()

    def show_error_message(self, message):
        error_label = MDLabel(text=message, theme_text_color="Secondary", halign="center")
        self.item_list.add_widget(error_label)

    def save_data(self):
        with open('shopping_list.txt', 'w') as file:
            for item_text, item_cost in self.items:
                file.write(f"{item_text} - {item_cost:.2f}\n")


if __name__ == '__main__':
    ShoppingListApp().run()