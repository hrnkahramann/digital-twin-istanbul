import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import random
import pandas as pd
from datetime import datetime
import numpy as np
import os

from simulation import SensorNode
from weather import get_weather

# ================= CONFIG =================
st.set_page_config(layout="wide")
st.title("🌍 Digital Twin – Istanbul IoT Simulation")

TRACKED_METRICS = ["temperature", "humidity", "battery"]

UNIT_MAP = {
    "temperature": "°C",
    "humidity": "%",
    "battery": "%"
}

# ================= DATA STORAGE =================
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "sensor_log.csv")
os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(CSV_PATH):
    pd.DataFrame(
        columns=[
            "time", "node_id",
            "temperature", "humidity", "battery",
            "lat", "lon", "scenario"
        ]
    ).to_csv(CSV_PATH, index=False)

# ================= SESSION =================
defaults = {
    "nodes": [],
    "selected_node": None,
    "running": False,
    "scenario": "Normal",
    "update_count": 0
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ================= SCENARIO EFFECT =================
def apply_scenario(node):
    s = st.session_state.scenario
    if s == "Normal":
        return

    if s == "Sıcak Hava":
        node.data["temperature"] += random.uniform(1, 2)
        node.data["humidity"] -= random.uniform(5, 10)
        node.data["battery"] -= random.uniform(2, 4)

    elif s == "Nemli Ortam":
        node.data["humidity"] += random.uniform(3, 6)
        node.data["temperature"] -= random.uniform(0.5, 1.5)
        node.data["battery"] -= random.uniform(1, 2)

    elif s == "Düşük Batarya":
        node.data["battery"] -= random.uniform(5, 10)

    node.data["temperature"] = float(np.clip(node.data["temperature"], -20, 50))
    node.data["humidity"] = float(np.clip(node.data["humidity"], 0, 100))
    node.data["battery"] = float(np.clip(node.data["battery"], 0, 100))

# ================= NODE CREATION =================
def create_nodes():
    nodes = []
    for _ in range(random.randint(5, 12)):
        lat = random.uniform(40.90, 41.10)
        lon = random.uniform(28.80, 29.20)

        node = SensorNode(lat, lon)
        node.update(get_weather(lat, lon))

        node.prev = {k: None for k in TRACKED_METRICS}
        node.normal_snapshot = None
        node.prev_normal_snapshot = None

        node.history = {k: [] for k in TRACKED_METRICS}
        node.history["time"] = []

        now = datetime.now()
        for k in TRACKED_METRICS:
            node.history[k].append(float(node.data[k]))
        node.history["time"].append(now)

        nodes.append(node)
    return nodes

# ================= UPDATE =================
def update_all_nodes():
    now = datetime.now()
    rows = []

    for n in st.session_state.nodes:

        # önceki senaryolu değerler
        for k in TRACKED_METRICS:
            n.prev[k] = float(n.data[k])

        # önceki normal snapshot
        if n.normal_snapshot:
            n.prev_normal_snapshot = n.normal_snapshot.copy()

        # NORMAL
        n.update(get_weather(n.latitude, n.longitude))
        n.normal_snapshot = {k: float(n.data[k]) for k in TRACKED_METRICS}

        # SENARYO
        apply_scenario(n)

        for k in TRACKED_METRICS:
            n.history[k].append(float(n.data[k]))
        n.history["time"].append(now)

        rows.append({
            "time": now,
            "node_id": n.id,
            "temperature": n.data["temperature"],
            "humidity": n.data["humidity"],
            "battery": n.data["battery"],
            "lat": n.latitude,
            "lon": n.longitude,
            "scenario": st.session_state.scenario
        })

    pd.DataFrame(rows).to_csv(CSV_PATH, mode="a", header=False, index=False)
    st.session_state.update_count += 1

# ================= SIDEBAR =================
st.sidebar.header("Simulation")

if st.sidebar.button("▶ Sistemi Başlat"):
    st.session_state.nodes = create_nodes()
    st.session_state.running = True
    st.session_state.selected_node = None
    st.session_state.update_count = 0

if st.sidebar.button("⏹ Sistemi Durdur"):
    st.session_state.running = False
    st.session_state.nodes = []
    st.session_state.selected_node = None

st.session_state.scenario = st.sidebar.selectbox(
    "🌦 Senaryo",
    ["Normal", "Sıcak Hava", "Nemli Ortam", "Düşük Batarya"]
)

if st.sidebar.button("🔄 Tek Güncelle") and st.session_state.running:
    update_all_nodes()
    st.success("Veriler güncellendi")

metric = st.sidebar.selectbox("Gösterilecek Veri", ["ALL"] + TRACKED_METRICS)
visible_metrics = TRACKED_METRICS if metric == "ALL" else [metric]

# ================= LAYOUT =================
left, right = st.columns([2.6, 1.4])

# ================= MAP =================
if st.session_state.running:
    with left:
        m = folium.Map(location=[41.01, 28.97], zoom_start=10)
        heat_data = []

        for node in st.session_state.nodes:
            val = np.mean([node.data[k] for k in TRACKED_METRICS]) if metric == "ALL" else node.data[metric]

            folium.Marker(
                [node.latitude, node.longitude],
                tooltip=f"NODE {node.id}",
                icon=folium.Icon(icon="signal", prefix="fa")
            ).add_to(m)

            heat_data.append([node.latitude, node.longitude, val])

        HeatMap(heat_data, radius=30, blur=18).add_to(m)
        map_data = st_folium(m, height=520, returned_objects=["last_object_clicked"])
else:
    with left:
        st.info("🚫 Sistem kapalı")

# ================= NODE SELECT =================
if st.session_state.running and map_data and map_data.get("last_object_clicked"):
    lat = map_data["last_object_clicked"]["lat"]
    for n in st.session_state.nodes:
        if abs(n.latitude - lat) < 0.00001:
            st.session_state.selected_node = n
            break

# ================= RIGHT PANEL =================
with right:
    if not st.session_state.running:
        st.warning("📴 Sistem durduruldu")
        st.stop()

    # ---------- NODE SEÇİLİ DEĞİL ----------
    if not st.session_state.selected_node:

        if metric == "ALL":
            st.subheader("📊 Tüm Nodelar – Genel Durum")
            df_all = pd.DataFrame([{k: n.data[k] for k in TRACKED_METRICS} for n in st.session_state.nodes])

            cols = st.columns(len(TRACKED_METRICS))
            for col, key in zip(cols, TRACKED_METRICS):
                col.metric(key.capitalize(), f"{df_all[key].mean():.2f}{UNIT_MAP[key]}")

            st.line_chart(df_all)

        else:
            st.subheader(f"📊 Tüm Node’lar – {metric.capitalize()}")
            data = {f"Node {n.id}": n.data[metric] for n in st.session_state.nodes}
            df_metric = pd.DataFrame.from_dict(data, orient="index", columns=[metric.capitalize()])
            st.bar_chart(df_metric)

        st.stop()

    # ---------- NODE SEÇİLİ ----------
    n = st.session_state.selected_node
    df = pd.DataFrame(n.history).set_index("time")

    st.subheader(f"📡 NODE {n.id}")
    st.caption(f"🌦 Aktif Senaryo: {st.session_state.scenario}")

    if st.session_state.scenario == "Normal":
        cols = st.columns(len(visible_metrics))
        for col, key in zip(cols, visible_metrics):
            cur = n.data[key]
            prev = n.prev[key]
            delta = None if prev is None else cur - prev
            col.metric(key.capitalize(), f"{cur:.2f}{UNIT_MAP[key]}", None if delta is None else f"{delta:+.2f}")

        st.line_chart(df[visible_metrics].tail(30))
        st.line_chart(df[visible_metrics].diff().dropna().tail(30))

    else:
        lc, rc = st.columns(2)

        with lc:
            st.subheader("🟢 Normal")
            cols = st.columns(len(visible_metrics))
            for col, key in zip(cols, visible_metrics):
                cur = n.normal_snapshot[key]
                prev = n.prev_normal_snapshot[key] if n.prev_normal_snapshot else None
                delta = None if prev is None else cur - prev
                col.metric(key.capitalize(), f"{cur:.2f}{UNIT_MAP[key]}", None if delta is None else f"{delta:+.2f}")
            st.line_chart(df[visible_metrics].tail(30))

        with rc:
            st.subheader(f"🟡 {st.session_state.scenario}")
            cols = st.columns(len(visible_metrics))
            for col, key in zip(cols, visible_metrics):
                cur = n.data[key]
                prev = n.prev[key]
                delta = None if prev is None else cur - prev
                col.metric(key.capitalize(), f"{cur:.2f}{UNIT_MAP[key]}", None if delta is None else f"{delta:+.2f}")
            st.line_chart(df[visible_metrics].tail(30))

        st.subheader(f"📉 Normal – {st.session_state.scenario} Karşılaştırması")
        comp = pd.DataFrame({
            "Normal": {k: n.normal_snapshot[k] for k in visible_metrics},
            st.session_state.scenario: {k: n.data[k] for k in visible_metrics}
        })
        st.bar_chart(comp)

    with open(CSV_PATH, "rb") as f:
        st.download_button("📥 CSV İndir", f, "iot_sensor_data.csv")
