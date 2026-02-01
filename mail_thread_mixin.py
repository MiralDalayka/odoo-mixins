from odoo import models, fields, api

class EnrollmentRequest(models.Model):
    _name = 'college.enrollment.request'
    _description = 'Enrollment Request'
    _inherit = ['mail.thread']  # <-- Adds chatter functionality

    student_id = fields.Many2one('res.partner', string='Student', required=True, tracking=True)
    course_id = fields.Many2one('college.course', string='Course', required=True, tracking=True)
    state = fields.Selection([('draft', 'Draft'),('submitted', 'Submitted'),('approved', 'Approved'),('rejected', 'Rejected')], default='draft', tracking=True)

    request_date = fields.Date(string='Request Date', default=fields.Date.today())

    # Optional: Track specific field changes for notifications
    _track = {
        'state': {
            'college_enrollment_request.mt_request_submitted': lambda self, cr, uid, obj, ctx=None: obj.state == 'submitted',
            'college_enrollment_request.mt_request_approved': lambda self, cr, uid, obj, ctx=None: obj.state == 'approved',
            'college_enrollment_request.mt_request_rejected': lambda self, cr, uid, obj, ctx=None: obj.state == 'rejected',
        },
    }

    def submit_request(self):
        self.state = 'submitted'
        # Post a message to the chatter
        self.message_post(body=f"Enrollment request for course <b>{self.course_id.name}</b> submitted by {self.student_id.name}.", subject="Request Submitted", message_type='notification')

    def approve_request(self):
        self.state = 'approved'
        # Post a message to the chatter
        self.message_post( body=f"Enrollment request for course <b>{self.course_id.name}</b> approved.", subject="Request Approved", message_type='notification' )

    def reject_request(self, reason):
        self.state = 'rejected'
        # Post a message to the chatter
        self.message_post(body=f"Enrollment request for course <b>{self.course_id.name}</b> rejected. Reason: {reason}", subject="Request Rejected", message_type='notification')

    def add_student_to_followers(self, partner_id):
        # Subscribe a partner (e.g., Registrar staff) to receive chatter notifications
        self.message_subscribe([partner_id])

    def remove_student_from_followers(self, partner_id):
        # Unsubscribe a partner from chatter notifications
        self.message_unsubscribe([partner_id])
