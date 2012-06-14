from tigershark.facade import ElementAccess
from tigershark.facade import X12LoopBridge
from tigershark.facade import X12SegmentBridge
from tigershark.facade import enum
from tigershark.facade import D8
from tigershark.facade import DR
from tigershark.facade import TM
from tigershark.facade import boolean
from tigershark.facade.enum.common import date_or_time_qualifier
from tigershark.facade.enum.common import reference_id_qualifier
from tigershark.facade.enum.common import id_code_qualifier


class Header(X12LoopBridge):
    loopName = "HEADER"

    class _HierarchicalTransaction(X12LoopBridge):
        """Use this to start the transaction set.

        This also indicates the sequence of hierarchical levels of information
        that will follow, though that information is not used at this time."""
        structure = ElementAccess("BHT", 1, x12type=enum(
            {"0022": "Information Source, Information Receiver, Subscriber, "
                "or Dependent."}, raw_unknowns=True))
        purpose = ElementAccess("BHT", 2, x12type=enum({
            "01": "Cancellation",
            "11": "Response",
            "13": "Request",
            "36": "Authority to Dedduct (Reply)"}, raw_unknowns=True))
        transaction_id = ElementAccess("BHT", 3)
        creation_date = ElementAccess("BHT", 4, x12type=D8)
        creation_time = ElementAccess("BHT", 5, x12type=TM)
        type = ElementAccess("BHT", 6, x12type=enum({
            "RT": "Spend Down",
            "RU": "Medical Services Reservation"}, raw_unknowns=True))

    def __init__(self, aLoop, *args, **kwargs):
        super(Header, self).__init__(aLoop, *args, **kwargs)
        self.hierarchical_transaction_info = self._HierarchicalTransaction(
                aLoop)


class HL(object):
    id = ElementAccess("HL", 1)
    parent_id = ElementAccess("HL", 2)
    level = ElementAccess("HL", 3, x12type=enum(
        {"20": "Information Source",
         "21": "Information Receiver",
         "22": "Subscriber",
            }))
    has_children = ElementAccess("HL", 4, x12type=boolean("1"))


class TraceNumber(X12SegmentBridge):
    """ Uniquely identify this transaction set.

    Also aid in reassociating payments and remittances that have been
    separated.
    """
    trace_type = ElementAccess("TRN", 1, x12type=enum({
            "1": "Current Transaction Trace Numbers",
            "2": "Referenced Transaction Trace Numbers (Value from 270)"}))
    trace_number = ElementAccess("TRN", 2)
    entity_id = ElementAccess("TRN", 3)
    entity_additional_id = ElementAccess("TRN", 4)


class NamedEntity(X12SegmentBridge):
    entity_identifier = ElementAccess("NM1", 1, x12type=enum({
            "03": "Dependent",
            "1P": "Provider",
            "2B": "Third-Party Administrator",
            "36": "Employer",
            "80": "Hospital",
            "FA": "Facility",
            "GP": "Gateway Provider",
            "IL": "Insured",
            "P5": "Plan Sponsor",
            "PR": "Payer",
            "QC": "Patient"}))
    entity_type = ElementAccess("NM1", 2, x12type=enum({
            "1": "Person",
            "2": "Non-Person Entity"}))

    last_name = ElementAccess("NM1", 3)
    org_name = ElementAccess("NM1", 3)
    first_name = ElementAccess("NM1", 4)
    middle_initial = ElementAccess("NM1", 5)
    suffix = ElementAccess("NM1", 7)

    id_code = ElementAccess("NM1", 9)
    id_code_qual = ElementAccess("NM1", 8, x12type=enum(id_code_qualifier))

    @property
    def is_person(self):
        return self.entity_type[0] == "1"

    @property
    def is_organization(self):
        return self.entity_type[0] == "2"


class ReferenceID(X12SegmentBridge):
    reference_id_qualifier = ElementAccess("REF", 1,
            x12type=enum(reference_id_qualifier))
    reference_id = ElementAccess("REF", 2)
    description = ElementAccess("REF", 3)


