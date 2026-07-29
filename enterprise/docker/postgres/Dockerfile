# Use an official PostgreSQL image as the base image
FROM postgres:latest

# Copy configuration files into the container
COPY postgres.conf /etc/postgresql/13/main/postgresql.conf

# Expose port 5432 for PostgreSQL traffic
EXPOSE 5432

# Command to run when starting the container
CMD ["postgres"]
