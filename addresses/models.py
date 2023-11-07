from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.snippets.models import register_snippet


from contacts.models import Contact
from core.models import TimeStampedModel


class CountryChoices(models.TextChoices):
    ARUBA = "ABW", _("Aruba")
    AFGHANISTAN = "AFG", _("Afghanistan")
    ANGOLA = "AGO", _("Angola")
    ANGUILLA = "AIA", _("Anguilla")
    ÅLAND_ISLANDS = "ALA", _("Åland Islands")
    ALBANIA = "ALB", _("Albania")
    ANDORRA = "AND", _("Andorra")
    UNITED_ARAB_EMIRATES = "ARE", _("United Arab Emirates")
    ARGENTINA = "ARG", _("Argentina")
    ARMENIA = "ARM", _("Armenia")
    AMERICAN_SAMOA = "ASM", _("American Samoa")
    ANTARCTICA = "ATA", _("Antarctica")
    FRENCH_SOUTHERN_TERRITORIES = "ATF", _("French Southern Territories")
    ANTIGUA_AND_BARBUDA = "ATG", _("Antigua and Barbuda")
    AUSTRALIA = "AUS", _("Australia")
    AUSTRIA = "AUT", _("Austria")
    AZERBAIJAN = "AZE", _("Azerbaijan")
    BURUNDI = "BDI", _("Burundi")
    BELGIUM = "BEL", _("Belgium")
    BENIN = "BEN", _("Benin")
    BONAIRE_SINT_EUSTATIUS_AND_SABA = "BES", _("Bonaire, Sint Eustatius and Saba")
    BURKINA_FASO = "BFA", _("Burkina Faso")
    BANGLADESH = "BGD", _("Bangladesh")
    BULGARIA = "BGR", _("Bulgaria")
    BAHRAIN = "BHR", _("Bahrain")
    BAHAMAS = "BHS", _("Bahamas")
    BOSNIA_AND_HERZEGOVINA = "BIH", _("Bosnia and Herzegovina")
    SAINT_BARTHÉLEMY = "BLM", _("Saint Barthélemy")
    BELARUS = "BLR", _("Belarus")
    BELIZE = "BLZ", _("Belize")
    BERMUDA = "BMU", _("Bermuda")
    BOLIVIA_PLURINATIONAL_STATE_OF = "BOL", _("Bolivia (Plurinational State of)")
    BRAZIL = "BRA", _("Brazil")
    BARBADOS = "BRB", _("Barbados")
    BRUNEI_DARUSSALAM = "BRN", _("Brunei Darussalam")
    BHUTAN = "BTN", _("Bhutan")
    BOUVET_ISLAND = "BVT", _("Bouvet Island")
    BOTSWANA = "BWA", _("Botswana")
    CENTRAL_AFRICAN_REPUBLIC = "CAF", _("Central African Republic")
    CANADA = "CAN", _("Canada")
    COCOS_KEELING_ISLANDS = "CCK", _("Cocos (Keeling) Islands")
    SWITZERLAND = "CHE", _("Switzerland")
    CHILE = "CHL", _("Chile")
    CHINA = "CHN", _("China")
    COTE_DIVOIRE = "CIV", _("Côte d'Ivoire")
    CAMEROON = "CMR", _("Cameroon")
    CONGO_DEMOCRATIC_REPUBLIC_OF_THE = "COD", _("Congo, Democratic Republic of the")
    CONGO = "COG", _("Congo")
    COOK_ISLANDS = "COK", _("Cook Islands")
    COLOMBIA = "COL", _("Colombia")
    COMOROS = "COM", _("Comoros")
    CABO_VERDE = "CPV", _("Cabo Verde")
    COSTA_RICA = "CRI", _("Costa Rica")
    CUBA = "CUB", _("Cuba")
    CURAÇAO = "CUW", _("Curaçao")
    CHRISTMAS_ISLAND = "CXR", _("Christmas Island")
    CAYMAN_ISLANDS = "CYM", _("Cayman Islands")
    CYPRUS = "CYP", _("Cyprus")
    CZECHIA = "CZE", _("Czechia")
    GERMANY = "DEU", _("Germany")
    DJIBOUTI = "DJI", _("Djibouti")
    DOMINICA = "DMA", _("Dominica")
    DENMARK = "DNK", _("Denmark")
    DOMINICAN_REPUBLIC = "DOM", _("Dominican Republic")
    ALGERIA = "DZA", _("Algeria")
    ECUADOR = "ECU", _("Ecuador")
    EGYPT = "EGY", _("Egypt")
    ERITREA = "ERI", _("Eritrea")
    WESTERN_SAHARA = "ESH", _("Western Sahara")
    SPAIN = "ESP", _("Spain")
    ESTONIA = "EST", _("Estonia")
    ETHIOPIA = "ETH", _("Ethiopia")
    FINLAND = "FIN", _("Finland")
    FIJI = "FJI", _("Fiji")
    FALKLAND_ISLANDS_MALVINAS = "FLK", _("Falkland Islands (Malvinas)")
    FRANCE = "FRA", _("France")
    FAROE_ISLANDS = "FRO", _("Faroe Islands")
    MICRONESIA_FEDERATED_STATES_OF = "FSM", _("Micronesia (Federated States of)")
    GABON = "GAB", _("Gabon")
    UNITED_KINGDOM_OF_GREAT_BRITAIN_AND_NORTHERN_IRELAND = "GBR", _(
        "United Kingdom of Great Britain and Northern Ireland"
    )
    GEORGIA = "GEO", _("Georgia")
    GUERNSEY = "GGY", _("Guernsey")
    GHANA = "GHA", _("Ghana")
    GIBRALTAR = "GIB", _("Gibraltar")
    GUINEA = "GIN", _("Guinea")
    GUADELOUPE = "GLP", _("Guadeloupe")
    GAMBIA = "GMB", _("Gambia")
    GUINEA_BISSAU = "GNB", _("Guinea-Bissau")
    EQUATORIAL_GUINEA = "GNQ", _("Equatorial Guinea")
    GREECE = "GRC", _("Greece")
    GRENADA = "GRD", _("Grenada")
    GREENLAND = "GRL", _("Greenland")
    GUATEMALA = "GTM", _("Guatemala")
    FRENCH_GUIANA = "GUF", _("French Guiana")
    GUAM = "GUM", _("Guam")
    GUYANA = "GUY", _("Guyana")
    HONG_KONG = "HKG", _("Hong Kong")
    HEARD_ISLAND_AND_MCDONALD_ISLANDS = "HMD", _("Heard Island and McDonald Islands")
    HONDURAS = "HND", _("Honduras")
    CROATIA = "HRV", _("Croatia")
    HAITI = "HTI", _("Haiti")
    HUNGARY = "HUN", _("Hungary")
    INDONESIA = "IDN", _("Indonesia")
    ISLE_OF_MAN = "IMN", _("Isle of Man")
    INDIA = "IND", _("India")
    BRITISH_INDIAN_OCEAN_TERRITORY = "IOT", _("British Indian Ocean Territory")
    IRELAND = "IRL", _("Ireland")
    IRAN_ISLAMIC_REPUBLIC_OF = "IRN", _("Iran (Islamic Republic of)")
    IRAQ = "IRQ", _("Iraq")
    ICELAND = "ISL", _("Iceland")
    ISRAEL = "ISR", _("Israel")
    ITALY = "ITA", _("Italy")
    JAMAICA = "JAM", _("Jamaica")
    JERSEY = "JEY", _("Jersey")
    JORDAN = "JOR", _("Jordan")
    JAPAN = "JPN", _("Japan")
    KAZAKHSTAN = "KAZ", _("Kazakhstan")
    KENYA = "KEN", _("Kenya")
    KYRGYZSTAN = "KGZ", _("Kyrgyzstan")
    CAMBODIA = "KHM", _("Cambodia")
    KIRIBATI = "KIR", _("Kiribati")
    SAINT_KITTS_AND_NEVIS = "KNA", _("Saint Kitts and Nevis")
    KOREA_REPUBLIC_OF = "KOR", _("Korea, Republic of")
    KUWAIT = "KWT", _("Kuwait")
    LAO_PEOPLES_DEMOCRATIC_REPUBLIC = "LAO", _("Lao People's Democratic Republic")
    LEBANON = "LBN", _("Lebanon")
    LIBERIA = "LBR", _("Liberia")
    LIBYA = "LBY", _("Libya")
    SAINT_LUCIA = "LCA", _("Saint Lucia")
    LIECHTENSTEIN = "LIE", _("Liechtenstein")
    SRI_LANKA = "LKA", _("Sri Lanka")
    LESOTHO = "LSO", _("Lesotho")
    LITHUANIA = "LTU", _("Lithuania")
    LUXEMBOURG = "LUX", _("Luxembourg")
    LATVIA = "LVA", _("Latvia")
    MACAO = "MAC", _("Macao")
    SAINT_MARTIN_FRENCH_PART = "MAF", _("Saint Martin (French part)")
    MOROCCO = "MAR", _("Morocco")
    MONACO = "MCO", _("Monaco")
    MOLDOVA_REPUBLIC_OF = "MDA", _("Moldova, Republic of")
    MADAGASCAR = "MDG", _("Madagascar")
    MALDIVES = "MDV", _("Maldives")
    MEXICO = "MEX", _("Mexico")
    MARSHALL_ISLANDS = "MHL", _("Marshall Islands")
    NORTH_MACEDONIA = "MKD", _("North Macedonia")
    MALI = "MLI", _("Mali")
    MALTA = "MLT", _("Malta")
    MYANMAR = "MMR", _("Myanmar")
    MONTENEGRO = "MNE", _("Montenegro")
    MONGOLIA = "MNG", _("Mongolia")
    NORTHERN_MARIANA_ISLANDS = "MNP", _("Northern Mariana Islands")
    MOZAMBIQUE = "MOZ", _("Mozambique")
    MAURITANIA = "MRT", _("Mauritania")
    MONTSERRAT = "MSR", _("Montserrat")
    MARTINIQUE = "MTQ", _("Martinique")
    MAURITIUS = "MUS", _("Mauritius")
    MALAWI = "MWI", _("Malawi")
    MALAYSIA = "MYS", _("Malaysia")
    MAYOTTE = "MYT", _("Mayotte")
    NAMIBIA = "NAM", _("Namibia")
    NEW_CALEDONIA = "NCL", _("New Caledonia")
    NIGER = "NER", _("Niger")
    NORFOLK_ISLAND = "NFK", _("Norfolk Island")
    NIGERIA = "NGA", _("Nigeria")
    NICARAGUA = "NIC", _("Nicaragua")
    NIUE = "NIU", _("Niue")
    NETHERLANDS_KINGDOM_OF_THE = "NLD", _("Netherlands, Kingdom of the")
    NORWAY = "NOR", _("Norway")
    NEPAL = "NPL", _("Nepal")
    NAURU = "NRU", _("Nauru")
    NEW_ZEALAND = "NZL", _("New Zealand")
    OMAN = "OMN", _("Oman")
    PAKISTAN = "PAK", _("Pakistan")
    PANAMA = "PAN", _("Panama")
    PITCAIRN = "PCN", _("Pitcairn")
    PERU = "PER", _("Peru")
    PHILIPPINES = "PHL", _("Philippines")
    PALAU = "PLW", _("Palau")
    PAPUA_NEW_GUINEA = "PNG", _("Papua New Guinea")
    POLAND = "POL", _("Poland")
    PUERTO_RICO = "PRI", _("Puerto Rico")
    KOREA_DEMOCRATIC_PEOPLES_REPUBLIC_OF = "PRK", _(
        "Korea (Democratic People's Republic of)"
    )
    PORTUGAL = "PRT", _("Portugal")
    PARAGUAY = "PRY", _("Paraguay")
    PALESTINE_STATE_OF = "PSE", _("Palestine, State of")
    FRENCH_POLYNESIA = "PYF", _("French Polynesia")
    QATAR = "QAT", _("Qatar")
    RÉUNION = "REU", _("Réunion")
    ROMANIA = "ROU", _("Romania")
    RUSSIAN_FEDERATION = "RUS", _("Russian Federation")
    RWANDA = "RWA", _("Rwanda")
    SAUDI_ARABIA = "SAU", _("Saudi Arabia")
    SUDAN = "SDN", _("Sudan")
    SENEGAL = "SEN", _("Senegal")
    SINGAPORE = "SGP", _("Singapore")
    SOUTH_GEORGIA_AND_THE_SOUTH_SANDWICH_ISLANDS = "SGS", _(
        "South Georgia and the South Sandwich Islands"
    )
    SAINT_HELENA_ASCENSION_AND_TRISTAN_DA_CUNHA = "SHN", _(
        "Saint Helena, Ascension and Tristan da Cunha"
    )
    SVALBARD_AND_JAN_MAYEN = "SJM", _("Svalbard and Jan Mayen")
    SOLOMON_ISLANDS = "SLB", _("Solomon Islands")
    SIERRA_LEONE = "SLE", _("Sierra Leone")
    EL_SALVADOR = "SLV", _("El Salvador")
    SAN_MARINO = "SMR", _("San Marino")
    SOMALIA = "SOM", _("Somalia")
    SAINT_PIERRE_AND_MIQUELON = "SPM", _("Saint Pierre and Miquelon")
    SERBIA = "SRB", _("Serbia")
    SOUTH_SUDAN = "SSD", _("South Sudan")
    SAO_TOME_AND_PRINCIPE = "STP", _("Sao Tome and Principe")
    SURINAME = "SUR", _("Suriname")
    SLOVAKIA = "SVK", _("Slovakia")
    SLOVENIA = "SVN", _("Slovenia")
    SWEDEN = "SWE", _("Sweden")
    ESWATINI = "SWZ", _("Eswatini")
    SINT_MAARTEN_DUTCH_PART = "SXM", _("Sint Maarten (Dutch part)")
    SEYCHELLES = "SYC", _("Seychelles")
    SYRIAN_ARAB_REPUBLIC = "SYR", _("Syrian Arab Republic")
    TURKS_AND_CAICOS_ISLANDS = "TCA", _("Turks and Caicos Islands")
    CHAD = "TCD", _("Chad")
    TOGO = "TGO", _("Togo")
    THAILAND = "THA", _("Thailand")
    TAJIKISTAN = "TJK", _("Tajikistan")
    TOKELAU = "TKL", _("Tokelau")
    TURKMENISTAN = "TKM", _("Turkmenistan")
    TIMOR_LESTE = "TLS", _("Timor-Leste")
    TONGA = "TON", _("Tonga")
    TRINIDAD_AND_TOBAGO = "TTO", _("Trinidad and Tobago")
    TUNISIA = "TUN", _("Tunisia")
    TÜRKIYE = "TUR", _("Türkiye")
    TUVALU = "TUV", _("Tuvalu")
    TAIWAN_PROVINCE_OF_CHINA = "TWN", _("Taiwan, Province of China")
    TANZANIA_UNITED_REPUBLIC_OF = "TZA", _("Tanzania, United Republic of")
    UGANDA = "UGA", _("Uganda")
    UKRAINE = "UKR", _("Ukraine")
    UNITED_STATES_MINOR_OUTLYING_ISLANDS = "UMI", _(
        "United States Minor Outlying Islands"
    )
    URUGUAY = "URY", _("Uruguay")
    UNITED_STATES_OF_AMERICA = "USA", _("United States of America")
    UZBEKISTAN = "UZB", _("Uzbekistan")
    HOLY_SEE = "VAT", _("Holy See")
    SAINT_VINCENT_AND_THE_GRENADINES = "VCT", _("Saint Vincent and the Grenadines")
    VENEZUELA_BOLIVARIAN_REPUBLIC_OF = "VEN", _("Venezuela (Bolivarian Republic of)")
    VIRGIN_ISLANDS_BRITISH = "VGB", _("Virgin Islands (British)")
    VIRGIN_ISLANDS_US = "VIR", _("Virgin Islands (U.S.)")
    VIET_NAM = "VNM", _("Viet Nam")
    VANUATU = "VUT", _("Vanuatu")
    WALLIS_AND_FUTUNA = "WLF", _("Wallis and Futuna")
    SAMOA = "WSM", _("Samoa")
    YEMEN = "YEM", _("Yemen")
    SOUTH_AFRICA = "ZAF", _("South Africa")
    ZAMBIA = "ZMB", _("Zambia")
    ZIMBABWE = "ZWE", _("Zimbabwe")


