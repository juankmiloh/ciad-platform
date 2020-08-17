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
) FT7_FT8,
(
    SELECT 
        DISTINCT ID_MERCADO,
        NOM_MERCADO,
        ESTADO 
    FROM 
        CARG_COMERCIAL_E.MERCADO_EMPRESA 
    WHERE 
        ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG 
        AND NOM_MERCADO NOT LIKE '%Mercado Prueba%' 
        AND NOM_MERCADO NOT LIKE '%Mercado de Prueba%'
) MERCADO 
WHERE FT7_FT8.CAR_T1669_ID_MERCADO = MERCADO.ID_MERCADO 
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
    T10.*,
    T9.*,
    T13.*,
    (T10.C12_C4 + T9.C13_C15 + T10.C14_C6 + T9.C15_C16) AS C16_DCR,
    (LEAST(1,((T9.C1_C7 + T9.C3_C2) / (T10.C12_C4 + T9.C13_C15 + T10.C14_C6 + T9.C15_C16)))) AS C17_QC,
    ((T9.C4_C8 + T9.C6_C3) / (T9.C1_C7 + T9.C3_C2)) AS C22_PC,
    (1 - (LEAST(1,((T9.C1_C7 + T9.C3_C2) / (T10.C12_C4 + T9.C13_C15 + T10.C14_C6 + T9.C15_C16))))) AS C18_QB,
    (T9.C8_C6 / T9.C7_C5) AS C23_PB,
    (T9.C19_C9 + T9.C20_C10) AS C21_QAGD,
    (T13.C9_C1 + T9.C10_C4) AS C11_MCAPLICADO,
    (LEAST(1,((T9.C1_C7 + T9.C3_C2) / (T10.C12_C4 + T9.C13_C15 + T10.C14_C6 + T9.C15_C16))) * ((C25_C14 * ((T9.C4_C8 + T9.C6_C3) / (T9.C1_C7 + T9.C3_C2))) + (1 - C25_C14) * (T13.C9_C1 + T9.C10_C4))) AS C29_GCONTRATOS,
    ((1 - (LEAST(1,((T9.C1_C7 + T9.C3_C2) / (T10.C12_C4 + T9.C13_C15 + T10.C14_C6 + T9.C15_C16)))) - (T9.C19_C9 + T9.C20_C10)) * (T9.C8_C6 / T9.C7_C5)) AS C30_GBOLSA,
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
        CAR_CARG_PERIODO,
        ID_EMPRESA,
        CAR_1672_ID_MERCADO 
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
--- CONSULTA PARA HALLAR VALOR DEL COMPONENTE T
------------------------------------------------------------------------------------------
SELECT 
    FT78.ID_EMPRESA,
    FT78.CAR_T1669_ID_MERCADO,
    FT78.CAR_T1669_NT_PROP,
    FT78.CAR_CARG_ANO,
    FT78.CAR_CARG_PERIODO,
    FT78.CAR_T1669_TM AS C3_C6,
    FT13.* 
FROM 
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
)FT78,
(
    SELECT CAR_T1673_STN_MO AS C4_C2 
    FROM ENERGIA_CREG_015.CAR_INFORMACION_GENERAL 
    WHERE CAR_CARG_ANO = :ANIO_ARG 
    AND CAR_CARG_PERIODO = :PERIODO_ARG
)FT13 
WHERE FT78.CAR_T1669_NT_PROP = :NTPROP_ARG OR 'TODOS' = :NTPROP_ARG;

------------------------------------------------------------------------------------------
--- CONSULTA PARA HALLAR VALOR DEL COMPONENTE P - COMPONENTE PERDIDAS 015
------------------------------------------------------------------------------------------
SELECT 
    CPTEP.*,
    (C16 + C20 + C15) AS C24,
    (C17 + C21 + C15) AS C25,
    (C18 + C22 + C15) AS C26,
    (C19 + C23 + C15) AS C27 
FROM
(
    SELECT 
        FT9.*,
        CPTE_G.C28_CG AS CG,
        CPTE_T.C5_CT AS CT,
        FT10.*,
        FT11.*,
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
        AND CAR_CARG_PERIODO = :PERIODO_ARG 
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
            CAR_CARG_ANO,
            CAR_CARG_PERIODO,
            ID_EMPRESA,
            CAR_1672_ID_MERCADO,
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
)CPTEP;

