from odoo import models, fields, api

class ResPartner(models.Model):
    _description = "Informasi Penulis dan Penerbit"
    _inherit = ['res.partner']

    is_penulis = fields.Boolean(
        string='Penulis?',
    )
    is_penerbit = fields.Boolean(
        string='Penerbit?',
    )
    born_date = fields.Date(
        string='Tanggal Lahir',
    )
    death_date = fields.Date(
        string='Tanggal Wafat',
    )
    buku_ids = fields.Many2many(
        string='Daftar Buku',
        comodel_name='books.buku',
        relation='partner_buku_rel',
        column1='partner_id',
        column2='buku_id'
    )
    _sql_constraints = [
    ('unique_name', 'unique(name)', 'Nama sudah digunakan!'),
]

    
    
    
    
    
