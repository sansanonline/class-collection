import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="校内/院内职务统计", page_icon="📋", layout="centered")

st.title("📋 校内/院内职务统计收集表")
st.divider()

# 基本信息
name = st.text_input("姓名")
student_id = st.text_input("学号")

# 职务信息
job = st.text_input("担任职务（如：班长、学生会干事）")
department = st.text_input("所属单位（如：班级、院学生会、校团委）")
term = st.text_input("任职时间（如：2025.09-至今）（可选）")

remark = st.text_input("备注（可选）")

st.divider()

# 读取已有数据
file = "职务统计.xlsx"
if os.path.exists(file):
    df = pd.read_excel(file)
else:
    df = pd.DataFrame(columns=["姓名", "学号", "职务", "所属单位", "任职时间", "备注"])

# 提交逻辑
if st.button("✅ 提交", use_container_width=True):
    if not all([name, student_id, job]):
        st.error("⚠️ 姓名、学号、职务为必填项")
    else:
        new_data = pd.DataFrame({
            "姓名": [name],
            "学号": [student_id],
            "职务": [job],
            "所属单位": [department],
            "任职时间": [term],
            "备注": [remark]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(file, index=False)
        st.success("🎉 提交成功！")

# --- 【核心新增】下载按钮 ---
st.divider()
st.subheader("📥 管理员下载数据")
if st.button("生成 Excel 下载链接"):
    if os.path.exists(file) and not df.empty:
        # 把数据转成可下载的 Excel 格式
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        buffer.seek(0)

        # 显示下载按钮
        st.download_button(
            label="📊 点击下载 职务统计.xlsx",
            data=buffer,
            file_name="职务统计.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ 暂无提交数据，无法下载")

st.caption("仅用于班级职务统计，提交后可由管理员下载汇总")
