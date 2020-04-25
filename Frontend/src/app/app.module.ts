import { BrowserModule } from '@angular/platform-browser';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { FormsModule, ReactiveFormsModule  } from '@angular/forms';
import { HammerModule } from '@angular/platform-browser';
import {
  IgxButtonModule, IgxCardModule, IgxCarouselModule,
  IgxIconModule, IgxInputGroupModule, IgxLayoutModule,
  IgxNavbarModule, IgxNavigationDrawerModule, IgxRippleModule, IgxSelectModule,
} from 'igniteui-angular';
import { MatBottomSheetModule, MAT_BOTTOM_SHEET_DEFAULT_OPTIONS } from '@angular/material/bottom-sheet';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import {MatDatepickerModule} from '@angular/material/datepicker';
import { MatFabMenuModule } from '@angular-material-extensions/fab-menu';
import { HttpClientModule } from '@angular/common/http';
import { MatSelectModule } from '@angular/material/select';
import { MatDividerModule } from '@angular/material/divider';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatFormFieldModule, MAT_FORM_FIELD_DEFAULT_OPTIONS } from '@angular/material/form-field';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatInputModule } from '@angular/material/input';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatCardModule } from '@angular/material/card';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialogModule, MAT_DIALOG_DEFAULT_OPTIONS } from '@angular/material/dialog';
import { IgxExcelExporterService } from 'igniteui-angular';
import { MatTabsModule } from '@angular/material/tabs';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatTooltipModule } from '@angular/material/tooltip';


import { SidenavMenuComponent } from './views/sidenav-menu/sidenav-menu.component';
import { HomeComponent } from './views/home/home.component';
import { MapInterrupcionComponent } from './views/map-interrupcion/map-interrupcion.component';
import { MapOptionsComponent } from './views/map-interrupcion/map-options/map-options.component';
import { MapPqrsComponent } from './views/map-pqrs/map-pqrs.component';
import { TarifaritoComponent } from './views/tarifarito/tarifarito.component';
import { ProcesosDiegComponent } from './views/procesos-dieg/procesos-dieg.component';
import { MapStatisticsComponent } from './views/map-interrupcion/map-statistics/map-statistics.component';

@NgModule({
  declarations: [
    AppComponent,
    SidenavMenuComponent,
    HomeComponent,
    MapInterrupcionComponent,
    MapOptionsComponent,
    MapPqrsComponent,
    TarifaritoComponent,
    ProcesosDiegComponent,
    MapStatisticsComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    LayoutModule,
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    FormsModule,
    ReactiveFormsModule,
    HammerModule,
    IgxButtonModule,
    IgxCardModule,
    IgxCarouselModule,
    IgxIconModule,
    IgxInputGroupModule,
    IgxLayoutModule,
    IgxNavbarModule,
    IgxNavigationDrawerModule,
    IgxRippleModule,
    IgxSelectModule,
    MatBottomSheetModule,
    MatProgressSpinnerModule,
    MatDatepickerModule,
    MatFabMenuModule,
    HttpClientModule,
    MatSelectModule,
    MatDividerModule,
    MatGridListModule,
    MatFormFieldModule,
    FlexLayoutModule,
    MatInputModule,
    MatProgressBarModule,
    MatCardModule,
    MatAutocompleteModule,
    MatSlideToggleModule,
    MatSnackBarModule,
    MatDialogModule,
    MatTabsModule,
    MatTableModule,
    MatSortModule,
    MatTooltipModule,
  ],
  providers: [
    { provide: MAT_FORM_FIELD_DEFAULT_OPTIONS, useValue: {appearance: 'outline'} },
    { provide: MAT_BOTTOM_SHEET_DEFAULT_OPTIONS, useValue: {hasBackdrop: true} },
    { provide: MAT_DIALOG_DEFAULT_OPTIONS, useValue: {hasBackdrop: true} },
    IgxExcelExporterService,
  ],
  schemas: [NO_ERRORS_SCHEMA],
  bootstrap: [AppComponent],
})
export class AppModule {
}
