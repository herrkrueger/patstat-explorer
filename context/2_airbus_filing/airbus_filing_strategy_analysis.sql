-- =============================================================================
-- AIRBUS Anmeldestrategie-Analyse (PATSTAT BigQuery)
-- =============================================================================
-- Erstellt: 2025-02-06
-- Zweck: Umfassende Analyse der Patentstrategie von Airbus über 10+ Jahre
-- Zielgruppe: PATLIB-Training, PIZnet-Seminar, Consulting-Demo
-- Ausführung: EPO Technology Intelligence Platform (TIP) oder BigQuery
-- =============================================================================
--
-- WICHTIG: Airbus hat viele Namensvarianten in PATSTAT:
--   - AIRBUS (Muttergesellschaft)
--   - AIRBUS OPERATIONS (Flugzeugbau)
--   - AIRBUS DEFENCE AND SPACE (ehemals EADS/Cassidian)
--   - AIRBUS HELICOPTERS (ehemals Eurocopter)
--   - AIRBUS GROUP (Holdingname 2014-2017)
--   - Historische Namen: EADS, EUROCOPTER, ASTRIUM, CASSIDIAN
--
-- Die Queries nutzen han_name (harmonisierte Namen) UND person_name
-- für maximale Abdeckung.
-- =============================================================================


-- =============================================================================
-- QUERY A: Airbus Namensvarianten identifizieren
-- =============================================================================
/*
BUSINESS QUESTION:
Welche Namensvarianten von Airbus existieren in PATSTAT und wie viele 
Anmeldungen hat jede Variante?

STAKEHOLDER: Alle - Grundlage für weitere Analysen
ERKLÄRUNG: Erste Exploration, um die Anmelderlandschaft zu verstehen.
Airbus hat durch Umbenennungen und Tochtergesellschaften viele Varianten.
*/

SELECT 
    p.person_name,
    p.han_name,
    p.psn_name,
    p.psn_sector,
    p.person_ctry_code,
    COUNT(DISTINCT pa.appln_id) AS applications,
    MIN(a.appln_filing_year) AS first_filing_year,
    MAX(a.appln_filing_year) AS last_filing_year
FROM tls206_person p
JOIN tls207_pers_appln pa ON p.person_id = pa.person_id
JOIN tls201_appln a ON pa.appln_id = a.appln_id
WHERE pa.applt_seq_nr > 0
  AND (
    LOWER(p.person_name) LIKE '%airbus%'
    OR LOWER(p.han_name) LIKE '%airbus%'
    OR LOWER(p.person_name) LIKE '%eurocopter%'
    OR LOWER(p.person_name) LIKE '%astrium%'
    OR LOWER(p.person_name) LIKE '%cassidian%'
    OR (LOWER(p.person_name) LIKE '%eads%' 
        AND LOWER(p.person_name) NOT LIKE '%beads%'
        AND LOWER(p.person_name) NOT LIKE '%leads%'
        AND LOWER(p.person_name) NOT LIKE '%heads%')
  )
  AND a.appln_filing_year >= 2000
GROUP BY p.person_name, p.han_name, p.psn_name, p.psn_sector, p.person_ctry_code
HAVING COUNT(DISTINCT pa.appln_id) >= 5
ORDER BY applications DESC
LIMIT 100;


-- =============================================================================
-- QUERY B: Anmeldetrend Airbus gesamt (2014-2024)
-- =============================================================================
/*
BUSINESS QUESTION:
Wie hat sich die gesamte Patentanmeldeaktivität von Airbus in den letzten 
10 Jahren entwickelt? Steigt, sinkt oder stagniert das Portfolio?

STAKEHOLDER: IP-Strategie, Management, Investoren-Kommunikation

ERKLÄRUNG: Zählt DOCDB-Familien (nicht Einzelanmeldungen), um 
Mehrfacheinreichungen desselben Schutzrechts zu vermeiden.
Unterscheidet nach Geschäftsbereichen (Operations, Defence, Helicopters).
*/

