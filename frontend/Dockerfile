FROM node:20-alpine

WORKDIR /app

# Копирование package files
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование кода
COPY . .

# Сборка (для production)
# RUN npm run build

# Для development - запуск dev сервера
EXPOSE 5173

CMD ["npm", "run", "dev"]

