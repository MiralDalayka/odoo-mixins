from odoo import models, fields, api

class Course(models.Model):
    _name = 'college.course'
    _description = 'Course'
    _inherit = ['rating.mixin', 'mail.thread']  # Adds rating and chatter functionality

    name = fields.Char(string='Course Name', required=True, tracking=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    def submit_rating(self, student_id, rating_value, comment=None):
        """
        Submit a rating for this course by a student
        rating_value: integer (1 to 5)
        comment: optional text feedback
        """
        self.ensure_one()
        rating = self.env['rating.rating'].create({
            'res_model': self._name,
            'res_id': self.id,
            'rating': rating_value,
            'partner_id': student_id,
            'message': comment,
        })

        # Optional: Post a message in chatter
        msg = f"New rating submitted: {rating_value}/5"
        if comment:
            msg += f" with comment: {comment}"
        self.message_post(body=msg, subject="New Course Rating", message_type='notification')

        return rating

    def get_rating_summary(self):
        """
        Return a dictionary with rating stats:
        - Average rating
        - Count of ratings
        - Distribution of ratings
        """
        self.ensure_one()
        stats = self.rating_get_stats()
        return stats
