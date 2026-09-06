# ==========================================
# Multi-stage Dockerfile for NestJS Production
# ==========================================

# --- Stage 1: Build & Dependencies ---
FROM node:18-alpine AS builder

WORKDIR /usr/src/app

# Install build tools if needed
RUN apk add --no-cache python3 make g++

# Copy package descriptors
COPY package*.json ./

# Install all dependencies (including devDependencies needed for build)
RUN npm install

# Copy source code and config
COPY tsconfig*.json nest-cli.json ./
COPY src/ ./src/

# Compile TypeScript to production JavaScript (output to dist/)
RUN npm run build

# --- Stage 2: Production Runtime ---
FROM node:18-alpine AS runner

WORKDIR /usr/src/app

ENV NODE_ENV=production
ENV PORT=3000

# Copy package descriptors for production install
COPY package*.json ./

# Install ONLY production dependencies to keep image small & secure
RUN npm install --only=production && npm cache clean --force

# Copy compiled JavaScript from builder stage
COPY --from=builder /usr/src/app/dist ./dist

# Security: run application as non-privileged 'node' user
USER node

# Expose NestJS application port
EXPOSE 3000

# Container healthcheck (checks Swagger / API health)
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/v1 || exit 1

# Start the production application
CMD ["node", "dist/main.js"]
