import json, re, jwt, bcrypt, random

from django.views import View
from django.http import JsonResponse
from django.db.utils import DataError
from django.core.mail import send_mail
from datetime import datetime, timedelta


from .models import User
from .decorator import login_decorator
from my_settings import SECRET_KEY, ALGORITHM
from .decorator import login_decorator


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        email_format = re.compile("\w+[@]\w+[.]\w+")
        password_format = re.compile(
            "^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$"
        )

        try:
            if not email_format.search(data["email"]):
                return JsonResponse({"message": "INVALID_EMAIL_FORMAT"}, status=400)
            if not password_format.match(data["password"]):
                return JsonResponse({"message": "INVALID_PASSWORD_FORMAT"}, status=400)

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message": "USER_ALREADY_EXISTS"}, status=400)

            salt = bcrypt.gensalt()
            encoded_passwrod = data["password"].encode("utf-8")
            hashed_password = bcrypt.hashpw(encoded_passwrod, salt)
            decoded_password = hashed_password.decode("utf-8")

            User.objects.create(
                name=data["name"],
                password=decoded_password,
                email=data["email"],
                phone=data["phone"],
                agree_service=data["agree_service"],
                agree_maketing=data["agree_maketing"],
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except DataError:
            return JsonResponse({"message": "DATA_TOO_LONG"}, status=400)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = User.objects.get(email=data["email"])

            if not User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            if not bcrypt.checkpw(
                data["password"].encode("utf-8"), user.password.encode("utf-8")
            ):
                return JsonResponse({"message": "PASSWORD_ERROR"}, status=401)

            user.auth_number = ""
            user.save()

            if data["token_status"] == True:
                access_token = jwt.encode(
                    {
                        "id": user.id,
                        "exp": datetime.utcnow() + timedelta(days=30),
                    },
                    SECRET_KEY,
                    algorithm=ALGORITHM,
                )

                return JsonResponse(
                    {
                        "message": "SUCCESS",
                        "token": access_token,
                    },
                    status=200,
                )
            access_token = jwt.encode(
                {"id": user.id, "exp": datetime.utcnow() + timedelta(hours=2)},
                SECRET_KEY,
                algorithm=ALGORITHM,
            )

            return JsonResponse(
                {
                    "message": "SUCCESS",
                    "token": access_token,
                },
                status=200,
            )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class SendEmailView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data["email"]

            random_num = random.randint(10000, 99999)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            send_mail(
                "[올마이투어]비밀번호 재설정",
                f"안녕하세요 올마이투어입니다.\n비밀번호 재설정를 위해 아래의 인증번호를 입력해주세요.\n인증번호 : {random_num}",
                "",
                [email],
                fail_silently=False,
            )

            user = User.objects.filter(email=email)
            user.update(auth_number=random_num)

            return JsonResponse({"message": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class AuthenticationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data["email"])
            access_token = jwt.encode({"id": user.id}, SECRET_KEY, algorithm=ALGORITHM)

            if not data["auth_number"] == user.auth_number:
                return JsonResponse({"message": "AUTH_NUMBER_ERROR"}, status=401)

            access_token = jwt.encode(
                {"id": user.id, "exp": datetime.utcnow() + timedelta(minutes=5)},
                SECRET_KEY,
                algorithm=ALGORITHM,
            )
            return JsonResponse(
                {
                    "message": "SUCCESS",
                    "token": access_token,
                },
                status=200,
            )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class NewPasswordView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            password_format = re.compile(
                "^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$"
            )

            if not password_format.match(data["newpw"]):
                return JsonResponse({"message": "INVALID_PASSWORD_FORMAT"}, status=400)

            salt = bcrypt.gensalt()
            encoded_passwrod = data["newpw"].encode("utf-8")
            print(data["newpw"])
            hashed_password = bcrypt.hashpw(encoded_passwrod, salt)
            decoded_password = hashed_password.decode("utf-8")

            user = User.objects.get(id=request.user.id)
            user.password = decoded_password
            user.auth_number = ""
            user.save()

            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class DoubleCheckEmailView(View):
    def post(self, request):
        data = json.loads(request.body)

        email_format = re.compile("\w+[@]\w+[.]\w+")

        try:
            if not email_format.search(data["email"]):
                return JsonResponse({"message": "INVALID_EMAIL_FORMAT"}, status=400)

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message": "DUPLICATE_EMAIL"}, status=400)

            return JsonResponse({"message": "NOT_DUPLICATE_EMAIL"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)


class MypageView(View):
    @login_decorator
    def get(self, request):
        user = request.user

        result = {
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "password": user.password,
            "is_maker": user.is_maker,
            "agree_service": user.agree_service,
            "agree_maketing": user.agree_maketing,
        }

        return JsonResponse({"Result": result}, status=200)


class PhoneCertificationView(View):
    def post(self, request):
        data = json.loads(request.body)

        certification_number = data.get("certification")

        if certification_number == "123456":
            return JsonResponse({"MESSAGE": "SAME"}, status=200)

        return JsonResponse({"MESSAGE": "DISCORD"}, status=400)