------------------------------------------------------------------------------------------
--- CONSULTA PARA OBTENER VALORES DEL COMPONENTE P - COMPONENTE PERDIDAS 097
------------------------------------------------------------------------------------------
SELECT 
    CPTEP.*
FROM
(
    SELECT 
        FT9.*,
        CPTE_G.C28_CG AS CG,
        CPTE_T.C5_CT AS CT,
        FT10.*
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
            CAR_CARG_ANO,
            CAR_CARG_PERIODO,
            ID_EMPRESA,
            CAR_1672_ID_MERCADO,
            CAR_1672_ADR_IPRSTN AS C6_C17,
            CAR_1672_APR_IPRSTN AS C7_C18 
        FROM ENERGIA_CREG_015.CAR_VAR_COSTO_UNT_PS_CU_119_UR
        WHERE 
            CAR_CARG_ANO = :ANIO_ARG 
            AND CAR_CARG_PERIODO = :PERIODO_ARG 
            AND (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
            AND (CAR_1672_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG)
    )FT9
)CPTEP;

------------------------------------------------------------------------------------------
--- CONSULTA PARA HALLAR VALOR DEL COMPONENTE P - COMPONENTE PERDIDAS 097
------------------------------------------------------------------------------------------
SELECT 
    CPTEP.*,
    (C16 + C20) AS C24,
    (C17 + C21) AS C25,
    (C18 + C22) AS C26,
    (C19 + C23) AS C27 
FROM
(
    SELECT 
        FT9.*,
        CPTE_G.C28_CG AS CG,
        CPTE_T.C5_CT AS CT,
        FT10.*,
        FT11.*,
        (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18) AS C9,
        (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18) AS C8,
        FT11.C15_C30 AS C15,
        ((CPTE_G.C28_CG *(FT11.C10_C21 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18))) / (1 - (FT11.C10_C21 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18)))) AS C16,
        (CPTE_T.C5_CT*FT11.C10_C21)/(1-FT11.C10_C21/100) + FT11.C15_C30 AS C20,
        
        ((CPTE_G.C28_CG *(FT11.C11_C20 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18))) / (1 - (FT11.C11_C20 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18)))) AS C17,
        (CPTE_T.C5_CT*FT11.C11_C20)/(1-FT11.C11_C20/100) + FT11.C15_C30 AS C21,
        
        ((CPTE_G.C28_CG *(FT11.C12_C19 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18))) / (1 - (FT11.C12_C19 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18)))) AS C18,
        (CPTE_T.C5_CT*FT11.C12_C19)/(1-FT11.C12_C19/100) + FT11.C15_C30 AS C22,
        
        ((CPTE_G.C28_CG *(FT11.C13_C18 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18))) / (1 - (FT11.C13_C18 / 100 + (FT10.C3_C6 + FT10.C5_C7 + FT9.C7_C18) / (FT10.C2_C4 + FT10.C3_C6 + FT10.C4_C5 + FT10.C5_C7 + FT9.C6_C17 + FT9.C7_C18)))) AS C19,
        (CPTE_T.C5_CT*FT11.C13_C18)/(1-FT11.C13_C18/100) + FT11.C15_C30 AS C23 
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
        AND CAR_CARG_PERIODO = :PERIODO_ARG 
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
            CAR_CARG_ANO,
            CAR_CARG_PERIODO,
            ID_EMPRESA,
            CAR_1672_ID_MERCADO,
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
        SELECT :CAR_T1679_PR4 AS C13_C18,
               :CAR_T1679_PR3 AS C12_C19,
               :CAR_T1679_PR2 AS C11_C20,
               :CAR_T1679_PR1 AS C10_C21,
               :CAR_T1679_CPROG AS C15_C30
        FROM ENERGIA_CREG_015.CAR_INFORMACION_ASIC_LAC_DISTI
        WHERE 
            CAR_CARG_ANO = :ANIO_ARG 
            AND CAR_CARG_PERIODO = :PERIODO_ARG 
            AND (CAR_T1679_ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG)
    )FT11
)CPTEP;

