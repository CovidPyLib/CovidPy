# Copyright (c) 2022, CovidPyLib
# This file is part of CovidPy v0.1.2
#
# The project has been distributed in the hope it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You can use it and/or modify it under the terms of the GNU General Public License v3.0 or later.
# You should have received a copy of the GNU General Public License along with the project.

import time
import io
import json

from dataclasses import dataclass
from qrcode.image.pil import PilImage

from typing import Union, Dict


def stringify(value) -> str:
    if isinstance(value, dict):
        for key, val in value.items():
            value[key] = stringify(val)
        return json.dumps(value, indent=4)
    elif isinstance(value, list):
        return [item.to_dict() for item in value]
    else:
        return str(value)


class VaccinesReccs:
    pfizer_recc = """Comirnaty 30 micrograms/dose concentrate for dispersion for injection is indicated for active immunisation to prevent COVID-19 caused by SARS-CoV-2 virus, in individuals 12 years of age and older.

    Comirnaty 30 micrograms/dose dispersion for injection is indicated for active immunisation to prevent COVID-19 caused by SARS-CoV-2 virus, in individuals 12 years of age and older.

    Comirnaty 10 micrograms/dose concentrate for dispersion for injection is indicated for active immunisation to prevent COVID-19 caused by SARS-CoV-2 virus, in children aged 5 to 11 years.

    The use of this vaccine should be in accordance with official recommendations."""

    janssen_recc = """COVID-19 Vaccine Janssen is indicated for active immunisation to prevent COVID-19 caused by SARS-CoV-2 in individuals 18 years of age and older.

    The use of this vaccine should be in accordance with official recommendations."""

    novavax_recc = """Nuvaxovid is indicated for active immunisation to prevent COVID-19 caused by SARS-CoV-2 in individuals 18 years of age and older.

    The use of this vaccine should be in accordance with official recommendations."""

    moderna_recc = """Spikevax is indicated for active immunisation to prevent COVID-19 caused by SARS-CoV-2 in individuals 12 years of age and older.

    The use of this vaccine should be in accordance with official recommendations."""

    az_recc = """Vaxzevria is indicated for active immunisation to prevent COVID 19 caused by SARS CoV 2, in individuals 18 years of age and older.
    The use of this vaccine should be in accordance with official recommendations."""


class QRCode:
    def __init__(
        self, img: PilImage, rawdata: dict, in_blacklist: bool, instance
    ) -> None:
        super().__init__()
        self.raw_data = rawdata
        self.pil_img = img
        self.in_blacklist = in_blacklist
        self.__cpyinstance = instance

    def save(self, path: str):
        self.pil_img.save(path)

    def to_bytesio(self) -> io.BytesIO:
        bio = io.BytesIO()
        self.pil_img.save(bio)
        return bio

    def decode(self):
        self.__cpyinstance.decode(self)

    def verify(self):
        self.__cpyinstance.verify(self)


@dataclass
class VerifyResult:
    valid: bool
    revoked: bool


class VaccineInfo:
    def __init__(
        self,
        codename=None,
        knownas=None,
        name=None,
        productor=None,
        indications=None,
        substance=None,
        emalink=None,
    ) -> None:
        self.eu_codename = codename
        self.known_as = knownas
        self.vaccine_name = name
        self.productor_name = productor
        self.eu_indications = indications
        self.active_substance = substance
        self.ema_link = emalink

    def to_dict(self) -> dict:
        return {
            "eu_codename": self.eu_codename,
            "known_as": self.known_as,
            "vaccine_name": self.vaccine_name,
            "productor_name": self.productor_name,
            "eu_indications": self.eu_indications,
            "active_substance": self.active_substance,
            "ema_link": self.ema_link,
        }

    def __str__(self) -> str:
        return json.dumps(
            {
                "eu_codename": self.eu_codename,
                "known_as": self.known_as,
                "vaccine_name": self.vaccine_name,
                "productor_name": self.productor_name,
                "eu_indications": self.eu_indications,
                "active_substance": self.active_substance,
                "ema_link": self.ema_link,
            },
            indent=4,
        )


