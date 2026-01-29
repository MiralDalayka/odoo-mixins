from odoo import models, fields, api

class CrmLead(models.Model):
    _name = 'crm.lead'
    _description = 'CRM Lead'
    _inherit = ['utm.mixin', 'mail.thread']

    name = fields.Char(string='Lead Name', required=True, tracking=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    description = fields.Text(string='Notes')

    def set_utm_campaign(self, source=None, medium=None, campaign=None, content=None):
        """
        Set UTM parameters for the lead
        Example: Google Ads, Email Newsletter, A/B testing content
        """
        self.ensure_one()
        if source:
            self.utm_source = source
        if medium:
            self.utm_medium = medium
        if campaign:
            self.utm_campaign = campaign
        if content:
            self.utm_content = content

        # Optional: Post message in chatter
        self.message_post(
            body=f"UTM data updated: Source={self.utm_source}, Medium={self.utm_medium}, "
                 f"Campaign={self.utm_campaign}, Content={self.utm_content}",
            subject="UTM Update",
            message_type='notification'
        )

    def get_utm_summary(self):
        """Return a dictionary summarizing the UTM tracking info"""
        self.ensure_one()
        return {
            'utm_source': self.utm_source,
            'utm_medium': self.utm_medium,
            'utm_campaign': self.utm_campaign,
            'utm_content': self.utm_content,
        }
