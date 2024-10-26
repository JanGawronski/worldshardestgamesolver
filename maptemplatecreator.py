from PIL import Image

dims = (16, 7)

img = Image.new('RGB', dims)
img.putdata([(256, 256, 256) for _ in range(dims[0]*dims[1])])
img.save("maptemplate.png")