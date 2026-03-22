import streamlit as st

from openai import OpenAI

# Initialize client (uses your environment variable)
client = OpenAI(api_key="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")

st.set_page_config(page_title="Physics AI Solver")

st.title("⚡ Physics AI Solver")

# Mode selection
mode = st.radio("Select Mode:", ["Learning", "Exam"])

# Input box
problem = st.text_area(
    "Enter your physics problem:",
    placeholder="""Example:
A block of mass 2 kg moves at 3 m/s. Find kinetic energy.

You can also write:
v = 3 m/s
m = 2 kg

Tips:
- Use ^ for powers → v^2
- Use sqrt() → sqrt(2gh)
- Use sin(), cos()
"""
)


if st.button("Solve"):

    if problem.strip() == "":
        st.warning("Please enter a problem.")
    else:
        is_derivation = any(word in problem.lower() for word in [
            "derive", "derivation", "prove", "show that"
            ])

        if mode == "Learning":
            prompt = f"""
            You are an excellent physics professor.

            Explain the solution in a natural, flowing way like a good teacher.

            - Start by understanding the problem
            - Introduce the key idea or formula naturally
            - Solve step-by-step with clear reasoning
            - Include brief derivation or justification if helpful
            - End with the final answer clearly

            IMPORTANT:
            - Do NOT use rigid headings like "Given", "Find"
            - Do NOT sound robotic or like a checklist
            - Keep it clear, smooth, and easy to read
            - Use LaTeX for equations with $...$

            Be rigorous but clear.

            You can ignore the structure to better cater to the needs of the problem given. 
            But make sure to pick up on what the user wants to know, given by the student in the prompt

            Format equations using LaTeX inside $...$.
            Example: $E = \frac{1}{2}mv^2$
            DO NOT use code blocks or triple backticks.
            Write equations using LaTeX inline with $...$ only.
            DO NOT use \[ \] or display math blocks

            Use clear formatting for steps.
            Break explanation into short paragraphs.
            Add spacing between steps.
            Avoid long dense blocks of text.
            Explain like you're teaching, not writing a textbook.

            Problem:{problem}"""
            

        else:
            prompt = f"""
Solve this physics problem for an exam.

Structure:
1. Formula
2. Substitution
3. Final answer
4. Tips and tricks for similar models in examination.

Format equations using LaTeX inside $...$.
Example: $E = \frac{1}{2}mv^2$
DO NOT use code blocks or triple backticks.
Write equations using LaTeX inline with $...$ only.

Use clear formatting for steps.

Problem:{problem}"""

        with st.spinner("Solving..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                
            )

        solution = response.choices[0].message.content

        st.markdown("### 📘 Solution")
        st.write(solution)