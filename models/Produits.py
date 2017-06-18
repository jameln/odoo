# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Produits(models.Model):

    _name = 'gctjara.produits'
    
    _rec_name = 'name'

    name = fields.Char(
        string='Appelation',
        required=True,
        index=True,
        help='Le nom du produit',
        size=50,
        
        )    

    code = fields.Char(
        string='Code',
        required=True,
        index=True,
        help='Le code du produit',
        size=50
        )

    # dateexpiration = fields.Datetime(
    #     string='Date Expiration',
    #     default=fields.datetime.now(),
    #     )
    
    description = fields.Text(
        string='Description'
        )
    
    prixunit=fields.Float(
        string='Prix unitaire',
        default=0.0,
        digits=(16, 3),
        required=True
        )
    
    prixvente=fields.Float(
        string='Prix de vente',
        default=0.0,
        digits=(16, 3),
        required=True
        )
    

    produitemballee_ids = fields.One2many(
        comodel_name='gctjara.produitemballee',
        string='Emballage',
        inverse_name='produit_id'
    )
    
    emballages_id = fields.Many2many(
        comodel_name='gctjara.emballage', 
        string='Emballages',
        store=False
        )
    
