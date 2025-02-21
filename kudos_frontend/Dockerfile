# Use official Node.js image as base
FROM node:18

# Set working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first (leverage Docker caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire React project into the container
COPY . .

# Expose port 3000 for the React app
EXPOSE 3000

# Start React app in development mode
CMD ["npm", "start"]
