"""Constants for the ANEF API."""

from __future__ import annotations

from enum import Enum


class StageEnum(str, Enum):
    """Stages of the naturalisation request process."""

    CREATION_DEMANDE = 'Création de la demande'
    EXAMEN_PIECES = 'Examen des pièces en cours'
    DEPOT_DEMANDE = 'Dépôt de la demande'
    TRAITEMENT_EN_COURS = 'Traitement en cours'
    RECEPTION_RECEPISSE = 'Réception du récépissé de complétude'
    ENTRETIEN_ASSIMILATION = "Entretien d'assimilation"
    DECISION_STATUEE = 'Décision statuée'
    CEREMONIE_LIVRET = 'Cérémonie de remise du livret'


class ServiceEnum(str, Enum):
    """Services handling the naturalisation request process."""

    PREFECTURE = 'PREFECTURE'
    ANEF = 'ANEF'
    SDANF = 'SDANF'
    SCEC = 'SCEC'
    DECRET = 'DECRET'


class APICodeEnum(str, Enum):
    """API return codes and their description for the naturalisation request process."""

    DRAFT = 'draft'
    VERIFICATION_FORMELLE_A_TRAITER = 'Vérification formelle : à traiter'
    VERIFICATION_FORMELLE_EN_COURS = 'Vérification formelle : en cours'
    VERIFICATION_FORMELLE_MISE_EN_DEMEURE = 'Vérification formelle : mise en demeure'
    CSS_MISE_EN_DEMEURE_A_AFFECTER = 'CSS : mise en demeure à affecter'
    CSS_MISE_EN_DEMEURE_A_REDIGER = 'CSS : mise en demeure à rédiger'
    INSTRUCTION_A_AFFECTER = 'Instruction : à affecter'
    INSTRUCTION_RECEPISSE_COMPLETUDE_A_ENVOYER = 'Instruction : récépissé de complétude à envoyer'
    INSTRUCTION_RECEPISSE_COMPLETUDE_A_ENVOYER_RETOUR_COMPLEMENT_A_TRAITER = (
        'Instruction : récépissé de complétude à envoyer (retour complément à traiter)'
    )
    INNTRUCTION_DATE_EA_A_FIXER = "Instruction : date d'entretien d'assimilation à fixer"
    EA_DEMANDE_REPORT_EA = "Entretien d'assimilation : demande de report de l'entretien d'assimilation"
    EA_EN_ATTENTE_EA = "Entretien d'assimilation : en attente de l'entretien d'assimilation"
    EA_CREA_A_VALIDER = "Entretien d'assimilation : compte-rendu de l'entretien d'assimilation à valider"
    PROP_DECISION_PREF_A_EFFECTUER = 'Proposition de décision préfectorale : à effectuer'
    PROP_DECISION_PREF_EN_ATTENTE_RETOUR_HIERARCHIQUE = (
        'Proposition de décision préfectorale : en attente de retour hiérarchique'
    )
    PROP_DECISION_PREF_PROP_A_EDITER = 'Proposition de décision préfectorale : proposition à éditer'
    PROP_DECISION_PREF_EN_ATTENTE_RETOUR_SIGNATURE = (
        'Proposition de décision préfectorale : en attente de retour de signature'
    )
    CONTROLE_A_EFFECTUER = 'Contrôle : à effectuer'
    CONTROLE_EN_ATTENTE_PEC = "Contrôle : en attente de pièce d'état civil"
    CONTROLE_PEC_A_FAIRE = "Contrôle : pièce d'état civil à faire"
    CONTROLE_TRANSMISE_POUR_DECRET = 'Contrôle : transmise pour décret'
    CONTROLE_EN_ATTENTE_RETOUR_HIERARCHIQUE = 'Contrôle : en attente de retour hiérarchique'
    CONTROLE_DECISION_A_EDITER = 'Contrôle : décision à éditer'
    CONTROLE_EN_ATTENTE_SIGNATURE = 'Contrôle : en attente de signature'
    TRANSMIS_A_AC = 'Transmis à AC'
    A_VERIFIER_AVANT_INSERTION_DECRET = "À vérifier avant l'insertion dans le décret"
    PRETE_POUR_INSERTION_DECRET = "Prêt pour l'insertion dans le décret"
    DECRET_NATURALISATION_PUBLIC = 'Décret de naturalisation publié'
    DECRET_EN_PREPARATION = 'Décret en préparation'
    DECRET_A_QUALIFIER = 'Décret à qualifier'
    DECRET_EN_VALIDATION = 'Décret en validation'
    CSS_EN_DELAIS_RECOURS = 'CSS en délais de recours'
    DECISION_NEGATIVE_EN_DELAIS_RECOURS = 'Décision négative en délais de recours'
    IRRECEVABILITE_MANIFESTE = 'Irrecevabilité manifeste'
    DECISION_NOTIFIEE = 'Décision notifiée'
    CSS_NOTIFIE = 'CSS notifié'
    DEMANDE_EN_COURS_RAPO = 'Demande en cours RAPO'
    CONTROLE_DEMANDE_NOTIFIEE = 'Contrôle : demande notifiée'
    DECRET_PUBLIE = 'Décret publié'
    UNKNOWN = 'Unknown'


class LanguageEnum(str, Enum):
    """List of supported languages."""

    EN = 'en'
    FR = 'fr'
    ES = 'es'