eu_codenames: Dict[str, VaccineInfo] = {
    "EU/1/20/1528": VaccineInfo(
        "EU/1/20/1528",
        "Pfizer",
        "Comirnaty",
        "BioNTech Manufacturing GmbH",
        VaccinesReccs.pfizer_recc,
        "tozinameran, COVID-19 mRNA vaccine (nucleoside-modified)",
        "https://www.ema.europa.eu/en/medicines/human/summaries-opinion/comirnaty",
    ),
    "EU/1/20/1525": VaccineInfo(
        "EU/1/20/1525",
        "Janssen",
        "COVID-19 Vaccine Janssen",
        "Janssen-Cilag International NV",
        VaccinesReccs.janssen_recc,
        "COVID-19 vaccine (Ad26.COV2-S [recombinant])",
        "https://www.ema.europa.eu/en/medicines/human/EPAR/covid-19-vaccine-janssen",
    ),
    "EU/1/21/1618": VaccineInfo(
        "EU/1/21/1618",
        "Novavax",
        "Nuvaxovid",
        "Novavax CZ, a.s.",
        VaccinesReccs.novavax_recc,
        "COVID-19 Vaccine (recombinant, adjuvanted)",
        None,
    ),
    "EU/1/20/1507": VaccineInfo(
        "EU/1/20/1507",
        "Moderna",
        "Spikevax",
        "MODERNA BIOTECH SPAIN, S.L.",
        VaccinesReccs.moderna_recc,
        "COVID-19 mRNA Vaccine (nucleoside modified)",
        "https://www.ema.europa.eu/en/medicines/human/summaries-opinion/covid-19-vaccine-moderna",
    ),
    "EU/1/21/1529": VaccineInfo(
        "EU/1/21/1529",
        "AstraZeneca",
        "Vaxzevria",
        "AstraZeneca AB",
        VaccinesReccs.az_recc,
        "COVID-19 Vaccine (ChAdOx1-S [recombinant])",
        "https://www.ema.europa.eu/en/medicines/human/EPAR/vaxzevria-previously-covid-19-vaccine-astrazeneca",
    ),
}

diseasedict: dict = {"840539006": "Covid-19 (SARS-CoV-1)"}


class Person:
    def __init__(self, jsonp, date) -> None:
        self.raw_data = [jsonp, date]
        self.first_name = jsonp["fn"]
        self.last_name = jsonp["gn"]
        self.date_of_birth = date
        self.formatted_first_name = jsonp["fnt"]
        self.formatted_last_name = jsonp["gnt"]

    def to_dict(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "formatted_first_name": self.formatted_first_name,
            "formatted_last_name": self.formatted_last_name,
        }

    def __str__(self):
        return json.dumps(
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "date_of_birth": self.date_of_birth,
                "formatted_first_name": self.formatted_first_name,
                "formatted_last_name": self.formatted_last_name,
            },
            indent=4,
        )


class VaccinationCertificateInfo:
    def __init__(self, jsoni) -> None:
        self.vaccine = eu_codenames[jsoni["mp"]]
        self.somministrated_doses = jsoni["dn"]
        self.max_doses = jsoni["sd"]
        self.issuer = jsoni["is"]
        self.vaccination_date = jsoni["dt"]
        self.vaccination_country = jsoni["co"]
        self.certificate_identifier = jsoni["ci"]
        self.disease = diseasedict[jsoni["tg"]]
        self.disease_code = jsoni["tg"]
        self.vaccine_identifier = jsoni["vp"]
        self.vaccination_country_code = jsoni["co"]

    def to_dict(self) -> dict:
        return {
            "vaccine": self.vaccine.to_dict(),
            "somministrated_doses": self.somministrated_doses,
            "max_doses": self.max_doses,
            "issuer": self.issuer,
            "vaccination_date": self.vaccination_date,
            "vaccination_country": self.vaccination_country,
            "certificate_identifier": self.certificate_identifier,
            "disease": self.disease,
            "disease_code": self.disease_code,
            "vaccine_identifier": self.vaccine_identifier,
            "vaccination_country_code": self.vaccination_country_code,
        }

    def __str__(self) -> str:
        return json.dumps(
            {
                "vaccine": str(self.vaccine),
                "somministrated_doses": self.somministrated_doses,
                "max_doses": self.max_doses,
                "issuer": self.issuer,
                "vaccination_date": self.vaccination_date,
                "vaccination_country": self.vaccination_country,
                "certificate_identifier": self.certificate_identifier,
                "disease": self.disease,
                "disease_code": self.disease_code,
                "vaccine_identifier": self.vaccine_identifier,
            },
            indent=4,
        )