class ContactInformation(X12SegmentBridge):
    contact_code = ElementAccess("PER", 1, x12type=enum({
        "IC": "Information Contact"}, raw_unknowns=True))
    contact_name = ElementAccess("PER", 2)
    contact_edi = ElementAccess("PER", oneOf=("ED", (3, 4), (5, 6), (7, 8)))
    contact_email = ElementAccess("PER", oneOf=("EM", (3, 4), (5, 6), (7, 8)))
    contact_fax = ElementAccess("PER", oneOf=("FX", (3, 4), (5, 6), (7, 8)))
    contact_home_phone = ElementAccess("PER",
            oneOf=("HP", (3, 4), (5, 6), (7, 8)))
    contact_work_phone = ElementAccess("PER",
            oneOf=("WP", (3, 4), (5, 6), (7, 8)))
    contact_phone = ElementAccess("PER", oneOf=("TE", (3, 4), (5, 6), (7, 8)))
    contact_phone_ext = ElementAccess("PER",
            oneOf=("EX", (3, 4), (5, 6), (7, 8)))


class Address(X12SegmentBridge):
    addr1 = ElementAccess("N3", 1)
    addr2 = ElementAccess("N3", 2)


class Location(X12SegmentBridge):
    city = ElementAccess("N4", 1)
    state = ElementAccess("N4", 2)
    zip = ElementAccess("N4", 3)
    country_code = ElementAccess("N4", 4)
    location_type = ElementAccess("N4", 5, x12type=enum({
        "CY": "County/Parish",
        "FI": "Federal Information Processing Standards (FIPS) 55 (Named "
                "Populated Places)"}, raw_unknowns=True))
    location_id = ElementAccess("N4", 6)


class DemographicInformation(X12SegmentBridge):
    birth_date = ElementAccess("DMG", 2, x12type=D8, qualifier=(1, "D8"))
    gender = ElementAccess("DMB", 3, x12type=enum({
        "F": "Female",
        "M": "Male",
        "U": "Unknown"}))


class Relationship(X12SegmentBridge):
    is_insured = ElementAccess("INS", 1, x12type=boolean('Y'))
    relationship = ElementAccess("INS", 2, x12type=enum({
        "01": "Spouse",
        "18": "Self",
        "19": "Child",
        "21": "Unknown",
        "34": "Other Adult"}, raw_unknowns=True))
    maintenance_type = ElementAccess("INS", 3, x12type=enum({
        "001": "Change"}, raw_unknowns=True))
    maintenance_reason = ElementAccess("INS", 4, x12type=enum({
        "25": "Cahnge in Identifying Data Elements"}, raw_unknowns=True))
    student_status = ElementAccess("INS", 9, x12type=enum({
        "F": "Full-time",
        "N": "Not a Student",
        "P": "Part-time"}))
    handicapped = ElementAccess("INS", 10, x12type=boolean("Y"))
    birth_sequence_number = ElementAccess("INS", 17)


class DateOrTimePeriod(X12SegmentBridge):
    type = ElementAccess("DTP", 1, x12type=enum(date_or_time_qualifier))
    time = ElementAccess("DTP", 3, x12type=D8, qualifier=(2, "D8"))
    time_range = ElementAccess("DTP", 3, x12type=DR, qualifier=(2, "RD8"))


class Diagnosis(X12SegmentBridge):
    principal_diagnosis_icd9_code = ElementAccess("III", 2,
            qualifier=(1, "BK"))
    diagnosis_icd9_code = ElementAccess("III", 2, qualifier=(1, "BF"))
    other_code = ElementAccess("III", 2, qualifier=(1, "ZZ"), x12type=enum({
        "11": "Office",
        "12": "Home",
        "21": "Inpatient Hospital",
        "22": "Outpatient Hospital",
        "23": "Emergency Room - Hospital",
        "24": "Ambulatory Surgical Center",
        "25": "Birthing Center",
        "26": "Military Treatment Facility",
        "31": "Skilled Nursing Facility",
        "32": "Nursing Facility",
        "33": "Custodial Care Facility",
        "34": "Hospice",
        "41": "Ambulance - Land",
        "42": "Ambulance - Air or Water",
        "50": "Federally Qualified Health Center",
        "51": "Inpatient Psychiatric Facility",
        "52": "Psychiatric Facility Partial Hospitalization",
        "53": "Community Mental Health Center",
        "54": "Intermediate Care Facility/Mentally Retarded",
        "55": "Residential Substance Abuse Treatment Facility",
        "56": "Psychiatric Residential Treatment Center",
        "60": "Mass Immunization Center",
        "61": "Comprehensive Inpatient Rehabilitation Facility",
        "62": "Comprehensive Outpatient Rehabilitation Facility",
        "65": "End-Stage Renal Disease Treatment Facility",
        "71": "State or Local Public Health Clinic",
        "72": "Rural Health Clinic",
        "81": "Independent Laboratory 99 Other Unlisted Facility"},
        raw_unknowns=True))
