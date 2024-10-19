from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, rand, floor
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, FloatType
import random
from datetime import datetime, timedelta

# Создаем объект SparkSession
spark = (SparkSession.builder
    .appName("InternetShopData")
    .getOrCreate())

# Список возможных товаров
products = ['Laptop', 'Smartphone', 'Headphones', 'Smartwatch', 'Tablet']

# Функция для генерации случайной даты за последний год
def generate_random_date():
    start_date = datetime.now() - timedelta(days=365)
    random_days = random.randint(0, 365)
    return start_date + timedelta(days=random_days)

# Генерируем данные
num_rows = 1000  # Минимальное количество строк, можно изменить

data = []
for _ in range(num_rows):
    order_date = generate_random_date()
    user_id = random.randint(1, 1000)  # Генерация случайного UserID
    product = random.choice(products)  # Случайный продукт из списка
    quantity = random.randint(1, 5)  # Случайное количество в пределах от 1 до 5
    price = round(random.uniform(10.0, 1000.0), 2)  # Случайная цена в пределах от 10 до 1000
    data.append((order_date, user_id, product, quantity, price))

# Создаем схему для DataFrame
schema = StructType([
    StructField("Date", DateType(), True),
    StructField("UserID", IntegerType(), True),
    StructField("Product", StringType(), True),
    StructField("Quantity", IntegerType(), True),
    StructField("Price", FloatType(), True)
])

# Создаем DataFrame
df = spark.createDataFrame(data, schema)

# Сохранить сгенерированный DataFrame в формате CSV для последующего анализа
df.write.csv("data.csv", header=True, mode="overwrite")

# Показываем содержимое DataFrame
df.show(10)

# Останавливаем SparkSession
spark.stop()