class NAATest:
    def __init__(self, jsoni) -> None:
        self.test_name = jsoni["nm"]
        self.test_type_name = "Nucleic acid amplification with probe detection"
        self.collection_date_iso = jsoni["sc"]
        self.description = """The LOINC Probe.amp.tar method is used for assays that include a nucleic acid amplification step, in which many copies of the nucleic acid sequence(s) of interest are made, followed by detection of the target nucleic acid of interest using a hybridization probe. Nucleic acid amplification can be done using different techniques such as polymerase chain reaction (PCR). The primary difference between the Probe.amp.tar and Non-probe.amp.tar Methods is the technique used for target nucleic acid detection. Note that for historical reasons, this Method also includes traditional techniques for identifying PCR target amplification products, such as gel separation and staining to identify the fragments based on their expected sizes."""
        self.raw_content = jsoni

    def to_dict(self) -> dict:
        return {
            "test_name": self.test_name,
            "test_type_name": self.test_type_name,
            "collection_date_iso": self.collection_date_iso,
            "description": self.description,
            "raw_content": self.raw_content,
        }

    def __str__(self) -> str:
        return json.dumps(
            {
                "test_name": self.test_name,
                "collection_date_iso": self.collection_date_iso,
                "description": self.description,
                "raw_content": self.raw_content,
            },
            indent=4,
        )


class RATest:
    def __init__(self, jsoni) -> None:
        self.test_name = jsoni["nm"]
        self.test_type_name = "Rapid immunoassay"
        self.collection_date_iso = jsoni["sc"]
        self.description = """The immunoassay method (IA) encompasses most immunoassays that detect the linking of antigens and antibodies via special signaling mechanisms, including EIA, ELISA, chemiluminescence and other similar tests that produce one measure (quantitative or qualitative) of the analyte of interest. Tests that are not included within the IA method include immune blot (IB) and immune fluorescence (IF), immune stain, and immune-based flow cytometry (FC), which were created as distinct methods because they usually yield multiple related observations and can provide information about the presence or amount of a target analyte as well as its location on a smear, tissue slice or cell.
The rapid immunoassay (IA.rapid) method is used for IA that take 60 minutes or less from start to finish."""
        self.raw_content = jsoni

    def to_dict(self) -> dict:
        return {
            "test_name": self.test_name,
            "test_type_name": self.test_type_name,
            "collection_date_iso": self.collection_date_iso,
            "description": self.description,
            "raw_content": self.raw_content,
        }

    def __str__(self) -> str:
        return json.dumps(
            {
                "test_name": self.test_name,
                "collection_date_iso": self.collection_date_iso,
                "description": self.description,
                "raw_content": self.raw_content,
            },
            indent=4,
        )


class TestCertificateInfo:
    def __init__(self, jsoni) -> None:
        self.test_type_code = jsoni["tp"]
        self.test_type = "NAA" if self.test_type_code == "LP6464-4" else "RAT"
        self.test = None
        self.naa_test = None
        self.rat_test = None
        if self.test_type_code == "LP6464-4":
            self.naa_test = NAATest(jsoni)
            self.test = self.naa_test
        else:
            self.rat_test = RATest(jsoni)
            self.test = self.rat_test
        self.test_result_code = jsoni["tr"]
        self.covid_detected = self.test_result_code == "260373001"
        self.test_manufacturer = jsoni["ma"]
        self.disease = diseasedict[jsoni["tg"]]
        self.disease_code = jsoni["tg"]
        self.certificate_identifier = jsoni["ci"]
        self.test_country_code = jsoni["co"]

    def to_dict(self) -> dict:
        return {
            "test_type_code": self.test_type_code,
            "test_type": self.test_type,
            "test": self.test.to_dict() if self.test else None,
            "test_result_code": self.test_result_code,
            "covid_detected": self.covid_detected,
            "test_manufacturer": self.test_manufacturer,
            "disease": self.disease,
            "disease_code": self.disease_code,
            "certificate_identifier": self.certificate_identifier,
            "test_country_code": self.test_country_code,
        }

    def __str__(self) -> str:
        return json.dumps(
            {
                "test_type_code": self.test_type_code,
                "test_type": self.test_type,
                "naa_test": str(self.naa_test),
                "rat_test": str(self.rat_test),
                "test": str(self.test),
                "test_result_code": self.test_result_code,
                "covid_detected": self.covid_detected,
                "test_manufacturer": self.test_manufacturer,
                "disease": self.disease,
                "disease_code": self.disease_code,
                "certificate_identifier": self.certificate_identifier,
                "test_country_code": self.test_country_code,
            },
            indent=4,
        )


