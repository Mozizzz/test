#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/9/30 15:29
# @Author  : LLZ
# @File    : step1.py
# @Software: PyCharm
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="GenomeDB - BW文件数据库",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)


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

    # 可视化区域 - 使用 Streamlit 内置图表
    st.subheader("📈 数据可视化")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### 实验类型分布")
        assay_counts = df['assay'].value_counts()
        st.bar_chart(assay_counts)

        # 显示一些统计数据
        st.markdown("#### 数据统计")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**文件大小分布**")
            # 模拟文件大小数据
            file_sizes = [int(x.split()[0]) for x in df['file_size']]
            st.metric("平均大小", f"{np.mean(file_sizes):.1f} MB")
            st.metric("最大大小", f"{np.max(file_sizes)} MB")

        with col2:
            st.write("**时间分布**")
            monthly_count = df.groupby(df['date_added'].dt.month).size()
            st.line_chart(monthly_count)

    with col2:
        st.markdown("#### 物种分布")
        species_counts = df['species'].value_counts()
        st.dataframe(species_counts)

        st.markdown("#### 最近添加")
        recent_datasets = df.nlargest(5, 'date_added')
        for _, row in recent_datasets.iterrows():
            st.write(f"**{row['id']}**")
            st.caption(f"{row['description']}")
            st.caption(f"添加: {row['date_added'].strftime('%Y-%m-%d')}")
            st.divider()

    # 侧边栏
    with st.sidebar:
        st.markdown("## 🧭 导航")
        st.markdown("---")
        st.markdown("### 📤 数据上传")

        uploaded_file = st.file_uploader("上传BW文件", type=['bw', 'bigwig'])
        if uploaded_file is not None:
            st.success(f"已上传: {uploaded_file.name}")

        st.markdown("---")
        st.markdown("### ℹ️ 关于")
        st.markdown("""
        **GenomeDB** 是一个开放的基因组数据浏览器和数据库。

        **功能特点:**
        - 多维度数据浏览和筛选
        - 数据可视化
        - 支持多种数据格式
        - 开放数据访问
        """)


if __name__ == "__main__":
    main()