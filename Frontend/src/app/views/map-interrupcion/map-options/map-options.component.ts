import { Component, Inject, ViewChild, ElementRef } from '@angular/core';
import { loadModules } from 'esri-loader';
import { MatBottomSheetRef } from '@angular/material/bottom-sheet';
import { MAT_BOTTOM_SHEET_DATA } from '@angular/material/bottom-sheet';
import { FormControl, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MomentDateAdapter, MAT_MOMENT_DATE_ADAPTER_OPTIONS } from '@angular/material-moment-adapter';
import { DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';
import { MatDatepicker } from '@angular/material/datepicker';

import * as moment from 'moment';
import { Moment } from 'moment';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { IOptionsMapa } from 'src/app/models/IOptionsMapa.model';

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

export interface Empresa {
  cod_empresa: number;
  nombre: string;
  servicio: string;
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

  stateCtrl = new FormControl();
  optionsMap = this.formBuilder.group({
    anio: [null, Validators.required],
    mes: null,
    empresa: [null, Validators.required],
    causa: [null, Validators.required]
  });

  filteredEmpresas: Observable<Empresa[]>;

  constructor(private bottomSheetRef: MatBottomSheetRef<MapOptionsComponent>,
              @Inject(MAT_BOTTOM_SHEET_DATA) public data: any,
              private formBuilder: FormBuilder) {
                this.filteredEmpresas = this.optionsMap.get('empresa').valueChanges
                  .pipe(
                    startWith(''),
                    map(state => state ? this._filterStates(state) : this.suiEmpresas.slice())
                  );
              }

  tipeMoment: Moment;
  date = new FormControl(moment());
  sendDate: Date;
  startDate: Date;
  suiAnios: any[] = this.data.suiAnios;
  suiCausas: any[] = this.data.suiCausas;
  suiEmpresas: Empresa[] = this.data.suiEmpresas;

  errorMessage = '';
  selectAnio: number;
  selectMes: number;
  selectEmpresa: string;
  selectCausa: number;

  sendData: IOptionsMapa;

  ngOnInit(): void {
    this.suiEmpresas.unshift({
      cod_empresa: 0,
      nombre: 'TODAS',
      servicio: 'ENERGIA'
    });
    this.suiCausas.unshift({
      cod_causa: 0,
      col_sui: 'Todas',
      descripcion: 'TODAS'
    });
    console.log(this.data.optionsMap);
    this.selectAnio = this.data.optionsMap.ano;
    this.selectMes = this.data.optionsMap.mes - 1;
    const ctrlDate = this.date.value;
    ctrlDate.month(this.selectMes);
    this.optionsMap.get('mes').setValue(ctrlDate);
    this.startDate = new Date(this.selectAnio, this.selectMes, 1); // Actualizar año y mes seleccionado en el modal de meses
    this.selectEmpresa = this.suiEmpresas.find(empresa => empresa.cod_empresa === this.data.optionsMap.empresa).nombre;
    this.selectCausa = this.data.optionsMap.causa;
    // subscribe to observable que se ejecuta cuando se da click al backdrop del modal
    this.bottomSheetRef.backdropClick().subscribe((evt) => {
      this.suiEmpresas.splice(0, 1); // Se eliminan los valores adicionados al arreglo (TODAS)
      this.suiCausas.splice(0, 1);   // Se eliminan los valores adicionados al arreglo (TODAS)
    });
  }

  private _filterStates(value: string): Empresa[] {
    const filterValue = value.toLowerCase();
    return this.suiEmpresas.filter(state => state.nombre.toLowerCase().indexOf(filterValue) === 0);
  }

  sendDataParent() {
    const empresaNombre = this.optionsMap.get('empresa').value;
    const codEmpresa = this.suiEmpresas.find(empresa => empresa.nombre === empresaNombre).cod_empresa;
    const causaNombre = this.suiCausas.find(causa => causa.cod_causa === this.optionsMap.get('causa').value).descripcion;
    this.optionsMap.get('empresa').setValue(codEmpresa);
    this.optionsMap.get('mes').setValue(moment(this.optionsMap.get('mes').value).format('M'));
    this.sendData = {
      ano: this.optionsMap.get('anio').value,
      mes: this.optionsMap.get('mes').value,
      empresa: this.optionsMap.get('empresa').value,
      nombEmpresa: empresaNombre,
      causa: this.optionsMap.get('causa').value,
      nombCausa: causaNombre,
      zoom: this.data.view.zoom,
      latitud: this.data.view.center.latitude,
      longitud: this.data.view.center.longitude
    };
    this.bottomSheetRef.dismiss(this.sendData); // cerrar modal y pasar datos a la vista padre
    // subscribe to observable que se ejecuta despues de cerrar el modal
    this.bottomSheetRef.afterDismissed().subscribe(async () => {
      this.suiEmpresas.splice(0, 1); // Se eliminan los valores adicionados al arreglo (TODAS)
      this.suiCausas.splice(0, 1);   // Se eliminan los valores adicionados al arreglo (TODAS)
    });
  }

  somethingChanged(select: any): void {
    const mesActual = this.optionsMap.get('mes').value.format('M') - 1;
    this.startDate = new Date(select, mesActual, 1); // Actualizar año y mes seleccionado en el modal de meses
  }

  chosenYearHandler(normalizedYear: Moment) {
    // const ctrlValue = this.optionsMap.get('mes').value;
    // ctrlValue.year(normalizedYear.year());
    // this.optionsMap.get('mes').setValue(ctrlValue);
  }

  chosenMonthHandler(normalizedMonth: Moment, datepicker: MatDatepicker<Moment>) {
    console.log('event', normalizedMonth, 'dp', datepicker);
    const ctrlValue = this.date.value;
    ctrlValue.month(normalizedMonth.month());
    console.log('ctrlValue', ctrlValue);
    this.optionsMap.get('mes').setValue(ctrlValue);
    this.startDate = new Date(this.selectAnio, ctrlValue.format('M') - 1, 1); // Actualizar año y mes seleccionado en el modal de meses
    datepicker.close();
  }

  // Cambiar apariencia del boton de opciones de Basemap a Claro
  changeOptionBtnToLight(): void {
    this.data.fabOptions[2].icon = 'wb_sunny';
    this.data.fabOptions[2].imgUrl = '';
    this.data.fabOptions[2].tooltip = 'Modo Claro';
    delete this.data.fabOptions[2].color; // Se elimina la propiedad 'color' del objeto con id 3 para dejarlo claro
  }
}