WITH airbus_apps AS (
    SELECT DISTINCT
        a.appln_id,
        a.docdb_family_id,
        a.appln_filing_year,
        a.appln_auth,
        a.granted,
        a.docdb_family_size,
        CASE
            WHEN LOWER(p.person_name) LIKE '%airbus operations%' THEN 'Airbus Operations (Flugzeugbau)'
            WHEN LOWER(p.person_name) LIKE '%airbus defence%' 
              OR LOWER(p.person_name) LIKE '%airbus defense%' THEN 'Airbus Defence & Space'
            WHEN LOWER(p.person_name) LIKE '%airbus helicopter%'
              OR LOWER(p.person_name) LIKE '%eurocopter%' THEN 'Airbus Helicopters'
            WHEN LOWER(p.person_name) LIKE '%airbus group%' THEN 'Airbus Group (Holding)'
            WHEN LOWER(p.person_name) LIKE '%airbus s%a%s%' THEN 'Airbus SAS (Zentrale)'
            WHEN LOWER(p.person_name) LIKE '%astrium%' THEN 'Astrium (→ Defence & Space)'
            WHEN LOWER(p.person_name) LIKE '%cassidian%' THEN 'Cassidian (→ Defence & Space)'
            WHEN LOWER(p.person_name) LIKE '%eads%' THEN 'EADS (→ Airbus Group)'
            ELSE 'Airbus (andere/unspezifisch)'
        END AS business_unit
    FROM tls201_appln a
    JOIN tls207_pers_appln pa ON a.appln_id = pa.appln_id
    JOIN tls206_person p ON pa.person_id = p.person_id
    WHERE pa.applt_seq_nr > 0
      AND a.appln_filing_year BETWEEN 2014 AND 2024
      AND (
        LOWER(p.person_name) LIKE '%airbus%'
        OR LOWER(p.person_name) LIKE '%eurocopter%'
        OR LOWER(p.person_name) LIKE '%astrium%'
        OR LOWER(p.person_name) LIKE '%cassidian%'
        OR (LOWER(p.person_name) LIKE '%eads%' 
            AND LOWER(p.person_name) NOT LIKE '%beads%'
            AND LOWER(p.person_name) NOT LIKE '%leads%'
            AND LOWER(p.person_name) NOT LIKE '%heads%')
      )
)

SELECT 
    appln_filing_year,
    business_unit,
    COUNT(DISTINCT docdb_family_id) AS patent_families,
    COUNT(DISTINCT appln_id) AS total_applications,
    COUNT(DISTINCT CASE WHEN granted = 'Y' THEN appln_id END) AS granted_applications,
    ROUND(AVG(docdb_family_size), 1) AS avg_family_size
FROM airbus_apps
GROUP BY appln_filing_year, business_unit
ORDER BY appln_filing_year, patent_families DESC;


-- =============================================================================
-- QUERY C: Geographische Anmeldestrategie
-- =============================================================================
/*
BUSINESS QUESTION:
In welchen Ländern/Regionen meldet Airbus seine Patente an?
Hat sich die geographische Strategie verändert (z.B. mehr China)?

STAKEHOLDER: IP-Portfolio-Management, Internationale Expansion

ERKLÄRUNG: Vergleicht die Anmeldebehörden (appln_auth) zwischen zwei 
Zeiträumen: 2014-2018 (früh) vs. 2019-2024 (spät).
Zeigt Verschiebungen in der geographischen Priorität.
*/

WITH airbus_apps AS (
    SELECT DISTINCT
        a.appln_id,
        a.docdb_family_id,
        a.appln_auth,
        a.appln_filing_year,
        CASE 
            WHEN a.appln_filing_year BETWEEN 2014 AND 2018 THEN 'Periode 1 (2014-2018)'
            WHEN a.appln_filing_year BETWEEN 2019 AND 2024 THEN 'Periode 2 (2019-2024)'
        END AS period
    FROM tls201_appln a
    JOIN tls207_pers_appln pa ON a.appln_id = pa.appln_id
    JOIN tls206_person p ON pa.person_id = p.person_id
    WHERE pa.applt_seq_nr > 0
      AND a.appln_filing_year BETWEEN 2014 AND 2024
      AND (
        LOWER(p.person_name) LIKE '%airbus%'
        OR LOWER(p.person_name) LIKE '%eurocopter%'
        OR LOWER(p.person_name) LIKE '%astrium%'
      )
),

