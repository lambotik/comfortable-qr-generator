import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import *
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple, Dict, List
import logging
import os
import sys
from datetime import datetime
import colorsys
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_FILE = "qr_code.png"


class SimpleLanguageManager:
    """Упрощенная система языка"""

    def __init__(self):
        self.language = "ru"
        self.texts = {
            "ru": {
                "welcome": "🎨 ГЕНЕРАТОР QR-КОДОВ",
                "menu_title": "ГЛАВНОЕ МЕНЮ",
                "option1": "📱 Создать QR-код с настройками",
                "option2": "⚡ Быстрый QR-код (ссылка/текст)",
                "option3": "👤 Контакт (визитка)",
                "option4": "📍 Контакт с GPS",
                "option5": "ℹ️  О программе",
                "option0": "❌ Выход",
                "prompt": "Выберите действие: ",

                # Контактные данные
                "contact_title": "📇 ВВЕДИТЕ КОНТАКТНЫЕ ДАННЫЕ",
                "optional_field": "(не обязательно)",
                "name": "Имя: ",
                "surname": "Фамилия: ",
                "phone": "Телефон: ",
                "email": "Email: ",
                "company": "Компания: ",
                "position": "Должность: ",
                "website": "Веб-сайт: ",
                "gps": "GPS координаты (широта,долгота): ",
                "address": "Адрес: ",
                "notes": "Заметки: ",

                # Цвета
                "color_title": "🎨 ВЫБОР ЦВЕТОВ",
                "choose_color": "Выберите цвет",
                "rainbow_colors": [
                    "🔴 Красный", "🟠 Оранжевый", "🟡 Желтый",
                    "🟢 Зеленый", "🔵 Синий", "🟣 Фиолетовый"
                ],
                "custom_color": "🌈 Свой цвет (HEX)",
                "bg_color": "Фон",
                "qr_color": "QR-код",
                "frame_color": "Рамка",
                "text_color": "Текст",
                "enter_color": "Введите HEX цвет (#RRGGBB): ",
                "invalid_color": "❌ Неверный формат цвета",

                # Дизайн
                "design_title": "🎨 НАСТРОЙКА ДИЗАЙНА",
                "qr_style": "Стиль QR-кода:",
                "styles": ["□ Квадраты", "○ Круги", "◐ Скругленные"],
                "frame_style": "Тип рамки:",
                "frames": ["Без рамки", "Тонкая рамка", "С текстом"],
                "frame_text": "Текст над QR-кодом: ",
                "frame_text_example": "Пример: МОЯ ВИЗИТКА, SCAN ME, CONTACT",

                # Предварительный просмотр
                "preview_title": "🎨 ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР",
                "background": "Фон",
                "qr_code": "QR-код",
                "frame": "Рамка",
                "header": "Заголовок",

                # Сохранение
                "save_title": "💾 СОХРАНЕНИЕ",
                "filename": "Имя файла: ",
                "file_saved": "✅ Файл сохранен: ",
                "overwrite": "Файл существует. Перезаписать? (д/н): ",

                # Сообщения
                "select_language": "🌍 ВЫБЕРИТЕ ЯЗЫК:",
                "russian": "🇷🇺 Русский",
                "english": "🇺🇸 English",
                "language_selected": "✅ Язык выбран: ",
                "creating": "🔄 Создаю QR-код...",
                "success": "✅ QR-код успешно создан!",
                "error": "❌ Ошибка: ",
                "goodbye": "👋 До свидания!",
                "back": "↩️  Назад",
                "continue": "Продолжить работу? (д/н): ",
                "open_file": "📂 Открыть файл? (д/н): ",
                "change_colors": "🔄 Изменить цвета? (д/н): ",
                "change_frame_text": "✏️  Изменить текст рамки? (д/н): ",
                "yes": "д",
                "no": "н",

                # Да/Нет ответы
                "yes_options": ["д", "да", "y", "yes"],
                "no_options": ["н", "нет", "n", "no"],

                # GPS специфичные
                "gps_instructions": "Формат: 55.7558,37.6173 (Москва)\nОставьте пустым если не нужно",
                "gps_added": "✅ GPS координаты добавлены",

                # Валидация
                "text_required": "❌ Текст не может быть пустым",
                "name_required": "❌ Имя обязательно",

                # Цветовые имена
                "color_names": {
                    "#000000": "Черный",
                    "#FFFFFF": "Белый",
                    "#FF0000": "Красный",
                    "#00FF00": "Зеленый",
                    "#0000FF": "Синий",
                    "#FFFF00": "Желтый",
                    "#FFA500": "Оранжевый",
                    "#800080": "Фиолетовый",
                    "#008080": "Бирюзовый",
                    "#FFC0CB": "Розовый",
                    "#A52A2A": "Коричневый",
                    "#808080": "Серый",
                    "#006666": "Темно-бирюзовый",
                    "#1E88E5": "Светло-синий",
                    "#0D47A1": "Темно-синий"
                }
            },
            "en": {
                "welcome": "🎨 QR-CODE GENERATOR",
                "menu_title": "MAIN MENU",
                "option1": "📱 Create QR-code with settings",
                "option2": "⚡ Quick QR-code (link/text)",
                "option3": "👤 Contact (business card)",
                "option4": "📍 Contact with GPS",
                "option5": "ℹ️  About",
                "option0": "❌ Exit",
                "prompt": "Select action: ",

                # Contact data
                "contact_title": "📇 ENTER CONTACT DETAILS",
                "optional_field": "(optional)",
                "name": "First name: ",
                "surname": "Last name: ",
                "phone": "Phone: ",
                "email": "Email: ",
                "company": "Company: ",
                "position": "Position: ",
                "website": "Website: ",
                "gps": "GPS coordinates (latitude,longitude): ",
                "address": "Address: ",
                "notes": "Notes: ",

                # Colors
                "color_title": "🎨 COLOR SELECTION",
                "choose_color": "Choose color",
                "rainbow_colors": [
                    "🔴 Red", "🟠 Orange", "🟡 Yellow",
                    "🟢 Green", "🔵 Blue", "🟣 Purple"
                ],
                "custom_color": "🌈 Custom color (HEX)",
                "bg_color": "Background",
                "qr_color": "QR code",
                "frame_color": "Frame",
                "text_color": "Text",
                "enter_color": "Enter HEX color (#RRGGBB): ",
                "invalid_color": "❌ Invalid color format",

                # Design
                "design_title": "🎨 DESIGN SETTINGS",
                "qr_style": "QR code style:",
                "styles": ["□ Squares", "○ Circles", "◐ Rounded"],
                "frame_style": "Frame type:",
                "frames": ["No frame", "Thin frame", "With text"],
                "frame_text": "Text above QR code: ",
                "frame_text_example": "Example: MY CARD, SCAN ME, CONTACT",

                # Preview
                "preview_title": "🎨 PREVIEW",
                "background": "Background",
                "qr_code": "QR code",
                "frame": "Frame",
                "header": "Header",

                # Save
                "save_title": "💾 SAVE",
                "filename": "Filename: ",
                "file_saved": "✅ File saved: ",
                "overwrite": "File exists. Overwrite? (y/n): ",

                # Messages
                "select_language": "🌍 SELECT LANGUAGE:",
                "russian": "🇷🇺 Russian",
                "english": "🇺🇸 English",
                "language_selected": "✅ Language selected: ",
                "creating": "🔄 Creating QR code...",
                "success": "✅ QR code created successfully!",
                "error": "❌ Error: ",
                "goodbye": "👋 Goodbye!",
                "back": "↩️  Back",
                "continue": "Continue working? (y/n): ",
                "open_file": "📂 Open file? (y/n): ",
                "change_colors": "🔄 Change colors? (y/n): ",
                "change_frame_text": "✏️  Change frame text? (y/n): ",
                "yes": "y",
                "no": "n",

                # Yes/No answers
                "yes_options": ["y", "yes", "д", "да"],
                "no_options": ["n", "no", "н", "нет"],

                # GPS specific
                "gps_instructions": "Format: 55.7558,37.6173 (Moscow)\nLeave empty if not needed",
                "gps_added": "✅ GPS coordinates added",

                # Validation
                "text_required": "❌ Text cannot be empty",
                "name_required": "❌ Name is required",

                # Color names
                "color_names": {
                    "#000000": "Black",
                    "#FFFFFF": "White",
                    "#FF0000": "Red",
                    "#00FF00": "Green",
                    "#0000FF": "Blue",
                    "#FFFF00": "Yellow",
                    "#FFA500": "Orange",
                    "#800080": "Purple",
                    "#008080": "Turquoise",
                    "#FFC0CB": "Pink",
                    "#A52A2A": "Brown",
                    "#808080": "Gray",
                    "#006666": "Dark turquoise",
                    "#1E88E5": "Light blue",
                    "#0D47A1": "Dark blue"
                }
            }
        }

    def set_language(self, lang: str):
        """Установить язык"""
        if lang in self.texts:
            self.language = lang
            lang_name = "Русский" if lang == "ru" else "English"
            print(f"{self.t('language_selected')}{lang_name}")

    def t(self, key: str) -> str:
        """Получить текст на текущем языке"""
        return self.texts[self.language].get(key, key)

    def get_color_name(self, hex_color: str) -> str:
        """Получить название цвета на текущем языке"""
        color_names = self.texts[self.language].get("color_names", {})
        return color_names.get(hex_color.upper(), hex_color)

    def get_yes_no(self, prompt_key: str) -> bool:
        """Получить ответ да/нет с учетом языка"""
        response = input(f"👉 {self.t(prompt_key)}").lower().strip()
        yes_options = self.texts[self.language].get("yes_options", ["y", "yes"])
        return response in yes_options


