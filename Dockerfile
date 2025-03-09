FROM python:3.11

# Cài công cụ cần thiết và phụ thuộc cho psycopg2-binary
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget tar libpq-dev gcc python3-dev libc6-dev procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Tải và cài OpenJDK 22
RUN wget https://github.com/adoptium/temurin22-binaries/releases/download/jdk-22.0.1%2B8/OpenJDK22U-jre_x64_linux_hotspot_22.0.1_8.tar.gz -O /tmp/openjdk-22.tar.gz && \
    mkdir -p /usr/lib/jvm && \
    tar -xzf /tmp/openjdk-22.tar.gz -C /usr/lib/jvm && \
    mv /usr/lib/jvm/jdk-22* /usr/lib/jvm/java-22 && \
    rm /tmp/openjdk-22.tar.gz

# Thiết lập biến môi trường cho Java 22
ENV JAVA_HOME=/usr/lib/jvm/java-22
ENV PATH="$JAVA_HOME/bin:$PATH"

# Cập nhật pip và cài đặt PySpark cục bộ
RUN pip install --no-cache-dir pyspark==3.5.5

# Cài các phụ thuộc còn lại từ requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép file .jar và project
COPY postgresql-42.7.5.jar /usr/local/lib/
COPY . /app
WORKDIR /app

# Chạy script khi container khởi động
CMD ["python", "analyze_weather.py"]