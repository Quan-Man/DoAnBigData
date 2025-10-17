import streamlit as st
import pandas as pd
from hdfs import InsecureClient
from io import StringIO
import psycopg2
from update import update_all_jobs


# --- Kết nối HDFS ---
client = InsecureClient("http://localhost:9870", user="hadoopthanhtruc")

st.title("Phân tích dữ liệu mỹ phẩm trên nền tảng Tiki và Hasaki")

# --- PHẦN TIKI ---
st.write("### 🔹 Phân tích dữ liệu từ Tiki")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Số lượt đánh giá theo phân loại sản phẩm (Tiki)"):
        with client.read("/user/hadoopthanhtruc/tiki_output_job1/part-00000") as reader:
            df = pd.read_csv(reader, sep="\t", names=["Tên sản phẩm", "Số đánh giá"])
            st.dataframe(df)

with col2:
    if st.button("Trung bình điểm đánh giá theo thương hiệu (Tiki)"):
        with client.read("/user/hadoopthanhtruc/tiki_output_job2/part-00000") as reader:
            df = pd.read_csv(reader, sep="\t", names=["Thương hiệu", "Điểm TB"])
            st.dataframe(df)

with col3:
    if st.button("Phân bố giá sản phẩm (Tiki)"):
        with client.read("/user/hadoopthanhtruc/tiki_output_job3/part-00000") as reader:
            df = pd.read_csv(reader, sep="\t", names=["Khoảng giá", "Số lượng"])
            st.dataframe(df)

# --- PHẦN HASAKI ---
st.write("---")
st.write("### 🔹 Phân tích dữ liệu từ Hasaki")

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("Top sản phẩm có nhiều đánh giá nhất (Hasaki)"):
        with client.read("/user/hadoopthanhtruc/hasaki_output_job1/part-00000") as reader:
            df = pd.read_csv(reader, sep="\t", names=["Tên sản phẩm", "Số đánh giá"])
            st.dataframe(df)

with col5:
    if st.button("Trung bình điểm đánh giá theo thương hiệu (Hasaki)"):
        with client.read("/user/hadoopthanhtruc/hasaki_output_job2/part-00000") as reader:
            df = pd.read_csv(reader, sep="\t", names=["Thương hiệu", "Điểm TB"])
            st.dataframe(df)

with col6:
    if st.button("Phân bố giá sản phẩm (Hasaki)"):
        with client.read("/user/hadoopthanhtruc/hasaki_output_job3/part-00000") as reader:
            df = pd.read_csv(reader, sep="\t", names=["Khoảng giá", "Số lượng"])
            st.dataframe(df)

# Phần So sánh giữa 2 nền tảng
st.write("---")
st.write("### 🔹 So sánh dữ liệu giữa Tiki và Hasaki")

col7, col8 = st.columns(2)

with col7:
    if st.button("So sánh giá trung bình theo thương hiệu"):
        try:
            with client.read("/user/hadoopthanhtruc/tiki_hasaki_output_price/part-00000") as reader:
                df = pd.read_csv(reader, sep="\t", header=None, names=["Thương hiệu", "Tiki_avg", "Hasaki_avg", "Chênh lệch (%)"])
                st.dataframe(df)
        except Exception as e:
            st.error(f"Lỗi đọc dữ liệu: {e}")

with col8:
    if st.button("So sánh điểm đánh giá trung bình giữa hai nền tảng"):
        try:
            with client.read("/user/hadoopthanhtruc/tiki_hasaki_output_rating/part-00000") as reader:
                df = pd.read_csv(reader, sep="\t", header=None, names=["Thương hiệu", "Tiki_avg_rating", "Hasaki_avg_rating"])
                st.dataframe(df)
        except Exception as e:
            st.error(f"Lỗi đọc dữ liệu: {e}")

# --- Kết nối PostgreSQL ---
def get_connection():
    return psycopg2.connect(
        dbname="bigdata",
        user="sqoopdb",
        password="13062005",
        host="localhost",
        port="5432"
    )
    
# --- Load lại các mapreduce có liên quan đến CRUD ---
st.header("Cập nhật toàn bộ kết quả MapReduce có liên quan đến dữ liệu mới")

if st.button("Chạy lại Job MapReduce trên tập Hasaki"):
    progress = st.progress(0)
    logs = ""

    def progress_callback(p):
        progress.progress(p)

    def log_callback(msg):
        st.write(msg)

    logs = update_all_jobs(progress_callback, log_callback)
    st.success("Cập nhật hoàn tất!")
    with st.expander("Log chi tiết"):
        st.text(logs)

    # ⚡ Thay st.experimental_rerun() bằng st.rerun()
    st.session_state["updated"] = True
    st.rerun()

# --- CRUD ---
st.write("---")
st.header("Quản lý dữ liệu Hasaki (CRUD trên PostgreSQL)")

# --- Tìm kiếm sản phẩm ---
st.subheader("Tìm kiếm sản phẩm theo tên")
search_keyword = st.text_input("Nhập từ khóa")

if st.button("Tìm kiếm"):
    conn = get_connection()
    query = """
        SELECT * FROM hasaki
        WHERE LOWER(product_name) LIKE LOWER(%s)
        ORDER BY id DESC
        LIMIT 20;
    """
    df = pd.read_sql_query(query, conn, params=(f"%{search_keyword}%",))
    conn.close()

    if df.empty:
        st.warning("Không tìm thấy sản phẩm nào khớp với từ khóa.")
    else:
        st.success(f"Tìm thấy {len(df)} sản phẩm:")
        st.dataframe(df)


# --- Thêm sản phẩm ---
st.subheader("Thêm sản phẩm mới")
with st.form("add_product"):
    product_name = st.text_input("Tên sản phẩm")
    price_vnd = st.number_input("Giá (VNĐ)", min_value=0)
    brand = st.text_input("Thương hiệu")
    sold = st.number_input("Đã bán", min_value=0)
    rating = st.number_input("Điểm đánh giá", min_value=0.0, max_value=5.0, step=0.1)
    review_count = st.number_input("Số lượng đánh giá", min_value=0)
    category = st.text_input("Danh mục")
    submitted = st.form_submit_button("Thêm")

    if submitted:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO hasaki (product_name, price_vnd, brand, sold, rating, review_count, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (product_name, price_vnd, brand, sold, rating, review_count, category))
        conn.commit()
        conn.close()
        st.success("Đã thêm sản phẩm mới!")

# --- Xóa sản phẩm ---
st.subheader("Xóa sản phẩm")
delete_name = st.text_input("Nhập id sản phẩm để xóa")
if st.button("Xóa"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM hasaki WHERE id = %s;", (delete_name,))
    conn.commit()
    conn.close()
    st.warning(f"Đã xóa sản phẩm: {delete_name}")

# --- Cập nhật điểm đánh giá ---
st.subheader("Cập nhật điểm đánh giá sản phẩm")
update_name = st.text_input("Tên sản phẩm cần cập nhật điểm đánh giá")
new_rating = st.number_input("Điểm mới", min_value=0.0, max_value=5.0, step=0.1)
if st.button("Cập nhật"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE hasaki SET rating = %s WHERE product_name = %s;", (new_rating, update_name))
    conn.commit()
    conn.close()
    st.success(f"Đã cập nhật điểm đánh giá cho: {update_name}")