# count_number_of_bees_on_the_image
# How to run:
docker build .
docker run --name bee -p 8080:8080 image_id -d
curl http://<DOCKER-IP>:8080/api/input?image_url=http://domain.com/image.jpeg