geo_by_period AS (
    SELECT
        period,
        appln_auth,
        COUNT(DISTINCT docdb_family_id) AS families,
        COUNT(DISTINCT appln_id) AS applications
    FROM airbus_apps
    WHERE period IS NOT NULL
    GROUP BY period, appln_auth
    HAVING COUNT(DISTINCT appln_id) >= 10
)

SELECT 
    appln_auth,
    CASE 
        WHEN appln_auth = 'EP' THEN 'Europäisches Patentamt'
        WHEN appln_auth = 'US' THEN 'US Patent Office'
        WHEN appln_auth = 'CN' THEN 'China (CNIPA)'
        WHEN appln_auth = 'FR' THEN 'Frankreich (INPI)'
        WHEN appln_auth = 'DE' THEN 'Deutschland (DPMA)'
        WHEN appln_auth = 'WO' THEN 'PCT (WIPO)'
        WHEN appln_auth = 'JP' THEN 'Japan (JPO)'
        WHEN appln_auth = 'KR' THEN 'Südkorea (KIPO)'
        WHEN appln_auth = 'IN' THEN 'Indien'
        WHEN appln_auth = 'BR' THEN 'Brasilien'
        ELSE appln_auth
    END AS authority_name,
    MAX(CASE WHEN period = 'Periode 1 (2014-2018)' THEN applications END) AS apps_2014_2018,
    MAX(CASE WHEN period = 'Periode 2 (2019-2024)' THEN applications END) AS apps_2019_2024,
    MAX(CASE WHEN period = 'Periode 1 (2014-2018)' THEN families END) AS families_2014_2018,
    MAX(CASE WHEN period = 'Periode 2 (2019-2024)' THEN families END) AS families_2019_2024,
    ROUND(
        SAFE_DIVIDE(
            MAX(CASE WHEN period = 'Periode 2 (2019-2024)' THEN applications END) - 
            MAX(CASE WHEN period = 'Periode 1 (2014-2018)' THEN applications END),
            MAX(CASE WHEN period = 'Periode 1 (2014-2018)' THEN applications END)
        ) * 100, 1
    ) AS change_percent
FROM geo_by_period
GROUP BY appln_auth
ORDER BY COALESCE(
    MAX(CASE WHEN period = 'Periode 2 (2019-2024)' THEN applications END), 0
) DESC;


-- =============================================================================
-- QUERY D: Technologiefelder und Verschiebungen
-- =============================================================================
/*
BUSINESS QUESTION:
In welchen Technologiefeldern patentiert Airbus am stärksten?
Gibt es erkennbare Verschiebungen (z.B. mehr Digitalisierung, Drohnen, 
Nachhaltigkeit/Wasserstoff)?

STAKEHOLDER: R&D-Strategie, Technologie-Scouting

ERKLÄRUNG: Nutzt tls230_appln_techn_field für die Zuordnung zu den 
35 WIPO-Technologiefeldern. Vergleicht zwei Perioden.
*/

WITH airbus_apps AS (
    SELECT DISTINCT
        a.appln_id,
        a.appln_filing_year,
        CASE 
            WHEN a.appln_filing_year BETWEEN 2014 AND 2018 THEN 'early'
            WHEN a.appln_filing_year BETWEEN 2019 AND 2024 THEN 'recent'
        END AS period
    FROM tls201_appln a
    JOIN tls207_pers_appln pa ON a.appln_id = pa.appln_id
    JOIN tls206_person p ON pa.person_id = p.person_id
    WHERE pa.applt_seq_nr > 0
      AND a.appln_filing_year BETWEEN 2014 AND 2024
      AND LOWER(p.person_name) LIKE '%airbus%'
),

tech_by_period AS (
    SELECT
        tfi.techn_sector,
        tfi.techn_field,
        tf.techn_field_nr,
        aa.period,
        COUNT(DISTINCT aa.appln_id) AS applications
    FROM airbus_apps aa
    JOIN tls230_appln_techn_field tf ON aa.appln_id = tf.appln_id
    JOIN tls901_techn_field_ipc tfi ON tf.techn_field_nr = tfi.techn_field_nr
    WHERE aa.period IS NOT NULL
    GROUP BY tfi.techn_sector, tfi.techn_field, tf.techn_field_nr, aa.period
)

