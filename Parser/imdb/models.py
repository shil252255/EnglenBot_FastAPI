from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum, Float, Table, create_engine


SQL_URL = "sqlite:///./database.db"

Base = declarative_base()

engine = create_engine(SQL_URL, connect_args={"check_same_thread": False}, echo=False)

title_types = (
    'SHORT', 'MOVIE', 'TVSERIES', 'TVSHORT', 'TVMOVIE', 'TVEPISODE', 'TVMINISERIES', 'TVSPECIAL',
    'VIDEO', 'VIDEOGAME', 'TVPILOT',
)

regions = (
    'UA', 'DE', 'HU', 'GR', 'RU', 'US', 'JP', 'FR', 'RO', 'GB', 'CA', 'PT', 'AU', 'ES', 'FI', 'PL', 'AR', 'RS', 'UY',
    'IT', 'BR', 'DK', 'TR', 'XWW', 'XEU', 'SK', 'CZ', 'SE', 'NZ', 'MX', 'NO', 'XYU', 'AT', 'VE', 'CSHH', 'SI', 'SUHH',
    'IN', 'TW', 'LT', 'NL', 'CO', 'IR', 'BG', 'SG', 'BE', 'VN', 'HR', 'DZ', 'CH', 'BF', 'PH', 'XWG', 'HK', 'CN', 'XSA',
    'EE', 'IS', 'PR', 'DDDE', 'IL', 'EG', 'XKO', 'CL', 'IE', 'JM', 'KR', 'PE', 'GE', 'BY', 'BA', 'AE', 'PA', 'TH', 'ZA',
    'TJ', 'XSI', 'MY', 'LV', 'ID', 'PK', 'BD', 'CU', 'AL', 'BO', 'EC', 'XAS', 'CR', 'PY', 'DO', 'GT', 'SV', 'UZ',
    'BUMM', 'YUCS', 'XPI', 'BJ', 'AZ', 'NG', 'CM', 'MA', 'GL', 'MN', 'LI', 'LU', 'MZ', 'BM', 'KZ', 'MD', 'LB', 'IQ',
    'TM', 'MK', 'TN', 'HT', 'AM', 'LK', 'ME', 'CG', 'CI', 'SY', 'NP', 'QA', 'TO', 'SN', 'GH', 'JO', 'KP', 'KG', 'NE',
    'GN', 'VDVN', 'TD', 'SO', 'SD', 'MC', 'TT', 'GA', 'BS', 'LY', 'AO', 'KH', 'MR', 'AF', 'MG', 'ML', 'GY', 'CY', 'ET',
    'GU', 'SR', 'MT', 'TG', 'PG', 'MU', 'BI', 'CF', 'NI', 'ZW', 'ZM', 'GW', 'DJ', 'RW', 'TZ', 'GI', 'LA', 'SC', 'GP',
    'XAU', 'FO', 'PS', 'ZRCD', 'MO', 'AW', 'KW', 'CV', 'SL', 'SM', 'CD', 'BT', 'LS', 'HN', 'KE', 'MQ', 'AD', 'ER', 'NA',
    'MM', 'SA', 'CSXX', 'IM', 'XKV', 'BH', 'BB', 'BZ', 'UG', 'AG', 'NU', 'OM', 'BW', 'LR', 'AN', 'MV', 'YE', 'GM', 'KY',
    'NC', 'DM', 'TL', 'MP', 'VA', 'GQ', 'FJ', 'SZ', 'RE', 'EH', 'PF', 'VG', 'LC', 'MW', 'BN', 'ST', 'KM', 'FM', 'AI',
    'GD', 'VI', 'SB', 'GF', 'AQ', 'MH', 'CW', 'WS', 'VC', 'AS', 'XNA', 'MS', 'VU', 'SH', 'KI', 'KN', 'CC', 'GS', 'TV',
    'CK', 'PW', 'NR', 'JE', 'TC',
)

