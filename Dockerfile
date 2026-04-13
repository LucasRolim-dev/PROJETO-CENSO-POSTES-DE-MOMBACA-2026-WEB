FROM node:18-alpine

WORKDIR /app

ENV NODE_ENV=production

COPY package*.json ./
RUN npm install --omit=dev

COPY . .

# Segurança: roda como usuário não-root
USER node

EXPOSE 3000
CMD ["npm", "start"]