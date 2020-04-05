import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './views/home/home.component';
import { MapPqrsComponent } from './views/map-pqrs/map-pqrs.component';
import { MapInterrupcionComponent } from './views/map-interrupcion/map-interrupcion.component';
import { TarifaritoComponent } from './views/tarifarito/tarifarito.component';
import { ProcesosDiegComponent } from './views/procesos-dieg/procesos-dieg.component';


const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'map-pqrs', component: MapPqrsComponent },
  { path: 'map-page', component: MapInterrupcionComponent },
  { path: 'tarifarito', component: TarifaritoComponent },
  { path: 'procesos-dieg', component: ProcesosDiegComponent },
  { path: '',   redirectTo: '/home', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