SELECT 
    techn_sector,
    techn_field,
    MAX(CASE WHEN period = 'early' THEN applications END) AS apps_2014_2018,
    MAX(CASE WHEN period = 'recent' THEN applications END) AS apps_2019_2024,
    ROUND(
        SAFE_DIVIDE(
            MAX(CASE WHEN period = 'recent' THEN applications END) - 
            MAX(CASE WHEN period = 'early' THEN applications END),
            MAX(CASE WHEN period = 'early' THEN applications END)
        ) * 100, 1
    ) AS growth_percent
FROM tech_by_period
GROUP BY techn_sector, techn_field
HAVING COALESCE(MAX(CASE WHEN period = 'early' THEN applications END), 0) +
       COALESCE(MAX(CASE WHEN period = 'recent' THEN applications END), 0) >= 20
ORDER BY growth_percent DESC NULLS LAST;


-- =============================================================================
-- QUERY E: IPC-Hauptklassen Top 20 mit Trend
-- =============================================================================
/*
BUSINESS QUESTION:
Welche IPC-Klassen dominieren bei Airbus und welche wachsen am stärksten?
Dies zeigt konkret, in welchen Technologien investiert wird.

STAKEHOLDER: Patentabteilung, Technologie-Benchmarking

ERKLÄRUNG: Extrahiert IPC-Hauptklassen (4 Zeichen, z.B. B64C = Flugzeuge)
und vergleicht Perioden. B64 (Luftfahrt) sollte dominieren, aber 
Verschiebungen zu G06 (Computing), H04 (Kommunikation) zeigen Digitalisierung.
*/

WITH airbus_apps AS (
    SELECT DISTINCT
        a.appln_id,
        a.appln_filing_year,
        CASE 
            WHEN a.appln_filing_year BETWEEN 2014 AND 2018 THEN 'early'
            WHEN a.appln_filing_year BETWEEN 2019 AND 2024 THEN 'recent'
        END AS period
    FROM tls201_appln a
    JOIN tls207_pers_appln pa ON a.appln_id = pa.appln_id
    JOIN tls206_person p ON pa.person_id = p.person_id
    WHERE pa.applt_seq_nr > 0
      AND a.appln_filing_year BETWEEN 2014 AND 2024
      AND LOWER(p.person_name) LIKE '%airbus%'
),

ipc_analysis AS (
    SELECT
        SUBSTR(ipc.ipc_class_symbol, 1, 4) AS ipc_main_class,
        aa.period,
        COUNT(DISTINCT aa.appln_id) AS applications
    FROM airbus_apps aa
    JOIN tls209_appln_ipc ipc ON aa.appln_id = ipc.appln_id
    WHERE aa.period IS NOT NULL
    GROUP BY SUBSTR(ipc.ipc_class_symbol, 1, 4), aa.period
)

SELECT 
    ipc_main_class,
    CASE ipc_main_class
        WHEN 'B64C' THEN 'Flugzeuge/Hubschrauber'
        WHEN 'B64D' THEN 'Flugzeugausrüstung'
        WHEN 'B64F' THEN 'Flughafeneinrichtungen'
        WHEN 'B64G' THEN 'Kosmonautik'
        WHEN 'F02C' THEN 'Gasturbinen'
        WHEN 'F02K' THEN 'Strahltriebwerke'
        WHEN 'G01S' THEN 'Radar/Navigation'
        WHEN 'G06F' THEN 'Datenverarbeitung'
        WHEN 'G06N' THEN 'KI/Neuronale Netze'
        WHEN 'H04L' THEN 'Datenübertragung'
        WHEN 'H04B' THEN 'Nachrichtentechnik'
        WHEN 'B29C' THEN 'Kunststoffverarbeitung (Composite)'
        WHEN 'G05B' THEN 'Steuerungstechnik'
        WHEN 'G05D' THEN 'Regelungstechnik'
        WHEN 'H01Q' THEN 'Antennen'
        WHEN 'B32B' THEN 'Schichtwerkstoffe'
        WHEN 'F16B' THEN 'Befestigungselemente'
        WHEN 'C08J' THEN 'Polymer-Verarbeitung'
        WHEN 'H02J' THEN 'Energieverteilung'
        WHEN 'Y02T' THEN 'Nachhaltiger Transport'
        ELSE ipc_main_class
    END AS description,
    COALESCE(MAX(CASE WHEN period = 'early' THEN applications END), 0) AS apps_2014_2018,
    COALESCE(MAX(CASE WHEN period = 'recent' THEN applications END), 0) AS apps_2019_2024,
    COALESCE(MAX(CASE WHEN period = 'early' THEN applications END), 0) +
    COALESCE(MAX(CASE WHEN period = 'recent' THEN applications END), 0) AS total,
    ROUND(
        SAFE_DIVIDE(
            MAX(CASE WHEN period = 'recent' THEN applications END) - 
            MAX(CASE WHEN period = 'early' THEN applications END),
            MAX(CASE WHEN period = 'early' THEN applications END)
        ) * 100, 1
    ) AS growth_percent
