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
  total?: number;
}

export interface IDialogData {
  view: any;
  fabOptions: any;
  optionsMap: IOptionsMapa;
  suiAnios: number;
  suiCausas: any;
  suiEmpresas: any;
  updateLayerCSV: boolean;
  dataCSV: any;
}

export interface IEmpresa {
  cod_empresa: number;
  nombre: string;
  servicio: string;
}

export interface ICausas {
  calzesp: number;
  castnat: number;
  centro_poblado: string;
  cod_dane: string;
  cod_empresa: string;
  exp: number;
  fnivel1: number;
  infra: number;
  latitude: number;
  longitude: number;
  nom_empresa: string;
  npnexc: number;
  pnexc: number;
  remer: number;
  segciu: number;
  stnstr: number;
  sumi: number;
  terr: number;
  total: number;
  tsubest: number;
  length?: number;
}

export interface ICausa {
  causa: string;
  descripcion?: string;
  horas_interrupcion: number;
}

export interface ISUIError {
  status: number;
  message: number;
}
