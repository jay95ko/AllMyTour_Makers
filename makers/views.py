import json
import base64

from django.http.response import JsonResponse
from django.views import View

from django.core.files.storage import FileSystemStorage
from django.db import transaction
from users.decorator import login_decorator

from .models import (
    Category,
    DraftSns,
    Evidence,
    Maker,
    Maker_tour,
    Region,
    Sns,
    Language,
    Tour,
    DraftMaker,
    DraftTour,
    DraftMaker_Drafttour,
    DraftCategory,
    DraftLanguage,
    DraftRegion,
    DraftEvidence,
)


class MakerApplyView(View):
    @login_decorator
    @transaction.atomic
    def post(self, request):
        try:
            data = json.loads(request.POST["data"])
            makernickname = data["makernickname"]
            makername = data["makername"]
            introduce = data["introduce"]
            languages = data["language"]
            sns_address_list = data["sns_address"]
            bank = data["bank"]
            account_number = data.get("account_number")
            account_holder = data["account_holder"]
            productform = data["productform"]
            status = data["status"]
            evidence_kind = data["evidence_kind"]
            regions = data["region"]
            categories = data["category"]
            tour_kind = data["tour"]
            limit_people = data["limit_people"]
            limit_load = data["limit_load"]

            PROFILE = request.FILES.get("profile")
            IDCARD = request.FILES.get("idcard")
            BANKBOOK = request.FILES.get("bankbook")
            EVIDENCE_IMAGE = request.FILES.get("evidence_image")

            if PROFILE:
                uploaded_profile = PROFILE
                fs = FileSystemStorage(location="media/profile", base_url="profile")
                filename = fs.save(uploaded_profile.name, uploaded_profile)
                uploaded_profile_url = fs.url(filename)
                profile = uploaded_profile_url

            if IDCARD:
                uploaded_idcard = IDCARD
                fs = FileSystemStorage(location="media/idcard", base_url="idcard")
                filename = fs.save(uploaded_idcard.name, uploaded_idcard)
                uploaded_idcard_url = fs.url(filename)
                idcard = uploaded_idcard_url

            if BANKBOOK:
                uploaded_bankbook_image = BANKBOOK
                fs = FileSystemStorage(location="media/bankbook", base_url="bankbook")
                filename = fs.save(
                    uploaded_bankbook_image.name, uploaded_bankbook_image
                )
                uploaded_bankbook_image_url = fs.url(filename)
                bankbook = uploaded_bankbook_image_url
            else:
                bankbook = None

            if EVIDENCE_IMAGE:
                uploaded_evidence = EVIDENCE_IMAGE
                fs = FileSystemStorage(location="media/evidence", base_url="evidence")
                filename = fs.save(uploaded_evidence.name, uploaded_evidence)
                uploaded_evidence_url = fs.url(filename)
                evidence = uploaded_evidence_url
            else:
                evidence = None

            if not (makername and makernickname and PROFILE and introduce and IDCARD):
                return JsonResponse({"MESSAGE": "ENTER_REQUIRED_VALUES"}, status=400)

            maker = Maker.objects.create(
                user_id=request.user.id,
                makername=makername,
                makernickname=makernickname,
                introduce=introduce,
                profile=profile,
                idcard=idcard,
                bankbook_image=bankbook,
                status=status,
                bank=bank,
                account_number=account_number,
                account_holder=account_holder,
                productform=productform,
            )
            for language in languages:
                Language.objects.get_or_create(Language=language)
                maker.language.add(Language.objects.get(Language=language).id)

            for sns_address in sns_address_list:
                Sns.objects.get_or_create(maker_id=maker.id, address=sns_address)

            Evidence.objects.create(
                image=evidence, maker_id=maker.id, kind=evidence_kind
            )

            for region in regions:
                Region.objects.get_or_create(region=region)
                maker.region.add(Region.objects.get(region=region).id)

            for name in categories:
                Category.objects.get_or_create(name=name)
                maker.category.add(Category.objects.get(name=name).id)

            if Tour.objects.filter(kind=tour_kind).exists():
                tour = Tour.objects.get(kind=tour_kind)
                Maker_tour.objects.create(
                    limit_people=limit_people,
                    limit_load=limit_load,
                    tour_id=tour.id,
                    maker_id=maker.id,
                )
            user = request.user
            user.is_maker = True
            user.save()

            return JsonResponse({"MESSAGE": "CREATED"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"MESSAGE": "VALUE_ERROR"}, status=400)


