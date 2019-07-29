# How to run:
docker build . <br/>
docker run --name bee -p 8080:8080 image_id -d <br/>
curl http://<DOCKER-IP>:8080/api/input?image_url=http://domain.com/image.jpeg
