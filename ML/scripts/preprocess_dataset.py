"""
Compress the images in the original dataset from (1024 x 1024) to (256 x 256)
"""

import os
import numpy as np
from PIL import Image
import json

from cv2 import fillPoly, imwrite
from shapely import wkt
from shapely.geometry import mapping, Polygon
from skimage.io import imread
from tqdm import tqdm

IMAGES_BASE_PATH = '/content/train1/images/'
LABELS_BASE_PATH = '/content/train1/labels/'

image_names = os.listdir(IMAGES_BASE_PATH)
label_names = os.listdir(LABELS_BASE_PATH)
print(len(image_names))
print(len(label_names))

label_to_id = {
    'no-damage': 1,
    'minor-damage': 2,
    'major-damage': 3,
    'destroyed': 4,
    'un-classified': 5
}

def read_json(path):
  with open(path) as f:
    j = json.load(f)
  return j

def get_dimensions(image_path):
  img = imread(image_path)
  img = np.array(img)
  w, h, c = img.shape
  return (w, h, c)

def get_feature_info(feature):
  props = {}

  for feat in feature['features']['xy']:
    feat_shape = wkt.loads(feat['wkt'])

    coords = list(mapping(feat_shape)['coordinates'][0])

    if 'subtype' in feat['properties']:
      damage_class = feat['properties']['subtype']
    else:
      damage_class = 'no-damage'

    encoded_damage_class = label_to_id[damage_class]

    props[feat['properties']['uid']] = (np.array(coords, np.int32), encoded_damage_class)

  return props

def mask_polygons_together_with_border(size, polys, border, mode='damage'):
  mask_img = np.zeros(size, np.uint8)

  for uid, tup in polys.items():
    poly, damage_class_num = tup
    if mode == 'segmentation' and damage_class_num > 1:
      damage_class_num = 1

    polygon = Polygon(poly)

    (poly_center_x, poly_center_y) = polygon.centroid.coords[0]
    polygon_points = polygon.exterior.coords

    shrunk_polygon = []
    for (x, y) in polygon_points:
      if x < poly_center_x:
        x += border
      elif x > poly_center_x:
        x -= border

      if y < poly_center_y:
        y += border
      elif y > poly_center_y:
        y -= border

      shrunk_polygon.append([x, y])

    ns_poly = np.array(shrunk_polygon, np.int32)

    fillPoly(mask_img, [ns_poly], (damage_class_num, damage_class_num, damage_class_num))

  mask_img = mask_img[:, :, 0].squeeze()
  print(f'shape of final mask_img: {mask_img.shape}')
  return mask_img

border_width = 2
MASKS_BASE_PATH = '/data/train/masks'

for label_path in tqdm(label_names):
  title_id = label_path[:-5]
  label_path = f'{LABELS_BASE_PATH}{label_path}'
  image_path = f'{IMAGES_BASE_PATH}{title_id}.png'
  target_path_damage = f'{MASKS_BASE_PATH}{title_id}.png'
  target_path_seg = f'{MASKS_BASE_PATH}house_seg_{title_id}.png'

  label_json = read_json(label_path)

  title_size = get_dimensions(image_path)

  polys = get_feature_info(label_json)

  mask_img_damage = mask_polygons_together_with_border(title_size, polys, border_width, mode='damage')

  imwrite(target_path_damage, mask_img_damage)

  mask_img_segmentation = mask_polygons_together_with_border(title_size, polys, border_width, mode='segmentation')

  imwrite(target_path_seg, mask_img_segmentation)


TARGET_SHAPE_IMAGE = [256, 256, 3]
TARGET_SHAPE_MASK = [256, 256, 1]

i_h, i_w, i_c = TARGET_SHAPE_IMAGE
m_h, m_w, m_c = TARGET_SHAPE_MASK

MASKS_BASE_PATH = '/data/train1/masks'

IMAGES_TARGET_PATH = '/data/train/images/'
MASKS_TARGET_PATH = '/data/train/masks/'

for filename in image_names:
  print(filename)
  img = Image.open(f'{IMAGES_BASE_PATH}{filename}')
  img = img.resize((i_h, i_w))
  img = np.array(img)
  img = np.reshape(img, (i_h, i_w, i_c))
  img = Image.fromarray(img)
  img.save(f'{IMAGES_TARGET_PATH}{filename}')

  mask1 = Image.open(f'{MASKS_BASE_PATH}{filename}')
  mask1 = mask1.resize((m_h, m_w))
  mask1 = np.array(mask1)
  # mask1 = np.reshape(mask1, (m_h, m_w, m_c))
  mask1 = Image.fromarray(mask1)
  mask1.save(f'{MASKS_TARGET_PATH}{filename}')

  mask2 = Image.open(f'{MASKS_BASE_PATH}house_seg_{filename[:-4]}.png')
  mask2 = mask2.resize((m_h, m_w))
  mask2 = np.array(mask2)
  # mask2 = np.reshape(mask2, (m_h, m_w, m_c))
  mask2 = Image.fromarray(mask2)
  mask2.save(f'{MASKS_TARGET_PATH}house_seg_{filename[:-4]}.png')
