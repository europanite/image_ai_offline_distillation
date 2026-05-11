FROM node:20-bookworm

WORKDIR /app

COPY app/package.json ./

RUN corepack enable \
    && corepack prepare yarn@1.22.22 --activate \
    && yarn install --ignore-engines --non-interactive --network-timeout 600000 \
    && test -x ./node_modules/.bin/expo \
    && ./node_modules/.bin/expo --version

COPY app ./

EXPOSE 8081

CMD ["./node_modules/.bin/expo", "start", "--web", "--host", "lan", "--port", "8081"]
