export interface IOptionsMapa {
  ano: number;
  mes: number;
  empresa: number;
  nombEmpresa?: string;
  causa: number;
  colSui?: string;
  nombCausa?: string;
  zoom: number;
  latitud: number;
  longitud: number;
  total?: string;
}

export interface DialogData {
  view: any;
  fabOptions: any;
  optionsMap: IOptionsMapa;
  suiAnios: number;
  suiCausas: any;
  suiEmpresas: any;
  updateLayerCSV: boolean;
  dataCSV: any;
}

export const MY_FORMATS = {
  parse: {
    dateInput: 'MMMM',
  },
  display: {
    dateInput: 'MMMM',
    monthYearLabel: 'MMM',
  },
};

export interface Empresa {
  cod_empresa: number;
  nombre: string;
  servicio: string;
}
