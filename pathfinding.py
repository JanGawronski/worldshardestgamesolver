from PIL import Image
from queue import Queue
from time import time


def BFS(G, start, end):
    T = len(G)
    Y = len(G[0])
    X = len(G[0][0])

    visited = [[[False for _ in range(X)] for _ in range(Y)] for _ in range(T)]
    distance = [[[float("inf") for _ in range(X)] for _ in range(Y)] for _ in range(T)]
    parent = [[[None for _ in range(X)] for _ in range(Y)] for _ in range(T)]

    Q = Queue()

    distance[start[0]][start[1]][start[2]] = 0
    visited[start[0]][start[1]][start[2]] = True

    Q.put((start[0], start[1], start[2]))

    endTime = 0

    while not Q.empty():
        t, y, x = Q.get()

        if y == end[0] and x == end[1]:
            endTime = t
            break

        if not visited[(t + 1) % T][y][x] and G[(t + 1) % T][y][x]:
            visited[(t + 1) % T][y][x] = True
            distance[(t + 1) % T][y][x] = distance[t][y][x] + 1
            parent[(t + 1) % T][y][x] = (t, y, x)
            Q.put(((t + 1) % T, y, x))

        if x + 1 < X and not visited[(t + 1) % T][y][x + 1] and G[(t + 1) % T][y][x + 1]:
            visited[(t + 1) % T][y][x + 1] = True
            distance[(t + 1) % T][y][x + 1] = distance[t][y][x] + 1
            parent[(t + 1) % T][y][x + 1] = (t, y, x)
            Q.put(((t + 1) % T, y, x + 1))

        if x - 1 >= 0 and not visited[(t + 1) % T][y][x - 1] and G[(t + 1) % T][y][x - 1]:
            visited[(t + 1) % T][y][x - 1] = True
            distance[(t + 1) % T][y][x - 1] = distance[t][y][x] + 1
            parent[(t + 1) % T][y][x - 1] = (t, y, x)
            Q.put(((t + 1) % T, y, x - 1))

        if y + 1 < Y and not visited[(t + 1) % T][y + 1][x] and G[(t + 1) % T][y + 1][x]:
            visited[(t + 1) % T][y + 1][x] = True
            distance[(t + 1) % T][y + 1][x] = distance[t][y][x] + 1
            parent[(t + 1) % T][y + 1][x] = (t, y, x)
            Q.put(((t + 1) % T, y + 1, x))

        if y - 1 >= 0 and not visited[(t + 1) % T][y - 1][x] and G[(t + 1) % T][y - 1][x]:
            visited[(t + 1) % T][y - 1][x] = True
            distance[(t + 1) % T][y - 1][x] = distance[t][y][x] + 1
            parent[(t + 1) % T][y - 1][x] = (t, y, x)
            Q.put(((t + 1) % T, y - 1, x))


    v = (endTime, end[0], end[1])
    path = [v]
    while parent[v[0]][v[1]][v[2]] != start:
        v = parent[v[0]][v[1]][v[2]]
        path.append(v)
    path.reverse()

    return path, distance[endTime][end[0]][end[1]]