class DraftMakerView(View):
    @login_decorator
    @transaction.atomic
    def post(self, request):
        try:
            data = json.loads(request.POST["data"])
            makernickname = data["makernickname"]
            makername = data["makername"]
            introduce = data["introduce"]
            languages = data["language"]
            sns_address_list = data["sns_address"]
            status = data["status"]
            bank = data["bank"]
            account_number = data.get("account_number")
            account_holder = data["account_holder"]
            productform = data["productform"]
            evidence_kind = data["evidence_kind"]
            regions = data["region"]
            categories = data["category"]
            tour_kind = data["tour"]
            limit_people = data["limit_people"]
            limit_load = data["limit_load"]

            PROFILE = request.FILES.get("profile")
            IDCARD = request.FILES.get("idcard")
            BANKBOOK = request.FILES.get("bankbook")
            EVIDENCE_IMAGE = request.FILES.get("evidence_image")

            if PROFILE:
                uploaded_profile = PROFILE
                fs = FileSystemStorage(location="media/profile", base_url="profile")
                filename = fs.save(uploaded_profile.name, uploaded_profile)
                uploaded_profile_url = fs.url(filename)
                profile = uploaded_profile_url
            else:
                profile = None

            if IDCARD:
                uploaded_idcard = IDCARD
                fs = FileSystemStorage(location="media/idcard", base_url="idcard")
                filename = fs.save(uploaded_idcard.name, uploaded_idcard)
                uploaded_idcard_url = fs.url(filename)
                idcard = uploaded_idcard_url
            else:
                idcard = None

            if BANKBOOK:
                uploaded_bankbook_image = BANKBOOK
                fs = FileSystemStorage(location="media/bankbook", base_url="bankbook")
                filename = fs.save(
                    uploaded_bankbook_image.name, uploaded_bankbook_image
                )
                uploaded_bankbook_image_url = fs.url(filename)
                bankbook = uploaded_bankbook_image_url
            else:
                bankbook = None

            if EVIDENCE_IMAGE:
                uploaded_evidence = EVIDENCE_IMAGE
                fs = FileSystemStorage(location="media/evidence", base_url="evidence")
                filename = fs.save(uploaded_evidence.name, uploaded_evidence)
                uploaded_evidence_url = fs.url(filename)
                evidence = uploaded_evidence_url
            else:
                evidence = None

            draftmaker = DraftMaker.objects.create(
                user_id=request.user.id,
                makername=makername,
                makernickname=makernickname,
                introduce=introduce,
                profile=profile,
                idcard=idcard,
                bankbook_image=bankbook,
                status=status,
                bank=bank,
                account_number=account_number,
                account_holder=account_holder,
                productform=productform,
            )

            for language in languages:
                DraftLanguage.objects.get_or_create(Language=language)
                draftmaker.language.add(DraftLanguage.objects.get(Language=language).id)

            for sns_address in sns_address_list:
                DraftSns.objects.get_or_create(
                    maker_id=draftmaker.id, address=sns_address
                )

            DraftEvidence.objects.create(
                image=evidence, maker_id=draftmaker.id, kind=evidence_kind
            )

            for region in regions:
                DraftRegion.objects.get_or_create(region=region)
                draftmaker.region.add(DraftRegion.objects.get(region=region).id)

            for name in categories:
                DraftCategory.objects.get_or_create(name=name)
                draftmaker.category.add(DraftCategory.objects.get(name=name).id)

            if DraftTour.objects.filter(kind=tour_kind).exists():
                drafttour = DraftTour.objects.get(kind=tour_kind)
                DraftMaker_Drafttour.objects.create(
                    limit_people=limit_people,
                    limit_load=limit_load,
                    tour_id=drafttour.id,
                    draftmaker_id=draftmaker.id,
                )
            user = request.user
            user.is_maker = True
            user.save()

            return JsonResponse(
                {
                    "MESSAGE": "DRAFT_CREATED",
                },
                status=201,
            )

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"MESSAGE": "VALUE_ERROR"}, status=400)


