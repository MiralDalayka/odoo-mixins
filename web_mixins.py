from odoo import models, fields, api

class Course(models.Model):
    _name = 'college.course'
    _description = 'Course'
    _inherit = ['website.published.mixin', 'website.seo.metadata', 'mail.thread']

    name = fields.Char(string='Course Name', required=True, tracking=True)
    description = fields.Text(string='Course Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    seats_available = fields.Integer(string='Seats Available', default=0)

    # Website publishing fields are automatically added by the mixins:
    # is_published, seo_title, seo_description, seo_keywords

    def publish_course(self):
        """Publish the course on the website"""
        self.ensure_one()
        self.toggle_publish()  # Switch the published state to visible
        self.message_post(
            body=f"Course <b>{self.name}</b> has been published on the website.",
            subject="Course Published",
            message_type='notification'
        )

    def unpublish_course(self):
        """Unpublish the course from the website"""
        self.ensure_one()
        self.toggle_publish()  # Switch the published state to invisible
        self.message_post(
            body=f"Course <b>{self.name}</b> has been unpublished from the website.",
            subject="Course Unpublished",
            message_type='notification'
        )

    def get_course_url(self):
        """Return the public website URL for the course"""
        self.ensure_one()
        return self.website_url()

    def set_seo_metadata(self, title=None, description=None, keywords=None):
        """Set SEO metadata for better search visibility"""
        self.ensure_one()
        if title:
            self.seo_title = title
        if description:
            self.seo_description = description
        if keywords:
            self.seo_keywords = keywords

    def fetch_seo_metadata(self):
        """Return SEO metadata for the course"""
        return self.get_seo_metadata()