FROM ipc_analysis
GROUP BY ipc_main_class
HAVING COALESCE(MAX(CASE WHEN period = 'early' THEN applications END), 0) +
       COALESCE(MAX(CASE WHEN period = 'recent' THEN applications END), 0) >= 20
ORDER BY total DESC
LIMIT 25;


-- =============================================================================
-- QUERY F: Erteilungsquote und Time-to-Grant
-- =============================================================================
/*
BUSINESS QUESTION:
Wie erfolgreich ist Airbus bei der Patentdurchsetzung?
Wie lange dauert es bis zur Erteilung bei verschiedenen Ämtern?

STAKEHOLDER: Patent Prosecution, Portfolio-Management

ERKLÄRUNG: Nutzt publn_first_grant = 'Y' (zuverlässiger als Legal Events).
Time-to-Grant = Erstveröffentlichung der Erteilung minus Anmeldedatum.
*/

WITH airbus_apps AS (
    SELECT DISTINCT
        a.appln_id,
        a.appln_auth,
        a.appln_filing_date,
        a.appln_filing_year,
        a.granted
    FROM tls201_appln a
    JOIN tls207_pers_appln pa ON a.appln_id = pa.appln_id
    JOIN tls206_person p ON pa.person_id = p.person_id
    WHERE pa.applt_seq_nr > 0
      AND a.appln_filing_year BETWEEN 2014 AND 2021  -- bis 2021 für genug Grant-Zeit
      AND LOWER(p.person_name) LIKE '%airbus%'
      AND a.appln_auth IN ('EP', 'US', 'CN', 'FR', 'DE', 'JP', 'KR')
),

grant_info AS (
    SELECT 
        aa.appln_id,
        aa.appln_auth,
        aa.appln_filing_date,
        aa.appln_filing_year,
        aa.granted,
        MIN(CASE WHEN pub.publn_first_grant = 'Y' THEN pub.publn_date END) AS grant_date
    FROM airbus_apps aa
    LEFT JOIN tls211_pat_publn pub ON aa.appln_id = pub.appln_id
    GROUP BY aa.appln_id, aa.appln_auth, aa.appln_filing_date, aa.appln_filing_year, aa.granted
)

SELECT 
    appln_auth,
    COUNT(*) AS total_applications,
    COUNT(CASE WHEN granted = 'Y' THEN 1 END) AS granted,
    ROUND(COUNT(CASE WHEN granted = 'Y' THEN 1 END) * 100.0 / COUNT(*), 1) AS grant_rate_pct,
    ROUND(AVG(
        CASE WHEN grant_date IS NOT NULL AND grant_date > appln_filing_date
        THEN DATE_DIFF(grant_date, appln_filing_date, DAY) / 365.25
        END
    ), 1) AS avg_years_to_grant,
    ROUND(APPROX_QUANTILES(
        CASE WHEN grant_date IS NOT NULL AND grant_date > appln_filing_date
        THEN DATE_DIFF(grant_date, appln_filing_date, DAY) / 365.25
        END, 2)[OFFSET(1)], 1) AS median_years_to_grant
FROM grant_info
GROUP BY appln_auth
ORDER BY total_applications DESC;


-- =============================================================================
-- QUERY G: Co-Applicants und Kooperationsstrategie
-- =============================================================================
/*
BUSINESS QUESTION:
Mit wem kooperiert Airbus bei Patentanmeldungen?
Gibt es Trends zu mehr oder weniger Ko-Anmeldungen?

STAKEHOLDER: Open Innovation, Forschungskooperationen

ERKLÄRUNG: Identifiziert Ko-Anmelder bei Airbus-Patenten.
nb_applicants > 1 zeigt Ko-Anmeldungen.
*/

