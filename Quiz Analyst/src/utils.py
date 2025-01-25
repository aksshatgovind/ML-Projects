import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def plot_score_trends(quiz_attempts):
    attempts_sorted = sorted(quiz_attempts, key=lambda x: datetime.strptime(x['submitted_at'], "%Y-%m-%dT%H:%M:%S.%f+05:30"))
    
    quiz_titles = [attempt['quiz']['title'] for attempt in attempts_sorted]
    scores = [attempt['score'] for attempt in attempts_sorted]
    dates = [datetime.strptime(attempt['submitted_at'], "%Y-%m-%dT%H:%M:%S.%f+05:30") for attempt in attempts_sorted]
    
    plt.plot(dates, scores, marker='o', color='b')
    plt.xticks(rotation=45)
    plt.xlabel('Date of Attempt')
    plt.ylabel('Score')
    plt.title('User Score Over Time')
    plt.tight_layout()
    plt.savefig('Quiz Analyst/images/score_trends.png')


def generate_recommendations(weak_areas, trends):
    recommendations = {}
    for topic, accuracy in weak_areas.items():
        recommendations[topic] = f"Focus on {topic} to improve your understanding."

    for student, avg_score in trends.items():
        if avg_score < 50:
            recommendations[student] = "Focus on improving your overall accuracy with easier questions."
        else:
            recommendations[student] = "Challenge yourself with more difficult questions to improve."

    return recommendations

def define_student_persona(performance_data):
    persona = {}
    student_performance = {}
    
    for data in performance_data:
        student_id = data['quiz_title']  
        accuracy = data['accuracy']
        
        accuracy_value = float(accuracy.replace('%', '').strip()) / 100.0
        
        if student_id not in student_performance:
            student_performance[student_id] = []
        
        student_performance[student_id].append(accuracy_value)
    
    for student_id, accuracies in student_performance.items():
        average_accuracy = np.mean(accuracies)
        
        if average_accuracy < 0.4:
            persona[student_id] = "Struggling Learner: Needs more practice on basics."
        elif average_accuracy < 0.7:
            persona[student_id] = "Improver: Showing steady progress, but needs focus on specific topics."
        else:
            persona[student_id] = "Top Performer: Great job! Focus on challenging problems for further growth."
    
    return persona


def plot_performance_trends(trends):
    students = list(trends.keys())  
    scores = list(trends.values()) 
    
    fig, ax = plt.subplots()
    ax.bar(students, scores, color='blue')

    ax.set_xlabel('Student ID')
    ax.set_ylabel('Average Score')
    ax.set_title('Performance Trends')

    ax.set_xticks(range(len(students)))  
    ax.set_xticklabels(students, rotation=90)  
    plt.savefig('Quiz Analyst/images/performance_trends.png')

def plot_quiz_performance(quiz_data):
    quiz_titles = [data['quiz_title'] for data in quiz_data]
    scores = [data['score'] for data in quiz_data]
    accuracies = [float(data['accuracy'].replace('%', '').strip()) for data in quiz_data]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.bar(quiz_titles, scores, color='skyblue', label='Scores', alpha=0.7)
    ax1.set_xlabel('Quiz Title')
    ax1.set_ylabel('Scores', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xticklabels(quiz_titles, rotation=45, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(quiz_titles, accuracies, color='orange', marker='o', label='Accuracy', linestyle='-', linewidth=2)
    ax2.set_ylabel('Accuracy (%)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    plt.title('Quiz Performance Analysis')
    plt.tight_layout()
    plt.savefig('Quiz Analyst/images/quiz_performance.png')


def plot_student_performance(trends):
    students = list(trends.keys()) 
    scores = list(trends.values()) 
    
    plt.figure(figsize=(10, 6))
    plt.bar(students, scores, color='lightgreen', alpha=0.7)
    plt.xlabel('Student ID')
    plt.ylabel('Average Score')
    plt.title('Student Performance Distribution')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('Quiz Analyst/images/student_performance_distribution.png')


def plot_weak_areas(weak_areas):
    topics = list(weak_areas.keys())
    accuracies = [weak_areas[topic] for topic in topics]
    
    num_vars = len(topics)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    accuracies += accuracies[:1]  
    angles += angles[:1]  

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, accuracies, color='red', alpha=0.25)
    ax.plot(angles, accuracies, color='red', linewidth=2)

    ax.set_yticklabels([])  
    ax.set_xticks(angles[:-1]) 
    ax.set_xticklabels(topics, fontsize=12, ha='right')

    plt.title('Weak Areas Radar Chart', size=15, color='black')
    plt.tight_layout()
    plt.savefig('Quiz Analyst/images/weak_areas.png')