title_languages = (
    'ja', 'en', 'sv', 'tr', 'es', 'sr', 'cs', 'ru', 'fr', 'hi', 'sk', 'fa', 'bg', 'ca', 'qbn', 'nl', 'pt', 'cmn', 'uz',
    'uk', 'qbp', 'ar', 'rn', 'bs', 'ga', 'de', 'th', 'yi', 'ka', 'hr', 'sl', 'he', 'it', 'tg', 'yue', 'kk', 'bn', 'da',
    'el', 'fi', 'be', 'gsw', 'gl', 'eu', 'az', 'ms', 'pl', 'id', 'mr', 'qbo', 'mi', 'ta', 'lt', 'lv', 'af', 'la', 'hy',
    'ur', 'te', 'ml', 'tl', 'mk', 'et', 'gd', 'cy', 'qal', 'ro', 'xh', 'gu', 'kn', 'eka', 'ko', 'ky', 'wo', 'no', 'is',
    'hu', 'sq', 'vi', 'zh', 'tk', 'pa', 'sd', 'ps', 'zu', 'ku', 'roa', 'tn', 'rm', 'su', 'jv', 'lb', 'st', 'prs', 'fro',
    'haw', 'mn', 'lo', 'my', 'am', 'qac', 'ne', 'myv', 'br', 'iu', 'cr',
)

genres_association_table = Table(
    "genres_association_table",
    Base.metadata,
    Column("title_id", ForeignKey("basics_titles.id")),
    Column("genre_id", ForeignKey("genres.id")),)


class BasicsTitle(Base):
    """Contains the following information for titles"""

    __tablename__ = 'basics_titles'

    id = Column(Integer, primary_key=True, unique=True, nullable=False, comment='alphanumeric unique identifier of the title')
    titleType = Column(Enum(title_types), comment='the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)')
    isAdult = Column(Boolean,  comment='0: non-adult title; 1: adult title')
    startYear = Column(Integer,  comment='represents the release year of a title. In the case of TV Series, it is the series start year')
    endYear = Column(Integer, nullable=True, comment='TV Series end year. \\N for all other title types')
    runtimeMinutes = Column(Integer, comment='Column primary runtime of the title, in minutes')

    genres = relationship("Genre", secondary=genres_association_table)

    def __repr__(self):
        return f'<Title Model: id = {self.id}, titleType = {self.titleType}, primaryTitle = {self.primaryTitle}, ' \
               f'isAdult = {self.isAdult}, startYear = {self.startYear}, endYear = {self.endYear}, ' \
               f'runtimeMinutes= {self.runtimeMinutes}, genres = {self.genres}>'


class Rating(Base):
    """Contains the IMDb rating and votes information for titles"""

    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    title_id = Column(ForeignKey("basics_titles.id"), comment='alphanumeric unique identifier of the title')
    averageRating = Column(Float, comment='weighted average of all the individual user ratings')
    numVotes = Column(Integer, comment='number of votes the title has received')

    def __str__(self):
        return f'{self.averageRating}({self.numVotes})'

    def __repr__(self):
        return self.__str__()


class Genre(Base):
    """Contains genre information"""

    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return self.name


class TitlesAkas(Base):

    __tablename__ = 'akas'

    id = Column(Integer, primary_key=True)
    title_id = Column(ForeignKey('basics_titles.id'), comment='a tconst, an alphanumeric unique identifier of the title')
    ordering = Column(Integer, comment='a number to uniquely identify rows for a given titleId')
    title = Column(String, comment='the localized title')
    region = Column(Enum(regions), comment='the region for this version of the title')
    language = Column(Enum(title_languages), comment=' the language of the title')
    isOriginalTitle = Column(Boolean, comment='0: not original title; 1: original title')

    def __str__(self):
        return f'[{self.title_id}] - {self.title}({self.region}/{self.language})'

    def __repr__(self):
        return self.__str__()

