# comfortable-qr-generator
### QR Code Generator with GPS and Address

![Full information](https://github.com/lambotik/comfortable-qr-generator/blob/main/idea/photo_2025-12-30_14-31-33.jpg)

![Example QR](https://github.com/lambotik/comfortable-qr-generator/blob/main/idea/example_qr.png)

A powerful program for creating stylish QR codes with support for electronic business cards (vCard), GPS coordinates, and addresses. Perfect for businesses, events, and personal use.
___
### 🚀 Features
Core Functions:

✅ Create QR codes for text, links, and contact information

✅ Generate electronic business cards in vCard format

✅ Add GPS coordinates to QR codes

✅ Include full addresses

✅ Automatic data formatting for QR scanners
___
### Design & Customization:
2 QR Code Shapes: rectangular, rounded corners

4 Module Styles: classic, circular, rounded, minimalistic

12 Color Themes: black & white, blue, green, red, purple, orange, vCard style, professional, premium gold, metallic gray, location, map

8 Frame Types: no frame, simple, double, thick, VISIT CARD, BUSINESS CARD, CONTACT, custom text
___
### Special Business Card Features:
Automatic business card detection by scanners

GPS coordinates open in mapping applications

Full compatibility with Android and iOS

Thin frames with text placed close to QR code
___
### 📦 Installation & Setup
Requirements:
Python 3.7 or higher

Required dependencies:

```
pip install qrcode[pil] pillow
```
Running the Program:
```
python qr_generator.py
```
___
### 🎯 How to Use
### 1. Program Launch
After launching, you'll see the main menu with 6 options:

```text
1. 🎨 Create QR code with customization
2. ⚡ Quick generation
3. 📇 Create basic business card (vCard)
4. 📍 Create business card with GPS and address
5. 💎 Business card with your custom header
6. ℹ️  About
0. ❌ Exit
```
___
### 2. Content Types
When choosing option 1, you get 4 content types:
```text
MAIN MENU
1. 📱 Create QR-code with settings
2. ⚡ Quick QR-code (link/text)
3. 👤 Contact (business card)
4. 📍 Contact with GPS
5. ℹ️  About
0. ❌ Exit
```
___
### 3. 🎨 COLOR SELECTION
```text
Choose color for Background:
----------------------------------------
1. Black #000000
2. White #FFFFFF
3. Red #FF0000
4. Green #00FF00
5. Blue #0000FF
6. Yellow #FFFF00
7. Orange #FFA500
8. Purple #800080
9. Turquoise #008080
10. Pink #FFC0CB
11. 🌈 Custom color (HEX)
0. ↩️  Back
```
___
### 4. Creating a GPS Business Card
To create a business card with GPS coordinates:

Select "📍 Create business card with GPS and address"

Fill in personal information:

* First and last name

* Phone and email

* Company and position (optional)

* Website (optional)

* Adding GPS Coordinates:


Format: latitude,longitude

Example: ```53.5045,27.5815```

Get coordinates from Google Maps or Yandex Maps

Program automatically validates coordinate correctness

Adding Address:

Example: 
```
Lenina St. 10, Minsk, Belarus, 220000
```
___
### 5. Design Customization

Step-by-step design customization:

* QR Code Shape - rectangle or rounded corners

* Module Style - 4 different module designs

* Color Theme - 12 ready-made color schemes

* Frame - 8 frame types with customization options
___
### 6. Saving Results

QR code saved in PNG format

Custom filename option

Program checks for existing files and offers overwrite

Option to open file immediately after creation
___
### 7. 🎨 Design Features
Recommendations for Business Cards:

* Shape: Rounded corners for modern look

* Style: Classic for maximum readability

* Color: vCard Style (blue) or Location (turquoise)

* Frame: Thin frame with text (VISIT CARD, BUSINESS CARD, CONTACT or custom)

### Recommendations for GPS Business Cards:

* "Location" Theme: turquoise tones for addresses

* "Map" Theme: terracotta tones for GPS markers

* Frame: Thin with closely positioned text
___
### 📱 Compatibility
### QR Code Scanners:

* 100% compatible with all popular QR scanners

* Automatic vCard format recognition

* Android and iOS prompt "Add Contact" when scanning

* GPS Coordinates: Open in Google Maps, Yandex Maps, and other applications

* Correct format for navigation systems

* Text representation for easy copying
___
### 💡 Usage Tips
For Best Readability:

* Print QR code at least 3×3 cm

* Use contrasting colors

* Choose classic module style for business cards
___
### For Business Cards:

* Minimum print size: 4×4 cm

* Light background recommended

* Test scanning before mass printing
___
### For GPS Business Cards:

* Verify coordinates are correct

* Test opening in mapping applications

* Add clear header ("FIND ME", "MY ADDRESS")
___
### 🔧 Technical Features
Data Format for Business Cards:
```
BEGIN:VCARD
VERSION:3.0
N:Lastname;Firstname;;;
FN:Firstname Lastname
TEL;TYPE=CELL,VOICE:+79991234567
EMAIL;TYPE=WORK,INTERNET:email@example.com
ORG:Company
TITLE:Position
GEO:53.904500,27.561500
ADR;TYPE=WORK,PREF:;;Lenina St. 10, Minsk, Belarus, 220000;;;;
REV:20241231T235959Z
END:VCARD
```
Error Correction:
For business cards: ERROR_CORRECT_H (high level)

For regular text: ERROR_CORRECT_Q (above average)
___
### 8. 🐛 Troubleshooting
If QR Code Doesn't Scan:

* Increase print size

* Use more contrasting colors

* Choose classic module style

* Ensure data isn't too long

If Business Card Doesn't Add to Contacts:

* Check phone format (+7xxxxxxxxxx)

* Ensure it starts with BEGIN:VCARD

* Try a different QR scanner

* Check QR code size (minimum 4×4 cm)
___
### 9. 📄 License
Program provided as is. Author is not responsible for any issues related to program usage.

### ✨ New Features in Version 9.0
* GPS coordinates added to business cards

* Full address inclusion

* 2 new color themes for locations

* Automatic coordinate formatting

* Improved scanner compatibility

* Note: The program automatically validates GPS coordinates and suggests optimal design settings based on the selected content type.