class Address(TimeStampedModel):
    name = models.CharField(
        _("Name"),
        null=False,
        blank=True,
        max_length=255,
        help_text="Name but not required",
    )
    is_learning_center = models.BooleanField(
        _("Is Learning Center"),
        null=False,
        blank=False,
        default=False,
    )
    line_one = models.CharField(
        _("line one"),
        null=False,
        blank=False,
        max_length=255,
        help_text="Required",
    )
    line_two = models.CharField(
        _("line two"),
        null=False,
        blank=True,
        max_length=255,
        help_text="Not required",
    )
    city_town_village = models.CharField(
        _("city town or village"),
        null=False,
        blank=False,
        max_length=255,
        help_text="Required",
    )
    prefecture_state = models.CharField(
        _("prefecture or state"),
        null=False,
        blank=True,
        max_length=100,
        help_text="Not required but preferable if available",
    )
    postal_code = models.CharField(
        _("post code or zip code"),
        null=False,
        blank=True,
        max_length=100,
        help_text="Not required but preferable if available",
    )
    country = models.CharField(
        _("country"),
        null=False,
        blank=False,
        max_length=3,
        choices=CountryChoices.choices,
        default=CountryChoices.JAPAN,
        help_text="Required",
    )

    def __str__(self) -> str:
        if self.name:
            return self.name
        return self.line_one


