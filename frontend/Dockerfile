# Production image for the React frontend: build the static bundle with
# Vite, then serve it with nginx. Multi-stage so the final image doesn't
# carry node_modules or the Vite toolchain - just static files.
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

# Baked in at build time since Vite inlines VITE_* vars into the static
# bundle - there's no server to read env vars from at runtime for a
# static SPA. Pass this at `docker build --build-arg` time to point the
# built frontend at your deployed backend URL.
ARG VITE_API_BASE_URL=http://localhost:8000/api/v1
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
