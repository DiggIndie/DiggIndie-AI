# app/models/__init__.py
# 모든 모델을 임포트하여 SQLAlchemy relationship이 정상 작동하도록 함

from app.models.band import Band
from app.models.band_description import BandDescription
from app.models.keyword import Keyword, BandKeyword
from app.models.member import Member
from app.models.member_band import MemberBand
from app.models.member_keyword import MemberKeyword
from app.models.band_recommend import BandRecommend
from app.models.top_track import TopTrack

__all__ = [
    "Band",
    "BandDescription",
    "Keyword",
    "BandKeyword",
    "Member",
    "MemberBand",
    "MemberKeyword",
    "BandRecommend",
    "TopTrack",
]
