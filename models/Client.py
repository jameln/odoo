# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Client(models.Model):
     _name = 'gctjara.client'

     _rec_name = 'name'

     _inherit='mail.thread'

     
     name = fields.Char('Nom', required=True)
    

     company_name = fields.Char('Company Name')
     
     image = fields.Binary(
                           string='Image',
                           attachment=True,
                           help="This field holds the image used as avatar for this contact, limited to 1024x1024px",
                           )
     
     email = fields.Char('Email')
     
     phone = fields.Char('Telephone')
     
     fax = fields.Char('Fax')
     
     mobile = fields.Char('Portable')
     
     adresse = fields.Char('Adresse')
     
     street = fields.Char()
     
     street2 = fields.Char()
     
     zip = fields.Char(change_default=True)
     
     city = fields.Char()
     
     active = fields.Boolean(default=True)
     
#      produits_id = fields.Many2one(
#          string='Produits',
#          comodel_name='gctjara.produits'
#          )
#         
     
     commande_id = fields.One2many(
       string="Commandes",
       ondelete='restrict',
       comodel_name='gctjara.cmdclient',
       inverse_name='client_id',
                                  )
       
     facture_id = fields.One2many(
       string="Factures",
       ondelete='restrict',
       comodel_name='gctjara.facturevente',
       inverse_name='client_id',
       )

     nature_reg_acceptee=fields.Selection(
        string='Mode de règlement acceptées',
        default='',
        selection=[
            ('ch', 'Chèque'),
            ('es', 'Espèce'),
            ('vr', 'Virement'),
            ('tr', 'Traite'),
            ('pr', 'Prélevement')
        ]
    )
     mode_reglement_autorisee=fields.Selection(
        string='Mode de règlement autoriées',
        default='',
        selection=[
            ('livraison', 'A la livraison'),
            ('Contre', 'Contre rembourssement'),
            ('Suivi', 'Suivi'),
            ('avance', 'A l\'avance'),
            ('determiner', 'A determiner')
        ]
    )
     type_de_relation =fields.Selection(
        string='Type de relation',
        default='',
        selection=[
            ('livraison', 'Intense'),
            ('Confiante', 'Confiante'),
            ('Inexistante', 'Inexistante'),
            ('Réserve', 'Réservée'),
            ('Negative', 'Negative'),
            ('Limite', 'Limitée')
        ]
    )
 
     
