from PIL import Image

# Open the PNG file
img = Image.open('config_python_icon_132473.png')
# Convert to RGBA if not already
if img.mode != 'RGBA':
    img = img.convert('RGBA')
# Save as ICO (multiple sizes for best compatibility)
sizes = [(256,256), (128,128), (64,64), (32,32), (16,16)]
img.save('icon.ico', format='ICO', sizes=sizes)
print('icon.ico created successfully.')
