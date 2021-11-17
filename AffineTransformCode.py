import random
from PIL import Image, ImageOps
import os


def affine_distortions(img):
    width, height = img.size

    #Sheer Horizontal
    if random.uniform(0, 1) > 0.5:
        rho_x = random.uniform(-0.3, 0.3)
        # rho_x = math.radians(rho_x)
        img = ImageOps.invert(img.convert('RGB'))
        img = img.transform(img.size, Image.AFFINE, (1, rho_x, 0, 0, 1, 0))
        img = ImageOps.invert(img.convert('RGB'))

    #Sheer Vertical
    if random.uniform(0, 1) > 0.5:
        rho_y = random.uniform(-0.3, 0.3)
        # rho_y - math.radians(rho_y)
        img = ImageOps.invert(img.convert('RGB'))
        img = img.transform(img.size, Image.AFFINE, (1, 0, 0, rho_y, 1, 0))
        img = ImageOps.invert(img.convert('RGB'))

    #Scale X
    if random.uniform(0, 1) > 0.5:
        s_x = random.uniform(0.8, 1.2)
    else:
        s_x = 1

    #Scale Y
    if random.uniform(0, 1) > 0.5:
        s_y = random.uniform(0.8, 1.2)
    else:
        s_y = 1
    # img = img.resize((round(s_x * img.size[0]), round(s_y * img.size[1])), Image.ANTIALIAS)
    img = ImageOps.invert(img.convert('RGB'))
    img = img.resize((round(s_x * img.size[0]), round(s_y * img.size[1])))
    img = ImageOps.invert(img.convert('RGB'))

    #Rotate Image
    if random.uniform(0, 1) > 0.5:
        theta = random.uniform(-10.0, 10.0)
        img = img.rotate(theta, expand=1, fillcolor=(255, 255, 255))

    #Translate X
    if random.uniform(0, 1) > 0.5:
        t_x = random.uniform(-2, 2)
        img = ImageOps.invert(img.convert('RGB'))
        img = img.transform(img.size, Image.AFFINE, (1, 0, t_x, 0, 1, 0))
        img = ImageOps.invert(img.convert('RGB'))

    #Translate Y
    if random.uniform(0, 1) > 0.5:
        t_y = random.uniform(-2, 2)
        img = ImageOps.invert(img.convert('RGB'))
        img = img.transform(img.size, Image.AFFINE, (1, 0, 0, 0, 1, t_y))
        img = ImageOps.invert(img.convert('RGB'))

    #Crop to final size
    img = ImageOps.invert(img.convert('RGB'))
    img = img.crop((0, 0, width, height))
    img = ImageOps.invert(img.convert('RGB'))

    return img


def generate_distortions(imagesLoc, saveLoc, k=3):
    foldersOfInterest = ['images_background', 'images_background_small1', 'images_evaluation']
    for i in range(0, len(foldersOfInterest)):
        tmp = imagesLoc + '/' + foldersOfInterest[i]

        for root, _, files in os.walk(tmp):
            if 'character' in root:
                saveDir = saveLoc + '/' + root.split('/')[-1]
                if not os.path.isdir(saveDir):
                    os.makedirs(saveDir)

                for f in files:
                    omniFilePath = root + '/' + f
                    originalImg = Image.open(omniFilePath)
                    fname, fend = f.split('.')
                    for j in range(0, k):
                        distortedImgLoc = saveDir + '/' + fname + '_' + str(j) + '.' + fend
                        distortedImg = affine_distortions(originalImg)
                        distortedImg.save(distortedImgLoc)

    print("Operation Complete.")
    return 1


if __name__ == '__main__':
    set_k = 2
    transformationSaveLocation = './affineTransform'
    omniLoc = './omniglot/python'
    generate_distortions(omniLoc, transformationSaveLocation, set_k)