@register_snippet
class ExperienceAddress(models.Model):
    name = models.CharField(
        _("Name"),
        null=False,
        blank=False,
        max_length=255,
        help_text="Place name in English",
    )
    display_name = models.CharField(
        _("Display name"),
        null=False,
        blank=False,
        max_length=255,
        help_text="Place name in to be displayed on site",
    )
    line_one = models.CharField(
        _("Line one"),
        null=False,
        blank=False,
        max_length=255,
        help_text="Line one to be displayed on site",
    )
    line_two = models.CharField(
        _("Line two"),
        null=False,
        blank=True,
        max_length=255,
        help_text="Line two to be displayed on site",
    )
    city_town_village = models.CharField(
        _("City town or village"),
        null=False,
        blank=False,
        max_length=255,
        help_text="city, town or village to be displayed on site",
    )
    prefecture_state = models.CharField(
        _("Prefecture or state"),
        null=False,
        blank=False,
        max_length=100,
        help_text="Prefecture to be displayed on site",
    )
    postal_code = models.CharField(
        _("Post code or zip code"),
        null=False,
        blank=True,
        max_length=100,
        help_text="Not required but preferable if available. Displayed on site",
    )
    country = models.CharField(
        _("Country"),
        null=False,
        blank=False,
        max_length=3,
        choices=CountryChoices.choices,
        default=CountryChoices.JAPAN,
        help_text="Required",
    )

    class Meta:
        verbose_name = "Experience Address"
        verbose_name_plural = "Experience Addresses"

    def __str__(self) -> str:
        return self.name


# ============= /* Intermediary Models */==================


class AddressTypeChoices(models.TextChoices):
    HOME = "HOM", _("Home")
    WORK = "WRK", _("Work")
    HEAD_OFFICE = "HOF", _("Head Office")
    BRANCH_OFFICE = "BRO", _("Branch Office")


class ContactAddress(models.Model):
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
    )
    contact_type = models.CharField(
        _("Contact type"),
        null=False,
        blank=False,
        choices=AddressTypeChoices.choices,
        default=AddressTypeChoices.HOME,
        max_length=3,
    )
    is_primary = models.BooleanField(
        _("Is primary"),
        blank=False,
        null=False,
        default=False,
    )
