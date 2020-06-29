-------------------------------------------------------------------------------------------------------------
-- CONSULTA PARA ENCONTRAR LA TABLA CORRESPONDIENTE AL FORMATO DE TARIFAS | SE BUSCA POR NOMBRE DE CAMPO(T's)
-------------------------------------------------------------------------------------------------------------
SELECT * FROM all_tab_columns
WHERE COLUMN_NAME LIKE '%1673%';

-------------------------------------------------------------------------------------------------------------
-- CONSULTA PARA BUSCAR UNA TABLA EN UN ESQUEMA DE BASE DE DATOS
-------------------------------------------------------------------------------------------------------------
SELECT * FROM all_tab_columns
WHERE TABLE_NAME LIKE '%FORMATO7%';

-------------------------------------------------------------------------------------------------------------
-- CONSULTA PARRILLA COSTO UNITARIO
-------------------------------------------------------------------------------------------------------------
SELECT FT7.* FROM -- TRAEMOS LOS DATOS QUE NO TUVIERON CORRECCIÓN
( -- TRAEMOS LOS DATOS DE FT7 (DATOS QUE NO TUVIERON CORRECCIÓN Y LOS QUE TIENEN CORRECCIÓN DE FT8)
    SELECT * FROM ENERGIA_CREG_015.CAR_COSTO_UNITARIO_119_UR
    WHERE 
        (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG)
        AND (CAR_T1669_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG)
        AND CAR_CARG_ANO = :ANIO_ARG
        AND CAR_CARG_PERIODO = :PERIODO_ARG
        AND CAR_T1676_ANIO_CORREG IS NULL
)FT7
LEFT JOIN -- LE QUITAMOS LOS DATOS DE FT8 (DATOS CORREGIDOS)
(
    SELECT * FROM ENERGIA_CREG_015.CAR_COSTO_UNITARIO_119_UR
    WHERE 
        (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG)
        AND (CAR_T1669_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG)
        AND CAR_CARG_ANO = :ANIO_ARG
        AND CAR_CARG_PERIODO = :PERIODO_ARG
        AND CAR_T1676_ANIO_CORREG IS NOT NULL
)F8
ON FT7.CAR_T1669_ID_MERCADO = F8.CAR_T1669_ID_MERCADO
AND FT7.ID_EMPRESA = F8.ID_EMPRESA
AND FT7.CAR_T1669_NT_PROP = F8.CAR_T1669_NT_PROP
AND FT7.CAR_CARG_ANO = F8.CAR_CARG_ANO
AND FT7.CAR_CARG_PERIODO = F8.CAR_CARG_PERIODO
WHERE (FT7.CAR_T1676_ANIO_CORREG IS NULL AND F8.CAR_T1676_ANIO_CORREG IS NULL)
UNION -- LE AGREGAMOS LOS DATOS DE FT8
(
    SELECT * FROM ENERGIA_CREG_015.CAR_COSTO_UNITARIO_119_UR
    WHERE 
        (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG)
        AND (CAR_T1669_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG)
        AND CAR_CARG_ANO = :ANIO_ARG
        AND CAR_CARG_PERIODO = :PERIODO_ARG
        AND CAR_T1676_ANIO_CORREG IS NOT NULL
); --FT8

-- ORDENANDO LA CONSULTA ANTERIOR POR ID_MERCADO
SELECT * FROM 
(
    (
        SELECT FT7.* FROM 
        (
            SELECT * FROM ENERGIA_CREG_015.CAR_COSTO_UNITARIO_119_UR 
            WHERE 
                (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
                AND (CAR_T1669_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG) 
                AND CAR_CARG_ANO = :ANIO_ARG 
                AND CAR_CARG_PERIODO = :PERIODO_ARG 
                AND CAR_T1676_ANIO_CORREG IS NULL
        )FT7 
        LEFT JOIN 
        (
            SELECT * FROM ENERGIA_CREG_015.CAR_COSTO_UNITARIO_119_UR 
            WHERE 
                (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
                AND (CAR_T1669_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG) 
                AND CAR_CARG_ANO = :ANIO_ARG 
                AND CAR_CARG_PERIODO = :PERIODO_ARG 
                AND CAR_T1676_ANIO_CORREG IS NOT NULL
        )F8 
        ON FT7.CAR_T1669_ID_MERCADO = F8.CAR_T1669_ID_MERCADO 
        AND FT7.ID_EMPRESA = F8.ID_EMPRESA 
        AND FT7.CAR_T1669_NT_PROP = F8.CAR_T1669_NT_PROP 
        AND FT7.CAR_CARG_ANO = F8.CAR_CARG_ANO 
        AND FT7.CAR_CARG_PERIODO = F8.CAR_CARG_PERIODO 
        WHERE (FT7.CAR_T1676_ANIO_CORREG IS NULL AND F8.CAR_T1676_ANIO_CORREG IS NULL) 
    )
    UNION 
    (
        SELECT * FROM ENERGIA_CREG_015.CAR_COSTO_UNITARIO_119_UR 
        WHERE 
            (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
            AND (CAR_T1669_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG) 
            AND CAR_CARG_ANO = :ANIO_ARG 
            AND CAR_CARG_PERIODO = :PERIODO_ARG 
            AND CAR_T1676_ANIO_CORREG IS NOT NULL
    )
)
ORDER BY CAR_T1669_ID_MERCADO ASC;

-------------------------------------------------------------------------------------------------------------
-- CONSULTA PARA TRAER CANTIDAD DE DATOS CORREGIDOS Y NO CORREGIDOS FT7 - FT8
-------------------------------------------------------------------------------------------------------------
SELECT ID_EMPRESA, CAR_T1669_ID_MERCADO, CAR_T1669_NT_PROP, COUNT(*) FROM ENERGIA_CREG_015.CAR_COSTO_UNITARIO_119_UR
WHERE 
    --ID_EMPRESA = 2322
    --AND CAR_T1669_ID_MERCADO = 173
    CAR_CARG_ANO = 2020
    AND CAR_CARG_PERIODO = 2
GROUP BY ID_EMPRESA, CAR_T1669_ID_MERCADO, CAR_T1669_NT_PROP
ORDER BY CAR_T1669_NT_PROP;

-------------------------------------------------------------------------------------------------------------
-- CONSULTA PARA HHALLAR VALOR DEL COMPONENTE G
-------------------------------------------------------------------------------------------------------------
SELECT 
    ((LEAST(1,((T9.C1_C7 + T9.C3_C2) / (T10.C12_C4 + T9.C13_C15 + T10.C14_C6 + T9.C15_C16))) * ((C25_C14 * ((T9.C4_C8 + T9.C6_C3) / (T9.C1_C7 + T9.C3_C2))) + (1 - C25_C14) * (T13.C9_C1 + T9.C10_C4))) + ((1 - (LEAST(1,((T9.C1_C7 + T9.C3_C2) / (T10.C12_C4 + T9.C13_C15 + T10.C14_C6 + T9.C15_C16)))) - (T9.C19_C9 + T9.C20_C10)) * (T9.C8_C6 / T9.C7_C5)) + T9.C24_C13 + T9.C26_C11) AS C28_CG 
FROM 
(
    SELECT 
        CAR_T1671_DMRE AS C12_C4,
        CAR_T1671_PRRE AS C14_C6,
        CAR_T1671_ECC AS C2_C2,
        CAR_T1671_VECC AS C5_C3 
    FROM ENERGIA_CREG_015.CAR_T1671_INFORMACION_ASIC_LAC 
    WHERE CAR_CARG_ANO = :ANIO_ARG 
    and CAR_CARG_PERIODO = :PERIODO_ARG 
    AND (CAR_T1671_ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
) T10,
(
    SELECT 
        CAR_1672_ECC AS C1_C7,
        CAR_1672_AECC AS C3_C2,
        CAR_1672_VECC AS C4_C8,
        CAR_1672_CB AS C7_C5,
        CAR_1672_VCB AS C8_C6,
        CAR_1672_ADMRE_G AS C13_C15,
        CAR_1672_APRRE_G AS C15_C16,
        CAR_1672_AVECC AS C6_C3,
        CAR_1672_AGPE AS C19_C9,
        CAR_1672_GD AS C20_C10,
        CAR_1672_AJ AS C24_C13,
        CAR_1672_ALFA AS C25_C14,
        CAR_1672_GTR AS C26_C11,
        CAR_1672_CFNC AS C27_C12,
        CAR_1672_AMC AS C10_C4,
        CAR_CARG_ANO,
        CAR_CARG_PERIODO 
    FROM 
        ENERGIA_CREG_015.CAR_VAR_COSTO_UNT_PS_CU_119_UR 
    WHERE 
        CAR_CARG_ANO = :ANIO_ARG 
        AND CAR_CARG_PERIODO = :PERIODO_ARG 
        AND (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
        AND (CAR_1672_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG) 
) T9,
(
SELECT 
    CAR_T1673_MC AS C9_C1 
FROM ENERGIA_CREG_015.CAR_INFORMACION_GENERAL 
    WHERE 
        CAR_CARG_ANO = :ANIO_ARG 
        AND CAR_CARG_PERIODO = :PERIODO_ARG 
)T13;


------------------------------------------------------------------------------------------
--- CONSULTA PARA HHALLAR VALOR DEL COMPONENTE T - PREGUNTAR A DIEGO
------------------------------------------------------------------------------------------
SELECT FT7.C3_C6 + FT13.C4_C2 AS C5_CT FROM 
(
SELECT CAR_T1669_DNM AS C3_C6 
FROM ENERGIA_CREG_015.CAR_COSTO_UNITARIO_119_UR
WHERE ID_EMPRESA = 2103
AND CAR_T1669_ID_MERCADO = 176
AND CAR_CARG_ANO = 2020
AND CAR_CARG_PERIODO = 2
)FT7,
(
SELECT CAR_T1673_STN_MO AS C4_C2 
FROM ENERGIA_CREG_015.CAR_INFORMACION_GENERAL
WHERE CAR_CARG_ANO = 2019
AND CAR_CARG_PERIODO = 12
)FT13;

------------------------------------------------------------------------------------------
--- CONSULTA PARA HHALLAR VALOR DEL COMPONENTE P - COMPONENTE PERDIDAS 015
------------------------------------------------------------------------------------------
SELECT 
    (C16 + C20 + C15) AS C24,
    (C17 + C21 + C15) AS C25,
    (C18 + C22 + C15) AS C26,
    (C19 + C23 + C15) AS C27
FROM
(
    SELECT 
        FT11.C15_C30 AS C15,
        (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18) AS C8,
        (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18) AS C9,
        ((CPTE_G.C28_CG *(FT11.C10_C21 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18))) / (1 - (FT11.C10_C21 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18)))) AS C16,
        ((CPTE_T.C5_CT * FT11.C10_C21 / 100) / (1 - FT11.C10_C21 / 100)) AS C20,
        
        ((CPTE_G.C28_CG *(FT11.C11_C20 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18))) / (1 - (FT11.C11_C20 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18)))) AS C17,
        ((CPTE_T.C5_CT * FT11.C11_C20 / 100) / (1 - FT11.C11_C20 / 100)) AS C21,
        
        ((CPTE_G.C28_CG *(FT11.C12_C19 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18))) / (1 - (FT11.C12_C19 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18)))) AS C18,
        ((CPTE_T.C5_CT * FT11.C12_C19 / 100) / (1 - FT11.C12_C19 / 100)) AS C22,
        
        ((CPTE_G.C28_CG *(FT11.C13_C18 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18))) / (1 - (FT11.C13_C18 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18)))) AS C19,
        ((CPTE_T.C5_CT * FT11.C13_C18 / 100) / (1 - FT11.C13_C18 / 100)) AS C23
    FROM
    (
        SELECT 
            ((LEAST(1,((T9.C1_C7 + T9.C3_C2) / (T10.C12_C4 + T9.C13_C15 + T10.C14_C6 + T9.C15_C16))) * ((C25_C14 * ((T9.C4_C8 + T9.C6_C3) / (T9.C1_C7 + T9.C3_C2))) + (1 - C25_C14) * (T13.C9_C1 + T9.C10_C4))) + ((1 - (LEAST(1,((T9.C1_C7 + T9.C3_C2) / (T10.C12_C4 + T9.C13_C15 + T10.C14_C6 + T9.C15_C16)))) - (T9.C19_C9 + T9.C20_C10)) * (T9.C8_C6 / T9.C7_C5)) + T9.C24_C13 + T9.C26_C11) AS C28_CG 
        FROM 
        (
            SELECT 
                CAR_T1671_DMRE AS C12_C4,
                CAR_T1671_PRRE AS C14_C6,
                CAR_T1671_ECC AS C2_C2,
                CAR_T1671_VECC AS C5_C3 
            FROM ENERGIA_CREG_015.CAR_T1671_INFORMACION_ASIC_LAC 
            WHERE CAR_CARG_ANO = :ANIO_ARG 
            and CAR_CARG_PERIODO = :PERIODO_ARG 
            AND (CAR_T1671_ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
        ) T10,
        (
            SELECT 
                CAR_1672_ECC AS C1_C7,
                CAR_1672_AECC AS C3_C2,
                CAR_1672_VECC AS C4_C8,
                CAR_1672_CB AS C7_C5,
                CAR_1672_VCB AS C8_C6,
                CAR_1672_ADMRE_G AS C13_C15,
                CAR_1672_APRRE_G AS C15_C16,
                CAR_1672_AVECC AS C6_C3,
                CAR_1672_AGPE AS C19_C9,
                CAR_1672_GD AS C20_C10,
                CAR_1672_AJ AS C24_C13,
                CAR_1672_ALFA AS C25_C14,
                CAR_1672_GTR AS C26_C11,
                CAR_1672_CFNC AS C27_C12,
                CAR_1672_AMC AS C10_C4,
                CAR_CARG_ANO,
                CAR_CARG_PERIODO 
            FROM 
                ENERGIA_CREG_015.CAR_VAR_COSTO_UNT_PS_CU_119_UR 
            WHERE 
                CAR_CARG_ANO = :ANIO_ARG 
                AND CAR_CARG_PERIODO = :PERIODO_ARG 
                AND (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
                AND (CAR_1672_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG) 
        ) T9,
        (
        SELECT 
            CAR_T1673_MC AS C9_C1 
        FROM ENERGIA_CREG_015.CAR_INFORMACION_GENERAL 
            WHERE 
                CAR_CARG_ANO = :ANIO_ARG 
                AND CAR_CARG_PERIODO = :PERIODO_ARG 
        )T13
    )CPTE_G,
    (
        SELECT CAR_T1673_STN_MO AS C5_CT 
        FROM ENERGIA_CREG_015.CAR_INFORMACION_GENERAL
        WHERE CAR_CARG_ANO = 2020
        AND CAR_CARG_PERIODO = 1
    )CPTE_T,
    (
        SELECT 
            CAR_T1671_DMRE AS C2_C4,
            CAR_T1671_PRRE AS C3_C6,
            CAR_T1671_DMNR AS C4_C5,
            CAR_T1671_PRNR AS C5_C7
        FROM ENERGIA_CREG_015.CAR_T1671_INFORMACION_ASIC_LAC
        WHERE CAR_CARG_ANO = :ANIO_ARG 
        and CAR_CARG_PERIODO = :PERIODO_ARG 
        AND (CAR_T1671_ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
    )FT10,
    (
        SELECT 
            CAR_1672_ADR_IPRSTN AS C6_C17,
            CAR_1672_APR_IPRSTN AS C7_C18
        FROM ENERGIA_CREG_015.CAR_VAR_COSTO_UNT_PS_CU_119_UR
        WHERE 
            CAR_CARG_ANO = :ANIO_ARG 
            AND CAR_CARG_PERIODO = :PERIODO_ARG 
            AND (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
            AND (CAR_1672_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG)
    )FT9,
    (
        SELECT CAR_T1679_PR4 AS C13_C18,
               CAR_T1679_PR3 AS C12_C19,
               CAR_T1679_PR2 AS C11_C20,
               CAR_T1679_PR1 AS C10_C21,
               CAR_T1679_CPROG AS C15_C30
        FROM ENERGIA_CREG_015.CAR_INFORMACION_ASIC_LAC_DISTI
        WHERE 
            CAR_CARG_ANO = :ANIO_ARG 
            AND CAR_CARG_PERIODO = :PERIODO_ARG 
            AND (CAR_T1679_ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG)
    )FT11
);

------------------------------------------------------------------------------------------
--- CONSULTA PARA HHALLAR VALOR DEL COMPONENTE D - COMPONENTE DISTRIBUCION 015
------------------------------------------------------------------------------------------
SELECT 
    CPTE_D.*,
    C14+(C3/(1-C10/100))+C1+C2+C11 AS C18,
    C14+(C3/(1-C10/100))+C2+C11 AS C19,
    C14+(C3/(1-C10/100))+(C1/2)+C2+C11 AS C20,
    C15+C3+C12 AS C21,
    C16+C4+C13 AS C22,
    C17 AS C23
FROM
(
    SELECT 
        FT11.*,
        FT13.*,
        C5 / (1 - C6 / 100) AS C14,
        C5 / (1 - C7 / 100) AS C15,
        C5 / (1 - C8 / 100) AS C16,
        C5 / (1 - C9 / 100) AS C17
    FROM
    (
        SELECT 
            CAR_T1679_PR4 AS C9,
            CAR_T1679_PR3 AS C8,
            CAR_T1679_PR2 AS C7,
            CAR_T1679_PR1 AS C6,
            CAR_T1679_P1 AS C10,
            CAR_T1679_CDI AS C1,
            CAR_T1679_CDA AS C2,
            CAR_T1679_CD2 AS C3,
            CAR_T1679_CD3 AS C4,
            CAR_T1679_DTCS1 AS C11,
            CAR_T1679_DTCS2 AS C12,
            CAR_T1679_DTCS3 AS C13
        FROM ENERGIA_CREG_015.CAR_INFORMACION_ASIC_LAC_DISTI
        WHERE 
            CAR_CARG_ANO = :ANIO_ARG 
            AND CAR_CARG_PERIODO = :PERIODO_ARG 
            AND (CAR_T1679_ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG)
    )FT11,
    (
        SELECT 
            CASE 
                WHEN :EMPRESA_ARG = 2249 THEN CAR_T1673_CD4_NORTE
                ELSE CAR_T1673_CD4_CENTRO_SUR
            END AS C5
        FROM ENERGIA_CREG_015.CAR_INFORMACION_GENERAL 
        WHERE 
            CAR_CARG_ANO = :ANIO_ARG 
            AND CAR_CARG_PERIODO = :PERIODO_ARG
    )FT13
)CPTE_D;


------------------------------------------------------------------------------------------
--- CONSULTA PARA HALLAR VALOR DEL COMPONENTE Dtun
------------------------------------------------------------------------------------------
SELECT
    FT12.*,
    FT11.*,
    C1 - (C2 / 2) AS C3,
    C1 - C2 AS C4
FROM 
(
    SELECT 
        CASE WHEN CAR_1674_ADD = 1 THEN CAR_1674_DT_UN_NT1 END AS C1,
        CASE WHEN CAR_1674_ADD = 1 THEN CAR_1674_DT_UN_NT2 END AS C5,
        CASE WHEN CAR_1674_ADD = 1 THEN CAR_1674_DT_UN_NT3 END AS C6
    FROM ENERGIA_CREG_015.CAR_T1674_INFORMACION_ADD
) FT12,
(
    SELECT 
        CAR_T1679_CDI AS C2
    FROM ENERGIA_CREG_015.CAR_INFORMACION_ASIC_LAC_DISTI
    WHERE 
        CAR_CARG_ANO = :ANIO_ARG 
        AND CAR_CARG_PERIODO = :PERIODO_ARG 
        AND (CAR_T1679_ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG)
)FT11;


------------------------------------------------------------------------------------------
--- CONSULTA PARA HALLAR VALOR DEL COMPONENTE R - REESTRICCIONES
------------------------------------------------------------------------------------------
SELECT 
    (C1 + C2 + C3 + C4) AS C5,
    (C1 + C2 + C3 + C4) / C6
FROM 
(
    SELECT 
        CAR_1672_AREST AS C4
    FROM 
        ENERGIA_CREG_015.CAR_VAR_COSTO_UNT_PS_CU_119_UR 
    WHERE 
        CAR_CARG_ANO = :ANIO_ARG 
        AND CAR_CARG_PERIODO = :PERIODO_ARG 
        AND (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
        AND (CAR_1672_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG) 
)T9,
(
    SELECT 
        CAR_T1671_RTCSA AS C1,
        CAR_T1671_VDESV AS C2,
        CAR_T1671_GUATAPE AS C3
    FROM ENERGIA_CREG_015.CAR_T1671_INFORMACION_ASIC_LAC
    WHERE CAR_CARG_ANO = :ANIO_ARG 
    and CAR_CARG_PERIODO = :PERIODO_ARG 
    AND (CAR_T1671_ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
)FT10,
(
    SELECT 
        CASE WHEN CAR_T1743_TIPO_FACT = 1 THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END AS C6
    FROM ENERGIA_CREG_015.CAR_T1743_TC2FACTURACION_USU 
    WHERE
        IDENTIFICADOR_EMPRESA = :EMPRESA_ARG
        AND CAR_CARG_PERIODO = :PERIODO_ARG
        AND CAR_CARG_ANO = :ANIO_ARG
)FTC2;