# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ReglementVente(models.Model):

    _name = 'gctjara.regvente'
    
    _rec_name = 'numero'

    _inherit = 'mail.thread'

    
    numero = fields.Char(
        string='Numero règlement',
        required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.regvente.seq')
                         )
    
    date = fields.Date(string='Date règlement',
                      required=True,
                      default=fields.datetime.now(),
                      help='La date de création de la facture'
                      )
    
    datevaleur = fields.Date(string='Date valeur',
                            default=fields.datetime.now(),
                            )
    
    dateoperation=fields.Date(
        string='Date d\'opération',
        default=fields.datetime.now(),
                            )
    
    daterecption = fields.Date(string='Date réception',
                             default=fields.datetime.now(),
                             )

    duration = fields.Integer(
        string='Durée de raprrochement',
        compute='_get_duration'
    )

    @api.depends('date', 'daterecption')
    def _get_duration(self):
        for r in self:
            start_date = fields.Datetime.from_string(r.date)
            end_date = fields.Datetime.from_string(r.daterecption)
            r.duration = (end_date - start_date).days
    #
    # tauxtva = fields.Char(
    #     string='TVA',
    #
    #     digits=(16, 3)
    # )
    # prixht = fields.Float(
    #     string='Prix HT',
    #
    #     digits=(16, 3)
    # )
   
    prixttc = fields.Float(
        string='Prix TTC',
        
        digits=(16, 3)
    )

    facture_id = fields.Many2many(
        string='Réf. facture',
        comodel_name='gctjara.facturevente'
    )

    modepayment=fields.Selection(
        string='Mode de payment',
        default='',
        selection=[
            ('ch', 'Chèque'),
            ('es', 'Espèce'),
            ('vr', 'Virement'),
            ('tr', 'Traite'),
            ('pr', 'Prélevement')
        ]
    )
    etatrapp=fields.Selection(
        string='Etat de rapprochement',
        default='',
        selection=[
            ('cd', 'A céditer'),
            ('db', 'A débiter'),
            ('vs', 'A versé'),
            ('rp', 'Rapproché'),
        
        ]
    )

    def Rapproche(self):
        self.write({'etatrapp': 'rp'})
        return True


    numerochq=fields.Char(string='Numero')


    
    description = fields.Text(
        string='Description',
       
    )
    upload_file=fields.Binary(string='Upload File')
    
    file_name=fields.Char(string='File Name')

