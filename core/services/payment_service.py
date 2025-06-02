from core.models import PHI_THANHTOAN

def get_thang_no(ma_hd):
    """
    Lấy danh sách các tháng chưa thanh toán của một hợp đồng
    """
    return PHI_THANHTOAN.objects.filter(
        MA_HD=ma_hd,
        DA_THANH_TOAN='N'
    ).values_list('THANG_NAM', flat=True)