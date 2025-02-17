import glob
import math
import cv2
import numpy as np
import scipy.spatial as spatial
import scipy.cluster as cluster
from collections import defaultdict
from statistics import mean
import os

# Ensure the raw_data directory exists
output_dir = './raw_data/'
os.makedirs(output_dir, exist_ok=True)

# Read image and do lite image processing


def read_img(file):
    img = cv2.imread(str(file), 1)

    W = 1000
    height, width, depth = img.shape
    imgScale = W / width
    newX, newY = img.shape[1] * imgScale, img.shape[0] * imgScale
    img = cv2.resize(img, (int(newX), int(newY)))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.blur(gray, (5, 5))
    return img, gray_blur

# Canny edge detection


def canny_edge(img, sigma=0.33):
    v = np.median(img)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(img, lower, upper)
    return edges

# Hough line detection


def hough_line(edges, min_line_length=100, max_line_gap=10):
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 125,
                           min_line_length, max_line_gap)
    if lines is None or len(lines) == 0:
        print("No lines detected.")
        return np.array([])  # Retorna uma matriz vazia para evitar erros
    lines = np.reshape(lines, (-1, 2))
    return lines


# Separate line into horizontal and vertical


def h_v_lines(lines):
    h_lines, v_lines = [], []
    for rho, theta in lines:
        if theta < np.pi / 4 or theta > np.pi - np.pi / 4:
            v_lines.append([rho, theta])
        else:
            h_lines.append([rho, theta])
    return h_lines, v_lines

# Find the intersections of the lines


def line_intersections(h_lines, v_lines):
    points = []
    for r_h, t_h in h_lines:
        for r_v, t_v in v_lines:
            a = np.array([[np.cos(t_h), np.sin(t_h)],
                         [np.cos(t_v), np.sin(t_v)]])
            b = np.array([r_h, r_v])
            inter_point = np.linalg.solve(a, b)
            points.append(inter_point)
    return np.array(points)

# Hierarchical cluster (by euclidean distance) intersection points


def cluster_points(points):
    dists = spatial.distance.pdist(points)
    single_linkage = cluster.hierarchy.single(dists)
    flat_clusters = cluster.hierarchy.fcluster(single_linkage, 15, 'distance')
    cluster_dict = defaultdict(list)
    for i in range(len(flat_clusters)):
        cluster_dict[flat_clusters[i]].append(points[i])
    cluster_values = cluster_dict.values()
    clusters = map(lambda arr: (np.mean(np.array(arr)[:, 0]), np.mean(
        np.array(arr)[:, 1])), cluster_values)
    return sorted(list(clusters), key=lambda k: [k[1], k[0]])

# Average the y value in each row and augment original point


def augment_points(points):
    points_shape = list(np.shape(points))
    augmented_points = []
    for row in range(int(points_shape[0] / 11)):
        start = row * 11
        end = (row * 11) + 10
        rw_points = points[start:end + 1]
        rw_y = []
        rw_x = []
        for point in rw_points:
            x, y = point
            rw_y.append(y)
            rw_x.append(x)
        y_mean = mean(rw_y)
        for i in range(len(rw_x)):
            point = (rw_x[i], y_mean)
            augmented_points.append(point)
    augmented_points = sorted(augmented_points, key=lambda k: [k[1], k[0]])
    return augmented_points

# Crop board into separate images


def write_crop_images(img, points, img_count, folder_path='./raw_data/'):
    num_list = []
    shape = list(np.shape(points))
    start_point = shape[0] - 14

    if int(shape[0] / 11) >= 8:
        range_num = 8
    else:
        range_num = int((shape[0] / 11) - 2)

    for row in range(range_num):
        start = start_point - (row * 11)
        end = (start_point - 8) - (row * 11)
        num_list.append(range(start, end, -1))

    for row in num_list:
        for s in row:
            base_len = math.dist(points[s], points[s + 1])
            bot_left, bot_right = points[s], points[s + 1]
            start_x, start_y = int(bot_left[0]), int(
                bot_left[1] - (base_len * 2))
            end_x, end_y = int(bot_right[0]), int(bot_right[1])

            # Ensure coordinates are within image bounds
            start_x = max(0, start_x)
            start_y = max(0, start_y)
            end_x = min(img.shape[1], end_x)
            end_y = min(img.shape[0], end_y)

            if start_x < end_x and start_y < end_y:
                cropped = img[start_y:end_y, start_x:end_x]
                img_count += 1
                cv2.imwrite(os.path.join(
                    folder_path, f'alpha_data_image{img_count}.jpeg'), cropped)
            else:
                print(f"Invalid crop: start_x={start_x}, end_x={
                      end_x}, start_y={start_y}, end_y={end_y}")

    return img_count


# Create a list of image file names
img_filename_list = []
folder_name = './test_data/*'
for path_name in glob.glob(folder_name):
    img_filename_list.append(path_name)

# Process images
img_count = 20000
print_number = 0
for file_name in img_filename_list:
    print(f"Processing: {file_name}")
    img, gray_blur = read_img(file_name)
    edges = canny_edge(gray_blur)
    lines = hough_line(edges)

    # Verifique se há linhas detectadas
    if lines.size == 0:
        print(f"No lines detected in {file_name}. Skipping.")
        continue

    h_lines, v_lines = h_v_lines(lines)

    # Verifique se há linhas horizontais e verticais suficientes
    if len(h_lines) < 11 or len(v_lines) < 11:
        print(f"Insufficient lines detected in {file_name}. Skipping.")
        continue

    intersection_points = line_intersections(h_lines, v_lines)
    points = cluster_points(intersection_points)
    points = augment_points(points)

    # Tente cortar as imagens e capture erros
    try:
        img_count = write_crop_images(img, points, img_count)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        continue

    print(f"Processed: {file_name}")


print("Total images processed:", print_number)
