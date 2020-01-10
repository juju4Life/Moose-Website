import cloudinary
import cloudinary.api


cloudinary.config(
  cloud_name = "hbgpxhz8q",
  api_key = "591748276146296",
  api_secret = "pp1dmYHQxnQELvAP9OB-WashY3Y"
)


def get_image(card):
    image_path = card.set_name
    image_url = card.name.split(" ")
    image_url = "_".join(image_url).replace("'", "_")
    return cloudinary.CloudinaryImage("{}/{}".format(image_path, image_url) + ".png").image(alt="card image")