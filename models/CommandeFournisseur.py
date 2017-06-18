# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CommandeFournisseur(models.Model):
     _name = 'gctjara.cmdfournisseur'
     
     _rec_name = 'numero'
     
     _inherit='mail.thread'
     
     numero = fields.Char(
         string='Numero ',
        # default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.cmdfrs.seq')
        default=lambda self: self._newrecord(),
        store=True,
        readonly=True
        
     )
     emplacement = fields.Selection(
         string='Emplacement',
         default='commande',

         selection=[
             ('commande', 'Commandé'),
             ('route', 'En route'),
             ('depot', 'Au dépôt'),

         ]
     )

     @api.model
     def _newrecord(self):
         sequence = self.env['ir.sequence'].search([('code','=','gctjara.cmdfrs.seq')])
         next= sequence.get_next_char(sequence.number_next_actual)
         return next
     
     @api.model
     def create(self, vals):
        vals['numero'] = self.env['ir.sequence'].next_by_code('gctjara.cmdfrs.seq')
        return super(CommandeFournisseur, self).create(vals)
     
     datecommande = fields.Date('Date',
                            required=True,
                            default=fields.datetime.now(),
                            help='Date création',
                            readonly=True)
     
     datereception = fields.Date('Date de reception',
                            required=True,
                            default=fields.datetime.now(),
                            help='Date   reception  de la commande ')
     
     description = fields.Text(
         String='Description',
         default='Liste des descritpions'
         )
     texthtml=fields.Html(string='Log' )
     
     fournisseur_id = fields.Many2one(
         comodel_name='gctjara.fournisseur',
         string="Fournisseur",
         ondelete='restrict'
         )
      
     attachment = fields.One2many(
         'ir.attachment',
         'cmdfournisseur',
         string='Pièces jointes'
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
        comodel_name='gctjara.lignecmdachat',
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
           for rec in self :
               montanttot = 0
               montantht = 0
               montantremise = 0
               montanttva = 0
               for lca in rec.lignecmd_id:
                       montanttot += lca.prix_total
                       montantht +=lca.prix_ht
                       montantremise +=lca.prix_ht*(float(lca.remise/100))
                       montanttva += (lca.prix_ht*(1 - (float(lca.remise/100))))*(float(lca.tva/100))
               rec.montant=montanttot
               rec.montant_ht=montantht
               rec.montanttva=montanttva
               rec.montantremise=montantremise


  
     
     def write(self, values):
        print values
        if values.has_key('state'):
            if values.get('state') == 'sa':
                values['state'] = 'br'
        result = super(CommandeFournisseur, self).write(values)
        return result

     @api.multi
     def afficher(self):
        print "afficher()"
        raise ValidationError('id commande : ' + str(self.id))
        return True

     def cmdfrs_brouillon(self):

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

            
     def create_factachat(self):
        sequences = self.env['ir.sequence'].next_by_code('gctjara.factureachat.seq') 
        record = self.env['gctjara.factureachat'].create({
            
              'numero' :  sequences,
              'datefact': self.datereception,
              'fournisseur_id':self.fournisseur_id.id,
              'commande_id' : self.id, 

            })
        
        for rec in self:
            for r in rec.lignecmd_id :
                r.reffact=  record.id
                record1 = self.env['gctjara.lignefactachat'].create({
                    'quantite':r.quantite,
                    'quantitetot': r.quantitetot,
                    'embalageproduit_id':r.embalageproduit_id.id,
                    'prix_ht': r.prix_ht,
                    'prix_total':r.prix_total,
                    'facture_id':record.id,
                    'prixunit':r.prixunit,
                    'tva':r.tva,
                    'remise': r.remise,
                    })
        return True
    
     def create_bon_entree(self):

         sequences = self.env['ir.sequence'].next_by_code('gctjara.bonentree.seq')
         record = self.env['gctjara.bonentree'].create({

             'numero': sequences,
             'date': fields.datetime.now().strftime('%m/%d/%Y %H:%M'),
             'fournisseur_id': self.fournisseur_id.id,
             'commande_id': self.id

         })
         print ("Commmande id  =================>"+str(self.id))

         for rec in self:
             for r in rec.lignecmd_id:
                 record1 = self.env['gctjara.lignebonentree'].create({
                     'quantite': r.quantite,
                     'quantitetot': r.quantitetot,
                     'embalageproduit_id': r.embalageproduit_id.id,
                     'prix_total': r.prix_total,
                     'prixunit': r.prixunit,
                     'prix_ht': r.prix_ht,
                     'tva': r.tva,
                     'remise': r.remise,
                     'bonentree_id': record.id,
                     'commande_id': self.id #[(0,0,self.id)]

                 })
         return True

    
    
    
     @api.one
     def cmdfrs_valider(self):
        info1 =str(self.description)
        info2=str('Commande fournisseur valide le: ' + str(fields.datetime.now().strftime('%d/%m/%Y %H:%M')))
        texthtml="<ul><li>"+info1+"</li><br/><li>"+info2+"</li></ul>"
        self.write({
            'state': 'va',
            'description': info1 +"\n" +info2,
            'texthtml':texthtml,
            'emplacement': 'route'

            })
        self.create_factachat()

        return True

     def cmdfrs_terminer(self):
        self.write({
            'state': 'tr',
            'emplacement': 'depot'
        })
        self.create_bon_entree()
        return True
    
     def cmdfrs_annuler(self):
        if self.valid=='Confirme':
            raise ValidationError("Cette commande fournisseur est verouillee!")
        self.write({'state': 'an'})
        return True

     


class Attachment(models.Model):
  
     _inherit = 'ir.attachment'
     _name = 'ir.attachment'
       
     cmdfournisseur = fields.Many2one(
        'gctjara.cmdfournisseur',
        string="Pièces jointes"
    ) 
