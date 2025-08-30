FROM node:lts-bookworm-slim as builder

# Copy the application code to the container
COPY . /app

# Create app directory
WORKDIR /app

RUN npm install

# Build the Vite application for production
RUN npm run build

# Use Nginx to serve the static build files
FROM nginx:stable-alpine3.21-perl
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]