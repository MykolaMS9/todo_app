from .models import UserSettings


def set_cards_per_page(user, cards_per_page):
    UserSettings.objects.filter(user=user).update(cards_per_page=cards_per_page)
