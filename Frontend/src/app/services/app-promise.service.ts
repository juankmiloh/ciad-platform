import { Injectable } from '@angular/core';
import { ICausa, IOptionsMapa, ICausas } from '../models/IOptionsMapa.model';

@Injectable({
  providedIn: 'root',
})
export class AppPromiseService {

  dataCompleted: boolean;
  arrayDataCausas: ICausa[] = [];
  arrayDataGraphic: any[] = [];

  constructor() { }

  // funcion para transformar arreglo de causas en objeto de causas
  public async transformData(data: ICausa, suiCausas: any): Promise<ICausa[]> {
    let contador = 0;
    this.arrayDataCausas = [];
    Object.entries(data).forEach(value => {
      if (contador > 5 && contador < 19) {
        const obj = {
          causa: value[0],
          descripcion: suiCausas.find(causa => causa.col_sui === value[0].toUpperCase()).descripcion,
          horas_interrupcion: parseFloat(String(value[1])), // Se pasa de unknown a float
        };
        this.arrayDataCausas.push(obj);
      }
      contador++;
    });
    return this.arrayDataCausas;
  }

  // funcion para transformar arreglo de causas en objeto de causas
  public async transformDataToGraphic(data: ICausas): Promise<ICausa[]> {
    let contador = 0;
    this.arrayDataGraphic = [];
    const totalInt = data.total;
    Object.entries(data).forEach(value => {
      if (contador > 5 && contador < 19) {
        if (value[1] !== '0') {
          const obj = {
            name: value[0],
            value: parseFloat(String(value[1])), // Se pasa de unknown a float
            extra: {
              percentage: ((totalInt - (totalInt - parseFloat(String(value[1])))) / totalInt) * 100,
            },
          };
          this.arrayDataGraphic.push(obj);
        }
      }
      contador++;
    });
    return this.arrayDataGraphic;
  }
}
