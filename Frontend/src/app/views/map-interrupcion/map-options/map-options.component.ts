import { Component, Inject } from '@angular/core';
import { loadModules } from 'esri-loader';
import { MatBottomSheetRef } from '@angular/material/bottom-sheet';
import { MAT_BOTTOM_SHEET_DATA } from '@angular/material/bottom-sheet';
import { FormControl, FormGroup, FormBuilder, Validators } from '@angular/forms';
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

interface IOptionsMap {
  anio: number;
  fecha: Date;
  empresa: number;
  causa: number;
}

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

  constructor(private bottomSheetRef: MatBottomSheetRef<MapOptionsComponent>,
              @Inject(MAT_BOTTOM_SHEET_DATA) public data: any,
              private formBuilder: FormBuilder) {}
  tipeMoment: Moment;
  optionsMap = this.formBuilder.group({
    anio: [null, Validators.required],
    fecha: null,
    empresa: [null, Validators.required],
    causa: [null, Validators.required]
  });

  date =  new FormControl(moment());
  startDate: Date;
  mesActual = new Date().getMonth();
  suiAnios: any[] = this.data.suiAnios;

  errorMessage = '';
  selectAnio = 2018; // Valor que actualiza el select

  ngOnInit(): void {
    console.log(this.optionsMap.value);
  }

  captureData() {
    // this.optionsMap.get('fecha').setValue(moment(this.optionsMap.get('date')).format('M'));
    console.log('Opciones Modal', this.optionsMap.value);
  }

  somethingChanged(select: any): void {
    console.log('anio', select);
    this.startDate = new Date(select, this.mesActual, 1);
  }

  chosenYearHandler(normalizedYear: Moment) {
    // const ctrlValue = this.optionsMap.get('fecha').value;
    // ctrlValue.year(normalizedYear.year());
    // this.optionsMap.get('fecha').setValue(ctrlValue);
  }

  chosenMonthHandler(normalizedMonth: Moment, datepicker: MatDatepicker<Moment>) {
    console.log('event', normalizedMonth, 'dp', datepicker);
    const ctrlValue = this.date.value;
    ctrlValue.month(normalizedMonth.month());
    this.optionsMap.get('fecha').setValue(ctrlValue);
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
