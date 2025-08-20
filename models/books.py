from odoo import models, fields

class Buku(models.Model):
    _name = 'books.buku'
    _description = 'Data Buku'

    image = fields.Binary(string='Foto')
    name = fields.Char(string='Judul Buku', required=True)
    penulis = fields.Char(string='Penulis')
    jumlah = fields.Integer(string='Stok Buku', default=1)
    tanggal_terbit = fields.Date(string='Tanggal Terbit')
    kategori = fields.Selection([
        ('fiksi', 'Fiksi'),
        ('non-fiksi', 'Non-Fiksi')
    ], string='Kategori', default='fiksi')
    deskripsi = fields.Text(string='Deskripsi')
