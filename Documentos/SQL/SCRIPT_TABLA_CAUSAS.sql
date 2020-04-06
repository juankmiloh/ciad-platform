CREATE TABLE CAUSAS_INTERR(
    COD_CAUSA NUMBER(5,0),
    COL_SUI VARCHAR2(50 BYTE),
    DESCRIPCION VARCHAR2(50 BYTE)
);

INSERT INTO CAUSAS_INTERR VALUES (16, 'PNEXC', 'Programadas no excluibles');
INSERT INTO CAUSAS_INTERR VALUES (18, 'NPNEXC', 'No programadas no excluibles');
INSERT INTO CAUSAS_INTERR VALUES (20, 'REMER', 'Racionamiento de emergencia');
INSERT INTO CAUSAS_INTERR VALUES (22, 'STNSTR', 'Eventos de activos STN | STR');
INSERT INTO CAUSAS_INTERR VALUES (24, 'SEGCIU', 'Seguridad ciudadana');
INSERT INTO CAUSAS_INTERR VALUES (26, 'FNIVEL1', 'Falla activo de Nivel 1');
INSERT INTO CAUSAS_INTERR VALUES (28, 'CASTNAT', 'Catastrofes naturales');
INSERT INTO CAUSAS_INTERR VALUES (30, 'TERR', 'Actos de terrorismo');
INSERT INTO CAUSAS_INTERR VALUES (32, 'CALZESP', 'Acuerdos de calidad en las zonas especiales');
INSERT INTO CAUSAS_INTERR VALUES (34, 'TSUBEST', 'Trabajos en Subestaciones (PARR)');
INSERT INTO CAUSAS_INTERR VALUES (36, 'INFRA', 'Traslados y adecuaciones de la infraestructura');
INSERT INTO CAUSAS_INTERR VALUES (38, 'SUMI', 'Programas de limitación del suministro');
INSERT INTO CAUSAS_INTERR VALUES (40, 'EXP', 'Proyectos de expansión');

COMMIT;