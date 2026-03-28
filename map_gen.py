import cv2
import numpy as np
import yaml

#?--------------------------?#
name = "65_in_tv_map"

width = 1.44
height = 0.81

resolution = 0.01
origin = [0.0, 0.0, 0.0]
#?--------------------------?#


#!--------------------------------------------------------!#
data = {
    'image': f'{name}.pgm',   # string is fine here
    'mode': 'trinary',
    'resolution': resolution, # float, not {resolution}
    'origin': origin,         # list, not string
    'negate': 0,
    'occupied_thresh': 0.65,
    'free_thresh': 0.25
}

with open(f'./maps/{name}.yaml', 'w') as file:
    yaml.dump(data, file, default_flow_style=None)

px_w = int(width / resolution)
px_h = int(height / resolution)
img = np.zeros((px_h+2, px_w+2)).astype('uint8')

img[1:-1, 1:-1] = 255

print(np.shape(img))
print(img)

cv2.imwrite(f'./maps/{name}.pgm', img)
#!--------------------------------------------------------!#