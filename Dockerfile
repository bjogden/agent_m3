# Use a lightweight Python image
FROM python:3.11-slim

# Install uv using the official installer copy method
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy configuration files first for efficient caching
COPY pyproject.toml .

# Install dependencies into a system/global context inside the container
RUN uv pip install --system -r pyproject.toml

# Copy the application source code
COPY src/ ./src/

# Run the agent script
CMD ["python", "src/agent.py"]