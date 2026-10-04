"""Export reproductible du nettoyage de Jules pour les notebooks suivants.
Depuis la racine : python src/export_processed.py
Les règles sont reprises sans changement des cellules 12, 29 et 30 du notebook 01.
"""
from pathlib import Path
import re
import json
import hashlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/welddb.data"
DEST = ROOT / "data/processed"

# Noms de colonnes, groupes par famille.
# On prefixe par l'unite quand elle est ambigue (_ppm, _pct, _MPa, _C) pour
# eviter toute erreur d'interpretation plus tard.

# Colonnes 1 a 12 : concentrations en pourcentage massique.
COMPOSITION_WT = ["C", "Si", "Mn", "S", "P", "Ni", "Cr", "Mo", "V", "Cu", "Co", "W"]

# Colonnes 13 a 21 : concentrations en parties par million.
COMPOSITION_PPM = ["O_ppm", "Ti_ppm", "N_ppm", "Al_ppm", "B_ppm",
                   "Nb_ppm", "Sn_ppm", "As_ppm", "Sb_ppm"]

# Colonnes 22 a 30 : parametres du procede de soudage.
PROCESS = ["Current_A", "Voltage_V", "AC_DC", "Electrode_pol",
           "HeatInput_kJmm", "InterpassT_C", "WeldType",
           "PWHT_T_C", "PWHT_time_h"]

# Colonnes 31 a 38 : proprietes mecaniques (cibles candidates).
MECHANICAL = ["YieldStrength_MPa", "UTS_MPa", "Elongation_pct",
              "ReductionArea_pct", "CharpyT_C", "CharpyToughness_J",
              "Hardness", "FATT50"]

# Colonnes 39 a 43 : fractions de microstructure, en pourcentage.
MICROSTRUCTURE = ["PrimaryFerrite_pct", "FerriteSecondPhase_pct",
                  "AcicularFerrite_pct", "Martensite_pct",
                  "FerriteCarbide_pct"]

# Colonne 44.
IDENTIFIER = ["WeldID"]

COMPOSITION = COMPOSITION_WT + COMPOSITION_PPM
COLUMNS = COMPOSITION + PROCESS + MECHANICAL + MICROSTRUCTURE + IDENTIFIER

# Colonnes a ne jamais convertir en nombre : les trois variables categorielles
# du procede, plus l'identifiant de soudure.
CATEGORIELLES = ["AC_DC", "Electrode_pol", "WeldType"] + IDENTIFIER


# Expressions regulieres, une par famille.
RE_CENSURE = re.compile(r"^<\s*(\d+\.?\d*)$")              # <0.002
RE_INTERVALLE = re.compile(r"^(\d+\.?\d*)\s*-\s*(\d+\.?\d*)$")   # 150-200
RE_TOT_RES = re.compile(r"^(\d+\.?\d*)tot(\d+\.?\d*|nd)res$")    # 48tot18res
RE_UNITE = re.compile(r"^(\d+\.?\d*)\s*\(?\s*([A-Za-z]+\s*\d*)\s*\)?$")  # 143(Hv30)


