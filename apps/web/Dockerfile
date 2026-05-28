FROM node:20-alpine

WORKDIR /app

# Copy entire monorepo
COPY . .

# Install pnpm globally
RUN npm install -g pnpm

# Install all monorepo dependencies
RUN pnpm install --frozen-lockfile

# Change to web app directory
WORKDIR /app/apps/web

# Build the Next.js app for production
RUN pnpm build

# Expose port 3000
EXPOSE 3000

# Start the Next.js production server
CMD ["pnpm", "start"]
