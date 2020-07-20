import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sidenav-menu',
  templateUrl: './sidenav-menu.component.html',
  styleUrls: ['./sidenav-menu.component.scss'],
})
export class SidenavMenuComponent {
  myWindow: Window;

  constructor(private router: Router) {}

  @ViewChild('sidenav') sidenav: MatSidenav;

  opcion = 'SDEGC - CIAD | Superservicios';

  close(reason: string) {
    if (reason !== 'na') {
      if (reason === 'Mapa de PQR´s' || reason === 'Tarifarito | Grupo Tarifario') {
        this.sidenav.close();
        this.router.navigateByUrl('/');
        this.opcion = 'SDEGC - CIAD | Superservicios';
      } else {
        this.opcion = reason;
        this.sidenav.close();
      }
    } else {
      this.sidenav.close();
    }
  }

}
