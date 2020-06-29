----------------------------------------------------------------------------------------
-- SCRIPT PARA OBTENER EMPRESAS DE ENERGIA
----------------------------------------------------------------------------------------
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
             EMP.ARE_ESP_SECUE_CREG
    UNION
    SELECT ARE_ESP_SECUE,
           ARE_ESP_NOMBRE,
           'ENERGIA' SERVICIO 
    FROM
        RUPS.ARE_ESP_EMPRESAS
    WHERE ARE_ESP_SECUE = 44278
)
ORDER BY ARE_ESP_NOMBRE ASC;