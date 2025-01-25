import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from collections import defaultdict
import json
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from PIL import Image

from utils import plot_score_trends, generate_recommendations, define_student_persona, plot_performance_trends, plot_student_performance, plot_weak_areas

def load_json(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            print("Error decoding JSON!")
            return None
    return data

def summarize_performance(quiz_attempts):
    performance_report = []
    for attempt in quiz_attempts:
        quiz_info = attempt['quiz']
        quiz_title = quiz_info.get('title', 'Untitled Quiz')
        score = attempt['score']
        accuracy = attempt['accuracy']
        total_questions = attempt['total_questions']
        correct_answers = attempt['correct_answers']
        incorrect_answers = attempt['incorrect_answers']
        
        report = {
            'quiz_title': quiz_title,
            'score': score,
            'accuracy': accuracy,
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'total_questions': total_questions
        }
        performance_report.append(report)
    
    return performance_report

def calculate_question_difficulty(df_incorrect, total_attempts):
    question_difficulty = {}

    # Calculate the difficulty as the ratio of incorrect answers to total attempts
    for index, row in df_incorrect.iterrows():
        question_id = row['question_id']
        incorrect_count = row['incorrect_count']

        difficulty = incorrect_count / total_attempts.get(question_id, 1)  
        question_difficulty[question_id] = difficulty
    
    return question_difficulty

def analyze_weak_areas(df_incorrect, question_difficulty, threshold=0.5):
    weak_areas = {}

    # Identify questions where the difficulty is above the threshold
    for question_id, difficulty in question_difficulty.items():
        if difficulty > threshold:
            weak_areas[question_id] = difficulty

    return weak_areas


def analyze_incorrect_answers(quiz_data, hist_quiz_data):
    incorrect_questions = defaultdict(int)

    quiz = quiz_data.get('quiz', None)
    if not quiz:
        print("No quiz data found!")
        return {}

    questions = quiz.get('questions', [])

    # Track incorrect attempts for each question
    for attempt in hist_quiz_data:
        response_map = attempt['response_map']
        quiz_id = attempt['quiz_id']

        if quiz_id != quiz['id']:
            continue

        for question in questions:
            question_id = question.get('id')
            correct_option = None

            # Find correct option for the question
            for opt in question['options']:
                if opt.get('is_correct', False):
                    correct_option = opt['id']
                    break

            if correct_option is None:
                continue

            user_answer = response_map.get(str(question_id))

            if user_answer != correct_option:
                incorrect_questions[question_id] += 1

    df_incorrect = pd.DataFrame(list(incorrect_questions.items()), columns=["question_id", "incorrect_count"])

    return df_incorrect


def identify_trends(historical_data):
    trends = {}
    user_scores = {}
    
    for attempt in historical_data:
        user_id = attempt['user_id']
        score = attempt['score']
        
        if user_id not in user_scores:
            user_scores[user_id] = []
        
        user_scores[user_id].append(score)
    
    for user_id, scores in user_scores.items():
        avg_score = np.mean(scores)
        trends[user_id] = avg_score
    
    return trends

model_name = "gpt2"  
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def get_llm_reasoning(question_text, correct_answer, incorrect_answers):
    prompt = (
        f"Question: {question_text}\n"
        f"Correct Answer: {correct_answer}\n"
        f"Incorrect Answers: {', '.join(incorrect_answers)}\n"
        f"Explain why the correct answer is correct and why the incorrect answers are incorrect."
    )

    # Tokenize the input text for GPT-2
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(inputs, max_length=150, num_return_sequences=1, temperature=0.7)

    explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return explanation[len(prompt):].strip()  

def analyze_question_focus(quiz_data, hist_quiz_data):
    question_focus = defaultdict(lambda: {'correct': 0, 'incorrect': 0, 'total': 0, 'distractor_probabilities': {}, 'reasoning': {}})
    
    quiz = quiz_data.get('quiz', None)
    if not quiz:
        print("No quiz data found!")
        
    quiz_id = quiz.get('id')  
    if not quiz_id:
        print("Quiz ID not found!")
        
    for attempt in hist_quiz_data:
        response_map = attempt['response_map']
        attempt_quiz_id = attempt.get('quiz_id')  
        
        if attempt_quiz_id != quiz_id:
            continue

        for question in quiz['questions']:
            question_id = question['id']
            correct_option = next((opt for opt in question['options'] if opt.get('is_correct', False)), None)
            
            if not correct_option:
                continue
            
            correct_option_id = correct_option['id']
            correct_answer_text = correct_option['text']  
            selected_option_id = response_map.get(str(question_id))

            question_focus[question_id]['total'] += 1
            if selected_option_id == correct_option_id:
                question_focus[question_id]['correct'] += 1
            else:
                question_focus[question_id]['incorrect'] += 1

            # Track distractor probabilities (for incorrect answers)
            for opt in question['options']:
                option_id = opt['id']
                if option_id not in question_focus[question_id]['distractor_probabilities']:
                    question_focus[question_id]['distractor_probabilities'][option_id] = 0
                if selected_option_id != correct_option_id and selected_option_id == option_id:
                    question_focus[question_id]['distractor_probabilities'][option_id] += 1

            for opt in question['options']:
                option_id = opt['id']
                option_text = opt['text']
                is_correct = opt.get('is_correct', False)

                # Skip the correct option, since it's not a distractor
                if is_correct:
                    continue

                # Reasoning: Why might this incorrect answer be selected?
                if option_id == selected_option_id:
                    reasoning = get_llm_reasoning(question['question'], correct_answer_text, [opt['text'] for opt in question['options'] if not opt.get('is_correct', False)])
                    question_focus[question_id]['reasoning'][option_id] = reasoning

    for question_id, data in question_focus.items():
        total_attempts = data['correct'] + data['incorrect']
        if total_attempts > 0:
            for option_id, incorrect_count in data['distractor_probabilities'].items():
                data['distractor_probabilities'][option_id] /= total_attempts

    for question_id, data in question_focus.items():
        if data['incorrect'] > 0:
            data['reasoning']['common_misconceptions'] = {
                "1": "Confusion Over Terminology: Users may be unfamiliar with the specific characteristics of epithelial tissue and might confuse it with other tissue types that also have prominent roles in body functions (muscle for movement, connective for structure, nervous for communication).",
                "2": "Similar Functionality: Users may focus too much on the function of the tissue (e.g., transport, protection) rather than structural differences. Epithelial tissue performs many functions (like protection and secretion) that other tissues might also carry out in some form, leading to confusion.",
                "3": "Lack of Clear Visual Cues: Without visual diagrams or clear explanations of where each tissue type is located, users might have a hard time recalling specific locations and characteristics. This could result in picking wrong answers based on vague associations.",
                "4": "Over-generalization or Misapplication of Knowledge: When users learn about one tissue type in a general sense, they might incorrectly apply that information across the board, failing to notice critical details that distinguish tissues from one another.",
                "5": "Limited Contextual Understanding: In some cases, users might select answers based on partial or fragmented knowledge. For example, if they have read about ciliated columnar epithelium in a general respiratory or reproductive system context, they might apply this knowledge more broadly, without fully understanding the unique characteristics of other tissue types."
            }

    if not question_focus:
        question_focus['common_misconceptions'] = {
            "1": "Confusion Over Terminology: Users may be unfamiliar with the specific characteristics of epithelial tissue and might confuse it with other tissue types that also have prominent roles in body functions (muscle for movement, connective for structure, nervous for communication).",
            "2": "Similar Functionality: Users may focus too much on the function of the tissue (e.g., transport, protection) rather than structural differences. Epithelial tissue performs many functions (like protection and secretion) that other tissues might also carry out in some form, leading to confusion.",
            "3": "Lack of Clear Visual Cues: Without visual diagrams or clear explanations of where each tissue type is located, users might have a hard time recalling specific locations and characteristics. This could result in picking wrong answers based on vague associations.",
            "4": "Over-generalization or Misapplication of Knowledge: When users learn about one tissue type in a general sense, they might incorrectly apply that information across the board, failing to notice critical details that distinguish tissues from one another.",
            "5": "Limited Contextual Understanding: In some cases, users might select answers based on partial or fragmented knowledge. For example, if they have read about ciliated columnar epithelium in a general respiratory or reproductive system context, they might apply this knowledge more broadly, without fully understanding the unique characteristics of other tissue types."
        }

    return question_focus

def generate_pdf_with_images_and_output(pdf_filename, images_path, rec, persona, question_focus):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 24)
    c.drawString(200, height - 50, "Quiz Analyst")
    c.setFont("Helvetica", 12)
    
    y_position = height - 100

    c.drawString(50, y_position, 'Recommendations: ')
    y_position -= 20
    if isinstance(rec, dict):
        for key, value in rec.items():
            c.drawString(50, y_position, f"{key}: {value}")
            y_position -= 20
    else:
        c.drawString(50, y_position, str(rec))  
        y_position -= 20

    c.drawString(50, y_position, 'User Persona: ')
    y_position -= 20
    if isinstance(persona, dict):
        for key, value in persona.items():
            c.drawString(50, y_position, f"{key}: {value}")
            y_position -= 20
    else:
        c.drawString(50, y_position, str(persona)) 
        y_position -= 20

    c.drawString(50, y_position, 'Question Focus: ')
    y_position -= 20
    if isinstance(question_focus, defaultdict):
        misconceptions = question_focus.get('common_misconceptions', {})
        for idx, misconception in misconceptions.items():
            c.drawString(50, y_position, f"{idx}. {misconception}")
            y_position -= 20
            if y_position < 50:  
                c.showPage()
                y_position = height - 50  
    else:
        c.drawString(50, y_position, str(question_focus))  
        y_position -= 20

    image_files = [f for f in os.listdir(images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        img = Image.open(image_path)
        
        img_width, img_height = img.size
        max_width = width - 100  
        max_height = height - 200  

        if img_width > max_width or img_height > max_height:
            aspect_ratio = min(max_width / img_width, max_height / img_height)
            img_width = int(img_width * aspect_ratio)
            img_height = int(img_height * aspect_ratio)
        
        y_position -= img_height + 20 
        c.drawImage(image_path, 50, y_position, width=img_width, height=img_height)

        y_position -= img_height + 30  

        if y_position < 50: 
            c.showPage()
            y_position = height - 50  

    c.save()


if __name__ == '__main__':
    quiz_data = load_json('Quiz Analyst/data/quiz_data.json')
    hist_quiz_data = load_json('Quiz Analyst/data/hist_quiz_data.json')

    performance_report = summarize_performance(hist_quiz_data)
    print("Performance Report:")
    for report in performance_report:
        print(report)

    incorrect_question_analysis = analyze_incorrect_answers(quiz_data, hist_quiz_data)

    total_attempts = {q['id']: len(hist_quiz_data) for q in quiz_data['quiz']['questions']} 
    question_difficulty = calculate_question_difficulty(incorrect_question_analysis, total_attempts)

    weak_areas = analyze_weak_areas(incorrect_question_analysis, question_difficulty)

    trends = identify_trends(hist_quiz_data)
    print("Trends in Quiz:", trends)

    plot_score_trends(hist_quiz_data)
    plot_performance_trends(trends)
    plot_student_performance(trends)
    plot_weak_areas(weak_areas)

    rec = generate_recommendations(weak_areas, trends)
    print('Recommendations: ', rec)

    persona = define_student_persona(performance_report)
    print('User Persona: ', persona)

    question_focus = analyze_question_focus(quiz_data, hist_quiz_data)
    print("Question focus: ", question_focus)

    generate_pdf_with_images_and_output(
    'Quiz Analyst/reports/Quiz_Analyst_Report.pdf',
    'Quiz Analyst/images',
    rec=rec,
    persona=persona,
    question_focus=question_focus
    )
    