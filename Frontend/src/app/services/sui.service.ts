import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap, map} from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class SuiService {

  constructor(public http: HttpClient) { }

  serverUrl = 'http://192.168.1.60:5055';

  getAnios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.serverUrl}/anios`).pipe(
      tap(data => console.log('Carga anios exitosa!')), catchError(this.handleError)
    );
  }

  private handleError(err: HttpErrorResponse) {
    let errorMessage = '';
    if (err.error instanceof ErrorEvent) {
      errorMessage = `An error ocurred ${ err.error.message }`;
    } else {
      errorMessage = `Server returned code: ${err.status}, error message is:
      ${err.message}`;
    }
    console.log(errorMessage);
    return throwError(errorMessage);
  }

}
