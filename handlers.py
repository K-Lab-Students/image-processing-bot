import uuid
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from algorithms import sappu_method_extract_contours, adaptive_filter_extract_contours, merge_images
from PIL import Image
import io

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Отправь мне изображение (как фото или документ), и я обработаю его.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Отправь мне изображение (как фото или документ), и я обработаю его.')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive('user_photo.jpg')
    await ask_for_algorithm(update)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document = update.message.document
    if document.mime_type.startswith('image/'):
        file = await document.get_file()
        await file.download_to_drive('user_photo.jpg')
        await ask_for_algorithm(update)
    else:
        await update.message.reply_text('Пожалуйста, отправьте изображение.')

async def ask_for_algorithm(update: Update) -> None:
    keyboard = [
        # [
        #     InlineKeyboardButton("Алгоритм 1", callback_data='algorithm_1'),
        #     InlineKeyboardButton("Алгоритм 2", callback_data='algorithm_2'),
        # ],
        [
            InlineKeyboardButton("Контур Sappu", callback_data='sappu_method'),
        ],
        [
            InlineKeyboardButton("Контур Адаптивный", callback_data='adaptive_filter')
        ],
        [
            InlineKeyboardButton("Контур Комбинированный", callback_data='combined_method')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите алгоритм обработки:')
    await update.message.reply_text(
        '*Контур Sappu* - все контуры замкнуты, но есть потеря данных.\n*Контур Адаптивный* - есть разрывы контуров, но много деталей.\n*Контур Комбинированный* - одновременное применение обоих методов.',
        reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    choice = query.data

    input_image_path = 'user_photo.jpg'
    output_image_path = 'processed_image.jpg'

    if choice == 'algorithm_1':
        image = Image.open(input_image_path)
        processed_image = image.filter(ImageFilter.BLUR)
        processed_image.save(output_image_path)
    elif choice == 'algorithm_2':
        image = Image.open(input_image_path)
        processed_image = image.filter(ImageFilter.CONTOUR)
        processed_image.save(output_image_path)
    elif choice == 'sappu_method':
        # Применить метод Sappu
        sappu_method_extract_contours(input_image_path, output_image_path)
    elif choice == 'adaptive_filter':
        # Применить адаптивный фильтр
        adaptive_filter_extract_contours(input_image_path, output_image_path)
    elif choice == 'combined_method':
        # Применить комбинированный метод
        prefix = str(uuid.uuid4())
        sappu_temp_path = prefix + '_sappu_tmp.png'
        adaptive_temp_path = prefix + '_adaptive_tmp.png'
        sappu_method_extract_contours(input_image_path, sappu_temp_path)
        adaptive_filter_extract_contours(input_image_path, adaptive_temp_path)
        merge_images(sappu_temp_path, adaptive_temp_path, output_image_path)

    with open(output_image_path, 'rb') as file:
        await query.message.reply_document(document=file)