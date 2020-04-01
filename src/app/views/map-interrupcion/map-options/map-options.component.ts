import { Component, Inject } from '@angular/core';
import { loadModules } from 'esri-loader';
import { MatBottomSheetRef } from '@angular/material/bottom-sheet';
import { MAT_BOTTOM_SHEET_DATA } from '@angular/material/bottom-sheet';
import { FormControl } from '@angular/forms';
import { MomentDateAdapter, MAT_MOMENT_DATE_ADAPTER_OPTIONS } from '@angular/material-moment-adapter';
import { DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';
import { MatDatepicker } from '@angular/material/datepicker';

import * as moment from 'moment';
import { Moment } from 'moment';

export const MY_FORMATS = {
  parse: {
    dateInput: 'MMMM',
  },
  display: {
    dateInput: 'MMMM',
    monthYearLabel: 'MMM',
    // dateA11yLabel: 'LL',
    // monthYearA11yLabel: 'MMMM',
  },
};

@Component({
  selector: 'app-map-options',
  templateUrl: './map-options.component.html',
  styleUrls: ['./map-options.component.scss'],
  providers: [
    {provide: MAT_DATE_LOCALE, useValue: 'es-ES'}, // Permite ver el calendario en español
    {
      provide: DateAdapter,
      useClass: MomentDateAdapter,
      deps: [MAT_DATE_LOCALE, MAT_MOMENT_DATE_ADAPTER_OPTIONS]
    },

    {provide: MAT_DATE_FORMATS, useValue: MY_FORMATS},
  ],
})
export class MapOptionsComponent {

  constructor(private bottomSheetRef: MatBottomSheetRef<MapOptionsComponent>, @Inject(MAT_BOTTOM_SHEET_DATA) public data: any) {}

  suiAnios: any[] = this.data.suiAnios;

  servicios: any[] = [
    {value: 'energia', viewValue: 'Energía'},
    {value: 'gas', viewValue: 'Gas'},
    {value: 'glp', viewValue: 'GLP'}
  ];

  errorMessage = '';

  date = new FormControl(moment());

  selectAnio = 2018; // Valor que actualiza el select

  somethingChanged(select: any): void {
    console.log(select);
  }

  chosenYearHandler(normalizedYear: Moment) {
    const ctrlValue = this.date.value;
    ctrlValue.year(normalizedYear.year());
    this.date.setValue(ctrlValue);
  }

  chosenMonthHandler(normalizedMonth: Moment, datepicker: MatDatepicker<Moment>) {
    const ctrlValue = this.date.value;
    ctrlValue.month(normalizedMonth.month());
    this.date.setValue(ctrlValue);
    datepicker.close();
  }

  // Cambiar apariencia del boton de opciones de Basemap a Claro
  changeOptionBtnToLight(): void {
    this.data.fabOptions[2].icon = 'wb_sunny';
    this.data.fabOptions[2].imgUrl = '';
    this.data.fabOptions[2].tooltip = 'Modo Claro';
    delete this.data.fabOptions[2].color; // Se elimina la propiedad 'color' del objeto con id 3 para dejarlo claro
  }

  async updateMap() {
    // this.changeOptionBtnToLight();

    console.log('datos desde abajo: ', this.data);
    console.log('valor zoom: ', this.data.view.zoom);
    // this.data.view.zoom = this.data.zoom;
    // this.data.view.center = [this.data.view.center.longitude, this.data.view.center.latitude];
    console.log('Propiedades Mapa Despues: ', this.data.view.map.layers.items[0].url);
    console.log('Propiedades basemap: ', this.data.view.map);
    const [CSVLayer] = await loadModules(['esri/layers/CSVLayer']);
    const url = 'assets/file_pqrs.csv';
    const template = {
      title: '{place}',
      content: 'Magnitude {mag} {type} hit {place} on {time}.'
    };
    const renderer = {
      type: 'heatmap',
      // field: 'numero_pqrs',
      colorStops: [
        { color: 'rgba(63, 40, 102, 0)', ratio: 0 }, // rango de 0 a 1
        { color: '#6300df', ratio: 0.083 },          // Azul claro
        { color: '#002dfe', ratio: 0.100 },          // Azul
        { color: '#00ff2c', ratio: 0.166 },          // Verde Clarito
        { color: '#a1ff00', ratio: 0.249 },          // Verde
        { color: '#e5ff00', ratio: 0.332 },          // Amarillo claro
        { color: '#fef700', ratio: 0.415 },          // Amarillo
        { color: '#ffc700', ratio: 0.498 },          // Amarillo oscuro
        { color: '#fea701', ratio: 0.581 },          // Naranja claro
        { color: '#ff6400', ratio: 0.664 },          // Naranja
        { color: '#ff3000', ratio: 1 }               // Rojo
      ],
      maxPixelIntensity: 2000,
      minPixelIntensity: 50
    };
    const layer = new CSVLayer({
      url,
      title: 'Interrupciones',
      copyright: 'DESARROLLADO POR JUAN CAMILO HERRERA - CIAD SSPD',
      popupTemplate: template,
      renderer
    });
    this.data.view.map.layers = layer; // Se agrega un nuevo layer CSV al mapa
    this.bottomSheetRef.dismiss(this.data); // cerrar modal y pasar datos a la vista padre
  }

}
