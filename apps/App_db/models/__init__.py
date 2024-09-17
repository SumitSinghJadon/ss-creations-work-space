from App_db.models import file_handover_mt

from .manpower_planning import ManpowerplanMT
from .manpower_hr import ManpowerHrMt
from .mmr import MmrMT
from .ot_approval import OtApproval
from .ot_master import OTMT
from .buyer_claim import BuyerClaimModel
from .energy_cost_model import EnergyCost
from .over_head_model import OverHeadMT
# OverHeadMT = OverHeadMT = []
# TNA

from .TnA.tna_template import TnaTemplateMt, TnaTemplateDt
from .TnA.tna_entry import TnaEntryMt, TnaEntryDt


# TnaActivityMaster = TnaTemplateMt = TnaTemplateDt = []