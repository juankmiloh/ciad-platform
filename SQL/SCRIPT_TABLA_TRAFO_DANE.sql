----------------------------------------------------------------------------------------
-- TABLA PARA GUARDAR INFORMACIÓN DE TRANSFORMADORES CON SU CORRESPONDIENTE CÓDIGO DANE
----------------------------------------------------------------------------------------
CREATE TABLE TRAFO_DANE(
    IDENTIFICADOR_EMPRESA NUMBER(5,0),
    COD_TRAFO VARCHAR2(50 BYTE),
    COD_DANE VARCHAR2(8 BYTE)
);

----------------------------------------------------------------------------------------
-- INSERT TABLA 'TRAFO_DANE'
----------------------------------------------------------------------------------------
INSERT INTO TRAFO_DANE -- 2.109.954.653  Filas
SELECT DISTINCT F1.IDENTIFICADOR_EMPRESA, F1.CAR_T438_COD_CONEX, F23.DANE FROM
(
    SELECT
        IDENTIFICADOR_EMPRESA,
        CAR_T438_NIU,
        CAR_T438_COD_CONEX
    FROM
        CARG_COMERCIAL_E.CAR_T438_FORMATO1
    WHERE  
        CAR_T438_TIPO_CONEX = 'T'
        AND CAR_CARG_ANO = 2019
) F1,
(
    SELECT
        IDENTIFICADOR_EMPRESA,
        CAR_T439_NIU NIU,
        CAR_T439_DANE DANE
    FROM
        CARG_COMERCIAL_E.CAR_T439_FORMATO2
    WHERE
        CAR_CARG_ANO = 2019
    UNION ALL
    SELECT
        IDENTIFICADOR_EMPRESA,
        CAR_T440_NIU NIU,
        CAR_T440_DANE DANE
    FROM
        CARG_COMERCIAL_E.CAR_T440_FORMATO3
    WHERE
        CAR_CARG_ANO = 2019
) F23
WHERE
    F1.CAR_T438_NIU = NIU
    AND F1.IDENTIFICADOR_EMPRESA = F23.IDENTIFICADOR_EMPRESA;

----------------------------------------------------------------------------------------
-- SCRIPT PARA UNIR F5 CON SU RESPECTIVO CODIGO DANE
----------------------------------------------------------------------------------------
SELECT * FROM
(
    SELECT * FROM TRAFO_DANE
) TRAFODANE,
(
    SELECT
        CAR_T442_COD_TRANS,
        CAR_T442_LONG,
        CAR_T442_LAT,
        IDENTIFICADOR_EMPRESA
    FROM
        CARG_COMERCIAL_E.CAR_T442_FORMATO5
    WHERE
        IDENTIFICADOR_EMPRESA = 2249
        AND CAR_CARG_ANO = 2019
) F5
WHERE
    TRAFODANE.COD_TRAFO = F5.CAR_T442_COD_TRANS
    AND TRAFODANE.IDENTIFICADOR_EMPRESA = F5.IDENTIFICADOR_EMPRESA;

----------------------------------------------------------------------------------------
-- SCRIPT PARA OBTENER POR CODIGO DANE LA CANTIDAD DE MINUTOS DE INTERRUPCIÓN DE CADA UNA DE LAS CAUSAS
-- SE OBTIENE TAMBIEN EL TOTAL DE MINUTOS DE INTERRUPCION DE TODAS LAS CAUSAS POR CODIGO DANE
-- SE MUESTRA LATITUD Y LONGITUD DEL CENTRO POBLADO (CODIGO DANE)
----------------------------------------------------------------------------------------
SELECT 
    CONVERT(CP.NOMBRE_CENTRO_POBLADO, 'US7ASCII', 'EE8MSWIN1250'),
    CP.LONGITUD,
    CP.LATITUD,
    DANE_INTER.COD_DANE,
    DANE_INTER.IDENTIFICADOR_EMPRESA,
    ROUND(DANE_INTER.PNEXC,2),
    ROUND(DANE_INTER.NPNEXC,2),
    ROUND(DANE_INTER.REMER,2),
    ROUND(DANE_INTER.STNSTR,2),
    ROUND(DANE_INTER.SEGCIU,2),
    ROUND(DANE_INTER.FNIVEL1,2),
    ROUND(DANE_INTER.CASTNAT,2),
    ROUND(DANE_INTER.TERR,2),
    ROUND(DANE_INTER.CALZESP,2),
    ROUND(DANE_INTER.TSUBEST,2),
    ROUND(DANE_INTER.INFRA,2),
    ROUND(DANE_INTER.SUMI,2),
    ROUND(DANE_INTER.PEXP,2),
    ROUND(DANE_INTER.TOTAL_INTER/60,2) 
