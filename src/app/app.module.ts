import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { FormsModule } from '@angular/forms';
import { HammerModule } from '@angular/platform-browser';
import {
  IgxButtonModule, IgxCardModule, IgxCarouselModule,
  IgxIconModule, IgxInputGroupModule, IgxLayoutModule,
  IgxNavbarModule, IgxNavigationDrawerModule, IgxRippleModule, IgxSelectModule
} from 'igniteui-angular';

import { SidenavMenuComponent } from './views/sidenav-menu/sidenav-menu.component';
import { HomeComponent } from './views/home/home.component';
import { MapInterrupcionComponent } from './views/map-interrupcion/map-interrupcion.component';
import { MapOptionsComponent } from './views/map-interrupcion/map-options/map-options.component';
import { MapPqrsComponent } from './views/map-pqrs/map-pqrs.component';
import { TarifaritoComponent } from './views/tarifarito/tarifarito.component';
import { ProcesosDiegComponent } from './views/procesos-dieg/procesos-dieg.component';

@NgModule({
  declarations: [
    AppComponent,
    SidenavMenuComponent,
    HomeComponent,
    MapInterrupcionComponent,
    MapOptionsComponent,
    MapPqrsComponent,
    TarifaritoComponent,
    ProcesosDiegComponent
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
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
