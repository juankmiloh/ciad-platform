import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AppObservableService {

  private showAlertErrorSUI = new Subject<any>();

  constructor() {}

  setShowAlertErrorSUI(status: number) {
    this.showAlertErrorSUI.next(status);
  }

  getShowAlertErrorSUI(): Observable<any>  {
    return this.showAlertErrorSUI.asObservable();
  }
}
