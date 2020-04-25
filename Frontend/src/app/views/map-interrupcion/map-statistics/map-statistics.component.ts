import { Component, OnInit, Inject, ViewChild } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from 'src/app/models/IOptionsMapa.model';
import { IgxExcelExporterService, IgxExcelExporterOptions } from 'igniteui-angular';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { IOptionsMapa } from '../../../models/IOptionsMapa.model';

@Component({
  selector: 'app-map-statistics',
  templateUrl: './map-statistics.component.html',
  styleUrls: ['./map-statistics.component.scss'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})

export class MapStatisticsComponent implements OnInit {

  ELEMENT_DATA: IOptionsMapa[];
  dataSource: any;
  columnsToDisplay: string[];
  causa: string;
  fecha: any;
  meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
  resultsLength = 0;
  isLoadingResults = true;
  isRateLimitReached = false;
  date = new Date();
  hoy: any;

  @ViewChild(MatSort, {static: true}) sort: MatSort;

  constructor(public dialogRef: MatDialogRef<MapStatisticsComponent>,
              @Inject(MAT_DIALOG_DATA) public data: DialogData,
              private excelExportService: IgxExcelExporterService) {}

  onNoClick(): void {
    this.dialogRef.close();
  }

  ngOnInit() {
    this.hoy = `${this.date.getDate()}${this.date.getMonth() + 1}${this.date.getFullYear()}${this.date.getHours()}${this.date.getMinutes()}${this.date.getSeconds()}`;
    console.log('valores modal', this.data);
    this.causa = this.data.optionsMap.colSui.toUpperCase();
    this.fecha = `${this.meses[this.data.optionsMap.mes]}/${this.data.optionsMap.ano}`;
    this.dialogRef.afterOpened().subscribe((data) => {
      this.loadData();
    });
  }

  loadData() {
    this.data.dataCSV.then((data: any) => {
      this.ELEMENT_DATA = data;
      this.dataSource = new MatTableDataSource(this.ELEMENT_DATA);
      if (this.data.optionsMap.empresa === 0) {
        this.columnsToDisplay = ['nom_empresa', 'centro_poblado', 'causa', 'total', 'link'];
      } else {
        this.columnsToDisplay = ['nom_empresa', 'centro_poblado', 'causa', 'total'];
      }
      this.dataSource.sort = this.sort;
      this.isLoadingResults = false;
    }, (error: any) => {
      this.isRateLimitReached = true;
    });
  }

  updateMap(options: any) {
    const sendData = {
      ano: this.data.optionsMap.ano,
      mes: this.data.optionsMap.mes,
      empresa: parseInt(options.cod_empresa),
      nombEmpresa: options.nom_empresa,
      causa: this.data.optionsMap.causa,
      colSui: this.data.optionsMap.colSui,
      nombCausa: this.data.optionsMap.nombCausa,
      zoom: this.data.view.zoom,
      latitud: this.data.view.center.latitude,
      longitud: this.data.view.center.longitude,
    };
    this.dialogRef.close(sendData);
  }

  public exportButtonHandler() {
    // tslint:disable-next-line: max-line-length
    this.excelExportService.exportData(this.dataSource.filteredData, new IgxExcelExporterOptions(`Interupciones_${this.data.optionsMap.colSui}_${this.data.optionsMap.mes}${this.data.optionsMap.ano}_${this.hoy}`));
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

}
