FROM node:18-alpine

# Set working directory
WORKDIR /app

# Set production environment and API URL
ENV NODE_ENV=production
ENV CI=false
ENV REACT_APP_API_URL=https://backend-production-9ec1.up.railway.app/api/v1
ENV REACT_APP_ENVIRONMENT=production

# Copy package files
COPY package*.json ./

# Install dependencies (including dev deps needed for build)
RUN npm install && npm cache clean --force

# Copy source code
COPY . .

# Build the app for production
RUN npm run build

# Copy replace-env script
COPY replace-env.js ./

# Install serve to run the app
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Start the app with environment replacement
CMD ["sh", "-c", "node replace-env.js && serve -s build -l 3000"] 