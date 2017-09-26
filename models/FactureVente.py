# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime



class FactureVente(models.Model):
    
     _name = 'gctjara.facturevente'
     
     _rec_name = 'numero'
     
     _inherit = 'mail.thread'
     
     numero = fields.Char(
        string='N° facture',
        required=True,
        index=True,
        size=50,
        default= lambda self : self._newrecord()
       
    )

     @api.model
     def _newrecord(self):
         sequence = self.env['ir.sequence'].search([('code', '=', 'gctjara.facturevente.seq')])
         next = sequence.get_next_char(sequence.number_next_actual)
         return next

     @api.model
     def create(self, vals):
         vals['numerocmdc'] = self.env['ir.sequence'].next_by_code('gctjara.facturevente.seq')
         return super(FactureVente, self).create(vals)
    
     datefact = fields.Date(
        string='Date facture',
        required=True,
        default=fields.datetime.now(),
        help='La date de création de la facture'
    )
    
     datepayfact = fields.Date(
        string='Date payment',
        
        default=fields.datetime.now(),
        help='La date de payment de la facture'
    )

     description = fields.Text(
        string='Commentaire',
        required=False,
        help='Champ libre pour la saisie de commentaires'
    )

  
     valid = fields.Boolean(
        string='Ne pas annuler',
        default=False
    )
     
     state = fields.Selection(
        string='Etat',
        default='sa',
        selection=[
            ('sa', 'Saisie'),
            ('br', 'Brouillon'),
            ('va', 'Validee'),
            ('pa', 'Payee'),
            ('an', 'Annulee')
        ]
    )


     lignefact_id = fields.One2many(
        string='Produits',
        comodel_name='gctjara.lignefactvente',
        inverse_name='facture_id'
         )
     
     client_id = fields.Many2one('gctjara.client',
                                   string="Client",
                                   ondelete='restrict'
                                   )

     adresse = fields.Char(
         string='Adresse',
         related='client_id.adresse',
         readonly="1",
         store=True
     )

     bonlivraison_id = fields.Many2one(
         string="Bon livraison N°",
         ondelete='restrict',
         comodel_name='gctjara.bonlivraison'
                                   )
         
         
    
     attachment = fields.One2many(
         'ir.attachment',
         'facturevente',
          string='Pièce jointe'
                                )
     
     etatreglement=fields.Char(
        string='Etat facture',
        readonly='1',
        store=True,
        default=''
        )
     refregvente = fields.Many2many(comodel_name='gctjara.regvente',string='Réf reglement')
      
     attachment = fields.One2many('ir.attachment',
                               'factureachat',
                                string='Pièce jointe'
                                )

     currency_id = fields.Many2one('res.currency', string='Currency',
                                   default=lambda self: self.env.user.company_id.currency_id)

     timbre=fields.Float(
        string ='Timbre',
        default=0.500,
        digits=(16, 3),
        store=True
        )
    
     montantht = fields.Float(
         string='Montant HT',
         compute='_montant_totale',
         digits=(16, 3),
         default = 0.0,
         store=True
    )
     montant = fields.Float(
         string='Montant',
         compute='_montant_totale',
         digits=(16, 3),
         default = 0.0,
         store=True
    )
     montantttc=fields.Float(
         string='Montant TTC',
         compute='_montant_ttc',
         digits=(16, 3),
         default = 0.0,
         store=True
        )
     montantremise = fields.Float(
         string='Remise',
         compute='_montant_totale',
         digits=(16, 3),
         default=0.0,
         store=True
     )

     montanttva  = fields.Float(
         string='TVA',
         compute='_montant_totale',
         digits=(16, 3),
         default=0.0,
         store=True
     )


     @api.multi
     @api.depends("lignefact_id")
     def _montant_totale(self):
         for rec in self :

            montanttot=0
            mht=0
            montantremise=0
            montanttva=0
            for lfa in rec.lignefact_id:
                   montanttot = montanttot + lfa.prix_total
                   mht+= lfa.prix_ht
                   montantremise += lfa.prix_ht * (float(lfa.remise / 100))
                   montanttva +=  (lfa.prix_ht * (1-float(lfa.remise / 100)))*(float(lfa.tva / 100))

            rec.montant=montanttot
            rec.montantht=mht
            rec.montantremise=montantremise
            rec.montanttva=montanttva

     @api.one
     @api.depends("montant","timbre")
     def _montant_ttc(self):
       mmttc=0
       for mnt in self:
               mmttc = self.montant + self.timbre
       self.montantttc=mmttc
    
