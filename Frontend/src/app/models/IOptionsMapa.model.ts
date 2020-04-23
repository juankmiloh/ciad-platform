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
  result?: any;
}
