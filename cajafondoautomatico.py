#! /usr/bin/env python
# coding=utf-8
#
# 
# Este script dibuja el perfil exterior de corte la caja en un solo 
# path cerrado y añade despues los otros flejes necesarios con colores
# diferentes para identificarlos.
#     rojo > para cortes y perfil exterior
#     azul > para hendidos
#     verde > para taladros
#     amarillo > medios cortes
#
# TODO:
#     agregar opción de dibujo en cm/in
#     mover dibujo al centro del documento
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

__version__ = "0.2"

import inkex

class GenerarEstuche(inkex.EffectExtension):

    def add_arguments(self, pars):
        pars.add_argument("--width", type=float, default=30.0, help="Ancho de la caja")
        pars.add_argument("--height", type=float, default=30.0, help="Alto de la caja")
        pars.add_argument("--depth", type=float, default=30.0, help="Largo de la caja")
        pars.add_argument("--glue_tab", type=float, default=30.0, help="Ancho pestaña de engomado")
        pars.add_argument("--close_tab", type=float, default=30.0, help="Alto pestaña de cierre")
        pars.add_argument("--side_tabs", type=float, default=30.0, help="Alto pestañas laterales de cierre")
        pars.add_argument("--use_material_compensation", type=inkex.Boolean, default=False, help="Aplicar compensación de material")
        pars.add_argument("--material_compensation", type=float, default=0.2, help="Grueso del material.")
        pars.add_argument("--unit", default="mm", help="Tipo de unidades")

    def effect(self):
        centro_ancho_documento = self.svg.unittouu(self.document.getroot().get('width'))/2
        centro_alto_documento = self.svg.unittouu(self.document.getroot().get('height'))/2

        medida_pestana1=5
        medida_pestana2=1
        medida_pestana3=4
        medida_pestana4=3

        ancho_caja = self.svg.unittouu(str(self.options.width) + self.options.unit)
        alto_caja = self.svg.unittouu(str(self.options.height) + self.options.unit)
        largo_caja = self.svg.unittouu(str(self.options.depth) + self.options.unit)
        ancho_pestana_cola = self.svg.unittouu(str(self.options.glue_tab) + self.options.unit)
        alto_pestana_cierre = self.svg.unittouu(str(self.options.close_tab) + self.options.unit)
        alto_pestana = self.svg.unittouu(str(self.options.side_tabs) + self.options.unit)
        compensacion=0.0
		
        if self.options.use_material_compensation==True:
            compensacion=self.svg.unittouu(str(self.options.material_compensation) + self.options.unit)
            
        if self.options.unit=="cm":
            medida_pestana1=0.5
            medida_pestana2=0.1
            medida_pestana3=0.4
            medida_pestana3=0.3
			
        if self.options.unit=='in':
            medida_pestana1=0.196
            medida_pestana2=0.039
            medida_pestana3=0.157
            medida_pestana3=0.118

        medida1_pestanas_laterales=self.svg.unittouu(str(medida_pestana1) + self.options.unit)
        medida2_pestanas_laterales=self.svg.unittouu(str(medida_pestana2) + self.options.unit)
        medida3_pestanas_laterales=self.svg.unittouu(str(medida_pestana3) + self.options.unit)
        medida4_pestanas_laterales=self.svg.unittouu(str(medida_pestana4) + self.options.unit)

        id_caja = self.svg.get_unique_id('estuche-fondoautomatico')
        group = self.svg.get_current_layer().add(inkex.Group(id=id_caja))
        estilo_linea_cortes = {'stroke': '#FF0000', 'fill': 'none', 'stroke-width': str(self.svg.unittouu('1px'))}
        estilo_linea_hendidos = {'stroke': '#0000FF', 'fill': 'none', 'stroke-width': str(self.svg.unittouu('1px'))}
        estilo_linea_taladros = {'stroke': '#00FF00', 'fill': 'none', 'stroke-width': str(self.svg.unittouu('1px'))}
        estilo_linea_medioscortes = {'stroke': '#00FFFF', 'fill': 'none', 'stroke-width': str(self.svg.unittouu('1px'))}

        # line.path --> M = coordenadas absolutas
        # line.path --> l = dibuja una linea desde el punto actual a las coordenadas especificadas
        # line.path --> c = dibuja una curva beizer desde el punto actual a las coordenadas especificadas
        # line.path --> q = dibuja un arco desde el punto actual a las coordenadas especificadas usando un punto como referencia
        # line.path --> Z = cierra path
        
        #Perfil Exterior de la caja
        line = group.add(inkex.PathElement(id=id_caja + '-perfil-exterior'))
        line.path = [
			['M', [0, 0]],
			['l', [0, 0-largo_caja-compensacion]],
			['l', [compensacion, 0]],
			['q', [0,0-alto_pestana_cierre,alto_pestana_cierre, 0-alto_pestana_cierre]],
			['l', [ancho_caja-(alto_pestana_cierre*2)-(compensacion*2), 0]],
			['q', [alto_pestana_cierre,0,alto_pestana_cierre,alto_pestana_cierre]],
			['l', [compensacion, 0]],
			['l', [0, (largo_caja-compensacion)]],
			['l', [medida4_pestanas_laterales, 0-medida4_pestanas_laterales]],
			['l', [0,0-(alto_pestana-medida4_pestanas_laterales)]],
			['l', [(largo_caja-compensacion-medida2_pestanas_laterales-medida3_pestanas_laterales-medida4_pestanas_laterales-compensacion), 0]],
			['l', [medida3_pestanas_laterales, (alto_pestana-medida2_pestanas_laterales-medida1_pestanas_laterales)]],
			['l', [medida2_pestanas_laterales, medida2_pestanas_laterales]],
			['l', [0, medida1_pestanas_laterales]],
			['l', [0,compensacion]],
			['l', [ancho_caja, 0]],
			['l', [0,compensacion]],
			['l', [compensacion, 0]],
			['l', [0, 0-medida1_pestanas_laterales]],
			['l', [medida2_pestanas_laterales, 0-medida2_pestanas_laterales]],
			['l', [medida3_pestanas_laterales, 0-(alto_pestana-medida2_pestanas_laterales-medida1_pestanas_laterales)]], 
			['l', [(largo_caja-compensacion-medida2_pestanas_laterales-medida3_pestanas_laterales-medida4_pestanas_laterales), 0]],
			['l', [0,alto_pestana-medida4_pestanas_laterales]],
			['l', [medida4_pestanas_laterales, medida4_pestanas_laterales]],
			['l', [0, alto_caja]],
			['l', [0-((largo_caja/2)-compensacion),largo_caja/2]],
			['l', [0-((largo_caja/2)-compensacion-(medida2_pestanas_laterales)*2),0]],
			['l', [0-(medida2_pestanas_laterales),0-((largo_caja/2)-medida2_pestanas_laterales)]],
			['l', [0-medida2_pestanas_laterales,0-medida2_pestanas_laterales]],
			['l', [0-medida2_pestanas_laterales,medida2_pestanas_laterales]],
			['l', [0,largo_caja*0.7]],
			['l', [0-(((largo_caja*0.5)-medida2_pestanas_laterales)/2),0]],
			['l', [0-(((largo_caja*0.5)-medida2_pestanas_laterales)/2),0-((largo_caja*0.7)-(largo_caja*0.5))]],
			['l', [0-((ancho_caja/2)-((largo_caja*0.5)-medida2_pestanas_laterales)),0]],
			['l', [medida2_pestanas_laterales,medida3_pestanas_laterales]],
			['l', [0-((largo_caja*0.7)-(largo_caja*0.5))-medida3_pestanas_laterales,((largo_caja*0.7)-(largo_caja*0.5))-medida3_pestanas_laterales]],
			['l', [0-(((ancho_caja/2)-((largo_caja*0.5)))+((largo_caja*0.7)-(largo_caja*0.5))),0]],
			['l', [0-medida3_pestanas_laterales,0-((largo_caja*0.7)+(compensacion*2)+medida2_pestanas_laterales)]],
			['l', [0-((largo_caja/2)),largo_caja/2]],
			['l', [0-((largo_caja/2)-(medida2_pestanas_laterales)*2),0]],
			['l', [0-(medida2_pestanas_laterales),0-((largo_caja/2)-medida2_pestanas_laterales)]],
			['l', [0-medida2_pestanas_laterales,0-medida2_pestanas_laterales]],
			['l', [0-medida2_pestanas_laterales,medida2_pestanas_laterales]],
			['l', [0,largo_caja*0.7]],
			['l', [0-(((largo_caja*0.5)-medida2_pestanas_laterales)/2),0]],
			['l', [0-(((largo_caja*0.5)-medida2_pestanas_laterales)/2),0-((largo_caja*0.7)-(largo_caja*0.5))]],
			['l', [0-((ancho_caja/2)-((largo_caja*0.5)-medida2_pestanas_laterales)),0]],
			['l', [medida2_pestanas_laterales,medida3_pestanas_laterales]],
			['l', [0-((largo_caja*0.7)-(largo_caja*0.5))-medida3_pestanas_laterales,((largo_caja*0.7)-(largo_caja*0.5))-medida3_pestanas_laterales]],
			['l', [0-(((ancho_caja/2)-((largo_caja*0.5)))+((largo_caja*0.7)-(largo_caja*0.5))),0]],
			['l', [0-medida3_pestanas_laterales,0-((largo_caja*0.7)+compensacion)]],
			['l', [0, 0-medida2_pestanas_laterales]],
			['l', [0-ancho_pestana_cola, 0-(ancho_pestana_cola/2)-compensacion]],
			['l', [0, 0-(alto_caja-ancho_pestana_cola-(medida2_pestanas_laterales*2)-(compensacion*2))]],
			['l', [ancho_pestana_cola, 0-(ancho_pestana_cola/2)-compensacion]],
			['Z', []]
        ]
        line.style = estilo_linea_cortes
        
        #Hendidos
        line = group.add(inkex.PathElement(id=id_caja + '-perfil-hendidos-1'))
        line.path = [
			['M', [0,0]],
			['l', [0,alto_caja]],
			['Z', []]
		]
        line.style = estilo_linea_hendidos

        line = group.add(inkex.PathElement(id=id_caja + '-perfil-hendidos-2'))
        line.path = [
			['M', [ancho_caja,0]],
			['l', [0,alto_caja]],
			['Z', []]
		]
        line.style = estilo_linea_hendidos
        
        line = group.add(inkex.PathElement(id=id_caja + '-perfil-hendidos-3'))
        line.path = [
			['M', [ancho_caja+largo_caja,0]],
			['l', [0,alto_caja]],
			['Z', []]
		]
        line.style = estilo_linea_hendidos
        
        line = group.add(inkex.PathElement(id=id_caja + '-perfil-hendidos-4'))
        line.path = [
			['M', [ancho_caja+ancho_caja+largo_caja,0]],
			['l', [0,alto_caja]],
			['Z', []]
		]
        line.style = estilo_linea_hendidos
        
        line = group.add(inkex.PathElement(id=id_caja + '-perfil-hendidos-5'))
        line.path = [
			['M', [0,0]],
			['l', [ancho_caja,0]],
			['Z', []]
		]
        line.style = estilo_linea_hendidos
        
        line = group.add(inkex.PathElement(id=id_caja + '-perfil-hendidos-6'))
        line.path = [
			['M', [0,alto_caja+compensacion]],
			['l', [((largo_caja+ancho_caja)*2)-(compensacion*2),0]],
			['Z', []]
		]
        line.style = estilo_linea_hendidos
 
        line = group.add(inkex.PathElement(id=id_caja + '-perfil-hendidos-7'))
        line.path = [
			['M', [ancho_caja+compensacion,compensacion]],
			['l', [(largo_caja-compensacion*2),0]],
			['Z', []]
		]
        line.style = estilo_linea_hendidos
        
        line = group.add(inkex.PathElement(id=id_caja + '-perfil-hendidos-8'))
        line.path = [
			['M', [(ancho_caja*2)+largo_caja+(compensacion*2),compensacion]],
			['l', [(largo_caja-compensacion*2),0]],
			['Z', []]
		]
        line.style = estilo_linea_hendidos
        
        line = group.add(inkex.PathElement(id=id_caja + '-perfil-hendidos-9'))
        line.path = [
			['M', [compensacion,0-(largo_caja+compensacion)]],
			['l', [ancho_caja-(compensacion*2),0]],
			['Z', []]
		]
        line.style = estilo_linea_hendidos
        
        line = group.add(inkex.PathElement(id=id_caja + '-perfil-taladro-1'))
        line.path = [
			['M', [ancho_caja-medida2_pestanas_laterales+compensacion,alto_caja+medida2_pestanas_laterales+compensacion]],
			['l', [0-((largo_caja*0.5)-compensacion),(largo_caja*0.5)-compensacion]],
			['Z', []]
		]
        line.style = estilo_linea_taladros
        
        line = group.add(inkex.PathElement(id=id_caja + '-perfil-taladro-2'))
        line.path = [
			['M', [((ancho_caja*2)+largo_caja)-medida2_pestanas_laterales+(compensacion*2),alto_caja+medida2_pestanas_laterales+compensacion]],
			['l', [0-((largo_caja*0.5)-compensacion),(largo_caja*0.5)-compensacion]],
			['Z', []]
		]
        line.style = estilo_linea_taladros

if __name__ == '__main__':
    GenerarEstuche().run()
