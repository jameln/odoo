# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Notification(models.Model):
    _name = "gctjara.notification"
#     _order = "alert_date DESC"

    name = fields.Char(string="Titre", required=True)
    notification_date = fields.Date(string="Date",default=fields.datetime.now(), required=True)
    notification_level = fields.Selection(string="Niveau", selection=[
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('alert', 'Alerte')
    ], required=True)
    about = fields.Selection(string="A propos", selection=[
        ('regachat', 'Reglement d\'achat'),
        ('regvente', 'Reglement de vente'),
       
    ], required=True)
    description = fields.Text(string="Description")
    regachat_id = fields.Many2one(
        required=True,
        index=True,
        comodel_name="gctjara.regachat",
        string="Règlement"
)