lang = SimpleLanguageManager()

# Базовые цвета для удобства выбора
BASIC_COLORS = {
    "1": {"name": "black", "hex": "#000000"},
    "2": {"name": "white", "hex": "#FFFFFF"},
    "3": {"name": "red", "hex": "#FF0000"},
    "4": {"name": "green", "hex": "#00FF00"},
    "5": {"name": "blue", "hex": "#0000FF"},
    "6": {"name": "yellow", "hex": "#FFFF00"},
    "7": {"name": "orange", "hex": "#FFA500"},
    "8": {"name": "purple", "hex": "#800080"},
    "9": {"name": "turquoise", "hex": "#008080"},
    "10": {"name": "pink", "hex": "#FFC0CB"}
}


class ColorSelector:
    """Упрощенный выбор цветов"""

    @staticmethod
    def select_color(color_type: str, default: str = "#000000") -> str:
        """Выбор цвета из палитры или ввод своего"""
        print(f"\n{lang.t('choose_color')} для {lang.t(color_type)}:")
        print("-" * 40)

        # Показать базовые цвета
        for key, color_info in BASIC_COLORS.items():
            color_name = lang.get_color_name(color_info["hex"])
            print(f"{key}. {color_name} {color_info['hex']}")

        print(f"11. {lang.t('custom_color')}")
        print(f"0. {lang.t('back')}")

        while True:
            choice = input(f"\n👉 {lang.t('choose_color')} (0-11): ").strip()

            if choice == "0":
                return None

            if choice in BASIC_COLORS:
                selected = BASIC_COLORS[choice]["hex"]
                color_name = lang.get_color_name(selected)
                print(f"✅ Выбран: {color_name} {selected}")
                return selected

            elif choice == "11":
                # Кастомный цвет
                while True:
                    custom = input(f"👉 {lang.t('enter_color')}").strip()
                    if custom.startswith('#') and len(custom) == 7:
                        try:
                            int(custom[1:], 16)
                            print(f"✅ Выбран: {custom}")
                            return custom.upper()
                        except:
                            print(f"❌ {lang.t('invalid_color')}")
                    else:
                        print(f"❌ {lang.t('invalid_color')} Формат: #RRGGBB")

            # Прямой ввод HEX
            elif choice.startswith('#') and len(choice) == 7:
                try:
                    int(choice[1:], 16)
                    print(f"✅ Выбран: {choice}")
                    return choice.upper()
                except:
                    print(f"❌ {lang.t('invalid_color')}")

            print(f"❌ {lang.t('error')} Неверный выбор")


