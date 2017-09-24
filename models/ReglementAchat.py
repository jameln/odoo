# -*- coding: utf-8 -*-

from odoo import models, fields, api
import dateutil.parser

class ReglementAchat(models.Model):

    _name = 'gctjara.regachat'
    
    _rec_name = 'numero'

    _inherit = 'mail.thread'
    
    _order = "dateecheance desc"
    
    numero = fields.Char(
        string='Numero règlement',
        required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('gctjara.regachat.seq')
                         )
    
    date = fields.Date(string='Date règlement',
                      required=True,
                      default=fields.datetime.now(),
                      help='La date de création de la facture'
                      )
    
    datevaleur = fields.Date(
        string='Date valeur',
        default=fields.datetime.now(),
                            )
    
    dateoperation = fields.Date(
        string='Date d\'opération',
        default=fields.datetime.now(),
                            )
    dateecheance = fields.Date(
        string='Date d\'écheance',
        default=fields.datetime.now(),
                            )
    duration = fields.Integer(
        string='Durée de raprrochement',
        compute='_get_duration'
    )

    @api.depends('date', 'datevaleur')
    def _get_duration(self):
        for r in self:
            start_date = fields.Datetime.from_string(r.date)
            end_date = fields.Datetime.from_string(r.datevaleur)
            r.duration = (end_date - start_date).days

    

   
    prixttc = fields.Float(
        string='Prix TTC',
        
        digits=(16, 3)
    )

    facture_id = fields.Many2many(
        string='Réf. facture',
        comodel_name='gctjara.factureachat'
    )
  
            

    modepayment = fields.Selection(
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
    etatrapp = fields.Selection(
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

    numerochq = fields.Char(string='Numero')

    
    description = fields.Text(
        string='Description',
       
    )
    upload_file = fields.Binary(string='Upload File')
    
    file_name = fields.Char(string='File Name')

    def _cron_check_reglement_achat_expiration_date(self):
        print "reg achat cron in"
        regachat_ids = self.search([])
        print regachat_ids
#         config = self.env['ostool.config'].search_read([], order='write_date DESC', limit=1)
#         if not config:
#             raise UserError("Configuration Introuvable")
#         config = config[0]
#         alert_period = config.get('alert_period')
        # responsible_id = config.get('responsible_partner_id')
        about = 'regachat'
        for reg_id in regachat_ids:
            notification = False
            name = u""
            description = u""
#             rapproche = self.env['gctjara.regachat'].search_read([('regachat_id', '=', reg_id.id)], ['expiration'], order='dateecheance DESC')
            reg = self.browse(reg_id.id)
          
            
            date_reg =  dateutil.parser.parse(reg.date).date() # datetime.strptime(reg.date, '%Y-%m-%d %H:%M:%S')
            datech_reg=  dateutil.parser.parse(reg.dateecheance).date() #datetime.strptime(reg.dateecheance, '%Y-%m-%d %H:%M:%S')
            
            if date_reg == datech_reg :
                print " egale "
            elif date_reg > datech_reg :
                print  " inf "
            else :
                print " sup "
                
           
                
                
            
#             if rapproche:
#                 expiration = rapproche[0].get('expiration')
#                 if expiration <= 0:
#                     notification = True
#                     notification_type = 'notification'
#                     name = u"Expiration"
#                     description = u"Le contrat d'assurance du véhicule '" + v.name + u"' est expiré."
#                 elif expiration <= alert_period:
#                     notification = True
#                     notification_type = 'warning'
#                     name = u"Délais d'expiration proche"
#                     description = u"Le contrat d'assurance du véhicule '" + v.name + u"' expire dans " + unicode(str(expiration), 'utf-8') + u" jour(s)."
#             else:
#                 notification = True
#                 notification_type = 'info'
#                 name = u"Risque"
#                 description = u"Le véhicule '" + v.name + u"' ne possède aucun contrat d'assurance."
#             if notification :
#                 # print description
#                 self.env['gctjara.notification'].create({
#                     'name': name,
#                     'description': description,
#                     'notification_level': alert_type,
#                     'about': about,
#                     'notification_date': fields.datetime.today(),
#                     'regachat_id': v.id
#                 })
        print "reg achat cron out"
        return True
