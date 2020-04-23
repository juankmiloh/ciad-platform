import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { setDefaultOptions, loadModules, loadCss } from 'esri-loader';
import { MatBottomSheet } from '@angular/material/bottom-sheet';
import { MatFabMenu } from '@angular-material-extensions/fab-menu';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { ThemePalette } from '@angular/material/core';
import { MapOptionsComponent } from './map-options/map-options.component';
import { SuiService } from 'src/app/services/sui.service';
import { IOptionsMapa } from 'src/app/models/IOptionsMapa.model';
import * as d3 from 'd3';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { MapStatisticsComponent } from './map-statistics/map-statistics.component';

@Component({
  selector: 'app-map-interrupcion',
  templateUrl: './map-interrupcion.component.html',
  styleUrls: ['./map-interrupcion.component.scss']
})
export class MapInterrupcionComponent implements OnInit {

  constructor(private bottomSheet: MatBottomSheet,
              private suiService: SuiService,
              private snackBar: MatSnackBar,
              public dialog: MatDialog) {}

  // The <div> where we will place the map
  @ViewChild('mapViewNode', { static: true }) private mapViewEl: ElementRef;
  public view: any;

  public suiAnios: any[] = [];
  public suiCausas: any[] = [];
  public suiEmpresas: any[] = [];
  errorMessage = '';

  // opciones del progress de carga
  mode: ProgressSpinnerMode = 'determinate';
  value = 50;

  // Controla el CSS del Backdrop
  fbbackMap = 'fbback_map_hide';
  fbbackMapLoad = 'fbback_map_show_load';

  // Opciones del boton flotante
  isActive = false;
  color: ThemePalette = 'primary';
  btnFlotante = 'hideBtnFlotante';
  fabOptions: MatFabMenu[] = [
    {
      id: 1,
      icon: 'settings',
      tooltip: 'Configuración',
      tooltipPosition: 'before'
    },
    {
      id: 2,
      icon: 'assessment',
      tooltip: 'Estadísticas',
      tooltipPosition: 'before'
    },
    {
      id: 3,
      imgUrl: 'assets/img/brightness_3-white-18dp.svg',
      tooltip: 'Modo Oscuro',
      tooltipPosition: 'before',
      color: 'warn'
    },
  ];

  // Permite controlar el backdrop cuando se cambia el CSV
  updateLayerCSV = true;

  bottomSheetRef: any;

  options: IOptionsMapa;

  nombreEmpresa: string;

  meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

  dataCSV: any;
  resultModal: any;

  async ngOnInit() {
    // Initialize MapView and return an instance of MapView
    const fecha = new Date();
    const anoActual = fecha.getFullYear();
    const mesActual = fecha.getMonth() - 1;
    this.options = {
      ano: anoActual,
      mes: mesActual,
      empresa: 0,
      nombEmpresa: 'Todas las empresas',
      causa: 0,
      colSui: 'TODAS',
      nombCausa: 'programadas no excluibles',
      zoom: 4,
      latitud: 2.5,
      longitud: -73.47106040285713
    };
    await this.initializeMap(this.options).then(mapView => {});
    this.loadSuiAnios();
    this.loadSuiCausas();
    this.loadSuiEmpresas();
    // this.bottomSheet.open(MapOptionsComponent, {
    //   // Se pasan valores al modal de filtros
    //   data: { view: this.view, fabOptions: this.fabOptions },
    // });
    // this.openDialog();
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(MapStatisticsComponent, {
      height: '33em',
      width: '100%',
      data:
        {
          view: this.view,
          fabOptions: this.fabOptions,
          optionsMap: this.options,
          suiAnios: this.suiAnios,
          suiCausas: this.suiCausas,
          suiEmpresas: this.suiEmpresas,
          updateLayerCSV: this.updateLayerCSV,
          dataCSV: this.dataCSV,
          result: this.resultModal
        },
    });
    dialogRef.afterClosed().subscribe((dataFromModal: any) => {
      console.log('The dialog was closed', dataFromModal);
      this.updateLayerCSV = true;
      if (dataFromModal !== undefined) {
        this.addLayerMap(dataFromModal).then((data) => {
          this.view.map.layers = data; // Se agrega un nuevo layer CSV al mapa
        });
      }
    });
  }

