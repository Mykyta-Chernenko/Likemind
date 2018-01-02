# cookiecutter-drf-react

This is my favorite Web project tech stack and folder hierarchy.


[cookiecutter](https://github.com/audreyr/cookiecutter) template for
 - backend
   - django
   - django-rest-framework
 - frontend
   - reactjs
   - create-react-app

backend and frontend run on docker and are completely decoupled.
The backend has no knowledge of frontend. The frontend is static but can call the backend REST Apis.