class RecoveryCertificateInfo:
    def __init__(self, jsoni) -> None:
        self.first_positive_date_iso = jsoni["fr"]
        self.country_of_test = jsoni["co"]
        self.issuer = jsoni["is"]
        self.valid_from_iso = jsoni["df"]
        self.valid_until_iso = jsoni["du"]
        self.certificate_identifier = jsoni["ci"]

    def to_dict(self) -> dict:
        return {
            "first_positive_date_iso": self.first_positive_date_iso,
            "country_of_test": self.country_of_test,
            "issuer": self.issuer,
            "valid_from_iso": self.valid_from_iso,
            "valid_until_iso": self.valid_until_iso,
            "certificate_identifier": self.certificate_identifier,
        }

    def __str__(self) -> str:
        return json.dumps(
            {
                "first_positive_date_iso": self.first_positive_date_iso,
                "country_of_test": self.country_of_test,
                "issuer": self.issuer,
                "valid_from_iso": self.valid_from_iso,
                "valid_until_iso": self.valid_until_iso,
                "certificate_identifier": self.certificate_identifier,
            },
            indent=4,
        )


class Certificate:
    def __init__(self, jsoncert: dict) -> None:
        self.raw_data = jsoncert
        self.expiry_date_ts = jsoncert[4]
        self.release_date_ts = jsoncert[6]
        self.expiry_date = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.gmtime(self.expiry_date_ts)
        )
        self.release_date = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.gmtime(self.release_date_ts)
        )
        self.country_code = jsoncert[1]
        self.owner = Person(jsoncert[-260][1]["nam"], jsoncert[-260][1]["dob"])
        self.version = jsoncert[-260][1]["ver"]
        self.certificate_type = None
        self.vaccination_certificate: VaccinationCertificateInfo = None
        self.recovery_certificate: RecoveryCertificateInfo = None
        self.test_certificate: TestCertificateInfo = None
        self.unknown_certificate: dict = None
        self.certificate: Union[
            VaccinationCertificateInfo,
            RecoveryCertificateInfo,
            TestCertificateInfo,
            dict,
        ] = None
        if jsoncert[-260][1].get("v", None):
            self.certificate_type = "vaccine"
            self.vaccination_certificate = [
                VaccinationCertificateInfo(x) for x in jsoncert[-260][1]["v"]
            ]
            self.certificate = self.vaccination_certificate
        elif jsoncert[-260][1].get("r", None):
            self.certificate_type = "recovery"
            self.recovery_certificate = [
                RecoveryCertificateInfo(x) for x in jsoncert[-260][1]["r"]
            ]
            self.certificate = self.recovery_certificate
        elif jsoncert[-260][1].get("t", None):
            self.certificate_type = "test"
            self.test_certificate = [
                TestCertificateInfo(x) for x in jsoncert[-260][1]["t"]
            ]
            self.certificate = self.test_certificate
        else:
            self.certificate_type = "unknown"
            self.unknown_certificate = jsoncert
            self.certificate = self.unknown_certificate

    def to_dict(self) -> dict:
        return {
            "country_code": self.country_code,
            "owner": self.owner.to_dict(),
            "version": self.version,
            "certificate_type": self.certificate_type,
            "vaccination_certificate": stringify(self.vaccination_certificate),
            "recovery_certificate": stringify(self.recovery_certificate),
            "test_certificate": stringify(self.test_certificate),
            "certificate": stringify(self.certificate),
        }

    def __str__(self) -> str:
        return json.dumps(
            {
                "country_code": self.country_code,
                "owner": self.owner.to_dict(),
                "version": self.version,
                "certificate_type": self.certificate_type,
                "vaccination_certificate": stringify(self.vaccination_certificate),
                "recovery_certificate": stringify(self.recovery_certificate),
                "test_certificate": stringify(self.test_certificate),
                "certificate": stringify(self.certificate),
            },
            indent=4,
        )
