FROM python:3.12-slim

# 安裝系統依賴
RUN apt-get update && apt-get install -y libgl1

# 建立虛擬環境
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 安裝 Python 套件
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 複製你的應用程式進去容器
COPY . .

# 運行應用程式
CMD ["python", "main.py"]