WITH airbus_coapplications AS (
    SELECT DISTINCT
        a.appln_id,
        a.appln_filing_year,
        a.nb_applicants,
        p.person_name AS co_applicant,
        p.psn_sector AS co_sector,
        p.person_ctry_code AS co_country
    FROM tls201_appln a
    JOIN tls207_pers_appln pa ON a.appln_id = pa.appln_id
    JOIN tls206_person p ON pa.person_id = p.person_id
    WHERE pa.applt_seq_nr > 0
      AND a.nb_applicants > 1
      AND a.appln_filing_year BETWEEN 2014 AND 2024
      AND NOT LOWER(p.person_name) LIKE '%airbus%'  -- Nur den Partner zeigen
      AND a.appln_id IN (
          -- Nur Anmeldungen wo Airbus auch Anmelder ist
          SELECT pa2.appln_id 
          FROM tls207_pers_appln pa2
          JOIN tls206_person p2 ON pa2.person_id = p2.person_id
          WHERE pa2.applt_seq_nr > 0
            AND LOWER(p2.person_name) LIKE '%airbus%'
      )
)

SELECT 
    co_applicant,
    co_sector,
    co_country,
    COUNT(DISTINCT appln_id) AS joint_applications,
    MIN(appln_filing_year) AS first_cooperation,
    MAX(appln_filing_year) AS last_cooperation,
    COUNT(DISTINCT appln_filing_year) AS active_years
FROM airbus_coapplications
GROUP BY co_applicant, co_sector, co_country
HAVING COUNT(DISTINCT appln_id) >= 3
ORDER BY joint_applications DESC
LIMIT 30;


-- =============================================================================
-- QUERY H: Patent-Familiengröße als Strategieindikator
-- =============================================================================
/*
BUSINESS QUESTION:
Wie breit schützt Airbus seine Erfindungen international?
Steigt die durchschnittliche Familiengröße (= mehr Länder pro Erfindung)?

STAKEHOLDER: IP-Budget-Planung, Internationalisierung

ERKLÄRUNG: Die DOCDB-Familiengröße zeigt, in wie vielen Ländern eine 
Erfindung geschützt wird. Größere Familien = höhere strategische Bedeutung.
*/

WITH airbus_families AS (
    SELECT DISTINCT
        a.docdb_family_id,
        a.appln_filing_year,
        a.docdb_family_size
    FROM tls201_appln a
    JOIN tls207_pers_appln pa ON a.appln_id = pa.appln_id
    JOIN tls206_person p ON pa.person_id = p.person_id
    WHERE pa.applt_seq_nr > 0
      AND a.appln_filing_year BETWEEN 2014 AND 2024
      AND LOWER(p.person_name) LIKE '%airbus%'
      AND a.docdb_family_id > 0
      -- Nur Erstanmeldung pro Familie für korrekte Zuordnung
      AND a.appln_id = a.earliest_filing_id
)

SELECT 
    appln_filing_year,
    COUNT(DISTINCT docdb_family_id) AS unique_families,
    ROUND(AVG(docdb_family_size), 1) AS avg_family_size,
    ROUND(APPROX_QUANTILES(docdb_family_size, 2)[OFFSET(1)], 0) AS median_family_size,
    MAX(docdb_family_size) AS max_family_size,
    COUNT(CASE WHEN docdb_family_size >= 10 THEN 1 END) AS large_families_10plus,
    COUNT(CASE WHEN docdb_family_size >= 20 THEN 1 END) AS very_large_families_20plus,
    ROUND(COUNT(CASE WHEN docdb_family_size >= 10 THEN 1 END) * 100.0 / 
          COUNT(DISTINCT docdb_family_id), 1) AS pct_large_families
FROM airbus_families
GROUP BY appln_filing_year
ORDER BY appln_filing_year;


