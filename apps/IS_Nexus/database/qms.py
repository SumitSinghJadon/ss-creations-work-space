from IntelliSync_db.models import  CommonMaster,FirstLevelMaster 
 
def get_floor_by_unit_data(unit_id):
    common_master = CommonMaster.objects.filter(master_type__code='CT-36', value=unit_id).values()
    return list(common_master)


def get_line_by_floor_data(common_id):
    first_level =FirstLevelMaster.objects.filter(master_type__code='CT-37',common_master_id=common_id).values()
    return list(first_level)