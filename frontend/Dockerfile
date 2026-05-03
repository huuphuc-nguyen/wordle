# Stage 1: Build the Vite app
FROM node:24.9.0-alpine AS build

WORKDIR /react-app

RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN pnpm build

# Stage 2: Serve the built app
FROM node:24.9.0-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=build /react-app/dist /app

EXPOSE 3000

CMD ["serve", "-s", "-l", "3000", "/app"]
