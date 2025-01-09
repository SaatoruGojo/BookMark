# Social Image Sharing Application

This project is a **social application** built with Django and JavaScript that allows users to share and interact with images they find on the internet. The project focuses on implementing advanced functionalities such as social authentication, user activity streams, and infinite scrolling, providing a platform for users to connect and share content seamlessly.

![Screenshot Description](https://i.imgur.com/82g38v4.png)



## Features

### Authentication
- User registration, login, and profile management.
- Password reset functionality.
- Social authentication via Google using OAuth 2.0.

### Image Sharing
- Bookmarklet to share images from any website.
- Asynchronous image bookmarking and liking using JavaScript and Django.
- Automatic generation of image thumbnails using the `easy-thumbnails` package.
- Infinite scroll pagination for seamless browsing.

### Social Features
- Follow/unfollow functionality to connect with other users.
- Activity stream showing actions (e.g., uploading images, following users).
- User profiles with details and images.

### Performance and Optimization
- Image view tracking and ranking using Redis for fast I/O storage.
- Optimized database queries with Django Debug Toolbar.
- Signals to denormalize counts and improve performance.

## Technologies Used

- **Backend**: Django, Django REST Framework, Python Social Auth
- **Frontend**: JavaScript, HTML, CSS
- **Database**: SQLite (Development), Redis (for analytics and caching)
- **Others**: Django Debug Toolbar, easy-thumbnails

## Installation

 Create a `.env` file for environment variables and add your Google OAuth credentials:
   ```
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ALLOWED_HOSTS=*
   
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   ```
### **Set Up Redis**
To run the project, you need a Redis server. Use Docker to set it up:

#### **Pull the Redis Docker Image**
Execute the following command to pull the Redis Docker image:
```bash
docker pull redis:7.2.4
```

#### **Start the Redis Container**
Run the following command to start the Redis server:
```bash
docker run -it --rm --name redis -p 6379:6379 redis:7.2.4
```

> **Note:** The Redis server must be running for the project to work. Without it, the website will show a "machine refused to connect" error.
## Usage

1. Register or log in using your email or Google account.
2. Edit your profile to add details about yourself.
3. Use the **Bookmark it** button to share images from any website.
4. Browse images, like/unlike them, and follow other users.
5. View your personalized activity stream on the dashboard.

## Deployment

This project can be deployed on platforms like Heroku, AWS, or any cloud provider supporting Django. Ensure to set up Redis and configure environment variables for production.

## Contribution

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes.

