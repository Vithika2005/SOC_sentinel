# Use an official Redis image as the base image
FROM redis:latest

# Copy configuration files into the container
COPY redis.conf /usr/local/etc/redis/redis.conf

# Expose the default Redis port
EXPOSE 6379

# Command to run when starting the container
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