class ContactManager:
    """Управление контактными данными"""

    FIELDS = {
        "name": {"prompt": "name", "required": True},
        "surname": {"prompt": "surname", "required": False},
        "phone": {"prompt": "phone", "required": False},
        "email": {"prompt": "email", "required": False},
        "company": {"prompt": "company", "required": False},
        "position": {"prompt": "position", "required": False},
        "website": {"prompt": "website", "required": False},
        "gps": {"prompt": "gps", "required": False},
        "address": {"prompt": "address", "required": False},
        "notes": {"prompt": "notes", "required": False}
    }

    @staticmethod
    def get_contact_data(with_gps: bool = False) -> Dict:
        """Получить контактные данные от пользователя"""
        print(f"\n{lang.t('contact_title')}")
        print("=" * 50)

        contact = {}

        for field, config in ContactManager.FIELDS.items():
            # Пропускаем GPS если не требуется
            if field == "gps" and not with_gps:
                continue

            prompt = lang.t(config["prompt"])
            if field == "gps":
                print(f"\n📍 {lang.t('gps_instructions')}")

            if not config["required"]:
                prompt += f" {lang.t('optional_field')}"

            value = input(f"👉 {prompt}").strip()

            if config["required"] and not value:
                print(f"❌ {lang.t('error')} {lang.t('name_required')}")
                continue

            if value:
                contact[field] = value
                if field == "gps":
                    print(f"✅ {lang.t('gps_added')}")

        return contact

    @staticmethod
    def create_vcard(contact: Dict) -> str:
        """Создать vCard из контактных данных"""
        lines = ["BEGIN:VCARD", "VERSION:3.0"]

        # Имя
        name = contact.get('name', '')
        surname = contact.get('surname', '')
        if name or surname:
            lines.append(f"N:{surname};{name};;;")
            lines.append(f"FN:{name} {surname}".strip())

        # Телефон
        if phone := contact.get('phone'):
            lines.append(f"TEL;TYPE=CELL,VOICE:{phone}")

        # Email
        if email := contact.get('email'):
            lines.append(f"EMAIL;TYPE=WORK,INTERNET:{email}")

        # Компания
        if company := contact.get('company'):
            lines.append(f"ORG:{company}")

        # Должность
        if position := contact.get('position'):
            lines.append(f"TITLE:{position}")

        # Сайт
        if website := contact.get('website'):
            lines.append(f"URL:{website}")

        # GPS
        if gps := contact.get('gps'):
            lines.append(f"GEO:{gps}")

        # Адрес
        if address := contact.get('address'):
            lines.append(f"ADR;TYPE=WORK,PREF:;;{address};;;;")

        # Заметки
        if notes := contact.get('notes'):
            lines.append(f"NOTE:{notes}")

        lines.append(f"REV:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}")
        lines.append("END:VCARD")

        return "\n".join(lines)

    @staticmethod
    def create_text_contact(contact: Dict) -> str:
        """Создать текстовое представление контакта"""
        current_lang = lang.language

        if current_lang == "ru":
            text = "КОНТАКТНАЯ ИНФОРМАЦИЯ\n"
            text += "=" * 40 + "\n\n"

            if name := contact.get('name'):
                text += f"👤 Имя: {name}\n"
            if surname := contact.get('surname'):
                text += f"👤 Фамилия: {surname}\n"
            if phone := contact.get('phone'):
                text += f"📞 Телефон: {phone}\n"
            if email := contact.get('email'):
                text += f"📧 Email: {email}\n"
            if company := contact.get('company'):
                text += f"🏢 Компания: {company}\n"
            if position := contact.get('position'):
                text += f"💼 Должность: {position}\n"
            if website := contact.get('website'):
                text += f"🌐 Сайт: {website}\n"
            if gps := contact.get('gps'):
                text += f"📍 GPS: {gps}\n"
            if address := contact.get('address'):
                text += f"🏠 Адрес: {address}\n"
            if notes := contact.get('notes'):
                text += f"📝 Заметки: {notes}\n"

            text += f"\n📅 Создано: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        else:
            text = "CONTACT INFORMATION\n"
            text += "=" * 40 + "\n\n"

            if name := contact.get('name'):
                text += f"👤 Name: {name}\n"
            if surname := contact.get('surname'):
                text += f"👤 Surname: {surname}\n"
            if phone := contact.get('phone'):
                text += f"📞 Phone: {phone}\n"
            if email := contact.get('email'):
                text += f"📧 Email: {email}\n"
            if company := contact.get('company'):
                text += f"🏢 Company: {company}\n"
            if position := contact.get('position'):
                text += f"💼 Position: {position}\n"
            if website := contact.get('website'):
                text += f"🌐 Website: {website}\n"
            if gps := contact.get('gps'):
                text += f"📍 GPS: {gps}\n"
            if address := contact.get('address'):
                text += f"🏠 Address: {address}\n"
            if notes := contact.get('notes'):
                text += f"📝 Notes: {notes}\n"

            text += f"\n📅 Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        return text


