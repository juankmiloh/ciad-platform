import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap} from 'rxjs/operators';


@Injectable({
  providedIn: 'root',
})
export class SuiService {

  constructor(public http: HttpClient) { }

  serverUrl = 'http://192.168.1.60:5055';
  // serverUrl = 'http://localhost:5055';

  getAnios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.serverUrl}/i_anios`).pipe(
      tap(data => console.log('Carga anios exitosa!')), catchError(this.handleError),
    );
  }

  getCausas(): Observable<any[]> {
    return this.http.get<any[]>(`${this.serverUrl}/i_causas`).pipe(
      tap(data => console.log('Carga causas exitosa!')), catchError(this.handleError),
    );
  }

  getCausaId(id: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.serverUrl}/i_causas/${id}`).pipe(
      tap(data => console.log(JSON.stringify(data))), catchError(this.handleError),
      );
  }

  getEmpresas(): Observable<any[]> {
    return this.http.get<any[]>(`${this.serverUrl}/i_empresas`).pipe(
      tap(data => console.log('Carga empresas exitosa!')), catchError(this.handleError),
    );
  }

  getEmpresasId(id: number) {
    return new Promise((resolve, reject) => {
      this.http.get<any[]>(`${this.serverUrl}/i_empresas/${id}`).toPromise().then(res => {
        resolve(res);
      }, () => {
        catchError(this.handleError);
      });
    });
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
