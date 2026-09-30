import mysql.connector
import threading
import webbrowser
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Line
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior
 # from menu import PantallaConMenuContent, NewsContent, NewsDetailScreen, InternationalsContent, NationalsContent, AboutUsContent
 
from kivy.core.window import Window
 
# Establecer tamaño ventana simulando móvil (ejemplo 360x640)
Window.size = (360, 640)
 
 
class RoundedButton(Button):
    def __init__(self, **kwargs):
        self.bg_color = kwargs.pop('background_color', (0.3, 0.5, 0.8, 1))
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            Color(rgba=self.bg_color)
            self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
 
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
 
class WindowManager(ScreenManager):
    pass
 
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = RelativeLayout()
        try:
            background = Image(source='Imagenes/fondouno.png', allow_stretch=True, keep_ratio=False)
            root.add_widget(background)
        except:
            pass
        layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        try:
            logo = Image(source='logo.png', size_hint=(1, 10), size=(200, 200))
            layout.add_widget(logo)
        except:
            layout.add_widget(Label(text="ScholarNet", font_size=32))
        layout.add_widget(Label(text="Your dreams will be reality!", font_size=20))
        root.add_widget(layout)
        self.add_widget(root)
 
    def on_enter(self):
        Clock.schedule_once(self.go_to_login, 5)
 
    def go_to_login(self, *args):
        self.manager.current = "login"


# --- Inputs y botones redondeados ---
class RoundedInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
 
        # Quitar imagen de fondo por defecto
        self.background_normal = ''
        self.background_active = ''
 
        # Fondo blanco opaco con background_color
        self.background_color = (1, 1, 1, 1)  # blanco opaco
 
        # Texto negro
        self.foreground_color = (0, 0, 0, 1)
 
        # Hint gris oscuro
        self.hint_text_color = (0.3, 0.3, 0.3, 1)
 
        # Cursor negro
        self.cursor_color = (0, 0, 0, 1)
 
        self.padding = [15, 12, 15, 12]
        self.font_size = 16
 
        # Dibujar borde redondeado solo en canvas.before
        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1)  # color gris para el borde
            self.line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 8), width=1.5)
 
        self.bind(pos=self._update_line, size=self._update_line)
 
    def _update_line(self, *args):
        self.line.rounded_rectangle = (self.x, self.y, self.width, self.height, 8)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = RelativeLayout()
        background = Image(source='fondos.png', allow_stretch=True, keep_ratio=False)
        root.add_widget(background)
        layout = BoxLayout(orientation='vertical', spacing=15, padding=40)

        logo = Image(source='logo.png', size_hint=(None, None), size=(200, 200), pos_hint={'center_x':0.5})
        layout.add_widget(logo)

        layout.add_widget(Label(text='Welcome to ScholarNet', font_size=40))
        self.usuario = RoundedInput(hint_text="Username", multiline=False)
        layout.add_widget(self.usuario)
        self.clave = RoundedInput(hint_text="Password", password=True, multiline=False)
        layout.add_widget(self.clave)
        login_button = RoundedButton(
            text='Login',
            background_color=(118/225, 154/225, 199/255, 0.8),
            color=(1,1,1,1),
            height=40,
            font_size=14,
        )
        login_button.bind(on_press=self.validate_login)
        layout.add_widget(login_button)
        register_button = RoundedButton(
            text='Create Account',
            background_color=(118/225, 154/225, 199/255, 0.8),
            color=(1,1,1,1),
            height=40,
            font_size=14,
        )
        register_button.bind(on_press=self.go_to_register)
        layout.add_widget(register_button)
        root.add_widget(layout)
        self.add_widget(root)
 
    def validate_login(self, instance):
        threading.Thread(target=self._do_login).start()
 
    def _do_login(self):
        usuario = self.usuario.text
        clave = self.clave.text
        try:
            conexion = mysql.connector.connect(host='localhost', user='root', password='', database='kivy_login')
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (usuario, clave))
            resultado = cursor.fetchone()
            conexion.close()
            if resultado:
                Clock.schedule_once(lambda dt: self._login_success(usuario))
            else:
                Clock.schedule_once(lambda dt: self.show_popup("Error", "Invalid credentials"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_popup("Error", str(e)))
 
    def _login_success(self, usuario):
        self.manager.get_screen("usuario").nombre_usuario = usuario
        self.manager.current = "usuario"
 
    def show_popup(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4)).open()
 
    def go_to_register(self, instance):
        self.manager.current = "registro"
 
class RegistroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = RelativeLayout()
        background = Image(source='fondouno.png', allow_stretch=True, keep_ratio=False)
        root.add_widget(background)
        layout = BoxLayout(orientation='vertical', spacing=15, padding=40)

        logo = Image(source='logo.png', size_hint=(None, None), size=(200, 200), pos_hint={'center_x':0.5})
        layout.add_widget(logo)

        layout.add_widget(Label(text='📝 Register', font_size=44))
        self.usuario = RoundedInput(hint_text="New username", multiline=False)
        layout.add_widget(self.usuario)
        self.clave = RoundedInput(hint_text="New password", password=True, multiline=False)
        layout.add_widget(self.clave)
        create_button = RoundedButton(
            text='Create Account',
            background_color=(118/225, 154/225, 199/255, 0.8),
            color=(1,1,1,1),
            height=50,
        )
        create_button.bind(on_press=self.create_user)
        layout.add_widget(create_button)
        back_button = RoundedButton(
            text='Back to Login',
            background_color=(118/225, 154/225, 199/255, 0.8),
            color=(1,1,1,1),
            height=50,
        )
        back_button.bind(on_press=self.go_back_to_login)
        layout.add_widget(back_button)
        root.add_widget(layout)
        self.add_widget(root)
 
    def create_user(self, instance):
        usuario = self.usuario.text
        clave = self.clave.text
        try:
            conexion = mysql.connector.connect(host='localhost', user='root', password='', database='kivy_login')
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (usuario, clave))
            conexion.commit()
            conexion.close()
            self.show_popup("Success", "User registered successfully")
        except Exception as e:
            self.show_popup("Error", str(e))
 
    def show_popup(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4)).open()
 
    def go_back_to_login(self, instance):
        self.manager.current = "login"
 
 
class UsuarioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nombre_usuario = ""
 
        root = FloatLayout()
 
        try:
            fondo = Image(source='fondouno.png', allow_stretch=True, keep_ratio=False)
            root.add_widget(fondo)
        except:
            pass
 
        # Contenedor principal centrado
        self.layout = BoxLayout(
            orientation='vertical',
            spacing=25,
            padding=[20, 40, 20, 40],  # padding: left, top, right, bottom
            size_hint=(0.7, None),
            height=240,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
 
        self.label_bienvenida = Label(
            font_size=24,
            color=(0.2, 0.4, 0.6, 1),
            bold=True,
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=40,
        )
        self.label_bienvenida.bind(size=self.label_bienvenida.setter('text_size'))
        self.layout.add_widget(self.label_bienvenida)
 
        home_btn = RoundedButton(
            text='Choose Scholarship Type',
            size_hint=(1, None),
            height=50,
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=16,
        )
        home_btn.bind(on_press=lambda inst: setattr(self.manager, 'current', 'scholar_choice'))
        self.layout.add_widget(home_btn)
 
        logout_button = RoundedButton(
            text='Back',
            size_hint=(1, None),
            height=50,
            background_color=(0.6, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
            font_size=16,
        )
        logout_button.bind(on_press=self.logout)
        self.layout.add_widget(logout_button)
 
        root.add_widget(self.layout)
        self.add_widget(root)
 
    def on_pre_enter(self):
        self.label_bienvenida.text = f"🎉 Welcome to ScholarNet, {self.nombre_usuario}!"
 
    def logout(self, instance):
        self.manager.current = "login"
 
 
 
 
class ScholarshipChoiceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = RelativeLayout()
        try:
            fondo = Image(source='fondosye.png', allow_stretch=True, keep_ratio=False)
            root.add_widget(fondo)
        except:
            pass
 
        layout = BoxLayout(orientation='vertical', spacing=30, padding=[40, 120, 40, 40])  # espaciado y padding ajustado
 
        layout.add_widget(Label(
            text='[b]ScholarNet[/b]',
            markup=True,
            font_size=34,
            color=(0.2, 0.4, 0.6, 1),
            font_name='Garet-Heavy.ttf'
        ))
        layout.add_widget(Label(size_hint_y=None, height=80))
        layout.add_widget(Label(
            text='FIND YOUR PERFECT SCHOLARSHIP',
            font_size=16,
            color=(0, 0, 0, 1),
            font_name='Garet-Book.ttf'
        ))
 
        layout.add_widget(Label(
            text='WHAT TYPE OF SCHOLARSHIP WOULD YOU LIKE?',
            font_size=14,
            font_name='Garet-Book.ttf'
        ))
 
        btn_national = RoundedButton(
            text='NATIONAL',
            height=50,
            background_color=(0.4, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_name='Garet-Book.ttf'
        )
        btn_national.bind(on_press=lambda x: setattr(self.manager, 'current', 'nationals'))
        layout.add_widget(btn_national)
 
        btn_international = RoundedButton(
            text='INTERNATIONAL',
            height=50,
            background_color=(0.2, 0.4, 0.6, 1),
            color=(1, 1, 1, 1),
            font_name='Garet-Book.ttf'
        )
        btn_international.bind(on_press=lambda x: setattr(self.manager, 'current', 'internationals'))
        layout.add_widget(btn_international)
 
        back_btn = RoundedButton(
            text='← Back',
            height=50,
            background_color=(0.8, 0.8, 0.8, 1),
            color=(0, 0, 0, 1),
            font_name='Garet-Book.ttf'
        )
        back_btn.bind(on_press=lambda inst: setattr(self.manager, 'current', 'usuario'))
        layout.add_widget(back_btn)
 
        root.add_widget(layout)
        self.add_widget(root)
 
 
class CircularImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.allow_stretch = True
        self.keep_ratio = True
 
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.border_circle = Ellipse(pos=self.pos, size=self.size)
 
        self.bind(pos=self.update_circle, size=self.update_circle)
 
    def update_circle(self, *args):
        self.border_circle.pos = self.pos
        self.border_circle.size = self.size
 
class BotonRedondeado(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Transparente para usar canvas
        with self.canvas.before:
            Color(0.55, 0.70, 1, 1)  # Celeste
            self.rect = RoundedRectangle(radius=[15])
        self.bind(pos=self._update_rect, size=self._update_rect)
 
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
 
 
class BotonRedondeado(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        self.background_color = kwargs.pop('background_color', (0.7, 0.85, 1, 1))
        super().__init__(**kwargs)

        self.size_hint = kwargs.get('size_hint', (1, None))
        self.height = kwargs.get('height', dp(45))
        self.font_name = kwargs.get('font_name', 'Garet-Book.ttf')
        self.font_size = kwargs.get('font_size', 16)
        self.color = kwargs.get('color', (0, 0, 0, 1))
        self.halign = 'center'
        self.valign = 'middle'
        self.markup = True
        self.padding = (dp(10), dp(10))

        with self.canvas.before:
            self.color_instruction = Color(*self.background_color)
            self.rect = RoundedRectangle(radius=[dp(15)])

        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.bind(state=self.on_state_change)

    def update_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_state_change(self, instance, value):
        r, g, b, a = self.background_color
        if value == 'down':
            target_color = (r * 0.7, g * 0.7, b * 0.7, a)
        else:
            target_color = (r, g, b, a)

        Animation.cancel_all(self.color_instruction)
        anim = Animation(r=target_color[0], g=target_color[1], b=target_color[2], a=target_color[3], duration=0.2)
        anim.start(self.color_instruction)


class MenuLateral(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(orientation='vertical', size_hint=(None, 1), width=260, padding=dp(20), spacing=dp(15), **kwargs)
        self.screen_manager = screen_manager
        self.usuario = ""

        with self.canvas.before:
            Color(rgba=(0.85, 0.93, 0.98, 1))
            self.rect1 = Rectangle(pos=self.pos, size=(self.width, self.height / 2))
            Color(rgba=(1, 1, 1, 1))
            self.rect2 = Rectangle(pos=(self.x, self.y + self.height / 2), size=(self.width, self.height / 2))
            Color(0, 0, 0, 0.1)
            self.shadow = Rectangle(pos=(self.right - dp(8), self.y), size=(dp(8), self.height))

        self.bind(pos=self._update_rect, size=self._update_rect)

        self.add_widget(Label(
            text="ScholarNet",
            font_size=24,
            font_name="Garet-Heavy.ttf",
            size_hint=(1, None),
            height=dp(50),
            color=(0.1, 0.2, 0.35, 1),
            halign='center',
            valign='middle'
        ))

        self.nombre_usuario_label = Label(
            text="",
            font_size=16,
            font_name="Garet-Book.ttf",
            size_hint=(1, None),
            height=dp(30),
            color=(0.15, 0.3, 0.5, 1),
            halign='center',
            valign='middle'
        )
        self.add_widget(self.nombre_usuario_label)

        botones_info = [
            ("Experiences", "experiences"),
            ("News", "news"),
            ("Contact us", "contactus"),
            ("About us", "aboutus"),
            ("Back", "scholar_choice"),
        ]

        for texto, destino in botones_info:
            btn = BotonRedondeado(
                text=texto,
                height=dp(50),
                font_name="Garet-Book.ttf",
                font_size=18,
                background_color=(0.35, 0.65, 0.9, 1),
                color=(1, 1, 1, 1),
                on_release=lambda btn, destino=destino: self.cambiar_pantalla(destino)
            )
            self.add_widget(btn)

    def cambiar_pantalla(self, nombre_pantalla):
        self.screen_manager.current = nombre_pantalla

    def _update_rect(self, *args):
        self.rect1.pos = self.pos
        self.rect1.size = (self.width, self.height / 2)
        self.rect2.pos = (self.x, self.y + self.height / 2)
        self.rect2.size = (self.width, self.height / 2)
        self.shadow.pos = (self.right - dp(8), self.y)
        self.shadow.size = (dp(8), self.height)

    def set_usuario(self, nombre_usuario):
        self.usuario = nombre_usuario
        self.nombre_usuario_label.text = f"[b]{nombre_usuario}[/b]"
        self.nombre_usuario_label.markup = True

# ---------- CLASE MenuLateral ----------
# ---------------------- NewsScreen ----------------------
# ---------------------- NewsScreen ----------------------
# ---------------------- NewsScreen Decorada ----------------------
class NewsScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.sm = screen_manager

        # Fondo con imagen
        with self.canvas.before:
            self.bg_image = Rectangle(source="fondouno.png", pos=self.pos, size=Window.size)
        self.bind(pos=lambda w, p: setattr(self.bg_image, 'pos', p))
        self.bind(size=lambda w, s: setattr(self.bg_image, 'size', s))

        root_layout = FloatLayout()

        contenedor = BoxLayout(
            orientation='vertical',
            padding=[20, 60, 20, 20],
            spacing=15,
            size_hint=(1, 1)
        )

        # Título grande y moderno
        self.titulo = Label(
            text="[b]NEWS[/b]",
            markup=True,
            font_size=min(Window.width * 0.08, 36),
            size_hint=(1, None),
            height=70,
            halign='center',
            valign='middle',
            color=[0.05, 0.2, 0.5, 1]
        )
        self.titulo.bind(size=lambda lbl, *a: setattr(lbl, 'text_size', (lbl.width, None)))
        contenedor.add_widget(self.titulo)

        # Scroll para noticias
        scroll = ScrollView(size_hint=(1, 1))
        self.grid = BoxLayout(orientation='vertical', spacing=20, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        contenedor.add_widget(scroll)

        root_layout.add_widget(contenedor)
        self.add_widget(root_layout)

        # Ejemplo de noticias
        self.noticias = [
            {"img": "itcha.png", "titulo": "MINEDUCYT – ITCHA Scholarships",
             "resumen": "A new scholarship program for students across the country.",
             "contenido": "The Ministry of Education offers international scholarships covering tuition, accommodation, and transport."},
            {"img": "ues.png", "titulo": "Paid Scholarships – UES",
             "resumen": "A paid scholarship program for university students with good grades.",
             "contenido": "The University of El Salvador gives paid scholarships to students with a minimum grade average of 7.0 and full study load."},
        ]

        self.crear_tarjetas()
        Window.bind(on_resize=lambda *a: self.on_resize())

    def crear_tarjetas(self):
        self.grid.clear_widgets()
        for noticia in self.noticias:
            tarjeta = BoxLayout(
                orientation='vertical', spacing=10, size_hint_y=None, padding=[10]*4
            )

            # Fondo tarjeta moderno con sombra
            with tarjeta.canvas.before:
                Color(1, 1, 1, 0.95)
                rect = RoundedRectangle(pos=tarjeta.pos, size=tarjeta.size, radius=[20])
            tarjeta.bind(pos=lambda w, p, r=rect: setattr(r, "pos", p))
            tarjeta.bind(size=lambda w, s, r=rect: setattr(r, "size", s))

            # Hover/efecto "flotante"
            def on_touch_down(instance, touch):
                if instance.collide_point(*touch.pos):
                    Animation(y=instance.y + 5, d=0.1).start(instance)
            def on_touch_up(instance, touch):
                Animation(y=instance.y, d=0.1).start(instance)
            tarjeta.bind(on_touch_down=on_touch_down, on_touch_up=on_touch_up)

            # Imagen de noticia
            img = Image(
                source=noticia["img"],
                size_hint_y=None,
                height=180,
                allow_stretch=True,
                keep_ratio=False
            )
            tarjeta.add_widget(img)

            # Título
            lbl_titulo = Label(
                text=f"[b]{noticia['titulo']}[/b]",
                size_hint_y=None,
                halign='left',
                valign='middle',
                markup=True,
                font_size=min(Window.width * 0.055, 22),
                color=[0.05, 0.2, 0.5, 1]
            )
            lbl_titulo.bind(size=lambda lbl, *a: setattr(lbl, 'text_size', (lbl.width, None)))
            lbl_titulo.bind(texture_size=lambda lbl, size: setattr(lbl, 'height', lbl.texture_size[1]))
            tarjeta.add_widget(lbl_titulo)

            # Resumen
            lbl_resumen = Label(
                text=noticia['resumen'],
                size_hint_y=None,
                halign='left',
                valign='top',
                markup=True,
                font_size=min(Window.width * 0.045, 18),
                color=[0.1, 0.1, 0.1, 1]
            )
            lbl_resumen.bind(size=lambda lbl, *a: setattr(lbl, 'text_size', (lbl.width, None)))
            lbl_resumen.bind(texture_size=lambda lbl, size: setattr(lbl, 'height', lbl.texture_size[1]))
            tarjeta.add_widget(lbl_resumen)

            # Botón Read More moderno celeste
            btn_ver = RoundedButton(
                text="Read More",
                size_hint_y=None,
                height=45,
                font_size=16,
                background_color=(0.4, 0.7, 1, 1),  # Celeste bonito
                color=(1,1,1,1)
            )
            btn_ver.bind(on_press=lambda instance, n=noticia: self.ver_detalle(n))
            tarjeta.add_widget(btn_ver)

            # Ajustar altura
            def ajustar_altura(*args):
                total = img.height + lbl_titulo.height + lbl_resumen.height + btn_ver.height
                total += tarjeta.spacing*3 + tarjeta.padding[1] + tarjeta.padding[3]
                tarjeta.height = total

            lbl_resumen.bind(height=lambda *a: ajustar_altura())
            lbl_titulo.bind(height=lambda *a: ajustar_altura())
            ajustar_altura()

            self.grid.add_widget(tarjeta)

    def on_resize(self):
        self.titulo.font_size = min(Window.width * 0.08, 36)
        for tarjeta in self.grid.children:
            for widget in tarjeta.children:
                if isinstance(widget, Label):
                    widget.text_size = (widget.width, None)
                    widget.texture_update()

    def ver_detalle(self, noticia):
        # Animación al abrir detalle
        self.sm.get_screen("news_detail").update_content(noticia)
        self.sm.current = "news_detail"
        anim = Animation(opacity=0, duration=0)
        self.sm.get_screen("news_detail").opacity = 0
        Animation(opacity=1, d=0.3).start(self.sm.get_screen("news_detail"))


# ---------------------- DetailScreen Moderno ----------------------
class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fondo
        with self.canvas.before:
            self.bg_rect = Rectangle(source="fondos.png", pos=self.pos, size=Window.size)
        self.bind(pos=lambda w, p: setattr(self.bg_rect, 'pos', p))
        self.bind(size=lambda w, s: setattr(self.bg_rect, 'size', s))

        root_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        # Imagen arriba
        self.img = Image(
            size_hint_y=None,
            height=250,
            allow_stretch=True,
            keep_ratio=False
        )
        root_layout.add_widget(self.img)

        # Scroll con contenido
        self.info_box = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            padding=10
        )
        self.info_box.bind(minimum_height=self.info_box.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self.info_box)
        root_layout.add_widget(scroll)

        # Botón Back moderno celeste
        self.back_btn = RoundedButton(
            text="Back",
            size_hint=(0.3, None),
            height=50,
            background_color=(0.4,0.7,1,1),
            color=(1,1,1,1),
            font_size=16
        )
        self.back_btn.bind(on_press=self.volver)
        root_layout.add_widget(self.back_btn)

        self.add_widget(root_layout)

    def update_content(self, noticia):
        self.img.source = noticia["img"]

        self.info_box.clear_widgets()

        # Título
        lbl_titulo = Label(
            text=f"[b]{noticia['titulo']}[/b]",
            markup=True,
            font_size=22,
            color=[0.05,0.2,0.5,1],
            size_hint_y=None,
            halign='left',
            valign='middle'
        )
        lbl_titulo.text_size = (Window.width - 40, None)
        lbl_titulo.bind(texture_size=lambda lbl, size: setattr(lbl, 'height', lbl.texture_size[1]))
        self.info_box.add_widget(lbl_titulo)

        # Contenido
        lbl_contenido = Label(
            text=noticia["contenido"],
            markup=True,
            font_size=18,
            halign='left',
            valign='top',
            color=[0.1,0.1,0.1,1],
            size_hint_y=None
        )
        lbl_contenido.text_size = (Window.width - 40, None)
        lbl_contenido.bind(texture_size=lambda lbl, size: setattr(lbl, 'height', lbl.texture_size[1]))
        self.info_box.add_widget(lbl_contenido)

    def volver(self, instance):
        self.manager.current = "news"   
class ExperiencesScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        root = FloatLayout()

        # Fondo
        fondo = Image(source="fondos.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(fondo)

        # Overlay semitransparente
        with root.canvas:
            Color(0, 0, 0, 0.08)
            self.overlay = Rectangle(size=root.size, pos=root.pos)
        root.bind(size=lambda inst, val: setattr(self.overlay, 'size', val),
                  pos=lambda inst, val: setattr(self.overlay, 'pos', val))

        # Scrollable layout
        scroll = ScrollView(size_hint=(1,1))
        layout = BoxLayout(orientation='vertical', spacing=20, padding=[15, 20, 15, 20], size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Título
        titulo_label = Label(
            text='[b]EXPERIENCES[/b]',
            markup=True,
            font_size=28,
            font_name="Garet-Heavy.ttf",
            color=(0.1, 0.2, 0.35, 1),
            size_hint_y=None,
            height=50,
            halign='center',
            valign='middle'
        )
        titulo_label.text_size = (360 - 30, None)
        titulo_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        layout.add_widget(titulo_label)

        experiencias = [
            ("Kenia.jpg", "Experience Fundación ¡ADOC!", "Kenia Aguilar", "Graduated", "Centro ¡Supérate! ADOC\nProm 2018", 
             "Being a scholarship student at Centro Supérate ADOC was an amazing experience. It was a safe space to learn, express myself, and form friendships. Everything I gained is valuable for my future studies and career. The Supérate culture taught me that “impossible” doesn’t exist and inspired me to give back. I highly recommend this opportunity!"),
            ("cami.jpeg", "Experience Fundación ¡ADOC!", "Camila Arias", "Undergraduated", "Centro ¡Supérate! ADOC\nProm 2025",
             "¡Supérate! ADOC has played a key role in my academic and personal development. Through its programs, I have strengthened my skills, enhanced my confidence, and prepared myself to face future challenges. This scholarship has provided the guidance and tools I needed to be in a strong position today. I am truly grateful for the positive impact it has had on my life."),
            ("xav.jpeg", "Walton Experience", "Xavier Maldonado", "Undergraduated", "Walton International",
             "The Walton scholarship program completely changed my life. I have learned not only the parts of my career but also applied to different leadership positions that gave me first-hand experience, unforgettable friendships, and an academic formation of excellence. The campus is not very big nor very small, one can get to know all the students and it feels like a great community. Friendships become inseparable as they grow."),
            ("Kevin.jpeg", "Walton Experience", "Kevin Hernández", "Graduated", "Walton International",
             "This scholarship was a great experience because I had the opportunity to grow both academically and professionally. In addition, I was able to meet people from other cultures and backgrounds, which makes the experience of studying abroad truly amazing. A great opportunity!")
        ]

        for img, titulo, autor, degree, center, exp_text in experiencias:
            exp_box = BoxLayout(orientation='vertical', padding=15, spacing=8, size_hint_y=None)
            exp_box.height = 280

            # Fondo redondeado
            with exp_box.canvas.before:
                Color(0.93, 0.96, 1, 1)
                exp_box.rect = RoundedRectangle(size=exp_box.size, pos=exp_box.pos, radius=[20])
            exp_box.bind(size=lambda inst, val: setattr(inst.rect, 'size', val))
            exp_box.bind(pos=lambda inst, val: setattr(inst.rect, 'pos', val))

            # Imagen centrada en FloatLayout
            img_container = FloatLayout(size_hint_y=None, height=150)
            img_widget = Image(
                source=img,
                size_hint=(None, None),
                size=(330, 150),  # ajusta a tamaño tarjeta
                pos_hint={'center_x':0.5, 'center_y':0.5},
                allow_stretch=True,
                keep_ratio=True
            )
            img_container.add_widget(img_widget)
            exp_box.add_widget(img_container)

            # Texto centrado debajo de la imagen
            text_container = BoxLayout(orientation='vertical', spacing=4, size_hint=(1, None))
            text_container.bind(minimum_height=text_container.setter('height'))

            text_container.add_widget(Label(
                text=f"[b]{titulo}[/b]",
                markup=True,
                font_name="Garet-Book.ttf",
                font_size=16,
                color=(0.05, 0.1, 0.3, 1),
                size_hint_y=None,
                height=22,
                halign='center',
                valign='middle',
                text_size=(360 - 60, None)
            ))
            text_container.add_widget(Label(
                text=f"{autor} | {degree}",
                font_name="Garet-Book.ttf",
                font_size=14,
                color=(0.2, 0.2, 0.25, 1),
                size_hint_y=None,
                height=20,
                halign='center',
                valign='middle',
                text_size=(360 - 60, None)
            ))
            text_container.add_widget(Label(
                text=center,
                font_name="Garet-Book.ttf",
                font_size=14,
                color=(0.2, 0.2, 0.25, 1),
                size_hint_y=None,
                height=20,
                halign='center',
                valign='middle',
                text_size=(360 - 60, None)
            ))

            exp_box.add_widget(text_container)

            # Botón View
            view_btn = RoundedButton(
                text="View",
                size_hint=(None, None),
                size=(120, 40),
                background_color=(0.35, 0.7, 1, 1),
                color=(1, 1, 1, 1),
                pos_hint={'center_x': 0.5},
                font_name="Garet-Book.ttf"
            )
            view_btn.bind(on_release=lambda x, d=(img, titulo, autor, degree, center, exp_text): self.open_detail(*d))
            exp_box.add_widget(view_btn)

            layout.add_widget(exp_box)

        scroll.add_widget(layout)
        root.add_widget(scroll)
        self.add_widget(root)

    def open_detail(self, img, titulo, autor, degree, center, exp_text):
        detail_screen = self.sm.get_screen('experience_detail')
        detail_screen.update_content(img, titulo, degree, center, exp_text)
        self.sm.current = 'experience_detail'



class ExperienceDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()

        fondo = Image(source="fondos.png", allow_stretch=True, keep_ratio=False)
        root.add_widget(fondo)

        scroll = ScrollView(size_hint=(1, 1))
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Tarjeta con sombra
        card = BoxLayout(
            orientation='vertical',
            padding=15,
            spacing=10,
            size_hint_y=None,
            size_hint_x=0.95,
            pos_hint={"center_x": 0.5}
        )
        card.bind(minimum_height=card.setter('height'))

        with card.canvas.before:
            # Sombra suave
            Color(0, 0, 0, 0.06)
            self.shadow = RoundedRectangle(pos=(card.pos[0]+4, card.pos[1]-4), size=(card.size[0], card.size[1]), radius=[25])
            # Fondo tarjeta
            Color(0.95, 0.97, 1, 1)
            self.rect_bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[25])
        card.bind(pos=self._update_rect_bg, size=self._update_rect_bg)

        # Imagen centrada
        self.img_widget = Image(
            size_hint=(None, None),
            size=(220, 220),
            pos_hint={"center_x": 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        card.add_widget(self.img_widget)

        # Textos centrados
        self.name_label = Label(markup=True, font_size=20, color=(0.05, 0.1, 0.3, 1),
                                size_hint_y=None, height=28, halign='center', text_size=(340, None),
                                font_name="Garet-Book.ttf")
        card.add_widget(self.name_label)

        self.degree_label = Label(font_size=16, color=(0.1, 0.1, 0.2, 1), size_hint_y=None, height=24,
                                  halign='center', text_size=(340, None), font_name="Garet-Book.ttf")
        card.add_widget(self.degree_label)

        self.center_label = Label(font_size=16, color=(0.1, 0.1, 0.2, 1), size_hint_y=None, height=24,
                                  halign='center', text_size=(340, None), font_name="Garet-Book.ttf")
        card.add_widget(self.center_label)

        # Texto largo de la experiencia
        self.exp_label = Label(font_size=14, font_name="Garet-Book.ttf", color=(0.05, 0.05, 0.2, 1),
                               text_size=(340, None), halign="justify", valign="top", size_hint_y=None)
        self.exp_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        card.add_widget(self.exp_label)

        layout.add_widget(card)

        # Botón Back
        back_btn = RoundedButton(
            text="Back",
            size_hint=(None, None),
            size=(120, 40),
            pos_hint={"center_x": 0.5},
            background_color=(0.4, 0.7, 1, 1),
            color=(1, 1, 1, 1),
            font_name="Garet-Book.ttf"
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'experiences'))
        layout.add_widget(back_btn)

        scroll.add_widget(layout)
        root.add_widget(scroll)
        self.add_widget(root)

    def _update_rect_bg(self, *args):
        self.rect_bg.pos = self.children[0].children[0].pos
        self.rect_bg.size = self.children[0].children[0].size
        self.shadow.pos = (self.rect_bg.pos[0]+4, self.rect_bg.pos[1]-4)
        self.shadow.size = self.rect_bg.size

    def update_content(self, img, name, degree, center, exp_text):
        self.img_widget.source = img
        self.name_label.text = f"[b]{name}[/b]"
        self.degree_label.text = degree
        self.center_label.text = center
        self.exp_label.text = exp_text

class ContactanosScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
 
        # Fondo decorativo
        fondo = Image(source='fondouno.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(fondo)
 
        # Contenedor principal
        layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            padding=30,
            size_hint=(.95, .9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(layout)
 
        # Título
        layout.add_widget(Label(
            text='[b]CONTACT US[/b]',
            markup=True,
            font_size=28,
            font_name='Garet-Heavy.ttf',
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=70,
            halign='center',
            valign='middle'
        ))
 
        # Cuadro informativo
        info_box = self.cuadro_info(
            "Feel free to reach out to us at any time.\nWe'll get back to you as soon as possible 💬"
        )
        layout.add_widget(info_box)
 
        # Sección de contactos
        layout.add_widget(self.contacto_con_icono("telefono.png", "7681 - 8427"))
        layout.add_widget(self.contacto_con_icono("instagram.png", "scholarnet_sv"))
        layout.add_widget(self.contacto_con_icono("facebook.png", "scholarnet_sv"))
 
        # Botón Back
        layout.add_widget(Button(
            text='Back',
            size_hint=(None, None),
            size=(160, 50),
            background_color=(0.7, 0.85, 1, 1),
            color=(0, 0, 0, 1),
            font_size=16,
            font_name='Garet-Book.ttf',
            background_normal='',
            pos_hint={'center_x': 0.5},
            on_release=self.back_to_menu
        ))
 
    def cuadro_info(self, texto):
        box = BoxLayout(size_hint=(1, None), height=100, padding=15)
 
        with box.canvas.before:
            # Sombra
            Color(0, 0, 0, 0.08)
            shadow = RoundedRectangle(radius=[10], pos=(box.x + 2, box.y - 2), size=box.size)
            # Fondo suave
            Color(0.8, 0.9, 1, 1)
            rect = RoundedRectangle(radius=[10], pos=box.pos, size=box.size)
 
        def update_rects(*args):
            rect.pos = box.pos
            rect.size = box.size
            shadow.pos = (box.x + 2, box.y - 2)
            shadow.size = box.size
 
        box.bind(pos=update_rects, size=update_rects)
 
        label = Label(
            text=texto,
            halign='center',
            valign='middle',
            font_size=14,
            font_name='Garet-Book.ttf',
            color=(0, 0, 0, 1)
        )
        label.bind(size=label.setter('text_size'))
        box.add_widget(label)
 
        return box
 
    def contacto_con_icono(self, icono, texto):
        box = BoxLayout(size_hint=(1, None), height=50, spacing=10)
        box.add_widget(Image(source=icono, size_hint=(None, None), size=(50, 50)))
 
        box.add_widget(Button(
            text=texto,
            background_color=(0.85, 0.95, 1, 1),
            color=(0, 0, 0, 1),
            font_size=16,
            font_name='Garet-Book.ttf',
            background_normal='',
            size_hint=(1, None),
            height=50,
            border=(10, 10, 10, 10)
        ))
 
        return box
 
    def back_to_menu(self, instance):
        App.get_running_app().root.current = 'menu_principal'
 
class FondoCeleste(BoxLayout):
    def __init__(self, contenido_texto, font_size=14, **kwargs):
        super().__init__(orientation='vertical', padding=10, size_hint_y=None, **kwargs)
        self.bind(minimum_height=self.setter('height'))
 
        with self.canvas.before:
            Color(0.7, 0.9, 1, 1)  # Celeste suave
            self.rect = RoundedRectangle(radius=[10], pos=self.pos, size=self.size)
        self.bind(pos=self.actualizar_rect, size=self.actualizar_rect)
 
        self.label = Label(
            text=contenido_texto,
            font_size=font_size,
            font_name='Garet-Book.ttf',
            halign='center',
            valign='middle',
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None
        )
 
        # Ligamos el tamaño del texto al ancho del fondo
        self.bind(width=lambda inst, val: self.label.setter("text_size")(self.label, (val - 20, None)))
 
        # Ajusta altura dinámica
        self.label.bind(texture_size=self.ajustar_altura)
        self.add_widget(self.label)
 
    def actualizar_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
 
    def ajustar_altura(self, instance, value):
        instance.height = instance.texture_size[1] + 20
        self.height = instance.height + 20
 
class AboutUsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
 
        layout = FloatLayout()
 
        # Fondo decorativo general
        fondo = Image(source="fondos.png", allow_stretch=True, keep_ratio=False)
        layout.add_widget(fondo)
 
        # Scroll para todo el contenido
        scroll = ScrollView(size_hint=(1, 1))
        contenido = BoxLayout(
            orientation='vertical',
            padding=[20, 40, 20, 20],
            spacing=20,
            size_hint_y=None
        )
        contenido.bind(minimum_height=contenido.setter('height'))
 
        # Título principal
        titulo = Label(
            text='[b]ABOUT US[/b]',
            markup=True,
            font_size=24,
            font_name='Garet-Heavy.ttf',
            size_hint_y=None,
            height=40,
            color=(0.1, 0.1, 0.1, 1)
        )
        contenido.add_widget(titulo)
 
        # Mission
        contenido.add_widget(Label(
            text='[b]Mission[/b]',
            markup=True,
            font_size=18,
            font_name='Garet-Heavy.ttf',
            size_hint_y=None,
            height=30,
            color=(0.2, 0.2, 0.4, 1)
        ))
        contenido.add_widget(FondoCeleste(
            "The mission of our app is to provide access to complete, up-to-date and reliable information about scholarships and student aid, facilitating the search for opportunities to achieve their academic goals."
        ))
 
        # Vision
        contenido.add_widget(Label(
            text='[b]Vision[/b]',
            markup=True,
            font_size=18,
            font_name='Garet-Heavy.ttf',
            size_hint_y=None,
            height=30,
            color=(0.2, 0.2, 0.4, 1)
        ))
        contenido.add_widget(FondoCeleste(
            "To be the leading platform for the promotion of educational opportunities, recognized for its commitment to helping students access scholarships and grants."
        ))
 
        # Values
        contenido.add_widget(Label(
            text='[b]Values[/b]',
            markup=True,
            font_size=18,
            font_name='Garet-Heavy.ttf',
            size_hint_y=None,
            height=30,
            color=(0.2, 0.2, 0.4, 1)
        ))
 
        valores = ["INCLUSIVE", "ENGAGEMENT", "UNIVERSAL", "INNOVATION"]
        for val in valores:
            contenido.add_widget(FondoCeleste(val, font_size=14))
 
        scroll.add_widget(contenido)
        layout.add_widget(scroll)
 
        self.add_widget(layout)

class SocialButtons(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 20
        self.padding = [20, 10]
        self.size_hint_y = None
        self.height = 70

        # Botón de Facebook
        fb_btn = Button(
            background_normal='facebook_icon.png',  # Icono
            background_down='facebook_icon.png',
            size_hint=(None, None),
            size=(60, 60),
            border=(0, 0, 0, 0)
        )
        fb_btn.bind(on_press=lambda x: print("Facebook presionado"))

        # Botón de Instagram
        ig_btn = Button(
            background_normal='instagram_icon.png',  # Icono
            background_down='instagram_icon.png',
            size_hint=(None, None),
            size=(60, 60),
            border=(0, 0, 0, 0)
        )
        ig_btn.bind(on_press=lambda x: print("Instagram presionado"))

        self.add_widget(fb_btn)
        self.add_widget(ig_btn)
 
class IconButton(ButtonBehavior, Image):
    def __init__(self, source, url, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.url = url
        self.allow_stretch = True
        self.keep_ratio = True
        self.size_hint = (None, None)
        self.size = (40, 40)
    
    def on_release(self):
        webbrowser.open(self.url)


class NationalsContent(ScrollView):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.do_scroll_x = False

        # Container principal
        container = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(18), size_hint_y=None)
        container.bind(minimum_height=container.setter('height'))

        # Fondo con imagen
        with container.canvas.before:
            self.bg = Rectangle(source='fondos.png', pos=container.pos, size=container.size)
        container.bind(pos=lambda w, *a: setattr(self.bg, 'pos', w.pos))
        container.bind(size=lambda w, *a: setattr(self.bg, 'size', w.size))

        # Título
        titulo = Label(
            text="NATIONAL SCHOLARSHIPS",
            font_size=24,
            font_name="Garet-Heavy",
            halign="center",
            color=[0, 0, 0, 1],
            size_hint=(1, None),
            height=dp(40)
        )
        titulo.bind(size=lambda w, *a: setattr(titulo, "text_size", (w.width, None)))
        container.add_widget(titulo)

        # Imagen
        container.add_widget(Image(source="graduado.jpeg", size_hint=(1, None), height=dp(180)))

        # Descripción
        descripcion = Label(
            text=("Explore national scholarships designed to support talented students in your country. "
                  "Take advantage of these opportunities to advance your academic career."),
            font_size=14,
            font_name="Garet-Book",
            halign="center",
            valign="middle",
            color=[0, 0, 0, 1],
            size_hint=(1, None)
        )
        descripcion.bind(size=lambda w, *a: setattr(descripcion, "text_size", (w.width, None)))
        descripcion.bind(texture_size=lambda l, ts: setattr(l, "height", ts[1] + dp(10)))
        container.add_widget(descripcion)

        # Lista de becas
        self.becas_nacionales = [
    {
        "nombre": "Fundación Gloria Kriete",
        "imagen": "kriete.png",
        "titulo": "Fundación Gloria Kriete Scholarship",
        "descripcion": "Scholarships and programs that support Salvadoran youth through education, training, and social development initiatives.",
        "fecha": "August 31, 2025",
        "requisitos": [
            "Be a Salvadoran citizen",
            "Meet the specific criteria of the selected program",
            "Provide academic records and identification documents",
            "Participate in the selection process"
        ],
        "periodo": "May – July 2025",
        "inicio": "January 2026",
        "link": "https://fundaciongloriakriete.org/en_us/"
    },
    {
        "nombre": "Centro ¡Supérate! ADOC",
        "imagen": "adoc.png",
        "titulo": "¡Supérate! ADOC",
        "descripcion": "Academic and values-based training for students with limited resources.",
        "fecha": "October 5, 2025",
        "requisitos": [
            "Be currently in 9th–11th grade at a Salvadoran school",
            "Maintain GPA ≥ 8.0 (on 10-scale grading)",
            "Pass admission exam and personal interview",
            "Demonstrate leadership and community involvement"
        ],
        "periodo": "July – September 2025",
        "inicio": "January 2026",
        "link": "https://superate.org.sv/"
    },
    {
        "nombre": "Programa Jóvenes Talento UES",
        "imagen": "jovenes talento.png",
        "titulo": "Jóvenes Talento UES",
        "descripcion": "Scholarship for outstanding students to develop academic and research skills in STEM areas.",
        "fecha": "July 20, 2025",
        "requisitos": [
            "High school graduate with GPA ≥ 4.0 (on 5.0 scale)",
            "Accepted to UES pre-university program or academic test",
            "Provide a research proposal or portfolio",
            "Interview by selection committee"
        ],
        "periodo": "May – June 2025",
        "inicio": "September 2025",
        "link": "https://www.jovenestalento.edu.sv/"
    },
    {
        "nombre": "Beca Ministerio de Educación",
        "imagen": "ministerio.png",
        "titulo": "MINED Scholarship",
        "descripcion": "Financial aid for low-income students to pursue higher education in El Salvador.",
        "fecha": "August 10, 2025",
        "requisitos": [
            "Student enrolled in public high school final year",
            "Family income below the national poverty line",
            "Have a GPA ≥ 7.5 (on 10-scale grading)",
            "Submit household income documentation"
        ],
        "periodo": "May – July 2025",
        "inicio": "September 2025",
        "link": "https://portal.esco.gob.sv/es-ES/0/PUB/Home/Becas_Show?nav=AeAE16JK&niv=1"
    },
    {
        "nombre": "Beca Empresarial AVIANCA",
        "imagen": "avianca.png",
        "titulo": "Avianca Academic Excellence",
        "descripcion": "Supports top students in tourism and aeronautical studies.",
        "fecha": "September 1, 2025",
        "requisitos": [
            "Enroll in tourism or aeronautics program",
            "GPA ≥ 3.7 (on 4.0 scale)",
            "Submit motivational essay",
            "Demonstrate leadership potential"
        ],
        "periodo": "June – August 2025",
        "inicio": "January 2026",
        "link": "https://jobs.avianca.com/content/Becas-Mujeres-Pilotos/?locale=es_ES"
    }
]

        for beca in self.becas_nacionales:
            container.add_widget(self.crear_beca_card(beca))

        # Sección Our Team
        about_title = Label(
            text="Our Team",
            font_size=20,
            font_name="Garet-Heavy",
            halign="center",
            color=[0, 0, 0, 1],
            size_hint=(1, None),
            height=dp(40)
        )
        about_title.bind(size=lambda w, *a: setattr(about_title, "text_size", (w.width, None)))
        container.add_widget(about_title)

        container.add_widget(Image(source="Media.jpeg", size_hint=(1, None), height=dp(180)))

        about_desc = Label(
            text=("We are Scholarnet, committed to helping students find the best national and international "
                  "scholarship opportunities to achieve their academic dreams."),
            font_size=14,
            font_name="Garet-Book",
            halign="center",
            valign="middle",
            color=[0, 0, 0, 1],
            size_hint=(1, None)
        )
        about_desc.bind(size=lambda w, *a: setattr(about_desc, "text_size", (w.width, None)))
        about_desc.bind(texture_size=lambda l, ts: setattr(l, "height", ts[1] + dp(10)))
        container.add_widget(about_desc)

        # Redes centradas
        social_layout = BoxLayout(orientation='horizontal', spacing=dp(16), size_hint=(None, None))
        social_layout.width = dp(120)
        social_layout.height = dp(50)
        social_layout.pos_hint = {"center_x": 0.5}
        fb_icon = IconButton(source="facebook.png", url="https://facebook.com/TuPagina")
        ig_icon = IconButton(source="instagram.png", url="https://instagram.com/TuPagina")
        social_layout.add_widget(fb_icon)
        social_layout.add_widget(ig_icon)
        container.add_widget(social_layout)

        self.add_widget(container)

    def crear_beca_card(self, beca):
        card = BoxLayout(orientation='horizontal', size_hint=(1, None), padding=dp(14), spacing=dp(14))
        card.bind(minimum_height=card.setter('height'))

        with card.canvas.before:
            Color(0, 0, 0, 0.08)
            shadow_rect = RoundedRectangle(radius=[18], pos=(card.x, card.y - dp(2)), size=(card.width, card.height))
            Color(1, 1, 1, 1)
            bg_rect = RoundedRectangle(radius=[16], pos=card.pos, size=card.size)

        def _update_rects(instance, value):
            bg_rect.pos = instance.pos
            bg_rect.size = instance.size
            shadow_rect.pos = (instance.pos[0], instance.pos[1] - dp(2))
            shadow_rect.size = instance.size

        card.bind(pos=_update_rects, size=_update_rects)

        img = Image(source=beca["imagen"], size_hint=(None, None), allow_stretch=True, keep_ratio=True)
        img.size = (dp(110), dp(110))
        card.add_widget(img)

        info = BoxLayout(orientation='vertical', spacing=dp(6), size_hint=(1, None))
        info.bind(minimum_height=info.setter('height'))

        nombre = Label(text=beca["nombre"], font_size=16, font_name="Garet-Heavy", color=[0, 0, 0, 1], size_hint=(1, None))
        nombre.bind(size=lambda w, *a: setattr(nombre, "text_size", (w.width, None)))
        nombre.bind(texture_size=lambda l, ts: setattr(l, "height", ts[1]))
        info.add_widget(nombre)

        desc = Label(
            text=beca["descripcion"],
            font_size=14,
            font_name="Garet-Book",
            color=[0, 0, 0, 1],
            halign="left",
            valign="top",
            size_hint=(1, None)
        )
        desc.bind(size=lambda w, *a: setattr(desc, "text_size", (w.width, None)))
        desc.bind(texture_size=lambda l, ts: setattr(l, "height", ts[1]))
        info.add_widget(desc)

        actions = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(40))
        actions.add_widget(Label(size_hint_x=1))

        view_btn = Button(
            text="View",
            size_hint=(None, None),
            size=(dp(92), dp(36)),
            background_color=(0.4, 0.7, 1, 1),
            color=(1, 1, 1, 1),
            font_name="Garet-Book",
            background_normal='',
            border=(18, 18, 18, 18)  # Botón redondeado
        )
        view_btn.bind(on_release=lambda x, b=beca: self.ir_a_detalle(b))
        actions.add_widget(view_btn)

        info.add_widget(actions)
        card.add_widget(info)

        def _sync_height(*_):
            desired = max(dp(120), img.height + dp(20), nombre.height + desc.height + actions.height + dp(10))
            card.height = desired

        for w in (nombre, desc):
            w.bind(height=lambda *_: _sync_height())
            w.bind(texture_size=lambda *_: _sync_height())

        actions.bind(height=lambda *_: _sync_height())
        img.bind(size=lambda *_: _sync_height())
        _sync_height()

        return card

    def ir_a_detalle(self, beca):
        detalle = self.screen_manager.get_screen("beca_detalle")
        detalle.mostrar_detalle(
            titulo=beca["titulo"],
            descripcion=beca["descripcion"],
            fecha=beca["fecha"],
            requisitos=beca["requisitos"],
            periodo=beca["periodo"],
            inicio=beca["inicio"],
            link=beca["link"],
            imagen=beca["imagen"],
            origen="nationals"
        )
        self.screen_manager.current = "beca_detalle"


# =========================
class InternationalsScreen(ScrollView):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.do_scroll_x = False

        # Container principal
        container = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(18), size_hint_y=None)
        container.bind(minimum_height=container.setter('height'))

        # Fondo con imagen
        with container.canvas.before:
            self.bg = Rectangle(source='fondos.png', pos=container.pos, size=container.size)
        container.bind(pos=lambda w, *a: setattr(self.bg, 'pos', w.pos))
        container.bind(size=lambda w, *a: setattr(self.bg, 'size', w.size))

        # Título
        titulo = Label(
            text="INTERNATIONAL SCHOLARSHIPS",
            font_size=24,
            font_name="Garet-Heavy",
            halign="center",
            color=[0, 0, 0, 1],
            size_hint=(1, None),
            height=dp(40)
        )
        titulo.bind(size=lambda w, *a: setattr(titulo, "text_size", (w.width, None)))
        container.add_widget(titulo)

        # Imagen
        container.add_widget(Image(source="mundo.jpeg", size_hint=(1, None), height=dp(180)))

        # Descripción
        descripcion = Label(
            text=("Explore scholarships from around the world designed to help talented students like you study abroad, "
                  "gain global experiences, and access world-class education."),
            font_size=14,
            font_name="Garet-Book",
            halign="center",
            valign="middle",
            color=[0, 0, 0, 1],
            size_hint=(1, None)
        )
        descripcion.bind(size=lambda w, *a: setattr(descripcion, "text_size", (w.width, None)))
        descripcion.bind(texture_size=lambda l, ts: setattr(l, "height", ts[1] + dp(8)))
        container.add_widget(descripcion)

        # Lista de becas
        self.becas_internacionales = [
    {
        "nombre": "University of Salamanca",
        "imagen": "salamanca.png",
        "titulo": "University of Salamanca Scholarship",
        "descripcion": "Scholarships for Latin American students to pursue master's or doctoral studies in Spain.",
        "fecha": "August 31, 2025",
        "requisitos": [
            "Bachelor’s degree with GPA ≥ 8.0 (on 10-scale)",
            "Spanish proficiency (DELE B2 or equivalent)",
            "Research proposal or statement of purpose",
            "Two academic recommendation letters"
        ],
        "periodo": "April – July 2025",
        "inicio": "October 2025",
        "link": "https://www.usal.es/"
    },
    {
        "nombre": "Walton International Scholarship",
        "imagen": "walton.png",
        "titulo": "Walton Scholarship",
        "descripcion": "Full scholarships for Central American students to study at universities in the United States.",
        "fecha": "October 1, 2025",
        "requisitos": [
            "Completed undergraduate studies with GPA ≥ 3.0 (on 4.0 scale)",
            "TOEFL ≥ 90 or IELTS ≥ 6.5",
            "Leadership in community or university",
            "Submit project or thesis summary"
        ],
        "periodo": "May – August 2025",
        "inicio": "Fall 2026",
        "link": "https://www.wispweb.org/"
    },
    {
        "nombre": "Chevening Scholarship",
        "imagen": "chevening.png",
        "titulo": "Chevening Scholarship",
        "descripcion": "UK government scholarships for future leaders to study a master's degree in the United Kingdom.",
        "fecha": "November 7, 2025",
        "requisitos": [
            "Undergraduate degree with first-class or upper second-class honors",
            "Minimum two years of work experience",
            "Leadership potential, as demonstrated in essays",
            "References and English language proficiency"
        ],
        "periodo": "August – October 2025",
        "inicio": "September 2026",
        "link": "https://www.chevening.org/scholarships/"
    },
    {
        "nombre": "Erasmus+ Program",
        "imagen": "erasmus.png",
        "titulo": "Erasmus+ Scholarship",
        "descripcion": "Funding for students to study in various European countries through exchange programs.",
        "fecha": "June 15, 2025",
        "requisitos": [
            "Enrolled in an accredited university program in home country",
            "Nomination by home university",
            "Language proficiency depending on host country",
            "Academic transcript"
        ],
        "periodo": "January – April 2025",
        "inicio": "September 2025",
        "link": "https://erasmus-plus.ec.europa.eu/opportunities/opportunities-for-individuals/students/erasmus-mundus-joint-masters"
    },
    {
        "nombre": "DAAD Scholarship",
        "imagen": "daad.png",
        "titulo": "DAAD Scholarship",
        "descripcion": "Scholarships for international students to study or research in Germany.",
        "fecha": "October 31, 2025",
        "requisitos": [
            "University degree with top-class rankings",
            "German or English proficiency (depending on program)",
            "Research proposal or academic portfolio",
            "Two academic references"
        ],
        "periodo": "May – September 2025",
        "inicio": "April 2026",
        "link": "https://www.daad.de/en/studying-in-germany/scholarships/"
    }
] 

        for beca in self.becas_internacionales:
            container.add_widget(self.crear_beca_card(beca))

        # Sección Our Team
        about_title = Label(
            text="Our Team",
            font_size=20,
            font_name="Garet-Heavy",
            halign="center",
            color=[0, 0, 0, 1],
            size_hint=(1, None),
            height=dp(40)
        )
        about_title.bind(size=lambda w, *a: setattr(about_title, "text_size", (w.width, None)))
        container.add_widget(about_title)

        container.add_widget(Image(source="Media.jpeg", size_hint=(1, None), height=dp(180)))

        about_desc = Label(
            text=("We are Scholarnet, committed to helping students find the best national and international "
                  "scholarship opportunities to achieve their academic dreams."),
            font_size=14,
            font_name="Garet-Book",
            halign="center",
            valign="middle",
            color=[0, 0, 0, 1],
            size_hint=(1, None)
        )
        about_desc.bind(size=lambda w, *a: setattr(about_desc, "text_size", (w.width, None)))
        about_desc.bind(texture_size=lambda l, ts: setattr(l, "height", ts[1] + dp(10)))
        container.add_widget(about_desc)

        # Redes centradas
        social_layout = BoxLayout(orientation='horizontal', spacing=dp(16), size_hint=(None, None))
        social_layout.width = dp(120)
        social_layout.height = dp(50)
        social_layout.pos_hint = {"center_x": 0.5}
        fb_icon = IconButton(source="facebook.png", url="https://facebook.com/TuPagina")
        ig_icon = IconButton(source="instagram.png", url="https://www.instagram.com/scholarnet.sv/")
        social_layout.add_widget(fb_icon)
        social_layout.add_widget(ig_icon)
        container.add_widget(social_layout)

        self.add_widget(container)

    def crear_beca_card(self, beca):
        card = BoxLayout(orientation='horizontal', size_hint=(1, None), padding=dp(14), spacing=dp(14))
        card.bind(minimum_height=card.setter('height'))

        with card.canvas.before:
            Color(0, 0, 0, 0.08)
            shadow_rect = RoundedRectangle(radius=[18], pos=(card.x, card.y - dp(2)), size=(card.width, card.height))
            Color(1, 1, 1, 1)
            bg_rect = RoundedRectangle(radius=[16], pos=card.pos, size=card.size)

        def _update_rects(instance, value):
            bg_rect.pos = instance.pos
            bg_rect.size = instance.size
            shadow_rect.pos = (instance.pos[0], instance.pos[1] - dp(2))
            shadow_rect.size = instance.size

        card.bind(pos=_update_rects, size=_update_rects)

        img = Image(source=beca["imagen"], size_hint=(None, None), allow_stretch=True, keep_ratio=True)
        img.size = (dp(110), dp(110))
        card.add_widget(img)

        info = BoxLayout(orientation='vertical', spacing=dp(6), size_hint=(1, None))
        info.bind(minimum_height=info.setter('height'))

        nombre = Label(text=beca["nombre"], font_size=16, font_name="Garet-Heavy", color=[0, 0, 0, 1], size_hint=(1, None))
        nombre.bind(size=lambda w, *a: setattr(nombre, "text_size", (w.width, None)))
        nombre.bind(texture_size=lambda l, ts: setattr(l, "height", ts[1]))
        info.add_widget(nombre)

        desc = Label(
            text=beca["descripcion"],
            font_size=14,
            font_name="Garet-Book",
            color=[0, 0, 0, 1],
            halign="left",
            valign="top",
            size_hint=(1, None)
        )
        desc.bind(size=lambda w, *a: setattr(desc, "text_size", (w.width, None)))
        desc.bind(texture_size=lambda l, ts: setattr(l, "height", ts[1]))
        info.add_widget(desc)

        actions = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(40))
        actions.add_widget(Label(size_hint_x=1))

        view_btn = Button(
            text="View",
            size_hint=(None, None),
            size=(dp(92), dp(36)),
            background_color=(0.4, 0.7, 1, 1),
            color=(1, 1, 1, 1),
            font_name="Garet-Book",
            background_normal='',
            border=(18, 18, 18, 18)  # Botón redondeado
        )
        view_btn.bind(on_release=lambda x, b=beca: self.ir_a_detalle(b))
        actions.add_widget(view_btn)

        info.add_widget(actions)
        card.add_widget(info)

        def _sync_height(*_):
            desired = max(dp(120), img.height + dp(20), nombre.height + desc.height + actions.height + dp(10))
            card.height = desired

        for w in (nombre, desc):
            w.bind(height=lambda *_: _sync_height())
            w.bind(texture_size=lambda *_: _sync_height())

        actions.bind(height=lambda *_: _sync_height())
        img.bind(size=lambda *_: _sync_height())
        _sync_height()

        return card

    def ir_a_detalle(self, beca):
        detalle = self.screen_manager.get_screen("beca_detalle")
        detalle.mostrar_detalle(
            titulo=beca["titulo"],
            descripcion=beca["descripcion"],
            fecha=beca["fecha"],
            requisitos=beca["requisitos"],
            periodo=beca["periodo"],
            inicio=beca["inicio"],
            link=beca["link"],
            imagen=beca["imagen"],
            origen="internationals"
        )
        self.screen_manager.current = "beca_detalle"


# =========================
class BecaDetalleScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager

        # Root vertical
        root = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(16))
        with root.canvas.before:
            Color(0.95, 0.97, 1, 1)
            self.bg = RoundedRectangle(radius=[24], pos=root.pos, size=root.size)

        root.bind(pos=lambda w, *a: setattr(self.bg, "pos", w.pos))
        root.bind(size=lambda w, *a: setattr(self.bg, "size", w.size))
        self.bind(size=lambda *a: setattr(root, 'size', self.size))
        self.bind(pos=lambda *a: setattr(root, 'pos', self.pos))

        scroll = ScrollView(size_hint=(1, 1))

        content = BoxLayout(orientation='vertical', spacing=dp(16), padding=(dp(16), dp(16), dp(16), dp(24)), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Imagen
        self.imagen_beca = Image(size_hint=(1, None), height=dp(180), allow_stretch=True, keep_ratio=True)
        content.add_widget(self.imagen_beca)

        # Título
        self.titulo_label = Label(
            font_size=24, font_name="Garet-Heavy", color=[0.1,0.2,0.5,1],
            halign="center", size_hint=(1, None), bold=True
        )
        self.titulo_label.bind(size=lambda w, *a: setattr(self.titulo_label, "text_size", (w.width, None)))
        self.titulo_label.bind(texture_size=lambda l, ts: setattr(l, "height", ts[1]+dp(8)))
        content.add_widget(self.titulo_label)

        # Descripción
        self.descripcion_label = Label(
            font_size=16, font_name="Garet-Book", color=[0.15,0.15,0.45,1],
            halign="left", valign="top", size_hint=(1, None)
        )
        self.descripcion_label.bind(size=lambda w, *a: setattr(self.descripcion_label, "text_size", (w.width, None)))
        self.descripcion_label.bind(texture_size=lambda l, ts: setattr(l, "height", ts[1]+dp(8)))
        content.add_widget(self.descripcion_label)

        # Chips azules verticales
        self.chips_box = BoxLayout(orientation='vertical', spacing=dp(12), size_hint=(1, None))
        self.chips_box.bind(minimum_height=self.chips_box.setter('height'))

        def crear_chip(text):
            lbl = Label(text=text, font_size=14, font_name="Garet-Book", color=[0.05,0.1,0.4,1], halign="center", valign="middle", size_hint=(1, None), height=dp(36))
            lbl.bind(size=lambda w,*a: setattr(lbl, "text_size", (w.width-10, None)))
            box = BoxLayout(size_hint=(1, None), height=dp(40), padding=dp(4))
            with box.canvas.before:
                Color(0.6,0.85,1,0.3)
                pill = RoundedRectangle(radius=[14], pos=box.pos, size=box.size)
            box.bind(pos=lambda w,*a: setattr(pill,"pos",w.pos))
            box.bind(size=lambda w,*a: setattr(pill,"size",w.size))
            box.add_widget(lbl)
            return box

        self.fecha_label = crear_chip("Deadline: ")
        self.periodo_label = crear_chip("Application window: ")
        self.inicio_label = crear_chip("Start date: ")

        for chip in (self.fecha_label, self.periodo_label, self.inicio_label):
            self.chips_box.add_widget(chip)

        content.add_widget(self.chips_box)

        # Requirements
        self.req_box = BoxLayout(orientation='vertical', spacing=dp(12), padding=dp(12), size_hint=(1, None))
        self.req_box.bind(minimum_height=self.req_box.setter('height'))
        with self.req_box.canvas.before:
            Color(1,1,1,1)
            self.req_bg = RoundedRectangle(radius=[20], pos=self.req_box.pos, size=self.req_box.size)
        self.req_box.bind(pos=lambda w,*a: setattr(self.req_bg,"pos",w.pos))
        self.req_box.bind(size=lambda w,*a: setattr(self.req_bg,"size",w.size))

        self.req_title = Label(text="Requirements", font_size=18, font_name="Garet-Heavy", color=[0.1,0.25,0.5,1], halign="center", size_hint=(1,None), height=dp(32))
        self.req_title.bind(size=lambda w,*a: setattr(self.req_title,"text_size",(w.width,None)))
        self.req_box.add_widget(self.req_title)

        self.requisitos_container = BoxLayout(orientation='vertical', spacing=dp(8), size_hint=(1,None))
        self.requisitos_container.bind(minimum_height=self.requisitos_container.setter('height'))
        self.req_box.add_widget(self.requisitos_container)

        content.add_widget(self.req_box)

        # Botones
        btn_color = (0.2,0.6,1,1)

        self.link_btn = Button(text="More information", size_hint=(None,None), size=(dp(220),dp(44)),
                               background_color=btn_color, color=(1,1,1,1), font_name="Garet-Book",
                               background_normal='', pos_hint={"center_x":0.5}, bold=True)
        self.link_btn.bind(on_release=self.abrir_link)
        content.add_widget(self.link_btn)

        back_btn = Button(text="← Back", size_hint=(None,None), size=(dp(160),dp(44)),
                          background_color=btn_color, color=(1,1,1,1), font_name="Garet-Book",
                          background_normal='', pos_hint={"center_x":0.5}, bold=True)
        back_btn.bind(on_release=self.volver)
        content.add_widget(back_btn)

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

        self.current_link = None
        self.origen = None

    # Actualizar contenido
    def mostrar_detalle(self, titulo, descripcion, fecha, requisitos, periodo, inicio, link, imagen, origen):
        self.titulo_label.text = titulo
        self.descripcion_label.text = descripcion

        self.fecha_label.children[0].text = f"Deadline: {fecha}"
        self.periodo_label.children[0].text = f"Application window: {periodo}"
        self.inicio_label.children[0].text = f"Start date: {inicio}"

        self.requisitos_container.clear_widgets()
        for req in requisitos:
            item_box = BoxLayout(size_hint=(1,None), height=dp(50), padding=dp(8))
             #with item_box.canvas.before:
                #Color(0.95,0.95,0.97,1)
            pill = RoundedRectangle(radius=[12], pos=item_box.pos, size=item_box.size)
            item_box.bind(pos=lambda w,*a: setattr(pill,"pos",w.pos))
            item_box.bind(size=lambda w,*a: setattr(pill,"size",w.size))

            item_label = Label(text=req, font_size=15, font_name="Garet-Book", color=[0,0,0,1],
                               halign="left", valign="middle", text_size=(dp(280),None))
            item_label.bind(texture_size=lambda l,ts: setattr(item_label,"height",ts[1]))
            item_box.add_widget(item_label)
            self.requisitos_container.add_widget(item_box)

        self.current_link = link
        self.origen = origen
        self.imagen_beca.source = imagen

    def abrir_link(self, instance):
        if self.current_link:
            import webbrowser
            webbrowser.open(self.current_link)

    def volver(self, instance):
        if self.origen == "internationals":
            self.screen_manager.current = "internationals"
        elif self.origen == "nationals":
            self.screen_manager.current = "nationals"
        else:
            self.screen_manager.current = "nationals"


# Pantalla base con menú lateral y fondo decorativo
class PantallaConMenuContent(Screen):
    def __init__(self, screen_manager, nombre, contenido_widget, **kwargs):
        super().__init__(name=nombre, **kwargs)
        self.menu_abierto = False
        self.screen_manager = screen_manager

        root = FloatLayout()

        with root.canvas.before:
            Color(1, 1, 1, 1)
            self.rect_bg = Rectangle(size=root.size, pos=root.pos)
        root.bind(size=lambda inst, val: setattr(self.rect_bg, 'size', val),
                  pos=lambda inst, val: setattr(self.rect_bg, 'pos', val))

        self.content_wrapper = FloatLayout()
        self.content_wrapper.add_widget(contenido_widget)
        root.add_widget(self.content_wrapper)

        self.menu = MenuLateral(screen_manager)
        self.menu.size_hint = (None, 1)
        self.menu.width = 260
        self.menu.pos_hint = {}  # Asignar diccionario vacío para evitar error
        self.menu.x = -self.menu.width  # inicia oculto fuera de pantalla
        root.add_widget(self.menu)

        btn_menu = Button(
            size_hint=(None, None),
            size=(60, 60),
            pos_hint={'x': 0.02, 'top': 0.97},
            background_normal="menu.png",
            background_down="menu.png",
            background_color=(1, 1, 1, 1),
            border=(dp(20), dp(20), dp(20), dp(20)),
            on_release=self.toggle_menu
        )
        root.add_widget(btn_menu)

        self.add_widget(root)

    def toggle_menu(self, instance):
        if self.menu_abierto:
            anim = Animation(x=-self.menu.width, duration=0.3, t='out_quad')
            anim.start(self.menu)
        else:
            self.menu.pos_hint = {}  # Evitar error __delete__
            self.menu.x = -self.menu.width
            anim = Animation(x=0, duration=0.3, t='out_quad')
            anim.start(self.menu)

        self.menu_abierto = not self.menu_abierto



class LoginApp(App):
    def build(self):
        sm = WindowManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegistroScreen(name="registro"))
        sm.add_widget(UsuarioScreen(name="usuario"))
        sm.add_widget(ScholarshipChoiceScreen(name="scholar_choice"))
        
        

        sm.add_widget(PantallaConMenuContent(sm, 'experiences', ExperiencesScreen(sm)))

        sm.add_widget(PantallaConMenuContent(sm, 'news', NewsScreen(sm, name="news")))
        sm.add_widget(DetailScreen(name="news_detail"))

        sm.add_widget(PantallaConMenuContent(sm, 'contactus', ContactanosScreen()))
        sm.add_widget(PantallaConMenuContent(sm, 'aboutus', AboutUsScreen()))
        nationals_content = NationalsContent(sm)
        pantalla_nationals = PantallaConMenuContent(sm, "nationals", nationals_content)
        sm.add_widget(pantalla_nationals)
        pantalla_detalle = BecaDetalleScreen(name="beca_detalle", screen_manager=sm)
        sm.add_widget(pantalla_detalle)
        sm.add_widget(PantallaConMenuContent(sm, 'internationals', InternationalsScreen(sm)))
        sm.add_widget(ExperienceDetailScreen(name='experience_detail'))
        return sm
if __name__ == '__main__':
    LoginApp().run()
 
 