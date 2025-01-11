import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create input fields for item name and quantity
        self.item_name_input = TextInput(hint_text="Item Name", multiline=False, size_hint_y=None, height=30)
        self.item_quantity_input = TextInput(hint_text="Item Quantity", multiline=False, size_hint_y=None, height=30)
        self.new_quantity_input = TextInput(hint_text="New Quantity (For Update)", multiline=False, size_hint_y=None, height=30)

        # Create a search bar
        self.search_input = TextInput(hint_text="Search Item", multiline=False, size_hint_y=None, height=30)
        self.search_button = Button(text="Search", background_color=(0, 1, 0, 1))  # Green background
        self.search_button.bind(on_press=self.search_item)

        # Create a label for search result
        self.search_result_label = Label(text="Search Result: ", color=(0, 0, 0, 1), size_hint_y=None, height=30)

        # Buttons for adding, removing, updating, and viewing items
        add_button = Button(text="Add Item", background_color=(0, 1, 0, 1))  # Green background
        add_button.bind(on_press=self.add_item)

        remove_button = Button(text="Remove Item", background_color=(0, 1, 0, 1))  # Green background
        remove_button.bind(on_press=self.remove_item)

        update_button = Button(text="Update Item Quantity", background_color=(0, 1, 0, 1))  # Green background
        update_button.bind(on_press=self.update_item_quantity)

        view_button = Button(text="View Items", background_color=(0, 1, 0, 1))  # Green background
        view_button.bind(on_press=self.view_items)

        # Add widgets to the layout
        layout.add_widget(self.item_name_input)
        layout.add_widget(self.item_quantity_input)
        layout.add_widget(self.new_quantity_input)  # New input field for quantity update
        layout.add_widget(add_button)
        layout.add_widget(remove_button)
        layout.add_widget(update_button)
        layout.add_widget(view_button)

        # Add search bar and result label
        layout.add_widget(self.search_input)
        layout.add_widget(self.search_button)
        layout.add_widget(self.search_result_label)

        self.add_widget(layout)

        # Change background color of screen
        with self.canvas.before:
            Color(0, 0.8, 0, 1)  # Set a light green background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def add_item(self, instance):
        item_name = self.item_name_input.text
        item_quantity = self.item_quantity_input.text
        if item_name and item_quantity.isdigit():
            app = App.get_running_app()  # Access the ItemApp instance
            if item_name in app.items:
                app.items[item_name] += int(item_quantity)
            else:
                app.items[item_name] = int(item_quantity)
            self.item_name_input.text = ''
            self.item_quantity_input.text = ''
            app.save_items()

    def remove_item(self, instance):
        item_name = self.item_name_input.text
        app = App.get_running_app()  # Access the ItemApp instance
        if item_name in app.items:
            del app.items[item_name]
            self.item_name_input.text = ''
            app.save_items()

    def update_item_quantity(self, instance):
        item_name = self.item_name_input.text
        new_quantity = self.new_quantity_input.text
        if item_name and new_quantity.isdigit():
            app = App.get_running_app()  # Access the ItemApp instance
            if item_name in app.items:
                app.items[item_name] = int(new_quantity)  # Update the quantity
                self.new_quantity_input.text = ''  # Clear the new quantity input
                app.save_items()
            else:
                print(f"Item '{item_name}' does not exist.")
        else:
            print("Invalid input. Make sure the quantity is a number.")

    def view_items(self, instance):
        # Switch to the view items screen
        self.manager.current = 'view_items'

    def search_item(self, instance):
        search_term = self.search_input.text.strip().lower()  # Get the search term
        app = App.get_running_app()  # Access the ItemApp instance
        
        if search_term:
            # Search for the item in the dictionary (case insensitive)
            for item_name, quantity in app.items.items():
                if search_term in item_name.lower():
                    self.search_result_label.text = f"Search Result: {item_name} - Quantity: {quantity}"
                    return
            self.search_result_label.text = "Search Result: Item not found."
        else:
            self.search_result_label.text = "Search Result: Please enter an item name."


class ViewItemsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # ScrollView to show item table
        self.scrollview = ScrollView(size_hint=(1, None), height=400)
        self.grid_layout = GridLayout(cols=2, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        # Add table headers
        self.grid_layout.add_widget(Label(text="Item Name", bold=True, color=(0, 1, 0, 1)))  # Green color
        self.grid_layout.add_widget(Label(text="Quantity", bold=True, color=(0, 1, 0, 1)))  # Green color

        self.scrollview.add_widget(self.grid_layout)
        self.layout.add_widget(self.scrollview)

        back_button = Button(text="Back to Main Screen", background_color=(0, 1, 0, 1))  # Green background
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        # Update the table with items each time this screen is shown
        self.update_item_table()

    def update_item_table(self):
        # Clear the existing items in the table
        self.grid_layout.clear_widgets()

        # Add table headers again after clearing
        self.grid_layout.add_widget(Label(text="Item Name", bold=True, color=(0, 1, 0, 1)))  # Green color
        self.grid_layout.add_widget(Label(text="Quantity", bold=True, color=(0, 1, 0, 1)))  # Green color

        # Access the items from the app instance directly
        app = App.get_running_app()  # Access the ItemApp instance
        for item_name, quantity in app.items.items():
            self.grid_layout.add_widget(Label(text=item_name, color=(0, 1, 0, 1)))  # Green color
            self.grid_layout.add_widget(Label(text=str(quantity), color=(0, 1, 0, 1)))  # Green color

        # Adjust the height of the grid layout to fit the rows
        self.grid_layout.height = len(app.items) * 40

    def go_back(self, instance):
        # Switch back to the main screen
        self.manager.current = 'main_screen'


class ItemApp(App):
    def build(self):
        self.title = "HERBALIFE PRODUCTS"
        self.items = self.load_items()

        # Create ScreenManager to handle multiple screens
        screen_manager = ScreenManager()

        # Add the main screen and view items screen
        screen_manager.add_widget(MainScreen(name='main_screen'))
        screen_manager.add_widget(ViewItemsScreen(name='view_items'))

        return screen_manager

    def load_items(self):
        try:
            with open('items.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_items(self):
        with open('items.json', 'w') as file:
            json.dump(self.items, file)


if __name__ == '__main__':
    ItemApp().run()
