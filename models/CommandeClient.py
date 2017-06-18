# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CommandeClient(models.Model):
     _name = 'gctjara.cmdclient'
     
     _rec_name = 'numerocmdc'
     
     _inherit='mail.thread'

     
     numerocmdc = fields.Char(
        string='Numero ',
        default=lambda self: self._newrecord(),
        store=True,
        readonly=True
        )
     
    
     @api.model
     def _newrecord(self):
         sequence = self.env['ir.sequence'].search([('code','=','gctjara.cmdclt.seq')])
         next= sequence.get_next_char(sequence.number_next_actual)
         return next
     
     @api.model
     def create(self, vals):
        vals['numerocmdc'] = self.env['ir.sequence'].next_by_code('gctjara.cmdclt.seq')
        return super(CommandeClient, self).create(vals)
    
     
     datecommande = fields.Date(
         string='Date',
         required=True,
         default=fields.datetime.now(),
         help='Date création',
         readonly=True
     )
     
     datelivraison = fields.Date(
         string='Date de livraison',
         required=True,
         default=fields.datetime.now(),
         help='Date livraison  de la commande '
         )
     
     attachment = fields.One2many(
         'ir.attachment',
         'cmdclient',
         string='Pièces jointes'
                                )
     
     description = fields.Text(
         String='Description'
         )

     valid = fields.Selection(
         string="Etat",
         required=True,
         selection=[
             ('Confirme', 'Confirmé'),
             ('NonConfirme', 'Non Confirmé')
         ],
         default='NonConfirme'
     )
     valid_bool = fields.Boolean(compute="_valid_bool")

     @api.one
     def toggle_valid(self):
         if self.valid == 'Confirme':
             self.valid = 'NonConfirme'
         else:
             self.valid = 'Confirme'
         return True

     @api.depends("valid")
     def _valid_bool(self):
         for v in self:
             v.valid_bool = (v.valid != 'NonConfirme')
     
     client_id = fields.Many2one(
          string="Client",
          ondelete='restrict',
          comodel_name='gctjara.client'
       )

     adresse=fields.Char(
         string='Adresse',
         related='client_id.adresse',
         readonly="1",
         store=True
     )
     reglement_autorisee=fields.Selection(
         string='Mode de règlement',
         related='client_id.mode_reglement_autorisee',
         readonly="1",
         store=True,
         selection=[
             ('livraison', 'A la livraison'),
             ('Contre', 'Contre rembourssement'),
             ('Suivi', 'Suivi'),
             ('avance', 'A l\'avance'),
             ('determiner', 'A determiner')
         ]
     )
     
     
     state = fields.Selection(
        string='Etat',
        default='sa',
        selection=[
            ('sa', 'Saisie'),
            ('br', 'Brouillon'),
            ('va', 'Validee'),
            ('tr', 'Terminee'),
            ('an', 'Annulee')
        ]
    )
     
     lignecmd_id = fields.One2many(
        string='Produits',
        comodel_name='gctjara.lignecmdvente',
        inverse_name='commande_id'
         )
     
     montant_ht = fields.Float(
         string='Montant HT',
         compute='_montant_totale',
         digits=(16, 3),
         default = 0.0,
         store=True
    ) 
     
     montant = fields.Float(
         string='Montant TTC',
         compute='_montant_totale',
         digits=(16, 3),
         default = 0.0,
         store=True
    )
     
     montanttva=fields.Float(
        string='TVA',
        compute='_montant_totale',
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



     @api.multi
     @api.depends("lignecmd_id")
     def _montant_totale(self):
         print("0.01")
         for rec in self:
             montanttot = 0
             montantht = 0
             montantremise = 0
             montanttva = 0
             for lca in rec.lignecmd_id:
                 print("0.02")
                 montanttot += lca.prix_total
                 montantht += lca.prix_ht
                 montantremise += lca.prix_ht * (float(lca.remise / 100))
                 montanttva += (lca.prix_ht * (1 - (float(lca.remise / 100)))) * (float(lca.tva / 100))
             rec.montant = montanttot
             rec.montant_ht = montantht
             rec.montanttva = montanttva
             rec.montantremise = montantremise

     def write(self, values):
        print values
        if values.has_key('state'):
            if values.get('state') == 'sa':
                values['state'] = 'br'
        result = super(CommandeClient, self).write(values)
        return result

     @api.multi
     def afficher(self):
        print "afficher()"
        raise ValidationError('id commande : ' + str(self.id))
        return True

     def cmdclt_brouillon(self):

        self.write({'state': 'br'})
        return True
    
     def getClientID(self):
        if self.client_id: 
            return {
                'name' : 'client',
                'res_model':'res.partner',
                'res_id':self.client_id.id,
                'view_type':'form',
                'view_mode':'form',
                'type':'ir.actions.act_window'
                
                }

     @api.multi
     def create_bon_livraison(self):
         
        sequences = self.env['ir.sequence'].next_by_code('gctjara.bonlivraison.seq') 
        record = self.env['gctjara.bonlivraison'].create({
            
              'numero' :  sequences,
              'date':fields.datetime.now().strftime('%m/%d/%Y %H:%M'),
              'client_id':self.client_id.id,

              'commande_id' :  self.id
              
               })
        
        for rec in self:
             for r in rec.lignecmd_id :
                 record1 = self.env['gctjara.lignebonlivraison'].create({
                     'quantite':r.quantite,
                     'quantitetot':r.quantitetot,
                     'embalageproduit_id':r.embalageproduit_id.id,
                     'prix_total':r.prix_total,
                     'commande_id':record.id,
                     'prixvente':r.prixvente,
                     'prix_ht':r.prix_ht,
                     'tva':r.tva,
                     'remise':r.remise,
                     'bonlivraison_id':record.id,
                     'commande_id':self.id
                     
                     })
        return True
    
    
    
     @api.multi
     def cmdclt_valider(self):

         self.write({
            'state': 'va',
            'description':'Commande client valide le: ' + fields.datetime.now().strftime('%d/%m/%Y %H:%M')+' par '+str(self.env.user.name),
            })  
         self.create_bon_livraison()
         return True

     def cmdclt_terminer(self):
        self.write({'state': 'tr'})
        return True
    
     def cmdclt_annuler(self):
        if self.valid=="Confirme":
            raise ValidationError("Cette commande client est verouillee!")
        self.write({'state': 'an'})
        return True

     


class Attachment(models.Model):
  
     _inherit = 'ir.attachment'
     _name = 'ir.attachment'
       
     cmdclient = fields.Many2one(
        'gctjara.cmdclient',
        string="Pièces jointes"
    )