  ngOnDestroy() {
    try {
      this.bottomSheetRef.dismiss(); // Se cierra el modal
    } catch (error) {
    }
    if (this.view) {
      this.view.container = null; // destroy the map view
    }
  }

  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, {
      duration: 2000,
    });
  }

  // click boton flotante
  clickBtnFlotante(): void {
    if (this.isActive) {
      this.hideBackdrop();
    } else {
      this.showBackdrop('fbback_map_hide');
      this.btnFlotante = 'showBtnFlotante';
      this.isActive = true; // Se cambia la propiedad del btn flotante
    }
  }

  // Mostrar Backdrop
  showBackdrop(cssLoad: string): void {
    // console.log('showBackdrop');
    this.fbbackMap = 'fbback_map_init';
    this.fbbackMapLoad = cssLoad;
    this.view.popup.close(); // Se cierran los popups del mapa
  }

  // Ocultar Backdrop
  hideBackdrop(): void {
    // console.log('hideBackdrop');
    if (this.isActive) { // Si el btn flotante esta activo
      this.fbbackMap = 'fbback_map_hide';
      this.isActive = false; // Se cambia la propiedad del btn flotante
    }
  }

  // Captura la opcion seleccionada del boton flotante
  selectedAction = (event: number) => {
    this.fbbackMap = 'fbback_map_hide';
    // Click opcion filtros
    if (event === 1) {
      this.openBottomSheet();
    }
    // Click opcion estadisticas
    if (event === 2) {
      this.openDialog();
    }
    // Click opcion Basemap
    if (event === 3) {
      // console.log('BaseMap', this.fabOptions);
      const basemap = this.view.map.basemap.id;
      if (basemap === 'streets-night-vector') {
        this.view.map.basemap = 'streets-navigation-vector'; // Cambiar el baseMap a Claro
        this.changeOptionBtnToDark();
      } else {
        this.view.map.basemap = 'streets-night-vector'; // Cambiar el baseMap a Oscuro
        this.changeOptionBtnToLight();
      }
    }
  }

  // Cambiar apariencia del boton de opciones de Basemap a Oscuro
  changeOptionBtnToDark(): void {
    this.fabOptions[2].icon = '';
    this.fabOptions[2].imgUrl = 'assets/img/brightness_3-white-18dp.svg';
    this.fabOptions[2].tooltip = 'Modo Oscuro';
    this.fabOptions[2].color = 'warn';
  }

  // Cambiar apariencia del boton de opciones de Basemap a Claro
  changeOptionBtnToLight(): void {
    this.fabOptions[2].icon = 'wb_sunny';
    this.fabOptions[2].imgUrl = '';
    this.fabOptions[2].tooltip = 'Modo Claro';
    delete this.fabOptions[2].color; // Se elimina la propiedad 'color' del objeto con id 3 para dejarlo claro
  }

  // Mostrar modal de filtros
  openBottomSheet(): void {
    this.bottomSheetRef = this.bottomSheet.open(MapOptionsComponent, {
      // Se pasan valores al modal de filtros
      data:
        {
          view: this.view,
          fabOptions: this.fabOptions,
          optionsMap: this.options,
          suiAnios: this.suiAnios,
          suiCausas: this.suiCausas,
          suiEmpresas: this.suiEmpresas,
          updateLayerCSV: this.updateLayerCSV
        },
    });

    // subscribe to observable que se ejecuta una vez se abre el modal
    this.bottomSheetRef.afterOpened().subscribe(() => {
      this.updateLayerCSV = true;
    });

    // subscribe to observable que se ejecuta despues de cerrar el modal, obtiene los valores del hijo
    this.bottomSheetRef.afterDismissed().subscribe(async (dataFromChild) => {
      console.log('valores enviados del hijo', dataFromChild);
      this.updateLayerCSV = true;
      if (dataFromChild !== undefined) {
        this.addLayerMap(dataFromChild).then((data) => {
          this.view.map.layers = data; // Se agrega un nuevo layer CSV al mapa
        });
      }
    });

    // subscribe to observable que se ejecuta cuando se da click al backdrop del modal
    this.bottomSheetRef.backdropClick().subscribe((evt) => {
      this.updateLayerCSV = false;
    });
  }

  // Se carga el mapa
  async initializeMap(options: IOptionsMapa) {
    setDefaultOptions({ version: '4.12' }); // Se configura la version del API de ARCgis a utilizar
    loadCss('4.15'); // Se cargan los estilos de la version a utilizar

    sessionStorage.setItem('addLayerMapLayer', 'true');

    try {
      // Load the modules for the ArcGIS API for JavaScript
      // tslint:disable-next-line: max-line-length
      const [Track, Map, MapView, Search, Legend, BasemapToggle, watchUtils, FeatureLayer] = await loadModules(['esri/widgets/Track', 'esri/Map', 'esri/views/MapView', 'esri/widgets/Search', 'esri/widgets/Legend', 'esri/widgets/BasemapToggle', 'esri/core/watchUtils', 'esri/layers/FeatureLayer']);

      // Configure the Map
      const mapProperties = {
        basemap: 'streets-navigation-vector'
      };

      const map = new Map(mapProperties);

      // Initialize the MapView
      const mapViewProperties = {
        container: this.mapViewEl.nativeElement,
        center: [options.longitud, options.latitud], // [horizontal (long), vertical (lat)]
        zoom: options.zoom,
        constraints: {
          minZoom: 3,
          maxZoom: 19,
          snapToZoom: true
         },
        map
      };

      this.view = new MapView(mapViewProperties);

      // Mostrar backDrop de carga mientras se inicia la vista
      watchUtils.whenOnce(this.view, 'ready').then(() => {
        this.showBackdrop('fbback_map_show_load');
        this.btnFlotante = 'hideBtnFlotante';
      });

      // Display the loading indicator when the view is updating
      watchUtils.whenTrue(this.view, 'updating', (evt: any) => {
        // console.log('showLoad', evt);
        watchUtils.whenTrue(this.view, 'stationary', () => {
          // Get the new extent of view/map whenever map is updated.
          if (this.view.extent) {
            if (this.updateLayerCSV) {
              this.showBackdrop('fbback_map_show_load');
              this.btnFlotante = 'hideBtnFlotante';
            }
          }
        });
      });

      // Hide the loading indicator when the view stops updating
      watchUtils.whenFalse(this.view, 'updating', (evt: any) => {
        // console.log('closeLoad', evt);
        if (this.updateLayerCSV) {
          this.openSnackBar('Datos actualizados correctamente.', null);
          this.snackBar._openedSnackBarRef.afterOpened().subscribe(async (data) => {
            this.updateLayerCSV = false;
          });
        }
        this.fbbackMap = 'fbback_map_hide';
        this.btnFlotante = 'showBtnFlotante';
        watchUtils.whenTrue(this.view.popup, 'visible', (evt1: any) => {
          // console.log('show POPUP!', evt1);
          this.btnFlotante = 'hideBtnFlotante';
        });
      });

      const legend = new Legend({ view: this.view });
      const search = new Search({ view: this.view });
      const basemapToggle = new BasemapToggle({ view: this.view });
      const track = new Track({ view: this.view });

      legend.style = { type: 'card', layout: 'side-by-side' }; // CSS leyenda tipo card

      this.view.ui.add(legend, { position: 'bottom-left' });  // Muestra las convenciones del mapa
      this.view.ui.add(search, { position: 'top-right' });    // Muestra el input de busqueda
      this.view.ui.remove([basemapToggle, 'zoom']);           // Elimina los botones de zoom
      this.view.ui.add(track, 'top-right');                   // Muestra el boton de MyLocation

      this.view.map.layers = await this.addLayerMap(options); // Se agrega un nuevo layer CSV al mapa

      return this.view;

    } catch (error) {
      console.log('EsriLoader: ', error);
    }
  }

  async addLayerMap(options: IOptionsMapa) {
    this.updateLayerCSV = true;
    try {
      const [CSVLayer] = await loadModules(['esri/layers/CSVLayer']);
      // const url = 'assets/file_interrupciones.csv';
      // const url = 'http://192.168.1.60:5055/i_interrupcion/2016/7/604/32'; <-- NO DEVUELVE RESULTADOS VALIDAR CON UN ALERT
      const url = `http://192.168.1.60:5055/i_interrupcion/${options.ano}/${options.mes}/${options.empresa}/${options.causa}`;

      this.dataCSV = d3.csv(url);

      // Paste the url into a browser's address bar to download and view the attributes
      // in the CSV file. These attributes include:
      // * centro_poblado - nombre municipio
      // * longitude - longitud municipio
      // * latitude - latitud municipio
      // * cod_dane - codigo dane municipio
      // * cod_empresa - empresa del municipio
      // * total - total de horas de interrupciones

      const template = {
        // tslint:disable-next-line: max-line-length
        title:  '<div style="border: 0px solid black; background: #e3f2fd; width: 15em; border-radius: 5px; height: 4em; padding-top: 0.3em;">' +
                '  <small style="color: #3f51b5;"><b>{centro_poblado}</b></small><br>' +
                '  <small style="color: #212121; padding-left: 3%;">Horas de interrupción {total}</small>' +
                '</div>',
        content: '<div>' +
                 ' <small>Código DANE municipio {cod_dane}</small><br>' +
                 ` <small><u>{nom_empresa}</u> código {cod_empresa}</small><br>` +
                 ` <small>Interrupciones <u>${options.nombCausa.toUpperCase()}</u> para <u>${this.meses[options.mes].toUpperCase()}</u> de <u>${options.ano}</u></small>` +
                 '</div>',
      };

      // The heatmap renderer assigns each pixel in the view with
      // an intensity value. The ratio of that intensity value
      // to the maxPixel intensity is used to assign a color
      // from the continuous color ramp in the colorStops property
      const renderer = {
        type: 'heatmap',
        field: 'total',
        colorStops: [
          { color: 'rgba(63, 40, 102, 0)', ratio: 0 }, // rango de 0 a 1
          { color: '#6300df', ratio: 0.083 },          // Azul claro
          { color: '#2196f3', ratio: 0.100 },          // Azul
          { color: '#00ff2c', ratio: 0.166 },          // Verde Clarito
          { color: '#a1ff00', ratio: 0.249 },          // Verde
          { color: '#e5ff00', ratio: 0.332 },          // Amarillo claro
          { color: '#ffeb3b', ratio: 0.415 },          // Amarillo
          { color: '#ffc700', ratio: 0.498 },          // Amarillo oscuro
          { color: '#fea701', ratio: 0.581 },          // Naranja claro
          { color: '#ff9800', ratio: 0.664 },          // Naranja
          { color: '#f44336', ratio: 1 }               // Rojo
        ],
        minPixelIntensity: 0,
        maxPixelIntensity: 50000
      };

      const layer = new CSVLayer({
        url,
        title: `Interrupciones ${options.colSui} ${this.meses[options.mes]} de ${options.ano}`,
        copyright: 'DESARROLLADO POR JUAN CAMILO HERRERA - CIAD SUPERSERVICIOS',
        popupTemplate: template,
        renderer
      });

      // this.view.map.layers = layer; // Se agrega un nuevo layer CSV al mapa
      this.options = options;
      return layer;
    } catch (error) {
      console.log('EsriLoader: ', error);
    }
  }

  async loadSuiAnios() {
    this.suiService.getAnios().subscribe( anios => {
      this.suiAnios = anios;
      console.log(this.suiAnios);
      }, error => this.errorMessage = error
    );
  }

  loadSuiCausas() {
    this.suiService.getCausas().subscribe( causas => {
      this.suiCausas = causas;
      console.log(this.suiCausas);
      }, error => this.errorMessage = error
    );
  }

  loadSuiEmpresas() {
    this.suiService.getEmpresas().subscribe( empresas => {
      this.suiEmpresas = empresas;
      console.log(this.suiEmpresas);
      }, error => this.errorMessage = error
    );
  }

  async loadSuiEmpresa(idEmpresa: number) {
    const empresa = await this.suiService.getEmpresasId(idEmpresa);
    console.log('EMPRESA CONSULTADA: ', empresa);
    return empresa;
  }

}