class QRDesigner:
    """Дизайнер QR-кодов"""

    def __init__(self):
        self.styles = {
            "1": {"name": "Squares", "drawer": SquareModuleDrawer()},
            "2": {"name": "Circles", "drawer": CircleModuleDrawer()},
            "3": {"name": "Rounded", "drawer": RoundedModuleDrawer()}
        }

    def select_design(self) -> Dict:
        """Выбрать дизайн QR-кода"""
        print(f"\n{lang.t('design_title')}")
        print("=" * 50)

        # Выбор стиля QR-кода
        print(f"\n{lang.t('qr_style')}")
        styles = lang.t("styles")
        for i, style in enumerate(styles, 1):
            print(f"{i}. {style}")

        while True:
            style_choice = input(f"👉 {lang.t('choose_color')} (1-3): ").strip()
            if style_choice in ["1", "2", "3"]:
                break
            print(f"❌ {lang.t('error')}")

        # Выбор рамки
        print(f"\n{lang.t('frame_style')}")
        frames = lang.t("frames")
        for i, frame in enumerate(frames, 1):
            print(f"{i}. {frame}")

        while True:
            frame_choice = input(f"👉 {lang.t('choose_color')} (1-3): ").strip()
            if frame_choice in ["1", "2", "3"]:
                break
            print(f"❌ {lang.t('error')}")

        frame_text = ""
        if frame_choice == "3":  # Рамка с текстом
            print(f"\n✏️  {lang.t('frame_text_example')}")
            frame_text = input(f"👉 {lang.t('frame_text')}").strip()[:30]
            if not frame_text:
                frame_text = "QR CODE"

        # Выбор цветов
        colors = self.select_colors()

        return {
            "style": style_choice,
            "frame_type": frame_choice,
            "frame_text": frame_text.upper(),
            "colors": colors
        }

    def select_colors(self) -> Dict:
        """Выбрать цвета"""
        colors = {}

        print(f"\n{lang.t('color_title')}")
        print("=" * 50)

        # Фон
        colors["background"] = ColorSelector.select_color(
            "bg_color",
            "#FFFFFF"
        ) or "#FFFFFF"

        # QR-код
        colors["qr"] = ColorSelector.select_color(
            "qr_color",
            "#000000"
        ) or "#000000"

        # Рамка
        colors["frame"] = ColorSelector.select_color(
            "frame_color",
            "#000000"
        ) or "#000000"

        # Текст
        colors["text"] = ColorSelector.select_color(
            "text_color",
            "#000000"
        ) or "#000000"

        return colors

    def show_preview(self, design: Dict):
        """Показать предварительный просмотр настроек"""
        print(f"\n{lang.t('preview_title')}")
        print("=" * 50)

        colors = design["colors"]

        # Фон
        bg_name = lang.get_color_name(colors["background"])
        print(f"  {lang.t('background')}: {bg_name} {colors['background']}")

        # QR-код
        qr_name = lang.get_color_name(colors["qr"])
        print(f"  {lang.t('qr_code')}: {qr_name} {colors['qr']}")

        # Рамка
        if design["frame_type"] != "1":
            frame_name = lang.get_color_name(colors["frame"])
            print(f"  {lang.t('frame')}: {frame_name} {colors['frame']}")

            # Текст
            if design["frame_type"] == "3":
                text_name = lang.get_color_name(colors["text"])
                print(f"  {lang.t('text_color')}: {text_name} {colors['text']}")
                print(f"  {lang.t('header')}: {design['frame_text']}")