------------------------------------------------------------------------------------------
--- CONSULTA PARA HALLAR VALOR DEL COMPONENTE D - COMPONENTE DISTRIBUCION D015
------------------------------------------------------------------------------------------
SELECT 
    CPTE_D.*,
    C14+(C3/(1-C10/100))+C1+C2+C11 AS C18,
    C14+(C3/(1-C10/100))+C2+C11 AS C19,
    C14+(C3/(1-C10/100))+(C1/2)+C2+C11 AS C20,
    C15+C3+C12 AS C21,
    C16+C4+C13 AS C22,
    C17 AS C23,
    :ANIO_ARG AS ANO,
    :PERIODO_ARG AS PERIODO,
    :EMPRESA_ARG AS EMPRESA,
    :MERCADO_ARG AS MERCADO 
FROM
(
    SELECT 
        FT11.C1, FT11.C2, FT11.C3, FT11.C4,
        FT13.C5,
        FT11.C6, FT11.C7, FT11.C8, FT11.C9,
        FT11.C10, FT11.C11, FT11.C12, FT11.C13,
        C5 / (1 - C6 / 100) AS C14,
        C5 / (1 - C7 / 100) AS C15,
        C5 / (1 - C8 / 100) AS C16,
        C5 / (1 - C9 / 100) AS C17
    FROM
    (
        SELECT 
            CAR_T1679_CDI AS C1,
            CAR_T1679_CDA AS C2,
            CAR_T1679_CD2 AS C3,
            CAR_T1679_CD3 AS C4,
            CAR_T1679_PR1 AS C6,
            CAR_T1679_PR2 AS C7,
            CAR_T1679_PR3 AS C8,
            CAR_T1679_PR4 AS C9,
            CAR_T1679_P1 AS C10,
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
--- CONSULTA PARA OBTENER VALORES DEL COMPONENTE D - COMPONENTE DISTRIBUCION 097
------------------------------------------------------------------------------------------
SELECT 
    :ANIO_ARG AS ANO,
    :PERIODO_ARG AS PERIODO,
    :EMPRESA_ARG AS EMPRESA,
    :MERCADO_ARG AS MERCADO,
    CASE 
        WHEN :EMPRESA_ARG = 2249 THEN CAR_T1673_CD4_NORTE
        ELSE CAR_T1673_CD4_CENTRO_SUR
    END AS C5 
FROM ENERGIA_CREG_015.CAR_INFORMACION_GENERAL 
WHERE 
    CAR_CARG_ANO = :ANIO_ARG 
    AND CAR_CARG_PERIODO = :PERIODO_ARG;

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
        B.CAR_1674_DT_UN_NT1 AS C1,
        B.CAR_1674_DT_UN_NT2 AS C5,
        B.CAR_1674_DT_UN_NT3 AS C6
    FROM ENERGIA_CREG_015.CAR_T1674_INFORMACION_ADD A,
         ENERGIA_CREG_015.CAR_T1674_INFORMACION_ADD B
    WHERE A.CAR_1674_ADD = B.CAR_1674_ADD
    AND TO_NUMBER(A.CAR_1674_ADD) = :ADD_ARG
    AND A.CAR_CARG_ANO = :ANIO_ARG 
    AND A.CAR_CARG_PERIODO = :PERIODO_ARG 
    AND B.CAR_CARG_ANO = :ANIO_ARG 
    AND B.CAR_CARG_PERIODO = :PERIODO_ARG 
) FT12,
(
    SELECT 
        CAR_T1679_CDI AS C2,
        CAR_T1679_DT4
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
    (T10.C1 + T10.C2 + T10.C3 +T9.C4) AS C5,
    (T10.C1 + T10.C2 + T10.C3 +T9.C4) / TC2.C6 AS C7
FROM 
(
    SELECT 
        CAR_T1671_RTCSA AS C1,
        CAR_T1671_VDESV AS C2,
        CAR_T1671_GUATAPE AS C3 
    FROM ENERGIA_CREG_015.CAR_T1671_INFORMACION_ASIC_LAC 
    WHERE CAR_CARG_ANO = :ANIO_ARG 
    and CAR_CARG_PERIODO = :PERIODO_ARG 
    AND (CAR_T1671_ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
) T10, -- VALIDADO
(
    SELECT 
        CAR_1672_AREST AS C4,
        CAR_CARG_ANO,
        CAR_CARG_PERIODO,
        ID_EMPRESA,
        CAR_1672_ID_MERCADO 
    FROM 
        ENERGIA_CREG_015.CAR_VAR_COSTO_UNT_PS_CU_119_UR 
    WHERE 
        CAR_CARG_ANO = :ANIO_ARG 
        AND CAR_CARG_PERIODO = :PERIODO_ARG 
        AND (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
        AND (CAR_1672_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG) 
) T9, -- VALIDADO
(
    SELECT MERCADO, SUM(CAMPO6) AS C6 FROM 
    (
        SELECT 
            TO_NUMBER(SUBSTR(CAR_T1743_MERCADO_NIU, 1, INSTR(CAR_T1743_MERCADO_NIU, '-')-1)) AS MERCADO,
            CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 1) 
            THEN (CAR_T1743_CONS_USUARIO + CAR_T1743_CONS_CDC + CAR_T1743_RFT_CU + CAR_T1743_RFT_CDC) END AS CAMPO6 
        FROM ENERGIA_CREG_015.CAR_T1743_TC2FACTURACION_USU 
        WHERE
            IDENTIFICADOR_EMPRESA = :EMPRESA_ARG
            AND CAR_CARG_PERIODO = :PERIODO_ARG
            AND CAR_CARG_ANO = :ANIO_ARG
            AND TO_NUMBER(SUBSTR(CAR_T1743_MERCADO_NIU, 1, INSTR(CAR_T1743_MERCADO_NIU, '-')-1)) = :MERCADO_ARG
        GROUP BY TO_NUMBER(SUBSTR(CAR_T1743_MERCADO_NIU, 1, INSTR(CAR_T1743_MERCADO_NIU, '-')-1)),
                 CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 1) 
                 THEN (CAR_T1743_CONS_USUARIO + CAR_T1743_CONS_CDC + CAR_T1743_RFT_CU + CAR_T1743_RFT_CDC) END
    )
    GROUP BY MERCADO
) TC2;

------------------------------------------------------------------------------------------
--- CONSULTA PARA HALLAR VALOR DEL COMPONENTE C - COMERCIALIZACION
------------------------------------------------------------------------------------------
--- CONSULTA C ----- VALIDADA ------
----------------------------- ULTIMA CONSULTA -------------------------------
SELECT * FROM 
(
    SELECT CERTIFICADO.QUA_EST_ESTADO, RUPS.ARE_ESP_NOMBRE, FTE2.ID_EMPRESA, FTE2.ID_MERCADO, FECHAS_TIPO_GARANTIA_1, FTE2.TIPO_GARANTIA_1, FECHAS_TIPO_GARANTIA_2, FTE2.TIPO_GARANTIA_2, FECHAS_TIPO_GARANTIA_3, NVL(FTE2.TIPO_GARANTIA_3, 'SIN VALOR') FROM
    (
        SELECT ID_EMPRESA, NVL(TIPO_GARANTIA_1, 'SIN VALOR') AS FECHAS_TIPO_GARANTIA_1, NVL(TIPO_GARANTIA_2, 'SIN VALOR') AS FECHAS_TIPO_GARANTIA_2, NVL(TIPO_GARANTIA_3, 'SIN VALOR') AS FECHAS_TIPO_GARANTIA_3 FROM 
        (
            SELECT ID_EMPRESA, CAR_T1667_TIPO_GARANTIA, VALOR FROM 
            (
                SELECT 
                    ID_EMPRESA,
                    CAR_T1667_TIPO_GARANTIA,
                    CAR_T1667_MES_RECUPERACION,
                    CAR_CARG_PERIODO,
                    CASE WHEN CAR_T1667_MES_RECUPERACION > CAR_CARG_PERIODO THEN 'CUMPLE' ELSE 'NO CUMPLE' END AS VALOR
                FROM 
                    ENERGIA_CREG_015.CAR_GARANTIA_FINANCIERA 
                WHERE 
                    CAR_CARG_ANO = :ANIO_ARG 
                    AND CAR_CARG_PERIODO = :PERIODO_ARG 
                    AND (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
                    AND CAR_T1667_TIPO_GARANTIA IN (1, 2, 3) 
            )
        )
        PIVOT 
        (
            MAX(VALOR) -- Campo agrupado pivotado 
            FOR 
                CAR_T1667_TIPO_GARANTIA -- Campo cuyo contenido pasan a ser columnas 
            IN ('1' AS TIPO_GARANTIA_1, '2' AS TIPO_GARANTIA_2, '3' AS TIPO_GARANTIA_3) -- Nuevas columnas
        )
    ) FECHAS,
    (
        SELECT TPG3.ID_EMPRESA, TPG3.ID_MERCADO, TPG1_2.TIPO_GARANTIA_1, TPG1_2.TIPO_GARANTIA_2, TPG3.TIPO_GARANTIA_3 FROM 
        (
            SELECT ID_EMPRESA, NVL(TO_CHAR(TIPO_GARANTIA_1), 0) AS TIPO_GARANTIA_1, NVL(TO_CHAR(TIPO_GARANTIA_2), 0) AS TIPO_GARANTIA_2 FROM 
            (
                SELECT ID_EMPRESA, CAR_T1667_TIPO_GARANTIA, VALOR FROM 
                (
                    SELECT 
                        ID_EMPRESA,
                        CAR_T1667_TIPO_GARANTIA,
                        NVL(CASE WHEN CAR_T1667_TIPO_GARANTIA = 1 THEN SUM(CAR_T1667_COSTO_A_RECUPERAR) ELSE SUM(CAR_T1667_COSTO_A_RECUPERAR) END, 0) AS VALOR 
                    FROM 
                        ENERGIA_CREG_015.CAR_GARANTIA_FINANCIERA 
                    WHERE 
                        CAR_CARG_ANO = :ANIO_ARG 
                        AND CAR_CARG_PERIODO = :PERIODO_ARG 
                        AND (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
                        AND CAR_T1667_TIPO_GARANTIA IN (1, 2) 
                    GROUP BY ID_EMPRESA, CAR_T1667_TIPO_GARANTIA
                )
            )
            PIVOT 
            (
                MAX(VALOR) -- Campo agrupado pivotado 
                FOR 
                    CAR_T1667_TIPO_GARANTIA -- Campo cuyo contenido pasan a ser columnas 
                IN ('1' AS TIPO_GARANTIA_1, '2' AS TIPO_GARANTIA_2) -- Nuevas columnas
            )
        ) TPG1_2,
        (
            SELECT MERCADOS.ID_MERCADO, MERCADOS.NOM_MERCADO, GRT3.* FROM -- PROBADO CON EMPRESA 2322 | MERCADO 160 
            (
                SELECT ID_EMPRESA, RUPS.ARE_ESP_SECUE, RUPS.ARE_ESP_NOMBRE, GARANTIAS3.CAR_T1667_NIT_BENEFICIARIO, GARANTIAS3.TIPO_GARANTIA_3 FROM 
                (
                    SELECT ID_EMPRESA, CAR_T1667_NIT_BENEFICIARIO, NVL(TO_CHAR(TIPO_GARANTIA_1), 0) AS TIPO_GARANTIA_1, NVL(TO_CHAR(TIPO_GARANTIA_2), 0) AS TIPO_GARANTIA_2, NVL(TO_CHAR(TIPO_GARANTIA_3), 0) AS TIPO_GARANTIA_3 FROM 
                    (
                        SELECT ID_EMPRESA, CAR_T1667_NIT_BENEFICIARIO, CAR_T1667_TIPO_GARANTIA, VALOR FROM 
                        (
                            SELECT 
                                ID_EMPRESA,
                                CAR_T1667_NIT_BENEFICIARIO,
                                CAR_T1667_TIPO_GARANTIA,
                                NVL(SUM(CAR_T1667_COSTO_A_RECUPERAR), 0) AS VALOR 
                            FROM 
                                ENERGIA_CREG_015.CAR_GARANTIA_FINANCIERA 
                            WHERE 
                                CAR_CARG_ANO = :ANIO_ARG 
                                AND CAR_CARG_PERIODO = :PERIODO_ARG 
                                AND (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
                                --AND CAR_T1667_TIPO_GARANTIA IN (1, 2) 
                            GROUP BY ID_EMPRESA, CAR_T1667_NIT_BENEFICIARIO, CAR_T1667_TIPO_GARANTIA
                        )
                    )
                    PIVOT 
                    (
                        MAX(VALOR) -- Campo agrupado pivotado 
                        FOR 
                            CAR_T1667_TIPO_GARANTIA -- Campo cuyo contenido pasan a ser columnas 
                        IN ('1' AS TIPO_GARANTIA_1, '2' AS TIPO_GARANTIA_2, '3' AS TIPO_GARANTIA_3) -- Nuevas columnas
                    )
                ) GARANTIAS3,
                (
                    SELECT ARE_ESP_NOMBRE, ARE_ESP_SECUE, ARE_ESP_NIT FROM RUPS.ARE_ESP_EMPRESAS
                ) RUPS
                WHERE GARANTIAS3.CAR_T1667_NIT_BENEFICIARIO = RUPS.ARE_ESP_NIT
            ) GRT3,
            (
                SELECT 
                    DISTINCT ID_MERCADO,
                    ARE_ESP_SECUE,
                    NOM_MERCADO,
                    ESTADO 
                FROM 
                    CARG_COMERCIAL_E.MERCADO_EMPRESA 
                WHERE 
                    ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG 
                    AND ESTADO = 'A'
                    AND NOM_MERCADO NOT LIKE '%Mercado Prueba%' 
                    AND NOM_MERCADO NOT LIKE '%Mercado de Prueba%'
                UNION
                SELECT 
                    20481 AS ID_MERCADO,
                    20481 AS ARE_ESP_SECUE,
                    'XM COMPAÑIA DE EXPERTOS EN MERCADOS S.A. E.S.P.' AS NOM_MERCADO,
                    'A' AS ESTADO 
                FROM DUAL
            ) MERCADOS
            WHERE GRT3.ARE_ESP_SECUE = MERCADOS.ARE_ESP_SECUE
        ) TPG3
        WHERE TPG1_2.ID_EMPRESA = TPG3.ID_EMPRESA
    ) FTE2,
    (
        SELECT ARE_ESP_NOMBRE, ARE_ESP_SECUE, ARE_ESP_NIT FROM RUPS.ARE_ESP_EMPRESAS
    ) RUPS,
    (
        SELECT 
            CAR_TIAR_CODIGO,
            EXTRACT(MONTH FROM QUA_EST_FCHCERT) AS MES_CERTIFICADO,
            EXTRACT(YEAR FROM QUA_EST_FCHCERT) ANO_CERTIFICADO,
            QUA_EST_ESTADO 
        FROM CALIDAD_SUI.FAC_QUA_ESTADO 
        WHERE 
            CAR_TIAR_CODIGO = '1667'
            AND ARE_ESP_SECUE = :EMPRESA_ARG
            AND EXTRACT(YEAR FROM QUA_EST_FCHCERT) = :ANIO_ARG 
            AND EXTRACT(MONTH FROM QUA_EST_FCHCERT) = :PERIODO_ARG
    ) CERTIFICADO
    WHERE FTE2.ID_EMPRESA = RUPS.ARE_ESP_SECUE
) FT2,
(
    SELECT
         DISTINCT CAR_T1668_ID_MERCADO, 
         MAX(CAR_T1668_TARIFA_CFJM) AS C6 --CAR_T1668_TARIFA_CFJM AS C6 --- REVISAR CON DIEGO Y KELLY | APARECEN ESTRATOS
    FROM 
        ENERGIA_CREG_015.CAR_TARIFAS_PUBLICADAS
    WHERE 
        CAR_CARG_ANO = :ANIO_ARG 
        AND CAR_CARG_PERIODO = :PERIODO_ARG 
        AND (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
        AND (CAR_T1668_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG)
    GROUP BY CAR_T1668_ID_MERCADO,
             CAR_T1668_TARIFA_CFJM
)FT3, -- TENER EN CUENTA QUE ESTE FORMATO TIENE LOS CAMPOS DE MES Y AÑO CORREGIDO COM FT7
(
    SELECT 
        CAR_1672_CFJ AS C1,
        CAR_1672_RCT AS C13,
        CAR_1672_RCAE AS C14,
        CAR_1672_IFSSRI AS C15,
        CAR_1672_IFOES AS C16,
        CASE WHEN CAR_1672_BALANCE_SUBSIDIOS = 'D' THEN 'DEFICITARIO' ELSE 'SUPERAVITARIO' END AS C28,
        CAR_1672_ANIO AS C29,
        CAR_1672_TRIM AS C30,
        CAR_1672_MG_TRIM AS C31,
        CAR_1672_SUB1 AS C32,
        CAR_1672_R1 AS C36,
        CAR_1672_N AS C34,
        CAR_1672_SUB2 AS C33,
        CAR_1672_R2 AS C37,
        CAR_1672_M AS C35,
        CAR_1672_CREG AS C47,
        CAR_1672_SSPD AS C48,
        CASE WHEN CAR_1672_ACTIVIDAD = 'CP' THEN 'COMERCIALIZADOR PURO' ELSE 'COMERCIALIZADOR INTEGRADO' END AS C44,
        CAR_CARG_ANO,
        CAR_CARG_PERIODO,
        ID_EMPRESA,
        CAR_1672_ID_MERCADO 
    FROM 
        ENERGIA_CREG_015.CAR_VAR_COSTO_UNT_PS_CU_119_UR 
    WHERE 
        CAR_CARG_ANO = :ANIO_ARG 
        AND CAR_CARG_PERIODO = :PERIODO_ARG 
        AND (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
        AND (CAR_1672_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG) 
) T9, -- VALIDADO
(
    SELECT 
        CAR_T1671_CND AS C52,
        CAR_T1671_SIC AS C53
    FROM ENERGIA_CREG_015.CAR_T1671_INFORMACION_ASIC_LAC 
    WHERE CAR_CARG_ANO = :ANIO_ARG 
    and CAR_CARG_PERIODO = :PERIODO_ARG 
    AND (CAR_T1671_ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
) T10,
(
    SELECT 
        ID_EMPRESA,
        CAR_T1669_ID_MERCADO,
        CAR_T1669_NT_PROP,
        CAR_T1669_GM AS C7,
        CAR_T1669_TM AS C8,
        CAR_T1669_PRNM AS C9,
        CAR_T1669_DNM AS C10,
        CAR_T1669_RM AS C11 
    FROM ENERGIA_CREG_015.CAR_COSTO_UNITARIO_119_UR 
    WHERE 
        (ID_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) 
        AND (CAR_T1669_ID_MERCADO = :MERCADO_ARG OR 0 = :MERCADO_ARG) 
        AND CAR_CARG_ANO = :ANIO_ARG 
        AND CAR_CARG_PERIODO = :PERIODO_ARG 
        AND CAR_T1676_ANIO_CORREG IS NULL
        --AND CAR_T1669_NT_PROP = :NTPROP_ARG
)FT7,
(
    SELECT
        TO_NUMBER(SUBSTR(CAR_T1743_MERCADO_NIU, 1, INSTR(CAR_T1743_MERCADO_NIU, '-')-1)) AS MERCADO,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 1) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END AS C20,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 3) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END AS C22,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 5) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END AS C24,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 2) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END AS C21,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 4) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END AS C23,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 6) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END AS C25,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END AS C55
    FROM ENERGIA_CREG_015.CAR_T1743_TC2FACTURACION_USU 
    WHERE
        IDENTIFICADOR_EMPRESA = :EMPRESA_ARG
        AND CAR_CARG_PERIODO = :PERIODO_ARG
        AND CAR_CARG_ANO = :ANIO_ARG
        AND TO_NUMBER(SUBSTR(CAR_T1743_MERCADO_NIU, 1, INSTR(CAR_T1743_MERCADO_NIU, '-')-1)) = :MERCADO_ARG
    GROUP BY TO_NUMBER(SUBSTR(CAR_T1743_MERCADO_NIU, 1, INSTR(CAR_T1743_MERCADO_NIU, '-')-1)),
    CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 1) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 3) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 5) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 2) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 4) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1 AND CAR_T1743_TIPO_USU_RC = 6) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) 
        END,
        CASE WHEN (CAR_T1743_TIPO_FACT = 1) THEN 
        (CAR_T1743_CONS_USUARIO + 
         CAR_T1743_CONS_CDC + 
         CAR_T1743_RFT_CU + 
         CAR_T1743_RFT_CDC) END
)FTC2;
