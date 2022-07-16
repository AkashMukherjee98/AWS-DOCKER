FROM node:18-alpine3.15
WORKDIR /core
COPY . .
RUN npm run build
CMD ["npm", "start"]