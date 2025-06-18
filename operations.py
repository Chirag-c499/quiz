from models import Quiz, Question

def create_quiz(title, questions):
    quiz = Quiz.create(title=title)
    for q in questions:
        Question.create(
            quiz=quiz,
            text=q["text"],
            a=q["a"],
            b=q["b"],
            c=q["c"],
            d=q["d"],
            correct_answer=q["correct"]
        )
    quiz.save()