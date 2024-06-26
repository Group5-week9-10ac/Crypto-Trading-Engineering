# Use the official Node.js image as a base
FROM node:14

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your application code to the working directory
COPY . .

# Build your app
RUN npm run build

# Stage 2: Serve the React application with Nginx
FROM nginx:alpine

# Copy the build output from the previous stage to the NGINX html directory
COPY --from=0 /app/build /usr/share/nginx/html

# Expose port 80 to the Docker host
EXPOSE 80

# Start Nginx server to serve the React app
CMD ["nginx", "-g", "daemon off;"]
