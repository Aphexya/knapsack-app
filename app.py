import streamlit as st
from knapsack import brute_force_knapsack
import pandas as pd

# Konfigurasi halaman
st.set_page_config(
    page_title="Knapsack Problem Solver",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling yang lebih baik
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .solution-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .item-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .header-gradient {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: bold;
    }
    
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header dengan gradient
st.markdown('<h1 class="header-gradient">🎒 Knapsack Problem Solver</h1>', unsafe_allow_html=True)
st.markdown("**Temukan kombinasi optimal dengan algoritma brute force yang elegan!**")

# Sidebar untuk kontrol
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan")
    
    # Pilihan jumlah barang
    num_items = st.selectbox(
        "Jumlah barang:",
        options=[3, 4, 5, 6],
        index=1,
        help="Pilih jumlah barang yang ingin dianalisis"
    )
    
    # Reset ke default
    if st.button("🔄 Reset ke Default"):
        st.rerun()

# Nilai default yang disesuaikan dengan jumlah item
default_data = {
    3: {"weights": [7, 3, 4], "values": [42, 12, 40]},
    4: {"weights": [7, 3, 4, 5], "values": [42, 12, 40, 25]},
    5: {"weights": [7, 3, 4, 5, 2], "values": [42, 12, 40, 25, 15]},
    6: {"weights": [7, 3, 4, 5, 2, 6], "values": [42, 12, 40, 25, 15, 30]}
}

default_weights = default_data[num_items]["weights"]
default_values = default_data[num_items]["values"]
default_capacity = 10

# Layout responsif untuk input data
st.markdown("### 📦 Data Barang")

# Buat kolom yang responsif
cols = st.columns(min(3, num_items))
weights = []
values = []

for i in range(num_items):
    col_idx = i % len(cols)
    with cols[col_idx]:
        st.markdown(f"**Barang {i+1}**")
        berat = st.number_input(
            f"Berat (kg)",
            value=default_weights[i] if i < len(default_weights) else 1,
            min_value=1,
            key=f"w{i}",
            help=f"Masukkan berat barang ke-{i+1}"
        )
        nilai = st.number_input(
            f"Nilai ($)",
            value=default_values[i] if i < len(default_values) else 10,
            min_value=1,
            key=f"v{i}",
            help=f"Masukkan nilai barang ke-{i+1}"
        )
        weights.append(berat)
        values.append(nilai)

# Input kapasitas dengan styling
st.markdown("### 🎯 Kapasitas Knapsack")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    capacity = st.number_input(
        "Kapasitas maksimum (kg):",
        value=default_capacity,
        min_value=1,
        help="Masukkan kapasitas maksimum knapsack"
    )

# Tombol hitung dengan spacing
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    calculate_button = st.button("🔍 Hitung Kombinasi Optimal", type="primary")

if calculate_button:
    with st.spinner('🔄 Menghitung kombinasi terbaik...'):
        max_value, best_combination, best_weight, logs = brute_force_knapsack(weights, values, capacity)
    
    # Tampilkan ringkasan dalam metric cards
    st.markdown("### 📊 Ringkasan Hasil")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Nilai Optimal</h3>
            <h2>${max_value}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚖️ Total Berat</h3>
            <h2>{best_weight} kg</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        selected_items = sum(best_combination)
        st.markdown(f"""
        <div class="metric-card">
            <h3>📦 Barang Dipilih</h3>
            <h2>{selected_items} item</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        efficiency = round((max_value / best_weight) * 100, 1) if best_weight > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚡ Efisiensi</h3>
            <h2>{efficiency}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabel evaluasi kombinasi dengan pandas
    st.markdown("### 📋 Evaluasi Semua Kombinasi")
    
    # Konversi logs ke DataFrame
    df_logs = pd.DataFrame(logs)
    df_logs.index = df_logs.index + 1
    
    # Styling untuk status
    def style_status(val):
        if val == "✅ Valid":
            return 'background-color: #d4edda; color: #155724'
        else:
            return 'background-color: #f8d7da; color: #721c24'
    
    styled_df = df_logs.style.applymap(style_status, subset=['status'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Solusi optimal dengan card styling
    st.markdown(f"""
    <div class="solution-card">
        <h2>🏆 Solusi Optimal</h2>
        <p><strong>Kombinasi Binary:</strong> {best_combination}</p>
        <p><strong>Total Berat:</strong> {best_weight} kg / {capacity} kg</p>
        <p><strong>Total Nilai:</strong> ${max_value}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detail barang yang dipilih
    st.markdown("### 📦 Detail Barang Terpilih")
    
    selected_items_details = []
    for i in range(num_items):
        if best_combination[i] == 1:
            selected_items_details.append({
                'Barang': f'Barang {i+1}',
                'Berat (kg)': weights[i],
                'Nilai ($)': values[i],
                'Rasio Nilai/Berat': round(values[i]/weights[i], 2)
            })
    
    if selected_items_details:
        df_selected = pd.DataFrame(selected_items_details)
        st.dataframe(df_selected, use_container_width=True)
        
        # Visualisasi dengan progress bars
        st.markdown("### 📊 Visualisasi Kapasitas")
        usage_percentage = (best_weight / capacity) * 100
        st.progress(usage_percentage / 100)
        st.markdown(f"**Penggunaan Kapasitas: {usage_percentage:.1f}%** ({best_weight}/{capacity} kg)")
    else:
        st.warning("⚠️ Tidak ada barang yang dapat dimasukkan ke dalam knapsack dengan kapasitas yang diberikan.")

# Footer dengan informasi tambahan
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>💡 <strong>Tips:</strong> Algoritma brute force mengevaluasi semua kemungkinan kombinasi untuk menemukan solusi optimal.</p>
    <p>Dibuat dengan ❤️ menggunakan Streamlit</p>
</div>
""", unsafe_allow_html=True)