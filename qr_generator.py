import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import *
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple, Dict
import logging
import os
import sys
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_FILE = "qr_code.png"


# Language system
class LanguageManager:
    """Manages language selection and text display"""

    LANGUAGES = {
        "en": "English",
        "ru": "Русский"
    }

    # English translations
    EN = {
        # Main menu
        "main_title": "QR-CODE GENERATOR WITH GPS AND ADDRESS",
        "main_subtitle": "Create QR-code business cards with GPS coordinates and addresses!",
        "perfect_for": "Perfect for business, events and personal meetings.",

        # Menu options
        "menu_title": "MAIN MENU",
        "menu_option1": "Create QR-code with customization",
        "menu_option2": "Quick generation",
        "menu_option3": "Create basic business card (vCard)",
        "menu_option4": "Create business card with GPS and address",
        "menu_option5": "Business card with your custom header",
        "menu_option6": "About",
        "menu_option0": "Exit",
        "menu_prompt": "Select action (0-6): ",

        # Common
        "back": "Back",
        "exit": "Exit",
        "continue": "Continue",
        "cancel": "Cancel",
        "save": "Save",
        "error": "Error",
        "success": "Success",
        "warning": "Warning",
        "select": "Select",
        "enter": "Enter",
        "choose": "Choose",
        "default": "Default",
        "custom": "Custom",

        # Content types
        "content_choice_title": "SELECT CONTENT TYPE",
        "content_option1": "Simple text or link",
        "content_option2": "Basic business card (vCard)",
        "content_option3": "Business card with GPS and address",
        "content_option4": "Contact data only (text)",
        "content_prompt": "Select type (0-4): ",

        # QR styles
        "styles": {
            "1": {"name": "Classic", "desc": "Standard square modules"},
            "2": {"name": "Circular", "desc": "Round dots (modern style)"},
            "3": {"name": "Rounded", "desc": "Modules with rounded corners"},
            "4": {"name": "Minimalist", "desc": "Squares with gaps"},
        },

        "shapes": {
            "1": {"name": "Rectangle", "desc": "Standard rectangular QR code shape"},
            "2": {"name": "Rounded corners", "desc": "QR code with rounded corners (modern)"},
        },

        "frames": {
            "1": {"name": "No frame", "desc": "Simple QR code without frame"},
            "2": {"name": "Simple frame", "desc": "Thin line around QR code"},
            "3": {"name": "Double frame", "desc": "Two concentric lines"},
            "4": {"name": "Thick frame", "desc": "Bold frame around QR code"},
            "5": {"name": "VISIT CARD", "desc": "Frame with VISIT CARD text"},
            "6": {"name": "BUSINESS CARD", "desc": "Frame with BUSINESS CARD text"},
            "7": {"name": "CONTACT", "desc": "Frame with CONTACT text"},
            "8": {"name": "Custom header", "desc": "Frame with your custom text"},
        },

        "color_themes": {
            "1": {"name": "Black & White", "fg": "#000000", "bg": "#FFFFFF", "outline": "#000000",
                  "desc": "Classic contrast style"},
            "2": {"name": "Blue", "fg": "#0066CC", "bg": "#FFFFFF", "outline": "#004488",
                  "desc": "Corporate blue on white"},
            "3": {"name": "Green", "fg": "#00AA00", "bg": "#FFFFFF", "outline": "#008800",
                  "desc": "Fresh green on white"},
            "4": {"name": "Red", "fg": "#CC0000", "bg": "#FFFFFF", "outline": "#AA0000",
                  "desc": "Bright red for accents"},
            "5": {"name": "Purple", "fg": "#6600CC", "bg": "#FFFFFF", "outline": "#5500AA", "desc": "Creative purple"},
            "6": {"name": "Orange", "fg": "#FF6600", "bg": "#FFFFFF", "outline": "#DD5500", "desc": "Energetic orange"},
            "7": {"name": "vCard Style", "fg": "#1E88E5", "bg": "#FFFFFF", "outline": "#0D47A1",
                  "desc": "Special style for business cards"},
            "8": {"name": "Professional", "fg": "#2E7D32", "bg": "#FFFFFF", "outline": "#1B5E20",
                  "desc": "Restrained green for business"},
            "9": {"name": "Premium Gold", "fg": "#000000", "bg": "#FFFFFF", "outline": "#D4AF37",
                  "desc": "Black & white with gold frame"},
            "10": {"name": "Metallic Gray", "fg": "#333333", "bg": "#FFFFFF", "outline": "#666666",
                   "desc": "Modern gray style"},
            "11": {"name": "Location", "fg": "#008080", "bg": "#FFFFFF", "outline": "#006666",
                   "desc": "Turquoise style for address cards"},
            "12": {"name": "Map", "fg": "#D35400", "bg": "#FFFFFF", "outline": "#A04000",
                   "desc": "Terracotta for GPS markers"},
        },

        # Text prompts
        "enter_text": "Enter text: ",
        "enter_text_or_link": "Enter text/link: ",
        "text_too_long": "Text too long. Maximum 4000 characters.",
        "text_cannot_be_empty": "Text cannot be empty. Please try again.",
        "enter_phone": "Phone (e.g., +79991234567): ",
        "enter_email": "Email: ",
        "enter_first_name": "First name: ",
        "enter_last_name": "Last name: ",
        "enter_company": "Company (optional): ",
        "enter_job_title": "Job title (optional): ",
        "enter_website": "Website (optional): ",

        # GPS
        "gps_title": "ADDING GPS COORDINATES",
        "gps_instructions": "You can add location coordinates\nFormat: latitude,longitude (e.g.: 53.9045,27.5615)\nGet coordinates from Google Maps or Yandex Maps\nLeave empty to skip",
        "gps_prompt": "Enter coordinates (latitude,longitude): ",
        "gps_invalid_format": "Invalid format. Use: latitude,longitude",
        "gps_invalid_range": "Invalid coordinate range.\nLatitude: -90 to 90, Longitude: -180 to 180",
        "gps_invalid_number": "Invalid format. Use numbers.",
        "gps_added": "GPS coordinates added: ",
        "try_again_or_skip": "Try again or press Enter to skip",

        # Address
        "address_title": "ADDING ADDRESS",
        "address_instructions": "You can add full address\nExample: Lenina St. 10, Minsk, Belarus, 220000\nLeave empty to skip",
        "address_prompt": "Enter address: ",
        "address_added": "Address added: ",
        "address_optional": "Address (optional): ",

        # Frame text
        "frame_text_title": "ENTER YOUR TEXT FOR FRAME",
        "frame_text_instructions": "Text will display in top part of QR code frame\nExamples:\n  • MY BUSINESS CARD\n  • CONTACT ME\n  • SCAN FOR INFO\n  • DIMA CHARNUkHA\n  • MOEX AQA",
        "frame_text_prompt": "Enter text (max 20 characters): ",
        "frame_text_too_long": "Text too long. Maximum 20 characters.",

        # File save
        "save_title": "SAVING RESULT",
        "save_instructions": "File will be saved in PNG format",
        "save_prompt": "Filename (default: {default_name}): ",
        "file_exists": "File '{filename}' already exists. Overwrite? (yes/no): ",
        "file_saved": "File saved: ",
        "enter_different_name": "Enter different filename.",

        # Colors
        "color_choice": "COLOR SELECTION",
        "frame_color_title": "FRAME COLOR SELECTION",
        "text_color_title": "TEXT COLOR ON FRAME",
        "choose_text_color": "Choose text color for frame:",
        "text_color_auto": "Automatic (contrast to frame)",
        "text_color_white": "White",
        "text_color_black": "Black",
        "text_color_gold": "Gold (#FFD700)",
        "text_color_silver": "Silver (#C0C0C0)",
        "contrast_black": "Contrast black text selected",
        "contrast_white": "Contrast white text selected",
        "white_selected": "White text selected",
        "black_selected": "Black text selected",
        "gold_selected": "Gold text selected (#FFD700)",
        "silver_selected": "Silver text selected (#C0C0C0)",

        # Frame color options
        "frame_color_auto": "Automatic (slightly darker than main color)",
        "frame_color_white": "White",
        "frame_color_black": "Black",
        "frame_color_contrast": "Contrast (opposite to background)",
        "frame_color_custom": "Enter custom color",
        "auto_color_selected": "Automatic color selected: ",
        "white_color_selected": "White color selected",
        "black_color_selected": "Black color selected",
        "contrast_black_selected": "Contrast color selected: black",
        "contrast_white_selected": "Contrast color selected: white",

        # Custom color input
        "custom_color_title": "ENTER FRAME COLOR",
        "color_examples": "Color examples:",
        "gps_color_suggestions": "Popular colors for GPS business cards:\n  #008080 - turquoise (location)\n  #D35400 - terracotta (map)\n  #0D47A1 - dark blue (official)",
        "frame_color_suggestions": "Popular colors for text frames:\n  #0D47A1 - dark blue (official)\n  #D4AF37 - gold (premium)\n  #424242 - dark gray (minimalism)\n  #2E7D32 - green (business)",
        "vcard_color_recommendations": "Recommendations for business cards:\n   • Blue (#1E88E5) - professional\n   • Dark blue (#0D47A1) - contrast",
        "color_format": "Enter color in format #RRGGBB\n(e.g.: #FF0000 for red)",
        "color_prompt": "Enter color: ",
        "invalid_color_format": "Invalid color format. Use HEX, e.g.: #FF0000 or #F00",
        "color_must_start_hash": "Color must start with # and contain 3, 4, 6 or 7 characters",
        "color_error": "Error determining color",
        "contrast_error": "Error determining contrast. Using white text",

        # Generation
        "generation_title": "CREATING QR-CODE...",
        "generation_params": "Creation parameters:",
        "generation_success": "QR-CODE SUCCESSFULLY CREATED!",
        "generation_info": "Information:",
        "size_pixels": "Size: {width}x{height} pixels",
        "file_size": "File size: {size} KB",
        "file_path": "Path: {path}",

        # Tips
        "business_card_tips": "Business card tips:",
        "phone_will_prompt": "When scanning, phone should prompt 'Add contact'",
        "your_header": "Your header: ",
        "thin_frame": "Thin frame, text close to QR code",
        "contains_gps": "Business card contains GPS coordinates",
        "can_open_in_maps": "Can open in maps",
        "try_other_scanner": "If not prompting, try different QR scanner",
        "print_minimum": "Print at minimum 4x4 cm",

        "general_tips": "General tips:",
        "check_with_phone": "Check scanning with phone",
        "print_minimum_small": "Print at minimum 3x3 cm",

        # About
        "about_title": "ABOUT THE PROGRAM",
        "version": "QR-code generator with GPS and address v9.0",
        "new_features": "NEW FEATURES:",
        "feature1": "• Adding GPS coordinates to business cards",
        "feature2": "• Including full addresses",
        "feature3": "• 2 new color themes for locations",
        "feature4": "• Automatic coordinate formatting",

        "gps_features": "GPS FEATURES:",
        "gps1": "• Format support: latitude,longitude",
        "gps2": "• Coordinate validation",
        "gps3": "• Added to vCard as GEO tag",
        "gps4": "• Text representation for convenience",

        "address_features": "ADDRESS FEATURES:",
        "address1": "• Full address in any format",
        "address2": "• Added to vCard as ADR tag",
        "address3": "• Saved in text form",

        "design_features": "DESIGN:",
        "design1": "• 2 QR code shapes",
        "design2": "• 4 module styles",
        "design3": "• 12 color themes (2 new for GPS)",
        "design4": "• 8 frame types",

        "compatibility": "COMPATIBILITY:",
        "comp1": "• 100% compatibility with QR scanners",
        "comp2": "• Automatic business card recognition",
        "comp3": "• GPS coordinates open in maps",
        "comp4": "• Android and iOS support",

        # VCard
        "vcard_title": "CREATING ELECTRONIC BUSINESS CARD (vCard)",
        "vcard_subtitle": "Fill data to create business card QR code\nWhen scanning, phone will prompt to add contact",
        "personal_data": "PERSONAL DATA",
        "contact_info": "CONTACT INFORMATION",
        "additional_info": "ADDITIONAL INFORMATION",
        "business_card_created": "Business card created!",
        "vcard_structure": "QR code structure:",
        "vcard_structure1": "1. vCard data (for adding to contacts)",
        "vcard_structure2": "2. Text representation (for viewing)",

        # Contact text
        "contact_text_title": "ENTER CONTACT DATA",
        "contact_instructions": "This data will be visible when scanning QR code",
        "personal_details": "Personal details:",
        "name_prompt": "Full name: ",
        "contact_details": "Contact information:",
        "additional_details": "Additional information:",
        "coordinates_optional": "coordinates (optional):",
        "gps_format_example": "Format: latitude,longitude (e.g.: 53.9045,27.5615)",
        "coordinates_prompt": "Coordinates: ",

        # Quick generation
        "quick_generate_title": "QUICK GENERATION",
        "quick_generate_prompt": "Enter text/link: ",

        # Language selection
        "language_title": "SELECT LANGUAGE",
        "language_prompt": "Select language (1-English, 2-Русский): ",
        "language_selected": "Language selected: ",

        # Yes/No prompts
        "open_file": "Open file? (yes/no): ",
        "return_to_menu": "Return to main menu? (yes/no): ",
        "proceed": "Proceed? (yes/no): ",
        "change_frame_color": "Change frame color? (yes/no): ",
        "change_text_color": "Change text color? (yes/no): ",

        # Errors
        "unexpected_error": "Unexpected error: ",
        "please_restart": "Please restart program",
        "user_interrupted": "Program interrupted by user",
        "creation_error": "Error creating QR code: ",
        "try_simplify": "Try to:",
        "simplify_text": "• Simplify text",
        "simpler_style": "• Use simpler style",
        "different_color": "• Choose different color",
        "check_vcard": "• Ensure vCard starts with BEGIN:VCARD",
        "try_again": "Please try again.",
        "enter_number_from_to": "Enter number from",

        # Text examples
        "text_examples": "Examples:\n  • https://example.com\n  • Any message or text\n  • Contact data manually",

        # Design recommendations
        "shape_recommendations": "💡 For business cards recommended:\n   • Rounded corners - modern style\n   • Rectangle - classic look",
        "style_recommendations": "💡 For business cards recommended:\n   • Circular - modern smartphones\n   • Classic - maximum readability",
        "gps_theme_recommendations": "💡 Special themes for GPS business cards:\n   11. Location - turquoise, for addresses\n   12. Map - terracotta, for GPS markers",
        "vcard_theme_recommendations": "💡 Special themes for business cards:\n   7. vCard Style - blue, for contacts\n   8. Professional - green, for business\n   9. Premium Gold - with gold frame\n   10. Metallic Gray - modern style",

        # Selection
        "selected_colors": "Selected colors",
        "main_qr_color": "Main QR code color",
        "background_color": "Background color",
        "default_frame_color": "Default frame color",
        "final_color_params": "Final color parameters",
        "qr_color": "QR code color",
        "frame_color": "Frame color",
        "frame_text_color": "Text color in frame",

        # Generation messages
        "creating_image_with_color": "Creating image with color",
        "on": "on",
        "styled_image_created": "Styled image created successfully",
        "styled_image_error": "Failed to create styled image",
        "trying_standard_image": "Trying to create standard image...",
        "standard_image_created": "Standard image created successfully",
        "adding_frame": "Adding frame",
        "saving_file": "Saving file",

        # GPS business card
        "create_gps_business_card": "Create business card with coordinates and address\nPerfect for business, events, meetings",
        "header_selected": "Header selected",
        "gps_card_settings": "Using optimal settings:\n• Shape: Rounded corners\n• Style: Classic (max readability)\n• Color: Location (turquoise)\n• Frame: Thin with text\n• Text: Close to QR code",
        "current_color": "Current color",
        "current_text_color": "Current text color",
        "contains_gps_address": "Business card contains GPS and address",
        "thin_frame_close_text": "Thin frame, text close to QR code",
        "file": "File",

        # Quick creation
        "quick_business_card_steps": "Create business card QR code in 3 steps:\n1. Fill in data\n2. Choose design\n3. Save QR code",
        "quick_design_for_business_card": "QUICK DESIGN FOR BUSINESS CARD",
        "recommended_settings": "Using recommended settings:\n• Shape: Rounded corners\n• Style: Circular\n• Color: vCard Style (blue)\n• Frame: Simple, blue",

        # Custom header
        "create_custom_header_business_card": "Create business card with your text in frame",
        "settings_for_business_card": "SETTINGS FOR BUSINESS CARD",
        "optimal_settings": "Using optimal settings:\n• Shape: Rounded corners\n• Style: Classic\n• Color: vCard Style (blue)\n• Frame: Thin with text",

        # Business card creation
        "creating_business_card_qr": "Creating business card QR code...",
        "customize_business_card_appearance": "Customize business card QR code appearance:",
        "data_format": "DATA FORMAT:",
        "optimized_vcard_format": "Using optimized vCard format",
        "vcard_for_contacts": "vCard data (for adding to contacts)",
        "text_for_viewing": "Text representation (for viewing)",
        "guaranteed_scanner_compatibility": "Guaranteed scanner compatibility",
        "creating_gps_business_card_qr": "Creating GPS business card QR code...",
        "customize_gps_business_card_appearance": "Customize GPS business card QR code appearance:",
        "includes_gps_address": "Includes GPS coordinates and address",

        # Quick generate
        "creating_qr": "Creating QR code...",
        "qr_created": "QR code created",

        # Goodbye
        "goodbye": "Goodbye! Thank you for using the program!",

        # Header
        "header": "Header",

        # Using simple frame
        "using_simple_frame": "Using simple frame without text",
    }

    # Russian translations
    RU = {
        # Main menu
        "main_title": "ГЕНЕРАТОР QR-КОДОВ С GPS И АДРЕСОМ",
        "main_subtitle": "Создавайте QR-коды визиток с GPS координатами и адресом!",
        "perfect_for": "Идеально для бизнеса, мероприятий и личных встреч.",

        # Menu options
        "menu_title": "ГЛАВНОЕ МЕНЮ",
        "menu_option1": "Создать QR-код с настройками",
        "menu_option2": "Быстрая генерация",
        "menu_option3": "Создать базовую визитку (vCard)",
        "menu_option4": "Создать визитку с GPS и адресом",
        "menu_option5": "Визитка с вашим заголовком",
        "menu_option6": "О программе",
        "menu_option0": "Выход",
        "menu_prompt": "Выберите действие (0-6): ",

        # Common
        "back": "Назад",
        "exit": "Выход",
        "continue": "Продолжить",
        "cancel": "Отмена",
        "save": "Сохранить",
        "error": "Ошибка",
        "success": "Успех",
        "warning": "Предупреждение",
        "select": "Выбрать",
        "enter": "Ввести",
        "choose": "Выберите",
        "default": "По умолчанию",
        "custom": "Свой",

        # Content types
        "content_choice_title": "ВЫБЕРИТЕ ТИП КОНТЕНТА",
        "content_option1": "Простой текст или ссылка",
        "content_option2": "Базовая визитка (vCard)",
        "content_option3": "Визитка с GPS и адресом",
        "content_option4": "Только контактные данные (текст)",
        "content_prompt": "Выберите тип (0-4): ",

        # QR styles
        "styles": {
            "1": {"name": "Классический", "desc": "Стандартные квадратные модули"},
            "2": {"name": "Круглый", "desc": "Круглые точки (современный стиль)"},
            "3": {"name": "Скругленный", "desc": "Модули со скругленными углами"},
            "4": {"name": "Минимализм", "desc": "Квадраты с промежутками"},
        },

        "shapes": {
            "1": {"name": "Прямоугольник", "desc": "Стандартная прямоугольная форма QR-кода"},
            "2": {"name": "Скругленные углы", "desc": "QR-код со скругленными углами (современно)"},
        },

        "frames": {
            "1": {"name": "Без обводки", "desc": "Простой QR-код без обрамления"},
            "2": {"name": "Простая обводка", "desc": "Тонкая линия вокруг QR-кода"},
            "3": {"name": "Двойная обводка", "desc": "Две концентрические линии"},
            "4": {"name": "Толстая обводка", "desc": "Жирная рамка вокруг QR-кода"},
            "5": {"name": "VISIT CARD", "desc": "Рамка с надписью VISIT CARD"},
            "6": {"name": "BUSINESS CARD", "desc": "Рамка с надписью BUSINESS CARD"},
            "7": {"name": "CONTACT", "desc": "Рамка с надписью CONTACT"},
            "8": {"name": "Свой заголовок", "desc": "Рамка с вашим собственным текстом"},
        },

        "color_themes": {
            "1": {"name": "Черно-белый", "fg": "#000000", "bg": "#FFFFFF", "outline": "#000000",
                  "desc": "Классический контрастный стиль"},
            "2": {"name": "Синий", "fg": "#0066CC", "bg": "#FFFFFF", "outline": "#004488",
                  "desc": "Корпоративный синий на белом"},
            "3": {"name": "Зеленый", "fg": "#00AA00", "bg": "#FFFFFF", "outline": "#008800",
                  "desc": "Свежий зеленый на белом"},
            "4": {"name": "Красный", "fg": "#CC0000", "bg": "#FFFFFF", "outline": "#AA0000",
                  "desc": "Яркий красный для акцентов"},
            "5": {"name": "Фиолетовый", "fg": "#6600CC", "bg": "#FFFFFF", "outline": "#5500AA",
                  "desc": "Креативный фиолетовый"},
            "6": {"name": "Оранжевый", "fg": "#FF6600", "bg": "#FFFFFF", "outline": "#DD5500",
                  "desc": "Энергичный оранжевый"},
            "7": {"name": "vCard Стиль", "fg": "#1E88E5", "bg": "#FFFFFF", "outline": "#0D47A1",
                  "desc": "Специальный стиль для визиток"},
            "8": {"name": "Профессиональный", "fg": "#2E7D32", "bg": "#FFFFFF", "outline": "#1B5E20",
                  "desc": "Сдержанный зеленый для бизнеса"},
            "9": {"name": "Премиум золото", "fg": "#000000", "bg": "#FFFFFF", "outline": "#D4AF37",
                  "desc": "Черно-белый с золотой обводкой"},
            "10": {"name": "Серый металлик", "fg": "#333333", "bg": "#FFFFFF", "outline": "#666666",
                   "desc": "Современный серый стиль"},
            "11": {"name": "Локация", "fg": "#008080", "bg": "#FFFFFF", "outline": "#006666",
                   "desc": "Бирюзовый стиль для визиток с адресом"},
            "12": {"name": "Карта", "fg": "#D35400", "bg": "#FFFFFF", "outline": "#A04000",
                   "desc": "Терракотовый для GPS меток"},
        },

        # Text prompts
        "enter_text": "Введите текст: ",
        "enter_text_or_link": "Введите текст/ссылку: ",
        "text_too_long": "Текст слишком длинный. Максимум 4000 символов.",
        "text_cannot_be_empty": "Текст не может быть пустым. Попробуйте еще раз.",
        "enter_phone": "Телефон (например, +79991234567): ",
        "enter_email": "Email: ",
        "enter_first_name": "Имя: ",
        "enter_last_name": "Фамилия: ",
        "enter_company": "Компания (не обязательно): ",
        "enter_job_title": "Должность (не обязательно): ",
        "enter_website": "Веб-сайт (не обязательно): ",

        # GPS
        "gps_title": "ДОБАВЛЕНИЕ GPS КООРДИНАТ",
        "gps_instructions": "Вы можете добавить координаты местоположения\nФормат: широта,долгота (например: 53.9045,27.5615)\nМожно получить координаты в Google Maps или Яндекс.Картах\nОставьте поле пустым, если не хотите добавлять координаты",
        "gps_prompt": "Введите координаты (широта,долгота): ",
        "gps_invalid_format": "Неверный формат. Используйте: широта,долгота",
        "gps_invalid_range": "Неверный диапазон координат.\nШирота: -90 до 90, Долгота: -180 до 180",
        "gps_invalid_number": "Неверный формат. Используйте числа.",
        "gps_added": "GPS координаты добавлены: ",
        "try_again_or_skip": "Попробуйте еще раз или нажмите Enter чтобы пропустить",

        # Address
        "address_title": "ДОБАВЛЕНИЕ АДРЕСА",
        "address_instructions": "Вы можете добавить полный адрес\nПример: ул. Ленина 10, Минск, Беларусь, 220000\nОставьте поле пустым, если не хотите добавлять адрес",
        "address_prompt": "Введите адрес: ",
        "address_added": "Адрес добавлен: ",
        "address_optional": "Адрес (не обязательно): ",

        # Frame text
        "frame_text_title": "ВВЕДИТЕ ВАШ ТЕКСТ ДЛЯ РАМКИ",
        "frame_text_instructions": "Текст будет отображаться в верхней части рамки QR-кода\nПримеры:\n  • МОЯ ВИЗИТКА\n  • CONTACT ME\n  • SCAN FOR INFO\n  • DIMA CHARNUkHA\n  • MOEX AQA",
        "frame_text_prompt": "Введите текст (максимум 20 символов): ",
        "frame_text_too_long": "Текст слишком длинный. Максимум 20 символов.",

        # File save
        "save_title": "СОХРАНЕНИЕ РЕЗУЛЬТАТА",
        "save_instructions": "Файл будет сохранен в формате PNG",
        "save_prompt": "Имя файла (по умолчанию: {default_name}): ",
        "file_exists": "Файл '{filename}' уже существует. Перезаписать? (да/нет): ",
        "file_saved": "Файл сохранен: ",
        "enter_different_name": "Введите другое имя файла.",

        # Colors
        "color_choice": "ВЫБОР ЦВЕТА",
        "frame_color_title": "ВЫБОР ЦВЕТА ОБВОДКИ",
        "text_color_title": "ЦВЕТ ТЕКСТА НА РАМКЕ",
        "choose_text_color": "Выберите цвет текста в рамке:",
        "text_color_auto": "Автоматический (контрастный к рамке)",
        "text_color_white": "Белый",
        "text_color_black": "Черный",
        "text_color_gold": "Золотой (#FFD700)",
        "text_color_silver": "Серебряный (#C0C0C0)",
        "contrast_black": "Выбран контрастный черный текст",
        "contrast_white": "Выбран контрастный белый текст",
        "white_selected": "Выбран белый текст",
        "black_selected": "Выбран черный текст",
        "gold_selected": "Выбран золотой текст (#FFD700)",
        "silver_selected": "Выбран серебряный текст (#C0C0C0)",

        # Frame color options
        "frame_color_auto": "Автоматический (немного темнее основного цвета)",
        "frame_color_white": "Белый",
        "frame_color_black": "Черный",
        "frame_color_contrast": "Контрастный (противоположный фону)",
        "frame_color_custom": "Ввести свой цвет",
        "auto_color_selected": "Выбран автоматический цвет: ",
        "white_color_selected": "Выбран белый цвет",
        "black_color_selected": "Выбран черный цвет",
        "contrast_black_selected": "Выбран контрастный цвет: черный",
        "contrast_white_selected": "Выбран контрастный цвет: белый",

        # Custom color input
        "custom_color_title": "ВВЕДИТЕ ЦВЕТ ОБВОДКИ",
        "color_examples": "Примеры цветов:",
        "gps_color_suggestions": "Популярные цвета для визиток с GPS:\n  #008080 - бирюзовый (локация)\n  #D35400 - терракотовый (карта)\n  #0D47A1 - темно-синий (официально)",
        "frame_color_suggestions": "Популярные цвета для рамок с текстом:\n  #0D47A1 - темно-синий (официально)\n  #D4AF37 - золотой (премиум)\n  #424242 - темно-серый (минимализм)\n  #2E7D32 - зеленый (бизнес)",
        "vcard_color_recommendations": "Рекомендация для визиток:\n   • Синий (#1E88E5) - профессионально\n   • Темно-синий (#0D47A1) - контрастно",
        "color_format": "Введите цвет в формате #RRGGBB\n(например: #FF0000 для красного)",
        "color_prompt": "Введите цвет: ",
        "invalid_color_format": "Неверный формат цвета. Используйте HEX, например: #FF0000 или #F00",
        "color_must_start_hash": "Цвет должен начинаться с # и содержать 3, 4, 6 или 7 символов",
        "color_error": "Ошибка определения цвета",
        "contrast_error": "Ошибка определения контраста. Используем белый текст",

        # Generation
        "generation_title": "СОЗДАНИЕ QR-КОДА...",
        "generation_params": "Параметры создания:",
        "generation_success": "QR-КОД УСПЕШНО СОЗДАН!",
        "generation_info": "Информация:",
        "size_pixels": "Размер: {width}x{height} пикселей",
        "file_size": "Размер файла: {size} KB",
        "file_path": "Путь: {path}",

        # Tips
        "business_card_tips": "Советы для визитки:",
        "phone_will_prompt": "При сканировании телефон должен предложить 'Добавить контакт'",
        "your_header": "Ваш заголовок: ",
        "thin_frame": "Тонкая рамка, текст близко к QR-коду",
        "contains_gps": "Визитка содержит GPS координаты",
        "can_open_in_maps": "Можно открыть в картах",
        "try_other_scanner": "Если не предлагает, попробуйте другой сканер QR-кодов",
        "print_minimum": "Распечатайте в размере не менее 4x4 см",

        "general_tips": "Советы:",
        "check_with_phone": "Проверьте сканирование телефоном",
        "print_minimum_small": "Распечатайте в размере не менее 3x3 см",

        # About
        "about_title": "О ПРОГРАММЕ",
        "version": "Генератор QR-кодов с GPS и адресом v9.0",
        "new_features": "НОВЫЕ ВОЗМОЖНОСТИ:",
        "feature1": "• Добавление GPS координат в визитку",
        "feature2": "• Включение полного адреса",
        "feature3": "• 2 новые цветовые темы для локаций",
        "feature4": "• Автоматическое форматирование координат",

        "gps_features": "GPS ФУНКЦИИ:",
        "gps1": "• Поддержка формата: широта,долгота",
        "gps2": "• Проверка корректности координат",
        "gps3": "• Добавление в vCard как GEO тег",
        "gps4": "• Текстовое представление для удобства",

        "address_features": "АДРЕСНЫЕ ФУНКЦИИ:",
        "address1": "• Полный адрес в любом формате",
        "address2": "• Добавление в vCard как ADR тег",
        "address3": "• Сохранение в текстовом виде",

        "design_features": "ДИЗАЙН:",
        "design1": "• 2 формы QR-кодов",
        "design2": "• 4 стиля точек",
        "design3": "• 12 цветовых тем (2 новые для GPS)",
        "design4": "• 8 типов обводки",

        "compatibility": "СОВМЕСТИМОСТЬ:",
        "comp1": "• 100% совместимость со сканерами QR-кодов",
        "comp2": "• Автоматическое распознавание визиток",
        "comp3": "• GPS координаты открываются в картах",
        "comp4": "• Поддержка Android и iOS",

        # VCard
        "vcard_title": "СОЗДАНИЕ ЭЛЕКТРОННОЙ ВИЗИТКИ (vCard)",
        "vcard_subtitle": "Заполните данные для создания QR-кода визитки\nПри сканировании телефон предложит добавить контакт",
        "personal_data": "ЛИЧНЫЕ ДАННЫЕ",
        "contact_info": "КОНТАКТНАЯ ИНФОРМАЦИЯ",
        "additional_info": "ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ",
        "business_card_created": "Визитка создана!",
        "vcard_structure": "Структура QR-кода:",
        "vcard_structure1": "1. vCard данные (для добавления в контакты)",
        "vcard_structure2": "2. Текстовое представление (для просмотра)",

        # Contact text
        "contact_text_title": "ВВЕДИТЕ КОНТАКТНЫЕ ДАННЫЕ",
        "contact_instructions": "Эти данные будут видны при сканировании QR-кода",
        "personal_details": "Личные данные:",
        "name_prompt": "Имя и фамилия: ",
        "contact_details": "Контактная информация:",
        "additional_details": "Дополнительная информация:",
        "coordinates_optional": "координаты (не обязательно):",
        "gps_format_example": "Формат: широта,долгота (например: 53.9045,27.5615)",
        "coordinates_prompt": "Координаты: ",

        # Quick generation
        "quick_generate_title": "БЫСТРАЯ ГЕНЕРАЦИЯ",
        "quick_generate_prompt": "Введите текст/ссылку: ",

        # Language selection
        "language_title": "ВЫБОР ЯЗЫКА",
        "language_prompt": "Выберите язык (1-English, 2-Русский): ",
        "language_selected": "Выбран язык: ",

        # Yes/No prompts
        "open_file": "Открыть файл? (да/нет): ",
        "return_to_menu": "Вернуться в главное меню? (да/нет): ",
        "proceed": "Начать создание? (да/нет): ",
        "change_frame_color": "Изменить цвет рамки? (да/нет): ",
        "change_text_color": "Изменить цвет текста? (да/нет): ",

        # Errors
        "unexpected_error": "Неожиданная ошибка: ",
        "please_restart": "Пожалуйста, перезапустите программу",
        "user_interrupted": "Программа прервана пользователем",
        "creation_error": "Ошибка при создании QR-кода: ",
        "try_simplify": "Попробуйте:",
        "simplify_text": "• Упростить текст",
        "simpler_style": "• Использовать более простой стиль",
        "different_color": "• Выбрать другой цвет",
        "check_vcard": "• Убедитесь, что vCard начинается с BEGIN:VCARD",
        "try_again": "Попробуйте еще раз.",
        "enter_number_from_to": "Введите число от",

        # Text examples
        "text_examples": "Примеры:\n  • https://example.com\n  • Любое сообщение или текст\n  • Контактные данные вручную",

        # Design recommendations
        "shape_recommendations": "💡 Для визиток рекомендуется:\n   • Скругленные углы - современный стиль\n   • Прямоугольник - классический вид",
        "style_recommendations": "💡 Для визиток рекомендуется:\n   • Круглый - современные смартфоны\n   • Классический - максимальная читаемость",
        "gps_theme_recommendations": "💡 Специальные темы для визиток с GPS:\n   11. Локация - бирюзовый, для адресов\n   12. Карта - терракотовый, для GPS меток",
        "vcard_theme_recommendations": "💡 Специальные темы для визиток:\n   7. vCard Стиль - синий, для контактов\n   8. Профессиональный - зеленый, для бизнеса\n   9. Премиум золото - с золотой обводкой\n   10. Серый металлик - современный стиль",

        # Selection
        "selected_colors": "Выбранные цвета",
        "main_qr_color": "Основной цвет QR-кода",
        "background_color": "Цвет фона",
        "default_frame_color": "Цвет обводки по умолчанию",
        "final_color_params": "Итоговые параметры цвета",
        "qr_color": "Цвет QR-кода",
        "frame_color": "Цвет обводки",
        "frame_text_color": "Цвет текста в рамке",

        # Generation messages
        "creating_image_with_color": "Создаю изображение с цветом",
        "on": "на",
        "styled_image_created": "Стилизованное изображение создано успешно",
        "styled_image_error": "Не удалось создать стилизованное изображение",
        "trying_standard_image": "Пробую создать стандартное изображение...",
        "standard_image_created": "Стандартное изображение создано успешно",
        "adding_frame": "Добавляю обводку",
        "saving_file": "Сохраняю файл",

        # GPS business card
        "create_gps_business_card": "Создайте визитку с координатами и адресом\nИдеально для бизнеса, мероприятий, встреч",
        "header_selected": "Выбран заголовок",
        "gps_card_settings": "Используем оптимальные настройки:\n• Форма: Скругленные углы\n• Стиль: Классический (макс. читаемость)\n• Цвет: Локация (бирюзовый)\n• Рамка: Тонкая с текстом\n• Текст: Близко к QR-коду",
        "current_color": "Текущий цвет",
        "current_text_color": "Текущий цвет текста",
        "contains_gps_address": "Визитка содержит GPS и адрес",
        "thin_frame_close_text": "Тонкая рамка, текст близко к QR-коду",
        "file": "Файл",

        # Quick creation
        "quick_business_card_steps": "Создайте QR-код визитки за 3 шага:\n1. Заполните данные\n2. Выберите дизайн\n3. Сохраните QR-код",
        "quick_design_for_business_card": "БЫСТРЫЙ ДИЗАЙН ДЛЯ ВИЗИТКИ",
        "recommended_settings": "Используем рекомендованные настройки:\n• Форма: Скругленные углы\n• Стиль: Круглый\n• Цвет: vCard Стиль (синий)\n• Обводка: Простая, синяя",

        # Custom header
        "create_custom_header_business_card": "Создайте визитку с вашим текстом в рамке",
        "settings_for_business_card": "НАСТРОЙКИ ДЛЯ ВИЗИТКИ",
        "optimal_settings": "Используем оптимальные настройки:\n• Форма: Скругленные углы\n• Стиль: Классический\n• Цвет: vCard Стиль (синий)\n• Рамка: Тонкая с текстом",

        # Business card creation
        "creating_business_card_qr": "Создаю QR-код визитки...",
        "customize_business_card_appearance": "Настройте внешний вид QR-кода визитки:",
        "data_format": "ФОРМАТ ДАННЫХ:",
        "optimized_vcard_format": "Используется оптимизированный vCard формат",
        "vcard_for_contacts": "vCard данные (для добавления в контакты)",
        "text_for_viewing": "Текстовое представление (для просмотра)",
        "guaranteed_scanner_compatibility": "Гарантированная совместимость со сканерами",
        "creating_gps_business_card_qr": "Создаю QR-код визитки с GPS...",
        "customize_gps_business_card_appearance": "Настройте внешний вид QR-кода визитки:",
        "includes_gps_address": "Включены GPS координаты и адрес",

        # Quick generate
        "creating_qr": "Создаю QR-код...",
        "qr_created": "QR-код создан",

        # Goodbye
        "goodbye": "До свидания! Спасибо за использование программы!",

        # Header
        "header": "Заголовок",

        # Using simple frame
        "using_simple_frame": "Используется простая рамка без текста",
    }

    def __init__(self):
        self.current_lang = "en"
        self.texts = self.EN

    def select_language(self) -> str:
        """Allow user to select language"""
        print("\n" + "=" * 60)
        print(self.EN["language_title"])
        print("=" * 60)

        for i, (code, name) in enumerate(self.LANGUAGES.items(), 1):
            print(f"{i}. {name}")

        while True:
            choice = input(self.EN["language_prompt"]).strip()
            if choice == "1":
                self.current_lang = "en"
                self.texts = self.EN
                print(f"{self.EN['language_selected']}English")
                return "en"
            elif choice == "2":
                self.current_lang = "ru"
                self.texts = self.RU
                print(f"{self.RU['language_selected']}Русский")
                return "ru"
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def t(self, key: str, **kwargs) -> str:
        """Get translated text with optional formatting"""
        text = self.texts.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except:
                return text
        return text

    def get_yes_no(self, prompt_key: str) -> bool:
        """Get yes/no answer based on language"""
        response = input(self.t(prompt_key)).lower()
        if self.current_lang == "ru":
            return response in ['да', 'д', 'y', 'yes']
        else:
            return response in ['yes', 'y', 'да', 'д']


