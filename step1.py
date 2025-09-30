#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/9/30 15:29
# @Author  : LLZ
# @File    : step1.py
# @Software: PyCharm
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="GenomeDB - BW文件数据库",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 添加缓存装饰器以提高性能
@st.cache_data
def load_data():
    """加载和生成示例数据"""
    datasets = []
    species_options = ["人类", "小鼠", "大鼠", "果蝇", "斑马鱼"]
    cell_type_options = ["HEK293", "HeLa", "K562", "MCF-7", "神经元"]
    condition_options = ["正常", "缺氧", "药物治疗", "基因敲除", "过表达"]
    assay_options = ["ChIP-seq", "ATAC-seq", "RNA-seq", "WGBS", "Hi-C"]

    for i in range(50):
        dataset = {
            "id": f"GSM{4056780 + i}",
            "description": f"{assay_options[i % 5]} in {cell_type_options[i % 5]} cells under {condition_options[i % 5]} condition",
            "species": species_options[i % 5],
            "cell_type": cell_type_options[i % 5],
            "condition": condition_options[i % 5],
            "assay": assay_options[i % 5],
            "file_size": f"{np.random.randint(100, 600)} MB",
            "date_added": datetime(2023, np.random.randint(1, 13), np.random.randint(1, 28))
        }
        datasets.append(dataset)

    return pd.DataFrame(datasets)


def main():
    # 加载数据
    df = load_data()

    # 应用标题
    st.title("🧬 GenomeDB - BW文件数据库")
    st.markdown("探索、可视化和分析不同实验条件下的BW文件数据")

    # 统计信息
    st.subheader("📊 数据概览")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("BW文件", len(df))
    with col2:
        st.metric("物种", df['species'].nunique())
    with col3:
        st.metric("细胞类型", df['cell_type'].nunique())
    with col4:
        st.metric("实验类型", df['assay'].nunique())

    # 筛选区域
    st.subheader("🔍 筛选数据集")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        species_filter = st.selectbox("物种", ["全部"] + list(df['species'].unique()))
    with col2:
        cell_type_filter = st.selectbox("细胞类型", ["全部"] + list(df['cell_type'].unique()))
    with col3:
        condition_filter = st.selectbox("实验条件", ["全部"] + list(df['condition'].unique()))
    with col4:
        assay_filter = st.selectbox("实验类型", ["全部"] + list(df['assay'].unique()))

    # 应用筛选
    filtered_df = df.copy()
    if species_filter != "全部":
        filtered_df = filtered_df[filtered_df['species'] == species_filter]
    if cell_type_filter != "全部":
        filtered_df = filtered_df[filtered_df['cell_type'] == cell_type_filter]
    if condition_filter != "全部":
        filtered_df = filtered_df[filtered_df['condition'] == condition_filter]
    if assay_filter != "全部":
        filtered_df = filtered_df[filtered_df['assay'] == assay_filter]

    # 搜索功能
    search_term = st.text_input("🔎 搜索数据集", placeholder="输入关键词搜索...")
    if search_term:
        filtered_df = filtered_df[filtered_df['description'].str.contains(search_term, case=False)]

    # 数据表格
    st.subheader("📋 数据集列表")

    if len(filtered_df) > 0:
        # 使用Streamlit原生的dataframe显示
        st.dataframe(
            filtered_df,
            column_config={
                "id": "数据集ID",
                "description": "描述",
                "species": "物种",
                "cell_type": "细胞类型",
                "condition": "实验条件",
                "assay": "实验类型",
                "file_size": "文件大小"
            },
            hide_index=True,
            use_container_width=True
        )

        st.info(f"显示 1-{len(filtered_df)} 条，共 {len(filtered_df)} 条记录")

        # 下载按钮
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 下载筛选结果 (CSV)",
            data=csv,
            file_name="genomedb_datasets.csv",
            mime="text/csv"
        )
    else:
        st.warning("没有找到匹配的数据集")

    # 可视化区域
    st.subheader("📈 数据可视化")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### 基因组浏览器视图")

        # 创建模拟的基因组浏览器视图
        fig = go.Figure()

        # 添加模拟的基因轨迹
        x_values = list(range(1000, 1100))
        y_values = np.sin(np.array(x_values) / 5) * 10 + 15 + np.random.normal(0, 2, 100)

        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines',
            fill='tozeroy',
            line=dict(color='#3498db'),
            name='信号强度'
        ))

        fig.update_layout(
            title="模拟基因组信号 - 染色体1: 1,000,000-1,000,500",
            xaxis_title="基因组位置",
            yaxis_title="信号强度",
            height=400,
            showlegend=True,
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 数据分布")

        # 创建饼图显示实验类型分布
        assay_counts = df['assay'].value_counts()
        fig_pie = px.pie(
            values=assay_counts.values,
            names=assay_counts.index,
            title="实验类型分布"
        )

        st.plotly_chart(fig_pie, use_container_width=True)

        # 最近添加的数据集
        st.markdown("#### 最近添加")
        recent_datasets = df.nlargest(5, 'date_added')
        for _, row in recent_datasets.iterrows():
            with st.expander(f"**{row['id']}**"):
                st.write(f"{row['description']}")
                st.caption(f"添加时间: {row['date_added'].strftime('%Y-%m-%d')}")

    # 侧边栏
    with st.sidebar:
        st.markdown("## 🧭 导航")

        st.markdown("---")
        st.markdown("### 📤 数据上传")

        uploaded_file = st.file_uploader("上传BW文件", type=['bw', 'bigwig'])
        if uploaded_file is not None:
            st.success(f"已上传: {uploaded_file.name}")

            # 显示上传文件的元数据表单
            with st.form("metadata_form"):
                st.markdown("### 文件元数据")
                dataset_id = st.text_input("数据集ID")
                description = st.text_area("描述")
                species = st.selectbox("物种", ["人类", "小鼠", "大鼠", "果蝇", "斑马鱼", "其他"])
                cell_type = st.text_input("细胞类型")
                condition = st.selectbox("实验条件", ["正常", "缺氧", "药物治疗", "基因敲除", "过表达", "其他"])
                assay_type = st.selectbox("实验类型", ["ChIP-seq", "ATAC-seq", "RNA-seq", "WGBS", "Hi-C", "其他"])

                submitted = st.form_submit_button("提交元数据")
                if submitted:
                    st.success("元数据已提交！")

        st.markdown("---")
        st.markdown("### ℹ️ 关于")
        st.markdown("""
        **GenomeDB** 是一个开放的基因组数据浏览器和数据库，为研究人员提供高质量的多组学数据。

        **功能特点:**
        - 多维度数据浏览和筛选
        - 集成基因组浏览器
        - 支持多种数据格式
        - 开放数据访问

        **技术支持:**
        - 📧 contact@genomedb.org
        - 🌐 www.genomedb.org
        """)


if __name__ == "__main__":
    main()