class MakerReviseView(View):
    @login_decorator
    @transaction.atomic
    def get(self, request):
        try:
            user = request.user

            if Maker.objects.filter(user_id=user.id).exists():
                maker = Maker.objects.get(user_id=user.id)
                evidences = Evidence.objects.select_related("maker").filter(
                    maker__user_id=user.id
                )

                result = {
                    "id": maker.id,
                    "makername": maker.makername,
                    "makernickname": maker.makernickname,
                    "introduce": maker.introduce,
                    "evidence": [
                        {
                            "evidence_kind": evidence.kind,
                            "evidence_image": base64.encodebytes(
                                open(evidence.image.path, "rb").read()
                            ).decode("utf-8"),
                            "evidence_name": evidence.image.name,
                            "evidence_url": evidence.image.url,
                        }
                        for evidence in evidences
                        if evidence.image
                    ],
                    "sns": list(maker.sns_set.values_list("address", flat=True)),
                    "language": list(maker.language.values_list("Language", flat=True)),
                    "category": list(maker.category.values_list("name", flat=True)),
                    "region": list(maker.region.values_list("region", flat=True)),
                    "bank": maker.bank,
                    "account_number": maker.account_number,
                    "account_holder": maker.account_holder,
                    "productform": maker.productform,
                    "tour": list(maker.tour.values_list("kind", flat=True)),
                }

                if Maker_tour.objects.filter(maker_id=maker).exists():
                    result["limit_people"] = Maker_tour.objects.get(
                        maker_id=maker
                    ).limit_people
                    result["limit_load"] = Maker_tour.objects.get(
                        maker_id=maker
                    ).limit_load

                if maker.profile:
                    result["profile"] = base64.encodebytes(
                        open(maker.profile.path, "rb").read()
                    ).decode("utf-8")
                    result["profile_name"] = maker.profile.name
                    result["profile_url"] = maker.profile.url

                if maker.idcard:
                    result["idcard"] = base64.encodebytes(
                        open(maker.idcard.path, "rb").read()
                    ).decode("utf-8")
                    result["idcard_name"] = maker.idcard.name
                    result["idcard_url"] = maker.idcard.url

                if maker.bankbook_image:
                    result["bankbook"] = base64.encodebytes(
                        open(maker.bankbook_image.path, "rb").read()
                    ).decode("utf-8")
                    result["bankbook_name"] = maker.bankbook_image.name
                    result["bankbook_url"] = maker.bankbook_image.url

            else:
                maker = DraftMaker.objects.get(user_id=user.id)
                evidences = DraftEvidence.objects.select_related("draftmaker").filter(
                    maker__user_id=user.id
                )

                result = {
                    "id": maker.id,
                    "makername": maker.makername,
                    "makernickname": maker.makernickname,
                    "introduce": maker.introduce,
                    "evidence": [
                        {
                            "evidence_kind": evidence.kind,
                            "evidence_image": base64.encodebytes(
                                open(evidence.image.path, "rb").read()
                            ).decode("utf-8"),
                            "evidence_name": evidence.image.name,
                            "evidence_url": evidence.image.url,
                        }
                        for evidence in evidences
                        if evidence.image
                    ],
                    "sns": list(maker.draftsns_set.values_list("address", flat=True)),
                    "language": list(maker.language.values_list("Language", flat=True)),
                    "category": list(maker.category.values_list("name", flat=True)),
                    "region": list(maker.region.values_list("region", flat=True)),
                    "bank": maker.bank,
                    "account_number": maker.account_number,
                    "account_holder": maker.account_holder,
                    "productform": maker.productform,
                    "tour": list(maker.tour.values_list("kind", flat=True)),
                }
                if DraftMaker_Drafttour.objects.filter(draftmaker_id=maker).exists():
                    result["limit_people"] = DraftMaker_Drafttour.objects.get(
                        draftmaker_id=maker
                    ).limit_people
                    result["limit_load"] = DraftMaker_Drafttour.objects.get(
                        draftmaker_id=maker
                    ).limit_load

                if maker.profile:
                    result["profile"] = base64.encodebytes(
                        open(maker.profile.path, "rb").read()
                    ).decode("utf-8")
                    result["profile_name"] = maker.profile.name
                    result["profile_url"] = maker.profile.url

                if maker.idcard:
                    result["idcard"] = base64.encodebytes(
                        open(maker.idcard.path, "rb").read()
                    ).decode("utf-8")
                    result["idcard_name"] = maker.idcard.name
                    result["idcard_url"] = maker.idcard.url

                if maker.bankbook_image:
                    result["bankbook"] = base64.encodebytes(
                        open(maker.bankbook_image.path, "rb").read()
                    ).decode("utf-8")
                    result["bankbook_name"] = maker.bankbook_image.name
                    result["bankbook_url"] = maker.bankbook_image.url

            return JsonResponse({"MESSAGE": result}, status=200)
        except Maker.DoesNotExist:
            return JsonResponse({"MESSAGE": "MAKERS DOES NOT EXIST"}, status=404)

    @login_decorator
    @transaction.atomic
    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.POST["data"])

            id = Maker.objects.get(user_id=user.id).id
            Maker.objects.get(id=id).delete()

            maker = Maker.objects.create(
                user_id=user.id,
                makername=data["makername"],
                makernickname=data["makernickname"],
                introduce=data["introduce"],
                bank=data.get("bank"),
                account_number=data.get("account_number"),
                account_holder=data.get("account_holder"),
                productform=data.get("productform"),
                profile=request.FILES["profile"],
                idcard=request.FILES["idcard"],
                bankbook_image=request.FILES.get("bankbook"),
            )

            if data.get("sns"):
                for sns in data["sns"]:
                    Sns.objects.create(
                        maker_id=maker.id,
                        address=sns,
                    )

            if data.get("evidence") and request.FILES.getlist("evidence"):
                for evidence, image in zip(
                    data["evidence"], request.FILES.getlist("evidence")
                ):
                    Evidence.objects.create(
                        kind=evidence, maker_id=maker.id, image=image
                    )

            if data.get("language"):
                for language in data["language"]:
                    Language.objects.get_or_create(Language=language)
                    maker.language.add(Language.objects.get(Language=language).id)

            if data.get("region"):
                for region in data["region"]:
                    Region.objects.get_or_create(region=region)
                    maker.region.add(Region.objects.get(region=region).id)

            if data.get("category"):
                for category in data["category"]:
                    Category.objects.get_or_create(name=category)
                    maker.category.add(Category.objects.get(name=category).id)

            if data.get("tour") == "차량투어":
                Maker_tour.objects.create(
                    maker_id=maker.id,
                    tour_id=Tour.objects.get(kind=data["tour"]).id,
                    limit_people=data.get("limit_people"),
                    limit_load=data.get("limit_load"),
                )

            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
        except Maker.DoesNotExist:
            return JsonResponse({"MESSAGE": "MAKERS DOES NOT EXISTS"}, status=404)
        except ValueError:
            return JsonResponse({"MESSAGE": "VALUE_ERROR"}, status=400)
