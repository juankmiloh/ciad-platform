import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
  selector: 'app-sidenav-menu',
  templateUrl: './sidenav-menu.component.html',
  styleUrls: ['./sidenav-menu.component.scss'],
})
export class SidenavMenuComponent {

  constructor() {}

  @ViewChild('sidenav') sidenav: MatSidenav;

  opcion = 'CIAD | Superservicios';

  close(reason: string) {
    if (reason !== 'na') {
      this.opcion = reason;
      this.sidenav.close();
    } else {
      this.sidenav.close();
    }
  }

}
