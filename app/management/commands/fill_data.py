# app/management/commands/fill_db.py
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from django.core.files import File
from io import BytesIO
from PIL import Image


class Command(BaseCommand):
    help = 'Fill the database with test data according to the specified ratio'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio multiplier for data generation')

    def create_test_image(self):
        image = Image.open("sam.jpg")
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        return File(image_io, name='test.jpg')

    def handle(self, *args, **options):
        ratio = options['ratio']
        fake = Faker()

        self.stdout.write(f"Starting database population with ratio {ratio}...")

        # Create Users and Profiles - теперь создаем последовательно
        self.stdout.write(f"Creating {ratio} users and profiles...")
        profiles = []
        for i in range(ratio):
            # Создаем пользователя
            username = fake.unique.user_name()
            email = fake.email()
            password = fake.password()
            user = User.objects.create(username=username, email=email, password=password)

            # Создаем профиль с аватаркой
            profile = Profile.objects.create(user_id=user)
            profile.avatar.save('avatar.jpg', self.create_test_image())
            profiles.append(profile)

            if i % 100 == 0:
                self.stdout.write(f"Created {i}/{ratio} users and profiles...")

        # Create Tags
        self.stdout.write(f"Creating {ratio} tags...")
        tags = []
        for i in range(ratio):
            name = fake.unique.word()[:100]
            tag = Tag(name=name)
            tags.append(tag)

        Tag.objects.bulk_create(tags, batch_size=1000)
        tags = list(Tag.objects.all())

        # Create Questions
        self.stdout.write(f"Creating {ratio * 10} questions...")
        questions = []
        for i in range(ratio * 10):
            author = random.choice(profiles)
            title = fake.sentence()[:255]
            text = fake.text(max_nb_chars=1000)
            tag = random.choice(tags)
            question = Question(user_id=author, title=title, text=text, tag_id=tag)
            questions.append(question)

        Question.objects.bulk_create(questions, batch_size=5000)
        questions = list(Question.objects.all())

        # Create Answers
        self.stdout.write(f"Creating {ratio * 100} answers...")
        answers = []
        for i in range(ratio * 100):
            author = random.choice(profiles)
            question = random.choice(questions)
            title = fake.sentence()[:255]
            text = fake.text(max_nb_chars=1000)
            is_correct = random.choice([True, False])
            answer = Answer(question_id=question, user_id=author, title=title, text=text, is_correct=is_correct)
            answers.append(answer)

        Answer.objects.bulk_create(answers, batch_size=10000)
        answers = list(Answer.objects.all())

        # Create Question Likes
        self.stdout.write(f"Creating {ratio * 100} question likes...")
        question_likes = []
        existing_question_likes = set()

        for i in range(ratio):
            profile = profiles[i]
            for j in range(100):
                question = random.choice(questions)

                existing_question_likes.add((profile.id, question.id))
                question_likes.append(QuestionLike(question_id=question, user_id=profile))

                if len(question_likes) % 10000 == 0:
                    QuestionLike.objects.bulk_create(question_likes, batch_size=10000)
                    question_likes = []

        if question_likes:
            QuestionLike.objects.bulk_create(question_likes, batch_size=10000)

        # Create Answer Likes
        self.stdout.write(f"Creating {ratio * 100} answer likes...")
        answer_likes = []
        existing_answer_likes = set()

        for i in range(ratio):
            profile = profiles[i]
            for j in range(100):
                answer = random.choice(answers)

                existing_answer_likes.add((profile.id, answer.id))
                answer_likes.append(AnswerLike(answer_id=answer, user_id=profile))

                if len(answer_likes) % 10000 == 0:
                    AnswerLike.objects.bulk_create(answer_likes, batch_size=10000)
                    answer_likes = []

        if answer_likes:
            AnswerLike.objects.bulk_create(answer_likes, batch_size=10000)

        self.stdout.write(self.style.SUCCESS(f"Successfully populated database with ratio {ratio}"))