import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { setDefaultOptions, loadModules, loadCss } from 'esri-loader';
import { MatBottomSheet } from '@angular/material/bottom-sheet';
import { MatFabMenu } from '@angular-material-extensions/fab-menu';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { ThemePalette } from '@angular/material/core';
import { MapOptionsComponent } from './map-options/map-options.component';
import { SuiService } from 'src/app/services/sui.service';

@Component({
  selector: 'app-map-interrupcion',
  templateUrl: './map-interrupcion.component.html',
  styleUrls: ['./map-interrupcion.component.scss']
})
export class MapInterrupcionComponent implements OnInit {

  constructor(private bottomSheet: MatBottomSheet, private suiService: SuiService) {}

  // The <div> where we will place the map
  @ViewChild('mapViewNode', { static: true }) private mapViewEl: ElementRef;
  public view: any;

  public suiAnios: any[] = [];
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

  async ngOnInit() {
    // Initialize MapView and return an instance of MapView
    await this.initializeMap().then(mapView => {});
    this.loadSuiAnios();
    // this.bottomSheet.open(MapOptionsComponent, {
    //   // Se pasan valores al modal de filtros
    //   data: { view: this.view, fabOptions: this.fabOptions },
    // });
  }

  ngOnDestroy() {
    if (this.view) {
      this.view.container = null; // destroy the map view
    }
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
      console.log('Estadisticas!');
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
    const bottomSheetRef = this.bottomSheet.open(MapOptionsComponent, {
      // Se pasan valores al modal de filtros
      data:
        {
          view: this.view,
          fabOptions: this.fabOptions,
          suiAnios: this.suiAnios,
          updateLayerCSV: this.updateLayerCSV
        },
    });

    // subscribe to observable que se ejecuta una vez se abre el modal
    bottomSheetRef.afterOpened().subscribe(() => {
      this.updateLayerCSV = true;
    });

    // subscribe to observable que se ejecuta despues de cerrar el modal, obtiene los valores del hijo
    bottomSheetRef.afterDismissed().subscribe((dataFromChild) => {
      // console.log('valores enviados del hijo', dataFromChild);
    });

    // subscribe to observable que se ejecuta cuando se da click al backdrop del modal
    bottomSheetRef.backdropClick().subscribe((evt) => {
      this.updateLayerCSV = false;
    });
  }

  // Se carga el mapa
  async initializeMap() {
    setDefaultOptions({ version: '4.12' }); // Se configura la version del API de ARCgis a utilizar
    loadCss('4.14'); // Se cargan los estilos de la version a utilizar

    sessionStorage.setItem('updateMapLayer', 'true');

    try {
      // Load the modules for the ArcGIS API for JavaScript
      // tslint:disable-next-line: max-line-length
      const [Track, Map, MapView, CSVLayer, Search, Legend, BasemapToggle, watchUtils] = await loadModules(['esri/widgets/Track', 'esri/Map', 'esri/views/MapView', 'esri/layers/CSVLayer', 'esri/widgets/Search', 'esri/widgets/Legend', 'esri/widgets/BasemapToggle', 'esri/core/watchUtils']);

      // const url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.csv';
      // const url = '';
      const url = 'assets/2.5_week.csv';

      // Paste the url into a browser's address bar to download and view the attributes
      // in the CSV file. These attributes include:
      // * mag - magnitude
      // * type - earthquake or other event such as nuclear test
      // * place - location of the event
      // * time - the time of the event

      const template = {
        title: '{place}',
        content: 'Magnitude {mag} {type} hit {place} on {time}.'
      };

      // The heatmap renderer assigns each pixel in the view with
      // an intensity value. The ratio of that intensity value
      // to the maxPixel intensity is used to assign a color
      // from the continuous color ramp in the colorStops property

      const renderer = {
        type: 'heatmap',
        colorStops: [
          { color: 'rgba(63, 40, 102, 0)', ratio: 0 },
          { color: '#472b77', ratio: 0.083 },
          { color: '#4e2d87', ratio: 0.166 },
          { color: '#563098', ratio: 0.249 },
          { color: '#5d32a8', ratio: 0.332 },
          { color: '#6735be', ratio: 0.415 },
          { color: '#7139d4', ratio: 0.498 },
          { color: '#7b3ce9', ratio: 0.581 },
          { color: '#853fff', ratio: 0.664 },
          { color: '#a46fbf', ratio: 0.747 },
          { color: '#c29f80', ratio: 0.83 },
          { color: '#e0cf40', ratio: 0.913 },
          { color: '#ffff00', ratio: 1 }
        ],
        maxPixelIntensity: 25,
        minPixelIntensity: 0
      };

      const layer = new CSVLayer({
        url,
        title: 'Interrupciones',
        copyright: 'DESARROLLADO POR JUAN CAMILO HERRERA - CIAD SUPERSERVICIOS',
        popupTemplate: template,
        renderer
      });

      // Configure the Map
      const mapProperties = {
        basemap: 'streets-navigation-vector',
        layers: [layer]
      };

      const map = new Map(mapProperties);

      // Initialize the MapView
      const mapViewProperties = {
        container: this.mapViewEl.nativeElement,
        center: [-73.47106040285713, 2.5], // [horizontal (long), vertical (lat)]
        zoom: 4,
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
        if (this.updateLayerCSV) {
          this.showBackdrop('fbback_map_show_load');
          this.btnFlotante = 'hideBtnFlotante';
        }
      });

      // Hide the loading indicator when the view stops updating
      watchUtils.whenFalse(this.view, 'updating', (evt: any) => {
        // console.log('closeLoad', evt);
        this.updateLayerCSV = false;
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

      return this.view;

    } catch (error) {
      console.log('EsriLoader: ', error);
    }
  }

  loadSuiAnios() {
    this.suiService.getAnios().subscribe( anios => {
      this.suiAnios = anios;
      console.log(this.suiAnios);
      }, error => this.errorMessage = error
    );
  }

}
