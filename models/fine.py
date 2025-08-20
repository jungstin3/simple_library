from odoo import models, fields, api

class Denda(models.Model):
    _name = 'fine.denda'
    _description = 'ini adalah denda'
    
    name = fields.Char(string='Nama Denda')
    jumlah = fields.Integer(string='Jumlah Denda')