# Initialize language manager
lang = LanguageManager()


class QRGenerator:
    """QR code generator with various styles and frames"""

    def __init__(self):
        # Load styles from language manager
        self.STYLES = lang.t("styles")
        self.SHAPES = lang.t("shapes")
        self.FRAMES = lang.t("frames")
        self.COLOR_THEMES = lang.t("color_themes")

    @staticmethod
    def validate_text(text: str) -> bool:
        """Validates input text for emptiness."""
        return len(text.strip()) > 0

    @staticmethod
    def create_rounded_mask(size: int, radius: int = 40) -> Image.Image:
        """Creates rounded corner mask."""
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
        return mask

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Converts HEX color to RGB."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c * 2 for c in hex_color)
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def add_outline_to_image(image: Image.Image, outline_type: str,
                             outline_color: str = "#000000", outline_width: int = 10,
                             text_color: str = "#FFFFFF", custom_text: str = "") -> Image.Image:
        """Adds outline to QR code image."""
        if outline_type == "1":  # No outline
            return image

        # Convert to RGBA if needed
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        width, height = image.size

        # Determine frame text
        frame_text = ""
        if outline_type == "5":  # VISIT CARD
            frame_text = "VISIT CARD"
        elif outline_type == "6":  # BUSINESS CARD
            frame_text = "BUSINESS CARD"
        elif outline_type == "7":  # CONTACT
            frame_text = "CONTACT"
        elif outline_type == "8":  # Custom header
            frame_text = custom_text if custom_text else lang.t("custom")

        # Determine outline thickness - make it THINNER
        if outline_type in ["5", "6", "7", "8"]:  # Frames with text
            thickness = max(15, height // 20)  # THINNER: 1/20 height or 15px minimum
        elif outline_type == "2":  # Simple outline
            thickness = outline_width
        elif outline_type == "3":  # Double outline
            thickness = outline_width * 2
        elif outline_type == "4":  # Thick outline
            thickness = outline_width * 3
        else:
            thickness = outline_width

        # Create new image with transparent background
        new_width = width + thickness * 2
        new_height = height + thickness * 2

        # For text frames add minimal additional space
        if outline_type in ["5", "6", "7", "8"]:
            text_area_height = max(20, thickness // 3)  # Very small area for text
        else:
            text_area_height = 0

        outlined = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(outlined)

        # Draw main outline
        if outline_type in ["5", "6", "7", "8"]:  # Frames with text
            draw.rectangle([0, 0, new_width, new_height], fill=outline_color)

            # Add text INSIDE frame, close to QR code
            try:
                font_size = min(new_width // 15, new_height // 20)
                font_size = max(20, font_size)

                font_paths = [
                    "arialbd.ttf",  # Arial Bold
                    "arial.ttf",  # Arial
                    "Arial",  # Mac/Linux
                    "/System/Library/Fonts/Helvetica.ttc",  # macOS
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
                    "C:\\Windows\\Fonts\\arialbd.ttf",  # Windows
                ]

                font = None
                for font_path in font_paths:
                    try:
                        font = ImageFont.truetype(font_path, font_size)
                        break
                    except:
                        continue

                if font is None:
                    font = ImageFont.load_default()
                    font_size = max(24, new_width // 12)

                # Calculate text width for centering
                try:
                    text_bbox = draw.textbbox((0, 0), frame_text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                except:
                    text_width = len(frame_text) * font_size // 2
                    text_height = font_size

                text_x = (new_width - text_width) // 2
                text_y = max(5, thickness // 5)

                # Draw text with light shadow for better readability
                shadow_offset = 1
                shadow_color = "#000000" if text_color != "#000000" else "#333333"
                draw.text((text_x + shadow_offset, text_y + shadow_offset),
                          frame_text, fill=shadow_color, font=font)
                draw.text((text_x, text_y), frame_text, fill=text_color, font=font)

            except Exception as e:
                print(f"⚠️  {lang.t('error')}: {e}")
                print(lang.t("using_simple_frame"))

        elif outline_type == "3":  # Double outline
            draw.rectangle([0, 0, new_width, new_height], fill=outline_color)
            inner_color = QRGenerator._adjust_color(outline_color, 50)
            inner_thickness = thickness // 4
            draw.rectangle(
                [inner_thickness, inner_thickness,
                 new_width - inner_thickness, new_height - inner_thickness],
                fill=inner_color
            )
        else:
            draw.rectangle([0, 0, new_width, new_height], fill=outline_color)

        # Determine QR code position
        if outline_type in ["5", "6", "7", "8"]:
            qr_x = thickness
            qr_y = thickness + text_area_height // 2
        else:
            qr_x = thickness
            qr_y = thickness

        # Insert QR code
        outlined.paste(image, (qr_x, qr_y), image)
        return outlined

    @staticmethod
    def _adjust_color(hex_color: str, adjustment: int) -> str:
        """Adjusts color brightness."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c * 2 for c in hex_color)

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        r = max(0, min(255, r + adjustment))
        g = max(0, min(255, g + adjustment))
        b = max(0, min(255, b + adjustment))

        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def apply_shape_to_image(image: Image.Image, shape_type: str, bg_color: str = "#FFFFFF") -> Image.Image:
        """Applies shape to image."""
        if shape_type == "1":  # Rectangle
            return image

        elif shape_type == "2":  # Rounded corners
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            width, height = image.size
            radius = min(40, width // 10, height // 10)

            mask = QRGenerator.create_rounded_mask(max(width, height), radius)
            mask = mask.resize((width, height))

            result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            result.paste(image, (0, 0), mask)

            background = Image.new('RGBA', (width, height), bg_color)
            background.paste(result, (0, 0), result)

            return background

        return image


class VCardGenerator:
    """vCard (electronic business card) generator"""

    @staticmethod
    def get_gps_coordinates():
        """Gets GPS coordinates from user."""
        print(f"\n📍 {lang.t('gps_title')}")
        print("-" * 40)
        print(lang.t("gps_instructions"))
        print()

        while True:
            gps_input = input(f"👉 {lang.t('gps_prompt')}").strip()

            if not gps_input:
                return None

            if ',' in gps_input:
                parts = gps_input.split(',')
                if len(parts) == 2:
                    try:
                        lat = float(parts[0].strip())
                        lon = float(parts[1].strip())

                        if -90 <= lat <= 90 and -180 <= lon <= 180:
                            return f"{lat:.6f},{lon:.6f}"
                        else:
                            print(f"❌ {lang.t('gps_invalid_range')}")
                    except ValueError:
                        print(f"❌ {lang.t('gps_invalid_number')}")
                else:
                    print(f"❌ {lang.t('gps_invalid_format')}")
            else:
                print(f"❌ {lang.t('gps_invalid_format')}")

            print(lang.t("try_again_or_skip"))

    @staticmethod
    def get_address():
        """Gets address from user."""
        print(f"\n🏠 {lang.t('address_title')}")
        print("-" * 40)
        print(lang.t("address_instructions"))
        print()

        address = input(f"👉 {lang.t('address_prompt')}").strip()
        return address if address else None

    @staticmethod
    def get_location_data(with_gps: bool = False, with_address: bool = False):
        """Gets both GPS and address data if needed."""
        gps_coordinates = None
        address = None

        if with_gps:
            gps_coordinates = VCardGenerator.get_gps_coordinates()
            if gps_coordinates:
                print(f"✅ {lang.t('gps_added')}{gps_coordinates}")

        if with_address:
            address = VCardGenerator.get_address()
            if address:
                print(f"✅ {lang.t('address_added')}{address}")

        return gps_coordinates, address

    @staticmethod
    def create_vcard(with_gps: bool = False, with_address: bool = False):
        """Creates vCard from user data."""
        print(f"\n📇 {lang.t('vcard_title')}")
        print("=" * 60)
        print(lang.t("vcard_subtitle"))
        print()

        print(f"👤 {lang.t('personal_data')}")
        print("-" * 40)
        first_name = input(lang.t("enter_first_name")).strip()
        last_name = input(lang.t("enter_last_name")).strip()

        print(f"\n📞 {lang.t('contact_info')}")
        print("-" * 40)
        phone = input(lang.t("enter_phone")).strip()
        email = input(lang.t("enter_email")).strip()

        print(f"\n💼 {lang.t('additional_info')}")
        print("-" * 40)
        company = input(lang.t("enter_company")).strip()
        job_title = input(lang.t("enter_job_title")).strip()
        website = input(lang.t("enter_website")).strip()

        gps_coordinates = None
        address = None

        # Get GPS and address data if needed
        if with_gps or with_address:
            print(f"\n📍 GETTING LOCATION DATA")
            print("-" * 40)
            gps_coordinates, address = VCardGenerator.get_location_data(with_gps, with_address)

        vcard_lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"N:{last_name};{first_name};;;",
            f"FN:{first_name} {last_name}",
        ]

        if phone:
            vcard_lines.append(f"TEL;TYPE=CELL,VOICE:{phone}")

        if email:
            vcard_lines.append(f"EMAIL;TYPE=WORK,INTERNET:{email}")

        if company:
            vcard_lines.append(f"ORG:{company}")

        if job_title:
            vcard_lines.append(f"TITLE:{job_title}")

        if website:
            vcard_lines.append(f"URL:{website}")

        if gps_coordinates:
            vcard_lines.append(f"GEO:{gps_coordinates}")
            vcard_lines.append(f"NOTE:GPS coordinates: {gps_coordinates}")

        if address:
            vcard_lines.append(f"ADR;TYPE=WORK,PREF:;;{address};;;;")
            vcard_lines.append(f"NOTE:Address: {address}")

        current_time = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        vcard_lines.append(f"REV:{current_time}")
        vcard_lines.append("END:VCARD")

        vcard_text = "\n".join(vcard_lines)

        contact_info = f"""
========================================
CONTACT INFORMATION

👤 Name: {first_name} {last_name}
📞 Phone: {phone}
📧 Email: {email}
"""

        if company:
            contact_info += f"🏢 Company: {company}\n"
        if job_title:
            contact_info += f"💼 Position: {job_title}\n"
        if website:
            contact_info += f"🌐 Website: {website}\n"

        if gps_coordinates:
            contact_info += f"📍 GPS coordinates: {gps_coordinates}\n"
            contact_info += f"   (copy to Google Maps or Yandex Maps)\n"

        if address:
            contact_info += f"🏠 Address: {address}\n"

        contact_info += f"\n📅 Created: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        contact_info += f"\n📱 QR-code generated by QR Generator"

        combined_text = f"""{vcard_text}

{contact_info}
"""

        print(f"\n✅ {lang.t('business_card_created')}")
        print(f"👤 Name: {first_name} {last_name}")
        print(f"📞 Phone: {phone}")
        print(f"📧 Email: {email}")

        if company:
            print(f"🏢 Company: {company}")

        if gps_coordinates:
            print(f"📍 GPS coordinates: {gps_coordinates}")

        if address:
            print(f"🏠 Address: {address}")

        print(f"\n📊 {lang.t('vcard_structure')}:")
        print(f"   1. {lang.t('vcard_structure1')}")
        print(f"   2. {lang.t('vcard_structure2')}")

        return combined_text, vcard_text


def display_intro():
    """Shows welcome message."""
    print("\n" + "=" * 60)
    print(f"📱 {lang.t('main_title')}")
    print("=" * 60)
    print(f"\n{lang.t('main_subtitle')}")
    print(f"{lang.t('perfect_for')}")
    print()


def get_content_choice():
    """Gets content type choice for QR code."""
    print(f"\n📝 {lang.t('content_choice_title')}")
    print("=" * 60)
    print(f"1. 📋 {lang.t('content_option1')}")
    print(f"2. 📇 {lang.t('content_option2')}")
    print(f"3. 📍 {lang.t('content_option3')}")
    print(f"4. 📞 {lang.t('content_option4')}")
    print(f"0. ↩️  {lang.t('back')}")

    while True:
        choice = input(f"\n👉 {lang.t('content_prompt')}").strip()
        if choice in ["0", "1", "2", "3", "4"]:
            return choice
        print(f"❌ {lang.t('error')}. {lang.t('try_again')}")


def get_text_input():
    """Gets text for QR code."""
    print(f"\n📝 TEXT OR LINK INPUT")
    print("-" * 40)
    print(lang.t("text_examples"))
    print()

    while True:
        text = input(f"👉 {lang.t('enter_text')}").strip()
        if text:
            if len(text) > 4000:
                print(f"⚠️  {lang.t('text_too_long')}")
                continue
            return text
        print(f"❌ {lang.t('text_cannot_be_empty')}")


def get_contact_text():
    """Gets contact data in text format."""
    print(f"\n👤 {lang.t('contact_text_title')}")
    print("-" * 40)
    print(lang.t("contact_instructions"))
    print()

    print(f"👤 {lang.t('personal_details')}")
    name = input(lang.t("name_prompt")).strip()

    print(f"\n📞 {lang.t('contact_details')}")
    phone = input(lang.t("enter_phone")).strip()
    email = input(lang.t("enter_email")).strip()

    print(f"\n💼 {lang.t('additional_details')}")
    company = input(lang.t("enter_company")).strip()
    position = input(lang.t("enter_job_title")).strip()
    website = input(lang.t("enter_website")).strip()

    print(f"\n📍 {lang.t('coordinates_optional')}")
    print(lang.t("gps_format_example"))
    gps = input(lang.t("coordinates_prompt")).strip()

    print(f"\n🏠 {lang.t('address_optional')}")
    address = input(lang.t("address_prompt")).strip()

    contact_text = f"""CONTACT INFORMATION

👤 {name}

📞 Phone: {phone}
📧 Email: {email}
"""

    if company:
        contact_text += f"🏢 Company: {company}\n"
    if position:
        contact_text += f"💼 Position: {position}\n"
    if website:
        contact_text += f"🌐 Website: {website}\n"
    if gps:
        contact_text += f"📍 GPS coordinates: {gps}\n"
    if address:
        contact_text += f"🏠 Address: {address}\n"

    contact_text += f"\n📅 Created: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    contact_text += f"\n📱 QR-code generated by QR Generator"

    return contact_text


def select_option(title: str, options: dict) -> str:
    """Shows selection menu with descriptions."""
    print(f"\n{title}")
    print("-" * 40)

    for key, option in options.items():
        print(f"  {key}. {option['name']}")
        print(f"     {option['desc']}")

    while True:
        choice = input(f"\n👉 {lang.t('choose')} (1-{len(options)}): ").strip()
        if choice in options:
            return choice
        print(f"❌ {lang.t('error')}. {lang.t('enter_number_from_to')} 1-{len(options)}")


def get_output_filename(default_name: str = "my_qr") -> str:
    """Gets filename for saving."""
    print(f"\n💾 {lang.t('save_title')}")
    print("-" * 40)
    print(lang.t("save_instructions"))
    print()

    while True:
        filename = input(lang.t("save_prompt", default_name=default_name)).strip()

        if not filename:
            filename = default_name

        filename = "".join(c for c in filename if c.isalnum() or c in ('-', '_', ' '))
        if not filename:
            filename = "qr_code"

        filename = filename.replace(' ', '_')

        if not filename.lower().endswith('.png'):
            filename = f"{filename}.png"

        if os.path.exists(filename):
            overwrite = input(lang.t("file_exists", filename=filename)).lower()
            if lang.current_lang == "ru":
                if overwrite not in ['да', 'д', 'y', 'yes']:
                    print(lang.t("enter_different_name"))
                    continue
            else:
                if overwrite not in ['yes', 'y', 'да', 'д']:
                    print(lang.t("enter_different_name"))
                    continue

        return filename


def get_custom_frame_text():
    """Gets custom text for frame."""
    print(f"\n🏷️  {lang.t('frame_text_title')}")
    print("-" * 40)
    print(lang.t("frame_text_instructions"))
    print()

    while True:
        text = input(f"👉 {lang.t('frame_text_prompt')}").strip()
        if text:
            if len(text) > 20:
                print(f"⚠️  {lang.t('frame_text_too_long')}")
                continue
            return text.upper()
        print(f"❌ {lang.t('text_cannot_be_empty')}")


def get_text_color_for_outline(outline_color: str) -> str:
    """Determines text color for frame."""
    print(f"\n🎨 {lang.t('text_color_title')}")
    print("-" * 40)
    print(lang.t("choose_text_color"))
    print(f"1. {lang.t('text_color_auto')}")
    print(f"2. {lang.t('text_color_white')}")
    print(f"3. {lang.t('text_color_black')}")
    print(f"4. {lang.t('text_color_gold')}")
    print(f"5. {lang.t('text_color_silver')}")

    while True:
        choice = input(f"\n👉 {lang.t('choose')} (1-5): ").strip()
        if choice == "1":  # Automatic contrast
            try:
                hex_color = outline_color.lstrip('#')
                if len(hex_color) == 3:
                    hex_color = ''.join(c * 2 for c in hex_color)
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                brightness = (r * 299 + g * 587 + b * 114) / 1000

                if brightness > 128:
                    text_color = "#000000"
                    print(f"✅ {lang.t('contrast_black')}")
                else:
                    text_color = "#FFFFFF"
                    print(f"✅ {lang.t('contrast_white')}")
                return text_color
            except:
                print(f"⚠️  {lang.t('contrast_error')}")
                return "#FFFFFF"

        elif choice == "2":  # White
            print(f"✅ {lang.t('white_selected')}")
            return "#FFFFFF"

        elif choice == "3":  # Black
            print(f"✅ {lang.t('black_selected')}")
            return "#000000"

        elif choice == "4":  # Gold
            print(f"✅ {lang.t('gold_selected')}")
            return "#FFD700"

        elif choice == "5":  # Silver
            print(f"✅ {lang.t('silver_selected')}")
            return "#C0C0C0"
        else:
            print(f"❌ {lang.t('error')}. {lang.t('try_again')}")


def get_outline_color(main_color: str, bg_color: str, for_vcard: bool = False, for_text_frame: bool = False,
                      with_gps: bool = False) -> str:
    """Determines frame color based on user choice."""
    print(f"\n🎨 {lang.t('frame_color_title')}")
    print("-" * 40)

    if with_gps:
        print(lang.t("gps_color_suggestions"))
        print()
    elif for_vcard and for_text_frame:
        print(lang.t("frame_color_suggestions"))
        print()
    elif for_vcard:
        print(lang.t("vcard_color_recommendations"))
        print()

    print(f"1. {lang.t('frame_color_auto')}")
    print(f"2. {lang.t('frame_color_white')}")
    print(f"3. {lang.t('frame_color_black')}")
    print(f"4. {lang.t('frame_color_contrast')}")
    print(f"5. {lang.t('frame_color_custom')}")

    while True:
        choice = input(f"\n👉 {lang.t('choose')} (1-5): ").strip()
        if choice == "1":  # Automatic
            try:
                hex_color = main_color.lstrip('#')
                if len(hex_color) == 3:
                    hex_color = ''.join(c * 2 for c in hex_color)
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                darker = f"#{max(0, r - 30):02x}{max(0, g - 30):02x}{max(0, b - 30):02x}"
                print(f"✅ {lang.t('auto_color_selected')}{darker}")
                return darker
            except Exception as e:
                print(f"⚠️  {lang.t('color_error')}: {e}")
                return "#000000"

        elif choice == "2":  # White
            print(f"✅ {lang.t('white_color_selected')}")
            return "#FFFFFF"

        elif choice == "3":  # Black
            print(f"✅ {lang.t('black_color_selected')}")
            return "#000000"

        elif choice == "4":  # Contrast
            try:
                hex_color = bg_color.lstrip('#')
                if len(hex_color) == 3:
                    hex_color = ''.join(c * 2 for c in hex_color)
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                brightness = (r * 299 + g * 587 + b * 114) / 1000

                if brightness > 128:
                    print(f"✅ {lang.t('contrast_black_selected')}")
                    return "#000000"
                else:
                    print(f"✅ {lang.t('contrast_white_selected')}")
                    return "#FFFFFF"
            except:
                print(f"⚠️  {lang.t('contrast_error')}")
                return "#000000"

        elif choice == "5":  # Custom color
            print(f"\n🌈 {lang.t('custom_color_title')}")
            print("-" * 40)

            if with_gps:
                print(lang.t("gps_color_suggestions"))
            elif for_text_frame:
                print(lang.t("frame_color_suggestions"))
            else:
                print(lang.t("color_examples"))

            print(f"\n{lang.t('color_format')}")
            print()

            while True:
                color = input(f"👉 {lang.t('color_prompt')}").strip()
                if color.startswith('#') and (len(color) == 7 or len(color) == 4):
                    try:
                        hex_part = color[1:]
                        if len(hex_part) == 3:
                            hex_part = ''.join(c * 2 for c in hex_part)
                        int(hex_part, 16)
                        return f"#{hex_part}"
                    except ValueError:
                        print(f"❌ {lang.t('invalid_color_format')}")
                else:
                    print(f"❌ {lang.t('color_must_start_hash')}")
        else:
            print(f"❌ {lang.t('error')}. {lang.t('try_again')}")


def generate_custom_qr(for_vcard: bool = False, with_gps: bool = False):
    """Generates QR code with custom settings."""
    # Initialize QRGenerator to get translated styles
    qr_gen = QRGenerator()

    print("\n" + "=" * 60)
    print("🔷 SELECT QR CODE SHAPE")
    print("=" * 60)

    if for_vcard:
        print(lang.t("shape_recommendations"))
        print()

    shape_choice = select_option("AVAILABLE SHAPES:", qr_gen.SHAPES)

    print("\n" + "=" * 60)
    print("🎨 SELECT QR CODE DOT STYLE")
    print("=" * 60)

    if for_vcard:
        print(lang.t("style_recommendations"))
        print()

    style_choice = select_option("AVAILABLE STYLES:", qr_gen.STYLES)

    print("\n" + "=" * 60)
    print("🌈 SELECT COLOR THEME")
    print("=" * 60)

    if with_gps:
        print(lang.t("gps_theme_recommendations"))
        print()
    elif for_vcard:
        print(lang.t("vcard_theme_recommendations"))
        print()

    color_choice = select_option("AVAILABLE COLOR THEMES:", qr_gen.COLOR_THEMES)

    color_theme = qr_gen.COLOR_THEMES[color_choice]
    main_color = color_theme["fg"]
    bg_color = color_theme["bg"]
    default_outline = color_theme.get("outline", "#000000")

    print(f"\n🎨 {lang.t('selected_colors')}:")
    print(f"   {lang.t('main_qr_color')}: {main_color}")
    print(f"   {lang.t('background_color')}: {bg_color}")
    print(f"   {lang.t('default_frame_color')}: {default_outline}")

    print("\n" + "=" * 60)
    print("🖌️  FRAME SETTINGS")
    print("=" * 60)

    outline_choice = select_option("FRAME TYPE:", qr_gen.FRAMES)

    outline_color = default_outline
    outline_width = 10
    text_color = "#FFFFFF"
    custom_text = ""

    is_text_frame = outline_choice in ["5", "6", "7", "8"]

    if outline_choice != "1":
        outline_color = get_outline_color(main_color, bg_color, for_vcard, is_text_frame, with_gps)

        if is_text_frame:
            text_color = get_text_color_for_outline(outline_color)

            if outline_choice == "8":
                custom_text = get_custom_frame_text()
                print(f"✅ {lang.t('your_header')}{custom_text}")

    print(f"\n🎨 {lang.t('final_color_params')}:")
    print(f"   {lang.t('qr_color')}: {main_color}")
    print(f"   {lang.t('background_color')}: {bg_color}")
    print(f"   {lang.t('frame_color')}: {outline_color}")
    if is_text_frame:
        print(f"   {lang.t('frame_text_color')}: {text_color}")

    return {
        "shape": shape_choice,
        "style": style_choice,
        "color_theme": color_theme,
        "outline_type": outline_choice,
        "outline_color": outline_color,
        "outline_width": outline_width,
        "text_color": text_color,
        "custom_text": custom_text,
    }


def create_qr_code(text: str, settings: dict, filename: str, is_vcard: bool = False) -> bool:
    """Creates QR code with given parameters."""
    try:
        qr_gen = QRGenerator()

        print("\n" + "=" * 60)
        print(f"🔄 {lang.t('generation_title')}")
        print("=" * 60)

        print(f"⚙️  {lang.t('generation_params')}:")
        print(f"   {lang.t('qr_color')}: {settings['color_theme']['fg']}")
        print(f"   {lang.t('background_color')}: {settings['color_theme']['bg']}")
        print(f"   {lang.t('style')}: {qr_gen.STYLES[settings['style']]['name']}")

        error_correction = qrcode.constants.ERROR_CORRECT_H if is_vcard else qrcode.constants.ERROR_CORRECT_Q
        box_size = 14 if is_vcard else 12

        qr = qrcode.QRCode(
            version=None,
            error_correction=error_correction,
            box_size=box_size,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        style = qr_gen.STYLES[settings["style"]]

        print(
            f"🖌️  {lang.t('creating_image_with_color')} {settings['color_theme']['fg']} {lang.t('on')} {settings['color_theme']['bg']}")

        try:
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=style["drawer"],
                fill_color=settings["color_theme"]["fg"],
                back_color=settings["color_theme"]["bg"]
            ).convert('RGBA')
            print(f"✅ {lang.t('styled_image_created')}")
        except Exception as e:
            print(f"⚠️  {lang.t('styled_image_error')}: {e}")
            print(lang.t("trying_standard_image"))
            img = qr.make_image(
                fill_color=settings["color_theme"]["fg"],
                back_color=settings["color_theme"]["bg"]
            ).convert('RGBA')
            print(f"✅ {lang.t('standard_image_created')}")

        img = QRGenerator.apply_shape_to_image(img, settings["shape"], settings["color_theme"]["bg"])

        if settings["outline_type"] != "1":
            print(f"🖼️  {lang.t('adding_frame')}: {settings['outline_color']}")
            final_image = QRGenerator.add_outline_to_image(
                img,
                settings["outline_type"],
                settings["outline_color"],
                settings["outline_width"],
                settings["text_color"],
                settings.get("custom_text", "")
            )
        else:
            final_image = img

        print(f"💾 {lang.t('saving_file')}: {filename}")
        final_image.save(filename, 'PNG', optimize=True)

        print("\n" + "=" * 60)
        print(f"🎉 {lang.t('generation_success')}")
        print("=" * 60)
        print(f"\n📊 {lang.t('generation_info')}:")
        print(lang.t("size_pixels", width=final_image.size[0], height=final_image.size[1]))
        print(lang.t("file_size", size=os.path.getsize(filename) // 1024))
        print(lang.t("file_path", path=os.path.abspath(filename)))

        if is_vcard:
            print(f"\n💡 {lang.t('business_card_tips')}:")
            print(f"   📱 {lang.t('phone_will_prompt')}")

            if settings["outline_type"] in ["5", "6", "7", "8"]:
                if settings["outline_type"] == "8":
                    print(f"   🏷️  {lang.t('your_header')}{settings.get('custom_text', '')}")
                else:
                    frame_text = {
                        "5": "VISIT CARD",
                        "6": "BUSINESS CARD",
                        "7": "CONTACT"
                    }.get(settings["outline_type"], "")
                    print(f"   🏷️  {lang.t('header')}: {frame_text}")
                print(f"   📏 {lang.t('thin_frame')}")

            if "GEO:" in text:
                print(f"   📍 {lang.t('contains_gps')}")
                print(f"   🗺️  {lang.t('can_open_in_maps')}")

            print(f"   👆 {lang.t('try_other_scanner')}")
            print(f"   🖨️  {lang.t('print_minimum')}")
        else:
            print(f"\n💡 {lang.t('general_tips')}:")
            print(f"   📱 {lang.t('check_with_phone')}")
            print(f"   🖨️  {lang.t('print_minimum_small')}")

        if os.path.exists(filename):
            if lang.get_yes_no("open_file"):
                if os.name == 'nt':
                    os.startfile(filename)
                elif os.name == 'posix':
                    if sys.platform == 'darwin':
                        os.system(f'open "{filename}"')
                    else:
                        os.system(f'xdg-open "{filename}"')

        return True

    except Exception as e:
        print(f"\n❌ {lang.t('creation_error')}{e}")
        import traceback
        traceback.print_exc()
        print(f"\n💡 {lang.t('try_simplify')}:")
        print(f"   • {lang.t('simplify_text')}")
        print(f"   • {lang.t('simpler_style')}")
        print(f"   • {lang.t('different_color')}")
        if is_vcard:
            print(f"   • {lang.t('check_vcard')}")
        return False


def quick_generate():
    """Quick generation with default parameters."""
    print(f"\n⚡ {lang.t('quick_generate_title')}")
    print("-" * 40)

    text = input(f"👉 {lang.t('quick_generate_prompt')}").strip()
    if not text:
        print(f"❌ {lang.t('text_cannot_be_empty')}")
        return

    filename = get_output_filename("quick_qr")

    print(f"\n🔄 {lang.t('creating_qr')}")

    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color="#000000",
            back_color="#FFFFFF"
        )

        img.save(filename)

        print(f"\n✅ {lang.t('qr_created')}: {filename}")
        print(f"📍 {lang.t('file_path', path=os.path.abspath(filename))}")

    except Exception as e:
        print(f"❌ {lang.t('error')}: {e}")


def create_vcard_with_location():
    """Creates business card with GPS and address."""
    print("\n" + "=" * 60)
    print("📍 BUSINESS CARD WITH GPS AND ADDRESS")
    print("=" * 60)
    print(lang.t("create_gps_business_card"))
    print()

    combined_text, vcard_text = VCardGenerator.create_vcard(with_gps=True, with_address=True)

    print("\n🏷️  SELECT FRAME HEADER")
    print("-" * 40)
    print("1. Use ready option")
    print("2. Enter custom text")

    while True:
        choice = input(f"\n👉 {lang.t('choose')} (1-2): ").strip()
        if choice == "1":
            print("\n📋 READY OPTIONS:")
            print("1. VISIT CARD")
            print("2. BUSINESS CARD")
            print("3. CONTACT")
            print("4. LOCATION")
            print("5. FIND ME")

            while True:
                frame_choice = input(f"\n👉 {lang.t('choose')} (1-5): ").strip()
                if frame_choice == "1":
                    outline_type = "5"
                    frame_name = "VISIT CARD"
                    break
                elif frame_choice == "2":
                    outline_type = "6"
                    frame_name = "BUSINESS CARD"
                    break
                elif frame_choice == "3":
                    outline_type = "7"
                    frame_name = "CONTACT"
                    break
                elif frame_choice == "4":
                    outline_type = "8"
                    frame_name = "LOCATION"
                    custom_text = "LOCATION"
                    break
                elif frame_choice == "5":
                    outline_type = "8"
                    frame_name = "FIND ME"
                    custom_text = "FIND ME"
                    break
                else:
                    print(f"❌ {lang.t('error')}. {lang.t('try_again')}")
            break
        elif choice == "2":
            outline_type = "8"
            custom_text = get_custom_frame_text()
            frame_name = custom_text
            break
        else:
            print(f"❌ {lang.t('error')}. {lang.t('try_again')}")

    print(f"\n✅ {lang.t('header_selected')}: {frame_name}")

    print("\n🎨 SETTINGS FOR GPS BUSINESS CARD")
    print("-" * 40)
    print(lang.t("gps_card_settings"))
    print()

    qr_gen = QRGenerator()
    settings = {
        "shape": "2",
        "style": "1",
        "color_theme": qr_gen.COLOR_THEMES["11"],
        "outline_type": outline_type,
        "outline_color": "#006666",
        "outline_width": 10,
        "text_color": "#FFFFFF",
        "custom_text": custom_text if outline_type == "8" and 'custom_text' in locals() else "",
    }

    print("🎨 FRAME COLOR SETTINGS")
    print("-" * 40)
    print(f"{lang.t('current_color')}: Dark turquoise (#006666)")

    if lang.get_yes_no("change_frame_color"):
        settings["outline_color"] = get_outline_color(
            settings["color_theme"]["fg"],
            settings["color_theme"]["bg"],
            for_vcard=True,
            for_text_frame=True,
            with_gps=True
        )

        try:
            hex_color = settings["outline_color"].lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join(c * 2 for c in hex_color)
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            brightness = (r * 299 + g * 587 + b * 114) / 1000

            if brightness > 128:
                settings["text_color"] = "#000000"
            else:
                settings["text_color"] = "#FFFFFF"
        except:
            settings["text_color"] = "#FFFFFF"

    print("\n🎨 TEXT COLOR SETTINGS")
    print("-" * 40)
    print(f"{lang.t('current_text_color')}: {settings['text_color']}")

    if lang.get_yes_no("change_text_color"):
        settings["text_color"] = get_text_color_for_outline(settings["outline_color"])

    filename = get_output_filename("business_card_gps")

    print("\n" + "=" * 60)
    print("⚙️  CREATION PARAMETERS")
    print("=" * 60)
    print(f"🏷️  {lang.t('header')}: {frame_name}")
    print(f"🎨 {lang.t('frame_color')}: {settings['outline_color']}")
    print(f"✏️  {lang.t('text_color')}: {settings['text_color']}")
    print(f"📍 {lang.t('contains_gps_address')}")
    print(f"📏 {lang.t('thin_frame_close_text')}")
    print(f"💾 {lang.t('file')}: {filename}")

    if not lang.get_yes_no("proceed"):
        print("🚫 Operation cancelled")
        return False

    return create_qr_code(combined_text, settings, filename, is_vcard=True)


def main():
    """Main program function."""
    # Select language first
    lang.select_language()

    display_intro()

    while True:
        print("\n" + "=" * 60)
        print(lang.t("menu_title"))
        print("=" * 60)
        print(f"1. 🎨 {lang.t('menu_option1')}")
        print(f"2. ⚡ {lang.t('menu_option2')}")
        print(f"3. 📇 {lang.t('menu_option3')}")
        print(f"4. 📍 {lang.t('menu_option4')}")
        print(f"5. 💎 {lang.t('menu_option5')}")
        print(f"6. ℹ️  {lang.t('menu_option6')}")
        print(f"0. ❌ {lang.t('menu_option0')}")

        choice = input(f"\n👉 {lang.t('menu_prompt')}").strip()

        if choice == "0":
            print(f"\n👋 {lang.t('goodbye')}")
            break

        elif choice == "1":
            content_choice = get_content_choice()

            if content_choice == "0":
                continue

            elif content_choice == "1":
                text = get_text_input()
                settings = generate_custom_qr()
                filename = get_output_filename("qr_code")
                create_qr_code(text, settings, filename)

            elif content_choice == "2":
                combined_text, vcard_text = VCardGenerator.create_vcard()
                print(f"\n📱 {lang.t('creating_business_card_qr')}")

                print(f"\n🎨 {lang.t('customize_business_card_appearance')}:")
                settings = generate_custom_qr(for_vcard=True)

                print(f"\n📝 {lang.t('data_format')}:")
                print(f"✅ {lang.t('optimized_vcard_format')}")
                print(f"   • {lang.t('vcard_for_contacts')}")
                print(f"   • {lang.t('text_for_viewing')}")
                print(f"   • {lang.t('guaranteed_scanner_compatibility')}")

                filename = get_output_filename("vcard_qr")
                create_qr_code(combined_text, settings, filename, is_vcard=True)

            elif content_choice == "3":
                combined_text, vcard_text = VCardGenerator.create_vcard(with_gps=True, with_address=True)
                print(f"\n📱 {lang.t('creating_gps_business_card_qr')}")

                print(f"\n🎨 {lang.t('customize_gps_business_card_appearance')}:")
                settings = generate_custom_qr(for_vcard=True, with_gps=True)

                print(f"\n📝 {lang.t('data_format')}:")
                print(f"✅ {lang.t('optimized_vcard_format')}")
                print(f"   • {lang.t('vcard_for_contacts')}")
                print(f"   • {lang.t('text_for_viewing')}")
                print(f"   • {lang.t('includes_gps_address')}")
                print(f"   • {lang.t('guaranteed_scanner_compatibility')}")

                filename = get_output_filename("vcard_gps_qr")
                create_qr_code(combined_text, settings, filename, is_vcard=True)

            elif content_choice == "4":
                text = get_contact_text()
                settings = generate_custom_qr()
                filename = get_output_filename("contact_qr")
                create_qr_code(text, settings, filename)

        elif choice == "2":
            quick_generate()

        elif choice == "3":
            print("\n" + "=" * 60)
            print("🚀 QUICK BUSINESS CARD CREATION")
            print("=" * 60)
            print(lang.t("quick_business_card_steps"))
            print()

            combined_text, vcard_text = VCardGenerator.create_vcard()

            print(f"\n🎨 {lang.t('quick_design_for_business_card')}")
            print("-" * 40)
            print(lang.t("recommended_settings"))
            print()

            qr_gen = QRGenerator()
            settings = {
                "shape": "2",
                "style": "2",
                "color_theme": qr_gen.COLOR_THEMES["7"],
                "outline_type": "2",
                "outline_color": "#0D47A1",
                "outline_width": 10,
                "text_color": "#FFFFFF",
                "custom_text": "",
            }

            filename = get_output_filename("business_card")
            create_qr_code(combined_text, settings, filename, is_vcard=True)

        elif choice == "4":
            create_vcard_with_location()

        elif choice == "5":
            print("\n" + "=" * 60)
            print("💎 BUSINESS CARD WITH YOUR CUSTOM HEADER")
            print("=" * 60)
            print(lang.t("create_custom_header_business_card"))
            print()

            combined_text, vcard_text = VCardGenerator.create_vcard()

            print("\n🏷️  SELECT FRAME HEADER")
            print("-" * 40)
            print("1. Use ready option")
            print("2. Enter custom text")

            while True:
                frame_choice = input(f"\n👉 {lang.t('choose')} (1-2): ").strip()
                if frame_choice == "1":
                    print("\n📋 READY OPTIONS:")
                    print("1. VISIT CARD")
                    print("2. BUSINESS CARD")
                    print("3. CONTACT")

                    while True:
                        choice_num = input(f"\n👉 {lang.t('choose')} (1-3): ").strip()
                        if choice_num == "1":
                            outline_type = "5"
                            frame_name = "VISIT CARD"
                            break
                        elif choice_num == "2":
                            outline_type = "6"
                            frame_name = "BUSINESS CARD"
                            break
                        elif choice_num == "3":
                            outline_type = "7"
                            frame_name = "CONTACT"
                            break
                        else:
                            print(f"❌ {lang.t('error')}. {lang.t('try_again')}")
                    break
                elif frame_choice == "2":
                    outline_type = "8"
                    custom_text = get_custom_frame_text()
                    frame_name = custom_text
                    break
                else:
                    print(f"❌ {lang.t('error')}. {lang.t('try_again')}")

            print(f"\n🎨 {lang.t('settings_for_business_card')}")
            print("-" * 40)
            print(lang.t("optimal_settings"))
            print()

            qr_gen = QRGenerator()
            settings = {
                "shape": "2",
                "style": "1",
                "color_theme": qr_gen.COLOR_THEMES["7"],
                "outline_type": outline_type,
                "outline_color": "#0D47A1",
                "outline_width": 10,
                "text_color": "#FFFFFF",
                "custom_text": custom_text if outline_type == "8" else "",
            }

            filename = get_output_filename("business_card_custom_header")
            create_qr_code(combined_text, settings, filename, is_vcard=True)

        elif choice == "6":
            print("\n" + "=" * 60)
            print(lang.t("about_title"))
            print("=" * 60)
            print(f"\n{lang.t('version')}")
            print(f"\n✨ {lang.t('new_features')}")
            print(f"{lang.t('feature1')}")
            print(f"{lang.t('feature2')}")
            print(f"{lang.t('feature3')}")
            print(f"{lang.t('feature4')}")

            print(f"\n📍 {lang.t('gps_features')}")
            print(f"{lang.t('gps1')}")
            print(f"{lang.t('gps2')}")
            print(f"{lang.t('gps3')}")
            print(f"{lang.t('gps4')}")

            print(f"\n🏠 {lang.t('address_features')}")
            print(f"{lang.t('address1')}")
            print(f"{lang.t('address2')}")
            print(f"{lang.t('address3')}")

            print(f"\n🎨 {lang.t('design_features')}")
            print(f"{lang.t('design1')}")
            print(f"{lang.t('design2')}")
            print(f"{lang.t('design3')}")
            print(f"{lang.t('design4')}")

            print(f"\n📱 {lang.t('compatibility')}")
            print(f"{lang.t('comp1')}")
            print(f"{lang.t('comp2')}")
            print(f"{lang.t('comp3')}")
            print(f"{lang.t('comp4')}")

        else:
            print(f"❌ {lang.t('error')}. {lang.t('try_again')}")

        if choice in ["1", "2", "3", "4", "5", "6"]:
            if not lang.get_yes_no("return_to_menu"):
                print(f"\n👋 {lang.t('goodbye')}")
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n👋 {lang.t('user_interrupted')}")
    except Exception as e:
        print(f"\n❌ {lang.t('unexpected_error')}{e}")
        import traceback

        traceback.print_exc()
        print(lang.t("please_restart"))