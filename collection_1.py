import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="校内/院内职务统计", page_icon="📋", layout="centered")

st.title("📋 校内/院内职务统计收集表")
st.divider()

# ---------------------- 同学可见：仅提交表单 ----------------------
name = st.text_input("姓名")
student_id = st.text_input("学号")
job = st.text_input("担任职务（如：校青协部员、学生会干事）")
department = st.text_input("所属单位（如：校青协、院学生会、校团委）")
term = st.text_input("任职时间（如：2025.09-至今）（可选）")
remark = st.text_input("备注（可选）")

st.divider()

# 初始化Excel文件
file = "职务统计.xlsx"
if os.path.exists(file):
    df = pd.read_excel(file)
else:
    df = pd.DataFrame(columns=["姓名", "学号", "职务", "所属单位", "任职时间", "备注"])

# 提交逻辑（同学可用）
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

# ---------------------- 管理员专属区（密码锁） ----------------------
st.divider()
st.subheader("🔐 管理员操作区")

# 1. 密码验证（改成你自己的密码，比如学号后6位）
admin_pwd = st.text_input("请输入管理员密码", type="password")
correct_pwd = "0254640"  # 这里改成你的专属密码！

if admin_pwd == correct_pwd:
    st.success("✅ 管理员身份验证通过")
    
    # 2. 查看所有提交数据
    st.write("### 📊 已提交数据预览")
    if df.empty:
        st.warning("暂无提交数据")
    else:
        st.dataframe(df, use_container_width=True)
    
    # 3. 清空数据（清理测试用）
    if st.button("🗑️ 清空所有数据（不可逆）"):
        if os.path.exists(file):
            os.remove(file)
        st.success("✅ 所有数据已清空！页面将刷新...")
        st.rerun()
    
    # 4. 下载数据（只有你能看到）
    st.write("### 📥 下载汇总数据")
    if st.button("生成 Excel 下载链接"):
        if os.path.exists(file) and not df.empty:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False)
            buffer.seek(0)
            st.download_button(
                label="📊 下载 职务统计.xlsx",
                data=buffer,
                file_name="职务统计.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("⚠️ 暂无提交数据，无法下载")
elif admin_pwd != "":
    st.error("❌ 密码错误，无法进行管理操作")

st.caption("仅用于班级职务统计，提交后数据由管理员统一汇总")
