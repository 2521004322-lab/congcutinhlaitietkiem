import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 APP TÍNH LÃI GỬI TIẾT KIỆM")
st.write("Nhập thông tin khoản tiền gửi để tính tiền lãi và tổng số tiền nhận được.")

# =========================
# NHẬP THÔNG TIN
# =========================

st.subheader("1. Thông tin khoản tiền gửi")

tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc_nhan_lai = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

loai_lai = st.radio(
    "Loại lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ".replace(",", ".")


# =========================
# TÍNH TOÁN
# =========================

if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất theo năm -> dạng thập phân
    lai_suat_nam = lai_suat / 100

    # Số tháng
    so_thang = ky_han

    # =========================
    # LÃI ĐƠN
    # =========================
    if loai_lai == "Lãi đơn":

        # Tiền lãi mỗi tháng
        lai_moi_thang = tien_gui * lai_suat_nam / 12

        # Tổng tiền lãi
        tong_lai = tien_gui * lai_suat_nam * so_thang / 12

        # Tổng tiền cuối kỳ
        tong_tien = tien_gui + tong_lai

    # =========================
    # LÃI KÉP
    # =========================
    else:

        # Lãi suất theo tháng
        lai_suat_thang = lai_suat_nam / 12

        # Số kỳ ghép lãi
        so_ky = so_thang

        # Tổng tiền cuối kỳ
        tong_tien = tien_gui * (1 + lai_suat_thang) ** so_ky

        # Tổng tiền lãi
        tong_lai = tong_tien - tien_gui

        # Tiền lãi định kỳ
        lai_moi_thang = tien_gui * lai_suat_thang

    # =========================
    # XÁC ĐỊNH TIỀN LÃI ĐỊNH KỲ
    # =========================

    if hinh_thuc_nhan_lai == "Hàng tháng":

        tien_lai_dinh_ky = lai_moi_thang

    elif hinh_thuc_nhan_lai == "Hàng quý":

        if loai_lai == "Lãi đơn":
            tien_lai_dinh_ky = lai_moi_thang * 3
        else:
            # Tiền lãi của 3 tháng đầu tiên
            tien_lai_dinh_ky = tien_gui * (
                (1 + lai_suat_thang) ** 3 - 1
            )

    else:
        # Cuối kỳ
        tien_lai_dinh_ky = tong_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.divider()
    st.subheader("2. Kết quả tính toán")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiền lãi định kỳ",
            dinh_dang_tien(tien_lai_dinh_ky)
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            dinh_dang_tien(tong_lai)
        )

    st.success(
        f"💰 Tổng số tiền nhận được: **{dinh_dang_tien(tong_tien)}**"
    )

    # =========================
    # CHI TIẾT
    # =========================

    st.subheader("3. Chi tiết khoản tiền gửi")

    st.write(f"**Số tiền gốc:** {dinh_dang_tien(tien_gui)}")
    st.write(f"**Kỳ hạn:** {so_thang} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")
    st.write(f"**Loại lãi:** {loai_lai}")

    st.divider()

    st.write(
        f"**Tổng kết:** Gửi {dinh_dang_tien(tien_gui)} "
        f"trong {so_thang} tháng với lãi suất {lai_suat:.2f}%/năm "
        f"→ tổng tiền lãi là **{dinh_dang_tien(tong_lai)}**, "
        f"tổng số tiền nhận được là **{dinh_dang_tien(tong_tien)}**."
    )
