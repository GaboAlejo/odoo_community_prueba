# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Alumno(models.Model):
    _name = 'escuela.alumno'
    _description = 'Alumno'
    _order = 'apellido_paterno, apellido_materno, nombre'
    _rec_name = 'nombre_completo'

    # Información personal
    nombre = fields.Char('Nombre', required=True, size=50)
    apellido_paterno = fields.Char('Apellido Paterno', required=True, size=50)
    apellido_materno = fields.Char('Apellido Materno', size=50)
    nombre_completo = fields.Char('Nombre Completo', compute='_compute_nombre_completo', store=True)
    
    # Información de contacto
    email = fields.Char('Correo Electrónico')
    telefono = fields.Char('Teléfono')
    direccion = fields.Text('Dirección')
    
    # Información académica
    fecha_nacimiento = fields.Date('Fecha de Nacimiento', required=True)
    edad = fields.Integer('Edad', compute='_compute_edad', store=True)
    grado = fields.Selection([
        ('1', 'Primer Grado'),
        ('2', 'Segundo Grado'),
        ('3', 'Tercer Grado'),
        ('4', 'Cuarto Grado'),
        ('5', 'Quinto Grado'),
        ('6', 'Sexto Grado'),
        ('7', 'Séptimo Grado'),
        ('8', 'Octavo Grado'),
        ('9', 'Noveno Grado'),
        ('10', 'Décimo Grado'),
        ('11', 'Undécimo Grado'),
        ('12', 'Duodécimo Grado'),
    ], string='Grado', required=True)
    
    # Información adicional
    numero_matricula = fields.Char('Número de Matrícula', required=True, copy=False, readonly=True, default=lambda self: _('Nuevo'))
    fecha_ingreso = fields.Date('Fecha de Ingreso', default=fields.Date.today, required=True)
    activo = fields.Boolean('Activo', default=True)
    notas = fields.Text('Notas Adicionales')
    
    # Información de contacto de emergencia
    contacto_emergencia = fields.Char('Contacto de Emergencia')
    telefono_emergencia = fields.Char('Teléfono de Emergencia')
    parentesco = fields.Char('Parentesco')

    @api.depends('nombre', 'apellido_paterno', 'apellido_materno')
    def _compute_nombre_completo(self):
        for record in self:
            nombre_completo = record.nombre or ''
            if record.apellido_paterno:
                nombre_completo += f' {record.apellido_paterno}'
            if record.apellido_materno:
                nombre_completo += f' {record.apellido_materno}'
            record.nombre_completo = nombre_completo.strip()

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        today = fields.Date.today()
        for record in self:
            if record.fecha_nacimiento:
                age = today.year - record.fecha_nacimiento.year
                if today.month < record.fecha_nacimiento.month or (today.month == record.fecha_nacimiento.month and today.day < record.fecha_nacimiento.day):
                    age -= 1
                record.edad = age
            else:
                record.edad = 0

    @api.model
    def create(self, vals):
        if vals.get('numero_matricula', _('Nuevo')) == _('Nuevo'):
            vals['numero_matricula'] = self.env['ir.sequence'].next_by_code('escuela.alumno') or _('Nuevo')
        return super(Alumno, self).create(vals)

    @api.constrains('fecha_nacimiento')
    def _check_fecha_nacimiento(self):
        for record in self:
            if record.fecha_nacimiento and record.fecha_nacimiento > fields.Date.today():
                raise ValidationError(_('La fecha de nacimiento no puede ser futura.'))

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError(_('Por favor ingrese un correo electrónico válido.'))
