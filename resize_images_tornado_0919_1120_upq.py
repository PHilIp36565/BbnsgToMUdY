# 代码生成时间: 2025-09-19 11:20:59
import os
import tornado.ioloop
import tornado.web
from PIL import Image
from tornado.options import define, options
import logging

# Define the options for the application
define('port', default=8888, help='Port to run the application on', type=int)

# Set up logging
logging.basicConfig(level=logging.INFO)

class ResizeImageHandler(tornado.web.RequestHandler):
    """
    Request handler that resizes an image.
    """
    def post(self):
        # Get the image path from the request body
        image_path = self.get_body_argument('image_path')
        target_width = self.get_body_argument('target_width', None)
        target_height = self.get_body_argument('target_height', None)

        # Check if the image path and target dimensions are provided
        if not image_path or not target_width or not target_height:
            self.write("Missing arguments")
            return

        try:
            # Open the image and resize it
            with Image.open(image_path) as img:
                img = img.resize((int(target_width), int(target_height)))
                # Save the resized image
                resized_image_path = os.path.splitext(image_path)[0] + "_resized" + os.path.splitext(image_path)[1]
                img.save(resized_image_path)
                self.write(f"Image resized successfully to {resized_image_path}")
        except Exception as e:
            self.write(f"Error resizing image: {str(e)}")

class Application(tornado.web.Application):
    """
    Creates the Tornado web application with the image resizing handler.
    """
    def __init__(self):
        handlers = [
            (r"/resize", ResizeImageHandler),
        ]
        super(Application, self).__init__(handlers)

if __name__ == "__main__":
    # Parse command line options
    tornado.options.parse_command_line()

    # Create the application and start the IOLoop
    app = Application()
    app.listen(options.port)
    logging.info(f"Server starting on port {options.port}")
    tornado.ioloop.IOLoop.current().start()
