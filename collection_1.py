import streamlit as st
import pandas as pd
import os

# 页面配置
st.set_page_config(
    page_title="校内/院内职务统计",
    page_icon="📋",
    layout="centered"
)

# 标题
st.title("📋 校内/院内职务统计收集表")
st.divider()

# 基础信息
name = st.text_input("姓名")
student_id = st.text_input("学号")

# 职务信息
job = st.text_input("担任职务（如：某某部部员）")
department = st.text_input("所属单位（如：院学生会、校团委、校青协）")
term = st.text_input("任职时间（如：2025.09-至今）（可选）")

# 备注
remark = st.text_input("备注（可选）")

st.divider()

# 提交
if st.button("✅ 提交", use_container_width=True):
    if not name or not student_id or not job:
        st.error("⚠️ 姓名、学号、职务不能为空")
    else:
        file = "职务统计结果.xlsx"

        data = {
            "姓名": [name],
            "学号": [student_id],
            "职务": [job],
            "所属单位": [department],
            "任职时间": [term],
            "备注": [remark]
        }

        df_new = pd.DataFrame(data)

        if os.path.exists(file):
            df_old = pd.read_excel(file)
            df = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df = df_new

        df.to_excel(file, index=False)
        st.success("🎉 提交成功！")

st.caption("仅用于班级校内/院内职务统计")