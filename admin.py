import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_admin_dashboard(cursor):
    """
    Display admin dashboard with statistics and analytics
    """
    st.header("📊 Admin Dashboard")

    try:
        # Get average performance by domain
        cursor.execute("SELECT domain, AVG(percentage) FROM results GROUP BY domain")
        data = cursor.fetchall()

        if data:
            df_admin = pd.DataFrame(data, columns=["Domain", "Average Percentage"])
            
            st.subheader("Performance by Domain")
            st.dataframe(df_admin, use_container_width=True)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(df_admin["Domain"], df_admin["Average Percentage"], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
            ax.set_ylabel("Average Percentage (%)")
            ax.set_ylim(0, 100)
            ax.set_title("Average Performance by Interview Domain")
            st.pyplot(fig)
        else:
            st.info("No data available yet")

        # Get total users
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        # Get total interviews
        cursor.execute("SELECT COUNT(*) FROM results")
        total_interviews = cursor.fetchone()[0]

        # Get average score
        cursor.execute("SELECT AVG(percentage) FROM results")
        avg_percentage = cursor.fetchone()[0]

        st.divider()
        st.subheader("Platform Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", total_users)
        with col2:
            st.metric("Total Interviews", total_interviews)
        with col3:
            st.metric("Average Score", f"{avg_percentage:.1f}%" if avg_percentage else "N/A")
        with col4:
            if total_users > 0:
                st.metric("Avg Interviews/User", f"{total_interviews/total_users:.1f}")

    except Exception as e:
        st.error(f"❌ Error loading admin dashboard: {e}")