FROM 
(
    SELECT 
        INTER.*,
        PNEXC+NPNEXC+REMER+STNSTR+SEGCIU+FNIVEL1+CASTNAT+TERR+CALZESP+TSUBEST+INFRA+SUMI+PEXP AS TOTAL_INTER 
    FROM 
    (
        SELECT 
            TRAFODANE.COD_DANE,
            F5.IDENTIFICADOR_EMPRESA,
            CASE WHEN (:PNEXC_ARG = 16) THEN SUM(F5.CAR_T442_MIN_PBEXC) ELSE 0 END AS PNEXC,
            CASE WHEN (:NPNEXC_ARG = 18) THEN SUM(F5.CAR_T442_MIN_NPNEXC) ELSE 0 END AS NPNEXC,
            CASE WHEN (:REMER_ARG = 20) THEN SUM(F5.CAR_T442_MIN_REMER) ELSE 0 END AS REMER,
            CASE WHEN (:STNSTR_ARG = 22) THEN SUM(F5.CAR_T442_MIN_STNSTR) ELSE 0 END AS STNSTR,
            CASE WHEN (:SEGCIU_ARG = 24) THEN SUM(F5.CAR_T442_MIN_SEG_CIU) ELSE 0 END AS SEGCIU,
            CASE WHEN (:FNIVEL1_ARG = 26) THEN SUM(F5.CAR_T442_MIN_FNIVEL1) ELSE 0 END AS FNIVEL1,
            CASE WHEN (:CASTNAT_ARG = 28) THEN SUM(F5.CAR_T442_MIN_CASTNAT) ELSE 0 END AS CASTNAT,
            CASE WHEN (:TERR_ARG = 30) THEN SUM(F5.CAR_T442_MIN_TERR) ELSE 0 END AS TERR,
            CASE WHEN (:CALZESP_ARG = 32) THEN SUM(F5.CAR_T442_MIN_CAL_ZESP) ELSE 0 END AS CALZESP,
            CASE WHEN (:TSUBEST_ARG = 34) THEN SUM(F5.CAR_T442_MIN_TSUBEST) ELSE 0 END AS TSUBEST,
            CASE WHEN (:INFRA_ARG = 36) THEN SUM(F5.CAR_T442_MIN_INFRA) ELSE 0 END AS INFRA,
            CASE WHEN (:SUMI_ARG = 38) THEN SUM(F5.CAR_T442_MIN_SUMI) ELSE 0 END AS SUMI,
            CASE WHEN (:PEXP_ARG = 40) THEN SUM(F5.CAR_T442_MIN_EXP) ELSE 0 END AS PEXP 
        FROM 
        (
            SELECT 
                * 
            FROM 
                CARG_COMERCIAL_E.CAR_T442_FORMATO5 
            WHERE 
                CAR_CARG_ANO = :ANIO_ARG
                AND (IDENTIFICADOR_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG)
                AND (CAR_CARG_MES = :MES_ARG OR :MES_ARG = 0 )
        ) F5,
        (SELECT * FROM TRAFO_DANE) TRAFODANE 
        WHERE 
            F5.CAR_T442_COD_TRANS = TRAFODANE.COD_TRAFO
            AND F5.IDENTIFICADOR_EMPRESA = TRAFODANE.IDENTIFICADOR_EMPRESA 
        GROUP BY 
            TRAFODANE.COD_DANE,
            F5.IDENTIFICADOR_EMPRESA
    ) INTER 
    WHERE PNEXC+NPNEXC+REMER+STNSTR+SEGCIU+FNIVEL1+CASTNAT+TERR+CALZESP+TSUBEST+INFRA+SUMI+PEXP > 0
) DANE_INTER,
(SELECT * FROM JHERRERAA.GIS_CENTRO_POBLADO) CP 
WHERE DANE_INTER.COD_DANE = CP.CODIGO_CENTRO_POBLADO;

