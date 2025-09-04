# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Escuela',
    'version': '1.0',
    'category': 'Education',
    'sequence': 10,
    'summary': 'Gestión de alumnos para instituciones educativas',
    'description': """
Módulo de Gestión Escolar
=========================

Este módulo permite gestionar la información de los alumnos de una institución educativa.

Características:
* Registro de alumnos con información personal
* Gestión de datos académicos
* Seguimiento de estudiantes
    """,
    'depends': ['base'],
    'data': [
        'data/sequences.xml',
        'security/ir.model.access.csv',
        'views/alumno_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
