FROM alpine:3.24
LABEL org.opencontainers.image.source=https://github.com/droans/ideabot
ENV LANG="C.UTF-8"
RUN --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk add --update-cache --virtual .build-deps \
        curl \
        git \
        nano \
        python3 \
        python3-dev \
        py3-pip && \
        rm -rf /usr/src/*

WORKDIR /app
RUN git clone https://github.com/droans/ideabot /app

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH"
RUN cd /app && uv venv && uv sync
CMD ["python", "/app/main.py"]