class QRGenerator:
    """Генератор QR-кодов"""

    @staticmethod
    def generate_qr(content: str, design: Dict, filename: str) -> bool:
        """Сгенерировать QR-код"""
        try:
            print(f"\n{lang.t('creating')}")

            # Создаем QR-код
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=12,
                border=4,
            )
            qr.add_data(content)
            qr.make(fit=True)

            # Применяем стиль
            designer = QRDesigner()
            style = designer.styles[design["style"]]

            try:
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=style["drawer"],
                    fill_color=design["colors"]["qr"],
                    back_color=design["colors"]["background"]
                ).convert('RGBA')
            except:
                img = qr.make_image(
                    fill_color=design["colors"]["qr"],
                    back_color=design["colors"]["background"]
                ).convert('RGBA')

            # Добавляем рамку если нужно
            if design["frame_type"] != "1":
                img = QRGenerator.add_frame(img, design)

            # Сохраняем
            img.save(filename, 'PNG', optimize=True)

            print(f"\n{lang.t('success')}")
            print(f"📁 {lang.t('file_saved')}{os.path.abspath(filename)}")

            return True

        except Exception as e:
            print(f"{lang.t('error')}{e}")
            return False

    @staticmethod
    def add_frame(image: Image.Image, design: Dict) -> Image.Image:
        """Добавить рамку к изображению"""
        width, height = image.size

        # Толщина рамки - УВЕЛИЧИВАЕМ для лучшей видимости
        if design["frame_type"] == "3":  # С текстом
            thickness = 80  # УВЕЛИЧЕНО с 20 до 80 пикселей
        else:  # Тонкая рамка
            thickness = 20

        # Новый размер
        new_width = width + thickness * 2
        new_height = height + thickness * 2

        # Создаем новое изображение
        frame_color = design["colors"]["frame"]
        framed = Image.new('RGBA', (new_width, new_height), frame_color)

        # Вставляем QR-код
        framed.paste(image, (thickness, thickness), image)

        # Добавляем текст если нужно - ДЕЛАЕМ БОЛЬШЕ
        if design["frame_type"] == "3" and design["frame_text"]:
            draw = ImageDraw.Draw(framed)

            # Пробуем разные шрифты
            font_paths = [
                "arialbd.ttf",  # Arial Bold
                "arial.ttf",  # Arial
                "Arial",  # Имя шрифта
                "/System/Library/Fonts/Helvetica.ttc",  # macOS
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
                "C:\\Windows\\Fonts\\arialbd.ttf",  # Windows
            ]

            font = None
            font_size = 0

            # Пробуем сделать текст КРУПНЫМ
            for try_size in [72, 60, 48, 36, 30]:  # Большие размеры
                for font_path in font_paths:
                    try:
                        font = ImageFont.truetype(font_path, try_size)
                        font_size = try_size
                        break
                    except:
                        continue
                if font:
                    break

            if not font:
                font = ImageFont.load_default()
                font_size = 36  # Большой размер по умолчанию

            # Рассчитываем позицию текста - ВВЕРХУ по центру
            try:
                # Получаем размер текста
                text_bbox = draw.textbbox((0, 0), design["frame_text"], font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
            except:
                # Если не получилось, используем приближение
                text_width = len(design["frame_text"]) * font_size // 2
                text_height = font_size

            # Позиция текста - ВВЕРХУ по центру
            text_x = (new_width - text_width) // 2
            text_y = max(10, thickness // 4)  # Очень близко к верху

            # Цвет текста
            text_color = design["colors"]["text"]

            # Добавляем тень для лучшей читаемости
            shadow_offset = 2
            # Автоматически определяем цвет тени
            if text_color == "#000000":
                shadow_color = "#333333"
            elif text_color == "#FFFFFF":
                shadow_color = "#000000"
            else:
                # Для других цветов используем черный или белый в зависимости от яркости
                try:
                    hex_color = text_color.lstrip('#')
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    brightness = (r * 299 + g * 587 + b * 114) / 1000
                    shadow_color = "#000000" if brightness > 128 else "#FFFFFF"
                except:
                    shadow_color = "#000000"

            # Рисуем тень
            draw.text((text_x + shadow_offset, text_y + shadow_offset),
                      design["frame_text"], fill=shadow_color, font=font)

            # Рисуем основной текст
            draw.text((text_x, text_y), design["frame_text"],
                      fill=text_color, font=font)

            print(f"✅ Текст добавлен: {design['frame_text']} (размер: {font_size}px)")

        return framed


def get_filename(default: str = "qr_code") -> str:
    """Получить имя файла"""
    print(f"\n{lang.t('save_title')}")
    print("-" * 40)

    while True:
        filename = input(f"👉 {lang.t('filename')}").strip()

        if not filename:
            filename = default

        # Очищаем имя файла
        filename = "".join(c for c in filename if c.isalnum() or c in ('-', '_', ' '))
        filename = filename.replace(' ', '_')

        if not filename.lower().endswith('.png'):
            filename += '.png'

        if os.path.exists(filename):
            if lang.get_yes_no("overwrite"):
                break
            else:
                print("🔄 Введите другое имя файла")
                continue

        break

    return filename


def create_custom_qr():
    """Создать QR-код с кастомными настройками"""
    print("\n📱 СОЗДАНИЕ QR-КОДА С НАСТРОЙКАМИ")
    print("=" * 50)

    # Выбор типа контента
    print("\n📝 ТИП КОНТЕНТА:")
    print("1. Текст или ссылка")
    print("2. Контакт (визитка)")
    print("3. Контакт с GPS")
    print(f"0. {lang.t('back')}")

    while True:
        choice = input(f"\n👉 {lang.t('prompt')}").strip()

        if choice == "0":
            return

        if choice == "1":
            # Простой текст
            text = input("👉 Введите текст или ссылку: ").strip()
            if not text:
                print(f"❌ {lang.t('text_required')}")
                continue

        elif choice == "2":
            # Контакт без GPS
            contact = ContactManager.get_contact_data(with_gps=False)
            if not contact:
                print(f"❌ {lang.t('error')} Нет данных контакта")
                return
            vcard = ContactManager.create_vcard(contact)
            text_contact = ContactManager.create_text_contact(contact)
            text = f"{vcard}\n\n{text_contact}"

        elif choice == "3":
            # Контакт с GPS
            contact = ContactManager.get_contact_data(with_gps=True)
            if not contact:
                print(f"❌ {lang.t('error')} Нет данных контакта")
                return
            vcard = ContactManager.create_vcard(contact)
            text_contact = ContactManager.create_text_contact(contact)
            text = f"{vcard}\n\n{text_contact}"

        else:
            print(f"❌ {lang.t('error')}")
            continue

        # Выбор дизайна
        designer = QRDesigner()
        design = designer.select_design()

        # Показать предварительный просмотр
        designer.show_preview(design)

        # Изменить настройки?
        if lang.get_yes_no("change_colors"):
            new_colors = designer.select_colors()
            design["colors"] = new_colors

        if design["frame_type"] == "3" and lang.get_yes_no("change_frame_text"):
            new_text = input(f"👉 {lang.t('frame_text')}").strip()[:30]
            if new_text:
                design["frame_text"] = new_text.upper()

        # Получение имени файла
        filename = get_filename()

        # Генерация QR-кода
        success = QRGenerator.generate_qr(text, design, filename)

        # Открыть файл?
        if success and os.path.exists(filename):
            if lang.get_yes_no("open_file"):
                try:
                    if os.name == 'nt':
                        os.startfile(filename)
                    elif sys.platform == 'darwin':
                        os.system(f'open "{filename}"')
                    else:
                        os.system(f'xdg-open "{filename}"')
                except:
                    print(f"⚠️  Не удалось открыть файл")

        break


def quick_qr():
    """Быстрое создание QR-кода"""
    print("\n⚡ БЫСТРЫЙ QR-КОД")
    print("=" * 50)

    text = input("👉 Введите текст или ссылку: ").strip()
    if not text:
        print(f"❌ {lang.t('text_required')}")
        return

    filename = get_filename("quick_qr")

    # Простой дизайн по умолчанию
    design = {
        "style": "1",
        "frame_type": "1",
        "frame_text": "",
        "colors": {
            "background": "#FFFFFF",
            "qr": "#000000",
            "frame": "#000000",
            "text": "#000000"
        }
    }

    QRGenerator.generate_qr(text, design, filename)


def create_contact_qr(with_gps: bool = False):
    """Создать QR-код визитки"""
    # Определяем заголовок окна
    if with_gps:
        title = "📍 ВИЗИТКА С GPS" if lang.language == "ru" else "📍 CONTACT WITH GPS"
    else:
        title = "👤 ВИЗИТКА" if lang.language == "ru" else "👤 BUSINESS CARD"

    print(f"\n{title}")
    print("=" * 50)

    # Получение данных контакта
    contact = ContactManager.get_contact_data(with_gps=with_gps)
    if not contact:
        print(f"❌ {lang.t('error')} Нет данных контакта")
        return

    # Создание vCard и текста
    vcard = ContactManager.create_vcard(contact)
    text_contact = ContactManager.create_text_contact(contact)
    content = f"{vcard}\n\n{text_contact}"

    # Автоматический выбор цветов для визитки
    if with_gps:
        qr_color = "#008080"  # Бирюзовый
        frame_color = "#006666"
    else:
        qr_color = "#1E88E5"  # Синий
        frame_color = "#0D47A1"

    colors = {
        "background": "#FFFFFF",
        "qr": qr_color,
        "frame": frame_color,
        "text": "#FFFFFF"
    }

    # Настройки дизайна
    design = {
        "style": "2",  # Круги
        "frame_type": "3",  # С текстом
        "frame_text": "",  # Начинаем с пустого текста
        "colors": colors
    }

    # Показываем примеры текста в зависимости от языка
    if lang.language == "ru":
        examples = ["МОЯ ВИЗИТКА", "SCAN ME", "КОНТАКТ", "VISIT CARD", "BUSINESS CARD"]
        if with_gps:
            examples.insert(0, "📍 LOCATION")
            examples.insert(1, "НАЙДИ МЕНЯ")
    else:
        examples = ["MY CARD", "SCAN ME", "CONTACT", "VISIT CARD", "BUSINESS CARD"]
        if with_gps:
            examples.insert(0, "📍 LOCATION")
            examples.insert(1, "FIND ME")

    print(f"\n✏️  {lang.t('frame_text_example')}")
    print("   " + ", ".join(examples))

    # Получаем текст от пользователя
    frame_text = input(f"👉 {lang.t('frame_text')}").strip()[:30]

    # Если пользователь ничего не ввел, используем разумный текст по умолчанию
    if not frame_text:
        if with_gps:
            frame_text = "LOCATION"
        else:
            # Пробуем использовать имя из контакта
            name = contact.get('name', '')
            surname = contact.get('surname', '')
            if name:
                if lang.language == "ru":
                    frame_text = f"{name.upper()}"
                    if surname:
                        frame_text += f" {surname.upper()}"
                else:
                    frame_text = f"{name.upper()}"
                    if surname:
                        frame_text += f" {surname.upper()}"
            else:
                frame_text = "CONTACT"

    design["frame_text"] = frame_text.upper()

    # Показать предварительный просмотр
    designer = QRDesigner()
    designer.show_preview(design)

    # Изменить настройки?
    if lang.get_yes_no("change_colors"):
        new_colors = designer.select_colors()
        design["colors"] = new_colors

    # Позволяем изменить текст рамки, если нужно
    print(f"\n✏️  Текущий текст: {design['frame_text']}")
    if lang.get_yes_no("change_frame_text"):
        print(f"\n📝 {lang.t('frame_text_example')}")
        print("   " + ", ".join(examples))
        new_text = input(f"👉 {lang.t('frame_text')}").strip()[:30]
        if new_text:
            design["frame_text"] = new_text.upper()

    # Сохранение
    if with_gps:
        default_name = "contact_gps_qr"
    else:
        # Используем имя для имени файла, если есть
        name = contact.get('name', 'contact')
        surname = contact.get('surname', '')
        if name:
            default_name = f"{name.lower()}"
            if surname:
                default_name += f"_{surname.lower()}"
            default_name += "_qr"
        else:
            default_name = "contact_qr"

    filename = get_filename(default_name)

    # Генерация
    success = QRGenerator.generate_qr(content, design, filename)

    # Открыть файл?
    if success and os.path.exists(filename):
        if lang.get_yes_no("open_file"):
            try:
                if os.name == 'nt':
                    os.startfile(filename)
                elif sys.platform == 'darwin':
                    os.system(f'open "{filename}"')
                else:
                    os.system(f'xdg-open "{filename}"')
            except:
                print(f"⚠️  Не удалось открыть файл")


def show_about():
    """Показать информацию о программе"""
    print("\n" + "=" * 60)
    print("🎨 QR-CODE GENERATOR")
    print("=" * 60)

    if lang.language == "ru":
        print("\n✨ ВОЗМОЖНОСТИ:")
        print("  • Создание QR-кодов любой сложности")
        print("  • Визитки с контактными данными")
        print("  • Поддержка GPS координат")
        print("  • Гибкая настройка цветов")
        print("  • Различные стили и рамки")
        print("\n🎨 ЦВЕТА:")
        print("  • Простой выбор из базовых цветов")
        print("  • Возможность ввода любого HEX цвета")
        print("  • Отдельная настройка фона, QR-кода, рамки и текста")
        print("\n📱 КОНТАКТЫ:")
        print("  • Любые поля: имя, телефон, email, сайт и др.")
        print("  • Автоматическое создание vCard")
        print("  • GPS координаты в стандартном формате")
        print("\n✏️  ТЕКСТ НА РАМКЕ:")
        print("  • Крупный читаемый текст")
        print("  • Автоматический выбор цвета для контраста")
        print("  • Тень для улучшения видимости")
    else:
        print("\n✨ FEATURES:")
        print("  • Create QR codes of any complexity")
        print("  • Business cards with contact data")
        print("  • GPS coordinates support")
        print("  • Flexible color customization")
        print("  • Various styles and frames")
        print("\n🎨 COLORS:")
        print("  • Easy selection from basic colors")
        print("  • Ability to enter any HEX color")
        print("  • Separate settings for background, QR code, frame and text")
        print("\n📱 CONTACTS:")
        print("  • Any fields: name, phone, email, website, etc.")
        print("  • Automatic vCard creation")
        print("  • GPS coordinates in standard format")
        print("\n✏️  FRAME TEXT:")
        print("  • Large readable text")
        print("  • Automatic color selection for contrast")
        print("  • Shadow for better visibility")


def main():
    """Основная функция программы"""

    # Выбор языка
    print(f"\n{lang.t('select_language')}")
    print(f"1. {lang.t('russian')}")
    print(f"2. {lang.t('english')}")

    while True:
        lang_choice = input("👉 Выбор / Choice: ").strip()
        if lang_choice == "1":
            lang.set_language("ru")
            break
        elif lang_choice == "2":
            lang.set_language("en")
            break
        else:
            print("❌ Please enter 1 or 2 / Пожалуйста, введите 1 или 2")

    print(f"\n{lang.t('welcome')}")
    print("=" * 60)

    while True:
        print(f"\n{lang.t('menu_title')}")
        print("-" * 40)
        print(f"1. {lang.t('option1')}")
        print(f"2. {lang.t('option2')}")
        print(f"3. {lang.t('option3')}")
        print(f"4. {lang.t('option4')}")
        print(f"5. {lang.t('option5')}")
        print(f"0. {lang.t('option0')}")

        choice = input(f"\n👉 {lang.t('prompt')}").strip()

        if choice == "0":
            print(f"\n{lang.t('goodbye')}")
            break

        elif choice == "1":
            create_custom_qr()

        elif choice == "2":
            quick_qr()

        elif choice == "3":
            create_contact_qr(with_gps=False)

        elif choice == "4":
            create_contact_qr(with_gps=True)

        elif choice == "5":
            show_about()

        else:
            print(f"❌ {lang.t('error')}")

        # Продолжить?
        if choice in ["1", "2", "3", "4", "5"]:
            if not lang.get_yes_no("continue"):
                print(f"\n{lang.t('goodbye')}")
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{lang.t('goodbye')}")
    except Exception as e:
        print(f"\n❌ {lang.t('error')}{e}")
        import traceback

        traceback.print_exc()