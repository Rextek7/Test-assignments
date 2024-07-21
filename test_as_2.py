from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Создаем SparkSession
spark = SparkSession.builder.appName("ProductsCategories").getOrCreate()

# Примерные данные
products_data = [(1, "Product A"), (2, "Product B"), (3, "Product C"), (4, "Product D")]
categories_data = [(1, "Category X"), (2, "Category Y"), (3, "Category Z")]
product_categories_data = [(1, 1), (1, 2), (2, 2), (3, 3)]

# Создаем DataFrame
products = spark.createDataFrame(products_data, ["product_id", "product_name"])
categories = spark.createDataFrame(categories_data, ["category_id", "category_name"])
product_categories = spark.createDataFrame(product_categories_data, ["product_id", "category_id"])

# Все пары «Имя продукта – Имя категории»
product_category_pairs = product_categories \
    .join(products, "product_id") \
    .join(categories, "category_id") \
    .select("product_name", "category_name")

# Имена всех продуктов, у которых нет категорий
products_without_categories = products \
    .join(product_categories, "product_id", "left_anti") \
    .select("product_name")

# Вывод результатов
product_category_pairs.show(truncate=False)
products_without_categories.show(truncate=False)

