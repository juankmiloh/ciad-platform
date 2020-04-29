import { Component, OnInit, Inject, ViewChild } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MapStatisticsComponent } from '../map-statistics/map-statistics.component';
import { IgxExcelExporterService, IgxExcelExporterOptions } from 'igniteui-angular';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { ICausas, ICausa, IOptionsMapa } from '../../../models/IOptionsMapa.model';
import { AppPromiseService } from '../../../services/app-promise.service';
// import { single } from '../../../data';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { SwalComponent } from '@sweetalert2/ngx-sweetalert2';

@Component({
  selector: 'app-map-graphics',
  templateUrl: './map-graphics.component.html',
  styleUrls: ['./map-graphics.component.scss'],
  providers: [NgxChartsModule],
})
export class MapGraphicsComponent implements OnInit {

  @ViewChild(MatSort, {static: true}) sort: MatSort;
  @ViewChild('alertSwal', { static: true }) private alertSwal: SwalComponent;

  columnsToDisplay: string[];
  dataSource: any;
  isLoadingResults = true;
  dialogAction = true;
  fecha: any;
  meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

  single: any[];
  // view: any[] = [700, 300];

  // options
  gradient: boolean = false;
  showLegend: boolean = true;
  showLabels: boolean = true;
  isDoughnut: boolean = true;
  legendTitle: any;
  legendPosition: string = 'right';
  hoy: any;
  date = new Date();

  constructor(public dialogRef: MatDialogRef<MapStatisticsComponent>,
              @Inject(MAT_DIALOG_DATA) public data: any,
              private excelExportService: IgxExcelExporterService,
              private appPromiseService: AppPromiseService) {
                // Object.assign(this, { single });
              }

  ngOnInit(): void {
    console.log(this.data);
    this.hoy = `${this.date.getDate()}${this.date.getMonth() + 1}${this.date.getFullYear()}${this.date.getHours()}${this.date.getMinutes()}${this.date.getSeconds()}`;
    this.fecha = `${this.meses[this.data.dataOptionsMap.optionsMap.mes]}/${this.data.dataOptionsMap.optionsMap.ano}`;
    this.dialogRef.afterOpened().subscribe(async (data) => {
      await this.loadData();
    });
  }

  async loadData() {
    await this.appPromiseService.transformData(this.data.dataOptions, this.data.dataOptionsMap.suiCausas).then((data: ICausa[]) => {
      // console.log('RETORNO DE PROMESA: ', data);
      this.dataSource = new MatTableDataSource(data);
      this.columnsToDisplay = ['causa', 'horas_interrupcion'];
      this.dataSource.sort = this.sort;
      this.isLoadingResults = false;
    }, (error) => {
      // console.log('error');
      this.alertSwal.swalOptions = {
        title: 'Info',
        text: 'Se ha perdido la conexión con el servidor',
        icon: 'info',
        confirmButtonText: 'Recargar Página',
        confirmButtonColor: '#ffa726',
        allowOutsideClick: false,
      };

      if (!this.alertSwal.swalVisible) { // si el modal no esta abierto
        this.alertSwal.fire().then((data) => {
          if (data.value) {
            window.location.reload();
          }
        });
      }
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  getTotalInterr() {
    try {
      return this.dataSource.filteredData.map(t => parseFloat(t.horas_interrupcion)).reduce((acc, value) => acc + value, 0);
    } catch (error) {
      // console.log(error);
    }
  }

  public exportButtonHandler() {
    // tslint:disable-next-line: max-line-length
    this.excelExportService.exportData(this.dataSource.filteredData, new IgxExcelExporterOptions(`Interupciones_${this.data.dataOptions.centro_poblado}_${this.data.dataOptionsMap.optionsMap.colSui}_${this.data.dataOptionsMap.optionsMap.mes}${this.data.dataOptionsMap.optionsMap.ano}_${this.hoy}`));
  }

  // se ejecuta cuando se cambia entre tabs
  async clickTab(evt: any) {
    // console.log('TAB SELECTED ', evt);
    if (evt.index === 0) {
      this.dialogAction = true;
    }

    if (evt.index === 1) { // Grafica
      this.dialogAction = false;
      this.legendTitle = parseFloat(this.data.dataOptions.total).toFixed(2);
      await this.appPromiseService.transformDataToGraphic(this.data.dataOptions).then((data: ICausa[]) => {
        // console.log('RETORNO DE PROMESA: ', data);
        this.single = data;
        Object.assign(this, { ...this.single });
      });
    }
  }

  tooltipText(val: any) {
    // console.log('TEXTO LABEL: ', val);
    return 0;
}

  onSelect(data): void {
    // console.log('Item clicked', JSON.parse(JSON.stringify(data)));
  }

  onActivate(data): void {
    // console.log('Activate', JSON.parse(JSON.stringify(data)));
  }

  onDeactivate(data): void {
    // console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  }
}