----------------------------------------------------------------------------------------
-- SCRIPT ANTERIOR ANEXANDOLE LA UNION CON LA TABLA DE EMPRESAS, PARA PODER ASOCIARLE EL NOMBRE DE LA EMPRESA
----------------------------------------------------------------------------------------
SELECT CONVERT(EMPRESA.ARE_ESP_NOMBRE, 'US7ASCII', 'EE8MSWIN1250'),
       INTERR.* 
FROM 
(
    SELECT 
        CONVERT(CP.NOMBRE_CENTRO_POBLADO, 'US7ASCII', 'EE8MSWIN1250'),
        CP.LONGITUD,
        CP.LATITUD,
        TO_CHAR(DANE_INTER.COD_DANE),
        DANE_INTER.IDENTIFICADOR_EMPRESA,
        ROUND(DANE_INTER.PNEXC/60,2),
        ROUND(DANE_INTER.NPNEXC/60,2),
        ROUND(DANE_INTER.REMER/60,2),
        ROUND(DANE_INTER.STNSTR/60,2),
        ROUND(DANE_INTER.SEGCIU/60,2),
        ROUND(DANE_INTER.FNIVEL1/60,2),
        ROUND(DANE_INTER.CASTNAT/60,2),
        ROUND(DANE_INTER.TERR/60,2),
        ROUND(DANE_INTER.CALZESP/60,2),
        ROUND(DANE_INTER.TSUBEST/60,2),
        ROUND(DANE_INTER.INFRA/60,2),
        ROUND(DANE_INTER.SUMI/60,2),
        ROUND(DANE_INTER.PEXP/60,2),
        ROUND(DANE_INTER.TOTAL_INTER/60,2) 
    FROM 
    (
        SELECT 
            INTER.*,
            PNEXC+NPNEXC+REMER+STNSTR+SEGCIU+FNIVEL1+CASTNAT+TERR+CALZESP+TSUBEST+INFRA+SUMI+PEXP AS TOTAL_INTER 
        FROM 
        (
            SELECT 
                TRAFODANE.COD_DANE,
                F5.IDENTIFICADOR_EMPRESA,
                CASE WHEN (:PNEXC_ARG = 16) THEN SUM(F5.CAR_T442_MIN_PBEXC) ELSE 0 END AS PNEXC,
                CASE WHEN (:NPNEXC_ARG = 18) THEN SUM(F5.CAR_T442_MIN_NPNEXC) ELSE 0 END AS NPNEXC,
                CASE WHEN (:REMER_ARG = 20) THEN SUM(F5.CAR_T442_MIN_REMER) ELSE 0 END AS REMER,
                CASE WHEN (:STNSTR_ARG = 22) THEN SUM(F5.CAR_T442_MIN_STNSTR) ELSE 0 END AS STNSTR,
                CASE WHEN (:SEGCIU_ARG = 24) THEN SUM(F5.CAR_T442_MIN_SEG_CIU) ELSE 0 END AS SEGCIU,
                CASE WHEN (:FNIVEL1_ARG = 26) THEN SUM(F5.CAR_T442_MIN_FNIVEL1) ELSE 0 END AS FNIVEL1,
                CASE WHEN (:CASTNAT_ARG = 28) THEN SUM(F5.CAR_T442_MIN_CASTNAT) ELSE 0 END AS CASTNAT,
                CASE WHEN (:TERR_ARG = 30) THEN SUM(F5.CAR_T442_MIN_TERR) ELSE 0 END AS TERR,
                CASE WHEN (:CALZESP_ARG = 32) THEN SUM(F5.CAR_T442_MIN_CAL_ZESP) ELSE 0 END AS CALZESP,
                CASE WHEN (:TSUBEST_ARG = 34) THEN SUM(F5.CAR_T442_MIN_TSUBEST) ELSE 0 END AS TSUBEST,
                CASE WHEN (:INFRA_ARG = 36) THEN SUM(F5.CAR_T442_MIN_INFRA) ELSE 0 END AS INFRA,
                CASE WHEN (:SUMI_ARG = 38) THEN SUM(F5.CAR_T442_MIN_SUMI) ELSE 0 END AS SUMI,
                CASE WHEN (:PEXP_ARG = 40) THEN SUM(F5.CAR_T442_MIN_EXP) ELSE 0 END AS PEXP 
            FROM 
            (
                SELECT 
                    * 
                FROM 
                    CARG_COMERCIAL_E.CAR_T442_FORMATO5 
                WHERE 
                    CAR_CARG_ANO = :ANIO_ARG
                    AND (IDENTIFICADOR_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG)
                    AND (CAR_CARG_MES = :MES_ARG OR :MES_ARG = 0 )
            ) F5,
            (SELECT * FROM TRAFO_DANE) TRAFODANE 
            WHERE 
                F5.CAR_T442_COD_TRANS = TRAFODANE.COD_TRAFO
                AND F5.IDENTIFICADOR_EMPRESA = TRAFODANE.IDENTIFICADOR_EMPRESA 
            GROUP BY 
                TRAFODANE.COD_DANE,
                F5.IDENTIFICADOR_EMPRESA
        ) INTER 
        WHERE PNEXC+NPNEXC+REMER+STNSTR+SEGCIU+FNIVEL1+CASTNAT+TERR+CALZESP+TSUBEST+INFRA+SUMI+PEXP > 0
    ) DANE_INTER,
    (SELECT * FROM JHERRERAA.GIS_CENTRO_POBLADO) CP 
    WHERE DANE_INTER.COD_DANE = CP.CODIGO_CENTRO_POBLADO
)INTERR,
(
    SELECT * FROM 
    (
        SELECT DISTINCT EMP.ARE_ESP_SECUE,
               EMP.ARE_ESP_NOMBRE,
               'ENERGIA' SERVICIO 
        FROM 
              RUPS.ARE_ESP_EMPRESAS EMP,
              RUPS.PAR_SERV_SERVICIOS SER,
              RUPS.ARE_SEES_SERESP ROM,
              RUPS.ARE_NESP_NATESP NES,
              RUPS.ARE_ACES_ACTESP ACT 
        WHERE 
              ROM.ARE_ESP_SECUE = EMP.ARE_ESP_SECUE
              AND ROM.PAR_SERV_SECUE = SER.PAR_SERV_SECUE
              AND ROM.ARE_ESP_SECUE = NES.ARE_ESP_SECUE
              AND ROM.ARE_ESP_SECUE = ACT.ARE_ESP_SECUE
              AND SER.PAR_SERV_SECUE IN (4)
              AND EMP.ARE_ESP_SECUE < 99900
              AND ROM.ARE_SEES_ESTADO = 'O'
              AND NES.ARE_NESP_ESTADO = 'O'
              AND ACT.ARE_ACES_ESTADO = 'O'
              AND EMP.ARE_ESP_ACTUALIZA IS NOT NULL
              AND EMP.ARE_ESP_ESTACT = 'A'
              AND EMP.ARE_ESP_SECUE_CREG <> 0 
        GROUP BY 
                 EMP.ARE_ESP_SECUE,
                 EMP.ARE_ESP_NOMBRE,
                 SER.PAR_SERV_NOMBRE,
                 EMP.ARE_ESP_ACTUALIZA,
                 EMP.ARE_ESP_ESTACT,
                 EMP.ARE_ESP_SECUE_CREG,
                 'ENERGIA' 
        UNION 
        SELECT ARE_ESP_SECUE,
               ARE_ESP_NOMBRE,
               'ENERGIA' SERVICIO 
        FROM 
            RUPS.ARE_ESP_EMPRESAS
        WHERE ARE_ESP_SECUE = 44278 
    )
)EMPRESA
WHERE IDENTIFICADOR_EMPRESA = ARE_ESP_SECUE;