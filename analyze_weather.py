import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import hour, avg

# Khởi tạo SparkSession
spark = SparkSession.builder.appName("WeatherAnalysis").getOrCreate()

# Đọc dữ liệu từ CSV
df = spark.read.csv("weather_data.csv", header=True, inferSchema=True)

# Chuyển đổi cột timestamp thành giờ
df = df.withColumn("hour", hour(df.timestamp))

# Tính nhiệt độ trung bình theo giờ
result = df.groupBy("hour").agg(avg("temperature").alias("avg_temperature"))

# Hiển thị kết quả
result.show()

# Lưu kết quả với overwrite
result.write.mode("overwrite").csv("average_temperature_by_hour", header=True)

# Dừng SparkSession
spark.stop()