-- =============================================================================
-- QUERY I: Nachhaltigkeits-/Zukunftstechnologie-Patente
-- =============================================================================
/*
BUSINESS QUESTION:
Wie stark investiert Airbus in Zukunftstechnologien?
Konkret: Wasserstoff, E-Flug, KI, Drohnen/UAV, Additive Fertigung

STAKEHOLDER: Technologie-Strategie, Nachhaltigkeit, ESG-Reporting

ERKLÄRUNG: Sucht nach spezifischen CPC/IPC-Klassen UND Titel-Keywords,
die auf Zukunftstechnologien hinweisen.
CPC Y02T = Climate Change Mitigation - Transport
*/

WITH airbus_apps AS (
    SELECT DISTINCT
        a.appln_id,
        a.appln_filing_year,
        a.docdb_family_id
    FROM tls201_appln a
    JOIN tls207_pers_appln pa ON a.appln_id = pa.appln_id
    JOIN tls206_person p ON pa.person_id = p.person_id
    WHERE pa.applt_seq_nr > 0
      AND a.appln_filing_year BETWEEN 2014 AND 2024
      AND LOWER(p.person_name) LIKE '%airbus%'
),

future_tech AS (
    SELECT 
        aa.appln_id,
        aa.appln_filing_year,
        CASE
            -- Wasserstoff/Brennstoffzelle
            WHEN cpc.cpc_class_symbol LIKE 'Y02E%60/5%'
              OR cpc.cpc_class_symbol LIKE 'H01M%8/%'
              OR cpc.cpc_class_symbol LIKE 'C01B%3/%'
              OR LOWER(t.appln_title) LIKE '%hydrogen%'
              OR LOWER(t.appln_title) LIKE '%fuel cell%'
              OR LOWER(t.appln_title) LIKE '%wasserstoff%'
            THEN 'Wasserstoff/Brennstoffzelle'
            -- Elektrischer Antrieb
            WHEN cpc.cpc_class_symbol LIKE 'B64D%27/24%'
              OR cpc.cpc_class_symbol LIKE 'H02K%'
              OR (LOWER(t.appln_title) LIKE '%electric%' AND LOWER(t.appln_title) LIKE '%propuls%')
              OR LOWER(t.appln_title) LIKE '%hybrid%propuls%'
            THEN 'Elektro-/Hybridantrieb'
            -- KI/Machine Learning  
            WHEN cpc.cpc_class_symbol LIKE 'G06N%'
              OR LOWER(t.appln_title) LIKE '%machine learning%'
              OR LOWER(t.appln_title) LIKE '%neural network%'
              OR LOWER(t.appln_title) LIKE '%deep learning%'
              OR LOWER(t.appln_title) LIKE '%artificial intell%'
            THEN 'Künstliche Intelligenz'
            -- UAV/Drohnen
            WHEN LOWER(t.appln_title) LIKE '%unmanned%'
              OR LOWER(t.appln_title) LIKE '%uav%'
              OR LOWER(t.appln_title) LIKE '%drone%'
              OR LOWER(t.appln_title) LIKE '%urban air mobil%'
              OR LOWER(t.appln_title) LIKE '%evtol%'
            THEN 'UAV/Drohnen/Urban Air Mobility'
            -- Additive Fertigung
            WHEN cpc.cpc_class_symbol LIKE 'B33Y%'
              OR LOWER(t.appln_title) LIKE '%additive manufactur%'
              OR LOWER(t.appln_title) LIKE '%3d print%'
            THEN 'Additive Fertigung (3D-Druck)'
            -- Nachhaltigkeit allgemein
            WHEN cpc.cpc_class_symbol LIKE 'Y02T%'
            THEN 'Nachhaltiger Transport (Y02T)'
        END AS future_tech_area
    FROM airbus_apps aa
    LEFT JOIN tls224_appln_cpc cpc ON aa.appln_id = cpc.appln_id
    LEFT JOIN tls202_appln_title t ON aa.appln_id = t.appln_id
    WHERE t.appln_title_lg = 'en'  -- Englische Titel für Keyword-Suche
)

SELECT 
    future_tech_area,
    appln_filing_year,
    COUNT(DISTINCT appln_id) AS applications
FROM future_tech
WHERE future_tech_area IS NOT NULL
GROUP BY future_tech_area, appln_filing_year
ORDER BY future_tech_area, appln_filing_year;


