# django_rest
Django REST API example implementation using Django REST Framework.

## How to get started

1. Create a ```.env``` file containing Postgres credentials. Here are the default values:

```
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

2. Build and run the container for the project. Make sure it is working properly.

```docker-compose up --build```

3. Close the container and do the migrations to the database.

```docker-compose run web python manage.py migrate```

4. Initialize the seed data.

```docker-compose run web python manage.py initdata```

5. Run the container. You may now use the API.

```docker-compose up```

## Using the API endpoints

### User Signup ```POST /auth/signup/```
```
curl -X POST http://localhost:8000/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "email": "email@email.com", "password": "password"}'
```

### User Login ```POST /auth/login/```
```
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "password"}'
```
This returns something like ```{"refresh": "REFRESH_TOKEN_HERE", "access": "ACCESS_TOKEN_HERE"}```. You may use the access token for endpoints requiring authentication.
The token lasts for 1 day. You can get a new access token through supplying the refresh token to ```/auth/login/refresh/```.

### Create Post ```POST /posts/```
```
curl -X POST http://localhost:8000/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN_HERE" \
  -d '{"title": "Post Title", "content": "Hello world!"}'
```

### Update Post ```PUT /posts/:id/```
```
curl -X PUT http://localhost:8000/posts/POST_ID_HERE/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN_HERE" \
  -d '{"title": "Updated Title", "content": "Updated content."}'  
```

### Delete Post ```DELETE /posts/:id/```
```
curl -L -X DELETE http://localhost:8000/posts/POST_ID_HERE/ \
  -H "Authorization: Bearer ACCESS_TOKEN_HERE"
```

### Retrieve User Posts ```GET /me/posts/```
```
curl -L -X GET http://localhost:8000/me/posts/ \
  -H "Authorization: Bearer ACCESS_TOKEN_HERE"
```

### Retrieve All Posts ```GET /posts/```
```
curl -L -X GET http://localhost:8000/posts/
```

### Retrieve Single Post ```GET /posts/:id/```
```
curl -L -X GET http://localhost:8000/posts/1/
```

### Create Comment ```POST /posts/:post_id/comments/```
```
curl -X POST http://localhost:8000/posts/POST_ID_HERE/comments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN_HERE" \
  -d '{"content": "This is a comment."}'  
```

### Delete Comment ```DELETE /posts/:post_id/comments/:id/```
```
curl -L -X DELETE http://localhost:8000/posts/POST_ID_HERE/comments/COMMENT_ID_HERE/ \
  -H "Authorization: Bearer ACCESS_TOKEN_HERE"
```

### Retrieve Post Comments ```GET /posts/:post_id/comments```
```
curl -X GET http://localhost:8000/posts/POST_ID_HERE/comments/
```
