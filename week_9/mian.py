import requests
import json
import random
# User class to store player information
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.score = 0  # Start score at 0

    def update_score(self, points: int):
        """Method to update user score"""
        self.score += points

    def __str__(self):
        return f"User: {self.name}, Age: {self.age}, Score: {self.score}"


# Question class to store individual question details
class Question:
    def __init__(self, question_text: str, correct_answer: str):
        self.question_text = question_text
        self.correct_answer = correct_answer

    def check_answer(self, user_answer: str) -> bool:
        """Method to check if user's answer is correct"""
        return user_answer.lower() == self.correct_answer.lower()

    def __str__(self):
        return f"Question: {self.question_text}, Correct Answer: {self.correct_answer}"


# QuizGame class to manage the flow of the game
class QuizGame:
    def __init__(self, user: User):
        self.user = user
        self.questions = []

    def fetch_questions(self, url: str):
        """Fetch questions from API and store them"""
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data['results']:
                question = Question(item['question'], item['correct_answer'])
                self.questions.append(question)
        else:
            print("Error fetching questions.")

    def play(self):
        """Start the quiz and check user's answers"""
        random.shuffle(self.questions)
        print(f"Welcome {self.user.name}, to the quiz game!")
        print(f"You will be asked {len(self.questions)} questions. Answer True/False.")

        for question in self.questions:
            print(question.question_text)
            user_answer = input("Your answer (True/False): ")
            if question.check_answer(user_answer):
                print("Correct!")
                self.user.update_score(10)  # Add 10 points for a correct answer
            else:
                print(f"Wrong! The correct answer was {question.correct_answer}.")

        print(f"Quiz over! {self.user.name}'s final score: {self.user.score}")


# Main program logic
if __name__ == "__main__":
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    user = User(name, age)

    quiz = QuizGame(user)
    quiz.fetch_questions("https://opentdb.com/api.php?amount=10&category=9&difficulty=easy&type=boolean")
    quiz.play()
