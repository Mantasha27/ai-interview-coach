import streamlit as st
import pandas as pd
import random
import time
import speech_recognition as sr
import matplotlib.pyplot as plt
import os

from database import init_db
from auth import login_system
from nlp_engine import evaluate_answer
from admin import show_admin_dashboard
from utils import speak_text


# ================================================
# PAGE CONFIG
# ================================================
st.set_page_config(page_title="AI Interview Coach", layout="wide")

conn, cursor = init_db()
login_system(cursor, conn)

DOMAINS = {
    "HR": ("hr_q.csv", "hr_a.csv"),
    "General": ("g_q.csv", "g_a.csv"),
    "Data Science": ("ds_q.csv", "ds_a.csv"),
    "Web Development": ("wd_q.csv", "wd_a.csv"),
}

menu = st.sidebar.radio("Navigation", ["Interview", "View Results", "Admin Dashboard"])


# ================================================
# SESSION STATE INITIALIZE
# ================================================
if "step" not in st.session_state:
    st.session_state.step = 0

if "answers" not in st.session_state:
    st.session_state.answers = [""] * 5

if "scores" not in st.session_state:
    st.session_state.scores = [0] * 5

if "confidence" not in st.session_state:
    st.session_state.confidence = [0] * 5


# =================================================
# INTERVIEW
# =================================================
if menu == "Interview":
    st.title("🎤 AI Interview Coach")

    domain = st.radio("Choose Domain", list(DOMAINS.keys()))

    if st.button("Start Interview", use_container_width=True, type="primary"):
        q_file, a_file = DOMAINS[domain]
        
        # ✅ Check if CSV files exist
        if not os.path.exists(q_file) or not os.path.exists(a_file):
            st.error(f"❌ Missing CSV files for {domain}. Please ensure {q_file} and {a_file} exist.")
        else:
            try:
                q_df = pd.read_csv(q_file)
                a_df = pd.read_csv(a_file)

                selected = random.sample(range(len(q_df)), 5)

                st.session_state.questions = q_df.iloc[selected].Question.tolist()
                st.session_state.expected = a_df.iloc[selected].Answer.tolist()

                # reset state
                st.session_state.answers = [""] * 5
                st.session_state.scores = [0] * 5
                st.session_state.confidence = [0] * 5
                st.session_state.step = 0
                st.session_state.domain = domain
                st.session_state.start_time = time.time()

                # clear old widget keys (prevents carry-over across interviews)
                for i in range(5):
                    st.session_state.pop(f"answer_box_{i}", None)
                    st.session_state.pop(f"audio_{i}", None)

                st.rerun()
            except Exception as e:
                st.error(f"❌ Error loading questions: {e}")

    if "questions" in st.session_state:
        step = st.session_state.step
        questions = st.session_state.questions
        expected = st.session_state.expected

        # ----------------------------------------
        # TIMER
        # ----------------------------------------
        elapsed = int(time.time() - st.session_state.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        # Display timer and warn if exceeding time
        timer_col1, timer_col2 = st.columns([3, 1])
        with timer_col1:
            st.write(f"⏱ Interview Time: **{minutes}:{seconds:02d}**")
        
        # ✅ Warn if exceeding 30 minutes
        if elapsed > 1800:
            st.warning("⚠️ Interview time exceeding 30 minutes. Consider wrapping up soon!")

        st.divider()

        # ----------------------------------------
        # QUESTION NAVIGATION (clickable anytime)
        # ----------------------------------------
        st.markdown("### 📌 Questions Navigation")
        cols = st.columns(5)
        for i in range(5):
            label = f"🟢 Q{i+1}" if st.session_state.answers[i].strip() else f"🔴 Q{i+1}"
            with cols[i]:
                if st.button(label, key=f"nav_{i}", use_container_width=True):
                    st.session_state.step = i
                    st.rerun()

        st.divider()

        # ----------------------------------------
        # QUESTION
        # ----------------------------------------
        st.markdown(f"### ❓ Question {step+1} / 5")
        st.write(f"**{questions[step]}**")

        if st.button("🔊 Hear Question", key=f"hear_{step}", use_container_width=True):
            try:
                speak_text(questions[step])
            except Exception as e:
                st.error(f"❌ Error playing audio: {e}")

        st.divider()

        # ----------------------------------------
        # AUDIO RECORDING & TEXT INPUT
        # ----------------------------------------
        st.markdown("#### 🎯 Answer This Question")
        
        tab1, tab2 = st.tabs(["🎤 Speak Your Answer", "📝 Type Your Answer"])
        
        with tab1:
            st.info("Click the microphone button and speak your answer clearly")
            audio = st.audio_input("Speak your answer", key=f"audio_{step}")

            if audio is not None:
                try:
                    recognizer = sr.Recognizer()

                    with sr.AudioFile(audio) as source:
                        audio_data = recognizer.record(source)

                    try:
                        text = recognizer.recognize_google(audio_data)

                        st.session_state.answers[step] = text
                        st.session_state[f"answer_box_{step}"] = text

                        # IMPORTANT: clear audio widget so it doesn't re-apply on reruns
                        st.session_state.pop(f"audio_{step}", None)

                        st.success("✅ Voice converted to text!")

                    except sr.UnknownValueError:
                        st.warning("⚠️ Audio not clear. Please speak louder or try again.")
                    except sr.RequestError:
                        st.error("❌ Error with speech recognition service. Please try again.")
                except Exception as e:
                    st.error(f"❌ Audio processing error: {e}")

        with tab2:
            st.info("Type or paste your answer below")

        # ----------------------------------------
        # ANSWER TEXTBOX (PER QUESTION, PRESERVED)
        # ----------------------------------------
        st.markdown("#### ✍️ Your Answer")
        answer = st.text_area(
            "Your Answer:",
            value=st.session_state.answers[step],
            key=f"answer_box_{step}",
            height=150,
            placeholder="Type or paste your answer here...",
            label_visibility="collapsed"
        )
        st.session_state.answers[step] = answer

        st.divider()

        # ----------------------------------------
        # NAVIGATION BUTTONS
        # ----------------------------------------
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("⬅️ Previous", disabled=(step == 0), use_container_width=True):
                st.session_state.step -= 1
                st.rerun()

        with col2:
            st.markdown(f"<div style='text-align: center; padding: 10px;'><b>Progress: {step + 1}/5</b></div>", unsafe_allow_html=True)

        with col3:
            if st.button("Next ➡️", disabled=(step == 4), use_container_width=True):
                st.session_state.step += 1
                st.rerun()

        st.divider()

        # ----------------------------------------
        # SUBMIT
        # ----------------------------------------
        if step == 4:
            if st.button("✅ Submit Interview", use_container_width=True, type="primary"):
                feedback_data = []

                for i in range(5):
                    student_ans = st.session_state.answers[i]
                    expected_ans = expected[i]

                    if student_ans.strip():
                        score, missing, feedback, conf = evaluate_answer(expected_ans, student_ans)
                    else:
                        score = 0
                        conf = 0
                        feedback = "❌ No answer provided"
                        missing = ["answer", "empty"]

                    st.session_state.scores[i] = score
                    st.session_state.confidence[i] = conf

                    feedback_data.append(
                        {
                            "question": questions[i],
                            "student": student_ans,
                            "expected": expected_ans,
                            "score": score,
                            "confidence": conf,
                            "feedback": feedback,
                            "missing": missing,
                        }
                    )

                total_score = sum(st.session_state.scores)
                percentage = (total_score / 50) * 100
                avg_conf = sum(st.session_state.confidence) / 5

                # ✅ Save to database with error handling
                try:
                    cursor.execute(
                        "INSERT INTO results VALUES (?,?,?,?,?)",
                        (
                            st.session_state["user"],
                            st.session_state.domain,
                            total_score,
                            percentage,
                            avg_conf,
                        ),
                    )
                    conn.commit()
                except Exception as e:
                    st.error(f"❌ Error saving results: {e}")
                    st.stop()

                # ===== RESULTS PAGE =====
                st.success("✅ Interview Completed!")
                
                st.markdown("---")
                
                # ✅ Display metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📊 Score", f"{total_score}/50", f"{total_score - 25}")
                with col2:
                    st.metric("📈 Percentage", f"{percentage:.1f}%", f"{percentage - 50:.1f}%")
                with col3:
                    st.metric("💡 Confidence", f"{avg_conf:.1f}%", f"{avg_conf - 50:.1f}%")

                st.markdown("---")
                
                # ✅ Performance graph
                st.subheader("📊 Performance Graph")
                fig, ax = plt.subplots(figsize=(10, 5))
                colors = ['🟢' if score >= 7 else '🟡' if score >= 5 else '🔴' 
                         for score in st.session_state.scores]
                bars = ax.bar(range(1, 6), st.session_state.scores, color=['#2ecc71' if s >= 7 else '#f39c12' if s >= 5 else '#e74c3c' for s in st.session_state.scores])
                ax.set_xlabel("Question Number", fontsize=12)
                ax.set_ylabel("Score (out of 10)", fontsize=12)
                ax.set_ylim(0, 10)
                ax.set_title(f"{st.session_state.domain} Interview Performance", fontsize=14, fontweight='bold')
                ax.grid(axis='y', alpha=0.3)
                st.pyplot(fig)

                st.markdown("---")
                
                # ✅ Download results as CSV
                st.subheader("📥 Download Results")
                csv_data = pd.DataFrame({
                    'Domain': [st.session_state.domain],
                    'Score': [total_score],
                    'Percentage': [percentage],
                    'Confidence': [avg_conf],
                    'Timestamp': [time.strftime('%Y-%m-%d %H:%M:%S')]
                })
                csv = csv_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name=f"interview_{st.session_state.domain}_{int(time.time())}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                st.markdown("---")
                
                # ✅ Detailed feedback
                st.markdown("## 📋 Detailed Feedback")
                
                for i, item in enumerate(feedback_data):
                    with st.expander(f"Question {i+1} - Score: {item['score']}/10 {'🟢' if item['score'] >= 7 else '🟡' if item['score'] >= 5 else '🔴'}", expanded=(i==0)):
                        st.markdown(f"**❓ Question:** {item['question']}")
                        st.markdown(f"**✍️ Your Answer:** {item['student']}")
                        st.markdown(f"**✅ Expected Answer:** {item['expected']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Score", f"{item['score']}/10")
                        with col2:
                            st.metric("Confidence", f"{item['confidence']}%")
                        
                        st.markdown(f"**💬 Feedback:** {item['feedback']}")
                        if item['missing']:
                            st.markdown(f"**⚠️ Missing Keywords:** `{', '.join(item['missing'])}`")


# =================================================
# VIEW RESULTS
# =================================================
if menu == "View Results":
    st.header("📊 Interview History")

    try:
        cursor.execute(
            "SELECT domain, score, percentage, confidence FROM results WHERE username=?",
            (st.session_state["user"],),
        )
        rows = cursor.fetchall()

        if rows:
            df = pd.DataFrame(rows, columns=["Domain", "Score", "Percentage", "Confidence"])
            
            st.subheader("All Interview Results")
            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Performance Trend")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(range(1, len(df) + 1), df["Percentage"], marker="o", linewidth=2, markersize=8, color='#3498db')
            ax.set_xlabel("Attempt Number", fontsize=12)
            ax.set_ylabel("Percentage Score (%)", fontsize=12)
            ax.set_title("Interview Performance Over Time", fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_ylim(0, 100)
            st.pyplot(fig)

            # ✅ Statistics
            st.subheader("📊 Your Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Interviews", len(df))
            with col2:
                st.metric("Average Score", f"{df['Percentage'].mean():.1f}%")
            with col3:
                st.metric("Best Score", f"{df['Percentage'].max():.1f}%")
            with col4:
                st.metric("Avg Confidence", f"{df['Confidence'].mean():.1f}%")

            # Domain breakdown
            st.subheader("📌 Performance by Domain")
            domain_stats = df.groupby("Domain")["Percentage"].agg(['count', 'mean', 'max']).round(1)
            st.dataframe(domain_stats, use_container_width=True)

        else:
            st.info("📭 No results yet. Start your first interview!")
    except Exception as e:
        st.error(f"❌ Error loading results: {e}")


# =================================================
# ADMIN DASHBOARD
# =================================================
if menu == "Admin Dashboard":
    if st.session_state.get("user") == "admin":
        show_admin_dashboard(cursor)
    else:
        st.warning("⛔ Admin access only. Please log in with admin credentials.")
