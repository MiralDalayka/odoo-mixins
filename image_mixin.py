from odoo import models, fields, api

class Course(models.Model):
    _name = 'college.course'
    _description = 'Course'
    _inherit = ['image.mixin', 'mail.thread']  # Adds image fields with automatic resizing + chatter

    name = fields.Char(string='Course Name', required=True, tracking=True)
    description = fields.Text(string='Course Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    # image.mixin automatically adds:
    # image_1920, image_1024, image_512, image_128
    # _compute_images() handles automatic resizing

    def upload_course_image(self, image_data):
        """
        Upload a new course image (binary) and automatically generate resized versions
        image_data: base64-encoded image
        """
        self.ensure_one()
        self.image_1920 = image_data  # Main high-resolution image
        # Smaller images are auto-generated via _compute_images
        self._compute_images()

        # Optional: Notify in chatter
        self.message_post( body=f"Course <b>{self.name}</b> image has been updated.", subject="Course Image Updated", message_type='notification')

    def get_course_thumbnail(self, size='128'):
        """
        Retrieve resized image based on size
        size options: '128', '512', '1024', '1920'
        """
        self.ensure_one()
        if size == '128':
            return self.image_128
        elif size == '512':
            return self.image_512
        elif size == '1024':
            return self.image_1024
        else:
            return self.image_1920
