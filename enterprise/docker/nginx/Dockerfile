# Use an official Nginx image as the base image
FROM nginx:latest

# Copy custom configuration files into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 for HTTP traffic
EXPOSE 80

# Command to run when starting the container
CMD ["nginx", "-g", "daemon off;"]
