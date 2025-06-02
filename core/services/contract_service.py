from datetime import datetime
from core.models import HOPDONG, PHI_COI, PHI_QUANLY

def tinh_phi_thang(hopdong, thang_nam):
    """
    Tính phí bảo hiểm cho một tháng cụ thể của hợp đồng
    """
    try:
        ngay_tinh = datetime.strptime(thang_nam, '%Y-%m')
        
        # Lấy tuổi của khách hàng tại thời điểm tính phí
        tuoi = ngay_tinh.year - hopdong.MA_KH.NGAY_SINH.year
        
        # Lấy phí cơ bản theo tuổi và mệnh giá
        phi_coi = PHI_COI.objects.get(
            MA_SP=hopdong.MA_SP,
            TUOI=tuoi,
            MENH_GIA=hopdong.MENH_GIA
        )
        
        # Lấy phí quản lý
        phi_quanly = PHI_QUANLY.objects.get(MA_SP=hopdong.MA_SP)
        
        # Tính tổng phí
        tong_phi = phi_coi.PHI + phi_quanly.PHI
        
        # Áp dụng chiết khấu nếu có
        if hopdong.CHIET_KHAU:
            tong_phi = tong_phi * (1 - hopdong.CHIET_KHAU / 100)
            
        return round(tong_phi, 2)
        
    except (ValueError, PHI_COI.DoesNotExist, PHI_QUANLY.DoesNotExist):
        return None