def prepareAnimation(pixelmap, path, T, level, circle, cubeDim, circleDim, multiplier):
    Y = len(pixelmap) * 10 * multiplier
    X = len(pixelmap[0]) * 10 * multiplier

    colormap = [[[pixelmap[y//(10 * multiplier)][x//(10 * multiplier)] for x in range(X)] for y in range(Y)] for _ in range(len(path))]


    obstaclePaths = []
    with open(f"./maptemplates/{level}.txt") as file:
        obstaclePaths = eval(file.read())[2]

    for obstacle in obstaclePaths:
        for t in range(len(path)):
            for y in range(circleDim):
                for x in range(circleDim):
                    if circle[y][x] and 0 <= y + obstacle[t % T][0] - 1 < Y and 0 <= x + obstacle[t % T][1] - 1 < X:
                        colormap[t][y + obstacle[t % T][0] - 1][x + obstacle[t % T][1] - 1] = (0, 0, 255, 255)

    counter = 0
    darkEdge = cubeDim // 8 + 1
    for t, y, x in path:
        for cy in range(cubeDim):
            for cx in range(cubeDim):
                if cy < darkEdge or cx < darkEdge or cy > cubeDim - darkEdge - 1 or cx > cubeDim - darkEdge - 1:
                    colormap[counter][y + cy][x + cx] = (126, 0, 0, 255)
                else:
                    colormap[counter][y + cy][x + cx] = (255, 0, 0, 255)
        counter += 1


    img = [Image.new('RGB', (X, Y)) for _ in range(len(path))]
    for t in range(len(path)):
        imgList = []
        for y in range(Y):
            for x in range(X):
                imgList.append(colormap[t][y][x])
        img[t].putdata(imgList)
    
    img[0].save(f'./mapanimations/{level}-{multiplier}.gif', save_all=True, append_images=img[1:], optimize=False, duration=40, loop=0)

def prepareDebugAnimation(path, level, multiplier, G):
    T = len(G)
    Y = len(G[0])
    X = len(G[0][0])

    colormap = [[[(255, 255, 255, 255) if G[t % T][y][x] else (0, 0, 0, 0) for x in range(X)] for y in range(Y)] for t in range(len(path))]


    counter = 0
    for t, y, x in path:
        colormap[counter][y][x] = (255, 0, 0, 255)
        counter += 1

    img = [Image.new('RGB', (X, Y)) for _ in range(len(path))]
    for t in range(len(path)):
        imgList = []
        for y in range(Y):
            for x in range(X):
                imgList.append(colormap[t][y][x])
        img[t].putdata(imgList)
    
    img[0].save(f'./debug/{level}-{multiplier}.gif', save_all=True, append_images=img[1:], optimize=False, duration=40, loop=0)

def calculateCircleCollision(multiplier, cubeDim):
    upperBound = [(((5 * multiplier)//2) ** 2 - x**2)**.5 for x in range(((5 * multiplier)//2) + 1)]

    circle = [[upperBound[abs(x - (5 * multiplier) // 2)] > abs(y - (5 * multiplier) // 2) for x in range(5 * multiplier)] for y in range(5 * multiplier)]

    collisionArray = [[True for _ in range(5 * multiplier + cubeDim)] for _ in range(5 * multiplier + cubeDim)]

    for y in range(5 * multiplier):
        for x in range(5 * multiplier):
            if circle[y][x]:
                for gy in range(cubeDim):
                    for gx in range(cubeDim):
                        collisionArray[y + gy][x + gx] = False
    
    return upperBound, circle, collisionArray

def prepareGraph(level, multiplier, cubeDim, T):
    img = Image.open(f"./maptemplates/{level}.png")

    X, Y = img.width * 10 * multiplier, img.height * 10 * multiplier

    pixels = list(img.getdata())

    pixelmap = [pixels[i:i + img.width] for i in range(0, len(pixels), img.width)]

    boolmap = [[not (r == 170 and g == 165 and b == 255) for r, g, b, x in row] for row in pixelmap]

    G = [[[boolmap[y//(10 * multiplier)][x//(10 * multiplier)] if y + cubeDim - 1 < Y and x + cubeDim - 1 < X and boolmap[(y + cubeDim - 1)//(10 * multiplier)][(x + cubeDim - 1)//(10 * multiplier)] and boolmap[(y + cubeDim - 1)//(10 * multiplier)][x//(10 * multiplier)] and boolmap[y//(10 * multiplier)][(x + cubeDim - 1)//(10 * multiplier)] else False for x in range(X)] for y in range(Y)] for _ in range(T)]

    return G, pixelmap, boolmap


def applyObstaclePaths(G, collisionArray, multiplier, cubeDim, circleDim, level):
    T = len(G)
    Y = len(G[0])
    X = len(G[0][0])
    with open(f"./maptemplates/{level}.txt") as file:
        obstaclePaths = eval(file.read())[2]

    for obstacle in obstaclePaths:
        for t in range(T):
            for y in range(-cubeDim, circleDim):
                for x in range(-cubeDim, circleDim):
                    if 0 <= y + obstacle[t][0] < Y and 0 <= x + obstacle[t][1] < X:
                        G[t][y + obstacle[t][0]][x + obstacle[t][1]] &= collisionArray[y + cubeDim][x + cubeDim]


def createMapPicture(G, multiplier):
    Y = len(G[0])
    X = len(G[0][0])
    img = Image.new('RGB', (X, Y))
    imgList = []
    for indey in range(Y):
        for index in range(X):
            if indey == 5 * multiplier and index == 140 * multiplier or indey == 35 * multiplier and index == 15 * multiplier:
                imgList.append((256, 0, 0))
            else:
                imgList.append((256, 256, 256) if G[0][indey][index] else (0, 0, 0))
    img.putdata(imgList)
    img.save("map.png")


def main():
    level = 6
    multiplier = 2
    cubeDim = 7 * multiplier
    circleDim = 5 * multiplier
    timestart = time()
    with open(f"./maptemplates/{level}.txt") as file:
        data = eval(file.read())
    
    T = data[0] * multiplier

    G, pixelmap, boolmap = prepareGraph(level, multiplier, cubeDim, T)

    upperBound, circle, collisionArray = calculateCircleCollision(multiplier, cubeDim)

    applyObstaclePaths(G, collisionArray, multiplier, cubeDim, circleDim, level)
    path = [(0, int(data[1][0][0] * multiplier), int(data[1][0][1] * multiplier))]
    for y, x in data[1][1:]:
        try:
            newPath, distance = BFS(G, path[-1], (int(y * multiplier), int(x * multiplier)))
        except:
            print("Couldn't find path")
            exit()
        path.extend(newPath)
        t = distance % T

    prepareAnimation(pixelmap, path, T, level, circle, cubeDim, circleDim, multiplier)
    #prepareDebugAnimation(path, level, multiplier, G)

    print(f"Calculation with multplier {multiplier} took {time() - timestart}")


if __name__ == "__main__":
    main()