def nettoyer_valeur(valeur, strategie_censure="moitie"):
    """Convertit une chaine brute en flottant.

    Renvoie un couple (valeur, motif), ou motif identifie le traitement
    applique. Ce motif alimente le masque de tracabilite, qui permet de
    chiffrer chaque decision de pre-traitement dans le rapport.
    """
    if valeur is None:
        return np.nan, "manquant"

    texte = str(valeur).strip()

    if texte == "" or texte.upper() == "N":
        return np.nan, "manquant"

    # Cas nominal : c'est deja un nombre.
    try:
        return float(texte), "propre"
    except ValueError:
        pass

    correspondance = RE_CENSURE.match(texte)
    if correspondance:
        seuil = float(correspondance.group(1))
        if strategie_censure == "moitie":
            return seuil / 2.0, "censure"
        if strategie_censure == "seuil":
            return seuil, "censure"
        return np.nan, "censure"

    correspondance = RE_INTERVALLE.match(texte)
    if correspondance:
        bas, haut = float(correspondance.group(1)), float(correspondance.group(2))
        return (bas + haut) / 2.0, "intervalle"

    # RE_TOT_RES doit etre teste AVANT RE_UNITE : cette derniere, plus
    # permissive, capturerait "54totndres" comme la valeur 54 suivie d'une
    # pretendue echelle "totndres". La valeur extraite serait correcte, mais le
    # motif de tracabilite serait faux.
    correspondance = RE_TOT_RES.match(texte)
    if correspondance:
        return float(correspondance.group(1)), "total_retenu"

    correspondance = RE_UNITE.match(texte)
    if correspondance:
        return float(correspondance.group(1)), "unite_retiree"

    # Forme inconnue : on ne devine pas, on signale pour traitement manuel.
    return np.nan, "non_interprete"




def exporter():
    brut = pd.read_csv(RAW, sep=r"\s+", header=None, dtype=str)
    assert brut.shape[1] == len(COLUMNS)
    df = brut.copy()
    df.columns = COLUMNS
    # Application a toutes les colonnes numeriques, en construisant en parallele
    # le masque de tracabilite.
    propre = df.copy()
    masque = pd.DataFrame(index=df.index, columns=df.columns, dtype=object)

    # On conserve les chaines brutes de Hardness avant conversion, pour en extraire
    # l'echelle de mesure.
    hardness_brut = df["Hardness"].copy()

    for col in COLUMNS:
        if col in CATEGORIELLES:
            serie = df[col].str.strip()
            masque[col] = np.where(serie.str.upper() == "N", "manquant", "propre")
            propre[col] = serie.replace({"N": np.nan})
            continue

        valeurs, motifs = zip(*(nettoyer_valeur(v) for v in df[col]))
        propre[col] = pd.Series(valeurs, index=df.index, dtype="float64")
        masque[col] = motifs

    # Echelle de durete, conservee a part (cf. decision 3).
    propre["hardness_scale"] = (
        hardness_brut.str.extract(r"\(?\s*([A-Za-z]+\s*\d*)\s*\)?$", expand=False)
        .str.replace(r"\s+", "", regex=True)
        .replace({"N": np.nan})
    )


    assert not (masque == "non_interprete").any().any()
    signatures = df[COLUMNS[:28]].apply(lambda r: "|".join(r), axis=1)
    groupes = pd.DataFrame({"groupe": pd.factorize(signatures, sort=True)[0],
                            "signature_brute": signatures}, index=df.index)
    DEST.mkdir(parents=True, exist_ok=True)
    for name, table in [("welddb_clean.csv", propre),
                        ("welddb_cleaning_mask.csv", masque),
                        ("welddb_groups.csv", groupes)]:
        table.to_csv(DEST / name, index_label="row_id")
    schema = {k: globals()[k] for k in ["COLUMNS", "CATEGORIELLES", "COMPOSITION", "PROCESS", "MECHANICAL", "MICROSTRUCTURE", "IDENTIFIER"]}
    meta = {"source": "nettoyage du notebook 01 de Jules, cellules 12, 29 et 30",
            "raw_sha256": hashlib.sha256(RAW.read_bytes()).hexdigest(),
            "exporter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "schema": schema, "rows": len(propre), "columns": len(propre.columns),
            "files_sha256": {name: hashlib.sha256((DEST/name).read_bytes()).hexdigest()
                             for name in ["welddb_clean.csv", "welddb_cleaning_mask.csv", "welddb_groups.csv"]}}
    (DEST / "welddb_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"Export du nettoyage de Jules : {len(propre)} lignes, {len(propre.columns)} colonnes, {groupes.groupe.nunique()} groupes.")
    return propre, masque, groupes

if __name__ == "__main__":
    exporter()
