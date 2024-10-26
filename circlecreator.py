from PIL import Image

dim = 20

upperBound = [((dim // 2) ** 2 - x**2)**.5 for x in range(dim // 2 + 1)]


plane = [[upperBound[abs(x - dim//2)] > abs(y - dim//2) for x in range(dim)] for y in range(dim)]



imgList = [(256, 256, 256) for _ in range(9* dim**2)]


for y in range(dim):
    for x in range(dim):
        if plane[y][x]:
            for gy in range(5 * dim // 7 + 1):
                for gx in range(5 * dim // 7 + 1):
                    imgList[(y - gy) * dim*3 + 6 * dim**2 + (x + 2 * dim - gx)] = (128, 128, 128)


for y in range(dim):
    for x in range(dim):
        if plane[y][x]:
            imgList[y * dim*3 + 6 * dim**2 + x + 2 * dim] = (0, 0, 0)


img = Image.new('RGB', (dim*3, dim*3))
img.putdata(imgList)
img.save("circle.png")