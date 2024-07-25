from PIL import Image
import cv2
import numpy as np

def sappu_method_extract_contours(input_image_path, output_image_path):
    image = cv2.imread(input_image_path)

    # Преобразуем изображение в градации серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применяем размытие для снижения шумов
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Используем метод Canny для нахождения краев
    edges = cv2.Canny(blurred_image, 50, 150)

    # Создаем финальное черно-белое изображение, где контуры - белые (1), фон - черный (0)
    contours_image = np.zeros_like(edges)
    contours_image[edges != 0] = 1

    # Сохраняем изображение
    cv2.imwrite(output_image_path, contours_image * 255)  # конвертируем 1 обратно в 255 для сохранения как изображение

def adaptive_filter_extract_contours(input_image_path, output_image_path):
    image = cv2.imread(input_image_path)

    # Преобразуем изображение в градации серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применяем адаптивное пороговое значение для выделения контуров
    thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Находим контуры
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Создаем финальное черно-белое изображение, где контуры - белые (255), фон - черный (0)
    contours_image = np.zeros_like(gray_image)
    cv2.drawContours(contours_image, contours, -1, (255), 1)  # рисуем контуры белым цветом

    # Сохраняем изображение
    cv2.imwrite(output_image_path, contours_image)

def merge_images(first_image_path, second_image_path, result_image_path):
    image1 = Image.open(first_image_path).convert('L')
    image2 = Image.open(second_image_path).convert('L')

    # Преобразуйте изображения в массивы numpy
    array1 = np.array(image1)
    array2 = np.array(image2)

    # Примените операцию ИЛИ к пикселям
    result_array = np.bitwise_or(array1, array2)

    # Преобразуйте результат обратно в изображение
    result_image = Image.fromarray(result_array)

    # Сохраните новое изображение
    result_image.save(result_image_path)