-- =============================================================================
-- QUERY J: Erfinder-Standorte (NUTS-Regionen)
-- =============================================================================
/*
BUSINESS QUESTION:
Wo sitzen die Erfinder von Airbus? Wie verteilt sich die Innovationskraft
auf die Standorte (Toulouse, Hamburg, München, Bremen, Manching...)?

STAKEHOLDER: Standortpolitik, Forschungsförderung, Politikberatung

ERKLÄRUNG: Nutzt NUTS-Codes der Erfinder (invt_seq_nr > 0).
NUTS Level 2 gibt die Region, Level 3 den Kreis.
*/

SELECT 
    p.person_ctry_code AS inventor_country,
    SUBSTR(p.nuts, 1, 4) AS nuts_region,
    n.nuts_label AS region_name,
    COUNT(DISTINCT a.appln_id) AS applications,
    COUNT(DISTINCT p.person_id) AS unique_inventors,
    CASE 
        WHEN a.appln_filing_year BETWEEN 2014 AND 2018 THEN 'early'
        WHEN a.appln_filing_year BETWEEN 2019 AND 2024 THEN 'recent'
    END AS period
FROM tls201_appln a
JOIN tls207_pers_appln pa ON a.appln_id = pa.appln_id
JOIN tls206_person p ON pa.person_id = p.person_id
LEFT JOIN tls904_nuts n ON SUBSTR(p.nuts, 1, 4) = n.nuts
WHERE pa.invt_seq_nr > 0  -- Nur Erfinder, nicht Anmelder
  AND a.appln_filing_year BETWEEN 2014 AND 2024
  AND a.appln_id IN (
      SELECT pa2.appln_id 
      FROM tls207_pers_appln pa2
      JOIN tls206_person p2 ON pa2.person_id = p2.person_id
      WHERE pa2.applt_seq_nr > 0
        AND LOWER(p2.person_name) LIKE '%airbus%'
  )
  AND p.nuts IS NOT NULL
  AND LENGTH(p.nuts) >= 4
GROUP BY p.person_ctry_code, SUBSTR(p.nuts, 1, 4), n.nuts_label,
         CASE 
             WHEN a.appln_filing_year BETWEEN 2014 AND 2018 THEN 'early'
             WHEN a.appln_filing_year BETWEEN 2019 AND 2024 THEN 'recent'
         END
HAVING COUNT(DISTINCT a.appln_id) >= 10
ORDER BY applications DESC;


-- =============================================================================
-- ZUSAMMENFASSUNG: Erwartete Ergebnisse und Interpretationshinweise
-- =============================================================================
/*
Die 10 Queries liefern zusammen ein vollständiges Bild der Airbus-Patentstrategie:

A) NAMENSVARIANTEN: Grundlage - zeigt alle Airbus-Entitäten in PATSTAT
B) ANMELDETREND: Gesamtbild - Patentaktivität nach Geschäftsbereich/Jahr
C) GEOGRAPHIE: Wo wird geschützt - EP/FR/US/CN-Verteilung und Trends
D) TECHNOLOGIEFELDER: Was wird geschützt - WIPO 35 Technologiefelder
E) IPC-KLASSEN: Detail - Top 25 IPC-Klassen mit Trends (B64=Luft, G06=IT...)
F) ERTEILUNGSQUOTE: Wie erfolgreich - Grant Rate und Time-to-Grant pro Amt
G) KOOPERATIONEN: Mit wem - Joint Applications mit Partnern
H) FAMILIENGRÖSSE: Wie breit - Internationaler Schutzumfang pro Erfindung
I) ZUKUNFTSTECH: Wohin geht es - H2, E-Flug, KI, Drohnen, 3D-Druck
J) ERFINDER-STANDORTE: Wo entsteht Innovation - NUTS-Regionen

TYPISCHE HYPOTHESEN ZUM VALIDIEREN:
1. Airbus verlagert IP-Investitionen von klassischem Flugzeugbau zu 
   Digitalisierung (G06) und Nachhaltigkeit (Y02T)
2. Der Anteil China-Anmeldungen steigt überproportional
3. Airbus Defence & Space wächst stärker als Airbus Operations
4. Kooperationen mit Universitäten nehmen zu
5. Toulouse/FR dominiert bei Erfindern, aber Hamburg/DE wächst
6. Familiengröße steigt (= selektivere, aber breitere Anmeldungen)
*/
