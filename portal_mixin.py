from odoo import models, fields, api
from odoo.exceptions import AccessError

class TuitionInvoice(models.Model):
    _name = 'college.tuition.invoice'
    _description = 'Tuition Invoice'
    _inherit = ['portal.mixin']  # <-- Enables portal access

    student_id = fields.Many2one('res.partner', string='Student', required=True)
    invoice_date = fields.Date(string='Invoice Date', default=fields.Date.today())
    amount_total = fields.Monetary(string='Total Amount')
    currency_id = fields.Many2one('res.currency', string='Currency')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], default='draft')

    # Optional: Sharing token for portal access
    portal_token = fields.Char(string="Portal Token", copy=False)

    def generate_portal_url(self):
        """Generate a secure portal URL for the invoice"""
        self.ensure_one()
        # Generates a URL like /my/invoice/<id>?access_token=<token>
        return self.portal_url()

    def check_student_access(self, partner_id):
        """Verify that a partner has access to this invoice"""
        if self.student_id.id != partner_id:
            raise AccessError("You do not have access to this invoice.")
        return True

    def share_with_student(self):
        """Generate a sharing token for portal access"""
        self.ensure_one()
        token = self.portal_share()
        return f"/my/invoice/{self.id}?access_token={token}"

    def mark_as_paid(self):
        self.state = 'paid'
        # Optional: Notify student via email or portal
        portal_url = self.generate_portal_url()
        self.message_post(
            body=f"Your invoice <b>{self.id}</b> has been marked as paid. You can view it here: {portal_url}",
            subject="Invoice Paid",
            message_type='notification'
        )
