from PIL import Image

img = Image.open("./maptemplate.png")

pixels = list(img.getdata())

gamemap = [pixels[i:i + img.width] for i in range(0, len(pixels), img.width)]

gamemap = [[1 if g == 255 else 0 for r, g, b, x in row] for row in gamemap]

for row in gamemap:
    print(*row)